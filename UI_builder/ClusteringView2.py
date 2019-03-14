# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Clustering.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

from PyQt4.Qt import QFileDialog
from PyQt4.QtCore import Qt, QRect
# Imports for the plotting

import ourLib.ExcelExport.excelExport as ee
from clustering_components.clustering_paramspace import ParameterAndScriptStack
# View components' import
from clustering_components.clustering_results import ClusteringResultsPopUp
from clustering_components.clustering_topbar import *
from clustering_components.clustering_plot import get_color
import clustering_components.clustering_plot as clustering_plot
import BrainMapper
from typing import List

from copy import deepcopy

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
    def __init__(self, message, widget, layout):
        super(InfoButton, self).__init__(parent=widget)
        self.message = message
        self.clicked.connect(self.open)
        layout.addWidget(self)

    def open(self):
        method_dict = get_selected_clustering_info()
        QtGui.QMessageBox.information(self, "Information", self.message, "ok")


class QTableNumericWidgetItem(QtGui.QTableWidgetItem):
    """ Custom QTableWidgetItem to sort on the value of the input"""

    def __init__(self, value, *__args):
        super().__init__(str(value), *__args)
        self.value = value
        self.setFlags(self.flags() ^ Qt.ItemIsEditable)

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __ge__(self, other) -> bool:
        return self.value >= other.value


