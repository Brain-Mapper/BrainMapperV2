# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Clustering.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1024, 731)
        self.widget = QtGui.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(10, 20, 371, 701))
        self.widget.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(10, 30, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName(_fromUtf8("label"))
        self.comboBox_2 = QtGui.QComboBox(self.widget)
        self.comboBox_2.setGeometry(QtCore.QRect(230, 30, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.widget_5 = QtGui.QWidget(self.widget)
        self.widget_5.setGeometry(QtCore.QRect(10, 170, 341, 251))
        self.widget_5.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget_5.setObjectName(_fromUtf8("widget_5"))
        self.widget_6 = QtGui.QWidget(self.widget)
        self.widget_6.setGeometry(QtCore.QRect(10, 440, 341, 251))
        self.widget_6.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget_6.setObjectName(_fromUtf8("widget_6"))
        self.plainTextEdit = QtGui.QPlainTextEdit(self.widget)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 80, 341, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.widget_2 = QtGui.QWidget(Form)
        self.widget_2.setGeometry(QtCore.QRect(400, 20, 611, 311))
        self.widget_2.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.tableWidget = QtGui.QTableWidget(self.widget_2)
        self.tableWidget.setGeometry(QtCore.QRect(-5, 0, 621, 311))
        self.tableWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setRowCount(5)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(7)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(8)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(6, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.widget_3 = QtGui.QWidget(Form)
        self.widget_3.setGeometry(QtCore.QRect(400, 450, 611, 271))
        self.widget_3.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.widget_4 = QtGui.QWidget(Form)
        self.widget_4.setGeometry(QtCore.QRect(400, 360, 611, 61))
        self.widget_4.setStyleSheet(_fromUtf8(""))
        self.widget_4.setObjectName(_fromUtf8("widget_4"))
        self.pushButton = QtGui.QPushButton(self.widget_4)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.pushButton.setIconSize(QtCore.QSize(20, 20))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.widget_4)
        self.pushButton_2.setGeometry(QtCore.QRect(310, 10, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.widget_4)
        self.pushButton_3.setGeometry(QtCore.QRect(100, 10, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(self.widget_4)
        self.pushButton_4.setGeometry(QtCore.QRect(410, 10, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_5 = QtGui.QPushButton(self.widget_4)
        self.pushButton_5.setGeometry(QtCore.QRect(510, 10, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.comboBox = QtGui.QComboBox(self.widget_4)
        self.comboBox.setGeometry(QtCore.QRect(190, 10, 111, 41))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.comboBox.setFont(font)
        self.comboBox.setMouseTracking(True)
        self.comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox.setAutoFillBackground(False)
        self.comboBox.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.tableWidget.resizeColumnsToContents)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Select a clustering methods", None))
        self.comboBox_2.setItemText(0, _translate("Form", "K-means", None))
        self.comboBox_2.setItemText(1, _translate("Form", "K-medoids", None))
        self.comboBox_2.setItemText(2, _translate("Form", "Agglomerative", None))
        self.comboBox_2.setItemText(3, _translate("Form", "Fuzzy C-means", None))
        self.plainTextEdit.setPlainText(_translate("Form", "You have to select columns to apply cluster on thos columns", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Image coll ID", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "File name", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "X", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Y", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Z", None))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Intensity", None))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "Assigned cluster", None))
        self.pushButton.setText(_translate("Form", "Run", None))
        self.pushButton_2.setText(_translate("Form", "Show", None))
        self.pushButton_3.setText(_translate("Form", "Export", None))
        self.pushButton_4.setText(_translate("Form", "Save as set", None))
        self.pushButton_5.setText(_translate("Form", "Go back", None))
        self.comboBox.setItemText(0, _translate("Form", "Silhouette", None))
        self.comboBox.setItemText(1, _translate("Form", "3D view", None))
        self.comboBox.setItemText(2, _translate("Form", "Repartition", None))
        self.comboBox.setItemText(3, _translate("Form", "Graphic", None))

