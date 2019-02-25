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

import numpy as np
import nibabel as nib
from os import path
from scipy import ndimage

from ourLib.dataExtraction.extractor import extract


# Take as argument the nifti's path file and load this one
def load_nifti(nifti_file):
    img = nib.load(nifti_file)
    return img


def get_data(img):
    data = np.array(img.get_data(), copy=True)
    return data


def max_value(list):
    max = list[0][3]
    for e in list:
        if int(e[3]) > max:
            max = int(e[3])
    return max


def min_value(list):
    min = list[0]
    for e in list:
        if e < min:
            min = e
    return min


def Extract_voxels_from_Nifti_file(data):
    """
    Extract from Nifti file, the list of voxels where intensity values are positives

    Arguments :
        data -- The matrix containing the nifti voxels data
lin
    Return :
        The list of voxels where intensity values are positives
    """
    mask = data > 0
    nb_interesting_voxels = len(data[mask].T)
    list_voxels = np.zeros(shape=(nb_interesting_voxels, 3))

    lx, ly, lz = data.shape
    c = 0
    for x in range(1, lx):
        if data[x].sum() > 0:
            for y in range(1, ly):
                if data[x][y].sum() > 0:
                    for z in range(1, lz):
                        if data[x][y][z] > 0:
                            list_voxels[c] = [int(x), int(y), int(z)]
                            c = c + 1
    return list_voxels.astype(int)


def max_shape(Nifti_collection):
    """
    Max shape beetween a collection of nifti file in each dimension

    Arguments :
        data -- Nifti collection

    Return :
        The max matrix shape
    """
    max_X = 0
    max_Y = 0
    max_Z = 0
    for file in Nifti_collection:
        # img = load_nifti(file)
        (x, y, z) = file.get_shape()
        if x > max_X:
            max_X = x
        if y > max_Y:
            max_Y = y
        if z > max_Z:
            max_Z = z
    return (max_X, max_Y, max_Z)


def save_nifti(data_nifti, filename):
    """
    Save the nifti image

    Arguments :
        data_nifti
        filename{string} -- file named
    """
    img = nib.Nifti1Image(data_nifti, np.eye(4))
    nib.save(img, filename)


def extract_name_without_path(list_nif_img):
    """
    Obtain names without a path

    Arguments :
        list_nif_img{list} -- list of images

    Return :
        list_name
    """
    list_name = ""
    for nifimage in list_nif_img:
        list_name = list_name + "\'" + nifimage.filename + "\' "
    return list_name


def addition_opperation(list_of_NifImage_obj):
    """
    Addition opperation between a list of Nifti Image Object

    Arguments :
        data -- List of Nifti Image Object

    Return :
        List with the one Nifti image object resulting from the Addition opperation
    """
    (lx, ly, lz) = max_shape(list_of_NifImage_obj)
    file_Nifti_clusterised = np.zeros(shape=(lx, ly, lz), dtype='f')
    for file in list_of_NifImage_obj:
        data = file.get_img_data()
        file_Nifti_clusterised = file_Nifti_clusterised + data
        file.uncache()
    output = "[Algorithm] > Addition\n[Input] > Nifti(s) file(s) : " + extract_name_without_path(
        list_of_NifImage_obj) + "\n[Arguments] > None\n[Output] > One Nifti file with dimensions : {" + str(
        lx) + ", " + str(ly) + ", " + str(lz) + "}"
    return ([file_Nifti_clusterised], output)

def multiplication_opperation(list_of_NifImage_obj,coefficent):
    """
    Multiplication opperation between a Nifti Image Object and a real factor

    Arguments :
        data -- Nifti Image object and a real number

    Return :
        Nifti Image Object resulting from the multiplication
    """
    (lx, ly, lz) = max_shape(list_of_NifImage_obj)
    file_Nifti_clusterised = np.zeros(shape=(lx, ly, lz), dtype='f')
    for file in list_of_NifImage_obj:
        data = file.get_img_data()
        file_Nifti_clusterised = file_Nifti_clusterised + data * coefficent
        file.uncache()
    output = "[Algorithm] > Multiplication\n[Input] > Nifti(s) file(s) : " + extract_name_without_path(
        list_of_NifImage_obj) + "\n[Arguments] > None\n[Output] > One Nifti file with dimensions : {" + str(
        lx) + ", " + str(ly) + ", " + str(lz) + "}"
    return ([file_Nifti_clusterised], output)

