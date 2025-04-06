import os
import subprocess
from types import NoneType
from typing import List, Dict
# pyside
from PySide2.QtWidgets import QDialog, QListWidgetItem
from PySide2.QtCore import Qt, Slot
# module
from polkit_manager_gui.log.syslog import message_syslog
from polkit_manager_gui.ui.ui_addexplicitdialog import Ui_Dialog
from polkit_manager_gui.utils.pkla.handler import name_pkla_file, create_pkla_file
from polkit_manager_gui.widgets.listitemwidget import ListItemWidget


class AddExplicitPrivelegeDialog(QDialog):
    def __init__(self,
                 priveleges_values: Dict[str, str],
                 policy: str,
                 action: str,
                 parent: NoneType = None) -> None:
        super(AddExplicitPrivelegeDialog, self).__init__(parent)
        # UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # parameters
        self.priveleges_values = priveleges_values
        self.policy = policy
        self.action = action
        # setting additional UI
        self._set_ui_elements()
        # connect UI actions
        self._connect_actions()
        # get users
        self.users = self._list_objects("/etc/passwd")
        # get groups
        self.groups = self._list_objects("/etc/group")
        # combine users and groups for combobox
        self.total_items = [self.users, self.groups]
        # signals handling
        self.op_abort = False  # operation abort - close dialog without saving
        self.op_end = False  # operation finish, save process

    def _set_ui_elements(self) -> None:
        """
        Sets main UI elements
        """
        # priority
        self.ui.priority_spinbox.setValue(50)
        # comboboxes
        for combobox_obj in [(self.ui.any_user_combobox, "Any"),
                             (self.ui.inactive_sess_combobox, "Inactive"),
                             (self.ui.active_sess_combobox, "Active")]:
            combobox, name = combobox_obj
            combobox.clear()
            for value in list(self.priveleges_values.values()):
                combobox.addItem(value)
            combobox.setAccessibleName(name)
        # objects layout
        self.ui.add_button.setFixedSize(120, 30)
        self.ui.remove_button.setFixedSize(120, 30)
        self.ui.remove_button.setEnabled(False)
        self.ui.manage_h_layout.setAlignment(Qt.AlignRight)
        # buttons layout
        self.ui.save_button.setFixedSize(120, 30)
        self.ui.save_button.setEnabled(False)
        self.ui.abort_button.setFixedSize(120, 30)
        self.ui.buttons_h_layout.setAlignment(Qt.AlignRight)

    def _connect_actions(self) -> None:
        """
        Connects UI objects to call methods on action
        """
        self.ui.name_line_edit.textChanged.connect(self._manage_save_button)
        # manage objects
        self.ui.objects_list_view.currentRowChanged.connect(self._enable_remove_button)
        self.ui.add_button.clicked.connect(self._add_object)
        self.ui.remove_button.clicked.connect(self._remove_object)
        # manage exit buttons
        self.ui.save_button.clicked.connect(self._save)
        self.ui.abort_button.clicked.connect(self._abort)

    @Slot()
    def _add_object(self) -> None:
        """
        Adds new object of user or group to List Widget
        """
        item = QListWidgetItem(self.ui.objects_list_view)
        self.ui.objects_list_view.addItem(item)
        list_item_widget = ListItemWidget(self.total_items)
        item.setSizeHint(list_item_widget.minimumSizeHint())
        self.ui.objects_list_view.setItemWidget(item, list_item_widget)
        if self.ui.objects_list_view.count() and self.ui.name_line_edit.text():
            self.ui.save_button.setEnabled(True)

    @Slot()
    def _remove_object(self) -> None:
        """
        Removes chosen object of user or group from List Widget
        """
        self.ui.objects_list_view.takeItem(self.ui.objects_list_view.currentRow())
        if self.ui.objects_list_view.currentRow() < 0:
            self.ui.remove_button.setEnabled(False)
            self.ui.save_button.setEnabled(False)

    @Slot()
    def _save(self) -> None:
        """
        Applies and saves new explicit priveleges
        """
        items = [self.ui.objects_list_view.item(index) for index in range(self.ui.objects_list_view.count())]
        objects = []
        for item in items:
            widget = self.ui.objects_list_view.itemWidget(item)
            if widget:
                objects.append((widget.source_combobox.currentIndex(), widget.object_combobox.currentText()))
        name = self.ui.name_line_edit.text()
        priority = self.ui.priority_spinbox.value()
        defaults_to_be_saved = {}
        for combobox_obj in [(self.ui.any_user_combobox, "allow_any"),
                             (self.ui.inactive_sess_combobox, "allow_inactive"),
                             (self.ui.active_sess_combobox, "allow_active")]:
            combobox, key = combobox_obj
            try:
                implicit_priv = list(self.priveleges_values.keys())[list(self.priveleges_values.values()).index(combobox.currentText())]
            except ValueError:
                implicit_priv = ""
            defaults_to_be_saved[key] = implicit_priv
        saving_file_path = name_pkla_file(priority, self.policy)
        file_contents = create_pkla_file(name, self.action, defaults_to_be_saved, objects)
        if os.path.exists(saving_file_path):
            mode = "a"
            file_contents.insert(0, "\n")
        else:
            mode = "w"
        with open(saving_file_path, mode) as _pkla_file:
            _pkla_file.writelines(file_contents)
        self.op_end = True
        if not self.op_abort:
            privelege_to_list = []
            for key, value in defaults_to_be_saved.items():
                if value:
                    privelege_to_list.append(f"{key}: {value}") 
            objects_to_list = []
            for _object in objects:
                _type, _name = _object
                if _type == 0:
                    _type_name = "unix-user"
                elif _type == 1:
                    _type_name = "unix-group"
                objects_to_list.append(f"{_type_name}: {_name}")
            objects_to_string = ", ".join(objects_to_list)
            privelege_to_string = ", ".join(privelege_to_list)
            msg = self.tr("For policy [{}] (action: [{}]) explicit priveleges were added: [{}], [{}], {}").format(self.policy,
                                                                                                                  self.action,
                                                                                                                  privelege_to_string,
                                                                                                                  objects_to_string,
                                                                                                                  name)
            message_syslog(msg)
        self.close()

    @Slot()
    def _abort(self) -> None:
        """
        Aborts process and closes dialog window
        """
        self.op_abort = True
        self.close()
    
    @Slot()
    def _enable_remove_button(self) -> None:
        """
        Enables Remove button
        """
        self.ui.remove_button.setEnabled(True)

    @Slot(str)
    def _manage_save_button(self, text: str) -> None:
        """
        Enables or disables Save button based on state of text and quantity of objects in List Widget
        """
        if text and self.ui.objects_list_view.count():
            self.ui.save_button.setEnabled(True)
        else:
            self.ui.save_button.setEnabled(False)

    def _list_objects(self, path: str) -> List[str]:
        """
        Lists found objects with path passed
        """
        call_output = subprocess.run(["cat", path], capture_output=True, text=True)
        objects = [_object.split(":")[0] for _object in call_output.stdout.split("\n")]
        return objects
