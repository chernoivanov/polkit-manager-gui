# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.13
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

import polkit_manager_gui.resources.resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1088, 590)
        self.action_quit = QAction(MainWindow)
        self.action_quit.setObjectName(u"action_quit")
        icon = QIcon()
        icon.addFile(u":/resources/quit.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_quit.setIcon(icon)
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        icon1 = QIcon()
        icon1.addFile(u":/resources/info.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_about.setIcon(icon1)
        self.action_expand_tree = QAction(MainWindow)
        self.action_expand_tree.setObjectName(u"action_expand_tree")
        icon2 = QIcon()
        icon2.addFile(u":/resources/expand.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_expand_tree.setIcon(icon2)
        self.action_collapse_tree = QAction(MainWindow)
        self.action_collapse_tree.setObjectName(u"action_collapse_tree")
        icon3 = QIcon()
        icon3.addFile(u":/resources/collapse.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_collapse_tree.setIcon(icon3)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.v_separator = QFrame(self.centralwidget)
        self.v_separator.setObjectName(u"v_separator")
        self.v_separator.setFrameShape(QFrame.HLine)
        self.v_separator.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.v_separator, 2, 0, 1, 1)

        self.policies_tree_view = QTreeView(self.centralwidget)
        self.policies_tree_view.setObjectName(u"policies_tree_view")
        font = QFont()
        font.setPointSize(13)
        self.policies_tree_view.setFont(font)
        self.policies_tree_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.policies_tree_view.setProperty("showDropIndicator", False)
        self.policies_tree_view.header().setVisible(False)

        self.gridLayout.addWidget(self.policies_tree_view, 1, 0, 1, 1)

        self.filter_line_edit = QLineEdit(self.centralwidget)
        self.filter_line_edit.setObjectName(u"filter_line_edit")
        self.filter_line_edit.setClearButtonEnabled(True)

        self.gridLayout.addWidget(self.filter_line_edit, 0, 0, 1, 1)

        self.priveleges_h_layout = QHBoxLayout()
        self.priveleges_h_layout.setSpacing(7)
        self.priveleges_h_layout.setObjectName(u"priveleges_h_layout")
        self.priveleges_h_layout.setContentsMargins(-1, 0, 0, -1)
        self.explicit_v_layout = QVBoxLayout()
        self.explicit_v_layout.setObjectName(u"explicit_v_layout")
        self.explicit_v_layout.setContentsMargins(0, -1, -1, -1)
        self.explicit_label = QLabel(self.centralwidget)
        self.explicit_label.setObjectName(u"explicit_label")
        self.explicit_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.explicit_label.setIndent(5)

        self.explicit_v_layout.addWidget(self.explicit_label)

        self.explicit_inner_h_layout = QHBoxLayout()
        self.explicit_inner_h_layout.setObjectName(u"explicit_inner_h_layout")
        self.explicit_inner_h_layout.setContentsMargins(-1, -1, 0, -1)
        self.explicit_table_view = QTableView(self.centralwidget)
        self.explicit_table_view.setObjectName(u"explicit_table_view")

        self.explicit_inner_h_layout.addWidget(self.explicit_table_view)

        self.explicit_buttons_v_layout = QVBoxLayout()
        self.explicit_buttons_v_layout.setObjectName(u"explicit_buttons_v_layout")
        self.explicit_buttons_v_layout.setContentsMargins(-1, -1, 0, -1)
        self.add_button = QPushButton(self.centralwidget)
        self.add_button.setObjectName(u"add_button")
        icon4 = QIcon()
        icon4.addFile(u":/resources/add.png", QSize(), QIcon.Normal, QIcon.Off)
        self.add_button.setIcon(icon4)

        self.explicit_buttons_v_layout.addWidget(self.add_button)

        self.remove_button = QPushButton(self.centralwidget)
        self.remove_button.setObjectName(u"remove_button")
        icon5 = QIcon()
        icon5.addFile(u":/resources/remove.png", QSize(), QIcon.Normal, QIcon.Off)
        self.remove_button.setIcon(icon5)

        self.explicit_buttons_v_layout.addWidget(self.remove_button)


        self.explicit_inner_h_layout.addLayout(self.explicit_buttons_v_layout)


        self.explicit_v_layout.addLayout(self.explicit_inner_h_layout)


        self.priveleges_h_layout.addLayout(self.explicit_v_layout)

        self.h_separator = QFrame(self.centralwidget)
        self.h_separator.setObjectName(u"h_separator")
        self.h_separator.setFrameShape(QFrame.VLine)
        self.h_separator.setFrameShadow(QFrame.Sunken)

        self.priveleges_h_layout.addWidget(self.h_separator)

        self.implicit_v_layout = QVBoxLayout()
        self.implicit_v_layout.setSpacing(10)
        self.implicit_v_layout.setObjectName(u"implicit_v_layout")
        self.implicit_v_layout.setContentsMargins(0, 0, -1, 0)
        self.implicit_label = QLabel(self.centralwidget)
        self.implicit_label.setObjectName(u"implicit_label")
        self.implicit_label.setLineWidth(1)
        self.implicit_label.setTextFormat(Qt.AutoText)
        self.implicit_label.setIndent(5)

        self.implicit_v_layout.addWidget(self.implicit_label)

        self.any_user_h_layout = QHBoxLayout()
        self.any_user_h_layout.setSpacing(50)
        self.any_user_h_layout.setObjectName(u"any_user_h_layout")
        self.any_user_h_layout.setContentsMargins(-1, 0, 10, -1)
        self.any_user_label = QLabel(self.centralwidget)
        self.any_user_label.setObjectName(u"any_user_label")

        self.any_user_h_layout.addWidget(self.any_user_label)

        self.any_user_combobox = QComboBox(self.centralwidget)
        self.any_user_combobox.setObjectName(u"any_user_combobox")

        self.any_user_h_layout.addWidget(self.any_user_combobox)

        self.any_user_h_layout.setStretch(0, 1)
        self.any_user_h_layout.setStretch(1, 2)

        self.implicit_v_layout.addLayout(self.any_user_h_layout)

        self.inactive_sess_h_layout = QHBoxLayout()
        self.inactive_sess_h_layout.setSpacing(50)
        self.inactive_sess_h_layout.setObjectName(u"inactive_sess_h_layout")
        self.inactive_sess_h_layout.setContentsMargins(-1, 0, 10, -1)
        self.inactive_sess_label = QLabel(self.centralwidget)
        self.inactive_sess_label.setObjectName(u"inactive_sess_label")

        self.inactive_sess_h_layout.addWidget(self.inactive_sess_label)

        self.inactive_sess_combobox = QComboBox(self.centralwidget)
        self.inactive_sess_combobox.setObjectName(u"inactive_sess_combobox")

        self.inactive_sess_h_layout.addWidget(self.inactive_sess_combobox)

        self.inactive_sess_h_layout.setStretch(0, 1)
        self.inactive_sess_h_layout.setStretch(1, 2)

        self.implicit_v_layout.addLayout(self.inactive_sess_h_layout)

        self.active_sess_h_layout = QHBoxLayout()
        self.active_sess_h_layout.setSpacing(50)
        self.active_sess_h_layout.setObjectName(u"active_sess_h_layout")
        self.active_sess_h_layout.setContentsMargins(-1, 0, 10, -1)
        self.active_sess_label = QLabel(self.centralwidget)
        self.active_sess_label.setObjectName(u"active_sess_label")

        self.active_sess_h_layout.addWidget(self.active_sess_label)

        self.active_sess_combobox = QComboBox(self.centralwidget)
        self.active_sess_combobox.setObjectName(u"active_sess_combobox")

        self.active_sess_h_layout.addWidget(self.active_sess_combobox)

        self.active_sess_h_layout.setStretch(0, 1)
        self.active_sess_h_layout.setStretch(1, 2)

        self.implicit_v_layout.addLayout(self.active_sess_h_layout)

        self.save_button_h_layout = QHBoxLayout()
        self.save_button_h_layout.setObjectName(u"save_button_h_layout")
        self.save_button_h_layout.setContentsMargins(-1, -1, 10, 0)
        self.save_button = QPushButton(self.centralwidget)
        self.save_button.setObjectName(u"save_button")
        icon6 = QIcon()
        icon6.addFile(u":/resources/save.png", QSize(), QIcon.Normal, QIcon.Off)
        self.save_button.setIcon(icon6)

        self.save_button_h_layout.addWidget(self.save_button)


        self.implicit_v_layout.addLayout(self.save_button_h_layout)

        self.implicit_v_layout.setStretch(0, 1)
        self.implicit_v_layout.setStretch(1, 4)
        self.implicit_v_layout.setStretch(2, 4)
        self.implicit_v_layout.setStretch(3, 4)

        self.priveleges_h_layout.addLayout(self.implicit_v_layout)

        self.priveleges_h_layout.setStretch(0, 1)
        self.priveleges_h_layout.setStretch(2, 1)

        self.gridLayout.addLayout(self.priveleges_h_layout, 3, 0, 1, 1)

        self.bottom_line = QFrame(self.centralwidget)
        self.bottom_line.setObjectName(u"bottom_line")
        self.bottom_line.setFrameShape(QFrame.HLine)
        self.bottom_line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.bottom_line, 4, 0, 1, 1)

        self.gridLayout.setRowStretch(1, 10)
        self.gridLayout.setRowStretch(3, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1088, 23))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuActions = QMenu(self.menubar)
        self.menuActions.setObjectName(u"menuActions")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuActions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.action_quit)
        self.menuActions.addAction(self.action_expand_tree)
        self.menuActions.addAction(self.action_collapse_tree)
        self.menuHelp.addAction(self.action_about)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Polkit Manager", None))
        self.action_quit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
#if QT_CONFIG(shortcut)
        self.action_quit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.action_expand_tree.setText(QCoreApplication.translate("MainWindow", u"Expand tree", None))
        self.action_collapse_tree.setText(QCoreApplication.translate("MainWindow", u"Collapse tree", None))
        self.filter_line_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Filter", None))
        self.explicit_label.setText(QCoreApplication.translate("MainWindow", u"Explicit Priveleges", None))
        self.add_button.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.remove_button.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.implicit_label.setText(QCoreApplication.translate("MainWindow", u"Implicit Priveleges", None))
        self.any_user_label.setText(QCoreApplication.translate("MainWindow", u"Any user", None))
        self.inactive_sess_label.setText(QCoreApplication.translate("MainWindow", u"Inactive session", None))
        self.active_sess_label.setText(QCoreApplication.translate("MainWindow", u"Active session", None))
        self.save_button.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuActions.setTitle(QCoreApplication.translate("MainWindow", u"Actions", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

