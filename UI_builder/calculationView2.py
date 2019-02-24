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

        ## Operations item ##
        # Operations which return only one matrix
        self.leftlist.addItem('addition')
        self.leftlist.addItem('division')
        self.leftlist.addItem('linear combinaison')
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
        Update the displayed information
        """
        item = self.leftlist.currentItem().text()

        if item == "addition":
            self.argument_name.setText("No argument")
            self.set_arguments_editable(False)
            self.textBrowser.setText(
                ""
            )

        elif item == "division":
            self.argument_name.setText("Coefficient")
            self.set_arguments_editable(True, "1")
            self.textBrowser.setText(
                ""
            )

        elif item == "linear combinaison":
            self.argument_name.setText("Coefficients")
            basic_coefficients =
            self.set_arguments_editable(True)
            self.textBrowser.setText(
                ""
            )

        elif item == "multiplication":
            self.argument_name.setText("Coefficient")
            self.set_arguments_editable(True)
            self.textBrowser.setText(
                ""
            )

    def count_nifti(selfs) -> int:
        img_selected = []
        for collection in collshow:
            for img in collection.nifimage_dict.values():
                img_selected.append(img)
        return len(img)



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
