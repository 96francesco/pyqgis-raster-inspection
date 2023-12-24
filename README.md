# Raster inspection with QGIS

## About
During my thesis work at Wageningen University & Research, I realized I had to manually review my ground truth data. I needed a way to quickly inspect the raster data and see if the ground truth data was correct. If not, I wanted to manually edit it or, if the discrepancy was too big, remove the ground truth - satellite image pair from my dataset. I discovered the QGIS plugin [Serval](https://plugins.qgis.org/plugins/Serval/), which allows to easily change the value of a raster layer with one click. However, I needed a way to quickly switch to the next raster layer and mark images to be removed from the dataset. That's why I created this Python script tool to ease this process.

## Installation

### Prerequisites
- You need to install [QGIS](https://qgis.org/en/site/forusers/download.html) and launch it.
- At the moment, the script asumes a specific naming convention for the images:
      - Ground truth images should be prefixed with gt_. For example, if you have a satellite image named image_0.tif, its corresponding ground truth image should be named image_gt_0.tif.
      - Both ground truth and corresponding satellite images must have a numeric index at the end of their names. This index is used by the script to determine the order of the images and switch to the next pair. 

### Download the script
1. Clone the repository or download the ZIP file and extract it.
```bash
git clone https://github.com/your-github-username/pyqgis-raster-inspector.git
```
2. Navigate to the downloaded/cloned directory

### Setting up
1. Place the satellite images and ground truth images in separate folders (you can use the example images provided in the repository to test the tool)
2. Also create a folder for the excluded images.

## Usage
1. In QGIS, open the Python console (Plugins > Python Console)
2. In the console pane, click on 'Show Editor' (the icon with the pencil). This will open the Python editor.
3. Click on 'Open script' and select the '**main.py**' file fro the downloaded/cloned repository.
4. Modify the following lines with the correct paths to your folders:
```python
image_folder = 'your\\image\\folder\\path'
gt_folder = 'your\\ground\\truth\\folder\\path'
exclusion_folder = 'your\\exclusion\\folder\\path'
```
You can also edit the following line, depending from which image yo want to start:
```python
start_index = 0
```
5. Run the script. The first pair of images will be loaded. You can use these methods:
      - '**load_next()**' to load the next pair of images
      - '**handler.mark_image()**' to mark the current pair of images to be excluded from the dataset. The images will be moved to the exclusion folder.

## Example data

## Contributing