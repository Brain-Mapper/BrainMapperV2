# NAME
#        nif-image
#
# DESCRIPTION
#
#       'nif-image' contains methods and the class 'ImageCollection' that represent and allow to
#       open, create and save a single NIfTI file
#       It will allow us to have a folder representation of the NIfTI files
#
# AUTHORS
#
#       Raphaël AGATHON - Maxime CLUCHLAGUE - Graziella HUSSON - Valentina ZELAYA
#       Marie ADLER - Aurélien BENOIT - Thomas GRASSELLINI - Lucie MARTIN


# System imports
import copy
import os

# Lib dependency imports
import numpy as np
import nibabel as nib
#import nilearn.plotting as nilplot


class NifImage(object):
    """
    A custom structure for representing NIfTI files in the application (uses Nibabel library to access NIfTI files data)
    """
    # Declare class attributes

    # Initialize instance attributes with empty values because several constructors needed
    def __init__(self, filename=None, nibabel_image=None):
        # type: (str, object) -> NifImage
        self.filename = filename
        self.nib_image = nibabel_image

    @classmethod
    def from_file(cls, one_filename):
        """
        Create a new NifImage from file path
        Nibabel chooses automatically to create a Spatial Image of class NIfTI1 or NIfTI2

        Arguments :
            one_filename -- the path to the .nii file to store

        Return :
           a NifImage instance
        """
        return cls(one_filename, nib.load(one_filename))

    @classmethod
    def from_array(cls, new_filename, image_data_array, affine, nifti_format=1):
        """
        Create a new NifImage from a data array
        Default format is NIfTI1

        Arguments :
            new_filename -- the new image's filename (for future saving)
            image_data_array -- the new image's data
            affine -- the affine transformation matrix (real world -> MNI)
            nifti_format -- the NIfTI file format required (1 or 2, other values raise error)

        Return :
            a NifImage instance
        """
        if nifti_format == 2:
            nib_nifti_class = nib.Nifti2Image
        elif nifti_format == 1:
            nib_nifti_class = nib.Nifti1Image
        else:
            raise ValueError('nifti_format must be 1 or 2,  %s was given' % nifti_format)

        return cls(new_filename, nib_nifti_class(image_data_array, affine))

    @classmethod
    def like(cls, new_filename, ref_img, image_data_array, same_header=False):
        """
        Arguments :
            new_filename -- the new image's filename (for future saving)
            ref_img -- a NifImage instance that will serve as reference
            image_data_array -- the new image's data
            same_header -- TRUE if we must use the same header as the ref_img's, FALSE if not (default)

        Return:
            a new NifImage instance
        """
        affine = ref_img.get_affine_matrix()

        header = None
        if same_header:
            header = copy.deepcopy(ref_img.get_header)

        nib_nifti_class = ref_img.get_img_class()

        return cls(new_filename, nib_nifti_class(image_data_array, affine, header=header))

    def set_filename(self, new_filename):
        self.filename = new_filename

    # TODO L'utiliser pour se placer en MNI !
    def get_affine_matrix(self):
        """
        Return the NIfTI images' affine
        An affine is the matrix that allows to pass from real world coordinates to
        the image coordinates (here, to MNI coordinates)

        Return :
            array
        """
        return self.nib_image.affine

    def get_header(self):
        return self.nib_image.header

    def get_img_class(self):
        return self.nib_image.__class__

    def get_nib_image(self):
        return self.nib_image

    def get_copy_img_data(self, finite_values=False):
        """
        Get the image data safely by using copy.deepcopy() so that if we modify
        the data, it won't affect the original image

        Arguments :
            finite_values -- FALSE if NaN and inf values in data array must be kept,TRUE if NaN and inf are to be replaced by 0

        Return :
            array
        """
        #img_data = np.array(copy.deepcopy(self.nib_image.get_data()))
        img_data = np.array(copy.deepcopy(self.nib_image.get_fdata()))

        # Some nifti images have NaN and inf as data values...
        if finite_values:
            infinite_values_mask = np.logical_not(np.isfinite(img_data))
            img_data[infinite_values_mask] = 0

        return img_data

    def get_info(self):
        info = ""
        try:
            info = "Location : %s\nSpatial Image : %s\n(\n shape=%s,\n affine=%s\n)" % \
                   (selfparam .filename,
                    self.nib_image.__class__.__name__,
                    repr(self.nib_image.shape),
                    repr(self.nib_image.affine))
        except:
            pass
        return info

    def is_binary_image(self):
        return np.array_equal(self.nib_image.get_data(), self.get_copy_img_data().astype(bool))

    def save_to_file(self, folder_path):
        self.nib_image.to_filename(os.path.join(folder_path, self.filename))

    def get_name(self):
        return self.filename

    def get_img_data(self):
        # Used only for the visualisation process
        data = self.nib_image.get_data()
        data = np.transpose(data, [2,0,1])
        d2 = np.empty(data.shape + (4,), dtype=np.ubyte)
        d2[..., 0] = data * (255./(data.max()/1))
        d2[..., 1] = d2[..., 0]
        d2[..., 2] = d2[..., 0]
        d2[..., 3] = d2[..., 0]
        d2[..., 3] = (d2[..., 3].astype(float) / 255.)**2 * 255

        # RGB orientation lines (optional)
        d2[:, 0, 0] = [255, 0, 0, 255]
        d2[0, :, 0] = [0, 255, 0, 255]
        d2[0, 0, :] = [0, 0, 255, 255]
        return d2
