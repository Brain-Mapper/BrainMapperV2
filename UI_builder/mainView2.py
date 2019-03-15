# -*- coding: utf-8 -*-

import sys
from datetime import *
from os import path

# Form implementation generated from reading ui file 'mainView.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!
import nibabel
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *
from PyQt4.QtCore import pyqtSignal

import ourLib.calculations2 as calculations

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from BrainMapper import *
import ourLib.ExcelExport.excelExport as ee
import ourLib.filesHandlers.image as im
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


class SelectedButton(QtGui.QPushButton):

    def __init__(self, coll, num, setname, date, parent=None):
        super(SelectedButton, self).__init__(parent=parent)
        self.coll = coll
        self.setname = setname
        self.num = num
        self.date = date

        self.setText("Set name : " + str(self.setname) + "\nName : " + str(
            self.coll.name) + "\nImage(s) : " + self.num + "\nLast modified : " + self.date)


class CollButton(QtGui.QCheckBox):
    # -- The CollButton class is a QCheckBox that show all collection info

    def __init__(self, coll, setname, selected_zone, checkBox, parent=None):
        super(CollButton, self).__init__(parent=parent)
        self.coll = coll
        self.setname = setname
        self.selected_zone = selected_zone
        self.checkBox = checkBox
        self.toggle()
        self.setChecked(False)
        self.stateChanged.connect(lambda: self.selectColl(self.setname))

        self.list = self.coll.get_img_list()

        try:
            dates = []
            for l in self.list:
                dates.append(creation_date(str(l)))
            date = max(dates)
            self.d = datetime.fromtimestamp(int(round(date))).strftime('%Y-%m-%d')
        except:
            self.d = datetime.fromtimestamp(int(round(time.time()))).strftime('%Y-%m-%d')
        label = "Set name : " + str(self.setname) + "\nName : " + str(self.coll.name) + "\nImage(s) : " + str(
            len(self.list)) + "\nLast modified : " + str(self.d)
        self.setText(label)
        self.setStyleSheet(
            "CollButton { spacing: 5px;border: 2px solid #000000;border-radius: 8px;padding: 1px 18px 1px 3px;};")
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(0)
        self.setSizePolicy(sizePolicy)

    def selectColl(self, setname):
        # -- This selectColl will add or delete the collection from the selected ones
        # self.selected_zone.addWidget(SelectedButton(self.coll,str(len(self.coll.get_img_list())),str(datetime.fromtimestamp(int(round(time.time()))).strftime('%Y-%m-%d'))))
        if (self.isChecked()):
            if self.coll not in collshow:
                collshow.append(self.coll)
        else:
            if self.coll in collshow:
                collshow.remove(self.coll)
            if len(collshow) == 0:
                self.checkBox.setChecked(False)
        for i in reversed(range(self.selected_zone.count())):
            self.selected_zone.itemAt(i).widget().setParent(None)
        for coll in collshow:
            self.selected_zone.addWidget(
                SelectedButton(coll, str(len(coll.get_img_list())), coll.getSetName().get_name(),
                               str(datetime.fromtimestamp(int(round(time.time()))).strftime('%Y-%m-%d'))))

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
        self.setText("Set name : " + str(self.setname) + "\nName : " + str(self.coll.name) + "\nImage(s) : " + str(
            len(list)) + "\nLast modified : " + str(d))


