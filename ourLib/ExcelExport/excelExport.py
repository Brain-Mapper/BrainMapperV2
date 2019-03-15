# NAME
#        excelExport
#
# DESCRIPTION
#
#       The module 'excelExport.py' contains all the functions export the data to the CSV format.
#
#
# AUTHORS
#
#       Raphaël AGATHON - Maxime CLUCHLAGUE - Graziella HUSSON - Valentina ZELAYA
#       Marie ADLER - Aurélien BENOIT - Thomas GRASSELLINI - Lucie MARTIN

import os

from qtconsole.qt import QtGui


def export_control(name, path):
    """
    Verify that the path and the name of file to be exported are correct

    Arguments :
    :param name: file name
    :param path: path of the directory link to this file name
    """
    if name == '':
        QtGui.QMessageBox.critical(None,
                                   "Error",
                                   "Please enter a file name"
                                   )
        return False
    elif path == '':
        QtGui.QMessageBox.critical(
            None,
            "Error",
            "Please choose a directory"
        )
        return False
    else:
        if os.path.exists(path):
            csv_name = str(name) + '.csv'
            if csv_name in os.listdir(path):
                QtGui.QMessageBox.critical(
                    None,
                    "Error",
                    "A file with this name already exist in this directory"
                )
                return False
            else:
                return True
        else:
            QtGui.QMessageBox.critical(
                None,
                "Error",
                "Please enter a valid directory path"
            )
            return False


def export(name: str, path: str, a_usable_dataset, labels=None):
    """
    Export some data from an usable dataset
    
    Arguments:
        name {str} -- name of the file
        path {str} -- path to the folder where we put the file
        a_usable_dataset {} -- data to be extracted
        labels {list} -- list of labels
    """

    if export_control(name, path):
        file_path = os.path.join(str(path), str(name) + '.csv')

        with_labels = labels is not None

        header = [
            u'Origin_file_name',
            u'X',
            u'Y',
            u'Z',
            u'Intensity',
        ]

        if with_labels:
            header.append("Assigned cluster")
            row_cont = 0

        f = open(file_path, 'w')
        f.write(','.join(header) + "\n")

        for udcoll in a_usable_dataset.get_usable_data_list():

            extracted_data_dictionary = udcoll.get_extracted_data_dict()

            for origin_file in extracted_data_dictionary.keys():
                data_array = extracted_data_dictionary[origin_file]
                for data_rows in range(0, data_array.shape[0]):
                    elements_to_put_on_line = [os.path.split(str(origin_file.filename))[1],
                                               str(data_array[data_rows, 0]),
                                               str(data_array[data_rows, 1]),
                                               str(data_array[data_rows, 2]),
                                               str(data_array[data_rows, 3]),
                                               ]
                    # put the file name at the first place
                    # put the coordinates and the intensity

                    if with_labels:
                        elements_to_put_on_line.append(str(labels[row_cont]))
                        row_cont += 1

                    f.write(','.join(elements_to_put_on_line) + '\n')
        f.close()


"""
def export_from_clustering(name: str, path:str, clusterizable_data:List[tuple], labels: List[str]):

    if export_control(name, path):
        header = [HEADER]
        for point, label in zip(clusterizable_data, labels):
"""
