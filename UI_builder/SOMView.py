# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SOM.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from typing import List, Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, pyqtSignal, QSize
from neupy import algorithms
from scipy.spatial import distance

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
        self.som_input: pd.DataFrame = None  # Input of the SOM as a Dataframe
        self.features_columns: List[str] = None  # Columns usable for the vizualisation
        # Som configuration
        self.grid_height: int = None
        self.grid_width: int = None
        # Som results
        self.data_neuron_index: List[int] = None  # List of association date to neuron
        self.imgs_result: Dict[str: np.ndarray] = None  # Visualisation result
        self.setupUi(self)

    def fill_table(self, som_input: pd.DataFrame):
        """ Fills this custom table with the data of a UsableDataSet obtained after data extraction.

            :param som_input: dataframe resulting from :func:`~ourLib.image.som_preparation`
            :return: Nothing
            """

        self.som_input = som_input
        self.features_columns = []

        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))

        font.setPointSize(8)

        # Set the size of the widget
        self.tableWidget.setColumnCount(len(som_input.columns))
        self.tableWidget.setRowCount(len(som_input))

        # Clean the comboBox
        for i in range(self.comboBox.count(), -1, -1):
            self.comboBox.removeItem(i)

        # Add the column header and the elements to the comboBox
        for i, column_name in enumerate(som_input.columns):
            item = QtGui.QTableWidgetItem()
            item.setFont(font)
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
            self.tableWidget.setHorizontalHeaderItem(i, item)
            item.setText(column_name)
            if column_name not in ["X", "Y", "Z"]:
                self.features_columns.append(column_name)
                self.comboBox.addItem(column_name)
        self.tableWidget.horizontalHeader().setVisible(True)

        # Add the data
        for i in range(0, len(som_input)):
            for j, column_name in enumerate(som_input.columns):
                item = QtGui.QTableWidgetItem(str(som_input.at[i, column_name]))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.tableWidget.setItem(i, j, item)

        # The columns are selectable
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectColumns)

        # The button show has to be disable while the som has not been trained
        self.comboBox.setEnabled(False)
        self.pushButton_show.setEnabled(False)

    def go_back(self):
        self.showMain.emit()

    def train(self):
        self.comboBox.setEnabled(False)
        self.pushButton_show.setEnabled(False)

        self.pushButton_train.setText("Preparing training")
        QtGui.qApp.processEvents()

        # Get the columns used to make the map
        items = self.tableWidget.selectedItems()

        columns = []

        if len(items) != 0:
            for index in range(0, len(items), self.tableWidget.rowCount()):
                columns.append(self.tableWidget.horizontalHeaderItem(items[index].column()).text())
        else:
            columns = ["X", "Y", "Z"]

        training_data = self.som_input[columns].values

        self.grid_height = int(self.lineEdit_height.text())
        self.grid_width = int(self.lineEdit_width.text())

        def on_epoch_start(optimizer):
            self.pushButton_train.setText(f"In training (epoch : {optimizer.last_epoch})")
            QtGui.qApp.processEvents()

        sofm = algorithms.SOFM(
            n_inputs=len(columns),

            # In clustering application we will prefer that
            # clusters will be updated independently from each
            # other. For this reason we set up learning radius
            # equal to zero
            learning_radius=float(self.lineEdit_radius.text()),
            reduce_radius_after=float(self.lineEdit_reduce_radius_after.text()),

            # Parameters controls learning rate for each neighbour. The further neighbour neuron from the
            # winning neuron the smaller that learning rate for it. Learning rate scales based on the
            # factors produced by the normal distribution with center in the place of a winning neuron and
            # standard deviation specified as a parameter. The learning rate for the winning neuron is
            # always equal to the value specified in the step parameter and for neighbour neurons it’s
            # always lower.
            std=float(self.lineEdit_std.text()),
            reduce_std_after=int(self.lineEdit_reduce_std_after.text()),

            # Feature grid defines shape of the output neurons. The new shape should be compatible with      #the
            # number of outputs
            features_grid=(self.grid_height, self.grid_width),

            # Defines connection type in feature grid
            grid_type='rect',

            # Defines function that will be used to compute closest weight to the input sample
            distance='euclid',

            # Training step size or learning rate
            step=float(self.lineEdit_step.text()),
            reduce_step_after=int(self.lineEdit_reduce_std_after.text()),

            # Shuffles dataset before every training epoch.
            shuffle_data=True,

            # Shows training progress in terminal
            verbose=False,

            # Signals
            signals=on_epoch_start,
        )

        number_of_epochs = int(self.lineEdit_nepochs.text())

        sofm.train(training_data, number_of_epochs)

        self.pushButton_train.setText("Formatting the results")
        QtGui.qApp.processEvents()

        weight = sofm.weight
        param_length = sofm.weight.shape[0]
        param_width = sofm.weight.shape[1]

        neurons = []
        for j in range(param_width):
            temp = []
            for index in range(param_length):
                temp.append(weight[index, j])
            neurons.append(temp)

        # Wipe the results
        # self.data_neuron_index = []

        self.imgs_result = {"__all__": np.zeros(shape=(self.grid_height, self.grid_width))}
        for column in self.features_columns:
            self.imgs_result[column] = np.zeros(shape=(self.grid_height, self.grid_width))

        # Associate each date to its neuron
        for index, data in enumerate(training_data):
            distance_min = distance.euclidean(data, neurons[0])
            best_neuron_index = 0
            for neuron_index in range(len(neurons)):
                new_distance = distance.euclidean(data, neurons[neuron_index])
                if new_distance < distance_min:
                    distance_min = new_distance
                    best_neuron_index = neuron_index
            # self.data_neuron_index.append(best_neuron_index)

            # Calculate the weight of each feature
            neuron_i = int(best_neuron_index / self.grid_width)
            neuron_j = best_neuron_index % self.grid_width
            self.imgs_result["__all__"][neuron_i, neuron_j] = self.imgs_result["__all__"][neuron_i, neuron_j] + 1
            for column in self.features_columns:
                if self.som_input[column][index] == 1:
                    self.imgs_result[column][neuron_i, neuron_j] = self.imgs_result[column][neuron_i, neuron_j] + 1

        for i in range(0, self.grid_height):
            for j in range(0, self.grid_width):
                number_of_data_in_neuron = self.imgs_result["__all__"][i, j]
                if number_of_data_in_neuron == 0:
                    for column in self.features_columns:
                        self.imgs_result[column][i, j] = 0.5
                else:
                    for column in self.features_columns:
                        self.imgs_result[column][i, j] = self.imgs_result[column][i, j] / number_of_data_in_neuron

        QtGui.QMessageBox.information(self, "Training done",
                                      f"The training is done you can visualize by clicking on the show button. "
                                      f"(You have used the columns: {columns})")
        self.comboBox.setEnabled(True)
        self.pushButton_show.setEnabled(True)
        self.pushButton_train.setText("Train")

    def showmap(self):
        column_name = self.comboBox.currentText()

        x = list(range(0, self.grid_width))
        y = list(range(0, self.grid_height))

        img = self.imgs_result[column_name]

        fig, ax = plt.subplots()
        im = ax.imshow(img, cmap="inferno", origin="lower", vmin=0, vmax=1)
        # Set the ticks
        ax.set_xticks(x)
        ax.set_yticks(y)
        ax.set_xticks(np.arange(img.shape[1] + 1) - .5, minor=True)
        ax.set_yticks(np.arange(img.shape[0] + 1) - .5, minor=True)
        ax.tick_params(length=0, width=0, which='both')
        # Set a colorbar
        cbar = ax.figure.colorbar(im,
                                  ax=ax,
                                  ticks=list([0, 0.25, 0.5, 0.75, 1]),
                                  orientation="horizontal")
        cbar_legend = f"Number of points with {column_name}/ Number of points"
        cbar.ax.set_xlabel(cbar_legend)
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
        self.label_std = QtGui.QLabel(self.widget_param)
        self.label_std.setObjectName(_fromUtf8("label_std"))
        self.gridLayout_5.addWidget(self.label_std, 11, 3, 1, 1)
        self.label_step = QtGui.QLabel(self.widget_param)
        self.label_step.setObjectName(_fromUtf8("label_step"))
        self.gridLayout_5.addWidget(self.label_step, 6, 3, 1, 1)
        self.label_width = QtGui.QLabel(self.widget_param)
        self.label_width.setObjectName(_fromUtf8("label_width"))
        self.gridLayout_5.addWidget(self.label_width, 1, 3, 1, 1)
        self.label_radius = QtGui.QLabel(self.widget_param)
        self.label_radius.setObjectName(_fromUtf8("label_radius"))
        self.gridLayout_5.addWidget(self.label_radius, 8, 3, 1, 1)
        self.label_height = QtGui.QLabel(self.widget_param)
        self.label_height.setObjectName(_fromUtf8("label_height"))
        self.gridLayout_5.addWidget(self.label_height, 0, 3, 1, 1)

        self.pushButton_5 = InfoButton(self.widget_param)
        self.pushButton_5.setMessage("[positive real]\n"
                                     "This is the learning rate. The lower this value is, the less the neurons are"
                                     "modified at each step.")
        self.pushButton_5.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.gridLayout_5.addWidget(self.pushButton_5, 6, 0, 1, 3)

        self.lineEdit_step = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_step.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_step.setObjectName(_fromUtf8("lineEdit_step"))
        self.gridLayout_5.addWidget(self.lineEdit_step, 6, 6, 1, 1)

        self.pushButton_7 = InfoButton(self.widget_param)
        self.pushButton_7.setMessage("[positive real]\n"
                                     "This parameter controls learning rate for each neighbor. Learning rate scales "
                                     "based on the factors produced by the normal distribution with center in the "
                                     "place of a winning neuron and standard deviation specified as a parameter. The "
                                     "learning rate for the winning neuron is always equal to the value specified in "
                                     "the step parameter and for neighbour neurons it’s always lower.")
        self.pushButton_7.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.gridLayout_5.addWidget(self.pushButton_7, 11, 0, 1, 3)

        self.pushButton_3 = InfoButton(self.widget_param)
        self.pushButton_3.setMessage("[positive integer]\n"
                                     "Width of the map."
                                     )
        self.pushButton_3.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout_5.addWidget(self.pushButton_3, 1, 0, 1, 2)

        self.pushButton_6 = InfoButton(self.widget_param)
        self.pushButton_6.setMessage("[positive integer]\n"
                                     "Parameter defines radius within which we consider all neurons as neighbours to "
                                     "the winning neuron. The bigger the value the more neurons will be updated after"
                                     " each iteration.")
        self.pushButton_6.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.gridLayout_5.addWidget(self.pushButton_6, 8, 0, 1, 1)

        self.lineEdit_width = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_width.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_width.setObjectName(_fromUtf8("lineEdit_width"))
        self.gridLayout_5.addWidget(self.lineEdit_width, 1, 6, 1, 1)
        self.lineEdit_radius = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_radius.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_radius.setObjectName(_fromUtf8("lineEdit_radius"))
        self.gridLayout_5.addWidget(self.lineEdit_radius, 8, 6, 1, 1)

        self.pushButton_2 = InfoButton(self.widget_param)
        self.pushButton_2.setMessage("[positive integer]\n"
                                     "Height of the map."
                                     )
        self.pushButton_2.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout_5.addWidget(self.pushButton_2, 0, 0, 1, 3)

        self.lineEdit_height = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_height.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_height.setObjectName(_fromUtf8("lineEdit_height"))
        self.gridLayout_5.addWidget(self.lineEdit_height, 0, 6, 1, 1)
        self.lineEdit_nepochs = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_nepochs.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_nepochs.setObjectName(_fromUtf8("lineEdit_nepochs"))
        self.gridLayout_5.addWidget(self.lineEdit_nepochs, 4, 6, 1, 1)
        self.label_nbiter = QtGui.QLabel(self.widget_param)
        self.label_nbiter.setObjectName(_fromUtf8("label_nbiter"))
        self.gridLayout_5.addWidget(self.label_nbiter, 4, 3, 1, 1)
        self.lineEdit_reduce_radius_after = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_reduce_radius_after.setObjectName(_fromUtf8("lineEdit_reduce_radius_after"))
        self.gridLayout_5.addWidget(self.lineEdit_reduce_radius_after, 9, 6, 1, 1)
        self.lineEdit_reduce_step_after = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_reduce_step_after.setObjectName(_fromUtf8("lineEdit_reduce_step_after"))
        self.gridLayout_5.addWidget(self.lineEdit_reduce_step_after, 7, 6, 1, 1)
        self.lineEdit_reduce_std_after = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_reduce_std_after.setObjectName(_fromUtf8("lineEdit_reduce_std_after"))
        self.gridLayout_5.addWidget(self.lineEdit_reduce_std_after, 12, 6, 1, 1)

        self.QPushButton_reduce_step_after_button = InfoButton(self.widget_param)
        self.QPushButton_reduce_step_after_button.setMessage(
            "[positive integer]\n"
            "Defines reduction rate at which parameter step will be reduced using the following formula:"
            "\nstep = step / (1 + current_epoch / reduce_step_after)"
        )
        self.QPushButton_reduce_step_after_button.setMaximumSize(QtCore.QSize(30, 16777215))
        self.QPushButton_reduce_step_after_button.setObjectName(_fromUtf8("QPushButton_reduce_step_after_button"))
        self.gridLayout_5.addWidget(self.QPushButton_reduce_step_after_button, 7, 0, 1, 1)

        self.pushButton_4 = InfoButton(self.widget_param)
        self.pushButton_4.setMessage(
            "[positive integer]\n"
            "One epoch is when an entire dataset is passed forward and backward through the neural network only once.")
        self.pushButton_4.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.gridLayout_5.addWidget(self.pushButton_4, 4, 0, 1, 1)

        self.QPushButton_reduce_radius_after = InfoButton(self.widget_param)
        self.QPushButton_reduce_radius_after.setMessage(
            "[positive integer]\n"
            "Every specified number of epochs learning_radius parameter will be reduced by 1."
        )
        self.QPushButton_reduce_radius_after.setMaximumSize(QtCore.QSize(30, 16777215))
        self.QPushButton_reduce_radius_after.setObjectName(_fromUtf8("QPushButton_reduce_radius_after"))
        self.gridLayout_5.addWidget(self.QPushButton_reduce_radius_after, 9, 0, 1, 1)

        self.QPushButton_reduce_std_after = InfoButton(self.widget_param)
        self.QPushButton_reduce_std_after.setMessage(
            "[positive integer]\n"
            "Defines reduction rate at which parameter std will be reduced using the following formula:\n"
            "std = std / (1 + current_epoch / reduce_std_after)")
        self.QPushButton_reduce_std_after.setMaximumSize(QtCore.QSize(30, 16777215))
        self.QPushButton_reduce_std_after.setObjectName(_fromUtf8("QPushButton_reduce_std_after"))
        self.gridLayout_5.addWidget(self.QPushButton_reduce_std_after, 12, 0, 1, 1)

        self.label = QtGui.QLabel(self.widget_param)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_5.addWidget(self.label, 7, 3, 1, 1)
        self.label_2 = QtGui.QLabel(self.widget_param)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_5.addWidget(self.label_2, 9, 3, 1, 1)
        self.label_3 = QtGui.QLabel(self.widget_param)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_5.addWidget(self.label_3, 12, 3, 1, 1)
        self.lineEdit_std = QtGui.QLineEdit(self.widget_param)
        self.lineEdit_std.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_std.setObjectName(_fromUtf8("lineEdit_std"))
        self.gridLayout_5.addWidget(self.lineEdit_std, 11, 6, 1, 1)
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
        self.tableWidget = QtGui.QTableWidget(self.widget_table)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout_3.addWidget(self.tableWidget, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.widget_table, 0, 1, 1, 1)

        # default value for the lineEdit
        self.lineEdit_height.setText("30")
        self.lineEdit_width.setText("6")
        self.lineEdit_nepochs.setText("100")
        self.lineEdit_step.setText("0.1")
        self.lineEdit_reduce_step_after.setText("100")
        self.lineEdit_radius.setText("1")
        self.lineEdit_reduce_radius_after.setText("100")
        self.lineEdit_std.setText("1")
        self.lineEdit_reduce_std_after.setText("100")

        # button interaction
        self.pushButton_train.clicked.connect(self.train)
        self.pushButton_goback.clicked.connect(self.go_back)
        self.pushButton_show.clicked.connect(self.showmap)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_param.setText(_translate("Form", "Parameters", None))
        self.label_std.setText(_translate("Form", "Std", None))
        self.label_step.setText(_translate("Form", "Step", None))
        self.label_width.setText(_translate("Form", "Width", None))
        self.label_radius.setText(_translate("Form", "Radius", None))
        self.label_height.setText(_translate("Form", "Height", None))
        self.pushButton_5.setText(_translate("Form", "?", None))
        self.pushButton_7.setText(_translate("Form", "?", None))
        self.pushButton_3.setText(_translate("Form", "?", None))
        self.pushButton_6.setText(_translate("Form", "?", None))
        self.pushButton_2.setText(_translate("Form", "?", None))
        self.label_nbiter.setText(_translate("Form", "Epochs", None))
        self.QPushButton_reduce_step_after_button.setText(_translate("Form", "?", None))
        self.pushButton_4.setText(_translate("Form", "?", None))
        self.QPushButton_reduce_radius_after.setText(_translate("Form", "?", None))
        self.QPushButton_reduce_std_after.setText(_translate("Form", "?", None))
        self.label.setText(_translate("Form", "Reduce_step_after", None))
        self.label_2.setText(_translate("Form", "Reduce_radius_after", None))
        self.label_3.setText(_translate("Form", "Reduce_std_after", None))
        self.pushButton_train.setText(_translate("Form", "Train", None))
        self.pushButton_show.setText(_translate("Form", "Show", None))
        self.pushButton_goback.setText(_translate("Form", "Go back", None))
        self.label_data.setText(_translate("Form", "Data used for the Self Organizing Map ( SOM)", None))