class SetButton(QtGui.QWidget):

    # styler = "SetButton {background-color: white; border-bottom: 1px solid black;} " \
    # "SetButton:hover {background-color : #ccff99;}"

    def __init__(self, my_set, image_zone, selected_zone, checkbox, checkimported, checkcalculation, checkclustering,
                 parent=None):
        # -- Will create all objects we need
        super(SetButton, self).__init__(parent=parent)

        self.my_set = my_set
        self.image_zone = image_zone
        self.selected_zone = selected_zone
        self.treeWidget = parent
        self.checkBox = checkbox
        self.checkimported = checkimported
        self.checkcalculation = checkcalculation
        self.checkclustering = checkclustering
        self.parent = parent

        hbox = QtGui.QHBoxLayout()

        self.check = QtGui.QCheckBox()
        self.check.setText(my_set.name)
        self.check.stateChanged.connect(self.state_changed)
        hbox.addWidget(self.check)
        ##print("pos", self.my_set.position)

        if self.my_set.position == 0:
            SSButton = QtGui.QPushButton()
            SSButton.setText("+")
            SSButton.clicked.connect(self.addSubet)
            SSButton.setStatusTip("Add sub set")
            SSButton.setFixedSize(QSize(20, 20))
            hbox.addWidget(SSButton)

        SupprButton = QtGui.QPushButton()
        SupprButton.setText("-")
        SupprButton.clicked.connect(self.deleteSet)
        SupprButton.setStatusTip("Delete this set or subset")
        SupprButton.setFixedSize(QSize(20, 20))
        hbox.addWidget(SupprButton)

        NameButton = QtGui.QPushButton()
        NameButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/writing.png'))
        NameButton.clicked.connect(self.changeName)
        NameButton.setStatusTip("Change Set Name")
        NameButton.setFixedSize(QSize(20, 20))
        hbox.addWidget(NameButton)

        if self.my_set.position == 0:
            ImportButton = QtGui.QPushButton()
            ImportButton.setText("Import")
            ImportButton.clicked.connect(self.importdata)
            ImportButton.setStatusTip("Import Data inside this set")
            ImportButton.setFixedSize(QSize(50, 20))
            hbox.addWidget(ImportButton)

        self.setLayout(hbox)

    def fromNiFile(self):
        # -- We create a collection with the list of images the user selected and give it to the main view and the edit view

        file = QFileDialog.getOpenFileNames(self, "Choose one file or more",
                                            "./", 'NifTI(*.nii *.nii.gz)')
        if (len(file) != 0):
            # TODO put the try/except
            # try:
            collec = do_image_collection(file, self.my_set)
            self.check.setChecked(True)
            # homepage.mainview.show_coll(collec)
            # homepage.edit_colls.fill_coll() #rapport a editview2
            # except Error as error:
            #     ##print(error)
            #     err = QtGui.QMessageBox.critical(self, "Error", "An error has occured. Maybe you tried to open a non-NIfTI file")

        # -- We create a collection with the list of images the user selected and give it to the main view and the edit view

    def fromExcel(self):
        file_name = QFileDialog.getOpenFileName(self, "Choose one file",
                                                "./", 'CSV(*.csv);;Excel files(*.xlsx *.xls)')
        if (len(file_name) != 0):
            # try:
            collec = simple_import(file_name, 'ressources/template_mni/mni_icbm152_t1_tal_nlin_asym_09a.nii',
                                   self.my_set)
            self.check.setChecked(True)
            # homepage.mainview.show_coll(collec)
            # homepage.edit_colls.fill_coll() #rapport a editview2
            # except:
            #     err = QtGui.QMessageBox.critical(self, "Error",
            #                                      "An error has occured. Maybe you tried to open a non-CSV file")

    def importdata(self):

        import_choice = QtGui.QMessageBox()
        import_choice.setWindowTitle('Import collections')

        self.check.setChecked(False)

        nifti_opt = QRadioButton("Import from NIfTI")
        excel_opt = QRadioButton("Import from Excel")
        nifti_opt.setChecked(True)

        l1 = import_choice.layout()
        l1.setContentsMargins(20, 0, 0, 20)
        # l1.addWidget(QLabel("You have selected (" + str(len(
        #     get_selected())) + ") image collections. \nThere is a total of (" + str(get_selected_images_number()) +
        #                     ") NIfTI images to be treated. \nPlease select the way "
        #                     "you would like to export these files : "),
        #              l1.rowCount() - 3, 0, 1, l1.columnCount() - 2, Qt.AlignCenter)
        rb_box = QtGui.QGroupBox()
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(nifti_opt)
        vbox.addWidget(excel_opt)

        rb_box.setLayout(vbox)
        l1.addWidget(rb_box, l1.rowCount() - 2, 0, Qt.AlignCenter)

        import_choice.setStandardButtons(QMessageBox.Cancel | QMessageBox.Apply)

        ret = import_choice.exec_()

        if ret == QtGui.QMessageBox.Apply:
            if nifti_opt.isChecked():
                self.fromNiFile()

            elif excel_opt.isChecked():
                self.fromExcel()

    def state_changed(self):
        global selected_images_collections
        global collshow
        dict = self.my_set.get_all_nifti_set()

        if self.check.isChecked():
            for d in dict:
                if d not in selected_images_collections:
                    selected_images_collections.append(d)
                    self.image_zone.addWidget(
                        CollButton(d, d.getSetName().get_name(), self.selected_zone, self.checkBox))
        else:
            for d in dict:
                selected_images_collections.remove(d)
                trouve = False
                i = 0
                while trouve == False and i < self.image_zone.count():
                    # #for i in reversed(range(self.image_zone.count())):
                    if self.image_zone.itemAt(i).widget().coll == d and self.image_zone.itemAt(
                            i).widget().setname == self.my_set.name:
                        trouve = True
                    else:
                        i = i + 1
                if trouve:
                    self.image_zone.itemAt(i).widget().setParent(None)
                trouve = False
                i = 0
                while trouve == False and i < self.selected_zone.count():
                    if self.selected_zone.itemAt(i).widget().coll == d and self.selected_zone.itemAt(
                            i).widget().setname == self.my_set.name:
                        trouve = True
                    else:
                        i = i + 1
                if trouve == True:
                    self.selected_zone.itemAt(i).widget().setParent(None)
                    collshow.remove(d)

        pos = self.my_set.position
        imported = self.parent.topLevelItem(pos)
        it = QTreeWidgetItemIterator(self.treeWidget.topLevelItem(pos))
        trouve = False
        while it.value():
            if it.value().parent() is not None:
                if self.treeWidget.itemWidget(it.value(), 0).check.isChecked():
                    trouve = True
            it += 1
        # ##print(pos)
        if trouve == False:
            if pos == 0:
                self.checkimported.setChecked(False)
            elif pos == 1:
                self.checkcalculation.setChecked(False)
            elif pos == 2:
                self.checkclustering.setChecked(False)

        # for i in reversed(range(self.image_zone.count())):
        #     ##print("boucle widget",self.image_zone.itemAt(i).widget().coll)
        #     self.image_zone.itemAt(i).widget().setParent(None)
        # for i in reversed(range(self.selected_zone.count())):
        #     self.selected_zone.itemAt(i).widget().setParent(None)

        # if self.check.isChecked():
        #     for coll in selected:
        #         trouve = False
        #         for i in reversed(range(self.image_zone.count())):
        #             if self.image_zone.itemAt(i).widget().coll == coll:
        #                 trouve = True
        #                 break;
        #         if trouve == False:
        #             self.image_zone.addWidget(CollButton(coll,coll.getSetName().get_name(),self.selected_zone))

        # BUG A CORRIGER QUAND ON CLIQUE SUR ALL ET QU IL Y A PLUS D UN ITEM
        # for coll in collshow:
        #     self.selected_zone.addWidget(SelectedButton(coll,str(len(coll.get_img_list())),my_set.get_name(),str(datetime.fromtimestamp(int(round(time.time()))).strftime('%Y-%m-%d'))))

    def changeName(self):
        # -- This changeName will change the name of the set selected.
        text, ok = QInputDialog.getText(self, 'Rename a set',
                                        "Enter a new name for your set currently named " + str(self.my_set.name) + ":")
        if (str(text) != ""):
            try:
                new_ok = True
                not_ok = ['^', '[', '<', '>', ':', ';', ',', '?', '"', '*', '|', '/', ']', '+', '$']
                if len(text) == 0:
                    new_ok = False
                for i in not_ok:
                    if i in str(text):
                        new_ok = False
                if new_ok and not exists_set(str(text)):
                    rm_set(self.my_set)
                    if (self.my_set.getParent() is not None):  # if its a subset
                        self.my_set.getParent().remove_subset(self.my_set.get_name())
                        self.my_set.set_name(str(text))
                        self.my_set.getParent().add_subset(self.my_set)
                    else:
                        self.my_set.set_name(str(text))
                    # ##print(self.my_set.get_name())
                    self.check.setText(str(text))
                    add_set(self.my_set)

                    # si on change le nom d'un set, il faut changer l'affichage graphique
                    listes = self.my_set.get_all_nifti_set_and_subset()
                    for i in reversed(range(self.image_zone.count())):
                        for elem in listes:
                            if self.image_zone.itemAt(i) is not None:
                                if self.image_zone.itemAt(i).widget().coll.name == elem.get_name():
                                    collbutton = self.image_zone.itemAt(i).widget()
                                    collbutton.setname = str(text)
                                    ##print(collbutton.coll.name)
                                    label = "Set name : " + str(collbutton.setname) + "\nName : " + str(
                                        collbutton.coll.name) + "\nImage(s) : " + str(
                                        len(collbutton.list)) + "\nLast modified : " + str(collbutton.d)
                                    ##print("label", label)
                                    collbutton.setText(label)

                    for i in reversed(range(self.selected_zone.count())):
                        for elem in listes:
                            if self.selected_zone.itemAt(i) is not None:
                                if self.selected_zone.itemAt(i).widget().coll.name == elem.get_name():
                                    selectedbutton = self.selected_zone.itemAt(i).widget()
                                    selectedbutton.setname = str(text)
                                    label = "Set name : " + str(selectedbutton.setname) + "\nName : " + str(
                                        selectedbutton.coll.name) + "\nImage(s) : " + selectedbutton.num + "\nLast modified : " + selectedbutton.date
                                    selectedbutton.setText(label)

                else:
                    err = QtGui.QMessageBox.critical(self, "Error",
                                                     "The name you entered is not valid (empty, invalid caracter or already exists)")
            except:
                err = QtGui.QMessageBox.critical(self, "Error",
                                                 "The name you entered is not valid (" + str(sys.exc_info()[0]) + ")")

    def addSubet(self):
        # -- This addSubet will add a subset to the set selected.
        text, ok = QInputDialog.getText(self, 'Create a Sub Set',
                                        "Enter a name for your sub set of set named " + str(self.my_set.name) + ":")
        # self.checkBox.setChecked(False)
        # self.checkimported.setChecked(False)
        if (str(text) != ""):
            try:
                new_ok = True
                not_ok = ['^', '[', '<', '>', ':', ';', ',', '?', '"', '*', '|', '/', ']', '+', '$']
                if len(text) == 0:
                    new_ok = False
                for i in not_ok:
                    if i in str(text):
                        new_ok = False
                if new_ok and not exists_set(str(text)):
                    # ##print("test")
                    ##print("position du set courant dans l arbre", self.my_set.position_arbre)
                    number_of_subset = len(self.my_set.subset_dict)
                    ##print("number of subset", number_of_subset)
                    position_arbre = self.my_set.position_arbre
                    position_arbre_nouveau = list(position_arbre)
                    position_arbre_nouveau.append(number_of_subset)
                    ss = self.my_set.add_empty_subset(str(text), position_arbre_nouveau)
                    ##print("position du subset", ss.position_arbre)
                    p = self.treeWidget.topLevelItem(0)
                    for i in range(len(position_arbre_nouveau) - 1):
                        p = p.child(position_arbre_nouveau[i])

                    ##print(self.treeWidget.itemWidget(p, 0).my_set.name)

                    item_0 = QtGui.QTreeWidgetItem(p)
                    item_0.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    self.treeWidget.setItemWidget(p.child(position_arbre_nouveau[-1]), 0,
                                                  SetButton(ss, self.image_zone, self.selected_zone,
                                                            self.checkBox, self.checkimported, self.checkcalculation,
                                                            self.checkclustering, self.treeWidget))
                    self.my_set.get_sub_set(str(text)).setParent(self.my_set)
                    add_set(ss)
                    set_current_set(ss)
                else:
                    err = QtGui.QMessageBox.critical(self, "Error",
                                                     "The name you entered is not valid (empty, invalid caracter or already exists)")
            except TypeError as e:
                ##print(e)
                err = QtGui.QMessageBox.critical(self, "Error",
                                                 "The name you entered is not valid (" + str(sys.exc_info()[0]) + ")")

    def deleteSet(self):

        def changementindice(set, indice_a_modif):
            ##print("len", len(set.getAllSubSets()))
            if len(set.getAllSubSets()) == 0:
                # ##print("subset pos arbre avant",set.position_arbre)
                # set.position_arbre[indice_a_modif]=set.position_arbre[indice_a_modif]-1
                # ##print("subset pos arbre apres",set.position_arbre)
                pass
            else:
                for subset in set.getAllSubSets():
                    # ##print("subset pos arbre avant",set.position_arbre)
                    subset.position_arbre[indice_a_modif] = subset.position_arbre[indice_a_modif] - 1
                    # ##print("subset pos arbre apres",set.position_arbre)
                    changementindice(subset, indice_a_modif)

        def deletebackdata(set):
            ##print("len", len(set.getAllSubSets()))
            if len(set.getAllSubSets()) == 0:
                sets.remove(set)
            else:
                for subset in set.getAllSubSets():
                    if set in sets:
                        sets.remove(set)
                    deletebackdata(subset)

        global selected_images_collections
        global collshow
        choice = QtGui.QMessageBox.question(self, 'Delete', "Are you sure to delete this set and all its sub-sets ?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            position = self.my_set.getPosition()
            indice_racine = self.my_set.position
            p = self.treeWidget.topLevelItem(indice_racine)
            position_arbre = self.my_set.position_arbre
            ##print("position_arbre", position_arbre)
            # position_arbre=list(position_arbre)

            # ##print("indice racine",indice_racine)
            # ##print("globalSets before", globalSets)

            if indice_racine == 1 or indice_racine == 2:
                it = QTreeWidgetItemIterator(p)
                while it.value():
                    if it.value().parent() is not None and it.value().parent() == p:
                        button = self.treeWidget.itemWidget(it.value(), 0)
                        if button.my_set == self.my_set:  # Si on trouve pas on doit parcourir les subset eventuels.
                            ##print("trouvé", button.my_set.name)
                            p.removeChild(it.value())
                    it += 1
            elif indice_racine == 0:
                if self.my_set.getParent() is not None:
                    for i in range(0, len(position_arbre) - 1):
                        # ##print("position_arbre avant", position_arbre)
                        p = p.child(position_arbre[0])
                        position_arbre.pop(0)
                        # ##print("position_arbre apres", position_arbre)
                        # ##print("p",p)
                else:
                    globalSets[indice_racine].remove(self.my_set)

                p.removeChild(p.child(position_arbre[0]))

            for d in self.my_set.get_all_nifti_set_and_subset():
                if d in selected_images_collections:
                    selected_images_collections.remove(d)
                if d in collshow:
                    collshow.remove(d)

            ##print("sets avant", sets)
            deletebackdata(self.my_set)
            ##print("sets apres", sets)

            listes = self.my_set.get_all_nifti_set_and_subset()

            if self.my_set.getParent() is not None:
                self.my_set.getParent().remove_subset(self.my_set.name)
                indice_a_modif = len(position_arbre)
                ##print("indice_a_modif", indice_a_modif)
                for set in self.my_set.getParent().getAllSubSets():
                    if set != self and set.position_arbre[indice_a_modif] > position_arbre[0]:
                        ###print("set pos arbre avant", set.position_arbre)
                        set.position_arbre[indice_a_modif] = set.position_arbre[indice_a_modif] - 1
                        ##print("set pos arbre apres", set.position_arbre)
                        changementindice(set, indice_a_modif)

                        # set.position -= 1
            # else:
            #     globalSets[indice_racine].remove(self.my_set)
            # for s in globalSets[indice_racine]:
            #     if s.position > self.my_set.position:
            #         s.position -= 1

            # ##print("globalSets after", globalSets)

            # lorsqu'on supprimer un set il faut changer l'affichage graphique
            # ##print("listes",listes)
            for i in reversed(range(self.image_zone.count())):
                for elem in listes:
                    if self.image_zone.itemAt(i) is not None:
                        if self.image_zone.itemAt(i).widget().coll.name == elem.get_name():
                            self.image_zone.itemAt(i).widget().setParent(None)

            for i in reversed(range(self.selected_zone.count())):
                for elem in listes:
                    if self.selected_zone.itemAt(i) is not None:
                        # ##print('name',self.selected_zone.itemAt(i).widget().coll.name)
                        if self.selected_zone.itemAt(i).widget().coll.name == elem.get_name():
                            self.selected_zone.itemAt(i).widget().setParent(None)


class MainView2(QtGui.QWidget):
    showClust = pyqtSignal()
    showEdit = pyqtSignal()
    showExport = pyqtSignal()
    showCalcul = pyqtSignal()
    showSOM = pyqtSignal()

    def __init__(self):
        super(MainView2, self).__init__()

        self.setupUi(self)

    def setupUi(self, Form):
        # Form.setObjectName(_fromUtf8("Form"))
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
        self.widget_list_of_sets.setMinimumSize(QtCore.QSize(400, 0))
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
        self.treeWidget.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"
                                                "border-color: rgb(255, 255, 255);"))
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.treeWidget.headerItem().setFont(0, font)
        self.treeWidget.headerItem().setBackground(0, QtGui.QColor(0, 0, 0, 0))

        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item = QWidget()
        itemLayout = QtGui.QHBoxLayout(item)
        itemLayout.setContentsMargins(3, 9, 9, 3)
        self.checkimported = QtGui.QCheckBox()
        self.checkimported.setText("Imported")
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.checkimported.setFont(font)
        self.checkimported.setStyleSheet("color: rgb(82, 99, 141);" "font-size: 9pt;")
        self.checkimported.stateChanged.connect(self.checkimportedall)
        itemLayout.addWidget(self.checkimported)
        addButton = QtGui.QPushButton()
        addButton.setText("+")
        addButton.clicked.connect(self.createSet)
        addButton.setStatusTip("Add sub set")
        addButton.setFixedSize(QSize(20, 20))
        itemLayout.addWidget(addButton)
        self.treeWidget.setItemWidget(self.treeWidget.topLevelItem(0), 0, item)

        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item = QWidget()
        itemLayout = QtGui.QHBoxLayout(item)
        itemLayout.setContentsMargins(3, 9, 9, 3)
        self.checkcalculation = QtGui.QCheckBox()
        self.checkcalculation.setText("Calculation")
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.checkcalculation.setFont(font)
        self.checkcalculation.setStyleSheet("color: rgb(194, 78, 80);" "font-size: 9pt;")
        self.checkcalculation.stateChanged.connect(self.checkcalculationall)
        itemLayout.addWidget(self.checkcalculation)
        self.treeWidget.setItemWidget(self.treeWidget.topLevelItem(1), 0, item)

        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item = QWidget()
        itemLayout = QtGui.QHBoxLayout(item)
        itemLayout.setContentsMargins(3, 9, 9, 3)
        self.checkclustering = QtGui.QCheckBox()
        self.checkclustering.setText("Clustering")
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.checkclustering.setFont(font)
        self.checkclustering.setStyleSheet("color: rgb(255, 205, 55);" "font-size: 9pt;")
        self.checkclustering.stateChanged.connect(self.checkclusteringall)
        itemLayout.addWidget(self.checkclustering)
        self.treeWidget.setItemWidget(self.treeWidget.topLevelItem(2), 0, item)

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
        self.checkBox.stateChanged.connect(self.checkselected)
        self.verticalLayout_image_collections.addWidget(self.checkBox)

        self.scrollArea = QtGui.QScrollArea(self.widget_image_collections)
        self.scrollArea.setWidgetResizable(True)
        self.widget_image_collections_show = QtGui.QWidget()
        self.widget_image_collections_show.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.verticalLayout_image_collections_show = QtGui.QFormLayout(self.widget_image_collections_show)
        self.verticalLayout_image_collections_show.setMargin(0)
        self.verticalLayout_image_collections_show.setContentsMargins(0, 0, 7, 0)
        self.scrollArea.setWidget(self.widget_image_collections_show)
        self.verticalLayout_image_collections.addWidget(self.scrollArea)

        self.label_image_collections.raise_()
        self.widget_image_collections_show.raise_()
        self.checkBox.raise_()
        self.horizontalLayout.addWidget(self.widget_image_collections)

        self.verticalLayout_selected = QtGui.QVBoxLayout()
        self.verticalLayout_selected.setSpacing(6)
        self.widget_selected = QtGui.QWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_selected.sizePolicy().hasHeightForWidth())
        self.widget_selected.setSizePolicy(sizePolicy)
        self.widget_selected.setMinimumSize(QtCore.QSize(50, 150))
        self.widget_selected.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
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

        self.scrollArea_2 = QtGui.QScrollArea(self.widget_selected)
        self.scrollArea_2.setWidgetResizable(True)
        self.widget_selected_view = QtGui.QWidget()
        self.widget_selected_view.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.verticalLayout_widget_selected_view = QtGui.QFormLayout(self.widget_selected_view)
        self.verticalLayout_widget_selected_view.setMargin(0)
        self.scrollArea_2.setWidget(self.widget_selected_view)
        self.verticalLayout_selected_view.addWidget(self.scrollArea_2)
        self.verticalLayout_selected.addWidget(self.widget_selected)

        self.horizontalLayout_buttons = QtGui.QHBoxLayout()
        self.horizontalLayout_buttons.setSpacing(6)
        self.horizontalLayout_buttons.setObjectName(_fromUtf8("horizontalLayout_buttons"))
        self.pushButton_edit = QtGui.QPushButton(Form)
        self.pushButton_edit.setObjectName(_fromUtf8("pushButton_edit"))
        self.horizontalLayout_buttons.addWidget(self.pushButton_edit)
        self.pushButton_export = QtGui.QPushButton(Form)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.pushButton_export.clicked.connect(self.export)
        self.horizontalLayout_buttons.addWidget(self.pushButton_export)
        self.pushButton_clustering = QtGui.QPushButton(Form)
        self.pushButton_clustering.setObjectName(_fromUtf8("pushButton_clustering"))
        self.horizontalLayout_buttons.addWidget(self.pushButton_clustering)
        self.pushButton_calculation = QtGui.QPushButton(Form)
        self.pushButton_calculation.setObjectName(_fromUtf8("pushButton_calculation"))
        self.pushButton_calculation.clicked.connect(self.calcul)
        self.horizontalLayout_buttons.addWidget(self.pushButton_calculation)
        self.pushButton_SOM = QtGui.QPushButton(Form)
        self.pushButton_SOM.setObjectName(_fromUtf8("pushButton_SOM"))
        self.pushButton_SOM.clicked.connect(self.SOM)
        self.horizontalLayout_buttons.addWidget(self.pushButton_SOM)
        self.verticalLayout_selected.addLayout(self.horizontalLayout_buttons)
        self.horizontalLayout.addLayout(self.verticalLayout_selected)
        self.widget_image_collections.raise_()
        self.widget_list_of_sets.raise_()

        default_name = datetime.fromtimestamp(int(round(time.time()))).strftime('--%m-%d %H-%M')

        my_set = newSet(default_name[2:], 0, [0])
        # set_current_set(my_set)
        # ##print(get_current_set().get_name())

        item_0 = QtGui.QTreeWidgetItem(self.treeWidget.topLevelItem(0))
        item_0.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        self.treeWidget.setItemWidget(self.treeWidget.topLevelItem(0).child(0), 0,
                                      SetButton(my_set, self.verticalLayout_image_collections_show,
                                                self.verticalLayout_widget_selected_view, self.checkBox,
                                                self.checkimported, self.checkcalculation,
                                                self.checkclustering, self.treeWidget))
        globalSets[0].append(my_set)

        self.pushButton_clustering.clicked.connect(self.extract_and_cluster)
        self.pushButton_edit.clicked.connect(self.edit_pannel)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def checkselected(self):
        for i in range(0, self.verticalLayout_image_collections_show.rowCount()):
            self.verticalLayout_image_collections_show.itemAt(i).widget().setChecked(self.checkBox.isChecked())

    def checkimportedall(self):
        imported = self.treeWidget.topLevelItem(0)
        it = QTreeWidgetItemIterator(self.treeWidget.topLevelItem(0))
        while it.value():
            if it.value().parent() is not None:
                self.treeWidget.itemWidget(it.value(), 0).check.setChecked(self.checkimported.isChecked())
            it += 1

    def checkclusteringall(self):
        clustering = self.treeWidget.topLevelItem(2)
        it = QTreeWidgetItemIterator(self.treeWidget.topLevelItem(2))
        while it.value():
            if it.value().parent() is not None and it.value().parent() == clustering:
                self.treeWidget.itemWidget(it.value(), 0).check.setChecked(self.checkclustering.isChecked())
            it += 1

    def checkcalculationall(self):
        calculation = self.treeWidget.topLevelItem(1)
        it = QTreeWidgetItemIterator(self.treeWidget.topLevelItem(1))
        while it.value():
            if it.value().parent() is not None and it.value().parent() == calculation:
                self.treeWidget.itemWidget(it.value(), 0).check.setChecked(self.checkcalculation.isChecked())
            it += 1

    def createSet(self):

        text, ok = QInputDialog.getText(self, 'Create a set',
                                        "Enter a new name for your new set :")
        # default_name = datetime.fromtimestamp(int(round(time.time()))).strftime('--%m-%d %H-%M-%S')
        if ok:
            new_ok = True
            not_ok = ['^', '[', '<', '>', ':', ';', ',', '?', '"', '*', '|', '/', ']', '+', '$']
            if len(text) == 0:
                new_ok = False
            for i in not_ok:
                if i in str(text):
                    new_ok = False
            if new_ok and not exists_set(str(text)):
                my_set = newSet(text, 0, [len(globalSets[0])])
                ##print(my_set.name)
                item_0 = QtGui.QTreeWidgetItem(self.treeWidget.topLevelItem(0))
                item_0.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                self.treeWidget.setItemWidget(self.treeWidget.topLevelItem(0).child(len(globalSets[0])), 0,
                                              SetButton(my_set, self.verticalLayout_image_collections_show,
                                                        self.verticalLayout_widget_selected_view, self.checkBox,
                                                        self.checkimported, self.checkcalculation,
                                                        self.checkclustering, self.treeWidget))
                globalSets[0].append(my_set)
            else:
                err = QtGui.QMessageBox.critical(self, "Error",
                                                 "The name you entered is not valid (empty, invalid caracter or already exists)")

    def updateTreeView(self):
        for s in setToAdd:
            ##print("s", s[1])
            ##print("len", len(globalSets[s[1]]))
            ##print("global", globalSets)
            item_0 = QtGui.QTreeWidgetItem(self.treeWidget.topLevelItem(s[1]))
            item_0.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            self.treeWidget.setItemWidget(self.treeWidget.topLevelItem(s[1]).child(len(globalSets[s[1]])), 0,
                                          SetButton(s[0], self.verticalLayout_image_collections_show,
                                                    self.verticalLayout_widget_selected_view, self.checkBox,
                                                    self.checkimported, self.checkcalculation,
                                                    self.checkclustering, self.treeWidget))
            globalSets[s[1]].append(s[0])
            setToAdd.remove(s)

    def updateColumn(self):
        global selected_images_collections
        global collshow

        # for i in reversed(range(self.verticalLayout_image_collections_show.count())):
        #     label = "Set name : " + str(
        #         self.verticalLayout_image_collections_show.itemAt(i).widget().setname) + "\nName : " + str(
        #         self.verticalLayout_image_collections_show.itemAt(i).widget().coll.name) + "\nNIfTI : " + str(
        #         len(self.verticalLayout_image_collections_show.itemAt(i).widget().list)) + "\nLast modified : " + str(
        #         self.verticalLayout_image_collections_show.itemAt(i).widget().d)
        #     ##print("label",label)
        #     self.verticalLayout_image_collections_show.itemAt(i).widget().setText(label)
        #     self.verticalLayout_image_collections_show.itemAt(i).widget().setChecked(False)

        for i in reversed(range(self.verticalLayout_widget_selected_view.count())):
            self.verticalLayout_widget_selected_view.itemAt(i).widget().setParent(None)

        for i in reversed(range(self.verticalLayout_image_collections_show.count())):
            self.verticalLayout_image_collections_show.itemAt(i).widget().setParent(None)

        # for i in reversed(range(self.verticalLayout_image_collections_show.count())):
        #     ##print(self.verticalLayout_image_collections_show.itemAt(i).widget())

        # ##print("collshow",collshow)
        del collshow[:]
        del selected_images_collections[:]

        imported = self.treeWidget.topLevelItem(0)
        clustering = self.treeWidget.topLevelItem(2)
        calculation = self.treeWidget.topLevelItem(1)

        it = QTreeWidgetItemIterator(self.treeWidget.topLevelItem(0))
        while it.value():
            if it.value().parent() is not None and it.value().parent() == imported:
                item = self.treeWidget.itemWidget(it.value(), 0)
                if item.check.isChecked():
                    dict = item.my_set.get_all_nifti_set()
                    for d in dict:
                        if d not in selected_images_collections:
                            selected_images_collections.append(d)
                            self.verticalLayout_image_collections_show.addWidget(
                                CollButton(d, d.getSetName().get_name(), self.verticalLayout_widget_selected_view,
                                           self.checkBox))
            it += 1

        it = QTreeWidgetItemIterator(self.treeWidget.topLevelItem(2))
        while it.value():
            if it.value().parent() is not None and it.value().parent() == clustering:
                item = self.treeWidget.itemWidget(it.value(), 0)
                if item.check.isChecked():
                    dict = item.my_set.get_all_nifti_set()
                    for d in dict:
                        if d not in selected_images_collections:
                            selected_images_collections.append(d)
                            self.verticalLayout_image_collections_show.addWidget(
                                CollButton(d, d.getSetName().get_name(), self.verticalLayout_widget_selected_view,
                                           self.checkBox))
            it += 1

        it = QTreeWidgetItemIterator(self.treeWidget.topLevelItem(1))
        while it.value():
            if it.value().parent() is not None and it.value().parent() == calculation:
                item = self.treeWidget.itemWidget(it.value(), 0)
                if item.check.isChecked():
                    dict = item.my_set.get_all_nifti_set()
                    for d in dict:
                        if d not in selected_images_collections:
                            selected_images_collections.append(d)
                            self.verticalLayout_image_collections_show.addWidget(
                                CollButton(d, d.getSetName().get_name(), self.verticalLayout_widget_selected_view,
                                           self.checkBox))
            it += 1

    def show_coll(self, coll):
        # -- This show_coll will add a collection to the current vizu
        get_current_vizu().add(coll)

    def export(self):
        if get_selected():
            export_choice = QtGui.QMessageBox()
            export_choice.setWindowTitle('Export dataSet')

            nifti_opt = QRadioButton("Export to NIfTI")
            excel_opt = QRadioButton("Export to CSV")
            nifti_opt.setChecked(True)

            l1 = export_choice.layout()
            l1.setContentsMargins(20, 0, 0, 20)
            l1.addWidget(QLabel("You have selected (" + str(len(
                get_selected())) + ") image collections. \nThere is a total of (" + str(get_selected_images_number()) +
                                ") NIfTI images to be treated. \nPlease select the way "
                                "you would like to export these files : "),
                         l1.rowCount() - 3, 0, 1, l1.columnCount() - 2, Qt.AlignCenter)
            rb_box = QtGui.QGroupBox()
            vbox = QtGui.QVBoxLayout()
            vbox.addWidget(nifti_opt)
            vbox.addWidget(excel_opt)

            rb_box.setLayout(vbox)
            l1.addWidget(rb_box, l1.rowCount() - 2, 0, Qt.AlignCenter)

            export_choice.setStandardButtons(QMessageBox.Cancel | QMessageBox.Apply)

            ret = export_choice.exec_()

            if ret == QtGui.QMessageBox.Apply:

                if nifti_opt.isChecked():

                    # save an addition of all the file as one (and only one) nifti file

                    # get the path where we will save the file
                    save_path: str = QFileDialog.getSaveFileName(self, "Save the nifti file")

                    if save_path is not None:
                        if "." not in save_path:
                            save_path = save_path + ".nii"
                        # put all the images in a single list
                        list_of_images: list = []
                        for image_collection in selected_images_collections:
                            for key in image_collection.nifimage_dict.keys():
                                list_of_images.append(image_collection.nifimage_dict[key])
                        # make an addition of all the image
                        result_matrix = calculations.addition_operation(list_of_images)
                        # get the result in an nibabel image with an mni affine
                        img: nibabel.nifti1.Nifti1Image = calculations.create_mni_nibabel_image_from_matrix(
                            result_matrix)
                        # save the image
                        try:
                            nibabel.save(img, save_path)
                        except FileExistsError as e:
                            QtGui.QMessageBox.critical(self,
                                                       "Error",
                                                       f"Error while saving the file: {e}.")
                        else:
                            QtGui.QMessageBox.information(self,
                                                          "Success",
                                                          f"The export has been saved at {save_path}.")

                elif excel_opt.isChecked():
                    type_choice = QtGui.QMessageBox()
                    type_choice.setWindowTitle('Export excel all or centroid')

                    all_opt = QRadioButton("Export all points")
                    centroid_opt = QRadioButton("Export only the centroid of each file")
                    all_opt.setChecked(True)

                    l2 = type_choice.layout()
                    l2.setContentsMargins(20, 0, 0, 20)
                    l2.addWidget(QLabel(" Excel Export \nPlease select the type of export"),
                                 l2.rowCount() - 3, 0, 1, l2.columnCount() - 2, Qt.AlignCenter)

                    rb_box = QtGui.QGroupBox()
                    vbox = QtGui.QVBoxLayout()
                    vbox.addWidget(all_opt)
                    vbox.addWidget(centroid_opt)

                    rb_box.setLayout(vbox)
                    l2.addWidget(rb_box, l2.rowCount() - 2, 0, Qt.AlignCenter)

                    type_choice.setStandardButtons(QMessageBox.Cancel | QMessageBox.Apply)

                    ret = type_choice.exec_()

                    if ret == QtGui.QMessageBox.Apply:

                        (f_path, f_name) = os.path.split(str(QFileDialog.getSaveFileName(self, "Browse Directory")))

                        if all_opt.isChecked():
                            extract_data_from_selected()
                        elif centroid_opt.isChecked():
                            extract_data_as_centroids_from_selected()

                    try:
                        ee.export(f_name, f_path, get_current_usableDataset())
                    except FileExistsError as e:
                        QtGui.QMessageBox.critical(self,
                                                   "Error",
                                                   f"Error while saving the file: {e}.")
                    else:
                        QtGui.QMessageBox.information(self,
                                                      "Success",
                                                      f"The export has been saved at {os.path.join(f_name, f_path)}.")



                else:
                    ##print("There was a problem in export options")
                    pass

        else:
            QtGui.QMessageBox.information(self, "Selection empty", "There's nothing to export.")
        ##print()

    def extract_and_cluster(self):
        if get_selected():
            choice = QtGui.QMessageBox()
            choice.setWindowTitle('Extract data for clustering')

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

                try:

                    if all_points_opt.isChecked():
                        extract_data_from_selected()

                    elif centroid_opt.isChecked():
                        extract_data_as_centroids_from_selected()

                    self.showClust.emit()

                except KeyError as k:
                    QtGui.QMessageBox.critical(self, "Bad Data", f"Some of the files don't have one of"
                                                                 f"the necessary columns :"
                                                                 f"{(str(k).split(']')[0]+']')[1:]}")



        else:
            QtGui.QMessageBox.information(self, "Selection empty", "There's no data to extract and clusterize.")

    def calcul(self):
        if get_selected():
            for collection in collshow:
                for img in collection.nifimage_dict.values():
                    if isinstance(img, image.Image):
                        if len(img.columns.intersection({"X", "Y", "Z", "Intensity"})) < 4:
                            QtGui.QMessageBox.information(self, "Selection empty", "Calculations are possible on data "
                                                                                   "with the columns X,Y,Z,Intensity")
                            return

            self.showCalcul.emit()
        else:
            QtGui.QMessageBox.information(self, "Selection empty", "There's no data to calculation.")

    def SOM(self):
        liste_col = get_selected()
        list_img = []
        for col in liste_col:
            for img in col.get_img_list().values():
                # ##print(type(img))
                if not (isinstance(img, NifImage)):
                    list_img.append(img)
                else:
                    QtGui.QMessageBox.critical(self, "Wrong data", "You can't use NIfTI images for the SOM window.")
                    return
        if len(list_img) > 0:
            self.input_som = im.som_preparation(list_img)
            ##print(f"self.input_som.columns : {self.input_som.columns}")
            if "X" not in self.input_som.columns or "Y" not in self.input_som.columns or "Z" not in self.input_som.columns:
                QtGui.QMessageBox.critical(self, "Wrong data", "The format of the data is not correct: there must "
                                                               "be an X, an Y and a Z column.")
            elif len(self.input_som.columns) == 3:
                QtGui.QMessageBox.critical(self, "Wrong data",
                                           "There is not additional information in the files.")
            else:
                self.showSOM.emit()
        else:
            QtGui.QMessageBox.critical(self, "Wrong data", "You didn't chose any files.")

    def edit_pannel(self):
        global selected_images_collections
        global collshow
        # -- This edit_pannel will show the edit view if selected is not empty
        # ##print("mv selected",selected)
        # ##print("mv collshow",collshow)
        if (get_selected()):
            self.showEdit.emit()
        else:
            QtGui.QMessageBox.information(self, "Selection empty", "There's no data to edit.")

    # def update(self):
    #     # -- This update will call the update function of collectionsDisplayBox
    #     self.collectionsDisplayBox.update()
    #     ##print()

    def updateafterimport(self):

        def insertionarbreimport(set, position):
            # ##print("len",len(set.getAllSubSets()))
            compteur = 0

            if len(set.getAllSubSets()) == 0:
                pass
            else:
                for subset in set.getAllSubSets():

                    position_arbre = position
                    position_arbre_nouveau = list(position_arbre)
                    position_arbre_nouveau.append(compteur)
                    subset.position_arbre = position_arbre_nouveau
                    ##print("position_arbre_nouveau", position_arbre_nouveau)
                    ##print("self.compteur", compteur)
                    compteur = compteur + 1
                    ##print("self.compteur after", compteur)
                    p = self.treeWidget.topLevelItem(0)
                    for i in range(len(position_arbre_nouveau) - 1):
                        p = p.child(position_arbre_nouveau[i])

                    item_0 = QtGui.QTreeWidgetItem(p)
                    item_0.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    self.treeWidget.setItemWidget(p.child(position_arbre_nouveau[-1]), 0,
                                                  SetButton(subset, self.verticalLayout_image_collections_show,
                                                            self.verticalLayout_widget_selected_view, self.checkBox,
                                                            self.checkimported, self.checkcalculation,
                                                            self.checkclustering, self.treeWidget))
                    # ##print("subset pos arbre avant",set.position_arbre)
                    # ##print("subset pos arbre apres",set.position_arbre)
                    insertionarbreimport(subset, position_arbre_nouveau)

        for elem in get_workspace_set():
            # ##print("parent",elem.getParent())
            # ##print("SET NAME",elem.name)
            # ##print('dic', elem.getAllSubSets())
            # for elem2 in elem.getAllSubSets():
            #     ##print("SET NAME 2",elem2.name)
            #     ##print('dic2', elem2.getAllSubSets())
            #     for elem3 in elem2.getAllSubSets():
            #         ##print("SET NAME 3",elem3.name)
            #         ##print('dic3', elem3.getAllSubSets())
            #         for elem4 in elem3.getAllSubSets():
            #             ##print("SET NAME 4",elem4.name)
            #             ##print('dic4', elem4.getAllSubSets())

            item_0 = QtGui.QTreeWidgetItem(self.treeWidget.topLevelItem(0))
            item_0.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            self.treeWidget.setItemWidget(self.treeWidget.topLevelItem(0).child(len(globalSets[0])), 0,
                                          SetButton(elem, self.verticalLayout_image_collections_show,
                                                    self.verticalLayout_widget_selected_view, self.checkBox,
                                                    self.checkimported, self.checkcalculation,
                                                    self.checkclustering, self.treeWidget))
            elem.position_arbre = [len(globalSets[0])]
            globalSets[0].append(elem)
            position_arbre = elem.position_arbre
            compteur = 0
            insertionarbreimport(elem, position_arbre)

            # self.my_set.get_sub_set(str(text)).setParent(self.my_set)
            # add_set(ss)
            # set_current_set(ss)

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
        ##print()
        pass

    def updateClusterRes(self):
        # self.setAccessBox.add2()
        ##print()
        pass

    def updateCalculRes(self):
        # self.setAccessBox.add3()
        ##print()
        pass

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_list_of_sets.setText(_translate("Form", "List of sets", None))
        self.treeWidget.headerItem().setText(0, _translate("Form", "List of set and subset", None))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        # self.treeWidget.topLevelItem(0).setText(0, _translate("Form", "Imported", None))
        # self.treeWidget.topLevelItem(1).setText(0, _translate("Form", "Calculation", None))
        # self.treeWidget.topLevelItem(2).setText(0, _translate("Form", "Clustering", None))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.label_image_collections.setText(_translate("Form", "Image collections", None))
        self.checkBox.setText(_translate("Form", "Select all", None))
        self.label_selected.setText(_translate("Form", "Selected ", None))
        self.pushButton_edit.setText(_translate("Form", "Edit", None))
        self.pushButton_export.setText(_translate("Form", "Export data", None))
        self.pushButton_clustering.setText(_translate("Form", "Clustering", None))
        self.pushButton_calculation.setText(_translate("Form", "Calculation", None))
        self.pushButton_SOM.setText(_translate("Form", "SOM", None))
