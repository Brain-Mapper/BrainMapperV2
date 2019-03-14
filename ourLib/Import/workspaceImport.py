# NAME
#        workspaceImport
#
# DESCRIPTION
#
#       The module 'workspaceImport.py' contains all the functions import from workspace
#
#
# AUTHORS
#
#       Raphaël AGATHON - Maxime CLUCHLAGUE - Graziella HUSSON - Valentina ZELAYA
#       Marie ADLER - Aurélien BENOIT - Thomas GRASSELLINI - Lucie MARTIN

from ourLib.filesHandlers.nifimage import NifImage
from ourLib.filesHandlers.set import Set
import BrainMapper
import os
from ..filesHandlers import image


def recursive_import(folder_path, actual_set, depth, globalSets):
    name_folder = os.path.split(folder_path)[-1]
    print("name folder",folder_path)
    if actual_set.name=="Imported_Set":
        actual_set.name=name_folder
    list = os.listdir(folder_path)
    print("list",list)
    for item in list:
        print("item",item)
        if not item.startswith('.'):
            item_path = os.path.join(folder_path, item)
            print("item_path",item_path)
            if os.path.isdir(item_path):
                item_list = os.listdir(item_path)
                print("item_list",item_list)
                print("len item list",len(item_list))
                # case for the set
                n = 0
                hn = 0
                for sub_item in item_list:
                    n = n + os.path.isfile(os.path.join(item_path, sub_item))
                    if sub_item.startswith('.'):
                        print("cc")
                        hn = hn + 1
                print("n",n)
                print("hn",hn)
                # because whe have hn hidden file
                if n == hn:
                    # root place, no need to have parent
                    print("depth",depth)
                    if depth != 0:
                        print("here")
                        actual_set.add_empty_subset(item,[0])
                        #BrainMapper.add_workspace_set(actual_set.subset_dict[item])
                        BrainMapper.add_set(actual_set.subset_dict[item])
                        actual_set.subset_dict[item].setParent(actual_set)
                        recursive_import(item_path, actual_set.subset_dict[item], depth + 1,globalSets)
                    else:
                        print("or here")
                        new_set = Set(item,0,[0])
                        #BrainMapper.add_workspace_set(new_set)
                        actual_set.add_subset(new_set)
                        BrainMapper.add_set(new_set)
                        recursive_import(item_path, new_set, depth + 1,globalSets)
                # case for the imageCollection
                elif n == len(item_list):
                    actual_set.add_empty_collection(item, actual_set)
                    for sub_item in item_list:
                        if not sub_item.startswith('.'):
                            extension = '.'.join(sub_item.split('.')[1:])
                            print("NAME OF SET",actual_set.name)
                            print("SUBSET OF SET",actual_set.subset_dict)
                            print("COLL OF SET",actual_set.collection_dict)
                            if extension in ['nii','nii.gz']:
                                actual_set.collection_dict[item].add(NifImage.from_file(os.path.join(item_path, sub_item)))
                            else:
                                if extension in ["xls", "xlsx"]:
                                    actual_set.collection_dict[item].add(image.ExcelImage(os.path.join(item_path, sub_item)))
                                elif extension in ["csv"]:
                                    actual_set.collection_dict[item].add(image.CSVImage(os.path.join(item_path, sub_item)))


def recursive_import_control(folder_path, sets):
    list = os.listdir(folder_path)
    for item in list:
        if not item.startswith('.'):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                item_list = os.listdir(item_path)
                # case for the set
                n = 0
                hn = 0
                for sub_item in item_list:
                    n = n + os.path.isfile(os.path.join(item_path, sub_item))
                    if sub_item.startswith('.'):
                        hn = hn + 1
                # because whe have hn hidden file
                if n == hn:
                    if item in sets:

                        return "The Set " + item + " already exist."

                    sets.append(item)
                    recursive_import_control(item_path, sets)
                elif n < len(item_list):

                    return "The file " + item + " is outside of an imageCollection."
            else:
                return "The file " + item + " is outside of an imageCollection."
