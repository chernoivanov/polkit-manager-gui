# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'addexplicitdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.13
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

import polkit_manager_gui.resources.resources_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(875, 549)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.dialog_label = QLabel(Dialog)
        self.dialog_label.setObjectName(u"dialog_label")
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.dialog_label.setFont(font)
        self.dialog_label.setMargin(5)
        self.dialog_label.setIndent(-1)

        self.gridLayout.addWidget(self.dialog_label, 0, 0, 1, 1)

        self.manage_h_layout = QHBoxLayout()
        self.manage_h_layout.setObjectName(u"manage_h_layout")
        self.manage_h_layout.setContentsMargins(5, 5, 5, 5)
        self.manage_label = QLabel(Dialog)
        self.manage_label.setObjectName(u"manage_label")
        self.manage_label.setIndent(10)

        self.manage_h_layout.addWidget(self.manage_label)

        self.add_button = QPushButton(Dialog)
        self.add_button.setObjectName(u"add_button")
        icon = QIcon()
        icon.addFile(u":/resources/add.png", QSize(), QIcon.Normal, QIcon.Off)
        self.add_button.setIcon(icon)

        self.manage_h_layout.addWidget(self.add_button)

        self.remove_button = QPushButton(Dialog)
        self.remove_button.setObjectName(u"remove_button")
        icon1 = QIcon()
        icon1.addFile(u":/resources/remove.png", QSize(), QIcon.Normal, QIcon.Off)
        self.remove_button.setIcon(icon1)
        self.remove_button.setIconSize(QSize(16, 16))

        self.manage_h_layout.addWidget(self.remove_button)

        self.manage_h_layout.setStretch(0, 1)
        self.manage_h_layout.setStretch(1, 2)
        self.manage_h_layout.setStretch(2, 2)

        self.gridLayout.addLayout(self.manage_h_layout, 10, 0, 1, 1)

        self.priority_h_layout = QHBoxLayout()
        self.priority_h_layout.setObjectName(u"priority_h_layout")
        self.priority_h_layout.setContentsMargins(5, 5, 5, 5)
        self.priority_label = QLabel(Dialog)
        self.priority_label.setObjectName(u"priority_label")
        self.priority_label.setIndent(10)

        self.priority_h_layout.addWidget(self.priority_label)

        self.priority_spinbox = QSpinBox(Dialog)
        self.priority_spinbox.setObjectName(u"priority_spinbox")

        self.priority_h_layout.addWidget(self.priority_spinbox)


        self.gridLayout.addLayout(self.priority_h_layout, 3, 0, 1, 1)

        self.line_2 = QFrame(Dialog)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_2, 4, 0, 1, 1)

        self.buttons_h_layout = QHBoxLayout()
        self.buttons_h_layout.setObjectName(u"buttons_h_layout")
        self.buttons_h_layout.setContentsMargins(5, 5, 5, 5)
        self.save_button = QPushButton(Dialog)
        self.save_button.setObjectName(u"save_button")
        icon2 = QIcon()
        icon2.addFile(u":/resources/save.png", QSize(), QIcon.Normal, QIcon.Off)
        self.save_button.setIcon(icon2)

        self.buttons_h_layout.addWidget(self.save_button)

        self.abort_button = QPushButton(Dialog)
        self.abort_button.setObjectName(u"abort_button")
        icon3 = QIcon()
        icon3.addFile(u":/resources/cancel.png", QSize(), QIcon.Normal, QIcon.Off)
        self.abort_button.setIcon(icon3)

        self.buttons_h_layout.addWidget(self.abort_button)

        self.buttons_h_layout.setStretch(0, 1)
        self.buttons_h_layout.setStretch(1, 1)

        self.gridLayout.addLayout(self.buttons_h_layout, 13, 0, 1, 1)

        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 2, 0, 1, 1)

        self.name_h_layout = QHBoxLayout()
        self.name_h_layout.setObjectName(u"name_h_layout")
        self.name_h_layout.setContentsMargins(5, 5, 5, 5)
        self.name_label = QLabel(Dialog)
        self.name_label.setObjectName(u"name_label")
        self.name_label.setIndent(10)

        self.name_h_layout.addWidget(self.name_label)

        self.name_line_edit = QLineEdit(Dialog)
        self.name_line_edit.setObjectName(u"name_line_edit")

        self.name_h_layout.addWidget(self.name_line_edit)

        self.name_h_layout.setStretch(0, 1)
        self.name_h_layout.setStretch(1, 1)

        self.gridLayout.addLayout(self.name_h_layout, 1, 0, 1, 1)

        self.active_sess_h_layout = QHBoxLayout()
        self.active_sess_h_layout.setSpacing(5)
        self.active_sess_h_layout.setObjectName(u"active_sess_h_layout")
        self.active_sess_h_layout.setContentsMargins(5, 5, 5, 5)
        self.active_sess_label = QLabel(Dialog)
        self.active_sess_label.setObjectName(u"active_sess_label")
        self.active_sess_label.setIndent(10)

        self.active_sess_h_layout.addWidget(self.active_sess_label)

        self.active_sess_combobox = QComboBox(Dialog)
        self.active_sess_combobox.setObjectName(u"active_sess_combobox")

        self.active_sess_h_layout.addWidget(self.active_sess_combobox)

        self.active_sess_h_layout.setStretch(0, 1)
        self.active_sess_h_layout.setStretch(1, 1)

        self.gridLayout.addLayout(self.active_sess_h_layout, 8, 0, 1, 1)

        self.line_4 = QFrame(Dialog)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_4, 12, 0, 1, 1)

        self.line_3 = QFrame(Dialog)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_3, 9, 0, 1, 1)

        self.any_user_h_layout = QHBoxLayout()
        self.any_user_h_layout.setObjectName(u"any_user_h_layout")
        self.any_user_h_layout.setContentsMargins(5, 5, 5, 5)
        self.any_user_label = QLabel(Dialog)
        self.any_user_label.setObjectName(u"any_user_label")
        self.any_user_label.setIndent(10)

        self.any_user_h_layout.addWidget(self.any_user_label)

        self.any_user_combobox = QComboBox(Dialog)
        self.any_user_combobox.setObjectName(u"any_user_combobox")

        self.any_user_h_layout.addWidget(self.any_user_combobox)

        self.any_user_h_layout.setStretch(0, 1)
        self.any_user_h_layout.setStretch(1, 1)

        self.gridLayout.addLayout(self.any_user_h_layout, 6, 0, 1, 1)

        self.inactive_sess_h_layout = QHBoxLayout()
        self.inactive_sess_h_layout.setObjectName(u"inactive_sess_h_layout")
        self.inactive_sess_h_layout.setContentsMargins(5, 5, 5, 5)
        self.inactive_sess_label = QLabel(Dialog)
        self.inactive_sess_label.setObjectName(u"inactive_sess_label")
        self.inactive_sess_label.setIndent(10)

        self.inactive_sess_h_layout.addWidget(self.inactive_sess_label)

        self.inactive_sess_combobox = QComboBox(Dialog)
        self.inactive_sess_combobox.setObjectName(u"inactive_sess_combobox")

        self.inactive_sess_h_layout.addWidget(self.inactive_sess_combobox)


        self.gridLayout.addLayout(self.inactive_sess_h_layout, 7, 0, 1, 1)

        self.objects_list_view = QListWidget(Dialog)
        self.objects_list_view.setObjectName(u"objects_list_view")
        self.objects_list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.objects_list_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.objects_list_view.setIconSize(QSize(16, 16))

        self.gridLayout.addWidget(self.objects_list_view, 11, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Add explicit privelege", None))
        self.dialog_label.setText(QCoreApplication.translate("Dialog", u"Set parameters for new explicit privelege:", None))
        self.manage_label.setText(QCoreApplication.translate("Dialog", u"Objects to apply:", None))
        self.add_button.setText(QCoreApplication.translate("Dialog", u"Add", None))
        self.remove_button.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.priority_label.setText(QCoreApplication.translate("Dialog", u"Policy priority:", None))
        self.save_button.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.abort_button.setText(QCoreApplication.translate("Dialog", u"Abort", None))
        self.name_label.setText(QCoreApplication.translate("Dialog", u"Configuration name:", None))
        self.active_sess_label.setText(QCoreApplication.translate("Dialog", u"Active session:", None))
        self.any_user_label.setText(QCoreApplication.translate("Dialog", u"Any user:", None))
        self.inactive_sess_label.setText(QCoreApplication.translate("Dialog", u"Inactive session:", None))
    # retranslateUi

