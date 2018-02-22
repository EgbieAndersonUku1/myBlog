
from time import time as time_stamp
from PIL import Image
import os
from uuid import uuid4

_IMAGE_ID = uuid4().hex


class Imager(object):
    """The image class takes an image and from image generates different size images."""
    def __init__(self, file_name, folder_path, image_id=None):
        Imager._does_folder_path_exist(folder_path)
        self.file = file_name
        self.folder_path = folder_path
        self._image_id = image_id or _IMAGE_ID
        self._img = self._load_image()
        self._is_image_ext_correct(file_name)

    def _load_image(self):
        """Loads an image from a file"""

        try:
            return Image.open(self.file)
        except:
            raise Exception('File not found')

    def generate_thumbnails(self, ext="png"):
        """generate_thumbnails(str) -> return(str)

        Generates an image of various sizes. The sizes are extra small,
        small, medium, large and extra large.

        :parameter
            - ext : The file extension to _save the file as. The default file extension is png.
        """

        Imager._check_img_extension(ext)

        self._img = self._crop_from_center()
        file_path = self._create_file_path(self.folder_path, self._create_img_file_name('orig_image', ext))
        self._img._save(file_path)
        return self._gen_sizes(ext)

    @staticmethod
    def _check_img_extension(ext):
        """Check whether the image extension is correct"""
        Imager._is_image_ext_correct(ext)
        return Imager._fix_img_extension(ext)

    @staticmethod
    def _fix_img_extension(ext):
        """fixes the image extention if it is incorrect"""
        return ext if ext.startswith('.') else "." + ext

    def _crop_from_center(self):
        """Takes an image and crop it from the center"""
        dst_landscape = 1 > self._img.width / self._img.height
        wh = self._img.width if dst_landscape else self._img.height

        return self._img.crop((int((self._img.width - wh) / 2), int((self._img.height - wh) / 2), int(wh), int(wh)))

    @staticmethod
    def _create_file_path(folder_path, file_name):
        """Takes a folder path and a file name and creates a path to that file path"""
        return os.path.join(folder_path, file_name)

    def _create_img_file_name(self, size, file_ext):
        """Creates a file name for the image"""

        self._is_image_ext_correct(file_ext)
        return "{}_{}.{}".format(self._image_id, size, file_ext)

    @staticmethod
    def _is_image_ext_correct(ext):
        """"""
        file_ext = ['png', 'jpeg', 'jpg', 'gif']
        assert ext.split(".")[-1].lower() in file_ext, 'File format must be either PNG, JPEG, JPG or GIF'

    def _gen_sizes(self, ext):
        """Takes img extension and image object and generates five images of differents sizes"""

        img_sizes = {'xsmall': 50, 'small': 70, 'medium': 200, 'large': 400, 'xlarge': 600}

        for size_type in img_sizes:
            size = img_sizes.get(size_type)
            new_img = self._resize_img(width=size, height=size)
            img_path = Imager._create_file_path(self.folder_path, self._create_img_file_name(size_type, ext))
            new_img._save(img_path)
        return str(time_stamp())

    def _resize_img(self, width, height):
        """Takes a width and a height and resizes the image to those attributes.
           Returns and image object
        """
        return self._img.resize((int(width), int(height)))

    @staticmethod
    def _does_folder_path_exist(folder_path):
        """"""
        assert os.path.exists(folder_path), 'The folder path does not exist!'
