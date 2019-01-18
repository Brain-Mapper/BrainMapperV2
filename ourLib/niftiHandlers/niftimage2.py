import copy
import os
import numpy as np
import nibabel as nib
import warnings

class NifImage(object):
    """
    A custom structure for representing NifTI files in the application
    """

    def __init__(self, filename=None, nibabel_image=None):
        self.filename = filenam
        self.nib_image = nibabel_image

    @staticmethod
    def from_file(one_filename):
        """
        Create a new NifImage from file path
        Nibabel chooses automatically to create a Spatial Image of class NIfTI1 or NIfTI2

        Arguments :
            one_filename -- the path to the .nii file to store

        Return :
            a NifImage instance
        """
        return NiftImage(one_filename, nib.load(one_filename))

    def set_filename(self, new_filename):
        """Change the filename for save purposes
        
        Arguments:
            new_filename {[type]} -- [description]
        """

        self.filename = new_filename
    
    def get_affine_matrix(self):
        affine = self.nib_image.affine
        self.nib_image.uncache()
        return affine

    def get_header(self):
        header = self.nib_image.header
        self.nib_image.uncache()
        return header

    def get_img_class(self):
        img_class = self.nib_image.__class__
        self.nib_image.uncache()
        return img_class

    def get_nib_image(self):
        warnings.warn("Use NifImage.get_nib_image(self) with caution as it can be responsible of data leak", RuntimeWarning)
        return self.nib_image

    def uncache(self):
        self.nib_image.uncache()

    def save_to_file(self, folder_path):
        self.nib_image.to_filename(os.path.join(folder_path, self.filename))

    def get_name(self):
        return self.filename