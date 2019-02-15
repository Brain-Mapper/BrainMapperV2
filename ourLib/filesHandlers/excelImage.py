import pandas as pd
from ..filesHandlers.imagecollection import ImageCollection
from abc import ABC, abstractmethod


class Image(ABC):
    """
    A custom structure for representing Csv files in the application
    The file is only opened during the extract phase
    """

    def __init__(self, filename):
        self.filename = filename

    @abstractmethod
    def extract(self):
        pass


class CSVImage(Image):
    def __init__(self, filename):
        super().__init__(filename)
        with open(self.filename) as buffer:
            self.column = list(pd.read_csv(buffer, nrows=1).columns)

    def extract(self):
        with open(self.filename) as buffer:
            return pd.read_csv(buffer)[["X", "Y", "Z", "Intensity"]].dropna().values


class ExcelImage(Image):
    def __init__(self, filename):
        super().__init__(filename)
        self.column = list(pd.read_excel(self.filename, nrows=1, encoding="sys.getfilesystemencoding()").columns)

    def extract(self):
        return pd.read_excel(self.filename, encoding="sys.getfilesystemencoding()")[
            ["X", "Y", "Z", "Intensity"]].dropna().values


def simple_import(file_path, currentSet):
    """
    Allow the user to import a csv file inside
    Arguments:
        csv_file_path {[type]} -- path to the csv file, must not contains accents
        currentSet {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    # try:
    # the open is necessary for path with accents on windows
    # as pandas doesn't seem to be able to manage them
    # with open(file_path) as buffer:
    #     columns = list(pd.read_csv(buffer, nrows=1, encoding="latin-1").columns)
    # except:
    #     QtGui.QMessageBox.critical(None, "Error",
    #                                "The file cannot be opened : verify that the path to the file is python compatible")
    #     return None
    # else:
    #     # If we can read the file

    extension = file_path.split(".")[-1].lower()
    if extension in ["xls", "xlsx"]:
        image = ExcelImage(file_path)
    elif extension in ["csv"]:
        image = CSVImage(file_path)

    coll = ImageCollection("default", currentSet)
    coll.set_name(file_path.split("/")[-1])
    coll.add(image)
    return coll