def division_opperation(list_of_NifImage_obj,coefficent):
    """
    Division opperation between a Nifti Image Object and a real factor

    Arguments :
        data -- Nifti Image object and a real number

    Rseturn :
        Nifti Image Object resulting from the division
    """
    (lx, ly, lz) = max_shape(list_of_NifImage_obj)
    file_Nifti_clusterised = np.zeros(shape=(lx, ly, lz), dtype='f')
    for file in list_of_NifImage_obj:
        data = file.get_img_data()
        file_Nifti_clusterised = file_Nifti_clusterised + data / coefficent
        file.uncache()
    output = "[Algorithm] > Division\n[Input] > Nifti(s) file(s) : " + extract_name_without_path(
        list_of_NifImage_obj) + "\n[Arguments] > None\n[Output] > One Nifti file with dimensions : {" + str(
        lx) + ", " + str(ly) + ", " + str(lz) + "}"
    return ([file_Nifti_clusterised], output)


def mean_opperation(list_of_NifImage_obj):
    """
    Mean opperation between a list of Nifti Image Object

    Arguments :
        data -- List of Nifti Image Object

    Return :
        List with the one Nifti image object resulting from the Mean opperation
    """
    (lx, ly, lz) = max_shape(list_of_NifImage_obj)
    file_Nifti_clusterised = np.zeros(shape=(lx, ly, lz), dtype='f')
    for file in list_of_NifImage_obj:
        data = file.get_copy_img_data()
        file_Nifti_clusterised = file_Nifti_clusterised + data
        file.uncache()
    file_Nifti_clusterised = file_Nifti_clusterised / len(list_of_NifImage_obj)
    output = "[Algorithm] > Mean\n[Input] > Nifti(s) file(s) : " + extract_name_without_path(
        list_of_NifImage_obj) + "\n[Arguments] > None\n[Output] > One Nifti file with dimensions : {" + str(
        lx) + ", " + str(ly) + ", " + str(lz) + "}"
    return ([file_Nifti_clusterised], output)


def erosion_opperation(list_of_NifImage_obj, argument):
    """
    Erosion opperation between a list of Nifti Image Object

    Arguments :
        data -- List of Nifti Image Object

    Return :
        List with the one Nifti image object resulting from the Erosion opperation
    """
    (lx, ly, lz) = max_shape(list_of_NifImage_obj)
    result = []
    for file in list_of_NifImage_obj:
        data = file.get_img_data()
        file_Nifti_clusterised = ndimage.binary_erosion(data, iterations=int(argument))
        result.append(file_Nifti_clusterised.astype(dtype='f'))
        file.uncache()
    output = "[Algorithm] > Erosion\n[Input] > Nifti(s) file(s) : " + extract_name_without_path(
        list_of_NifImage_obj) + "\n[Arguments] > Nb iteration = " + argument + "\n[Output] > One Nifti file with dimensions : {" + str(
        lx) + ", " + str(ly) + ", " + str(lz) + "}"
    return (result, output)


def dilation_opperation(list_of_NifImage_obj, argument):
    """
    Dilatation opperation between a list of Nifti Image Object

    Arguments :
        data -- List of Nifti Image Object

    Return :
        List with the one Nifti image object resulting from the Dilatation opperation
    """
    (lx, ly, lz) = max_shape(list_of_NifImage_obj)
    result = []
    for file in list_of_NifImage_obj:
        file_Nifti_clusterised = np.zeros(shape=(lx, ly, lz), dtype='f')
        data = file.get_img_data()
        file_Nifti_clusterised = ndimage.binary_dilation(data, iterations=int(argument))
        result.append(file_Nifti_clusterised.astype(dtype='f'))
        file.uncache()
    output = "[Algorithm] > Dilation\n[Input] > Nifti(s) file(s) : " + extract_name_without_path(
        list_of_NifImage_obj) + "\n[Arguments] > Nb iteration = " + argument + "\n[Output] > One Nifti file with dimensions : {" + str(
        lx) + ", " + str(ly) + ", " + str(lz) + "}"
    return (result, output)


