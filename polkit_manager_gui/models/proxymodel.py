# pyside
from PySide2.QtCore import QSortFilterProxyModel, Qt, QRegExp, QModelIndex


class FilterProxyModel(QSortFilterProxyModel):
    def setFilterRegExp(self, pattern: QRegExp) -> None:
        """
        Reimplemented
        """
        if isinstance(pattern, str):
            pattern = QRegExp(pattern, Qt.CaseInsensitive, QRegExp.FixedString)
        super(FilterProxyModel, self).setFilterRegExp(pattern)
    
    def _accept_index(self, index: QModelIndex) -> bool:
        """
        Validates index passed
        """
        if index.isValid():
            text = index.data(Qt.DisplayRole)
            if self.filterRegExp().indexIn(text) >= 0:
                return True
            for row in range(index.model().rowCount(index)):
                if self._accept_index(index.model().index(row, 0, index)):
                    return True
        return False
        
    def filterAcceptsRow(self, sourceRow: int, sourceParent: QModelIndex) -> bool:
        """
        Reimplemented
        """
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        return self._accept_index(index)
