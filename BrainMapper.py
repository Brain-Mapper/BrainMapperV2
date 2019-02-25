# NAME
#        BrainMapper
#
# DESCRIPTION
#
#       The module 'BrainMapper' is the controller of our application : it links the user interface and the library
#       that handles NIfTIs
#
# AUTHORS
#
#       Raphaël AGATHON - Maxime CLUCHLAGUE - Graziella HUSSON - Valentina ZELAYA
#       Marie ADLER - Aurélien BENOIT - Thomas GRASSELLINI - Lucie MARTIN


from ourLib.filesHandlers.nifimage import NifImage
from ourLib.filesHandlers.imagecollection import ImageCollection
from ourLib.filesHandlers.set import Set

from ourLib.dataExtraction import extractor as xt
from ourLib.dataExtraction.usable_data import UsableDataSet as uds
from ourLib.dataExtraction.image_recreation import image_recreation
from ourLib import clustering
from ourLib import calculations2 as calcul
from ourLib.Import import excelImport as imp
import ourLib.filesHandlers.image as csvImage
from ourLib.Import import workspaceImport as ws

from sys import maxsize as MAX

import os
import platform
import time
import json

import pandas as pd

# --- global variables ---
current_collec = None  # The current collection shown in edit view
selected_images_collections = []  # All image collections selected by the user in main page (usefull for all views that use data)
toRM = []  # Contains all images to remove in edit view (can be used somewhere else)
currentUsableDataset = None

sets = []  # List of all sets (and sub sets) created (usefull to know if a name is already used)
globalSets = [[], [], []]
setToAdd = []
workspace_sets = []  # List of all sets (and sub sets) created by workspace import
clusteringsets = []  # List of sets created as a result for clustering, permit to remember wich one to create
calculsets = []  # List of sets created as a result for calculation, permit to remember wich one to create
currentSet = None  # The current set shown in main view
currentVizu = None  # The current collections shown in main view

collshow = []
list_img = []

# Dictionary of available clustering methods
app_clustering_available = {}
with open('ressources/clustering_data/clustering_algorithms_available.json', 'r') as fc:
    app_clustering_available = json.load(fc)

# Global variable for currently selected clustering method
currentClusteringMethod = None


def open_nifti(path):
    """
    Opens a NIfTI file from path

    Arguments :
        path{string} -- the file path

    Return:
        NifImage instance
    """
    image = NifImage.from_file(path)
    return image


def do_image_collection(files, set_import):
    """
    Create an image collection from a list of file paths

    Arguments :
        files{list} -- file paths

    Return :
        ImageCollection instance
    """

    coll = ImageCollection("default", set_import)
    # We want an unique name for each collection
    # To do so we use the object ID
    name = str(coll).split("0x")
    name = name[1]
    coll.set_name(name[:-1])

    for file in files:
        # For french language, encode to latin1 -> to be able to take files with special characters of french in their file path
        filename = file  # .toLatin1().data()
        image = open_nifti(filename)
        coll.add(image)
    add_coll(coll)  # We add the collection create to selected by default
    print(set_import)
    set_import.add_collection(coll)  # We add the collection created in the current set
    return coll


def add_coll(coll):
    pass
    """
    Add a collection to the selected collection list [global variable 'selected']

    Arguments :
        coll -- ImageCollection instance
    """


def rm_coll(coll):
    """
    Remove a collection from the selected collection list [global variable 'selected']

    Arguments :
        coll -- ImageCollection instance
    """
    found = False
    for i in selected_images_collections:
        if i.name == coll.name:
            found = True
    if found:
        selected_images_collections.remove(coll)


def get_selected():
    """
    Return the selected collections (useful for all views that use data)

    Return :
        global variable 'selected'
    """
    print("collshow", collshow)
    return collshow


def get_selected_images_number():
    """
    Get the number of selected images

    Return :
        img_num{int}
    """
    img_num = 0
    for imgc in collshow:
        img_num = img_num + imgc.get_image_total_num()
    return img_num


def extract_data_from_selected():
    """
    Extract the interesting data from the selected image collections using extractor's module functions.
    Put this data in the global variable 'currentUsableDataSet'
    Global var 'currentUsableDataset' is modified
    """
    global currentUsableDataset
    currentUsableDataset = xt.extract_from_collection_list(collshow)


