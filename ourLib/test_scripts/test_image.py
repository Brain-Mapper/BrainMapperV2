import unittest
from ourLib.filesHandlers.image import CSVImage, ExcelImage, som_preparation

class MyTestCase(unittest.TestCase):
    def test_something(self):
        a = CSVImage("C:/Users/Aurélien/PycharmProjects/BrainMapperV2/test/test_image/file1.csv")
        b = CSVImage("C:/Users/Aurélien/PycharmProjects/BrainMapperV2/test/test_image/file2.csv")
        print(f"columns a : {a.columns}")
        print(f"columns b : {b.columns}")
        prepared = som_preparation([a, b])
        print(f"columns prepared : {prepared.columns}")
        assert (len(prepared) == len(a.get_dataframe()) + len(b.get_dataframe()))

if __name__ == '__main__':
    unittest.main()
