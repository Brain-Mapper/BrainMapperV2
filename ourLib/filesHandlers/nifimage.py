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
        self.filename = filename
        self.nib_image = nibabel_image

    @classmethod
    def from_file(cls,one_filename):
        """
        Create a new NifImage from file path
        Nibabel chooses automatically to create a Spatial Image of class NIfTI1 or NIfTI2

        Arguments :
            one_filename -- the path to the .nii file to store

        Return :
            a NifImage instance
        """
        return cls(one_filename, nib.load(one_filename))

    def set_filename(self, new_filename):
        """Change the filename for save purposes
        
        Arguments:
            new_filename {[type]} -- [description]
        """
        self.filename = new_filename
    
    def get_affine_matrix(self):
        """
        Returns the affine matrix of the nifti image. Use it to put the coordinates in MNI coordinates.
        """

        return self.nib_image.affine

    def get_header(self):
        """
        Returns the header of the nifti image.
        """
        return self.nib_image.header

    def get_img_class(self):
        """
        Returns the class of the nifti image
        """
        return self.nib_image.__class__

    def get_img_data(self, nan_to_0=True):
        """
        Returns the data of the image. Use uncache after to free memory !
        """
        # warnings.warn("Use NifImage.get_nib_image(self) with caution as it can be responsible of data leak", RuntimeWarning)
        img_data = self.nib_image.get_fdata()
        if nan_to_0:
            infinite_values_mask = np.logical_not(np.isfinite(img_data))
            img_data[infinite_values_mask] = 0
        return img_data

    def uncache(self):
        """
        THis function free the memory usage of the image. Use it when you don't need the image data anymore.
        """
        # warnings.warn("You have freed some memory", RuntimeWarning)
        self.nib_image.uncache()

    def get_shape(self):
        """
        Returns the shape of image
        """
        return self.nib_image.shape

    def save_to_file(self, folder_path):
        """
        Save to file
        """
        self.nib_image.to_filename(os.path.join(folder_path, self.filename))

    def get_name(self):
        """
        Returns the path of the file
        """
        return self.filename