def opening_opperation(list_of_NifImage_obj, argument):
    """
    Opening opperation between a list of Nifti Image Object

    Arguments :
        data -- List of Nifti Image Object

    Return :
        List with the one Nifti image object resulting from the Opening opperation
    """
    (lx, ly, lz) = max_shape(list_of_NifImage_obj)
    result = []
    for file in list_of_NifImage_obj:
        file_Nifti_clusterised = np.zeros(shape=(lx, ly, lz), dtype='f')
        data = file.get_img_data()
        file_Nifti_clusterised = ndimage.binary_opening(data, iterations=int(argument))
        result.append(file_Nifti_clusterised.astype(dtype='f'))
        file.uncache()
    output = "[Algorithm] > Opening\n[Input] > Nifti(s) file(s) : " + extract_name_without_path(
        list_of_NifImage_obj) + "\n[Arguments] > Nb iteration = " + argument + "\n[Output] > One Nifti file with dimensions : {" + str(
        lx) + ", " + str(ly) + ", " + str(lz) + "}"
    return (result, output)


def closing_opperation(list_of_NifImage_obj, argument):
    """
    Closing opperation between a list of Nifti Image Object

    Arguments :
        data -- List of Nifti Image Object

    Return :
        List with the one Nifti image object resulting from the Closing opperation
    """
    (lx, ly, lz) = max_shape(list_of_NifImage_obj)
    result = []
    for file in list_of_NifImage_obj:
        file_Nifti_clusterised = np.zeros(shape=(lx, ly, lz), dtype='f')
        data = file.get_img_data()
        file_Nifti_clusterised = ndimage.binary_closing(data, iterations=int(argument))
        result.append(file_Nifti_clusterised.astype(dtype='f'))
        file.uncache()
    output = "[Algorithm] > Closing\n[Input] > Nifti(s) file(s) : " + extract_name_without_path(
        list_of_NifImage_obj) + "\n[Arguments] > Nb iteration = " + argument + "\n[Output] > One Nifti file with dimensions : {" + str(
        lx) + ", " + str(ly) + ", " + str(lz) + "}"
    return (result, output)


def or_opperation(list_of_NifImage_obj):
    """
    Or opperation between a list of Nifti Image Object

    Arguments :
        data -- List of Nifti Image Object

    Return :
        List with the one Nifti image object resulting from the Or opperation
    """
    (lx, ly, lz) = max_shape(list_of_NifImage_obj)
    file_Nifti_clusterised = np.zeros(shape=(lx, ly, lz), dtype='f')
    for file in list_of_NifImage_obj:
        list_voxels = extract(file)
        # data = file.get_copy_img_data()
        for voxels in list_voxels:
            x = int(voxels[0])
            y = int(voxels[1])
            z = int(voxels[2])
            file_Nifti_clusterised[x][y][z] = 1
    output = "[Algorithm] > Boolean Union\n[Input] > Nifti(s) file(s) : " + extract_name_without_path(
        list_of_NifImage_obj) + "\n[Arguments] > None\n[Output] > One Nifti file with dimensions : {" + str(
        lx) + ", " + str(ly) + ", " + str(lz) + "}"
    return ([file_Nifti_clusterised], output)


def and_opperation(list_of_NifImage_obj):
    """
    And opperation between a list of Nifti Image Object

    Arguments :
        data -- List of Nifti Image Object

    Return :
        List with the one Nifti image object resulting from the And opperation
    """
    (lx, ly, lz) = max_shape(list_of_NifImage_obj)
    file_Nifti_clusterised = np.zeros(shape=(lx, ly, lz), dtype='f')
    list_pix = []
    for file in list_of_NifImage_obj:
        list_voxels = extract(file)
        for voxels in list_voxels:
            x = int(voxels[0])
            y = int(voxels[1])
            z = int(voxels[2])
            if not list_pix.__contains__([x, y, z]):
                list_pix.append([x, y, z])
            file_Nifti_clusterised[x][y][z] = file_Nifti_clusterised[x][y][z] + 1
    for e in list_pix:
        if file_Nifti_clusterised[e[0]][e[1]][e[2]] < len(list_of_NifImage_obj):
            file_Nifti_clusterised[e[0]][e[1]][e[2]] = 0
        else:
            file_Nifti_clusterised[e[0]][e[1]][e[2]] = 1
    output = "[Algorithm] > Boolean Intersection\n[Input] > Nifti(s) file(s) : " + extract_name_without_path(
        list_of_NifImage_obj) + "\n[Arguments] > None\n[Output] > One Nifti file with dimensions : {" + str(
        lx) + ", " + str(ly) + ", " + str(lz) + "}"
    return ([file_Nifti_clusterised], output)


