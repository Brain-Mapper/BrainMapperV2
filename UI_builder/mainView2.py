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

class CollButton(QtGui.QCheckBox):
    # -- The CollButton class is a QCheckBox that show all collection info

    def __init__(self, coll, parent=None):
        super(CollButton, self).__init__(parent=parent)
        self.coll = coll
        self.toggle()
        self.stateChanged.connect(self.selectColl)

        list = self.coll.get_img_list()

        try:
            dates = []
            for l in list:
                dates.append(creation_date(str(l)))
            date = max(dates)
            d = datetime.fromtimestamp(int(round(date))).strftime('%Y-%m-%d')
        except:
            d = datetime.fromtimestamp(int(round(time.time()))).strftime('%Y-%m-%d')
        label = "Name : " + str(self.coll.name) + "\nNIfTI : " + str(len(list)) + "\nLast modified : " + str(d)
        self.setText(label)
        self.setStyleSheet(
            "CollButton {background-color : #eee; spacing: 5px;border: 2px solid #99cccc;border-radius: 8px;padding: 1px 18px 1px 3px;max-width: 225%;}; CollButton::indicator {width: 13px; height: 13px;};")

    def selectColl(self):
        # -- This selectColl will add or delete the collection from the selected ones
        if (self.isChecked()):
            add_coll(self.coll)
        else:
            rm_coll(self.coll)

    def update(self):
        # -- This update will update the information of the collection if they have changed in the edit collection view
        list = self.coll.get_img_list()
        try:
            if list:
                dates = []
                for l in list:
                    dates.append(creation_date(str(l)))
                date = max(dates)
                d = datetime.fromtimestamp(int(round(date))).strftime('%Y-%m-%d')
            else:
                d = datetime.fromtimestamp(int(round(time.time()))).strftime('%Y-%m-%d')
        except:
            d = datetime.fromtimestamp(int(round(time.time()))).strftime('%Y-%m-%d')
        self.setText("Name : " + str(self.coll.name) + "\nNIfTI : " + str(len(list)) + "\nLast modified : " + str(d))

