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

from scipy import ndimage

from ourLib.dataExtraction.extractor import extract
from ourLib.filesHandlers.image import Image, CSVImage
from ourLib.filesHandlers.nifimage import NifImage
import numpy as np
import nibabel

# Size of an image in MNI format
X_MNI = 197
Y_MNI = 233
Z_MNI = 189
SHAPE_MNI = (X_MNI, Y_MNI, Z_MNI)
# Affine of a nibabel object in MNI format
MNI_AFFINE = np.array([
    [1.0, 0.0, 0.0, -98.0],
    [0.0, 1.0, 0.0, -134.0],
    [0.0, 0.0, 1.0, -72.0],
    [0.0, 0.0, 0.0, 1.0],
])


# TODO maybe add the support for np.matrix ?

def convert_from_mni_to_matrix(x, y, z):
    """
    Use it to pass from mni coordinates to matrix coordinates
    :param x: x in MNI coordinates
    :param y: y in MNI cordinates
    :param z: z in MNI coordinates
    :return: i,j,k in matrix coordinates
    """
    return x + 98, y + 134, z + 72


def create_mni_nibabel_image_from_matrix(data):
    """
    Create a nibabel image with an mni matrix from the result of an operation
    :param data: np.matrix of shape (197,233,189)
    :return: nibabel:nifti1:Nifti1Image
    """
    if data.shape != (X_MNI, Y_MNI, Z_MNI):
        warnings.warn("Shape of the data doesn't correspond to MNI standard", ValueError)
        return None
    return nibabel.nifti1.Nifti1Image(data, MNI_AFFINE)


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


def addition_operation(list_of_images, coefficient: float = 1):
    """
    Addition operation
    :param list_of_images: list of image, instances of classes Image or NifImage
    :param coefficient: each value is multiplied by this coefficient
    :return: one Image resulting of the addition operation
    """
    result_matrix = np.zeros(shape=max_shape(list_of_images), dtype='f')
    for img in list_of_images:
        if isinstance(img, NifImage):
            data = img.get_img_data()
            result_matrix = result_matrix + data * coefficient
            img.uncache()
        else:  # instance of Image
            for x, y, z, intensity in img.extract():
                i, j, k = convert_from_mni_to_matrix(x, y, z)
                result_matrix[i, j, k] = result_matrix[i, j, k] + intensity * coefficient
    return result_matrix


def multiplication_operation(list_of_images, coefficient: float):
    return addition_operation(list_of_images, coefficient)


def division_operation(list_of_images, coefficient: float):
    return addition_operation(list_of_images, 1 / coefficient)


def mean_operation(list_of_images):
    return addition_operation(list_of_images) / len(list_of_images)


def image_operation(list_of_images, iterations_number: int, operation):
    """
    :param list_of_images: list of image
    :param iterations_number: number of time the operation is effected
    :param operation: function to be executed on each nifti file
    :return: list of operated images
    """
    result = []
    for img in list_of_images:
        if isinstance(img, NifImage):
            data = img.get_img_data()
            eroded_img = operation(data, iterations=iterations_number)
            img.uncache()
        else:  # instance of Image
            data = np.zeros(SHAPE_MNI)
            for x, y, z, intensity in img.extract():
                i, j, k = convert_from_mni_to_matrix(x, y, z)
                data[i, j, k] = data[i, j, k] + intensity
            eroded_img = operation(data, iterations=iterations_number)
        result.append(eroded_img.astype(dtype='f'))
    return result


def erosion_operation(list_of_images, iterations_number):
    image_operation(list_of_images, iterations_number, ndimage.binary_erosion)


def dilation_operation(list_of_images, iterations_number):
    image_operation(list_of_images, iterations_number, ndimage.binary_dilation)


def opening_operation(list_of_images, iterations_number):
    image_operation(list_of_images, iterations_number, ndimage.binary_erosion)


def closing_operation(list_of_images, iterations_number):
    image_operation(list_of_images, iterations_number, ndimage.binary_closing)


def or_operation(list_of_images):
    """
    Or operation between images
    :param list_of_images
    :return: Resulting or matrix with 1 and 0
    """
    result_matrix = np.zeros(shape=max_shape(list_of_images), dtype='f')
    for img in list_of_images:
        for x, y, z, intensity in extract(img):
            i, j, k = convert_from_mni_to_matrix(x, y, z)
            result_matrix[i, j, k] = 1
    return result_matrix


def and_operation(list_of_images):
    result_matrix = np.zeros(shape=max_shape(list_of_images), dtype='f')
    non_zeros_voxels = set()
    for img in list_of_images:
        for x, y, z, intensity in extract(img):
            i, j, k = convert_from_mni_to_matrix(x, y, z)
            result_matrix[i, j, k] = result_matrix[i, j, k] + 1
            non_zeros_voxels.add((i, j, k))
    for i, j, k in non_zeros_voxels:
        result_matrix[i, j, k] = 0 if result_matrix[i, j, k] < len(list_of_images) else 0
    return result_matrix


# TODO mask operation ?

def linear_combination_operation(list_of_images, list_of_coef):
    result_matrix = np.zeros(shape=max_shape(list_of_images), dtype='f')
    for img, coefficient in zip(list_of_images, list_of_coef):
        if isinstance(img, NifImage):
            data = img.get_img_data()
            result_matrix = result_matrix + data * coefficient
            img.uncache()
        else:  # instance of Image
            for x, y, z, intensity in img.extract():
                i, j, k = convert_from_mni_to_matrix(x, y, z)
                result_matrix[i, j, k] = result_matrix[i, j, k] + intensity * coefficient
    return result_matrix


# TODO normalization ?

# TODO baricentre ?

def image_centroid(a_nifti_image):
    """
    Calculate the mean voxel ([x,y,z,intensity]) of a single image if this image

    Arguments :
        a_nifti_image -- A NifImage object (our custom representation of a NIfTI image

    Return :
        a 1x4 array containing an array
    """
    # Use extractor function to extract image data as a (nb_voxel_nonzero_intensity x 4) array
    # : array of [X,Y,Z, Intensity]
    extracted = extract(a_nifti_image)

    centroid = np.zeros(shape=(1, 4))

    centroid_x = 0
    centroid_y = 0
    centroid_z = 0
    centroid_intensity = 0

    count = 0

    for voxel in extracted:
        centroid_x = centroid_x + voxel[0]
        centroid_y = centroid_y + voxel[1]
        centroid_z = centroid_z + voxel[2]
        centroid_intensity = centroid_intensity + voxel[3]
        count = count + 1

    # Centroid - X,Y,Z, Intensity means
    centroid[0] = np.array([centroid_x / count, centroid_y / count, centroid_z / count, centroid_intensity / count])

    return centroid


# TODO entropy ?

def threshold_operation(list_of_images, threshold_min, threshold_max):
    result = []
    shape = max_shape(list_of_images)
    for img in list_of_images:
        if isinstance(img, NifImage):
            data = img.get_img_data()
            thresholded = [i if threshold_min <= i <= threshold_max else 0 for i in data.flat]
            thresholded = np.matrix(thresholded).reshape(img.get_shape())
            img.uncache()
        else:  # Image
            thresholded = np.zeros(shape, dtype='f')
            for x, y, z, intensity in img.extract():
                i, j, k = convert_from_mni_to_matrix(x, y, z)
                if threshold_min <= intensity <= threshold_max:
                    thresholded[i, j, k] = intensity
        result.append(thresholded)
    return result


if __name__ == "__main__":
    # Launch this test file from the
    # Test addition simple
    file1 = CSVImage("")
