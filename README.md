# README

This project processes images to determine the focal length distribution of person and scenery images using Python. It utilizes the YOLOv5 model for object detection to classify images as either containing a person or scenery.

## Prerequisites

Python version
- Python 3.10

Python library 
- pillow
- yolov5

## Usage

1. Update the `directory` variable in `main.py` with the paths to your image directories.

2. Run the script:
    ```sh
    python main.py
    ```

3. The script will output the number of person and scenery images found and generate histograms of the focal length distributions, saved as `person_focal_length_distribution.png` and `scenery_focal_length_distribution.png`.

## Files

- `main.py`: Main script to process images and generate focal length distribution plots.
- `util.py`: Utility functions including the `is_person` function which uses YOLOv5 for person detection in images.

## Functions

### `main.py`

- `get_focal_length(image_path)`: Extracts the focal length from the EXIF data of an image.
- `get_all_focal_lengths(directories)`: Iterates through directories to classify images and collect focal lengths.
- `plot_focal_length_distribution(focal_lengths, subject)`: Plots and saves the focal length distribution histogram.

### `util.py`

- `is_person(image_path)`: Uses YOLOv5 to detect if an image contains a person.
- `is_central(x1, y1, x2, y2, image_width, image_height)`: Determines if a detected object is centrally located in the image.
