import pandas as pd
from ..filesHandlers.imagecollection import ImageCollection
from abc import ABC, abstractmethod
from shutil import copy2


class Image(ABC):
    """
    A custom structure for representing images files in the application
    The file is only opened during the extract phase
    """

    def __init__(self, filename):
        # path of the file
        self.filename = filename

    def save(self, dest_path):
        """
        Copy the original file
        :param dest_path: where to put the copy
        """
        copy2(self.filename, dest_path)

    def to_nifti_image(self):
        data_img = self.extract()


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
    extension = file_path.split(".")[-1].lower()

    if extension in ["xls", "xlsx"]:
        image = ExcelImage(file_path)
    elif extension in ["csv"]:
        image = CSVImage(file_path)

    coll = ImageCollection("default", currentSet)
    coll.set_name(file_path.split("/")[-1])
    coll.add(image)
    return coll
