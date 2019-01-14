# NAME
#        excelImport
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

import sys
import importlib

importlib.reload(sys)
#sys.setdefaultencoding('utf8') pas besoin ??
from nibabel import Nifti1Image,load
from numpy import zeros
import numpy as np
from csv import reader as csv_reader
import time
from ourLib.niftiHandlers.imagecollection import ImageCollection
from ourLib.niftiHandlers.nifimage import NifImage


def simple_import(csv_file_path, template_mni_path, currentSet):
    """
    Method to import imageColection from a excel file.
    For this :method we considere that :
        - generated nifti have the same shape than the MNI152 one.
        - generated nifti have the same affine than the MNI152 one.

    The generated nifti and the imageCollection are not save with this method. they are just laod.
    So nifimage object have their strict file name as file name

    :param csv_file_path: path of the csv file.
    :param template_shape:
    :param template_affine:
    :return: imageCollection
    """

    # For french language, encode to latin1 ->
    # to be able to take files with special characters of french in their file path
    # -- Tested this, works on GNULinux but not on Windows, so taken off --
    #filename = csv_file_path.toLatin1().data()
    filename = csv_file_path
    #file = open(filename, "rb")     #encoding='ISO-8859-1')
    file = open(filename, "r")

    simple_header = [
        u'File_Name_Nifti',
        u'Surgeon_ID',
        u'Patient_ID',
        u'Localisation',
        u'Point_Name',
        u'Type_Of_Answer',
        u'X',
        u'Y',
        u'Z',
        u'Intensity'
    ]

    clustering_header = [
        u'Image Coll ID',
        u'Origin filename',
        u'X',
        u'Y',
        u'Z',
        u'Intensity',
        u'Assigned cluster'
    ]

    try:
        reader = csv_reader(file)

        row = next(reader)

        template_data = load(template_mni_path)
        template_affine = template_data.affine
        #template_data.set_qform(template_affine, code='mni')
        template_shape = template_data.shape

        # part for a simple import
        if row == simple_header:
            print('Simple import')
            point_dict = dict()

            coll = ImageCollection("default", currentSet)
            # We want an unique name for each collection
            # To do so we use the object ID
            name = str(coll).split("0x")
            name = name[1]
            coll.set_name(name[:-1])

            for row in reader:
                point = [int(float(row[6])), int(float(row[7])), int(float(row[8])), int(float(row[9]))]
                # regroup all points of the same file in point_dict
                if row[0] in point_dict.keys():
                    point_dict[row[0]].append(point)
                else:
                    point_dict[row[0]] = []
                    point_dict[row[0]].append(point)

            # recreate nifti image from this points
            for key in point_dict.keys():
                recreate_affine = template_affine
                recreate_data = zeros(template_shape)

                for point in point_dict[key]:
                    x_y_z = mni_to_voxel(point, recreate_affine)
                    recreate_data[int(x_y_z[0]), int(x_y_z[1]), int(x_y_z[2])] = point[3]

                recreate_image = Nifti1Image(recreate_data, recreate_affine)
                ni_image = NifImage(str(key) + ".csv", recreate_image)

                # put nifti images into a imageCollection
                coll.add(ni_image)

        # pat for clustering import
        elif row == clustering_header:
            print('Clustering import')
            point_dict = dict()

            coll = ImageCollection("default", currentSet)
            # We want an unique name for each collection
            # To do so we use the object ID
            name = str(coll).split("0x")
            name = name[1]
            coll.set_name(name[:-1])

            for row in reader:
                point = [int(float(row[2])), int(float(row[3])), int(float(row[4])), int(float(row[5]))]
                # regroup all points of the same file
                if row[6] in point_dict.keys():
                    point_dict[row[6]].append(point)
                else:
                    point_dict[row[6]] = []
                    point_dict[row[6]].append(point)

                    # recreate nifti image from this points
                    for key in point_dict.keys():

                        recreate_affine = template_affine
                        recreate_data = zeros(template_shape)

                        for point in point_dict[key]:
                            x_y_z = mni_to_voxel(point, recreate_affine)
                            recreate_data[int(x_y_z[0]), int(x_y_z[1]), int(x_y_z[2])] = point[3]

                        recreate_image = Nifti1Image(recreate_data, recreate_affine)
                        #recreate_image = Nifti1Image(recreate_data)
                        ni_image = NifImage("Cluster_" + key + ".csv", recreate_image)

                        # put nifti images into a imageCollection
                        coll.add(ni_image)

        else:
            print('Please use a valid csv file')

    finally:

        file.close()
    return coll