class ClusteringView2(QtGui.QWidget):
    showMain = pyqtSignal()

    def __init__(self):
        super(ClusteringView2, self).__init__()

        self.clust_chooser = None
        self.table_displayer = None

        self.results_popup = ClusteringResultsPopUp(':ressources/logo.png', ':ressources/app_icons_png/file-1.png')

        self.label: List[int] = None
        self.centroids: List[List[float]] = None
        self.belong = None
        self.columns_selected: List[str] = None
        self.number_of_points: int = None

        title_style = "QLabel { background-color : #ffcc33 ; color : black;  font-style : bold; font-size : 14px;}"

        self.setupUi(self)

    def fill_table(self, usable_dataset_instance):
        """
        Fills this custom table with the data of a UsableDataSet obtained after data extraction
        :param a_usable_dataset_instance: see UsableData for more details
        :return: Nothing"""

        self.tableWidget.setRowCount(usable_dataset_instance.get_row_num())

        self.number_of_points = 0

        for udcoll in BrainMapper.current_extracted_usable_data_list:

            extracted_data_dictionary = udcoll.get_extracted_data_dict()

            for origin_file in extracted_data_dictionary.keys():
                data_array = extracted_data_dictionary[origin_file]
                for data_rows in range(0, data_array.shape[0]):
                    self.tableWidget.setItem(self.number_of_points, 0,
                                             QtGui.QTableWidgetItem(udcoll.get_imgcoll_name()))
                    self.tableWidget.setItem(self.number_of_points, 1,
                                             QtGui.QTableWidgetItem(str(origin_file.filename)))
                    self.tableWidget.setItem(self.number_of_points, 2, QTableNumericWidgetItem(
                        data_array[data_rows, 0]))  # X coordinate at column 0
                    self.tableWidget.setItem(self.number_of_points, 3, QTableNumericWidgetItem(
                        data_array[data_rows, 1]))  # Y coordinate at column 1
                    self.tableWidget.setItem(self.number_of_points, 4, QTableNumericWidgetItem(
                        data_array[data_rows, 2]))  # Z coordinate at column 2
                    self.tableWidget.setItem(self.number_of_points, 5, QTableNumericWidgetItem(
                        data_array[data_rows, 3]))  # Intensity at column 3
                    self.tableWidget.setItem(self.number_of_points, 6, QtGui.QTableWidgetItem("None yet"))
                    self.number_of_points = self.number_of_points + 1

    def fill_clust_labels(self, assigned_labels_array, tableWidget):
        """
        Fill the 'Assigned cluster' column once we have the clustering labels result
        :param assigned_labels_array:
        :return:
        """
        colors = get_color(sorted(set(assigned_labels_array)), True)

        for row_count, label in enumerate(assigned_labels_array):
            item = QTableNumericWidgetItem(str(label))
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QtGui.QColor(colors[label][0], colors[label][1], colors[label][2], 150))
            tableWidget.setItem(row_count, 6, item)

    def update_details(self, clustering_method, user_values, centroids, validation_values, n_selected, n, scores,
                       type_score):
        self.info_panel.setText("")

        self.info_panel.insertPlainText(
            clustering_method + "\n-----------------------------------------------------------------------------\n")

        for param_name in user_values.keys():
            self.info_panel.insertPlainText(param_name + "\t\t\t " + str(user_values[param_name]) + "\n")

        self.info_panel.insertPlainText(f"columns selected  \t\t{self.columns_selected} \n")

        # Search of the number of cluster
        if clustering_method != "DBSCAN":
            if n_selected is not None:
                self.info_panel.insertPlainText(
                    "n_selected" + "\t\t\t" + str(n_selected) + " for " + type_score + " score " + "\n")
            self.info_panel.insertPlainText(
                "-----------------------------------------------------------------------------\n\n")
            range_of_cluster = read_n(n)
            length = range_of_cluster[1] - range_of_cluster[0] + 1
            if scores is not None:
                self.info_panel.insertPlainText(
                    "Different " + type_score + " scores for each value of clusters "
                                                "number\n"
                                                "-----------------------------------------------------------------------------\n")
                self.info_panel.insertPlainText("n \t\t scores \n\n")
                for n in range(length):
                    self.info_panel.insertPlainText(str(n + range_of_cluster[0]) + "\t\t" + str(scores[n]) + "\n\n")
                self.info_panel.insertPlainText(
                    "-----------------------------------------------------------------------------\n\n")
            # Centroids
            self.info_panel.insertPlainText(
                "Cluster centroids\n-----------------------------------------------------------------------------\n")
            count = 0
            if centroids is not None:
                for c in centroids:
                    self.info_panel.insertPlainText("Cluster " + str(count) + ": \t\t" + str(c) + "\n")
                    count = count + 1

            self.info_panel.insertPlainText(
                "-----------------------------------------------------------------------------\n\n")
        else:
            self.info_panel.insertPlainText(
                "-----------------------------------------------------------------------------\n\n")
            self.info_panel.insertPlainText(
                "If only noise has been found, the indexes are marked as None\n\n"
            )
        self.info_panel.insertPlainText(
            "Validation Indexes\n-----------------------------------------------------------------------------\n")

        self.info_panel.insertPlainText("Mean Silhouette : \t\t " + str(validation_values[0]) + "\n")
        self.info_panel.insertPlainText("This mean is between -1 and 1 and the best value is around 1." + "\n\n")
        self.info_panel.insertPlainText("Calinski-Habaraz score: \t " + str(validation_values[1]) + "\n\n")
        self.info_panel.insertPlainText("Davies-Bouldin index: \t\t " + str(validation_values[2]) + "\n\n")

    def clicked_table(self):
        ligne = self.tableResults.selectedIndexes()[0].row()
        i = int(self.tableResults.item(ligne, 0).text())
        self.fill_clust_labels(self.history_iterations[i].get("labels"), self.tableWidget)
        self.label = self.history_iterations[i].get("labels")
        self.centroids = self.history_iterations[i].get("centers")
        self.belong = self.history_iterations[i].get("belong")

        for k in range(self.tableResults.rowCount()):
            for j in range(self.tableResults.columnCount()):
                if k == ligne:
                    self.tableResults.item(k, j).setBackground(QtGui.QColor(168, 255, 250))
                elif int(self.tableResults.item(k, 0).text()) == self.the_best_iteration.get("iteration"):
                    self.tableResults.item(k, j).setBackground(QtGui.QColor(255, 250, 168))
                else:
                    self.tableResults.item(k, j).setBackground(QtGui.QColor(255, 255, 255))

    def createResultView(self, param_dict, selectedMethod):
        """ Create the result panel at the bottom of the application """
        # If there is only one iteration
        if "i_iter" not in param_dict.keys() or param_dict["i_iter"] == "1" and len(
                param_dict["n_clusters"].split("-")) == 1:
            for i in reversed(range(self.verticalLayout_result.count())):
                self.verticalLayout_result.itemAt(i).widget().setParent(None)
            self.info_panel = QtGui.QTextEdit()
            self.verticalLayout_result.addWidget(self.info_panel)
            self.update_details(selectedMethod, param_dict, self.centroids,
                                clustering_validation_indexes(self.label),
                                self.n_selected, self.n, self.scores, param_dict["score"])
        # If there is more than one iteration, the results are displayed under the form of a table
        else:
            for i in reversed(range(self.verticalLayout_result.count())):
                self.verticalLayout_result.itemAt(i).widget().setParent(None)
            self.tableResults = QtGui.QTableWidget(self.widget_result)
            self.tableResults.setObjectName(_fromUtf8("tableResults"))
            self.tableResults.setColumnCount(5)
            self.tableResults.setRowCount(1)
            item = QtGui.QTableWidgetItem()
            self.tableResults.setVerticalHeaderItem(0, item)
            self.tableResults.verticalHeaderItem(0).setText("")
            # Define the 5 columns
            self.tableResults.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem())
            self.tableResults.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem())
            self.tableResults.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem())
            self.tableResults.setHorizontalHeaderItem(3, QtGui.QTableWidgetItem())
            self.tableResults.setHorizontalHeaderItem(4, QtGui.QTableWidgetItem())
            self.tableResults.horizontalHeaderItem(0).setText("I_number")
            self.tableResults.horizontalHeaderItem(1).setText("Clusters")
            self.tableResults.horizontalHeaderItem(2).setText("Mean Silhouette")
            self.tableResults.horizontalHeaderItem(3).setText("Calinski-Habaraz")
            self.tableResults.horizontalHeaderItem(4).setText("Davies-Bouldin")

            if self.history_iterations[0]["fuzzy_partition_coefficient"] is not None:
                self.tableResults.setColumnCount(6)
                self.tableResults.setHorizontalHeaderItem(5, QtGui.QTableWidgetItem("Fuzzy partition coefficient"))

            self.tableResults.horizontalHeader().setCascadingSectionResizes(False)
            self.tableResults.horizontalHeader().setDefaultSectionSize(145)

            self.tableResults.setRowCount(len(self.history_iterations))
            # Add the items row by row
            for row_count, iteration in enumerate(self.history_iterations):
                item = QtGui.QTableWidgetItem()
                self.tableResults.setVerticalHeaderItem(row_count, item)
                self.tableResults.verticalHeaderItem(row_count).setText("")
                # Iteration number
                item = QTableNumericWidgetItem(row_count)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableResults.setItem(row_count, 0, item)
                # Number of clusters
                item = QTableNumericWidgetItem(iteration.get("clusters"))
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableResults.setItem(row_count, 1, item)
                # Silhouette score
                item = QTableNumericWidgetItem(iteration.get("silhouette_score"))
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableResults.setItem(row_count, 2, item)
                # Calinski_harabaz_score
                item = QTableNumericWidgetItem(iteration.get("calinski_harabaz_score"))
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableResults.setItem(row_count, 3, item)
                # Davies_bouldin_score
                item = QTableNumericWidgetItem(iteration.get("davies_bouldin_score"))
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableResults.setItem(row_count, 4, item)
                # Fuzzy partition score
                if self.history_iterations[0]["fuzzy_partition_coefficient"] is not None:
                    item = QTableNumericWidgetItem(iteration.get("fuzzy_partition_coefficient"))
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tableResults.setItem(row_count, 5, item)

            for j in range(self.tableResults.columnCount()):
                self.tableResults.item(self.the_best_iteration.get("iteration"), j).setBackground(
                    QtGui.QColor(255, 250, 168))
            self.tableResults.setSortingEnabled(True)
            self.tableResults.clicked.connect(self.clicked_table)
            # self.tableResults.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
            self.verticalLayout_result.addWidget(self.tableResults)

    def runSelectedClust(self, selectedMethod, param_dict):
        try:
            self.pushButton_show.setEnabled(False)
            self.pushButton_save.setEnabled(False)
            self.pushButton_export.setEnabled(False)
            self.comboBox_3.setEnabled(False)

            if param_dict is None:
                QtGui.QMessageBox.critical(self, "None algorithm chosen",
                                           f"Chose an algorithm")
                return

            self.columns_selected = []
            columns = self.tableWidget.selectedItems()
            rownumber = self.tableWidget.rowCount()
            columns_index = {
                2: "X",
                3: "Y",
                4: "Z",
            }
            if len(columns) != 0:
                for i in range(0, len(columns), rownumber):
                    if columns[i].column() in columns_index.keys():
                        self.columns_selected.append(columns_index[columns[i].column()])
                    else:
                        QtGui.QMessageBox.critical(self, "Wrong column chose",
                                                   f"The column {columns[i].column()} is invalid. You can "
                                                   f"only cluster the columns X, Y and Z"
                                                   )
                        return

            else:
                self.columns_selected = ['X', 'Y', 'Z']

            # print(f"selected_columns : {self.columns_selected}")
            self.pushButton_run.setText(f"Running on {self.columns_selected}")
            QtGui.qApp.processEvents()

            if selectedMethod == "DBSCAN":
                clustering_results = run_clustering(selectedMethod, param_dict, self.columns_selected)
                self.n_selected = "DBSCAN"
                param_dict["score"] = "DBSCAN"
                self.scores = []
            else:
                i_iter = int(param_dict["i_iter"])
                self.history_iterations = []

                self.the_best_iteration = {
                    "iteration": None,
                    "n_clusters": None,
                    "silhouette_score": None,
                    "calinski_harabaz_score": None,
                    "davies_bouldin_score": None,
                    "score": 100 if param_dict["score"] == "Davies-Bouldin" else 0,
                    "fpc": None,
                    "centers": None
                }

                self.scores = []

                range_of_cluster = read_n(param_dict["n_clusters"])

                if range_of_cluster[1] > self.number_of_points:
                    QtGui.QMessageBox.critical(self, "Number of clusters to high",
                                               f"You asked for {range_of_cluster[1]} clusters but there is only "
                                               f"{self.number_of_points}"
                                               f"points.")
                    return

                for n in range(range_of_cluster[0], range_of_cluster[1] + 1):
                    for i in range(i_iter):

                        self.pushButton_run.setText(f"Running n: {n}, i: {i}")
                        QtGui.qApp.processEvents()

                        self.history_iterations.append({})
                        index = len(self.history_iterations) - 1

                        copy_param_dict = deepcopy(param_dict)
                        copy_param_dict["n_clusters"] = n

                        clustering_results = run_clustering(selectedMethod, copy_param_dict, self.columns_selected)

                        if i_iter == 1 and range_of_cluster[0] == range_of_cluster[1] and n < len(
                                set(clustering_results["labels"])):
                            QtGui.QMessageBox.information(self, "Less clusters founded",
                                                          f"You asked for {n} clusters but the algorithm has stabilised at"
                                                          f"{len(set(clustering_results['labels']))}"
                                                          f"clusters.")

                        score_keys = {
                            "Mean silhouette": "silhouette_score",
                            "Calinski-Harabasz": "calinski_harabaz_score",
                            "Davies-Bouldin": "davies_bouldin_score",
                            "Fuzzy partition coefficient": "fpc",
                        }
                        score_methods = {
                            "Mean silhouette": lambda x, y: x > y,
                            "Calinski-Harabasz": lambda x, y: x > y,
                            "Davies-Bouldin": lambda x, y: x < y,
                            "Fuzzy partition coefficient": lambda x, y: x > y,
                        }
                        self.scores.append(clustering_results[score_keys[param_dict["score"]]])

                        if score_methods[param_dict["score"]](clustering_results[score_keys[param_dict["score"]]]
                                , self.the_best_iteration["score"]):
                            self.the_best_iteration["iteration"] = index
                            self.the_best_iteration["silhouette_score"] = clustering_results["silhouette_score"]
                            self.the_best_iteration["calinski_harabaz_score"] = clustering_results["calinski_harabaz_score"]
                            self.the_best_iteration["davies_bouldin_score"] = clustering_results["davies_bouldin_score"]
                            self.the_best_iteration["score"] = clustering_results[score_keys[param_dict["score"]]]
                            self.the_best_iteration["n_clusters"] = clustering_results["n"]
                            self.the_best_iteration["centers"] = clustering_results[
                                "centers"] if "centers" in clustering_results.keys() else None

                        # Add all the useful data in the history
                        self.history_iterations[index]["method_used"] = selectedMethod
                        self.history_iterations[index]["labels"] = clustering_results["labels"]
                        self.history_iterations[index]["data"] = clustering_results["clusterizable_dataset"]
                        self.history_iterations[index]["clusters"] = n
                        self.history_iterations[index]["centers"] = clustering_results[
                            "centers"] if "centers" in clustering_results.keys() else None

                        self.history_iterations[index]["silhouette_score"] = clustering_results["silhouette_score"]
                        self.history_iterations[index]["calinski_harabaz_score"] = clustering_results[
                            "calinski_harabaz_score"]
                        self.history_iterations[index]["davies_bouldin_score"] = clustering_results["davies_bouldin_score"]

                        # Fuzzy partition coefficient
                        if "fpc" in clustering_results.keys():
                            self.history_iterations[index]["fuzzy_partition_coefficient"] = clustering_results["fpc"]
                            self.history_iterations[index]["belong"] = clustering_results["belong"]
                        else:
                            self.history_iterations[index]["fuzzy_partition_coefficient"] = None

                self.n_selected = self.the_best_iteration["n_clusters"] if self.the_best_iteration[
                                                                               "n_clusters"] is not None else None

            # Update the params
            self.label = clustering_results["labels"]
            self.centroids = clustering_results["centers"] if "centers" in clustering_results.keys() else None

            self.n = param_dict["n_clusters"] if "n_clusters" in param_dict.keys() is not None else None

            # FuzzyCMeans
            if selectedMethod == 'FuzzyCMeans':
                self.belong = clustering_results["belong"]
            else:
                self.belong = None

            # HAC
            if selectedMethod == "AgglomerativeClustering":
                self.hac = clustering_results['hac']
                self.comboBox_3.model().item(3).setEnabled(True)
            else:
                self.hac = None
                self.comboBox_3.model().item(3).setEnabled(False)

            self.fill_clust_labels(self.label, self.tableWidget)

            validation_values = clustering_validation_indexes(self.label)

            self.update_details(selectedMethod, param_dict, self.centroids, validation_values, self.n_selected, self.n,
                                self.scores, param_dict["score"])
            self.pushButton_show.setEnabled(True)
            self.pushButton_save.setEnabled(True)
            self.pushButton_export.setEnabled(True)
            self.comboBox_3.setEnabled(True)

            self.createResultView(param_dict, selectedMethod)

        except ValueError:
            QtGui.QMessageBox.critical(self, "Error", "Error while clustering, verify that the parameters are corrects.")

        except UnboundLocalError:
            QtGui.QMessageBox.critical(self, "Error", "Error while clustering, verify that the parameters are corrects.")

        finally:
            self.pushButton_run.setText("Run")
            QtGui.qApp.processEvents()

    def export(self):
        if self.label is not None:
            (f_path, f_name) = os.path.split(str(QFileDialog.getSaveFileName(self, "Browse Directory")))
            ee.export(f_name, f_path, get_current_usableDataset(), self.label)
        else:
            QtGui.QMessageBox.information(self, "Run Clustering before", "No cluster affectation")

    def save(self):
        print("save -> self.label", self.label)
        if self.label is not None:
            makeClusterResultSet(get_current_usableDataset(), self.label)
            QtGui.QMessageBox.information(self, "Results saved!",
                                          "A set has been created in the clustering part at home page.")

        else:
            QtGui.QMessageBox.information(self, "Run Clustering before", "No cluster affectation")

    def go_back(self):
        for i in reversed(range(self.verticalLayout_result.count())):
            self.verticalLayout_result.itemAt(i).widget().setParent(None)
        self.info_panel = QtGui.QTextEdit()
        self.info_panel.setReadOnly(True)

        self.info_panel.setText("======= CLUSTERING VALIDATION INDEXES =======\n\n"
                                "No algorithm has been applied, no indexes were computed ...")

        self.verticalLayout_result.addWidget(self.info_panel)
        BrainMapper.current_extracted_clusterizable_data = None
        self.showMain.emit()

    def plot(self):
        type = self.comboBox_3.currentText()
        # print("plot -> type",type)
        if type == "Silhouette":
            clustering_plot.plot_silhouette(self.label, None)
        elif type == "3D view":
            if self.comboBox_methode.get_selected_method_name() == "FuzzyCMeans":
                clustering_plot.plot_3d_fuzzy(self.label, self.belong, centroids=self.centroids)
            else:
                clustering_plot.plot_3d_clusters(self.label, centroids=self.centroids)
        elif type == "Dendrogram":
            clustering_plot.plot_dendrogram(self.hac)
        elif type == "Cross sections":
            default = list(BrainMapper.current_extracted_clusterizable_data[0, 0:3])
            default = [str(int(i)) for i in default]
            default = ",".join(default)
            text, ok = QtGui.QInputDialog.getText(self, 'Choice of the coordinates',
                                                  'Enter the cross coordinates : x,y,z', text=default)
            c = list(map(int, text.split(',')))
            if len(c) != 3:
                QtGui.QMessageBox.warning(self, "Choice of the coordinates",
                                          "You must use the format x,y,z to enter the coordinates")
            else:
                clustering_plot.plot_cross_section(self.label, c)
        elif type == "Glass brain":
            clustering_plot.plot_glass_brain(self.label)

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1000, 650)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget_clustering = QtGui.QWidget(Form)
        self.widget_clustering.setMaximumSize(QtCore.QSize(400, 16777215))
        self.widget_clustering.setStyleSheet(
            _fromUtf8("QWidget#widget_clustering{background-color: rgb(255, 255, 255);}"))
        self.widget_clustering.setObjectName(_fromUtf8("widget_clustering"))
        self.verticalLayout_clustering = QtGui.QVBoxLayout(self.widget_clustering)
        self.verticalLayout_clustering.setContentsMargins(0, 0, 0, 9)
        self.verticalLayout_clustering.setObjectName(_fromUtf8("verticalLayout_clustering"))
        self.label_clustering = QtGui.QLabel(self.widget_clustering)
        self.label_clustering.setMinimumSize(QtCore.QSize(16777215, 30))
        self.label_clustering.setMaximumSize(QtCore.QSize(16777215, 80))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_clustering.setFont(font)
        self.label_clustering.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.label_clustering.setAlignment(QtCore.Qt.AlignCenter)
        self.label_clustering.setObjectName(_fromUtf8("label_clustering"))
        self.verticalLayout_clustering.addWidget(self.label_clustering)

        self.comboBox_methode = ClusteringChooser()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_methode.sizePolicy().hasHeightForWidth())
        self.comboBox_methode.setSizePolicy(sizePolicy)

        self.verticalLayout_clustering.addWidget(self.comboBox_methode)

        self.label_info = QtGui.QLabel(self.widget_clustering)
        self.label_info.setText("You have to select columns in the table to apply cluster on those columns")
        self.label_info.setWordWrap(True)
        self.verticalLayout_clustering.addWidget(self.label_info)

        self.widget_informations = QtGui.QWidget(self.widget_clustering)
        self.widget_informations.setObjectName(_fromUtf8("widget_informations"))
        self.verticalLayout_clustering.addWidget(self.widget_informations)
        title_style = "QLabel { background-color : #ffcc33 ; color : black;  font-style : bold; font-size : 14px;}"
        self.widget_parametres = ParameterAndScriptStack(title_style, self.comboBox_methode)

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.widget_parametres.setFont(font)
        self.widget_parametres.setStyleSheet(
            _fromUtf8("QWidget#widget_parametres{background-color: rgb(255, 255, 255);}"))
        self.widget_parametres.setObjectName(_fromUtf8("widget_parametres"))
        self.verticalLayout_clustering.addWidget(self.widget_parametres)
        self.horizontalLayout.addWidget(self.widget_clustering)
        self.verticalLayout_dataAndResult = QtGui.QVBoxLayout()
        self.verticalLayout_dataAndResult.setObjectName(_fromUtf8("verticalLayout_dataAndResult"))
        self.widget_tab = QtGui.QWidget(Form)
        self.widget_tab.setMinimumSize(QtCore.QSize(700, 200))
        self.widget_tab.setStyleSheet(_fromUtf8("QWidget#widget_tab{background-color: rgb(255, 255, 255);}"))
        self.widget_tab.setObjectName(_fromUtf8("widget_tab"))
        self.verticalLayout_tab = QtGui.QVBoxLayout(self.widget_tab)
        self.verticalLayout_tab.setContentsMargins(0, 0, 0, 9)
        self.verticalLayout_tab.setObjectName(_fromUtf8("verticalLayout_tab"))
        self.label_data = QtGui.QLabel(self.widget_tab)
        self.label_data.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_data.setFont(font)
        self.label_data.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.label_data.setAlignment(QtCore.Qt.AlignCenter)
        self.label_data.setObjectName(_fromUtf8("label_data"))
        self.verticalLayout_tab.addWidget(self.label_data)
        self.tableWidget = QtGui.QTableWidget(self.widget_tab)
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
        item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(8)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)

        # self.tableWidget.clicked.connect(self.addinclust)
        # self.tableWidget.horizontalHeaderItem(0).isSelected().connect(self.addinclust)
        # self.tableWidget.horizontalHeaderItem(0).clicked.connect(self.addinclust)

        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(6, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        # Select only the columns
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectColumns)
        self.verticalLayout_tab.addWidget(self.tableWidget)
        self.verticalLayout_dataAndResult.addWidget(self.widget_tab)
        self.widget_buttons = QtGui.QWidget(Form)
        self.widget_buttons.setMinimumSize(QtCore.QSize(0, 50))
        self.widget_buttons.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget_buttons.setObjectName(_fromUtf8("widget_buttons"))
        self.horizontalLayout_buttons = QtGui.QHBoxLayout(self.widget_buttons)
        self.horizontalLayout_buttons.setMargin(0)
        self.horizontalLayout_buttons.setObjectName(_fromUtf8("horizontalLayout_buttons"))
        self.pushButton_run = QtGui.QPushButton(self.widget_buttons)
        self.pushButton_run.setObjectName(_fromUtf8("pushButton_run"))

        self.pushButton_run.clicked.connect(
            lambda: self.runSelectedClust(self.comboBox_methode.get_selected_method_name(),
                                          self.widget_parametres.get_user_params()))
        self.horizontalLayout_buttons.addWidget(self.pushButton_run)

        self.comboBox_3 = QtGui.QComboBox(self.widget_buttons)
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.horizontalLayout_buttons.addWidget(self.comboBox_3)
        self.pushButton_show = QtGui.QPushButton(self.widget_buttons)
        self.pushButton_show.setObjectName(_fromUtf8("pushButton_show"))
        self.pushButton_show.clicked.connect(self.plot)
        self.horizontalLayout_buttons.addWidget(self.pushButton_show)
        self.pushButton_export = QtGui.QPushButton(self.widget_buttons)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.pushButton_export.clicked.connect(self.export)
        self.horizontalLayout_buttons.addWidget(self.pushButton_export)
        self.pushButton_save = QtGui.QPushButton(self.widget_buttons)
        self.pushButton_save.setObjectName(_fromUtf8("pushButton_save"))
        self.pushButton_save.clicked.connect(self.save)
        self.horizontalLayout_buttons.addWidget(self.pushButton_save)
        self.pushButton_back = QtGui.QPushButton(self.widget_buttons)
        self.pushButton_back.clicked.connect(self.go_back)
        self.pushButton_back.setObjectName(_fromUtf8("pushButton_back"))
        self.horizontalLayout_buttons.addWidget(self.pushButton_back)
        # InfoButton(get_selected_clustering_info()['algo_info'],self.widget_buttons,self.horizontalLayout_buttons)
        self.verticalLayout_dataAndResult.addWidget(self.widget_buttons)
        self.widget_result = QtGui.QWidget(Form)
        self.widget_result.setMinimumSize(QtCore.QSize(700, 0))
        self.widget_result.setMaximumSize(QtCore.QSize(16777215, 230))
        self.widget_result.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.widget_result.setObjectName(_fromUtf8("widget_result"))
        self.verticalLayout_result = QtGui.QVBoxLayout(self.widget_result)
        self.verticalLayout_result.setContentsMargins(0, 0, 0, 9)
        self.verticalLayout_result.setObjectName(_fromUtf8("verticalLayout_result"))
        self.label_result = QtGui.QLabel(self.widget_result)
        self.label_result.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_result.setFont(font)
        self.label_result.setStyleSheet(_fromUtf8("background-color: rgb(223, 223, 223);"))
        self.label_result.setAlignment(QtCore.Qt.AlignCenter)
        self.label_result.setObjectName(_fromUtf8("label_result"))
        self.verticalLayout_result.addWidget(self.label_result)
        self.widget_result_view = QtGui.QWidget(self.widget_result)
        self.widget_result_view.setObjectName(_fromUtf8("widget_result_view"))

        self.info_panel = QtGui.QTextEdit()
        self.info_panel.setReadOnly(True)

        self.info_panel.setText("======= CLUSTERING VALIDATION INDEXES =======\n\n"
                                "No algorithm has been applied, no indexes were computed ...")

        self.verticalLayout_result.addWidget(self.info_panel)

        self.verticalLayout_result.addWidget(self.widget_result_view)
        self.verticalLayout_dataAndResult.addWidget(self.widget_result)
        self.horizontalLayout.addLayout(self.verticalLayout_dataAndResult)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # self.tableWidget.cellPressed.connect(self.addinclust)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_clustering.setText(_translate("Form", "Clustering", None))

        self.label_data.setText(_translate("Form", "Data inside the collection", None))
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
        self.pushButton_run.setText(_translate("Form", "Run", None))
        self.pushButton_export.setText(_translate("Form", "Export", None))
        self.comboBox_3.setItemText(0, _translate("Form", "Silhouette", None))
        self.comboBox_3.setItemText(1, _translate("Form", "3D view", None))
        self.comboBox_3.setItemText(2, _translate("Form", "Cross sections", None))
        self.comboBox_3.setItemText(3, _translate("Form", "Dendrogram", None))
        self.comboBox_3.setItemText(4, _translate("Form", "Glass brain", None))
        self.pushButton_show.setText(_translate("Form", "Show", None))
        self.pushButton_save.setText(_translate("Form", "Save as set", None))
        self.pushButton_back.setText(_translate("Form", "Go back", None))
        self.label_result.setText(_translate("Form", "Result details", None))
