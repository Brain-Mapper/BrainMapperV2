import pandas as pd
from ..filesHandlers.imagecollection import ImageCollection
from abc import ABC, abstractmethod
from shutil import copy2
from typing import List, Set, Iterable
import tempfile


class Image(ABC):
    """
    A custom structure for representing images files in the application
    The file is only opened during the extract phase
    """
    filename: str
    columns: Set[str]

    def __init__(self, filename):
        # path of the file
        self.filename = filename

    def save(self, dest_path):
        """
        Copy the original file
        :param dest_path: where to put the copy
        """
        copy2(self.filename, dest_path)

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def get_dataframe(self):
        pass


class CSVImage(Image):
    def __init__(self, filename):
        super().__init__(filename)
        with open(self.filename) as buffer:
            self.columns = set(pd.read_csv(buffer, nrows=1).columns)

    def extract(self):
        with open(self.filename) as buffer:
            return pd.read_csv(buffer)[["X", "Y", "Z", "Intensity"]].dropna().values

    def get_dataframe(self):
        with open(self.filename) as buffer:
            return pd.read_csv(buffer).dropna()


class ExcelImage(Image):
    def __init__(self, filename):
        super().__init__(filename)
        self.columns = set(pd.read_excel(self.filename, nrows=1, encoding="sys.getfilesystemencoding()").columns)

    def extract(self):
        return pd.read_excel(self.filename, encoding="sys.getfilesystemencoding()")[
            ["X", "Y", "Z", "Intensity"]].dropna().values

    def get_dataframe(self):
        return pd.read_excel(self.filename, encoding="sys.getfilesystemencoding()").dropna()


class TempImage(Image):
    """ Image saved in a temporary file """

    def __init__(self, data: Iterable, labels: List[int] = None, prefix=None):
        f = tempfile.NamedTemporaryFile(prefix=prefix)
        super().__init__(f.name)
        self.file = f

        if labels is not None:
            self.columns = {"X", "Y", "Z", "Intensity", "Label"}
            self.file.write("X,Y,Z,Intensity,Label\n".encode())
            for row, label in zip(data, labels):
                self.file.write(
                    f"{','.join([str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(label)])}\n".encode())

        else:
            self.columns = {"X", "Y", "Z", "Intensity"}
            self.file.write("X,Y,Z,Intensity\n".encode())
            for row in data:
                self.file.write(f"{','.join([str(row[0]), str(row[1]), str(row[2]), str(row[3])])}\n".encode())

    def __del__(self):
        self.file.close()

    def extract(self):
        self.file.file.seek(0)
        return pd.read_csv(self.file)[["X", "Y", "Z", "Intensity"]].dropna().values

    def get_dataframe(self) -> pd.DataFrame:
        self.file.file.seek(0)
        return pd.read_csv(self.file).dropna()

    def save(self, dest_path):
        self.get_dataframe().to_csv(dest_path+".csv", index=False)


def simple_import(file_path, current_set):
    """
    Allow the user to import a file and return an Image
    Arguments:
        csv_file_path {[type]} -- path to the csv file, must not contains accents
        currentSet {[type]} -- [description]
    
    Returns:
        [Image]
    """
    extension = file_path.split(".")[-1].lower()

    if extension in ["xls", "xlsx"]:
        image = ExcelImage(file_path)
    elif extension in ["csv"]:
        image = CSVImage(file_path)

    coll = ImageCollection("default", current_set)
    coll.set_name(file_path.split("/")[-1])
    coll.add(image)
    return coll


def som_preparation(img_list: List[Image]) -> pd.DataFrame:
    """
    Prepare data for the SOMView
    :param img_list:
    :return:
    """
    # Obtain the columns that we can use on all the data
    columns = img_list[0].columns
    try:
        columns.remove("Intensity")
    finally:
        for img in img_list:
            columns = columns.intersection(img.columns)
        columns = list(columns)

        # Concatenate the data in one file
        selected: pd.DataFrame = pd.concat([img.get_dataframe()[columns] for img in img_list], ignore_index=True)

        # We don't want to obtains dummies on X,Y et Z
        columns.remove("X")
        columns.remove("Y")
        columns.remove("Z")

        # To correct input problem
        for column in columns:
            # some columns can be integer, so we have to use a try
            selected[column] = selected[column].astype(str).str.strip()


        return pd.get_dummies(selected, columns=columns, prefix_sep="=")
