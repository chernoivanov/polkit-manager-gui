import os
import sys
# pyside
from PySide2.QtWidgets import QApplication
# module
from polkit_manager_gui.mainwindow import MainWindow


if __name__ == "__main__":
    # app
    app = QApplication()
    # main window
    main_window = MainWindow()
    main_window.rezise_window()
    main_window.show()
    # exit
    sys.exit(app.exec_())
