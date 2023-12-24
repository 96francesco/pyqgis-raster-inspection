import os
import re
import shutil
import qgis_utils

class ImageHandler:
      def __init__(self, image_folder, gt_folder, exclusion_folder, initial_index=0):
        self.image_folder = image_folder
        self.gt_folder = gt_folder
        self.exclusion_folder = exclusion_folder
        self.current_index = initial_index
        self.gt_files = sorted([f for f in os.listdir(self.gt_folder) if f.endswith('.tif')],
                               key=self._sort_key)

      @staticmethod
      def _sort_key(filename):
            """
            Extract the index as a number from the filename.

            Parameters:
            filename (str): the filename to extract the index from.

            Returns:
            int: the extracted index, or 0 if no number is found.
            """
            numbers = re.findall(r'\d+', filename)
            return int(numbers[0]) if numbers else 0

      def load_next_image(self):
            """
            Load the next image and its corresponding ground truth image based 
            on the current index.

            Returns:
            tuple: A tuple containing two elements:
                  - The filename of the next ground truth image (str) 
                  or None if no more images.
                  - The filename of the corresponding image (str) 
                  or None if no more images.
            """
            if self.current_index < len(self.gt_files):
                  self.current_index += 1
                  return self.gt_files[self.current_index - 1], self._get_image_name(self.gt_files[self.current_index - 1])
            else:
                  print("No more images to load.")
                  return None, None

      def mark_image(self):
            """
            Marks the current image and its corresponding ground truth image 
            for exclusion.
            The images are moved from their original folders to the exclusion 
            folder. The ground truth image is moved from the ground truth folder, 
            and the corresponding regular image is moved from the regular image folder.
            """
            if self.current_index <= len(self.gt_files):
                  gt_image_name = self.gt_files[self.current_index - 1]
                  corresponding_image_name = self._get_image_name(gt_image_name)

                  # remove current images from QGIS
                  qgis_utils.remove_layer_from_qgis(gt_image_name)
                  qgis_utils.remove_layer_from_qgis(corresponding_image_name)

                  self._exclude(gt_image_name, self.gt_folder)
                  self._exclude(corresponding_image_name, self.image_folder)

      @staticmethod
      def _get_image_name(gt_image_name):
            """
            Generates the name of the corresponding image from a ground truth 
            image name.
            This method removes the 'gt_' prefix from a ground truth image name 
            to derive the name of the corresponding regular image.

            Parameters:
            gt_image_name (str): The filename of the ground truth image.

            Returns:
            str: The filename of the corresponding regular image.
            """
            return gt_image_name.replace('gt_', '')

      def _exclude(self, image_name, folder_path):
            """
            Moves an image from its current folder to the exclusion folder.

            Parameters:
            image_name (str): The name of the image file to be moved.
            folder_path (str): The current folder path of the image.

            Note: If the image file does not exist in the specified folder 
            path, no action is taken.
            """
            image_path = os.path.join(folder_path, image_name)
            if os.path.exists(image_path):
                  shutil.move(image_path, os.path.join(self.exclusion_folder, image_name))
                  print(f"Moved to exclusion: {image_name}")
            
      def get_current_image_pair(self):
            """
            Retrieves the filenames of the current pair of ground truth 
            and corresponding images.

            Returns:
            tuple: A tuple containing two elements:
                  - The filename of the current ground truth image (str) or None.
                  - The filename of the corresponding regular image (str) or None.
            """
            if self.current_index > 0 and self.current_index <= len(self.gt_files):
                  gt_image_name = self.gt_files[self.current_index - 1]
                  image_name = self._get_image_name(gt_image_name)
                  return gt_image_name, image_name
            return None, None
