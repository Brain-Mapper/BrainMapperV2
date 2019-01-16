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
from PyQt4.QtCore import Qt, QRect
# Imports for the plotting

import ourLib.ExcelExport.excelExport as ee
from clustering_components.clustering_paramspace import ParameterAndScriptStack
# View components' import
from clustering_components.clustering_results import ClusteringDataTable, ClusteringGraphs, ClusteringResultsPopUp
from clustering_components.clustering_topbar import *
import clustering_components.clustering_plot as clustering_plot

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

class ClusteringView2(QtGui.QWidget):

    showMain = pyqtSignal()

    def __init__(self):
        super(ClusteringView2, self).__init__()

        self.clust_chooser = None
        self.table_displayer = None

        self.results_popup = ClusteringResultsPopUp(':ressources/logo.png', ':ressources/app_icons_png/file-1.png')

        self.label = None
        self.centroids = None



        title_style = "QLabel { background-color : #ffcc33 ; color : black;  font-style : bold; font-size : 14px;}"


        self.setupUi(self)

    def popup_results_details(self, method_name, user_params):
        self.results_popup.setGeometry(QRect(100, 100, 500, 300))

        if self.label is not None:
            self.results_popup.update_details(method_name, user_params, self.centroids, clustering_validation_indexes(self.label,
                                                                                                      self.centroids,
                                                                                                      float(len(set(self.label)))))
        self.results_popup.show()


    def fill_table(self, usable_dataset_instance):
        #self.table_displayer.fill_with_extracted_data(usable_dataset_instance)

        """
        Fills this custom table with the data of a UsableDataSet obtained after data extraction
        :param a_usable_dataset_instance: see UsableData for more details
        :return: Nothing"""
        print("coucou")
        self.clustering_usable_dataset = usable_dataset_instance
        self.tableWidget.setRowCount(usable_dataset_instance.get_row_num())

        row_count = 0

        for udcoll in self.clustering_usable_dataset.get_usable_data_list():

            extracted_data_dictionary = udcoll.get_extracted_data_dict()

            for origin_file in extracted_data_dictionary.keys():
                data_array = extracted_data_dictionary[origin_file]
                for data_rows in range(0, data_array.shape[0]):
                    self.tableWidget.setItem(row_count, 0, QtGui.QTableWidgetItem(udcoll.get_imgcoll_name()))
                    self.tableWidget.setItem(row_count, 1, QtGui.QTableWidgetItem(str(origin_file.filename)))
                    self.tableWidget.setItem(row_count, 2, QtGui.QTableWidgetItem(str(data_array[data_rows, 0]))) # X coordinate at column 0
                    self.tableWidget.setItem(row_count, 3, QtGui.QTableWidgetItem(str(data_array[data_rows, 1]))) # Y coordinate at column 1
                    self.tableWidget.setItem(row_count, 4, QtGui.QTableWidgetItem(str(data_array[data_rows, 2]))) # Z coordinate at column 2
                    self.tableWidget.setItem(row_count, 5, QtGui.QTableWidgetItem(str(data_array[data_rows, 3]))) # Intensity at column 3
                    self.tableWidget.setItem(row_count, 6, QtGui.QTableWidgetItem("None yet"))
                    row_count = row_count+1


    def runSelectedClust(self):
        print(self.comboBox_methode.currentText())
        clustering_results = run_clustering(selectedMethod, param_dict)
        print("runSelectedCLud -> Param dict : {}".format(param_dict.keys()));
        self.label = clustering_results[0]
        self.centroids = clustering_results[1]
        self.table_displayer.fill_clust_labels(self.label)
        self.add_hist(param_dict, self.label)
        self.add_silhouette(self.label)

        # Plot the differents figures for test
        clustering_plot.plot_silhouette(self.label)
        clustering_plot.plot_3d_clusters(self.label)
        clustering_plot.plot_cross_section(self.label)

    def export(self):
        if self.label is not None:
            (f_path, f_name) = os.path.split(str(QFileDialog.getSaveFileName(self, "Browse Directory")))
            ee.clustering_export(f_name, f_path, self.table_displayer.clustering_usable_dataset, self.label)
        else:
            QtGui.QMessageBox.information(self, "Run Clustering before", "No cluster affectation")

    def save(self):
        if self.label is not None:
            makeClusterResultSet(self.table_displayer.clustering_usable_dataset, self.label)
            QtGui.QMessageBox.information(self, "Results saved!",
                                          "A set has been created in the clustering results tab at home page.")

        else:
            QtGui.QMessageBox.information(self, "Run Clustering before", "No cluster affectation")

    def go_back(self):
        # -- When the user wants to return to the main view, we reinit the cluster view
        #self.resultsGraphs.graph1.clear()
        #self.resultsGraphs.graph2.clear()

        self.showMain.emit()

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1000, 650)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget = QtGui.QWidget(Form)
        self.widget.setMaximumSize(QtCore.QSize(300, 16777215))
        self.widget.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 9)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.label_select_methode = QtGui.QLabel(self.widget)
        self.label_select_methode.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_select_methode.setFont(font)
        self.label_select_methode.setTextFormat(QtCore.Qt.AutoText)
        self.label_select_methode.setObjectName(_fromUtf8("label_select_methode"))
        self.verticalLayout_clustering.addWidget(self.label_select_methode)
        self.comboBox_methode = ClusteringChooser()
        # self.comboBox_methode = QtGui.QComboBox(self.widget_clustering)
        # sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.comboBox_methode.sizePolicy().hasHeightForWidth())
        # self.comboBox_methode.setSizePolicy(sizePolicy)
        # self.comboBox_methode.setMaximumSize(QtCore.QSize(16777215, 30))
        # font = QtGui.QFont()
        # font.setPointSize(10)
        # self.comboBox_methode.setFont(font)
        # self.comboBox_methode.setObjectName(_fromUtf8("comboBox_methode"))
        # self.comboBox_methode.addItem(_fromUtf8(""))
        # self.comboBox_methode.addItem(_fromUtf8(""))
        # self.comboBox_methode.addItem(_fromUtf8(""))
        # self.comboBox_methode.addItem(_fromUtf8(""))
        self.verticalLayout_clustering.addWidget(self.comboBox_methode)
        self.plainTextEdit = QtGui.QPlainTextEdit(self.widget_clustering)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy)
        self.plainTextEdit.setMaximumSize(QtCore.QSize(16777215, 80))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.verticalLayout_clustering.addWidget(self.plainTextEdit)
        self.widget_informations = QtGui.QWidget(self.widget_clustering)
        self.widget_informations.setObjectName(_fromUtf8("widget_informations"))
        self.verticalLayout_clustering.addWidget(self.widget_informations)
        title_style = "QLabel { background-color : #ffcc33 ; color : black;  font-style : bold; font-size : 14px;}"
        self.widget_parametres = ParameterAndScriptStack(title_style, self.comboBox_methode)
        #self.widget_parametres = QtGui.QWidget(self.widget_clustering)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.widget_6.setFont(font)
        self.widget_6.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget_6.setObjectName(_fromUtf8("widget_6"))
        self.verticalLayout.addWidget(self.widget_6)
        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.widget_2 = QtGui.QWidget(Form)
        self.widget_2.setMinimumSize(QtCore.QSize(700, 200))
        self.widget_2.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 9)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_3 = QtGui.QLabel(self.widget_2)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_3.addWidget(self.label_3)
        self.tableWidget = QtGui.QTableWidget(self.widget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMinimumSize(QtCore.QSize(660, 0))
        self.tableWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
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
        self.verticalLayout_tab.addWidget(self.tableWidget)
        self.verticalLayout_dataAndResult.addWidget(self.widget_tab)
        self.widget_buttons = QtGui.QWidget(Form)
        self.widget_buttons.setEnabled(True)
        self.widget_buttons.setMinimumSize(QtCore.QSize(0, 50))
        self.widget_buttons.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget_buttons.setStyleSheet(_fromUtf8(""))
        self.widget_buttons.setObjectName(_fromUtf8("widget_buttons"))
        self.horizontalLayout_buttons = QtGui.QHBoxLayout(self.widget_buttons)
        self.horizontalLayout_buttons.setMargin(0)
        self.horizontalLayout_buttons.setObjectName(_fromUtf8("horizontalLayout_buttons"))
        self.pushButton_run = QtGui.QPushButton(self.widget_buttons)
        self.pushButton_run.setObjectName(_fromUtf8("pushButton_run"))

        # self.pushButton_run.clicked.connect(lambda: self.runSelectedClust(self.clust_chooser.get_selected_method_name(),
        #                                                                   self.param_script_stack.get_user_params()))
        self.pushButton_run.clicked.connect(self.runSelectedClust)
        self.horizontalLayout_buttons.addWidget(self.pushButton_run)
        self.pushButton_export = QtGui.QPushButton(self.widget_buttons)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.horizontalLayout_buttons.addWidget(self.pushButton_export)
        self.comboBox_3 = QtGui.QComboBox(self.widget_buttons)
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.comboBox_3)
        self.pushButton_4 = QtGui.QPushButton(self.widget_4)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.pushButton_5 = QtGui.QPushButton(self.widget_4)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.pushButton_6 = QtGui.QPushButton(self.widget_4)
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.horizontalLayout_2.addWidget(self.pushButton_6)
        self.verticalLayout_2.addWidget(self.widget_4)
        self.widget_3 = QtGui.QWidget(Form)
        self.widget_3.setMinimumSize(QtCore.QSize(700, 0))
        self.widget_3.setMaximumSize(QtCore.QSize(16777215, 230))
        self.widget_3.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.widget_3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 9)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_4 = QtGui.QLabel(self.widget_3)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_4.addWidget(self.label_4)
        self.widget_7 = QtGui.QWidget(self.widget_3)
        self.widget_7.setObjectName(_fromUtf8("widget_7"))
        self.verticalLayout_4.addWidget(self.widget_7)
        self.verticalLayout_2.addWidget(self.widget_3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_clustering.setText(_translate("Form", "Clustering", None))
        self.label_select_methode.setText(_translate("Form", "Select a clustering methods", None))
        # self.comboBox_methode.setItemText(0, _translate("Form", "K-means", None))
        # self.comboBox_methode.setItemText(1, _translate("Form", "K-medoids", None))
        # self.comboBox_methode.setItemText(2, _translate("Form", "Agglomerative", None))
        # self.comboBox_methode.setItemText(3, _translate("Form", "Fuzzy C-means", None))
        self.plainTextEdit.setPlainText(_translate("Form", "You have to select columns to apply cluster on thos columns", None))
        self.label_3.setText(_translate("Form", "Data inside the collection", None))
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
        self.pushButton_3.setText(_translate("Form", "Run", None))
        self.pushButton_2.setText(_translate("Form", "Export", None))
        self.comboBox_3.setItemText(0, _translate("Form", "Sihouette", None))
        self.comboBox_3.setItemText(1, _translate("Form", "3D view", None))
        self.comboBox_3.setItemText(2, _translate("Form", "Repartition", None))
        self.comboBox_3.setItemText(3, _translate("Form", "Graphic", None))
        self.pushButton_4.setText(_translate("Form", "Show", None))
        self.pushButton_5.setText(_translate("Form", "Save as set", None))
        self.pushButton_6.setText(_translate("Form", "Go back", None))
        self.label_4.setText(_translate("Form", "Result details", None))
