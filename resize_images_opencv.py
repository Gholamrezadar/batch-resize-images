# Gholamreza Dar May 2023
# Resize all the images in the 'images' folder and save them in the 'resized_images' folder
# Supports parallel resizing of images
# Currently only works with .jpg images you can manually change the glob pattern to work with other image formats
# The resized images will be 40% of the original size, you can change the PERCENT variable to resize the images to a different size
# 40 percent was chosen because for the images taken with my phone (4000px by 3000px) it was the best size/quality tradeoff, change as needed

import cv2
import pathlib
from joblib import Parallel, delayed
import time

PERCENT = 0.4
SRC_FOLDER = 'images'
DEST_FOLDER = 'resized_images'

# Check if images folder exists otherwise exit
if not pathlib.Path(SRC_FOLDER).exists():
    print("The 'images' folder does not exist. Please create it and insert the images you want to resize into it.")
    exit()

# Path to the folder containing the images
path = pathlib.Path(SRC_FOLDER)

# Check if the resized_images folder exists, if not create it
if not pathlib.Path(DEST_FOLDER).exists():
    pathlib.Path(DEST_FOLDER).mkdir()

result_path = pathlib.Path(DEST_FOLDER)
images_count = len(list(path.glob("*.jpg")))

def resize_image(image_path, percent=PERCENT):
    print(f"Resizing {image_path.name}...")

    # Read the image
    image = cv2.imread(str(image_path))

    # Resize the image
    resized_image = cv2.resize(image, (int(image.shape[1] * PERCENT), int(image.shape[0] * PERCENT)), interpolation = cv2.INTER_AREA)

    # Save the resized image
    cv2.imwrite(str(result_path / image_path.name), resized_image) 

start_time = time.perf_counter_ns()
print(f"> Number of images: {images_count}")
print("Results will be saved in the 'resized_images' folder\n")
print("Resizing images in parallel...")
# Resize all the images in parallel
Parallel(n_jobs=-1)(delayed(resize_image)(image_path) for image_path in path.glob("*.jpg"))

print(f"\nDone in {round((time.perf_counter_ns() - start_time) / 1000000000, 2)} seconds\n")

# get the size of the original images folder in MB
print(f"> Size of the 'images' folder: {round(sum(f.stat().st_size for f in path.glob('*.jpg') if f.is_file()) / (1024 * 1024), 2)} MB")

# get the size of the resized images folder in MB
print(f"> Size of the 'resized_images' folder: {round(sum(f.stat().st_size for f in result_path.glob('*.jpg') if f.is_file()) / (1024 * 1024), 2)} MB")
