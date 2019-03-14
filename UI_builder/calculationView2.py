import sys
from os import path

from PyQt4 import QtGui
from PyQt4.Qt import *
from nibabel import Nifti1Image, load

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import BrainMapper
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

        ## Operations item ##
        # Operations which return only one matrix
        self.leftlist.addItem('addition')
        self.leftlist.addItem('division')
        self.leftlist.addItem('linear combination')
        self.leftlist.addItem('mean')
        self.leftlist.addItem('multiplication')
        self.leftlist.addItem('and')
        self.leftlist.addItem('or')
        for i in range(0, 7):
            self.leftlist.item(i).setBackgroundColor(QColor(244, 176, 66, 127))
        # Operations which return as much file as their is in entry
        self.leftlist.insertItem(7, 'closing')
        self.leftlist.insertItem(8, 'dilation')
        self.leftlist.insertItem(9, 'erosion')
        self.leftlist.insertItem(10, 'opening')
        self.leftlist.insertItem(11, 'threshold')
        for i in range(7, 12):
            self.leftlist.item(i).setBackgroundColor(QColor(237, 137, 217, 127))

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
        self.argument_name = QtGui.QLabel(self.widget1)
        self.argument_name.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.argument_name)
        self.arguments_line = QtGui.QLineEdit(self.widget1)
        self.arguments_line.setObjectName(_fromUtf8("param"))
        self.verticalLayout_2.addWidget(self.arguments_line)
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
        self.textBrowser_2.setMinimumSize(QtCore.QSize(0, 100))
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

    def set_arguments_editable(self, show: bool, text: str = ""):
        if show:
            self.arguments_line.setDisabled(False)
            self.arguments_line.setStyleSheet(
                """QLineEdit { background-color: white}""")
            self.arguments_line.setText(text)
            self.arguments_line.repaint()
        else:
            self.arguments_line.setDisabled(True)
            self.arguments_line.setStyleSheet(
                """QLineEdit { background-color: grey}""")
            self.arguments_line.setText(text)
            self.arguments_line.repaint()

    def display(self):
        """
        Update the displayed information when the user click on a row
        """
        item = self.leftlist.currentItem().text()

        if item == "addition":
            self.argument_name.setText("No argument")
            self.set_arguments_editable(False)
            self.textBrowser.setText(
                "Result: a unique image\n"
                "Addition all the images in input."
            )
            self.textBrowser_2.setText("[5, 4, 0]     [0, 4, 0]    [5, 8, 0]\n[0, 0, 3] + [0, 7, 4] = [0, 7, 7]\n[1, "
            "1, 2]     [3, 0, 0]    [4, 1, 2]")

        elif item == "division":
            self.argument_name.setText("Coefficient")
            self.set_arguments_editable(True, "1.0")
            self.textBrowser.setText(
                "Result: a unique image\n"
                "Addition all the images in input, and then divide all the intensity by the coefficient."
            )
            self.textBrowser_2.setText("[  6,   4,  0]           [3, 2, 0]\n[  0,   0,  4] / 2 = [0, 0, 2]\n[10, "
            "10, 2]           [5, 5, 1]")

        elif item == "linear combination":
            self.argument_name.setText("Coefficients")
            basic_coefficients = ",".join(["1.0"] * self.count_images())
            self.set_arguments_editable(True, basic_coefficients)
            filenames = []
            for i, name in enumerate(self.get_images_names()):
                filenames.append(str(i)+": "+name)
            self.textBrowser.setText(
                "Result: a unique image\n"
                "Addition all the images in input, but each image having all its intensity multiplied by the "
                "corresponding coefficient.\n"
                "List of filename:\n\t"
                + "\n\t".join(filenames)
            )
            self.textBrowser_2.setText("[0, 1, 0]           [0, 0, 0]           [0, 0, 1]           [0, 2, 3]\n"
            "[1, 0, 1] * 2 + [0, 1, 1] * 1 + [1, 0, 0] * 3 = [5, 1, 3]\n"
            "[0, 0, 0]           [1, 0, 0]           [0, 1, 1]           [1, 3, 3]")

        elif item == "mean":
            self.argument_name.setText("No argument")
            self.set_arguments_editable(False)
            self.textBrowser.setText(
                "Result: a unique image\n"
                "Addition all the images in input, and then divide all the intensity by the number of images."
            )
            self.textBrowser_2.setText("            [0, 3, 0]     [0, 0, 0]    [0, 0, 3]        [0, 3, 0]     [0, 0, 0]    [0, 0, 3]             [0, 1, 1]\n"
            "Mean([2, 0, 1] + [0, 9, 1] + [1, 0, 4]) = ( [2, 0, 1] + [0, 9, 1] + [1, 0, 4] ) / 3 = [1, 3, 2]\n"
            "            [0, 5, 0]     [9, 0, 3]    [0, 4, 3]        [0, 5, 0]     [9, 0, 3]    [0, 4, 3]             [3, 3, 2]")

        elif item == "multiplication":
            self.argument_name.setText("Coefficient")
            self.set_arguments_editable(True, "1.0")
            self.textBrowser.setText(
                "Result: a unique image\n"
                "Addition all the images in input, and then multiply all the intensity by a coefficient"
            )
            self.textBrowser_2.setText("[  6,   4,  0]           [12,   8,  0]\n[  0,   0,  4] * 2 = [  0,   0,  8]\n[10, "
            "10, 2]           [20, 20, 4]")

        elif item == "and":
            self.argument_name.setText("No argument")
            self.set_arguments_editable(False)
            self.textBrowser.setText(
                "Result: a unique image\n"
                "Realize the boolean intersection of the images in input. For each voxel in an image, if the intensity"
                "is superior to 0, this voxel is considered as true. The result is a unique image where each voxel"
                "is the intersection of voxels from the input images. "
            )
            self.textBrowser_2.setText("[5, 0, 0]        [2, 0, 2]     [ True, False, False]        [ True, False, True]      [ 1, 0, 0]\n"
            "[0, 3, 0] OR [0, 0, 0] = [ False, True, False] OR [ False, False, False] = [ 0, 0, 0]\n"
            "[0, 0, 4]        [1, 0, 1]     [ False, False, True]        [ True, False, True]      [ 0, 0, 1]")

        elif item == "or":
            self.argument_name.setText("No argument")
            self.set_arguments_editable(False)
            self.textBrowser.setText(
                "Result: a unique image\n"
                "Realize the boolean union of the images in input. For each voxel in an image, if the intensity"
                "is superior to 0, this voxel is considered as true. The result is a unique image where each voxel"
                "is the union of voxels from the input images."
            )
            self.textBrowser_2.setText("[5, 0, 0]        [2, 0, 2]     [ True, False, False]        [ True, False, True]      [ 1, 0, 1]\n"
            "[0, 3, 0] OR [0, 0, 0] = [ False, True, False] OR [ False, False, False] = [ 0, 1, 0]\n"
            "[0, 0, 4]        [1, 0, 1]     [ False, False, True]        [ True, False, True]      [ 1, 0, 1]")

        elif item == "closing":
            self.argument_name.setText("Number of iterations")
            self.set_arguments_editable(True, "1")
            self.textBrowser.setText(
                "Result : one image by image in input\n"
                "In mathematical morphology, the closing of a set (binary image) A by a structuring element B is the "
                "erosion of the dilation of that set, A * B = ( A (+) B ) (-) B, denote the dilation and erosion, "
                "respectively. In image processing, closing is, together with opening, the basic workhorse of "
                "morphological noise removal. Opening removes small objects, while closing removes small holes."
            )
            self.textBrowser_2.setText("                [0,1,0,0,0,0,0,0]      [0,1,0,0,0,0,0,0]  \n"
            "                [0,0,1,0,1,0,0,0]      [0,0,1,1,1,0,0,0]  \n"
            "Closing([0,0,0,1,1,1,0,0]) = [0,0,0,1,1,1,0,0]  \n"
            "                [0,0,1,1,1,1,1,0]      [0,0,1,1,1,1,1,0]  \n"
            "                [0,0,0,1,1,1,0,0]      [0,0,0,1,1,1,0,0]  \n"
            )

        elif item == "dilation":
            self.argument_name.setText("Number of iterations")
            self.set_arguments_editable(True, "1")
            self.textBrowser.setText(
                "Result : one image by image in input\n"
                "Dilation (usually represented by (+)) is one of the basic operations in mathematical morphology. "
                "Originally developed for binary images, it has been expanded first to grayscale images, and then to "
                "complete lattices. The dilation operation usually uses a structuring element for probing and "
                "expanding the shapes contained in the input image."
            )
            self.textBrowser_2.setText("                 [0,1,0,0,0,0,0,0]      [1,1,1,0,0,0,0,0]  \n"
            "                 [0,0,1,0,1,0,0,0]      [0,1,1,1,1,1,0,0]  \n"
            "Dilation([0,0,0,1,1,1,0,0]) = [0,0,1,1,1,1,1,0]  \n"
            "                 [0,0,1,1,1,1,1,0]      [0,1,1,1,1,1,1,1]  \n"
            "                 [0,0,0,1,1,1,0,0]      [0,0,1,1,1,1,1,0]  \n"
            )

        elif item == "erosion":
            self.argument_name.setText("Number of iterations")
            self.set_arguments_editable(True, "1")
            self.textBrowser.setText(
                "Result : one image by image in input\n"
                "Erosion (usually represented by (-)) is one of two fundamental operations (the other being dilation) "
                "in morphological image processing from which all other morphological operations are based. It was "
                "originally defined for binary images, later being extended to grayscale images, and subsequently to "
                "complete lattices."
            )
            self.textBrowser_2.setText("                [0,1,0,0,0,0,0,0]      [0,0,0,0,0,0,0,0]  \n"
            "                [0,0,1,0,1,0,0,0]      [0,0,0,0,0,0,0,0]  \n"
            "Erosion([0,0,0,1,1,1,0,0]) = [0,0,0,0,1,0,0,0]  \n"
            "                [0,0,1,1,1,1,1,0]      [0,0,0,1,1,1,0,0]  \n"
            "                [0,0,0,1,1,1,0,0]      [0,0,0,0,1,0,0,0]  \n"
            )

        elif item == "opening":
            self.argument_name.setText("Number of iterations")
            self.set_arguments_editable(True, "1")
            self.textBrowser.setText(
                "Result : one image by image in input\n"
                "In morphological opening ( A (-) B ) (+) B, erosion operation removes objects that are smaller than "
                "structuring element B and dilation operation restores the shape of remaining objects. However, "
                "restoring accuracy in dilation operation highly depends on the type of structuring element and the "
                "shape of restoring objects. The opening by reconstruction method is able to restore the objects "
                "completely after erosion applied."
            )
            self.textBrowser_2.setText("                  [0,1,0,0,0,0,0,0]      [0,0,0,0,0,0,0,0]  \n"
            "                  [0,0,1,0,1,0,0,0]      [0,0,0,0,0,0,0,0]  \n"
            "Opening([0,0,0,1,1,1,0,0]) = [0,0,0,1,1,1,0,0]  \n"
            "                  [0,0,1,1,1,1,1,0]      [0,0,1,1,1,1,1,0]  \n"
            "                  [0,0,0,1,1,1,0,0]      [0,0,0,1,1,1,0,0]  \n"
            )

        elif item == "threshold":
            self.argument_name.setText("min,max")
            self.set_arguments_editable(True, "0.0,1.0")
            self.textBrowser.setText(
                "Result : one image by image in input\n"
                "The threshold operation allows you to store only voxels whose intensity value is between the min and "
                "max parameters (min <= intensity <= max). All voxels that do not meet this criterion have their "
                "intensity that becomes zero. "
                "If no value is assigned to min and max then their values will be less the infinite and the less "
                "infinite respectively."
            )
            self.textBrowser_2.setText("                     [-5, 1, 0]  [2, 0, 2]       [0, 1, 0]  [0, 0, 0]\n"
            "threshold([-1, 3, 0], [1, 1, 0]) = ([0, 0, 0], [1, 1, 0]) avec min = 0 et max = 1\n"
            "                     [0, 1, 4]   [1, 0, 1]       [0, 1, 0]  [1, 0, 1]")

    def run_calculation(self):
        algorithm = self.leftlist.currentItem().text()
        arguments = self.arguments_line.text()

        img_selected = []
        for collection in BrainMapper.collshow:
            for img in collection.nifimage_dict.values():
                img_selected.append(img)

        self.console.setText("Calculation successful")

        if algorithm == "addition":
            result = [BrainMapper.calcul.addition_operation(img_selected)]
            self.popUpSaveFileResultCalculation(algorithm, result)

        elif algorithm == "division":
            try:
                coefficient = float(arguments)
            except ValueError:
                self.give_argument_error()
            else:
                result = [BrainMapper.calcul.division_operation(img_selected, coefficient)]
                self.popUpSaveFileResultCalculation(algorithm, result)

        elif algorithm == "linear combination":
            try:
                coefficients = [float(i) for i in arguments.split(",")]
            except ValueError:
                self.give_argument_error()
            else:
                result = [BrainMapper.calcul.linear_combination_operation(img_selected, coefficients)]
                self.popUpSaveFileResultCalculation(algorithm, result)

        elif algorithm == "mean":
            result = [BrainMapper.calcul.mean_operation(img_selected)]
            self.popUpSaveFileResultCalculation(algorithm, result)

        elif algorithm == "multiplication":
            try:
                coefficient = float(arguments)
            except ValueError:
                self.give_argument_error()
            else:
                result = [BrainMapper.calcul.multiplication_operation(img_selected, coefficient)]
                self.popUpSaveFileResultCalculation(algorithm, result)

        elif algorithm == "and":
            result = [BrainMapper.calcul.and_operation(img_selected)]
            self.popUpSaveFileResultCalculation(algorithm, result)

        elif algorithm == "or":
            result = [BrainMapper.calcul.or_operation(img_selected)]
            self.popUpSaveFileResultCalculation(algorithm, result)

        elif algorithm in ["closing", "dilation", "erosion", "opening"]:
            try:
                number_of_iterations = int(arguments)
            except ValueError:
                self.give_argument_error()
            else:
                result = BrainMapper.calcul.image_operation_from_str(
                    img_selected, number_of_iterations, algorithm)
                self.popUpSaveFileResultCalculation(algorithm, result)

        elif algorithm == "threshold":
            try:
                list_of_arguments = arguments.split(",")
                threshold_min = float(list_of_arguments[0])
                threshold_max = float(list_of_arguments[1])
            except ValueError:
                self.give_argument_error()
            else:
                result = BrainMapper.calcul.threshold_operation(img_selected, threshold_min, threshold_max )
                self.popUpSaveFileResultCalculation(algorithm, result)


    def give_argument_error(self):
        QtGui.QMessageBox.warning(self, "Error", "Given argument aren't corrects.")

    # noinspection PyMethodMayBeStatic,PyMethodMayBeStatic
    def count_images(self) -> int:
        img_selected = []
        for collection in BrainMapper.collshow:
            for img in collection.nifimage_dict.values():
                img_selected.append(img)
        return len(img_selected)

    # noinspection PyMethodMayBeStatic,PyMethodMayBeStatic
    def get_images_names(self) -> list:
        img_selected = []
        for collection in BrainMapper.collshow:
            for img in collection.nifimage_dict.values():
                img_selected.append(img.filename)
        return img_selected

    def go_back(self):
        self.showMain.emit()

    def retranslate_ui(self, form):
        form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Arguments", None))
        self.argument_name.setText(_translate("Form", "Name of argument", None))
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

    def popUpSaveFileResultCalculation(self, algorithm, result):
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
            setCalculation = BrainMapper.Set("calc_", 1, [len(globalSets[1])])
            setCalculation.set_name("calc_" + algorithm + "_" + str(id(setCalculation))[:5])
            coll = BrainMapper.ImageCollection("coll_", setCalculation)
            coll.set_name("coll_" + algorithm + "_" + str(id(coll)))
            for matrixData in result:
                template_mni_path = 'ressources/template_mni/mni_icbm152_t1_tal_nlin_asym_09a.nii'
                template_data = load(template_mni_path)
                template_affine = template_data.affine
                recreate_image = Nifti1Image(matrixData, template_affine)
                ni_image = BrainMapper.NifImage("" + str(time.time() * 1000), recreate_image)
                ni_image.set_filename("file_" + str(algorithm) + "_" + str(id(ni_image)) + ".nii")
                coll.add(ni_image)
            setCalculation.add_collection(coll)
            BrainMapper.makeCalculResultSet(setCalculation)
            self.console.setText(self.console.toPlainText()+"\n \nA new set has been created with the name: %s" %(setCalculation.get_name()) )
