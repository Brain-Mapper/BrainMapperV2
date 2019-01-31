# NAME
#        set
#
# DESCRIPTION
#
#       'set' contains methods and the class 'Set' that represent a collection of 'ImageCollection' and a collection
#       of 'Set'
#       It will allow us to store image data and other information as in-memory representations
#       of the users' NIfTI files
#
# AUTHORS
#
#       Raphaël AGATHON - Maxime CLUCHLAGUE - Graziella HUSSON - Valentina ZELAYA
#       Marie ADLER - Aurélien BENOIT - Thomas GRASSELLINI - Lucie MARTIN

# Lib dependency imports
from ourLib.filesHandlers.imagecollection import ImageCollection
from ourLib.filesHandlers.nifimage import NifImage
import os


class Set(object):
    """ A custom structure to contain several image collections """

    def __init__(self, name, position):
        """
        Constructor of the Set Class.

        Arguments :
            name{string} -- name of the Set.


        The Set contains two dictionary. The Goal of this representation is to make a folder/file like.
        subset_dict is a dictionary of Set, like list of folders.
        collection_dict is a dictionary of ImageCollection, like list of files.
        For the dictionaries, keys are the name the object linked.
        """
        self.name = name
        self.subset_dict = dict()
        self.collection_dict = dict()
        self.parent = None
        self.position = position

    def add_empty_subset(self, name):
        """
        Method to create a empty subset into the Set.
        Control if the name doesn't exist in subset_dict.

        Arguments :
            name{string} -- name of the new subset.
        """
        if name not in self.subset_dict.keys():
            p = self.number_of_subset()
            self.subset_dict[name] = Set(name,p)
            print("t")
            self.subset_dict[name].setParent(self)
            print("t1")
            return self.subset_dict[name]
        else:
            print('The Subset name : %s already exist' % name)
            return Null

    def add_empty_collection(self, name, set_name):
        """
        Method to create a empty image collection into the Set.
        control if the name doesn't exist in collection_dict.

        Arguments :
            name{string} -- name of the new ImageCollection
            set_name{string} -- name of the set_name
        """
        if name not in self.collection_dict.keys():
            self.collection_dict[name] = ImageCollection(name, set_name)
        else:
            print('The Image Collection name : %s already exist' % name)

    def add_subset(self, subset):
        """
        Method to add an existing Set.
        control if the subset name doesn't exist in subset_dict.

        Arguments :
            subset -- objet from the Set Class.
        """
        if subset.get_name not in self.subset_dict.keys():
            self.subset_dict[subset.get_name()] = subset
        else:
            print('The Subset name : %s already exist' % subset.get_name)

    def add_collection(self, collection):
        """
        Method to add an existing ImageCollection.
        control if the collection name doesn't exist in collection_dict.

        Arguments :
            collection -- object from the ImageCollection Class.
        """
        if collection.get_name() not in self.collection_dict.keys():
            self.collection_dict[collection.get_name()] = collection
        else:
            print('The Image Collection name : %s already exist' % collection.get_name)

    def batch_add_subset(self, subsets_array):
        """
        Method to add several Set at the same time using the add_subset method.

        Arguments :
            subsets_array -- array of Set to add into subset_dict.
        """
        for subset in subsets_array:
            self.add_subset(subset)

    def batch_add_collection(self, collection_array):
        """
        Method to add several ImageColection at the same time using the add_collection method.

        Arguments :
            collection_array -- array of ImageColletion to add into collection_dict.
        """
        for collection in collection_array:
            self.add_collection(collection)

    def remove_subset(self, name):
        """
        Method to remove a subset from subset_dict.

        Arguments :
            name{string} -- name set to remove.
        """
        del self.subset_dict[name]

    def remove_collection(self, name):
        """
        Method to remove a collection from collection_dict.

        Arguments :
            name{string} -- Set of the set to remove.
        """
        del self.collection_dict[name]

    def batch_remove_subset(self,subsets_array):
        """
        Method to remove several subset using remove subset_method.

        Arguments :
            subsets_array -- array of Set to remove from subset_dict.
        """
        for subset in subsets_array:
            self.remove_subset(subset)

    def batch_remove_collection(self,collection_array):
        """
        Method to remove several subset using remove collection_method.

        Arguments :
            collection_array -- array of ImageCollection to remove from collection_dict.
        """
        for collection in collection_array:
            self.remove_collection(collection)

    def get_name(self):
        """
        Getter for the name parameter.

        Return :
            name
        """
        return self.name

    def get_all_nifti_set(self):
        """
        Function to make a list of all the nifti image from collection-dict.

        Return :
            list of all the niftiImage of the Set. Don't take the nifti image of the subset.
        """
        all_collection = list()
        for collection in self.collection_dict.values():
            all_collection.append(collection)
        return all_collection

    def get_all_nifti_set_and_subset(self):
        """
        Function to make a list of all the nifti image of the Set.

        Return :
            list of all the nifti image of the Set and all its subset.
        """
        all_collection = self.get_all_nifti_set()
        for subset in self.subset_dict.values():
            all_collection.extend(subset.get_all_nifti_set_and_subset())
        return all_collection

    def number_of_subset(self):
        """
        Function to have the number of subset.

        Return :
            the number of subset.
        """
        return len(self.subset_dict.keys())

    def number_of_collection(self):
        """
        Function to have the number of collection.

        Return :
            the number of collection.
        """
        return len(self.collection_dict.keys())

    # TODO remove all the hidden file
    @classmethod
    def generate_from_folder(cls, set,  folder_path):
        """
        Method to build the all structure from a folder.

        Arguments :
            folder_path{string} -- folder witch contains the needed data.
        """
        list = os.listdir(folder_path)
        for item in list:
            if item != '.DS_Store':
                item_path = os.path.join(folder_path, item)
                if os.path.isdir(item_path):
                    item_list = os.listdir(item_path)
                    # case for the set
                    n = 0
                    for sub_item in item_list:
                        n = n + os.path.isfile(os.path.join(item_path, sub_item))
                    # 1 because whe have one hidden file
                    if n == 1:
                        set.add_empty_subset(item)
                        set.generate_from_folder(set.subset_dict[item], item_path)
                    # case for the imageCollection
                    elif n == len(item_list):
                        set.add_empty_collection(item)
                        for sub_item in item_list:
                            if sub_item != '.DS_Store':
                                set.collection_dict[item].add(NifImage.from_file(os.path.join(item_path, sub_item)))

    def set_name(self,name):
        self.name = name

    def get_sub_set(self,name):
        for i in self.subset_dict.values():
            if(i.name == name):
                return i
        return None

    def get_coll(self):
        return self.collection_dict

    def renameCollinSet(self, coll, name):
        collecs = self.collection_dict
        for i in collecs.values():
            if(i == coll):
                self.remove_collection(i.name)
                new_col = coll.set_name(name)
                self.add_collection(coll)

    def setParent(self, parent):
        self.parent = parent

    def getParentName(self):
        return self.parent.get_name()

    def getParent(self):
        return self.parent

    def getAllSubSets(self):
        return self.subset_dict.values()

    def get_all_subsets_subsubsets(self):

        def recursive_scan_of_subsets(subset_list, a_set):

            if len(a_set.subset_dict.values()) == 0:
                return subset_list
            else:
                for subset in a_set.subset_dict.values():
                    subset_list.append(subset)

                for subset in a_set.subset_dict.values():
                    return recursive_scan_of_subsets(subset_list, subset)

        return recursive_scan_of_subsets([], self)

    def getPosition(self):
        p = []
        p.append(self.position)
        parent = self.parent
        while parent!= None:
            print(parent.name)
            p.append(parent.position)
            parent = parent.parent
        p.append(0)
        p.reverse()
        print(p)
        return p
