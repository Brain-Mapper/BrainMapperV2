# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Clustering.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt4.Qt import QFileDialog
from PyQt4.QtCore import Qt, QRect, pyqtSignal
# Imports for the plotting
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


class SOMView(QtGui.QWidget):

    showMain = pyqtSignal()

    def __init__(self):
        super(SOMView, self).__init__()

        self.setupUi(self)


    def fill_table(self,list_entete,list_data):
        print("bjr")
        self.list_entete = list_entete
        self.list_data = list_data
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(8)
        self.tableWidget.setColumnCount(len(list_entete))
        self.tableWidget.setRowCount(int(len(list_data)/len(list_entete)))
        for i in range (0,len(list_entete)):
            item = QtGui.QTableWidgetItem()
            item.setFont(font)
            item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
            self.tableWidget.setHorizontalHeaderItem(i, item)
            item.setText(list_entete[i])
        self.tableWidget.horizontalHeader().setVisible(True)
        for i in range(0,int(len(list_data)/len(list_entete))):
            for j in range(0,len(list_entete)):
                self.tableWidget.setItem(i, j, QtGui.QTableWidgetItem(list_data[i+j]))

        """
        Fills this custom table with the data of a UsableDataSet obtained after data extraction
        :param a_usable_dataset_instance: see UsableData for more details
        :return: Nothing"""

        # self.clustering_usable_dataset = usable_dataset_instance
        # self.tableWidget.setRowCount(usable_dataset_instance.get_row_num())

        # row_count = 0

        # for udcoll in self.clustering_usable_dataset.get_usable_data_list():

        #     extracted_data_dictionary = udcoll.get_extracted_data_dict()

        #     for origin_file in extracted_data_dictionary.keys():
        #         data_array = extracted_data_dictionary[origin_file]
        #         for data_rows in range(0, data_array.shape[0]):
        #             self.tableWidget.setItem(row_count, 0, QtGui.QTableWidgetItem(udcoll.get_imgcoll_name()))
        #             self.tableWidget.setItem(row_count, 1, QtGui.QTableWidgetItem(str(origin_file.filename)))
        #             self.tableWidget.setItem(row_count, 2, QtGui.QTableWidgetItem(str(data_array[data_rows, 0]))) # X coordinate at column 0
        #             self.tableWidget.setItem(row_count, 3, QtGui.QTableWidgetItem(str(data_array[data_rows, 1]))) # Y coordinate at column 1
        #             self.tableWidget.setItem(row_count, 4, QtGui.QTableWidgetItem(str(data_array[data_rows, 2]))) # Z coordinate at column 2
        #             self.tableWidget.setItem(row_count, 5, QtGui.QTableWidgetItem(str(data_array[data_rows, 3]))) # Intensity at column 3
        #             self.tableWidget.setItem(row_count, 6, QtGui.QTableWidgetItem("None yet"))
        #             row_count = row_count+1


    def go_back(self):
        self.showMain.emit()

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1000, 650)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.widget_param_global = QtGui.QWidget(Form)
        self.widget_param_global.setMinimumSize(QtCore.QSize(330, 0))
        self.widget_param_global.setMaximumSize(QtCore.QSize(0, 16777215))
        self.widget_param_global.setObjectName(_fromUtf8("widget_param_global"))
        self.gridLayout_4 = QtGui.QGridLayout(self.widget_param_global)
        self.gridLayout_4.setContentsMargins(0, 0, 0, -1)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_param = QtGui.QLabel(self.widget_param_global)
        self.label_param.setMinimumSize(QtCore.QSize(0, 0))
        self.label_param.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_param.setFont(font)
        self.label_param.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.label_param.setAlignment(QtCore.Qt.AlignCenter)
        self.label_param.setObjectName(_fromUtf8("label_param"))
        self.gridLayout_4.addWidget(self.label_param, 0, 0, 1, 1)
        self.widget_param = QtGui.QWidget(self.widget_param_global)
        self.widget_param.setObjectName(_fromUtf8("widget_param"))
        self.gridLayout_5 = QtGui.QGridLayout(self.widget_param)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.lineEdit_std = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_std.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_std.setObjectName(_fromUtf8("lineEdit_std"))
        self.gridLayout_5.addWidget(self.lineEdit_std, 7, 0, 1, 1)
        self.lineEdit_6 = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_6.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))
        self.gridLayout_5.addWidget(self.lineEdit_6, 6, 0, 1, 1)
        self.label_step = QtGui.QLabel(self.widget_param)
        self.label_step.setObjectName(_fromUtf8("label_step"))
        self.gridLayout_5.addWidget(self.label_step, 5, 1, 1, 1)
        self.label_radius = QtGui.QLabel(self.widget_param)
        self.label_radius.setObjectName(_fromUtf8("label_radius"))
        self.gridLayout_5.addWidget(self.label_radius, 6, 1, 1, 1)
        self.label_nbiter = QtGui.QLabel(self.widget_param)
        self.label_nbiter.setObjectName(_fromUtf8("label_nbiter"))
        self.gridLayout_5.addWidget(self.label_nbiter, 4, 1, 1, 1)
        self.label_largeur = QtGui.QLabel(self.widget_param)
        self.label_largeur.setObjectName(_fromUtf8("label_largeur"))
        self.gridLayout_5.addWidget(self.label_largeur, 3, 1, 1, 1)
        self.lineEdit_step = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_step.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_step.setObjectName(_fromUtf8("lineEdit_step"))
        self.gridLayout_5.addWidget(self.lineEdit_step, 5, 0, 1, 1)
        self.label_std = QtGui.QLabel(self.widget_param)
        self.label_std.setObjectName(_fromUtf8("label_std"))
        self.gridLayout_5.addWidget(self.label_std, 7, 1, 1, 1)
        self.label_hauteur = QtGui.QLabel(self.widget_param)
        self.label_hauteur.setObjectName(_fromUtf8("label_hauteur"))
        self.gridLayout_5.addWidget(self.label_hauteur, 2, 1, 1, 1)
        self.lineEdit_nbiter = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_nbiter.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_nbiter.setObjectName(_fromUtf8("lineEdit_nbiter"))
        self.gridLayout_5.addWidget(self.lineEdit_nbiter, 4, 0, 1, 1)
        self.label_choice = QtGui.QLabel(self.widget_param)
        self.label_choice.setObjectName(_fromUtf8("label_choice"))
        self.gridLayout_5.addWidget(self.label_choice, 1, 1, 1, 1)
        self.lineEdit_largeur = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_largeur.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_largeur.setObjectName(_fromUtf8("lineEdit_largeur"))
        self.gridLayout_5.addWidget(self.lineEdit_largeur, 3, 0, 1, 1)
        self.lineEdit_hauteur = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_hauteur.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_hauteur.setObjectName(_fromUtf8("lineEdit_hauteur"))
        self.gridLayout_5.addWidget(self.lineEdit_hauteur, 2, 0, 1, 1)
        self.comboBox_choice = QtGui.QComboBox(self.widget_param)
        self.comboBox_choice.setMaximumSize(QtCore.QSize(150, 16777215))
        self.comboBox_choice.setObjectName(_fromUtf8("comboBox_choice"))

        self.gridLayout_5.addWidget(self.comboBox_choice, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.widget_param, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.widget_param_global, 0, 0, 2, 1)
        self.widget_button = QtGui.QWidget(Form)
        self.widget_button.setMaximumSize(QtCore.QSize(16777215, 60))
        self.widget_button.setObjectName(_fromUtf8("widget_button"))
        self.gridLayout_2 = QtGui.QGridLayout(self.widget_button)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.pushButton_train = QtGui.QPushButton(self.widget_button)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButton_train.setFont(font)
        self.pushButton_train.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.pushButton_train.setObjectName(_fromUtf8("pushButton_train"))
        self.gridLayout_2.addWidget(self.pushButton_train, 0, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(self.widget_button)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.comboBox.setFont(font)
        self.comboBox.setMouseTracking(True)
        self.comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox.setAutoFillBackground(False)
        self.comboBox.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))

        self.comboBox_choice.setFont(font)
        self.comboBox_choice.setMouseTracking(True)
        self.comboBox_choice.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox_choice.setAutoFillBackground(False)
        self.comboBox_choice.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.comboBox_choice.addItem(_fromUtf8(""))
        self.comboBox_choice.addItem(_fromUtf8(""))

        self.gridLayout_2.addWidget(self.comboBox, 0, 1, 1, 1)
        self.pushButton_show = QtGui.QPushButton(self.widget_button)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButton_show.setFont(font)
        self.pushButton_show.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.pushButton_show.setObjectName(_fromUtf8("pushButton_show"))
        self.gridLayout_2.addWidget(self.pushButton_show, 0, 2, 1, 1)
        self.pushButton_goback = QtGui.QPushButton(self.widget_button)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButton_goback.setFont(font)
        self.pushButton_goback.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.pushButton_goback.setObjectName(_fromUtf8("pushButton_goback"))
        self.pushButton_goback.clicked.connect(self.go_back)
        self.gridLayout_2.addWidget(self.pushButton_goback, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.widget_button, 1, 1, 1, 1)
        self.widget_table = QtGui.QWidget(Form)
        self.widget_table.setObjectName(_fromUtf8("widget_table"))
        self.gridLayout_3 = QtGui.QGridLayout(self.widget_table)
        self.gridLayout_3.setContentsMargins(0, 0, 0, -1)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_data = QtGui.QLabel(self.widget_table)
        self.label_data.setMinimumSize(QtCore.QSize(0, 30))
        self.label_data.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_data.setFont(font)
        self.label_data.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.label_data.setAlignment(QtCore.Qt.AlignCenter)
        self.label_data.setObjectName(_fromUtf8("label_data"))
        self.gridLayout_3.addWidget(self.label_data, 0, 0, 1, 1)
        # self.verticalLayout_tab = QtGui.QVBoxLayout(self.widget_tab)
        # self.verticalLayout_tab.setContentsMargins(0, 0, 0, 9)
        # self.verticalLayout_tab.setObjectName(_fromUtf8("verticalLayout_tab"))
        self.tableWidget = QtGui.QTableWidget(self.widget_table)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.gridLayout_3.addWidget(self.tableWidget, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.widget_table, 0, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_param.setText(_translate("Form", "Parameters", None))
        self.label_step.setText(_translate("Form", "Step", None))
        self.label_radius.setText(_translate("Form", "Radis", None))
        self.label_nbiter.setText(_translate("Form", "Nombre d\'itération", None))
        self.label_largeur.setText(_translate("Form", "Largeur", None))
        self.label_std.setText(_translate("Form", "Std", None))
        self.label_hauteur.setText(_translate("Form", "Hauteur", None))
        self.label_choice.setText(_translate("Form", "Hex or rect", None))
        self.pushButton_train.setText(_translate("Form", "Train", None))
        self.comboBox_choice.setItemText(1, _translate("Form", "Hex", None))
        self.comboBox_choice.setItemText(0, _translate("Form", "Rect", None))
        self.pushButton_show.setText(_translate("Form", "Show", None))
        self.pushButton_goback.setText(_translate("Form", "Go back", None))
        self.label_data.setText(_translate("Form", "Data used for the Self Organizing Map (SOM)", None))
