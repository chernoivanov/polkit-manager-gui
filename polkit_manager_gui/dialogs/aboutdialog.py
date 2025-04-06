# pyside
from PySide2.QtWidgets import QDialog
# module
from polkit_manager_gui.ui.ui_aboutdialog import Ui_Dialog
from polkit_manager_gui.utils.version import VERSION


class AboutDialog(QDialog):
    def __init__(self, parent = None) -> None:
        super(AboutDialog, self).__init__(parent)
        # UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self._set_ui_elements()

    def _set_ui_elements(self) -> None:
        """
        Sets texts for labels used
        """
        # title label
        self.ui.title_label.setText(self.tr("Polkit Manager GUI"))
        # version label
        self.ui.version_label.setText(self.tr("Version: {}").format(VERSION))
        # description label
        description = self.tr("Utility is developed for managing polkit priveleges")
        self.ui.description_label.setText(description)
