# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Edit.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *
from PyQt4.QtCore import pyqtSignal,QCoreApplication
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
        Form.resize(1024, 731)
        Form.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget = QtGui.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(10, 20, 371, 701))
        self.widget.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.widget_2 = QtGui.QWidget(Form)
        self.widget_2.setGeometry(QtCore.QRect(400, 20, 611, 701))
        self.widget_2.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.widget_3 = QtGui.QWidget(self.widget_2)
        self.widget_3.setGeometry(QtCore.QRect(10, 10, 591, 481))
        self.widget_3.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget_3.setObjectName(_fromUtf8("widget_3"))

        self.scrollArea = QtGui.QScrollArea(self.widget_3)
        self.scrollArea.setGeometry(QtCore.QRect(10, 110, 571, 361))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 569, 359))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.label_6 = QtGui.QLabel(self.widget_3)
        self.label_6.setGeometry(QtCore.QRect(140, 80, 291, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setText(_fromUtf8(""))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_5 = QtGui.QLabel(self.widget_3)
        self.label_5.setGeometry(QtCore.QRect(140, 50, 291, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setText(_fromUtf8(""))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_3 = QtGui.QLabel(self.widget_3)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_2 = QtGui.QLabel(self.widget_3)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label = QtGui.QLabel(self.widget_3)
        self.label.setGeometry(QtCore.QRect(10, 20, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_4 = QtGui.QLabel(self.widget_3)
        self.label_4.setGeometry(QtCore.QRect(160, 20, 291, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setText(_fromUtf8(""))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.widget_4 = QtGui.QWidget(self.widget_2)
        self.widget_4.setGeometry(QtCore.QRect(10, 510, 591, 80))
        self.widget_4.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget_4.setInputMethodHints(QtCore.Qt.ImhNone)
        self.widget_4.setObjectName(_fromUtf8("widget_4"))
        #self.widget_4.hide()
        self.pushButton = QtGui.QPushButton(self.widget_4)
        self.pushButton.setGeometry(QtCore.QRect(480, 20, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.widget_4)
        self.pushButton_2.setGeometry(QtCore.QRect(350, 20, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.label_7 = QtGui.QLabel(self.widget_4)
        self.label_7.setGeometry(QtCore.QRect(10, 20, 311, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.label_7.setText(_fromUtf8(""))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.widget_5 = QtGui.QWidget(self.widget_2)
        self.widget_5.setGeometry(QtCore.QRect(10, 610, 591, 80))
        self.widget_5.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget_5.setObjectName(_fromUtf8("widget_5"))
        self.pushButton_3 = QtGui.QPushButton(self.widget_5)
        self.pushButton_3.setGeometry(QtCore.QRect(490, 20, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(self.widget_5)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 20, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_5 = QtGui.QPushButton(self.widget_5)
        self.pushButton_5.setGeometry(QtCore.QRect(380, 20, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_6 = QtGui.QPushButton(self.widget_5)
        self.pushButton_6.setGeometry(QtCore.QRect(270, 20, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_7 = QtGui.QPushButton(self.widget_5)
        self.pushButton_7.setGeometry(QtCore.QRect(140, 20, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_3.setText(_translate("Form", "List of images : ", None))
        self.label_2.setText(_translate("Form", "Set name :", None))
        self.label.setText(_translate("Form", "Collection name :", None))
        self.pushButton.setText(_translate("Form", "Remove", None))
        self.pushButton_2.setText(_translate("Form", "Show Graphic", None))
        self.pushButton_3.setText(_translate("Form", "Go back", None))
        self.pushButton_4.setText(_translate("Form", "Save changes", None))
        self.pushButton_5.setText(_translate("Form", "Delete ", None))
        self.pushButton_6.setText(_translate("Form", "Add new", None))
        self.pushButton_7.setText(_translate("Form", "Change name", None))

