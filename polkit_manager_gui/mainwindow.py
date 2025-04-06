import os
import re
from typing import List
from types import NoneType
# pyside
from PySide2.QtWidgets import QMainWindow, QLabel, QAbstractItemView, QHeaderView, QMessageBox
from PySide2.QtCore import QEvent, QSettings, Qt, Slot, QModelIndex
from PySide2.QtGui import QStandardItemModel, QStandardItem, QFont, QPalette, QColor, QIcon, QPixmap
# module: dialogs
from polkit_manager_gui.dialogs.aboutdialog import AboutDialog
from polkit_manager_gui.dialogs.addexplicitdialog import AddExplicitPrivelegeDialog
# module: log
from polkit_manager_gui.log.syslog import message_syslog
# module: models
from polkit_manager_gui.models.explicitprivtablemodel import ExplicitPrivelegesTableModel
from polkit_manager_gui.models.proxymodel import FilterProxyModel
# module: ui
from polkit_manager_gui.ui.ui_mainwindow import Ui_MainWindow
# module: utils
from polkit_manager_gui.utils.paths import size_pos_settings_path
from polkit_manager_gui.utils.pkla.handler import remove_explicit_privelege
from polkit_manager_gui.utils.pkla.parser import parse_polkit_localauthority
from polkit_manager_gui.utils.xml.handler import get_policies, change_actions_defaults


