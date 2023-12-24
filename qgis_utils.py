from qgis.core import QgsRasterLayer, QgsProject
from qgis.utils import iface

def add_image_layer_to_qgis(image_name, image_path, opacity=1.0):
      """
      Adds an image layer to the QGIS project with specified opacity.

      Parameters:
      image_name (str): The name to assign to the layer in QGIS.
      image_path (str): The file path of the image to load.
      opacity (float, optional): The opacity level of the layer. 
                                    Defaults to 1.0 (fully opaque).

      Returns:
      QgsRasterLayer or None: The created raster layer if successful,
             or None if the layer creation fails.
      """
      layer = QgsRasterLayer(image_path, image_name)
      
      if layer.isValid():
                  if opacity != 1.0:
                        layer.renderer().setOpacity(opacity)
                  QgsProject.instance().addMapLayer(layer)
                  return layer
      else:
                  print(f"Failed to load image: {image_name}")
                  return None

def remove_layer_from_qgis(layer_name):
      """
      Removes a layer from the current QGIS project by its name.

      Parameters:
      layer_name (str): The name of the layer to be removed
        from the QGIS project.
      """
      layer = QgsProject.instance().mapLayersByName(layer_name)
      if layer:
            QgsProject.instance().removeMapLayer(layer[0].id())
