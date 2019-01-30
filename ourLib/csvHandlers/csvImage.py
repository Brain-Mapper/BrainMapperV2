import pandas as pd
from ..niftiHandlers.imagecollection import ImageCollection
from PyQt4 import QtGui

class CsvImage(object):
    """
    A custom structure for representing Csv files in the application
    The file is only opened during the extract phase
    """

    def __init__(self, filename, columns=None):
        self.filename = filename
        self.columns = columns

    def extract(self):
        with open(self.filename) as buffer:
            return pd.read_csv(buffer)[["X","Y","Z","Intensity"]].dropna().values 
    

def simple_import(csv_file_path, currentSet):
    """
    Allow the user to import a csv file inside
    Arguments:
        csv_file_path {[type]} -- path to the csv file, must not contains accents
        currentSet {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    
    try:
        # the open is necessary for path with accents on windows
        # as pandas doesn't seem to be able to manage them
        with open(csv_file_path) as buffer: 
            columns = list(pd.read_csv(buffer, nrows=1, encoding='utf-8').columns)
    except:
        QtGui.QMessageBox.critical(None, "Error", "The file cannot be opened : verify that the path to the file is python compatible")
        return None
    else:
        # If we can read the file
        csv_image = CsvImage(csv_file_path, columns)
        coll = ImageCollection("default", currentSet)
        # We want an unique name for each collection
        # To do so we use the object ID
        coll.set_name(csv_file_path.split("/")[-1])
        coll.add(csv_image)
        return coll

        