def extract_data_as_centroids_from_selected():
    """
      Extract the interesting data from the selected image collections using extractor's module functions
      and only centroids as points from each file. (one centroid per file)
      Put this data in the global variable 'currentUsableDataSet'
      Global var 'currentUsableDataset' is modified
    """
    global currentUsableDataset
    currentUsableDataset = xt.extract_from_collection_list_using_centroids(collshow)


def get_current_usableDataset():
    """
    Retrieve the UsableDataSet instance obtained by extracting data before clustering

    Return:
        a UsableDataSet instance
    """
    return currentUsableDataset


CLUSTERING_METHODS = {
    'KMeans': clustering.perform_kmeans,
    'KMedoids': clustering.perform_kmedoids,
    'AgglomerativeClustering': clustering.perform_agglomerative_clustering,
    'DBSCAN': clustering.perform_DBSCAN,
    'FuzzyCMeans': clustering.perform_FuzzyCMeans,
}

SCORING_METHODS = {
    'Davies-Bouldin': (clustering.compute_db, MAX, lambda old, new: new < old),
    'Calinski-Harabasz': (clustering.compute_calinski_habaraz, 0, lambda old, new: new > old),
    'Mean silhouette': (clustering.compute_mean_silhouette, -1, lambda old, new: new > old),
    'Fuzzy partition coefficient': None,
}


def read_n(n_clusters):
    """
    Method to return the interval of clusters numbers to test

    Arguments :
        n_clusters{string} -- string of number of clusters
    """
    if '-' not in n_clusters:
        interval = [int(n_clusters), int(n_clusters)]
    else:
        interval = n_clusters.replace(' ', '')
        interval = interval.split('-')
        for i in range(len(interval)):
            interval[i] = int(interval[i])
    return interval


def run_clustering(selectedClusteringMethod, params_dict):
    """
    A function to run a type of clustering algorithm, triggered by run button from interface

    Arguments :
        selectedClusteringMethod{string} -- the name of the user selected clustering method
        params_dict -- a dictionnary containing all necessary parameters for clustering and values given by the user

    Return :
        a list of clustering labels (to which cluster does one individual belong to)
    """
    clusterizable_dataset = currentUsableDataset.export_as_clusterizable()
    if selectedClusteringMethod in CLUSTERING_METHODS.keys():

        result = CLUSTERING_METHODS[selectedClusteringMethod](params_dict, clusterizable_dataset)

        result["n"] = int(params_dict["n_clusters"]) if selectedClusteringMethod != "DBSCAN" else len(
            set(clustering.filter(clusterizable_dataset, result["labels"])[1]))
        result["clusterizable_dataset"] = clusterizable_dataset
        try:
            result["silhouette_score"] = clustering.compute_mean_silhouette(clusterizable_dataset,
                                                                        result["labels"])
        except ValueError:
            result["silhouette_score"] = None
        try:
            result["calinski_harabaz_score"] = clustering.compute_calinski_habaraz(clusterizable_dataset, result["labels"])
        except ValueError:
            result["calinski_harabaz_score"] = None
        try :
            result["davies_bouldin_score"] = clustering.compute_db(clusterizable_dataset, result["labels"])
        except ValueError:
            result["davies_bouldin_score"] = None
    else:
        print('clustering method not recognised')
        result = ['']

    return result


def clustering_validation_indexes(labels, centroids, cluster_num):
    """
    Calculate the mean silhouette, the calinski harabaz score and the davies bouldin score

    Arguments :
        labels{list} -- clustering label
        centroids{list} -- centroids points for each cluster
        cluster_num{int} -- number of clusters

    Return :
        validation_indexes{list}
    """
    clustering_datamatrix = currentUsableDataset.export_as_clusterizable()
    validation_indexes = []

    # Mean silhouette
    validation_indexes.append(clustering.compute_mean_silhouette(X=clustering_datamatrix, predicted_labels=labels))
    # Calinski-Habaraz index
    validation_indexes.append(clustering.compute_calinski_habaraz(X=clustering_datamatrix, predicted_labels=labels))
    # Davies-Bouldin index
    validation_indexes.append(clustering.compute_db(X=clustering_datamatrix, predicted_labels=labels))

    return validation_indexes


