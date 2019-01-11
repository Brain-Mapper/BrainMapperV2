# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Edit.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
from PyQt4 import QtGui
from PyQt4.Qt import *
from PyQt4.QtCore import pyqtSignal,QCoreApplication
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSignal

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from BrainMapper import *

import pyqtgraph as pg
import pyqtgraph.opengl as gl

import UI_builder.resources
import re
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class EditView2(QtGui.QWidget):

    showMain = pyqtSignal()

    def __init__(self):
        super(EditView2, self).__init__()

        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1000, 650)
        Form.setMinimumSize(QtCore.QSize(200, 0))
        self.gridLayout_3 = QtGui.QGridLayout(Form)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.widget = QtGui.QWidget(Form)
        self.widget.setMaximumSize(QtCore.QSize(400, 16777215))
        self.widget.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_8 = QtGui.QLabel(self.widget)
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout_2.addWidget(self.label_8)
        self.widget_6 = QtGui.QWidget(self.widget)
        self.widget_6.setMinimumSize(QtCore.QSize(250, 0))
        self.widget_6.setObjectName(_fromUtf8("widget_6"))
        self.verticalLayout_2.addWidget(self.widget_6)
        self.horizontalLayout_2.addWidget(self.widget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget_2 = QtGui.QWidget(Form)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 300))
        self.widget_2.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.widget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_9 = QtGui.QLabel(self.widget_2)
        self.label_9.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_2.addWidget(self.label_9, 0, 0, 1, 1)
        self.widget_3 = QtGui.QWidget(self.widget_2)
        self.widget_3.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.gridLayout = QtGui.QGridLayout(self.widget_3)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.widget_3)
        self.label.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.label_4 = QtGui.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setText(_fromUtf8(""))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setText(_fromUtf8(""))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 1, 1, 2)
        self.label_3 = QtGui.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setText(_fromUtf8(""))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 2, 1, 1, 2)
        self.scrollArea = QtGui.QScrollArea(self.widget_3)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 702, 394))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 3, 0, 1, 3)
        self.scrollArea.raise_()
        self.label_6.raise_()
        self.label_5.raise_()
        self.label_3.raise_()
        self.label_2.raise_()
        self.label.raise_()
        self.label_4.raise_()
        self.gridLayout_2.addWidget(self.widget_3, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.widget_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_10 = QtGui.QLabel(Form)
        self.label_10.setMinimumSize(QtCore.QSize(200, 0))
        self.label_10.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.label_10.setText(_fromUtf8(""))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout_3.addWidget(self.label_10)
        self.pushButton_4 = QtGui.QPushButton(Form)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout_3.addWidget(self.pushButton_4)
        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_12 = QtGui.QPushButton(Form)
        self.pushButton_12.setObjectName(_fromUtf8("pushButton_12"))
        self.horizontalLayout.addWidget(self.pushButton_12)
        self.pushButton_11 = QtGui.QPushButton(Form)
        self.pushButton_11.setObjectName(_fromUtf8("pushButton_11"))
        self.horizontalLayout.addWidget(self.pushButton_11)
        self.pushButton_10 = QtGui.QPushButton(Form)
        self.pushButton_10.setObjectName(_fromUtf8("pushButton_10"))
        self.horizontalLayout.addWidget(self.pushButton_10)
        self.pushButton_9 = QtGui.QPushButton(Form)
        self.pushButton_9.setObjectName(_fromUtf8("pushButton_9"))
        self.horizontalLayout.addWidget(self.pushButton_9)
        self.pushButton_8 = QtGui.QPushButton(Form)
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.horizontalLayout.addWidget(self.pushButton_8)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_8.setText(_translate("Form", "Selected image collection", None))
        self.label_9.setText(_translate("Form", "Selected image collection", None))
        self.label.setText(_translate("Form", "Collection name :", None))
        self.label_2.setText(_translate("Form", "Set name :", None))
        self.label_3.setText(_translate("Form", "List of images : ", None))
        self.pushButton_4.setText(_translate("Form", "Show Graphic", None))
        self.pushButton_3.setText(_translate("Form", "Remove", None))
        self.pushButton_12.setText(_translate("Form", "Save changes", None))
        self.pushButton_11.setText(_translate("Form", "Change name", None))
        self.pushButton_10.setText(_translate("Form", "Add new", None))
        self.pushButton_9.setText(_translate("Form", "Delete", None))
        self.pushButton_8.setText(_translate("Form", "Go back", None))
