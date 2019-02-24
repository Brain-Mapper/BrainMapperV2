import unittest
import ourLib.calculations2 as cal
import ourLib.filesHandlers.image as image
import ourLib.filesHandlers.nifimage as nifimage

import numpy as np


# file1 has 3 points
# X Y Z Intensity
# 0 0 0 1
# 0 0 1 1
# 0 0 2 1

# file2 has 3 points
# X Y Z Intensity
# 0 0 0 2
# 0 0 1 2
# 0 0 2 2

class MyTestCase(unittest.TestCase):
    def test_addition(self):
        file1 = image.CSVImage("../../test/test_calculation/file1.csv")
        file1_nifti = nifimage.NifImage.from_file("../../test/test_calculation/file1.nii")

        expected = np.zeros(shape=cal.SHAPE_MNI, dtype='f')
        x_0, y_0, z_0 = cal.convert_from_mni_to_matrix(0, 0, 0)
        expected[x_0, y_0, z_0] = 5
        expected[x_0, y_0, z_0 + 1] = 5
        expected[x_0, y_0, z_0 + 2] = 5
        assert (cal.addition_operation([file1, file1_nifti, file1, file1, file1_nifti]) == expected).all()

    # filet
    # X, Y, Z, Intensity
    # 0, 0, 0, 1
    # 0, 0, 1, 2
    # 0, 0, 2, 3
    # 0, 0, 3, 4
    # 0, 0, 4, 5
    # 0, 0, 5, 6

    def test_threshold(self):
        filet = image.CSVImage("../../test/test_calculation/filet.csv")

        expected = np.zeros(shape=cal.SHAPE_MNI, dtype='f')
        x_0, y_0, z_0 = cal.convert_from_mni_to_matrix(0, 0, 0)
        expected[x_0, y_0, z_0 + 1] = 2
        expected[x_0, y_0, z_0 + 2] = 3
        expected[x_0, y_0, z_0 + 3] = 4
        expected[x_0, y_0, z_0 + 4] = 5

        assert (cal.threshold_operation([filet], 2, 5)[0] == expected).all()


if __name__ == '__main__':
    unittest.main()