def compute_sample_silhouettes(labels):
    """
    Calculate the silhouette value for each point

    Arguments :
        labels{list} -- clustering label
    """
    clustering_datamatrix = currentUsableDataset.export_as_clusterizable()
    return clustering.compute_samples_silhouette(X=clustering_datamatrix, predicted_labels=labels)


# ------------------------ CLUSTERING FUNCTIONS END HERE ---------------------------------------------------------


# def run_calculation(algorithm, list_of_images, arguments):
#     """
#     Method to choose the operation
#
#     Arguments :
#         selectedAlgorithm -- operation selected
#         nifti_collection -- collection selected
#         arguments -- arguments for the operation
#
#     Return :
#         file_result
#         output
#     """
#     if algorithm == "addition":
#         file_result = calcul.addition_operation(list_of_images)
#     if algorithm == "and":
#         file_result, output = calcul.and_operation(list_of_images)
#     if algorithm == "or":
#         file_result, output = calcul.or_opperation(list_of_images)
#     if algorithm == "linear combination":
#         file_result, output = calcul.linear_combination_opperation(list_of_images, arguments)
#     if algorithm == "mean":
#         file_result, output = calcul.mean_opperation(list_of_images)
#     if algorithm == "erosion":
#         file_result, output = calcul.erosion_opperation(list_of_images, arguments)
#     if algorithm == "Dilation":
#         file_result, output = calcul.dilation_opperation(list_of_images, arguments)
#     if algorithm == "Opening":
#         file_result, output = calcul.opening_opperation(list_of_images, arguments)
#     if algorithm == "Closing":
#         file_result, output = calcul.closing_opperation(list_of_images, arguments)
#     if algorithm == "Threshold":
#         file_result, output = calcul.threshold_opperation(list_of_images, arguments[0], arguments[1])
#     if algorithm == "Multiplication":
#         file_result, output = calcul.multiplication_opperation(list_of_images, arguments)
#     if algorithm == "Division":
#         file_result, output = calcul.division_opperation(list_of_images, arguments)
#     return file_result

def get_selected_from_name(name):
    """
    Returns the selected collection named "name" in the selected image collections list

    Arguments :
        name{string} -- The collection that we look for (unique ID)

    Return :
        ImageCollection
    """
    for x in collshow:
        if (name == x.name):
            return x


def get_toRM():
    """
    Method to obtain the images to remove

    Return:
        list of images to remove (useful for edit view -> save changes)
    """
    return toRM


def add_toRM(im):
    """
    Add an image to remove in the list toRM (useful for all views that use data)

    Arguments:
        im -- NifImage instance
    """
    toRM.append(im)


def rm_toRM(im):
    """
    Remove an image to remove from the list toRM (useful for all views that use data)

    Arguements :
        im -- NifImage instance
    """
    toRM.remove(im)


def reset_toRM():
    """
    Reset the list toRM (usefull for all views that use data and allow the list to be used somewhere else)
    """
    del toRM[:]


def set_current_coll(coll):
    """
    Set the current collection [global variable] (usefull to show the collection selected in edit view)

    Arguments :
        coll -- ImageCollection instance
    """
    global current_collec
    current_collec = coll


def get_current_coll():
    """
    Get the current collection [global variable]

    Return:
        Global variable current_collec
    """
    global current_collec
    return current_collec


def set_current_coll_name(name):
    """
    Set the current collection's name (useful to rename the collection selected in edit view)

    Arguments :
        name{string} -- the new name of the collection
    """
    cur = get_current_coll()
    cur.set_name(name)


def exists_selected(name):
    """
    Returns True if the collection's name "name" is already used by an other one in selected collections list (global var 'selected')

    Arguments :
        name{string} -- The collections' name to be tested

    Return :
        Boolean
    """
    for i in selected_images_collections:
        if (i.name == name):
            return True
    return False


def exists_coll_in_sets(name):
    """
    Returns True if the collection's name "name" is already used in one of the sets we have

    Arguments :
        name{string} -- The collections' name

    Return :
        Boolean
    """
    sets = get_all_sets()
    for s in sets:
        collecs = s.get_coll()
        for i in collecs.values():
            if (i.name == name):
                return True
    return False


