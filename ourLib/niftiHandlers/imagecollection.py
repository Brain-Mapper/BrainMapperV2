# NAME
#
#        image-collection
#
# DESCRIPTION
#
#       'image-collection' contains methods and the class 'ImageCollection' that represent
# 		a -series of NIfTI 2 Images that were loaded by the user
# 		(often associated to one patient, but this is optional)
# 		and that allows to have a group of in-memory representations of NIfTI Images
#    	(see nif-image.py)
#
# AUTHORS
#
#       Raphaël AGATHON - Maxime CLUCHLAGUE - Graziella HUSSON - Valentina ZELAYA
#       Marie ADLER - Aurélien BENOIT - Thomas GRASSELLINI - Lucie MARTIN


# Lib dependency imports
from ourLib.niftiHandlers.nifimage import NifImage


class ImageCollection(object):
    """
    A custom structure to keep several NifImage objects and other relevant information
    """
    def __init__(self, name, set_n):
        # It's better to have a dictionary, to associate an ID (here, just a name)
        # and the NIfTI Image instance
        self.nifimage_dict = dict()
        self.name = name
        self.set_n = set_n

    def add(self, a_nif_image):
        """
        Method to add a nifimage to the dictionary

        Arguments :
            a_nif_image
        """
        self.nifimage_dict[a_nif_image.filename] = a_nif_image

    def remove(self, name):
        """
        Method to remove a nifimage from the dictionary

        Arguments :
            name{string} -- file name of the nifimage
        """
        del self.nifimage_dict[name]

    def add_from_file(self, filename):
        """
        Method to add a nifimage from a file name to the dictionary

        Arguments :
            filename{string} -- filename
        """
        self.nifimage_dict[filename] = NifImage.from_file(filename)

    def batch_add_from_files(self, filenames_array):
        for filename in filenames_array:
            self.add_from_file(filename)

    def batch_save_collection(self, output_folder):
        for nifImage in self.nifimage_dict.values():
            nifImage.save_to_file(output_folder)

    def get_name(self):
        return self.name

    def get_img_list(self):
        return self.nifimage_dict

    def get_image_total_num(self):
        return len(self.nifimage_dict)

    def set_name(self, new):
        self.name = new

    def getSetName(self):
        return self.set_n

    def imExists(self, name):
        for nifImage in self.nifimage_dict.values():
            if(nifImage.filename == name):
                return True
        return False