class SetButton(QtGui.QWidget):

    #styler = "SetButton {background-color: white; border-bottom: 1px solid black;} " \
      # "SetButton:hover {background-color : #ccff99;}"

    def __init__(self, my_set, destination, parent=None):
      # -- Will create all objects we need
      super(SetButton, self).__init__( parent=parent)

      self.my_set = my_set
      self.destination=destination

      hbox = QtGui.QHBoxLayout()

      self.check = QtGui.QCheckBox()
      self.check.setText(my_set.name)
      self.check.stateChanged.connect(self.state_changed)
      hbox.addWidget(self.check)

      SSButton = QtGui.QPushButton()
      SSButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/up-arrow.png'))
      SSButton.clicked.connect(self.addSubet)
      SSButton.setStatusTip("Add sub set")
      SSButton.setFixedSize(QSize(20, 20))
      hbox.addWidget(SSButton)

      NameButton = QtGui.QPushButton()
      NameButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/writing.png'))
      NameButton.clicked.connect(self.changeName)
      NameButton.setStatusTip("Change Set Name")
      NameButton.setFixedSize(QSize(20, 20))
      hbox.addWidget(NameButton)

      self.setLayout(hbox)

    def state_changed(self):
       dict=self.my_set.get_all_nifti_set()
       if self.check.isChecked():
           print("CHECKED!")
           print(dict not in selected)
           for d in dict:
               if d not in selected:
                   selected.append(d)
           print(selected)
       else:
           for d in dict:
               selected.remove(d)
           print("UNCHECKED!")
           print(selected)
       for i in reversed(range(self.destination.count())):
           self.destination.itemAt(i).widget().setParent(None)
       for coll in selected:
               self.destination.addWidget(CollButton(coll))

    def changeName(self):
        # -- This changeName will change the name of the set selected.
        text, ok = QInputDialog.getText(self, 'Rename a set',
                                        "Enter a new name for your set currently named " + str(self.my_set.name) + ":")
        if (str(text) != ""):
            try:
                new_ok = True
                not_ok = ['^', '[', '<', '>', ':', ';', ',', '?', '"', '*', '|', '/', ']', '+', '$']
                for i in not_ok:
                    if i in str(text):
                        new_ok = False
                if new_ok and not exists_set(str(text)):
                    rm_set(self.my_set)
                    if (self.my_set.getParent() != None):  # if its a subset
                        self.my_set.getParent().remove_subset(self.my_set.get_name())
                        self.my_set.set_name(str(text))
                        self.my_set.getParent().add_subset(self.my_set)
                    else:
                        self.my_set.set_name(str(text))
                    self.check.setText(str(text))
                    print()
                    rec = QApplication.desktop().availableGeometry()
                    mainwind_h = rec.height()
                    mainwind_w = rec.width()
                    add_set(self.my_set)
                    self.parent().parent().parent().parent().parent().parent().update()
                else:
                    err = QtGui.QMessageBox.critical(self, "Error",
                                                     "The name you entered is not valid (empty, invalid caracter or already exists)")
            except:
                err = QtGui.QMessageBox.critical(self, "Error",
                                                 "The name you entered is not valid (" + str(sys.exc_info()[0]) + ")")

    def current_set(self):
        # -- This current_set will vizualize the set and the collections inside when pressed
        set_current_set(self.my_set)
        set_current_vizu(self.vizu)
        self.parent().parent().parent().parent().parent().parent().parent().parent().parent().updateVizu(self.vizu)
        self.parent().parent().parent().parent().parent().parent().parent().parent().parent().upCollLabel()

    def addSubet(self):
        # -- This addSubet will add a subset to the set selected.
        text, ok = QInputDialog.getText(self, 'Create a Sub Set',
                                        "Enter a name for your sub set of set named " + str(self.my_set.name) + ":")
        if (str(text) != ""):
            try:
                new_ok = True
                not_ok = ['^', '[', '<', '>', ':', ';', ',', '?', '"', '*', '|', '/', ']', '+', '$']
                for i in not_ok:
                    if i in str(text):
                        new_ok = False
                if new_ok and not exists_set(str(text)):
                    self.my_set.add_empty_subset(str(text))
                    self.SSList.addItem(str(text))
                    print("coucou")
                    ssSet = self.my_set.get_sub_set(str(text))
                    print("coucou2")
                    self.my_set.get_sub_set(str(text)).setParent(self.my_set)
                    add_set(ssSet)
                    set_current_set(ssSet)
                    self.parent().parent().parent().parent().parent().parent().parent().add(ssSet)
                else :
                    err = QtGui.QMessageBox.critical(self, "Error", "The name you entered is not valid (empty, invalid caracter or already exists)")
            except :
                err = QtGui.QMessageBox.critical(self, "Error", "The name you entered is not valid ("+str(sys.exc_info()[0])+")")

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
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1000, 650)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget_list_of_sets = QtGui.QWidget(Form)
        self.widget_list_of_sets.setMinimumSize(QtCore.QSize(250, 0))
        self.widget_list_of_sets.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.widget_list_of_sets.setObjectName(_fromUtf8("widget_list_of_sets"))
        self.verticalLayout_list_of_sets = QtGui.QVBoxLayout(self.widget_list_of_sets)
        self.verticalLayout_list_of_sets.setContentsMargins(0, 6, 0, 0)
        self.verticalLayout_list_of_sets.setSpacing(0)
        self.verticalLayout_list_of_sets.setObjectName(_fromUtf8("verticalLayout_list_of_sets"))
        self.label_list_of_sets = QtGui.QLabel(self.widget_list_of_sets)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_list_of_sets.setFont(font)
        self.label_list_of_sets.setAlignment(QtCore.Qt.AlignCenter)
        self.label_list_of_sets.setObjectName(_fromUtf8("label_list_of_sets"))
        self.verticalLayout_list_of_sets.addWidget(self.label_list_of_sets)
        self.treeWidget = QtGui.QTreeWidget(self.widget_list_of_sets)
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
        self.verticalLayout_list_of_sets.addWidget(self.treeWidget)
        self.horizontalLayout.addWidget(self.widget_list_of_sets)

        ################# image collections ###################################""
        self.widget_image_collections = QtGui.QWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_image_collections.sizePolicy().hasHeightForWidth())
        self.widget_image_collections.setSizePolicy(sizePolicy)
        self.widget_image_collections.setMinimumSize(QtCore.QSize(250, 200))
        self.widget_image_collections.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.widget_image_collections.setObjectName(_fromUtf8("widget_image_collections"))
        self.verticalLayout_image_collections = QtGui.QVBoxLayout(self.widget_image_collections)
        self.verticalLayout_image_collections.setContentsMargins(0, 6, 0, 0)
        self.verticalLayout_image_collections.setSpacing(0)
        self.verticalLayout_image_collections.setObjectName(_fromUtf8("verticalLayout_image_collections"))
        self.label_image_collections = QtGui.QLabel(self.widget_image_collections)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_image_collections.setFont(font)
        self.label_image_collections.setMouseTracking(False)
        self.label_image_collections.setAlignment(QtCore.Qt.AlignCenter)
        self.label_image_collections.setObjectName(_fromUtf8("label_image_collections"))
        self.verticalLayout_image_collections.addWidget(self.label_image_collections)
        self.checkBox = QtGui.QCheckBox(self.widget_image_collections)
        self.checkBox.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout_image_collections.addWidget(self.checkBox)
        self.widget_image_collections_show = QtGui.QWidget(self.widget_image_collections)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_image_collections_show.sizePolicy().hasHeightForWidth())
        self.widget_image_collections_show.setSizePolicy(sizePolicy)
        self.widget_image_collections_show.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget_image_collections_show.setObjectName(_fromUtf8("widget_image_collections_show"))
        self.verticalLayout_image_collections_show = QtGui.QFormLayout(self.widget_image_collections_show)
        self.verticalLayout_image_collections_show.setMargin(0)
        self.verticalLayout_image_collections_show.setObjectName(_fromUtf8("verticalLayout_image_collections_show"))
        self.verticalLayout_image_collections.addWidget(self.widget_image_collections_show)

        self.checkBox_collection = QtGui.QCheckBox(self.widget_image_collections_show)
        self.checkBox_collection.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.checkBox_collection.setObjectName(_fromUtf8("checkBox_collection"))
        self.verticalLayout_image_collections_show.addWidget(self.checkBox_collection)

        self.label_image_collections.raise_()
        self.widget_image_collections_show.raise_()
        self.checkBox.raise_()
        self.horizontalLayout.addWidget(self.widget_image_collections)
        self.verticalLayout_selected = QtGui.QVBoxLayout()
        self.verticalLayout_selected.setSpacing(6)
        self.verticalLayout_selected.setObjectName(_fromUtf8("verticalLayout_selected"))
        self.widget_selected = QtGui.QWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_selected.sizePolicy().hasHeightForWidth())
        self.widget_selected.setSizePolicy(sizePolicy)
        self.widget_selected.setMinimumSize(QtCore.QSize(50, 150))
        self.widget_selected.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.widget_selected.setObjectName(_fromUtf8("widget_selected"))
        self.verticalLayout_selected_view = QtGui.QVBoxLayout(self.widget_selected)
        self.verticalLayout_selected_view.setContentsMargins(0, 6, 0, 0)
        self.verticalLayout_selected_view.setSpacing(0)
        self.verticalLayout_selected_view.setObjectName(_fromUtf8("verticalLayout_selected_view"))
        self.label_selected = QtGui.QLabel(self.widget_selected)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_selected.setFont(font)
        self.label_selected.setMouseTracking(False)
        self.label_selected.setAlignment(QtCore.Qt.AlignCenter)
        self.label_selected.setObjectName(_fromUtf8("label_selected"))
        self.verticalLayout_selected_view.addWidget(self.label_selected)
        self.widget_selected_view = QtGui.QWidget(self.widget_selected)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_selected_view.sizePolicy().hasHeightForWidth())
        self.widget_selected_view.setSizePolicy(sizePolicy)
        self.widget_selected_view.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget_selected_view.setObjectName(_fromUtf8("widget_selected_view"))
        self.verticalLayout_selected_view.addWidget(self.widget_selected_view)
        self.verticalLayout_selected.addWidget(self.widget_selected)
        self.horizontalLayout_buttons = QtGui.QHBoxLayout()
        self.horizontalLayout_buttons.setSpacing(6)
        self.horizontalLayout_buttons.setObjectName(_fromUtf8("horizontalLayout_buttons"))
        self.pushButton_edit = QtGui.QPushButton(Form)
        self.pushButton_edit.setObjectName(_fromUtf8("pushButton_edit"))
        self.horizontalLayout_buttons.addWidget(self.pushButton_edit)
        self.pushButton_export = QtGui.QPushButton(Form)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.horizontalLayout_buttons.addWidget(self.pushButton_export)
        self.pushButton_clustering = QtGui.QPushButton(Form)
        self.pushButton_clustering.setObjectName(_fromUtf8("pushButton_clustering"))
        self.horizontalLayout_buttons.addWidget(self.pushButton_clustering)
        self.pushButton_calculation = QtGui.QPushButton(Form)
        self.pushButton_calculation.setObjectName(_fromUtf8("pushButton_calculation"))
        self.horizontalLayout_buttons.addWidget(self.pushButton_calculation)
        self.verticalLayout_selected.addLayout(self.horizontalLayout_buttons)
        self.horizontalLayout.addLayout(self.verticalLayout_selected)
        self.widget_image_collections.raise_()
        self.widget_list_of_sets.raise_()

        default_name = datetime.fromtimestamp(int(round(time.time()))).strftime('--%m-%d %H-%M')
        my_set = newSet(default_name[2:])
        set_current_set(my_set)
        print(get_current_set().get_name())

        item_0 = QtGui.QTreeWidgetItem(self.treeWidget.topLevelItem(0))
        item_0.setFlags(QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.treeWidget.setItemWidget(self.treeWidget.topLevelItem(0).child(0), 0, SetButton(my_set,self.verticalLayout_image_collections_show,self.treeWidget))

        # item_0 = QtGui.QTreeWidgetItem(self.treeWidget.topLevelItem(0).child(0))
        # item_0.setFlags(QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        # self.treeWidget.setItemWidget(self.treeWidget.topLevelItem(0).child(0).child(0), 0, SetButton(my_set,self.treeWidget))


        self.pushButton_clustering.clicked.connect(self.extract_and_cluster)
        self.pushButton_edit.clicked.connect(self.edit_pannel)

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
        self.label_list_of_sets.setText(_translate("Form", "List of sets", None))
        self.treeWidget.headerItem().setText(0, _translate("Form", "List of set and subset", None))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("Form", "Imported", None))
        self.treeWidget.topLevelItem(1).setText(0, _translate("Form", "Calculation", None))
        self.treeWidget.topLevelItem(2).setText(0, _translate("Form", "Clustering", None))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.label_image_collections.setText(_translate("Form", "Image collections", None))
        self.checkBox.setText(_translate("Form", "Select all", None))
        self.checkBox_collection.setText(_translate("Form", "collection1", None))
        self.label_selected.setText(_translate("Form", "Selected ", None))
        self.pushButton_edit.setText(_translate("Form", "Edit", None))
        self.pushButton_export.setText(_translate("Form", "Export data", None))
        self.pushButton_clustering.setText(_translate("Form", "Clustering", None))
        self.pushButton_calculation.setText(_translate("Form", "Calculation", None))