def add_image_coll(coll, files):
    """
    Add all images from a file paths list in a given collection

    Arguments :
        coll -- ImageCollection instance
        files{list} -- A list of file path's = Images to add
    """
    for file in files:
        coll.add_from_file(str(file))


def delete_current_coll():
    """
    Delete the current collection from its set and from the app
    """
    coll = get_current_coll()
    this_set = coll.getSetName()
    rm_coll(coll)
    reset_toRM()
    add_toRM(coll)  # We use toRM this time with a collection (toRM is rested just after used)
    set_current_coll(None)  # The current collection become None
    this_set.remove_collection(coll.name)
    print("selected", selected_images_collections)
    print("collshow", collshow)


def save_modifs():
    """
    Apply the changes the user made in the edit view (use toRM to know the images to remove from the current collection)
    """
    global current_collec
    for i in toRM:
        current_collec.remove(i.filename)
    reset_toRM()


def exists_set(name):
    """
    Return True if the set's name "name" is already used by another set

    Arguments :
        name{string} -- The tested set's name

    Return :
        Boolean
    """
    for i in sets:
        if (i.name == name):
            return True
    return False


def newSet(name, position):
    """
    Creates a new set a the name "name" and add it into the set list. Also change the current set with the new one

    Arguments :
        name{string} -- The new set's name

    Return :
        Set instance
    """
    global currentSet
    new_set = Set(name, position)
    sets.append(new_set)
    currentSet = new_set
    return new_set


def set_current_set(new_set):
    """
    Set the current set with new_set

    Arguments :
        new_set -- The set to which we have to set the current set
    """
    global currentSet
    currentSet = new_set


def creation_date(path_to_file):
    """
    Return the creation date for the file located at path_to_file

    Arguments :
        path_to_file{strig} -- file path

    Return :
        Date
    """
    filename, file_extension = os.path.splitext(path_to_file)
    if file_extension == ".csv":
        return time.time()
    else:
        if platform.system() == 'Windows':
            return os.path.getctime(path_to_file)
        else:
            stat = os.stat(path_to_file)
            try:
                return stat.st_birthtime
            except AttributeError:
                # We're probably on Linux.
                return stat.st_mtime


def add_set(my_set):
    """
    Add my_set to the sets list

    Arguments :
        my_set -- Set Instance to add
    """
    sets.append(my_set)


def rm_set(my_set):
    """
    Remove my_set from the sets list

    Arguments :
        my_set -- Set instance to remove
    """
    sets.remove(my_set)


def get_current_vizu():
    """
    Return the currentVisualisation (variable currentVizu)

    Return :
        currentVizu
    """
    global currentVizu
    return currentVizu


def set_current_vizu(collView):
    """
    Set the current vizu with the vizu collView

    Arguments :
        collView
    """
    global currentVizu
    currentVizu = collView


def get_current_set():
    """
    Return the current set [global var 'currentSet']
    """
    global currentSet
    return currentSet


def get_all_sets():
    """
    Return:
        Return all the sets that exists in the app [global var 'sets']
    """
    return sets


def getSetByName(name):
    """
    Return:
        the set that have the name 'name' in sets list. If it doesn't exist, return None
    """
    for i in sets:
        if i.get_name() == name:
            return i
    return None


def setColNameInSet(name):
    """
    Rename the current collection with the name "name". Even in its set and in selected

    Arguments :
        name{string} -- new name for collection
    """
    old = get_current_coll()

    this_set = old.getSetName()
    this_set.renameCollinSet(old, name)
    set_current_coll_name(name)
    cur_col = get_current_coll()
    add_coll(cur_col)


def set_selected_clustering_method(method_name):
    """
    Set the currently selected clustering method

    Arguments :
        method_name{string} -- the clustering method name
    """
    global currentClusteringMethod
    currentClusteringMethod = method_name


def get_selected_clustering_info():
    """
    Get the selected clustering method information from method dictionnary (loaded from json file)
    """
    if currentClusteringMethod is not None:
        return app_clustering_available[currentClusteringMethod]
    else:
        return None


