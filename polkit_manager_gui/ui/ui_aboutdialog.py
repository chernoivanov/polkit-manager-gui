# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'aboutdialog.ui'
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
        Dialog.resize(498, 148)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.icon_v_layout = QVBoxLayout()
        self.icon_v_layout.setSpacing(10)
        self.icon_v_layout.setObjectName(u"icon_v_layout")
        self.icon_v_layout.setContentsMargins(10, -1, 30, -1)
        self.icon_label = QLabel(Dialog)
        self.icon_label.setObjectName(u"icon_label")
        self.icon_label.setPixmap(QPixmap(u":/resources/privacy-policy.png"))

        self.icon_v_layout.addWidget(self.icon_label)


        self.gridLayout.addLayout(self.icon_v_layout, 0, 0, 1, 1)

        self.info_v_layout = QVBoxLayout()
        self.info_v_layout.setObjectName(u"info_v_layout")
        self.info_v_layout.setContentsMargins(10, -1, -1, -1)
        self.title_label = QLabel(Dialog)
        self.title_label.setObjectName(u"title_label")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.title_label.setFont(font)

        self.info_v_layout.addWidget(self.title_label)

        self.version_label = QLabel(Dialog)
        self.version_label.setObjectName(u"version_label")
        font1 = QFont()
        font1.setBold(True)
        font1.setItalic(True)
        self.version_label.setFont(font1)

        self.info_v_layout.addWidget(self.version_label)

        self.description_label = QLabel(Dialog)
        self.description_label.setObjectName(u"description_label")
        font2 = QFont()
        font2.setPointSize(13)
        self.description_label.setFont(font2)

        self.info_v_layout.addWidget(self.description_label)

        self.info_v_layout.setStretch(0, 1)
        self.info_v_layout.setStretch(1, 1)
        self.info_v_layout.setStretch(2, 4)

        self.gridLayout.addLayout(self.info_v_layout, 0, 1, 1, 1)

        self.gridLayout.setColumnStretch(1, 1)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"About Polkit Manager", None))
        self.icon_label.setText("")
        self.title_label.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.version_label.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.description_label.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
    # retranslateUi

