from typing import List
from types import NoneType
# pyside
from PySide2.QtWidgets import QWidget, QHBoxLayout, QComboBox
from PySide2.QtCore import Slot


class ListItemWidget(QWidget):
    def __init__(self, total_items: List, parent: NoneType = None) -> None:
        super(ListItemWidget, self).__init__(parent)
        self.total_items = total_items
        self.total_sources = [self.tr("Users"), self.tr("Groups")]
        self.row = QHBoxLayout()
        # sources
        self.source_combobox = QComboBox()
        self.source_combobox.addItems(self.total_sources)
        self.source_combobox.currentIndexChanged.connect(self._update_combobox_objects)
        self.row.addWidget(self.source_combobox)
        # objects
        self.object_combobox = QComboBox()
        self.object_combobox.addItems(self.total_items[0])
        self.row.addWidget(self.object_combobox)
        # final layout
        self.setLayout(self.row)

    @Slot(int)
    def _update_combobox_objects(self, index: int) -> None:
        """
        Updates <object_combobox> widget with index passed
        """
        self.object_combobox.clear()
        self.object_combobox.addItems(self.total_items[index])