def mask_opperation(Nifti_file_collection):
    (lx, ly, lz) = max_shape(Nifti_file_collection)
    file_Nifti_clusterised = np.zeros(shape=(lx, ly, lz), dtype='f')
    mask_file = Nifti_file_collection[0]
    data_file = Nifti_file_collection[1]
    list_voxels = extract(mask)
    data = data_file.get_img_data()
    mask = mask_file.get_img_data()
    for voxels in list_voxels:
        x = voxels[0]
        y = voxels[1]
        z = voxels[2]
        if data[int(x)][int(y)][int(z)] != 0:
            file_Nifti_clusterised[int(x)][int(y)][int(z)] = data[int(x)][int(y)][int(z)]
    mask_file.uncache()
    data_file.uncache()
    output = "[Algorithm] > Mask\n[Input] > Mask and file: " + extract_name_without_path(
        Nifti_file_collection) + "\n[Arguments] > None\n[Output] > One Nifti file with dimensions : {" + str(lx) + ", " + str(
        ly) + ", " + str(lz) + "}"
    return ([file_Nifti_clusterised], output)


def linear_combination_opperation(Nifti_file_collection, coef):
    (lx, ly, lz) = max_shape(Nifti_file_collection)
    file_Nifti_clusterised = np.zeros(shape=(lx, ly, lz), dtype='f')
    i = 0
    for file in Nifti_file_collection:
        data = file.get_img_data()
        list_voxels = extract(file)
        for voxels in list_voxels:
            x = voxels[0]
            y = voxels[1]
            z = voxels[2]
            file_Nifti_clusterised[int(x)][int(y)][int(z)] = file_Nifti_clusterised[int(x)][int(y)][int(z)] + data[int(x)][int(y)][int(z)] * int(coef[i])
        i = i + 1
        file.uncache()
    output = "[Algorithm] > Linear combination\n[Input] > Nifti(s) file(s) : " + extract_name_without_path(
        Nifti_file_collection) + "\n[Arguments] > None\n[Output] > One Nifti file with dimensions : {" + str(
        lx) + ", " + str(ly) + ", " + str(lz) + "}"
    return ([file_Nifti_clusterised], output)


def normalization_opperation(Nifti_file_collection):
    """
    Normalization opperation between a list of Nifti Image Object

    Arguments :
        data -- List of Nifti Image Object

    Return :
        List with the Nifti image object resulting from the Normalization opperation
    """
    (lx, ly, lz) = max_shape(Nifti_file_collection)
    file_Nifti_clusterised = np.zeros(shape=(lx, ly, lz), dtype='f')
    result = []
    for file in Nifti_file_collection:
        list_voxels = extract(file)
        max = float(max_value(list_voxels))
        # data = file.get_copy_img_data()
        for voxels in list_voxels:
            x = int(voxels[0])
            y = int(voxels[1])
            z = int(voxels[2])
            intensity = float(voxels[3])
            file_Nifti_clusterised[x][y][z] = intensity / max
        result.append(file_Nifti_clusterised)
    output = "[Algorithm] > Normalization\n[Input] > Nifti(s) file(s) : " + extract_name_without_path(
        Nifti_file_collection) + "\n[Arguments] > None\n[Output] > One Nifti file for each input file"
    return (result, output)


