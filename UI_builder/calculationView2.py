# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calculation.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

import sys
from os import path

from PyQt4 import QtGui
from PyQt4.Qt import *
from nibabel import Nifti1Image, load

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from BrainMapper import *

import time

from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSignal

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


class calculationView2(QtGui.QWidget):
    showMain = pyqtSignal()

    def __init__(self):
        super(calculationView2, self).__init__()

        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1000, 650)
        self.verticalLayout_7 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget = QtGui.QWidget(Form)
        self.widget.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.leftlist = QtGui.QListWidget(self.widget)
        self.leftlist.insertItem(0, 'Addition')
        self.leftlist.insertItem(1, 'Boolean Intersection')
        self.leftlist.insertItem(2, 'Boolean Union')
        self.leftlist.insertItem(3, 'Centroide')
        self.leftlist.insertItem(4, 'Closing')
        self.leftlist.insertItem(5, 'Dilation')
        self.leftlist.insertItem(6, 'Entropy')
        self.leftlist.insertItem(7, 'Erosion')
        self.leftlist.insertItem(8, 'Linear combination')
        self.leftlist.insertItem(9, 'Mask')
        self.leftlist.insertItem(10, 'Mean')
        self.leftlist.insertItem(11, 'Normalization')
        self.leftlist.insertItem(12, 'Opening')
        self.leftlist.insertItem(13, 'Threshold')
        self.leftlist.insertItem(14, 'Multiplication')
        self.leftlist.insertItem(15, 'Division')
        self.leftlist.setObjectName(_fromUtf8("leftlist"))
        self.leftlist.currentRowChanged.connect(self.display)
        self.verticalLayout.addWidget(self.leftlist)
        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.widget1 = QtGui.QWidget(Form)
        self.widget1.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, -1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.widget1)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.param = QtGui.QLineEdit(self.widget1)
        self.param.setObjectName(_fromUtf8("param"))
        self.verticalLayout_2.addWidget(self.param)
        self.verticalLayout_6.addWidget(self.widget1)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.clicked.connect(lambda: self.run_calculation())
        self.verticalLayout_6.addWidget(self.pushButton)
        self.widget_2 = QtGui.QWidget(Form)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.widget_2)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, -1)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_3 = QtGui.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_4.addWidget(self.label_3)
        self.textBrowser = QtGui.QTextBrowser(self.widget_2)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout_4.addWidget(self.textBrowser)
        self.verticalLayout_6.addWidget(self.widget_2)
        self.widget_3 = QtGui.QWidget(Form)
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.widget_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, -1)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.label_4 = QtGui.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_5.addWidget(self.label_4)
        self.textBrowser_2 = QtGui.QTextBrowser(self.widget_3)
        self.textBrowser_2.setObjectName(_fromUtf8("textBrowser_2"))
        self.verticalLayout_5.addWidget(self.textBrowser_2)
        self.verticalLayout_6.addWidget(self.widget_3)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.verticalLayout_7.addLayout(self.horizontalLayout)
        self.frame_2 = QtGui.QFrame(Form)
        self.frame_2.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.console = QtGui.QTextBrowser(self.frame_2)
        self.console.setObjectName(_fromUtf8("console"))
        self.verticalLayout_3.addWidget(self.console)
        self.verticalLayout_7.addWidget(self.frame_2)
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_2.clicked.connect(self.go_back)
        self.verticalLayout_7.addWidget(self.pushButton_2)

        self.retranslate_ui(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def display(self):

        item = self.leftlist.currentItem().text()
        if item == "Addition":
            # ----- Addition ------------------------------------
            self.textBrowser.setText(
                "The Addition algorithm make a addition with a collection of nifti makes the term some term of each "
                "voxel")
            self.textBrowser_2.setText(
                "\t[5, 3, 0]   [0, 4, 0]       [5, 8, 0]\n\t[0, 0, 3]   [0, 7, 4]       [0, 7, 7]\nAddition ( \t[1, "
                "1, 2] , [3, 0, 0] ) = [4, 1, 2]")

        elif item == "Boolean Intersection":
            # ----- Boolean Intersection -----------------------
            self.textBrowser.setText(
                "The Boolean intersection takes a set of files and returns a binary file of 0 and 1. A voxel with 1 "
                "value means that for every file this voxels have strictely positive intensity")
            self.textBrowser_2.setText(
                "\t[5, 9, 0]   [0, 4, 0]       [0, 1, 0]\n\t[0, 0, 3]   [0, 7, 4]       [0, 0, 1]\nBoolInter( \t[1, "
                "1, 2] , [3, 0, 0] ) = [1, 0, 0]")

        elif item == "Boolean Union":
            # ----- Boolean Union ----------------------------
            self.textBrowser.setText(
                "The Boolean union takes a set of files and returns a binary file of 0 and 1. A voxel with 1 value "
                "means that there exists in at least some files nifti a voxel whose intensity is strictly positive")
            self.textBrowser_2.setText(
                "\t[5, 9, 0]   [0, 4, 0]       [1, 1, 0]\n\t[0, 0, 3]   [0, 7, 0]       [0, 1, 1]\nBoolUnion( \t[0, "
                "1, 2] , [0, 0, 0] ) = [0, 1, 1]")

        elif item == "Centroide":
            # ----- Centroide ------------------------------------
            self.textBrowser.setText(
                "This algorithm calculates the centroid of each cluster present in one or a set of nifti files")
            self.textBrowser_2.setText("\t[0, 1, 0]\n\t[5, 2, 3]\nCentroid ( \t[0, 1, 0] ) = (1,1,1)")

        elif item == "Closing":
            # ----- Closing ------------------------------------

            self.textBrowser.setText(
                "In mathematical morphology, the closing of a set (binary image) A by a structuring element B is the "
                "erosion of the dilation of that set, A * B = ( A (+) B ) (-) B, denote the dilation and erosion, "
                "respectively. In image processing, closing is, together with opening, the basic workhorse of "
                "morphological noise removal. Opening removes small objects, while closing removes small holes.")
            self.textBrowser_2.setText("Opening(n) = Erosion(Dilation(n))")
            self.param.setText("1")

        elif item == "Dilation":
            # ----- Dilatation ---------------------------
            self.textBrowser.setText(
                "Dilation (usually represented by (+)) is one of the basic operations in mathematical morphology. "
                "Originally developed for binary images, it has been expanded first to grayscale images, and then to "
                "complete lattices. The dilation operation usually uses a structuring element for probing and "
                "expanding the shapes contained in the input image.")
            self.textBrowser_2.setText("ADD")
            self.param.setText("1")

        elif item == "Entropy":
            # ----- Entropy -----------------------------
            self.textBrowser.setText(
                "The entropy of an image is a decimal value that allows to characterize the degree of "
                "disorganization, or unpredictability of the information content of a system.")
            self.textBrowser_2.setText(
                "Entropy(Nifti img) = SUM(-Pi * log2(Pi))\nWhere Pi is the probability for the value i in the image "
                "to appear.")

        elif item == "Erosion":
            # ----- Erosion ------------------------------
            self.textBrowser.setText(
                "Erosion (usually represented by (-)) is one of two fundamental operations (the other being dilation) "
                "in morphological image processing from which all other morphological operations are based. It was "
                "originally defined for binary images, later being extended to grayscale images, and subsequently to "
                "complete lattices.")
            self.textBrowser_2.setText("ADD")
            self.param.setText("1")

        elif item == "Linear combination":
            # ----- Linear combination ---------------------------
            self.textBrowser.setText(
                "This algorithm makes the sum of a set of nifti files by associating a weight to each one of them (to "
                "caracterizes the importance)")
            self.textBrowser_2.setText("Linear(img1, .., imgN] , [c1, .., cN]) = c1*Ni_1 + .. + cN*Ni_N")
            self.param.setText("1;4")

        elif item == "Mask":
            # ----- Mask ---------------------------------
            self.textBrowser.setText(
                "The Mask process need two file : one named mask that permit to define which voxels in the second one "
                "will be selected. Only the voxels in the second one where the voxels in the mask with the same "
                "coordinates and a value > 0 will be selected.")
            self.textBrowser_2.setText(
                "\t[1, 1, 0]   [2, 4, 9]       [2, 4, 0]\n\t[0, 0, 1]   [3, 7, 5]       [0, 0, 5]\nMaskProc ( \t[1, "
                "0, 1] , [6, 8, 4] ) = [6, 0, 4]")

        elif item == "Mean":
            # ----- Mean ---------------------------------
            self.textBrowser.setText(
                "The Mean process averages a set of nifti files. The algorithm performs the sum for all voxels "
                "present in each file the divides the value obtained by the number of files")
            self.textBrowser_2.setText(
                "\t[5, 9, 0]   [0, 4, 0]       [2.5, 6.5, 0.0]\n\t[0, 0, 3]   [0, 7, 0]       [0.0, 3.5, "
                "1.5]\nMeanProc ( \t[0, 1, 2] , [0, 0, 0] ) = [0.0, 0.5, 1.0]")

        elif item == "Normalization":
            # ----- Normalization ------------------------------------
            self.textBrowser.setText(
                "The normalization algorithm creates one nifti file result for each input nifti file. This algorithm "
                "create a file where the values for each voxel are between 0 and 1. Different ways exit to normalize "
                "a nifti file, you can select in the options panel the desired method")
            self.textBrowser_2.setText("ADD")

        elif item == "Opening":
            # ----- Opening ------------------------------------
            self.textBrowser.setText(
                "In morphological opening ( A (-) B ) (+) B, erosion operation removes objects that are smaller than "
                "structuring element B and dilation operation restores the shape of remaining objects. However, "
                "restoring accuracy in dilation operation highly depends on the type of structuring element and the "
                "shape of restoring objects. The opening by reconstruction method is able to restore the objects "
                "completely after erosion applied.")
            self.textBrowser_2.setText("Opening(n) = Dilation(Erosion(n))")
            self.param.setText("1")

        elif item == "Threshold":
            # ----- Threshold ------------------------------------
            self.textBrowser.setText(
                "The threshold operation allows you to store only voxels whose intensity value is between the min and "
                "max parameters. All voxels that do not meet this criterion have their intensity that becomes zero. "
                "If no value is assigned to min and max then their values will be less the infinite and the less "
                "infinite respectively.")
            self.textBrowser_2.setText(
                "For each voxels in Nifti:\n\tif not min<voxels.intensity<max:\n\t\tvoxels.intensity = 0")

        elif item == "Multiplication":
            # ----- Multiplication ------------------------------------
            self.textBrowser.setText("ADD")
            self.textBrowser_2.setText("ADD")
            self.param.setText("1")

        elif item == "Division":
            # ----- Division ------------------------------------
            self.textBrowser.setText("ADD")
            self.textBrowser_2.setText("ADD")
            self.param.setText("1")

    # --------------------- Action for CALCULATE button -------------------
    def run_calculation(self):
        global collshow
        print("calculation in progress...")
        algorithm = self.leftlist.currentItem().text()
        # extraction of arguments here
        #
        #  ... TO DO ...
        #
        arguments = []
        nifti_selected = []

        for collection in collshow:
            for nifti in collection.nifimage_dict.values():
                # COPIE nifti_selected.append(nifti.filename)
                nifti_selected.append(nifti)
        if algorithm == "Mean":
            if len(nifti_selected) < 2:
                QtGui.QMessageBox.warning(self, "Error",
                                          algorithm + "algorithm " + " must have two or more input file")
            else:
                try:
                    algorithm_result, output = run_calculation(algorithm, nifti_selected, arguments)
                    self.console.setText(">>> \n" + output)
                    self.popUpSaveFileResultCalculation(algorithm, algorithm_result)

                except:
                    QtGui.QMessageBox.warning(self, "Error",
                                              "Impossible to execute " + algorithm + " algorithm")
        if algorithm == "Mask":
            if len(nifti_selected) != 2:
                QtGui.QMessageBox.warning(self, "Error",
                                          algorithm + "algorithm " + " must have two or more input file")
            else:
                try:
                    algorithm_result, output = run_calculation(algorithm, nifti_selected, arguments)
                    self.console.setText(">>> \n" + output)
                    self.popUpSaveFileResultCalculation(algorithm, algorithm_result)
                except:
                    QtGui.QMessageBox.warning(self, "Error",
                                              "Impossible to execute " + algorithm + " algorithm. This algorithm can only takes 2 File : The mask and the one which will be applied the mask. Please verify that you have select just 2 file in your collection.")

        if algorithm == "Linear combination":
            value = self.param.text()
            arguments = value.split(';')
            if len(nifti_selected) != len(arguments):
                QtGui.QMessageBox.warning(self, "Error",
                                          algorithm + "algorithm " + "must have the same number of arguments as the number of nifti files selected. Please enter %s arguments." % (
                                              len(nifti_selected)))
            else:
                try:
                    algorithm_result, output = run_calculation(algorithm, nifti_selected, arguments)
                    self.console.setText(">>> \n" + output)
                    self.popUpSaveFileResultCalculation(algorithm, algorithm_result)
                except:
                    QtGui.QMessageBox.warning(self, "Error",
                                              "Impossible to execute " + algorithm + " algorithm. Please check if you have correctly entering the coefficent list")
        if algorithm == "Boolean Intersection":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, arguments)
                self.console.setText(">>> \n" + output)
                self.popUpSaveFileResultCalculation(algorithm, algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute " + algorithm + " algorithm")
        if algorithm == "Boolean Union":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, arguments)
                self.console.setText(">>> \n" + output)
                self.popUpSaveFileResultCalculation(algorithm, algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute " + algorithm + " algorithm")
        if algorithm == "Normalization":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, arguments)
                self.console.setText(">>> \n" + output)
                self.popUpSaveFileResultCalculation(algorithm, algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute " + algorithm + " algorithm")
        if algorithm == "Centroide":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, arguments)
                self.console.setText(">>> \n" + output)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute " + algorithm + " algorithm")
        if algorithm == "Addition":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, arguments)
                self.console.setText(">>> \n" + output)
                self.popUpSaveFileResultCalculation(algorithm, algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute " + algorithm + " algorithm")
        if algorithm == "Entropy":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, arguments)
                self.console.setText(">>> \n" + output)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute " + algorithm + " algorithm")
        if algorithm == "Erosion":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, self.param.text())
                self.console.setText(">>> \n" + output)
                self.popUpSaveFileResultCalculation(algorithm, algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute " + algorithm + " algorithm")
        if algorithm == "Dilation":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, self.param.text())
                self.console.setText(">>> \n" + output)
                self.popUpSaveFileResultCalculation(algorithm, algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute " + algorithm + " algorithm")
        if algorithm == "Opening":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, self.param.text())
                self.console.setText(">>> \n" + output)
                self.popUpSaveFileResultCalculation(algorithm, algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute " + algorithm + " algorithm")
        if algorithm == "Closing":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, self.param.text())
                self.console.setText(">>> \n" + output)
                self.popUpSaveFileResultCalculation(algorithm, algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute " + algorithm + " algorithm")
        if algorithm == "Threshold":
            try:
                try:
                    min = float(self.thresholdMin.text())
                except:
                    min = -1000000.0
                try:
                    max = float(self.thresholdMax.text())
                except:
                    max = 1000000.0
                algorithm_result, output = run_calculation(algorithm, nifti_selected, [min, max])
                self.console.setText(">>> \n" + output)
                self.popUpSaveFileResultCalculation(algorithm, algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute " + algorithm + " algorithm\nPlease enter the lower bound (Min) and higher bound (Max). These two arguments must be double value (ex: 5.63)")
        if algorithm == "Multiplication":
            try:
                try:
                    mult_coef = float(self.param.text())
                    print(mult_coef)
                except:
                    mult_coef = 1
                    print("fail mult coef")
                algorithm_result, output = run_calculation(algorithm, nifti_selected, mult_coef)
                self.console.setText(">>> \n" + output)
                self.popUpSaveFileResultCalculation(algorithm, algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute " + algorithm + " algorithm")
        if algorithm == "Division":
            try:
                try:
                    div_coef = float(self.param.text())
                except:
                    div_coef = 1
                algorithm_result, output = run_calculation(algorithm, nifti_selected, div_coef)
                self.console.setText(">>> \n" + output)
                self.popUpSaveFileResultCalculation(algorithm, algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute " + algorithm + " algorithm")

    def popUpSaveFileResultCalculation(self, algorithm, result):
        global setToAdd
        choice = QtGui.QMessageBox()
        choice.setWindowTitle('Success !')
        l = choice.layout()
        l.setContentsMargins(20, 10, 10, 20)
        l.addWidget(QLabel(
            algorithm + " algorithm has been correctly applicated on nifti(s) file(s)\n\n\n\nDo you want save the algorithm's result as Set ?"),
            l.rowCount() - 3, 0, 1, l.columnCount() - 2, Qt.AlignCenter)
        choice.setStandardButtons(QMessageBox.Cancel | QMessageBox.Save)
        wantToSave = choice.exec_()
        if wantToSave == QtGui.QMessageBox.Save:
            setCalculation = Set("calc_", 1)
            setCalculation.set_name("calc_" + str(id(setCalculation)))
            coll = ImageCollection("coll_", setCalculation)
            coll.set_name("coll_" + str(id(coll)))
            for matrixData in result:
                template_mni_path = 'ressources/template_mni/mni_icbm152_t1_tal_nlin_asym_09a.nii'
                template_data = load(template_mni_path)
                template_affine = template_data.affine
                recreate_image = Nifti1Image(matrixData, template_affine)
                ni_image = NifImage("" + str(time.time() * 1000), recreate_image)
                ni_image.set_filename("file_" + str(algorithm) + "_" + str(id(ni_image)) + ".nii")
                coll.add(ni_image)
            setCalculation.add_collection(coll)
            makeCalculResultSet(setCalculation)

    def go_back(self):
        # -- When the user wants to return to the main view, we reinit the cluster view

        self.showMain.emit()

    def retranslate_ui(self, form):
        form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Arguments", None))
        self.label_2.setText(_translate("Form", "Name of argument", None))
        self.pushButton.setText(_translate("Form", "Calculate", None))
        self.label_3.setText(_translate("Form", "Description", None))
        self.textBrowser.setHtml(_translate("Form",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'Fira Sans\'; font-size:10pt; font-weight:200; font-style:normal;\">\n"
                                            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>",
                                            None))
        self.label_4.setText(_translate("Form", "Example", None))
        self.pushButton_2.setText(_translate("Form", "Go back", None))
