from types import NoneType
from typing import List, Optional
# pyside
from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt


class ExplicitPrivelegesTableModel(QAbstractTableModel):
    def __init__(self, priveleges: Optional[List] = [], parent: NoneType = None) -> None:
        super(ExplicitPrivelegesTableModel, self).__init__(parent)
        self.priveleges = priveleges if priveleges else []
        self.priveleges_ordered = self.__order_priveleges(self.priveleges)
        self.header_labels = ["Object", "Any", "Inactive", "Active"]

    def rowCount(self, parent: QModelIndex = QModelIndex) -> int:
        """
        Reimplemented
        """
        try:
            return len(self.priveleges_ordered)
        except TypeError:
            return 0
        
    def columnCount(self, parent: QModelIndex = QModelIndex) -> int:
        """
        Reimplemented
        """
        return len(self.header_labels)
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Optional[int]:
        """
        Reimplemented
        """
        # for display purposes
        self.tr_header_labels = [self.tr("Object"),
                                 self.tr("Any"),
                                 self.tr("Inactive"),
                                 self.tr("Active")]
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.tr_header_labels[section]
        return super().headerData(section, orientation, role)
    
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Optional[List]:
        """
        Reimplemented
        """
        if not index.isValid():
            return None
        if not 0 <= index.row() <= len(self.priveleges_ordered):
            return None
        if role == Qt.DisplayRole:
            return self.priveleges_ordered[index.row()][index.column()]
        return None
    
    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole) -> bool:
        """
        Reimplemented
        """
        if role == Qt.EditRole:
            self.priveleges_ordered[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, (role,))
            return True
        return False

    def getItem(self, index: QModelIndex) -> List[str]:
        """
        Reimplemented
        """
        row = index.row()
        if index.isValid() and 0 <= row <= self.rowCount():
            return self.priveleges_ordered[row]
        
    def __order_priveleges(self, priveleges: List[str]) -> List[List[str]]:
        """
        Orders passed priveleges to format suitable for .pkla file
        """
        data = []
        for _privelege in priveleges:
            for privelege in _privelege:
                partial_data = []
                name = privelege[0]
                name = name.lstrip("[").rstrip("]")
                ug_objects = privelege[1]
                ug_objects_formated = []
                for ug_obj in ug_objects:
                    ug_obj = ug_obj.rstrip()
                    ug_obj = ug_obj.split("-")[-1]
                    ug_objects_formated.append(ug_obj)
                objects_to_str = ", ".join(ug_objects_formated)
                partial_data.append(objects_to_str)
                defaults = privelege[2]
                allow_any = defaults.get("allow_any")
                if not allow_any:
                    allow_any = ""
                partial_data.append(allow_any)
                allow_inactive = defaults.get("allow_inactive")
                if not allow_inactive:
                    allow_inactive = ""
                partial_data.append(allow_inactive)
                allow_active = defaults.get("allow_active")
                if not allow_active:
                    allow_active = ""
                partial_data.append(allow_active)
                partial_data.append(name)
                pkla_file = privelege[3]
                partial_data.append(pkla_file)
                data.append(partial_data) 
        return data