# Extract volume of voxel's center of gravity from a nifti file
def baricentre_opperation(Nifti_file_collection, arguments):
    """
    Barycentre opperation between a list of Nifti Image Object

    Arguments :
        data -- List of Nifti Image Object
    """
    def baricentre_calculation_opperation(NiftiName, list_voxels):
        mean_x = 0
        mean_y = 0
        mean_z = 0
        for e in list_voxels:
            mean_x = mean_x + e[0]
            mean_y = mean_y + e[1]
            mean_z = mean_z + e[2]
        mean_x = mean_x / len(list_voxels)
        mean_y = mean_y / len(list_voxels)
        mean_z = mean_z / len(list_voxels)
        output = "File \'" + NiftiName + "\' | Centroid (x:" + str(mean_x) + ", y:" + str(mean_y) + " ,z:" + str(
            mean_z) + ")"
        return (output)

    output = "[Algorithm] > Centroid[Input] > Nifti(s) file(s)\n[Arguments] > None\n[Output] > \n"
    (lx, ly, lz) = max_shape(Nifti_file_collection)
    for file in Nifti_file_collection:
        list_voxels = extract(file)
        # (x, name) = path.split(file)
        output = output + baricentre_calculation_opperation(file.filename, list_voxels) + "\n"

    return None, output


# ------------------------ Valentina's calculations functions using project structures ------------------------------

def image_centroid(a_nifti_image):
    """
    Calculate the mean voxel ([x,y,z,intensity]) of a single image if this image

    Arguments :
        a_nifti_image -- A NifImage object (our custom representation of a NIfTI image

    Return :
        a 1x4 array containing an array
    """
    # TODO check if we need to calculate the centroid if the nifti_image is a CSV file
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

    # Saves memory !
    del extracted

    return centroid


# ----------------------------------------------------------------------------------------------


def entropie_opperation(Nifti_file_collection):
    """
    Entropie opperation between a list of Nifti Image Object

    Arguments :
        data -- List of Nifti Image Object

    Return :
        None
    """
    def entropie(data, list_voxels, nbPixTot):
        symbol = []
        occurForEachSymbol = []
        for e in list_voxels:
            if symbol.__contains__(data[int(e[0])][int(e[1])][int(e[2])]):
                indice = symbol.index(data[int(e[0])][int(e[1])][int(e[2])])
                occurForEachSymbol[indice] = occurForEachSymbol[indice] + 1
            else:
                symbol.append(data[int(e[0])][int(e[1])][int(e[2])])
                occurForEachSymbol.append(0)
        numberOfOccur = sum(occurForEachSymbol)
        entropie = 0
        for i in occurForEachSymbol:
            Pi = float(i) / float(nbPixTot)
            entropie = entropie - Pi * np.log2(Pi)
        proba0 = float(nbPixTot - numberOfOccur) / float(nbPixTot)
        entropie = entropie - proba0 * np.log2(proba0)
        return entropie

    (lx, ly, lz) = max_shape(Nifti_file_collection)
    output = "[Algorithm] > Entropy\n[Input] > Nifti(s) file(s) : " + extract_name_without_path(
        Nifti_file_collection) + "\n[Arguments] > None\n[Output] >\n"
    for file in Nifti_file_collection:
        data = file.get_copy_img_data()
        list_voxels = extract(file)
        output = output + "File \'" + file.filename + "\' | Entropy = " + str(
            entropie(data, list_voxels, lx * ly * lz)) + "\n"
        file.uncache()
    return None, output


def threshold_opperation(Nifti_file_collection, arguments):
    """
    Threshold opperation between a list of Nifti Image Object

    Arguments :
        data -- List of Nifti Image Object

    Return :
        List with the Nifti image object resulting from the Threshold opperation
    """
    result = []
    min = arguments[0]
    max = arguments[1]
    for file in Nifti_file_collection:

        file_Nifti_clusterised = np.zeros(file.nib_image.shape, dtype='f')
        list_voxels = extract(file)
        for voxels in list_voxels:
            x = int(voxels[0])
            y = int(voxels[1])
            z = int(voxels[2])
            intensity = voxels[3]
            if (intensity < min or intensity > max):
                file_Nifti_clusterised[x][y][z] = 0
            else:
                file_Nifti_clusterised[x][y][z] = intensity
        result.append(file_Nifti_clusterised)
    output = "[Algorithm] > Normalization\n[Input] > Nifti(s) file(s) : " + extract_name_without_path(
        Nifti_file_collection) + "\n[Arguments] > None\n[Output] > One Nifti file for each input file"
    return (result, output)
