# NAME
#        calculations
#
# DESCRIPTION
#
#       The module 'calculations' contains methods for mathematical or preprocessing operations on
#       nifti image collections, sets or single files
#
# AUTHORS
#
#       Raphaël AGATHON - Maxime CLUCHLAGUE - Graziella HUSSON - Valentina ZELAYA
#       Marie ADLER - Aurélien BENOIT - Thomas GRASSELLINI - Lucie MARTIN
import warnings
from ourLib.filesHandlers.image import Image
from ourLib.filesHandlers.nifimage import NifImage
import numpy as np

X_MNI = 197
Y_MNI = 233
Z_MNI = 189


def max_shape(list_of_image):
    max_x = X_MNI
    max_y = Y_MNI
    max_z = Z_MNI
    for img in list_of_image:
        if isinstance(img, NifImage):
            (x, y, z) = img.get_shape()
            if (x, y, z) != (X_MNI, Y_MNI, Z_MNI):
                warnings.warn("File '" + img.filename + "' has not MNI coordinates", RuntimeWarning)
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            if z > max_z:
                max_z = z
    return max_x, max_y, max_z


def addition_opperation(list_of_image):
    """
    Addition opperation
    :param list_of_image: list of image Image or NifImage
    :return: one Image resulting of the addition operation
    """
    (lx, ly, lz) = max_shape(list_of_image)
    result_img = np.zeros(shape=(lx, ly, lz), dtype='f')
    for img in list_of_image:
        if isinstance(img, NifImage):
            data = img.get_img_data()
            result_img = result_img + data
            img.uncache()
        else:  # instance of Image
            data = img.extract()
            for x, y, z, intensity in data:
                result_img[x, y, z] = result_img[x, y, z] + intensity
    return {
        "img": result_img,
    }
