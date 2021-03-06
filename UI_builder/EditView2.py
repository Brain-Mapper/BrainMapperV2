# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Edit.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
from PyQt4 import QtGui
from PyQt4.Qt import *
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSignal

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from BrainMapper import *
import clustering_components.clustering_plot as clustering_plot
from ourLib.dataExtraction.extractor import *
from ourLib.dataExtraction.usable_data import *
from ourLib.calculations2 import image_centroid

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


class Buttonpath(QtGui.QWidget):
    def __init__(self, filna, coll, parent=None):
        super(Buttonpath, self).__init__(parent=parent)
        # self.setStyleSheet(self.stysetStyleler)
        self.parent = parent
        # self.image = coll.get_img_list().get(filna)
        self.image = None
        for i in coll.get_img_list().values():
            f = i.filename.split("/")
            file = f[len(f) - 1]
            if file == filna:
                # print(i)
                self.image = i

        hbox = QtGui.QHBoxLayout()

        self.buttonp = QtGui.QPushButton("   " + filna)
        # self.buttonp.clicked.connect(lambda: self.actionpath(filna,parent))
        hbox.addWidget(self.buttonp)

        ShowButtoncoll = QtGui.QPushButton()
        ShowButtoncoll.setIcon(QtGui.QIcon('ressources/app_icons_png/eye.png'))
        ShowButtoncoll.clicked.connect(lambda: self.showColl(coll, parent))
        ShowButtoncoll.setStatusTip("Show graphic of the entire set")
        ShowButtoncoll.setFixedSize(QSize(20, 20))
        hbox.addWidget(ShowButtoncoll)

        SupprButton = QtGui.QPushButton()
        SupprButton.setText("-")
        SupprButton.clicked.connect(lambda: self.deleteImg(coll, filna, parent))
        SupprButton.setStatusTip("Delete this set or subset")
        SupprButton.setFixedSize(QSize(20, 20))
        hbox.addWidget(SupprButton)

        self.setLayout(hbox)

    def showColl(self, coll, parent):
        choice = QtGui.QMessageBox()
        choice.setWindowTitle('Data representation')
        centroid_opt = QRadioButton("Use centroids as file representation")
        all_points_opt = QRadioButton("Use all region points for each file")
        all_points_opt.setChecked(True)
        l = choice.layout()
        l.setContentsMargins(20, 0, 0, 20)
        l.addWidget(QLabel("You have selected (" + str(len(
            get_selected())) + ") image collections. \nThere is a total of ("
                           + str(
            get_selected_images_number()) + ") NIfTI images to be treated. \n\nPlease select the way "
                                            "you would like each file to be represented : "),
                    l.rowCount() - 3, 0, 1, l.columnCount() - 2, Qt.AlignCenter)
        rb_box = QtGui.QGroupBox()
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(all_points_opt)
        vbox.addWidget(centroid_opt)
        rb_box.setLayout(vbox)
        l.addWidget(rb_box, l.rowCount() - 2, 0, Qt.AlignCenter)
        choice.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ret = choice.exec_()
        if ret == QtGui.QMessageBox.Yes:
            points = []
            if all_points_opt.isChecked():
                # dict = self.coll.get_img_list()
                # for i in dict:
                data = extract(self.image)
                for j in range(len(data)):
                    points.append((data[j][0], data[j][1], data[j][2]))
                clustering_plot.plot_3d(points)
            elif centroid_opt.isChecked():
                data = image_centroid(self.image)
                for j in range(len(data)):
                    points.append((data[j][0], data[j][1], data[j][2]))
                clustering_plot.plot_3d(points)

            else:
                pass
                # print("There was a problem in data extraction options")

    def deleteImg(self, coll, name, parent):
        # -- This del_col will delete the current collection
        global list_img
        choice = QtGui.QMessageBox.question(self, 'Delete Image',
                                            "Are you sure you want to delete this image?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if choice == QtGui.QMessageBox.Yes:
            dictcopy = dict(coll.get_img_list())
            ##print("dic avant",coll.get_img_list().values())
            for i in dictcopy.values():
                filname = i.filename.split("/")
                ##print(filname)
                ##print(name)
                find = filname[len(filname) - 1]
                if find == name:
                    # coll.get_img_list().remove(i)
                    ##print(coll.get_img_list().keys())
                    ##print(type(coll.get_img_list()))
                    del coll.get_img_list()[i.filename]
            ##print("dic final",coll.get_img_list().values())
            ##print(list_img)
            list_img.remove(name)
            ##print(list_img)
            for i in reversed(range(self.parent.verticalLayout_4.count())):
                self.parent.verticalLayout_4.itemAt(i).widget().setParent(None)
            for i in range(0, len(list_img)):
                # print("cc")
                buttonpath = Buttonpath(list_img[i], coll, parent)
                self.parent.verticalLayout_4.addWidget(buttonpath)
            # self.parent.label_10.setText("")
            # self.parent.pushButton_4.setEnabled(False)

        else:
            pass
            # print("test")

    # def actionpath(self,filna,parent):
    #     self.parent=parent
    #     self.parent.label_10.setText(filna)
    #     self.parent.pushButton_3.setEnabled(True)
    #     self.parent.pushButton_4.setEnabled(True)


class CollectionAccessButton(QtGui.QWidget):
    # -- The CollectionAccessButton class is a QPushButton that call showInfos from the EditCollectionsView it knows
    # styler = "CollectionAccessButton {background-color: white; border-bottom: 1px solid black;} " \
    # "#CollectionAccessButton:hover {background-color : #ccff99;}"

    def __init__(self, coll, parent=None):
        super(CollectionAccessButton, self).__init__(parent=parent)
        # self.setStyleSheet(self.stysetStyleler)
        self.parent = parent
        self.coll = coll

        hbox = QtGui.QHBoxLayout()

        self.buttonc = QtGui.QPushButton()
        self.buttonc.setText(coll.name)
        self.buttonc.clicked.connect(lambda: self.showInfos(coll, parent))
        hbox.addWidget(self.buttonc)

        NameButtoncoll = QtGui.QPushButton()
        NameButtoncoll.setIcon(QtGui.QIcon('ressources/app_icons_png/writing.png'))
        NameButtoncoll.clicked.connect(lambda: self.changeNamecoll(coll, parent))
        NameButtoncoll.setStatusTip("Change collection name")
        NameButtoncoll.setFixedSize(QSize(20, 20))
        hbox.addWidget(NameButtoncoll)

        ShowButtoncoll = QtGui.QPushButton()
        ShowButtoncoll.setIcon(QtGui.QIcon('ressources/app_icons_png/eye.png'))
        ShowButtoncoll.clicked.connect(lambda: self.showColl(coll, parent))
        ShowButtoncoll.setStatusTip("Show graphic of the entire set")
        ShowButtoncoll.setFixedSize(QSize(20, 20))
        hbox.addWidget(ShowButtoncoll)

        IButton = QtGui.QPushButton()
        IButton.setText("+")
        IButton.clicked.connect(lambda: self.addImage(coll, parent))
        IButton.setStatusTip("Add image in this collection")
        IButton.setFixedSize(QSize(20, 20))
        hbox.addWidget(IButton)

        SupprButtoncoll = QtGui.QPushButton()
        SupprButtoncoll.setText("-")
        SupprButtoncoll.clicked.connect(lambda: self.del_col(coll, parent))
        SupprButtoncoll.setStatusTip("Delete this collection")
        SupprButtoncoll.setFixedSize(QSize(20, 20))
        hbox.addWidget(SupprButtoncoll)

        self.setLayout(hbox)

    def showColl(self, coll, parent):
        choice = QtGui.QMessageBox()
        choice.setWindowTitle('Data representation')
        centroid_opt = QRadioButton("Use centroids as file representation")
        all_points_opt = QRadioButton("Use all region points for each file")
        all_points_opt.setChecked(True)
        l = choice.layout()
        l.setContentsMargins(20, 0, 0, 20)
        l.addWidget(QLabel("You have selected (" + str(len(
            get_selected())) + ") image collections. \nThere is a total of ("
                           + str(
            get_selected_images_number()) + ") NIfTI images to be treated. \n\nPlease select the way "
                                            "you would like each file to be represented : "),
                    l.rowCount() - 3, 0, 1, l.columnCount() - 2, Qt.AlignCenter)
        rb_box = QtGui.QGroupBox()
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(all_points_opt)
        vbox.addWidget(centroid_opt)
        rb_box.setLayout(vbox)
        l.addWidget(rb_box, l.rowCount() - 2, 0, Qt.AlignCenter)
        choice.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ret = choice.exec_()
        if ret == QtGui.QMessageBox.Yes:
            points = []
            if all_points_opt.isChecked():
                dict = self.coll.get_img_list()
                for i in dict:
                    data = extract(dict[i])
                    for j in range(len(data)):
                        points.append((data[j][0], data[j][1], data[j][2]))
                clustering_plot.plot_3d(points)
            elif centroid_opt.isChecked():
                dict = extract_from_collection_as_centroid(self.coll).get_extracted_data_dict()
                for i in dict:
                    data = dict[i]
                    for j in range(len(data)):
                        points.append((data[j][0], data[j][1], data[j][2]))
                clustering_plot.plot_3d(points)

            else:
                pass
                # print("There was a problem in data extraction options")

    def del_col(self, coll, parent):
        # -- This del_col will delete the current collection
        global list_img
        global collshow
        choice = QtGui.QMessageBox.question(self, 'Delete Collection',
                                            "Are you sure you want to delete this collection?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            set_current_coll(coll)
            delete_current_coll()
            # self.parent.label_10.setText("")
            # self.parent.pushButton_4.setEnabled(False)
            for i in reversed(range(self.parent.verticalLayout_3.count())):
                self.parent.verticalLayout_3.itemAt(i).widget().setParent(None)
            for i in reversed(range(self.parent.verticalLayout_4.count())):
                self.parent.verticalLayout_4.itemAt(i).widget().setParent(None)
            self.parent.label_4.setText("")
            self.parent.label_5.setText("")
            del list_img[:]
            collshow.remove(coll)
            # print("collshow final",collshow)
            self.parent.fill_coll()

    def changeNamecoll(self, coll, parent):
        # -- This changeNamecoll will change the name of the current collection

        set_current_coll(coll)
        text, ok = QInputDialog.getText(self, 'Change name of the Collection',
                                        "Enter a new name for the collection named " + get_current_coll().name + ": ")
        if str(text) != "":
            try:
                new_ok = True
                not_ok = ['^', '[', '<', '>', ':', ';', ',', '?', '"', '*', '|', '/', ']', '+', '$']
                for i in not_ok:
                    if i in str(text):
                        new_ok = False
                if new_ok and not exists_coll_in_sets(str(text)):
                    setColNameInSet(str(text))

                    self.buttonc.setText(coll.name)
                    self.parent.label_4.setText(coll.name)
                    # cur_col = get_current_coll()
                    # self.redo(cur_col)
                else:
                    err = QtGui.QMessageBox.critical(self, "Error",
                                                     "The new name you entered is not valid (empty, invalid caracter or already exists)")
            except:
                err = QtGui.QMessageBox.critical(self, "Error",
                                                 "The name you entered is not valid (" + str(sys.exc_info()[0]) + ")")

    def showInfos(self, coll, parent):
        # -- Reload the InfosBar with the collection named name
        self.parent = parent
        reset_toRM()
        set_current_coll(coll)
        # self.label_name.setText(str(col.name))
        self.parent.label_4.setText(str(coll.name))
        self.parent.label_5.setText(str(coll.set_n.name))
        if len(list_img) != 0:
            for i in reversed(range(self.parent.verticalLayout_4.count())):
                self.parent.verticalLayout_4.itemAt(i).widget().setParent(None)
            del list_img[:]
        for i in coll.get_img_list().values():
            filname = i.filename.split("/")
            filna = filname[len(filname) - 1]
            if filna not in list_img:
                list_img.append(filna)
                buttonpath = Buttonpath(filna, coll, parent)
                self.parent.verticalLayout_4.addWidget(buttonpath)

    def addImage(self, coll, parent):
        global list_img
        # del list_img[:]
        # for i in reversed(range(self.parent.verticalLayout_4.count())):
        #     self.parent.verticalLayout_4.itemAt(i).widget().setParent(None)
        # -- This addImage will add the images selected by the user in the current collection (ALLO THE USER TO ADD A FILE THAT ALREADY EXISTS IN THE COLLECTION)
        path = QFileDialog.getOpenFileNames()
        if (path != ""):
            try:
                add_image_coll(coll, path)
                # self.redo(get_current_coll())
                for i in coll.get_img_list().values():
                    # print("bjr")
                    filname = i.filename.split("/")
                    filna = filname[len(filname) - 1]
                    # print("cc")
                    if filna not in list_img:
                        list_img.append(filna)
                        # print("cc2")
                        buttonpath = Buttonpath(filna, coll, parent)
                        self.parent.verticalLayout_4.addWidget(buttonpath)
            except:
                err = QtGui.QMessageBox.critical(self, "Error",
                                                 "An error has occured. Maybe you tried to open a non-NIfTI file")
                # #print (sys.exc_info()[0])


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
        self.verticalLayout_3 = QtGui.QFormLayout(self.widget_6)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 9)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
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
        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)
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
        self.verticalLayout_4 = QtGui.QFormLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
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

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_8 = QtGui.QPushButton(Form)
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.pushButton_8.clicked.connect(self.go_back)
        self.horizontalLayout.addWidget(self.pushButton_8)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def go_back(self):
        # -- When the user wants to return to the main view, we reinit the cluster view
        global list_img
        del list_img[:]
        for i in reversed(range(self.verticalLayout_3.count())):
            self.verticalLayout_3.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.verticalLayout_4.count())):
            self.verticalLayout_4.itemAt(i).widget().setParent(None)
        self.label_4.setText("")
        self.label_5.setText("")

        self.showMain.emit()

    def plot(self):
        choice = QtGui.QMessageBox()
        choice.setWindowTitle('Data representation')
        centroid_opt = QRadioButton("Use centroids as file representation")
        all_points_opt = QRadioButton("Use all region points for each file")
        all_points_opt.setChecked(True)
        l = choice.layout()
        l.setContentsMargins(20, 0, 0, 20)
        l.addWidget(QLabel("You have selected (" + str(len(
            get_selected())) + ") image collections. \nThere is a total of ("
                           + str(
            get_selected_images_number()) + ") NIfTI images to be treated. \n\nPlease select the way "
                                            "you would like each file to be represented : "),
                    l.rowCount() - 3, 0, 1, l.columnCount() - 2, Qt.AlignCenter)
        rb_box = QtGui.QGroupBox()
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(all_points_opt)
        vbox.addWidget(centroid_opt)
        rb_box.setLayout(vbox)
        l.addWidget(rb_box, l.rowCount() - 2, 0, Qt.AlignCenter)
        choice.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ret = choice.exec_()
        if ret == QtGui.QMessageBox.Yes:
            points = []
            if all_points_opt.isChecked():
                dict = self.coll.get_img_list()
                for i in dict:
                    data = extract(dict[i])
                    for j in range(len(data)):
                        points.append((data[j][0], data[j][1], data[j][2]))
                clustering_plot.plot_3d(points)
            elif centroid_opt.isChecked():
                dict = extract_from_collection_as_centroid(self.coll).get_extracted_data_dict()
                for i in dict:
                    data = dict[i]
                    for j in range(len(data)):
                        points.append((data[j][0], data[j][1], data[j][2]))
                clustering_plot.plot_3d(points)

            else:
                pass
                # print("There was a problem in data extraction options")

        dict = get_current_coll().get_img_list()
        for i in dict:
            data = extract(dict[i])
        points = [[], [], []]
        for j in range(len(data)):
            points[0].append(data[j][0])
            points[1].append(data[j][1])
            points[2].append(data[j][2])
        clustering_plot.plot_3d(points)

    def fill_coll(self):
        # -- Remove the right CollectionsAccessBar and replace it with a column fill with all the collections selected

        # old = splitter1.widget(1)
        # containerVbox.removeWidget(old)
        # old.setParent(None)
        # old.deleteLater()
        colls = get_selected()
        # labels = []
        # print("colls",colls)
        for x in colls:
            # labels.append(x.name)
            topleft = CollectionAccessButton(x, self)
            ##print(labels)
            # topleft=CollectionsAccessBar(labels, self)
            # topleft=
            # for lab in labels_array :
            #     self.parent.verticalLayout_3.addWidget(CollectionAccessButton(lab, self.parent))

            self.verticalLayout_3.addWidget(topleft)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_8.setText(_translate("Form", "Selected image collection", None))
        self.label_9.setText(_translate("Form", "Selected image collection", None))
        self.label.setText(_translate("Form", "Collection name :", None))
        self.label_2.setText(_translate("Form", "Set name :", None))
        self.label_3.setText(_translate("Form", "List of images : ", None))
        # self.pushButton_4.setText(_translate("Form", "Show Graphic", None))
        # self.pushButton_3.setText(_translate("Form", "Remove", None))
        # self.pushButton_12.setText(_translate("Form", "Save changes", None))
        self.pushButton_8.setText(_translate("Form", "Go back", None))
