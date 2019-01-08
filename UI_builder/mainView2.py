# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainView.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *
from PyQt4.QtCore import pyqtSignal

from datetime import *
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from BrainMapper import *
import UI_builder.resources
import ourLib.ExcelExport.excelExport as ee
import time
from ourLib.dataExtraction.image_recreation import *

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

class MainView2(QtGui.QWidget):

    showClust = pyqtSignal()
    showEdit = pyqtSignal()
    showExport = pyqtSignal()
    showCalcul = pyqtSignal()

    def __init__(self):
        super(MainView2, self).__init__()

        self.setupUi(self)

    def setupUi(self, Form):
        #Form.setObjectName(_fromUtf8("Form"))
        Form.resize(904, 482)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.widget_5 = QtGui.QWidget(Form)
        self.widget_5.setMinimumSize(QtCore.QSize(250, 0))
        self.widget_5.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.widget_5.setObjectName(_fromUtf8("widget_5"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.widget_5)
        self.verticalLayout_4.setContentsMargins(0, 6, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label = QtGui.QLabel(self.widget_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_4.addWidget(self.label)
        self.treeWidget = QtGui.QTreeWidget(self.widget_5)
        self.treeWidget.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);\n"
"border-color: rgb(255, 255, 255);"))
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.treeWidget.headerItem().setFont(0, font)
        self.treeWidget.headerItem().setBackground(0, QtGui.QColor(0, 0, 0, 0))
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item_0.setFont(0, font)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item_0.setBackground(0, brush)
        brush = QtGui.QBrush(QtGui.QColor(82, 99, 141))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item_0.setForeground(0, brush)
        item_0.setCheckState(0, QtCore.Qt.Unchecked)
        item_0.setFlags(QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item_0.setFont(0, font)
        brush = QtGui.QBrush(QtGui.QColor(194, 78, 80))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item_0.setForeground(0, brush)
        item_0.setCheckState(0, QtCore.Qt.Unchecked)
        item_0.setFlags(QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item_0.setFont(0, font)
        brush = QtGui.QBrush(QtGui.QColor(255, 205, 55))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item_0.setForeground(0, brush)
        item_0.setCheckState(0, QtCore.Qt.Unchecked)
        item_0.setFlags(QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.treeWidget.header().setVisible(False)
        self.treeWidget.header().setHighlightSections(False)
        self.verticalLayout_4.addWidget(self.treeWidget)
        self.horizontalLayout_2.addWidget(self.widget_5)
        self.widget_2 = QtGui.QWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMinimumSize(QtCore.QSize(250, 200))
        self.widget_2.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget_2)
        self.verticalLayout.setContentsMargins(0, 6, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setMouseTracking(False)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.checkBox = QtGui.QCheckBox(self.widget_2)
        self.checkBox.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout.addWidget(self.checkBox)
        self.widget = QtGui.QWidget(self.widget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_5.setMargin(0)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.verticalLayout.addWidget(self.widget)
        self.label_2.raise_()
        self.widget_5.raise_()
        self.widget.raise_()
        self.checkBox.raise_()
        self.horizontalLayout_2.addWidget(self.widget_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.widget_3 = QtGui.QWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMinimumSize(QtCore.QSize(200, 200))
        self.widget_3.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setContentsMargins(0, 6, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_3 = QtGui.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setMouseTracking(False)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.widget_4 = QtGui.QWidget(self.widget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget_4.setObjectName(_fromUtf8("widget_4"))
        self.treeWidget.raise_()
        self.verticalLayout_2.addWidget(self.widget_4)
        self.verticalLayout_3.addWidget(self.widget_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_4 = QtGui.QPushButton(Form)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.pushButton_4.raise_()
        self.widget_2.raise_()
        self.widget_3.raise_()
        self.label_3.raise_()
        self.widget_5.raise_()

        self.pushButton_4.clicked.connect(self.extract_and_cluster)
        self.pushButton.clicked.connect(self.edit_pannel)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def show_coll(self, coll):
        # -- This show_coll will add a collection to the current vizu
        get_current_vizu().add(coll)


    def export(self):
    #     if get_selected():
    #         export_choice = QtGui.QMessageBox()
    #         export_choice.setWindowTitle('Export dataSet')
    #
    #         nifti_opt = QRadioButton("Export to Nifti")
    #         excel_opt = QRadioButton("Export to CSV")
    #         nifti_opt.setChecked(True)
    #
    #         l1 = export_choice.layout()
    #         l1.setContentsMargins(20, 0, 0, 20)
    #         l1.addWidget(QLabel("You have selected (" + str(len(
    #             get_selected())) + ") image collections. \nThere is a total of (" + str(get_selected_images_number()) +
    #                             ") NIfTI images to be treated. \nPlease select the way "
    #                             "you would like to export these files : "),
    #                      l1.rowCount() - 3, 0, 1, l1.columnCount() - 2, Qt.AlignCenter)
    #         rb_box = QtGui.QGroupBox()
    #         vbox = QtGui.QVBoxLayout()
    #         vbox.addWidget(nifti_opt)
    #         vbox.addWidget(excel_opt)
    #
    #         rb_box.setLayout(vbox)
    #         l1.addWidget(rb_box, l1.rowCount() - 2, 0, Qt.AlignCenter)
    #
    #         export_choice.setStandardButtons(QMessageBox.Cancel | QMessageBox.Apply)
    #
    #         ret = export_choice.exec_()
    #
    #         if ret == QtGui.QMessageBox.Apply:
    #
    #             if nifti_opt.isChecked():
    #
    #                 folder_path = str(QFileDialog.getExistingDirectory())
    #                 image_recreation_from_list(folder_path, selected)
    #
    #             elif excel_opt.isChecked():
    #                 type_choice = QtGui.QMessageBox()
    #                 type_choice.setWindowTitle('Export excel all or centroid')
    #
    #                 all_opt = QRadioButton("Export all points")
    #                 centroid_opt = QRadioButton("Export only the centroid of each file")
    #                 all_opt.setChecked(True)
    #
    #                 l2 = type_choice.layout()
    #                 l2.setContentsMargins(20, 0, 0, 20)
    #                 l2.addWidget(QLabel(" Excel Export \nPlease select the type of export"),
    #                              l2.rowCount() - 3, 0, 1, l2.columnCount() - 2, Qt.AlignCenter)
    #
    #                 rb_box = QtGui.QGroupBox()
    #                 vbox = QtGui.QVBoxLayout()
    #                 vbox.addWidget(all_opt)
    #                 vbox.addWidget(centroid_opt)
    #
    #                 rb_box.setLayout(vbox)
    #                 l2.addWidget(rb_box, l2.rowCount() - 2, 0, Qt.AlignCenter)
    #
    #                 type_choice.setStandardButtons(QMessageBox.Cancel | QMessageBox.Apply)
    #
    #                 ret = type_choice.exec_()
    #
    #                 if ret == QtGui.QMessageBox.Apply:
    #
    #                     (f_path, f_name) = os.path.split(str(QFileDialog.getSaveFileName(self, "Browse Directory")))
    #
    #                     if all_opt.isChecked():
    #                         extract_data_from_selected()
    #                     elif centroid_opt.isChecked():
    #                         extract_data_as_centroids_from_selected()
    #
    #                 ee.simple_export(f_name, f_path, get_current_usableDataset())
    #
    #             else:
    #                 print("There was a problem in export options")
    #
    #     else:
    #         QtGui.QMessageBox.information(self, "Selection empty", "There's nothing to export.")
        print()

    def extract_and_cluster(self):
        # if get_selected():
        #     choice = QtGui.QMessageBox()
        #     choice.setWindowTitle('Extract data for clustering')
        #
        #     centroid_opt = QRadioButton("Use centroids as file representation")
        #     all_points_opt = QRadioButton("Use all region points for each file")
        #     all_points_opt.setChecked(True)
        #
        #     l = choice.layout()
        #     l.setContentsMargins(20, 0, 0, 20)
        #     l.addWidget(QLabel("You have selected (" + str(len(
        #         get_selected())) + ") image collections. \nThere is a total of ("
        #                        + str(
        #         get_selected_images_number()) + ") NIfTI images to be treated. \n\nPlease select the way "
        #                                         "you would like each file to be represented : "),
        #                 l.rowCount() - 3, 0, 1, l.columnCount() - 2, Qt.AlignCenter)
        #     rb_box = QtGui.QGroupBox()
        #     vbox = QtGui.QVBoxLayout()
        #     vbox.addWidget(all_points_opt)
        #     vbox.addWidget(centroid_opt)
        #
        #     rb_box.setLayout(vbox)
        #     l.addWidget(rb_box, l.rowCount() - 2, 0, Qt.AlignCenter)
        #
        #     choice.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        #
        #     ret = choice.exec_()
        #
        #     if ret == QtGui.QMessageBox.Yes:
        #
        #         if all_points_opt.isChecked():
        #             extract_data_from_selected()
        #
        #         elif centroid_opt.isChecked():
        #             extract_data_as_centroids_from_selected()
        #
        #         else:
        #             print("There was a problem in data extraction options")
        #
        #         self.showClust.emit()
        #
        # else:
        #     QtGui.QMessageBox.information(self, "Selection empty", "There's no data to extract and clusterize.")
        self.showClust.emit()
        print()

    def calcul(self):
        # if (get_selected()):
        #     self.showCalcul.emit()
        #
        # else:
        #     QtGui.QMessageBox.information(self, "Selection empty", "There's no data to calculation.")
        print()

    def edit_pannel(self):
        # -- This edit_pannel will show the edit view if selected is not empty
        # if (get_selected()):
        #     self.showEdit.emit()
        # else:
        #     QtGui.QMessageBox.information(self, "Selection empty", "There's no data to edit.")
        self.showEdit.emit()
        print()

    def show_set(self, new_set):
        # -- This show_set will add the new_set to the setAccessBox and display the current vizu that changed in the process
        set_current_set(new_set)
        self.treeWidget.addChild(QTreeWidgetItem(new_set))
        set_current_set(new_set)
        self.setAccessBox.add(new_set)
        self.updateVizu(get_current_vizu())

    def update(self):
        # -- This update will call the update function of collectionsDisplayBox
        self.collectionsDisplayBox.update()
        print()

    def updateVizu(self, newVizu):
        # -- This updateVizu will display the newVizu but not delete the old one to be able to chow it again later
        newVizu.update()
        self.collectionsDisplayBox = newVizu
        delete_me = self.splitter1.widget(1)
        delete_me.setParent(None)
        # DO NOT DO delete_me.deleteLater() -> we need it alive!
        self.splitter1.addWidget(newVizu)

    def upCollLabel(self):
        # -- This upCollLabel will display the name of the current set at top of the screen
        # label = get_current_set().name
        # limit = 500
        # if (len(label) > limit):
        #     nb = limit - len(label) + 1
        #     label = label[:nb] + "-"
        # self.collectionsDisplayBox.update_label(label)
        print()

    def updateClusterRes(self):
        #self.setAccessBox.add2()
        print()

    def updateCalculRes(self):
        #self.setAccessBox.add3()
        print()







    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "List of sets", None))
        self.treeWidget.headerItem().setText(0, _translate("Form", "List of set and subset", None))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("Form", "Imported", None))
        self.treeWidget.topLevelItem(1).setText(0, _translate("Form", "Calculation", None))
        self.treeWidget.topLevelItem(2).setText(0, _translate("Form", "Clustering", None))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.label_2.setText(_translate("Form", "Image collections", None))
        self.checkBox.setText(_translate("Form", "Select all", None))
        self.label_3.setText(_translate("Form", "Selected ", None))
        self.pushButton.setText(_translate("Form", "Edit", None))
        self.pushButton_2.setText(_translate("Form", "Export data", None))
        self.pushButton_4.setText(_translate("Form", "Clustering", None))
        self.pushButton_3.setText(_translate("Form", "Calculation", None))
