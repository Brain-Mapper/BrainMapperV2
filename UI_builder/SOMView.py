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
from PyQt4.QtCore import Qt, QRect, pyqtSignal, QSize
from BrainMapper import *

import math
import tkinter
import pandas as pd
from neupy import algorithms, utils
from scipy.spatial import distance
import matplotlib.pyplot as plt

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

GRID_HEIGHT = 0
GRID_WIDTH = 0
data_neuron_index = []


class InfoButton(QtGui.QPushButton):
    def __init__(self, widget):
        super(InfoButton, self).__init__(parent=widget)
        self.message = ""
        self.setFixedSize(QSize(20, 20))
        self.setText("?")
        self.clicked.connect(self.open)

    def setMessage(self, message):
        self.message = message

    def open(self):
        QtGui.QMessageBox.information(self, "Information", self.message, "ok")


class SOMView(QtGui.QWidget):
    showMain = pyqtSignal()

    def __init__(self):
        super(SOMView, self).__init__()
        self.setupUi(self)

    def fill_table(self, som_input: pd.DataFrame):
        """ Fills this custom table with the data of a UsableDataSet obtained after data extraction.

            :param som_input: dataframe resulting from :func:`~ourLib.image.som_preparation`
            :return: Nothing
            """

        self.som_input = som_input
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))

        font.setPointSize(8)
        self.tableWidget.setColumnCount(len(som_input.columns))
        self.tableWidget.setRowCount(len(som_input))
        for i in range(self.comboBox.count(), -1, -1):
            self.comboBox.removeItem(i)

        for i, column_name in enumerate(som_input.columns):
            item = QtGui.QTableWidgetItem()
            item.setFont(font)
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
            self.tableWidget.setHorizontalHeaderItem(i, item)
            item.setText(column_name)
            if column_name not in ["X", "Y", "Z"]:
                self.comboBox.addItem(column_name)
                # self.comboBox.setItemText(i, column_name)
        self.tableWidget.horizontalHeader().setVisible(True)
        for i in range(0, len(som_input)):
            for j, column_name in enumerate(som_input.columns):
                item = QtGui.QTableWidgetItem(str(som_input.at[i, column_name]))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.tableWidget.setItem(i, j, item)

        self.pushButton_show.setEnabled(False)

    def go_back(self):
        self.showMain.emit()

    def train(self):
        self.pushButton_show.setEnabled(True)

        global GRID_WIDTH
        global GRID_HEIGHT
        global data_neuron_index
        global last_column

        # You can use the below function when testing to eliminate the randomness
        # utils.reproducible()

        training_data = self.som_input[["X", "Y", "Z"]].values

        GRID_HEIGHT = int(self.lineEdit_hauteur.text())
        GRID_WIDTH = int(self.lineEdit_largeur.text())

        sofm = algorithms.SOFM(
            n_inputs=3,

            # In clustering application we will prefer that
            # clusters will be updated independently from each
            # other. For this reason we set up learning radius
            # equal to zero
            learning_radius=float(self.lineEdit_radius.text()),

            # Parameters controls learning rate for each neighbour. The further neighbour neuron from the
            # winning neuron the smaller that learning rate for it. Learning rate scales based on the
            # factors produced by the normal distribution with center in the place of a winning neuron and
            # standard deviation specified as a parameter. The learning rate for the winning neuron is
            # always equal to the value specified in the step parameter and for neighbour neurons it’s
            # always lower.
            std=float(self.lineEdit_std.text()),  # TODO : modifier

            # Feature grid defines shape of the output neurons. The new shape should be compatible with      #the
            # number of outputs
            features_grid=(GRID_HEIGHT, GRID_WIDTH),

            # Defines connection type in feature grid
            grid_type='rect',

            # Defines function that will be used to compute closest weight to the input sample
            distance='euclid',

            # Instead of generating random weights
            # (features / cluster centers) SOFM will sample
            # them from the data. Which means that after
            # initialization step 3 random data samples will
            # become cluster centers
            # weight='sample_from_data',

            # Training step size or learning rate
            step=float(self.lineEdit_step.text()),

            # Shuffles dataset before every training epoch.
            shuffle_data=True,

            # Shows training progress in terminal
            verbose=True,
        )

        sofm.train(training_data, int(self.lineEdit_nbiter.text()))

        weight = sofm.weight
        param_length = sofm.weight.shape[0]
        param_width = sofm.weight.shape[1]

        neurons = []
        for j in range(param_width):
            temp = []
            for i in range(param_length):
                temp.append(weight[i, j])
            neurons.append(temp)

        data_neuron_index = []
        for k in training_data:
            distance_min = distance.euclidean(k, neurons[0])
            best_neuron_index = 0
            for neuron_index in range(len(neurons)):
                new_distance = distance.euclidean(k, neurons[neuron_index])
                if new_distance < distance_min:
                    distance_min = new_distance
                    best_neuron_index = neuron_index
            data_neuron_index.append(best_neuron_index)

        self.pushButton_show.setEnabled(True)

        QtGui.QMessageBox.information(self, "Training done",
                                      "The training is done you can visualize by clicking on the show button.")

    def showmap(self):
        global GRID_WIDTH
        global GRID_HEIGHT
        global data_neuron_index

        column_name = self.comboBox.currentText()

        column_for_som = self.som_input[[column_name]].values

        print(f"data_neuron_index {data_neuron_index}")

        x = list(range(0, GRID_WIDTH))
        y = list(range(0, GRID_HEIGHT))

        img = np.zeros(shape=(GRID_HEIGHT, GRID_WIDTH))

        for neuron_index, column_value in zip(data_neuron_index, column_for_som):
            neuron_i = int(neuron_index / GRID_WIDTH)
            neuron_j = neuron_index % GRID_WIDTH
            img[neuron_i, neuron_j] = img[neuron_i, neuron_j] + 1 if column_value == 1 else img[neuron_i, neuron_j] - 1

        fig, ax = plt.subplots()
        im = ax.imshow(img, cmap="inferno", origin="lower")
        # Set the ticks
        ax.set_xticks(x)
        ax.set_yticks(y)
        ax.set_xticks(np.arange(img.shape[1] + 1) - .5, minor=True)
        ax.set_yticks(np.arange(img.shape[0] + 1) - .5, minor=True)
        ax.tick_params(length=0, width=0, which='both')
        # Set a colorbar
        cbar = ax.figure.colorbar(im,
                                  ax=ax,
                                  ticks=list(range(int(np.min(img)), int(np.max(img)) + 1)),
                                  orientation="horizontal")
        cbar_legend = f"Number of points with {column_name} - number of points with {column_name.replace('=','≠')}"
        cbar.ax.set_xlabel(cbar_legend)
        # Add black contour
        #ax.grid(which="minor", color="black", linestyle='-', linewidth=1)
        ax.set_title(f"SOM for {column_name}")
        fig.tight_layout()
        plt.show()

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
        self.pushButton_5 = self.help_button_height = InfoButton(self.widget_param)
        self.pushButton_5.setMessage("This is the learning rate.")
        self.pushButton_5.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.gridLayout_5.addWidget(self.pushButton_5, 6, 0, 1, 3)
        self.lineEdit_step = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_step.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_step.setObjectName(_fromUtf8("lineEdit_step"))
        self.lineEdit_step.setText("0.1")
        self.gridLayout_5.addWidget(self.lineEdit_step, 6, 6, 1, 1)
        self.pushButton_4 = self.help_button_height = InfoButton(self.widget_param)
        self.pushButton_4.setMessage(
            "One epoch is when an entire dataset is passed forward and backward through the neural network only once.")
        self.pushButton_4.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.gridLayout_5.addWidget(self.pushButton_4, 2, 0, 1, 1)
        self.lineEdit_std = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_std.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_std.setObjectName(_fromUtf8("lineEdit_std"))
        self.lineEdit_std.setText("1")
        self.gridLayout_5.addWidget(self.lineEdit_std, 10, 6, 1, 1)
        self.lineEdit_nbiter = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_nbiter.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_nbiter.setObjectName(_fromUtf8("lineEdit_nbiter"))
        self.lineEdit_nbiter.setText("10")
        self.gridLayout_5.addWidget(self.lineEdit_nbiter, 2, 6, 1, 1)
        self.pushButton_7 = self.help_button_height = InfoButton(self.widget_param)
        self.pushButton_7.setMessage(
            "This parameter controls learning rate for each neighbor. Learning rate scales based on the factors produced by the normal distribution with center in the place of a winning neuron and standard deviation specified as a parameter. The learning rate for the winning neuron is always equal to the value specified in the step parameter and for neighbour neurons it’s always lower.")
        self.pushButton_7.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.gridLayout_5.addWidget(self.pushButton_7, 10, 0, 1, 3)
        self.label_nbiter = QtGui.QLabel(self.widget_param)
        self.label_nbiter.setObjectName(_fromUtf8("label_nbiter"))
        self.gridLayout_5.addWidget(self.label_nbiter, 2, 3, 1, 1)
        self.lineEdit_largeur = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_largeur.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_largeur.setObjectName(_fromUtf8("lineEdit_largeur"))
        self.lineEdit_largeur.setText("20")
        self.gridLayout_5.addWidget(self.lineEdit_largeur, 1, 6, 1, 1)
        self.lineEdit_hauteur = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_hauteur.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_hauteur.setObjectName(_fromUtf8("lineEdit_hauteur"))
        self.lineEdit_hauteur.setText("20")
        self.gridLayout_5.addWidget(self.lineEdit_hauteur, 0, 6, 1, 1)
        self.pushButton_3 = self.help_button_height = InfoButton(self.widget_param)
        self.pushButton_3.setMessage(
            "Feature grid defines shape of the output neurons. Width is the width of the feature grid.")
        self.pushButton_3.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout_5.addWidget(self.pushButton_3, 1, 0, 1, 2)
        self.pushButton_2 = self.help_button_height = InfoButton(self.widget_param)
        self.pushButton_2.setMessage(
            "Feature grid defines shape of the output neurons. Height is the height of the feature grid.")
        self.pushButton_2.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout_5.addWidget(self.pushButton_2, 0, 0, 1, 3)
        self.pushButton_6 = self.help_button_height = InfoButton(self.widget_param)
        self.pushButton_6.setMessage(
            "Parameter defines radius within which we consider all neurons as neighbours to the winning neuron. The bigger the value the more neurons will be updated after each iteration.")
        self.pushButton_6.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.gridLayout_5.addWidget(self.pushButton_6, 7, 0, 1, 1)
        self.lineEdit_radius = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_radius.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_radius.setObjectName(_fromUtf8("lineEdit_radius"))
        self.lineEdit_radius.setText("2")
        self.gridLayout_5.addWidget(self.lineEdit_radius, 7, 6, 1, 1)
        self.label_radius = QtGui.QLabel(self.widget_param)
        self.label_radius.setObjectName(_fromUtf8("label_radius"))
        self.gridLayout_5.addWidget(self.label_radius, 7, 3, 1, 1)
        self.label_std = QtGui.QLabel(self.widget_param)
        self.label_std.setObjectName(_fromUtf8("label_std"))
        self.gridLayout_5.addWidget(self.label_std, 10, 3, 1, 3)
        self.label_step = QtGui.QLabel(self.widget_param)
        self.label_step.setObjectName(_fromUtf8("label_step"))
        self.gridLayout_5.addWidget(self.label_step, 6, 3, 1, 1, )
        self.label_largeur = QtGui.QLabel(self.widget_param)
        self.label_largeur.setObjectName(_fromUtf8("label_largeur"))
        self.gridLayout_5.addWidget(self.label_largeur, 1, 3, 1, 1)
        self.label_hauteur = QtGui.QLabel(self.widget_param)
        self.label_hauteur.setObjectName(_fromUtf8("label_hauteur"))
        self.gridLayout_5.addWidget(self.label_hauteur, 0, 3, 1, 1)
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
        self.pushButton_train.clicked.connect(self.train)
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
        self.gridLayout_2.addWidget(self.comboBox, 0, 1, 1, 1)
        self.pushButton_show = QtGui.QPushButton(self.widget_button)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButton_show.setFont(font)
        self.pushButton_show.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.pushButton_show.setObjectName(_fromUtf8("pushButton_show"))
        self.pushButton_show.clicked.connect(self.showmap)
        self.gridLayout_2.addWidget(self.pushButton_show, 0, 2, 1, 1)
        self.pushButton_goback = QtGui.QPushButton(self.widget_button)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButton_goback.setFont(font)
        self.pushButton_goback.setStyleSheet(_fromUtf8("background-color: rgb(209, 209, 209);"))
        self.pushButton_goback.setObjectName(_fromUtf8("pushButton_goback"))
        self.gridLayout_2.addWidget(self.pushButton_goback, 0, 3, 1, 1)
        self.pushButton_goback.clicked.connect(self.go_back)
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
        self.tableWidget = QtGui.QTableWidget(self.widget_table)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout_3.addWidget(self.tableWidget, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.widget_table, 0, 1, 1, 1)


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_param.setText(_translate("Form", "Parameters", None))
        self.pushButton_5.setText(_translate("Form", "?", None))
        self.pushButton_4.setText(_translate("Form", "?", None))
        self.pushButton_7.setText(_translate("Form", "?", None))
        self.label_nbiter.setText(_translate("Form", "Epochs", None))
        self.pushButton_3.setText(_translate("Form", "?", None))
        self.pushButton_2.setText(_translate("Form", "?", None))
        self.pushButton_6.setText(_translate("Form", "?", None))
        self.label_radius.setText(_translate("Form", "Radius", None))
        self.label_std.setText(_translate("Form", "Std", None))
        self.label_step.setText(_translate("Form", "Step", None))
        self.label_largeur.setText(_translate("Form", "Width", None))
        self.label_hauteur.setText(_translate("Form", "Height", None))
        self.pushButton_train.setText(_translate("Form", "Train", None))
        self.pushButton_show.setText(_translate("Form", "Show", None))
        self.pushButton_goback.setText(_translate("Form", "Go back", None))
        self.label_data.setText(_translate("Form", "Data used for the Self Organizing Map ( SOM)", None))