class MainWindow(QMainWindow):
    def __init__(self, parent: NoneType = None) -> None:
        super(MainWindow, self).__init__(parent)
        # main window initial activation
        self.initial_activation = True
        # UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # policies init
        self.policies = {}
        # explicit priveleges init
        self.explicit_priveleges = {}
        # polkit tree model
        self.polkit_tree_model = FilterProxyModel()
        self.polkit_tree_model.setRecursiveFilteringEnabled(True)
        self.polkit_tree_model.setSourceModel(QStandardItemModel(self.ui.policies_tree_view))
        # explicit priveleges model
        self.explicit_priveleges_table_model = ExplicitPrivelegesTableModel(self.explicit_priveleges)
        self.ui.explicit_table_view.setModel(self.explicit_priveleges_table_model)
        # setting additional UI
        self._set_ui_elements()
        # connect UI actions
        self._connect_actions()
        # dict of priveleges values to display properly
        self.priveleges_values = {"no": self.tr("Forbid"),
                                  "yes": self.tr("Allow"),
                                  "auth_self": self.tr("Authentication"),
                                  "auth_admin": self.tr("Admin authentication"),
                                  "auth_self_keep": self.tr("Authentication (keep)"),
                                  "auth_admin_keep": self.tr("Admin authentication (keep)")}
        # objects that are currently on focus
        self.defaults_on_focus = None
        self.explicit_privelege_on_focus = None

    def _set_ui_elements(self) -> None:
        """
        Sets main UI elements such as fonts, alignments and buttons' availability at the start
        """
        # set app icon
        self.setWindowIcon(QIcon(":/resources/privacy-policy.png"))
        # policies tree view
        self.ui.policies_tree_view.setModel(self.polkit_tree_model)
        # fonts
        bold_font = QFont()
        italic_font = QFont()
        bold_font.setBold(True)
        italic_font.setItalic(True)
        # implicit layout
        self.ui.implicit_label.setFont(bold_font)  # main implicit layout label
        self.ui.any_user_label.setFont(italic_font)  # any_user layout
        self.ui.inactive_sess_label.setFont(italic_font)  # inactive session layout
        self.ui.active_sess_label.setFont(italic_font)  # active session layout
        # disable implicit comboboxes until any policy is chosen
        self.ui.any_user_combobox.setEnabled(False)
        self.ui.inactive_sess_combobox.setEnabled(False)
        self.ui.active_sess_combobox.setEnabled(False)
        self.ui.save_button.setFixedSize(120, 30)  # save push button
        self.ui.save_button_h_layout.setAlignment(Qt.AlignRight)
        self.ui.save_button.setEnabled(False)  # disable button until changes captured
        # explicit layout
        self.ui.explicit_label.setFont(bold_font)  # main explicit layout label
        # explicit priveleges table view headers
        self.ui.explicit_table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.explicit_table_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        # disable buttons until changes captured
        self.ui.add_button.setEnabled(False)
        self.ui.remove_button.setEnabled(False)

    def _connect_actions(self) -> None:
        """
        Connects UI objects to call methods on action
        """
        # menu: file
        self.ui.action_quit.triggered.connect(self._quit)
        # menu: actions
        self.ui.action_expand_tree.triggered.connect(self.ui.policies_tree_view.expandAll)
        self.ui.action_collapse_tree.triggered.connect(self.ui.policies_tree_view.collapseAll)
        # menu: help
        self.ui.action_about.triggered.connect(self._show_about)
        # filter line edit
        self.ui.filter_line_edit.textChanged.connect(self._filter_tree_view)
        # policies tree view
        self.ui.policies_tree_view.clicked.connect(self._display_implicit_priveleges)
        # implicit layout objects
        self.ui.save_button.clicked.connect(self._save_new_implicit_state)
        # explicit layout objects
        self.ui.explicit_table_view.clicked.connect(self._get_explicit_privelege)
        self.ui.add_button.clicked.connect(self._add_new_explicit_privelege)
        self.ui.remove_button.clicked.connect(self._remove_existing_explicit_privelege)

    @Slot(str)
    def _filter_tree_view(self, text: str) -> None:
        """
        Filters policykit tree model view based on given text from filter line edit
        """
        self.polkit_tree_model.setFilterRegExp(text)
        self.ui.policies_tree_view.setModel(self.polkit_tree_model)

    @Slot(QModelIndex)
    def _display_implicit_priveleges(self, index: QModelIndex) -> None:
        """
        Updates UI objects of both implicit and explicit blocks based on current policykit
        action on focus

        """
        self.ui.remove_button.setEnabled(False)  # confirm button stays disabled when policy focus changes
        model = self.polkit_tree_model.sourceModel()
        try:
            item = model.itemFromIndex(index)
            item_name = item.text()
        except AttributeError:
            index = self.polkit_tree_model.mapToSource(index)
            item = model.itemFromIndex(index)
            item_name = item.text()
        self.current_item_on_focus = item
        parent = self.current_item_on_focus.parent()
        if parent:
            self.ui.add_button.setEnabled(True)
            for combobox_obj in [(self.ui.any_user_combobox, "Any"),
                                 (self.ui.inactive_sess_combobox, "Inactive"),
                                 (self.ui.active_sess_combobox, "Active")]:
                combobox, name = combobox_obj
                combobox.clear()
                for value in list(self.priveleges_values.values()):
                    combobox.addItem(value)
                combobox.setAccessibleName(name)
                combobox.activated.connect(self._activate_combobox_change)
            # palettes
            palette_disabled = QLabel().palette()
            palette_disabled.setColor(QPalette.WindowText, QColor("grey"))
            palette_enabled = QLabel().palette()
            palette_enabled.setColor(QPalette.WindowText, self.ui.implicit_label.palette().color(QPalette.WindowText))
            # manage policy's <defaults>
            parent_attributes = self.policies.get(parent.text())
            actions = parent_attributes.get("actions")
            defaults = actions.get(item_name).get("defaults")
            self.defaults_on_focus = defaults
            self.changed_defaults = self.defaults_on_focus.copy()
            # <allow_any> tag
            allow_any = defaults.get("allow_any")
            if allow_any:
                self.ui.any_user_label.setPalette(palette_enabled)
                self.ui.any_user_combobox.setCurrentText(self.priveleges_values.get(allow_any))
                self.ui.any_user_combobox.setEnabled(True)
            else:
                self.ui.any_user_label.setPalette(palette_disabled)
                self.ui.any_user_combobox.clear()
                self.ui.any_user_combobox.setEnabled(False)
            # <allow_inactive> tag
            allow_inactive = defaults.get("allow_inactive")
            if allow_inactive:
                self.ui.inactive_sess_label.setPalette(palette_enabled)
                self.ui.inactive_sess_combobox.setCurrentText(self.priveleges_values.get(allow_inactive))
                self.ui.inactive_sess_combobox.setEnabled(True)
            else:
                self.ui.inactive_sess_label.setPalette(palette_disabled)
                self.ui.inactive_sess_combobox.clear()
                self.ui.inactive_sess_combobox.setEnabled(False)
            # <allow_active> tag
            allow_active = defaults.get("allow_active")
            if allow_active:
                self.ui.active_sess_label.setPalette(palette_enabled)
                self.ui.active_sess_combobox.setCurrentText(self.priveleges_values.get(allow_active))
                self.ui.active_sess_combobox.setEnabled(True)
            else:
                self.ui.active_sess_label.setPalette(palette_disabled)
                self.ui.active_sess_combobox.clear()
                self.ui.active_sess_combobox.setEnabled(False)
            # manage table view
            explicit_priveleges = self._filter_explicit_priveleges(item_name)
            self.explicit_priveleges_table_model = ExplicitPrivelegesTableModel(explicit_priveleges)
            self.ui.explicit_table_view.setModel(self.explicit_priveleges_table_model)
        else:  # not a single policy is on focus
            self.ui.add_button.setEnabled(False)
            # clear comboboxes
            for combobox in [self.ui.any_user_combobox, self.ui.inactive_sess_combobox, self.ui.active_sess_combobox]:
                combobox.clear()

    def _activate_combobox_change(self) -> None:
        """
        Sets changes made in any of combobox obejects to class attribute vars and
        enables saving of changes
        """
        sender = self.sender()
        combobox_name = sender.accessibleName()
        changed_text = sender.currentText()
        implicit_key = list(self.priveleges_values.keys())[list(self.priveleges_values.values()).index(changed_text)]
        match combobox_name:
            case "Any": key = "allow_any"
            case "Inactive": key = "allow_inactive"
            case "Active": key = "allow_active"
            case _: key = None
        if key:
            self.changed_defaults[key] = implicit_key
        if self.defaults_on_focus == self.changed_defaults:  # in case the actual state of <defaults> did not change
            self.ui.save_button.setEnabled(False)
        else:
            self.ui.save_button.setEnabled(True)

    @Slot(QModelIndex)
    def _get_explicit_privelege(self, index: QModelIndex) -> None:
        """
        Gets current explicit privelege on focus and sets to class attribute var
        """
        explicit_privelege = self.explicit_priveleges_table_model.getItem(index)
        self.explicit_privelege_on_focus = (explicit_privelege, index)
        self.ui.remove_button.setEnabled(True)

    def _filter_explicit_priveleges(self, item_name: str) -> List[str]:
        """
        Filters explicit priveleges for table view
        """
        explicit_priveleges_objects = []
        for explicit_privelege_key in self.explicit_priveleges.keys():
            search_object = re.search(explicit_privelege_key, item_name)
            if search_object:
                explicit_priveleges_objects.append(self.explicit_priveleges.get(explicit_privelege_key))
        return explicit_priveleges_objects
    
    @Slot()
    def _save_new_implicit_state(self) -> None:
        """
        Applies and saves changes made to current action on focus
        """
        policy = self.current_item_on_focus.parent().text()
        action = self.current_item_on_focus.text()
        op_status, poss_err = change_actions_defaults(policy, action, self.changed_defaults)
        op_msg = QMessageBox()
        op_msg.setWindowTitle(self.tr("Saving implicit priveleges"))
        op_msg.setWindowIcon(QIcon(":/resources/save.png"))
        if op_status:  # True
            self.defaults_on_focus = self.changed_defaults.copy()
            op_msg.setIcon(QMessageBox.Information)
            op_msg.setText(self.tr("Implicit priveleges for {} ({}) were successfully changed").format(policy, action))
        else:  # op_status = False
            op_msg.setIcon(QMessageBox.Critical)
            op_msg.setText(self.tr("Error occured while saving changes made to implicit priveleges"))
            if poss_err:
                op_msg.setInformativeText(poss_err)
        op_msg.exec_()
        self.ui.save_button.setEnabled(False)
        self.policies = get_policies()  # ?

    @Slot()
    def _add_new_explicit_privelege(self) -> None:
        """
        Calls and shows Dialog where user fill forms to create new explicit priveleges
        Shows message after (depends on result, messages differ)
        """
        add_explicit_dialog = AddExplicitPrivelegeDialog(self.priveleges_values,
                                                         self.current_item_on_focus.parent().text(),
                                                         self.current_item_on_focus.text())
        add_explicit_dialog.exec_()
        op_abort = add_explicit_dialog.op_abort
        op_end = add_explicit_dialog.op_end
        op_msg = QMessageBox()
        op_msg.setWindowTitle(self.tr("Saving new explicit priveleges"))
        op_msg.setWindowIcon(QIcon(":/resources/save.png"))
        if not op_abort and op_end:
            op_msg.setIcon(QMessageBox.Information)
            op_msg.setText(self.tr("New explicit priveleges were successfully added"))
            self.explicit_priveleges = parse_polkit_localauthority()
            upd_explicit_table_objects = self._filter_explicit_priveleges(self.current_item_on_focus.text())
            self.explicit_priveleges_table_model = ExplicitPrivelegesTableModel(upd_explicit_table_objects)
            self.ui.explicit_table_view.setModel(self.explicit_priveleges_table_model)
        else:
            op_msg.setIcon(QMessageBox.Warning)
            op_msg.setText(self.tr("Something went wrong, changes are not applied"))
        op_msg.exec_()


    @Slot()
    def _remove_existing_explicit_privelege(self) -> None:
        """
        Removes explicit priveleges on focus
        Shows message after (depends on result, messages differ)
        """
        privelege, _ = self.explicit_privelege_on_focus
        action = self.current_item_on_focus.text()
        op_result, op_error = remove_explicit_privelege(privelege[-1], privelege[-2], action)
        op_msg = QMessageBox()
        op_msg.setWindowTitle(self.tr("Removing explicit priveleges"))
        op_msg.setWindowIcon(QIcon(":/resources/remove.png"))
        if op_result:
            policy = self.current_item_on_focus.parent().text()
            subject_items = privelege[0]
            allow_any = f"allow_any: {privelege[1]}" if privelege[1] else None
            allow_inactive = f"allow_inactive: {privelege[2]}" if privelege[2] else None
            allow_active = f"allow_active: {privelege[3]}" if privelege[3] else None
            priveleges_to_list = []
            for privelege in [allow_any, allow_inactive, allow_active]:
                if privelege:
                    priveleges_to_list.append(privelege)
            priveleges_to_str = ", ".join(priveleges_to_list)
            name = privelege[4]
            msg = self.tr("For policy [{}] (action: [{}]) explicit priveleges were added: [{}], [{}], {}").format(policy,
                                                                                                                  action,
                                                                                                                  priveleges_to_str,
                                                                                                                  subject_items,
                                                                                                                  name)
            message_syslog(msg)
            op_msg.setIcon(QMessageBox.Information)
            op_msg.setText(self.tr("Explicit priveleges were successfully removed"))
        else:
            op_msg.setIcon(QMessageBox.Critical)
            op_msg.setText(self.tr("Error occured while removing explicit priveleges"))
            op_msg.setInformativeText(op_error)
        op_msg.exec_()
        self.explicit_priveleges = parse_polkit_localauthority()
        upd_explicit_table_objects = self._filter_explicit_priveleges(self.current_item_on_focus.text())
        self.explicit_priveleges_table_model = ExplicitPrivelegesTableModel(upd_explicit_table_objects)
        self.ui.explicit_table_view.setModel(self.explicit_priveleges_table_model)
        self.ui.remove_button.setEnabled(False)
    
    @Slot()
    def _show_about(self) -> None:
        """
        Shows dialog with brief information about utility
        """
        about_dialog = AboutDialog()
        about_dialog.exec_()
    
    @Slot()
    def _quit(self) -> None:
        """
        Closes utility
        """
        self.close()
        
    def rezise_window(self) -> None:
        """
        Restores previous sizes of main window
        """
        if os.path.exists(size_pos_settings_path):
            settings_object = QSettings(size_pos_settings_path, QSettings.IniFormat)
            self.restoreGeometry(settings_object.value("windowGeometry"))
    
    def event(self, event) -> bool:
        """
        Handles all of the events captured during the run of utility
        """
        if event.type() == QEvent.WindowActivate and self.initial_activation:
            self.initial_activation = False
            self.policies = get_policies()
            model = self.polkit_tree_model.sourceModel()
            for policy, attributes in self.policies.items():
                item = QStandardItem(policy)
                item.setIcon(QIcon(":/resources/policy.png"))
                model.appendRow(item)
                for action in attributes["actions"]:
                    child = QStandardItem(action)
                    child.setIcon(QIcon(":/resources/action.png"))
                    item.appendRow(child)
                self.ui.policies_tree_view.setModel(model)
                self.polkit_tree_model.setFilterRegExp("")
            self.explicit_priveleges = parse_polkit_localauthority()
        # save changed windowGeometry
        elif event.type() == QEvent.Close:
            settings_object = QSettings(size_pos_settings_path, QSettings.IniFormat)
            settings_object.setValue("windowGeometry", self.saveGeometry())
        return super().event(event)