def makeClusterResultSet(a_usable_dataset, label):
    """
    Make results from clustering as sets and image collections

    Arguments :
        a_usable_dataset -- The data of the set, a UsableDataSet instance
        label -- cluster label
    """
    new_set = uds.extract_set_images_by_cluster(a_usable_dataset, label,
                                                'ressources/template_mni/mni_icbm152_t1_tal_nlin_asym_09a.nii')
    add_set(new_set)
    clusteringsets.append(new_set)
    setToAdd.append([new_set, 2])


def getClusterResultSets():
    """
    Return :
        Global variable clustering sets, containing the clustering results as a set
    """
    return clusteringsets


def rmClusterResultSets(s):
    """
    Remove a set from clustering results set

    Arguments :
        s: The set to remove
    """
    clusteringsets.remove(s)


# ---- IMPORT ----


def simple_import(csv_file_path, template_mni_path, set_import):
    """
    Import a file

    Arguments :
        csv_file_path{string} -- path for the csv file
        template_mni_path{string} -- path for the mni file

    Return :
        coll -- the collection
    """
    # coll = imp.simple_import(csv_file_path, template_mni_path, currentSet)
    coll = csvImage.simple_import(csv_file_path, currentSet)
    add_coll(coll)
    set_import.add_collection(coll)
    return coll


def makePoints(clustering_usable_dataset, label):
    """
    Arguments :
        clustering_usable_dataset -- data
        label -- clustering label

    Return :
        extract points
    """
    return uds.extract_points(clustering_usable_dataset, label)


def makeCalculResultSet(res_set):
    """
    Method to make calculs on set
    """
    add_set(res_set)
    calculsets.append(res_set)
    setToAdd.append([res_set, 1])


def getCalculResultSets():
    """
    Return:
        Global variable calculation sets, containing the calculation results as a set
    """
    return calculsets


def rmCalculResultSets(s):
    """
    Remove a set from calculation results set

    Arguments :
        s: The set to remove
    """
    calculsets.remove(s)


def rmAllCalculResultSets():
    """
    Remove all sets from calculation results set
    """
    for i in getCalculResultSets():
        calculsets.remove(i)
    for i in getCalculResultSets():
        calculsets.remove(i)


def general_workspace_import(folder_path):
    """
    Recursively importation

    Arguments :
        folder_path{string} -- path
    """
    ws.recursive_import(folder_path, currentSet, 0)


def general_workspace_import_control(folder_path):
    """
    Control the importation

    Arguments :
        folder_path{string} -- path
    """
    sets_name = []
    for set in sets:
        sets_name.append(set.get_name())
    test = ws.recursive_import_control(folder_path, sets_name)
    return test


def general_workspace_save(folder_path):
    """
    General save of the workspace

    Arguments :
        folder_path{string} -- path
    """
    for set in sets:
        print("SET",set)
        if set.getParent() is None:
            recursive_workspace_save(folder_path, set)


def recursive_workspace_save(folder_path, usable_set):
    """
    Save recursively workspace

    Arguments :
        folder_path{string} -- path
        usable_set : set
    """
    name = usable_set.get_name()
    new_folder_set_path = os.path.join(folder_path, name)

    if not os.path.exists(new_folder_set_path):
        os.makedirs(new_folder_set_path)

    for key in usable_set.collection_dict.keys():
        collection_name = usable_set.collection_dict[key].get_name()
        new_folder_collection_path = os.path.join(new_folder_set_path, collection_name)

        if not os.path.exists(new_folder_collection_path):
            os.makedirs(new_folder_collection_path)

        image_recreation(new_folder_collection_path, usable_set.collection_dict[key])

    for key in usable_set.subset_dict.keys():
        recursive_workspace_save(new_folder_set_path, usable_set.subset_dict[key])


def add_workspace_set(my_set):
    """
    Add my_set to the workspace sets list

    Arguments :
        my_set -- Set Instance to add
    """
    workspace_sets.append(my_set)


def rm_all_workspace_set():
    """
    Remove all sets from the workspace sets list
    """
    global workspace_sets
    workspace_sets = []


def rm_workspace_set(my_set):
    """
    Remove all sets from the workspace sets list

    Arguments :
        my_set -- Set Instance to remove
    """
    global workspace_sets
    workspace_sets.remove(my_set)


def get_workspace_set():
    """
    Get the workspace set
    """
    return workspace_sets