def mni_to_voxel(points:list, affine) -> list:
    """
    data : [x,y,z]
    affine : affine matrix
    -> return [x_in_voxel, y_in_voxel, z_in_voxel]
    """
    deltas = affine[:3, 3]
    x_y_z = [points[0], points[1], points[2]]
    x_y_z = x_y_z - deltas
    return x_y_z

#
# def excel_import(excel_file_path, template_mni_path, currentSet):
#
#
#     # For french language, encode to latin1 ->
#     # to be able to take files with special characters of french in their file path
#     # -- Tested this, works on GNULinux but not on Windows, so taken off --
#     filename = csv_file_path.toLatin1().data()
#     file = open(filename, "rb")     #encoding='ISO-8859-1')
#
#     simple_header = [
#         u'File_Name_Nifti',
#         u'Surgeon_ID',
#         u'Patient_ID',
#         u'Localisation',
#         u'Point_Name',
#         u'Type_Of_Answer',
#         u'X',
#         u'Y',
#         u'Z',
#         u'Intensity'
#     ]
#
#     clustering_header = [
#         u'Image Coll ID',
#         u'Origin filename',
#         u'X',
#         u'Y',
#         u'Z',
#         u'Intensity',
#         u'Assigned cluster'
#     ]
#
#     try:
#         reader = csv_reader(file)
#
#         row = reader.next()
#         print(row)
#
#         # part for a simple import
#         if row == simple_header:
#             print('yes')
#             point_dict = dict()
#
#             template_data = load(template_mni_path)
#             template_affine = template_data.affine
#             template_shape = template_data.shape
#
#             coll = ImageCollection("default", currentSet)
#             # We want an unique name for each collection
#             # To do so we use the object ID
#             name = str(coll).split("0x")
#             name = name[1]
#             coll.set_name(name[:-1])
#
#             for row in reader:
#                 point = [int(float(row[6])), int(float(row[7])), int(float(row[8])), int(float(row[9]))]
#                 # regroup all points of the same file
#                 if row[0] in point_dict.keys():
#                     point_dict[row[0]].append(point)
#                 else:
#                     point_dict[row[0]] = []
#                     point_dict[row[0]].append(point)
#
#             # recreate nifti image from this points
#             for key in point_dict.keys():
#                 recreate_affine = template_affine
#                 recreate_data = zeros(template_shape)
#
#                 for point in point_dict[key]:
#                     recreate_data[point[0], point[1], point[2]] = point[3]
#
#                 recreate_image = Nifti1Image(recreate_data, recreate_affine)
#                 ni_image = NifImage(unicode(str(key)) + ".csv", recreate_image)
#
#                 # put nifti images into a imageCollection
#                 coll.add(ni_image)
#
#         # pat for clustering import
#         elif row == clustering_header:
#             print('yes')
#             point_dict = dict()
#
#             template_data = load(template_mni_path)
#             template_affine = template_data.affine
#             template_shape = template_data.shape
#
#             coll = ImageCollection("default", currentSet)
#             # We want an unique name for each collection
#             # To do so we use the object ID
#             name = str(coll).split("0x")
#             name = name[1]
#             coll.set_name(name[:-1])
#
#             for row in reader:
#                 point = [int(float(row[2])), int(float(row[3])), int(float(row[4])), int(float(row[5]))]
#                 # regroup all points of the same file
#                 if row[6] in point_dict.keys():
#                     point_dict[row[6]].append(point)
#                 else:
#                     point_dict[row[6]] = []
#                     point_dict[row[6]].append(point)
#
#                     # recreate nifti image from this points
#                     for key in point_dict.keys():
#
#                         recreate_affine = template_affine
#                         recreate_data = zeros(template_shape)
#
#                         for point in point_dict[key]:
#                             recreate_data[point[0], point[1], point[2]] = point[3]
#
#                         recreate_image = Nifti1Image(recreate_data, recreate_affine)
#                         ni_image = NifImage("Cluster_" + key + ".csv", recreate_image)
#
#                         # put nifti images into a imageCollection
#                         coll.add(ni_image)
#
#
#         else:
#             print('Please use a valid csv file')
#
#     finally:
#
#         file.close()
#     return coll
