import os
import sys

# set directory
script_dir = 'your\\script\\directory\\path'
if script_dir not in sys.path:
      sys.path.append(script_dir)

from image_loader import ImageHandler
import qgis_utils

def main():
      image_folder = 'your\\image\\folder\\path'
      gt_folder = 'your\\ground\\truth\\folder\\path'
      exclusion_folder = 'your\\exclusion\\folder\\path'

      start_index = 0
      handler = ImageHandler(image_folder, gt_folder, exclusion_folder, start_index)

      def load_next_pair():
            # remove current images from QGIS if they exist
            if handler.current_index > 0:
                  current_gt_image, current_image = handler.get_current_image_pair()
                  qgis_utils.remove_layer_from_qgis(current_image)
                  qgis_utils.remove_layer_from_qgis(current_gt_image)

            # Load next pair of images
            gt_image_name, image_name = handler.load_next_image()
            if gt_image_name and image_name:
                  image_layer = qgis_utils.add_image_layer_to_qgis(image_name, 
                                                                   os.path.join(image_folder, image_name))
                  gt_layer = qgis_utils.add_image_layer_to_qgis(gt_image_name, 
                                                                os.path.join(gt_folder, gt_image_name), 
                                                                opacity=0.5) # 50% opacity

                  # zoom to the extent of the new image layer
                  if image_layer:
                        iface.mapCanvas().setExtent(image_layer.extent())
                        iface.mapCanvas().refresh()

            else:
                  print("No more images to load.")

      # load the first pair of images
      load_next_pair()

      # return the function and the handler instance
      return load_next_pair, handler

# assign the returned values to variable (to use outside the scope of main())
load_next, handler = main()

if __name__ == "__main__":
    main()
