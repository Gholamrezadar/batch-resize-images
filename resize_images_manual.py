## NOTE ##
# DO NOT USE THIS FILE
# USE 'resize_images.py'
# THIS FILE WAS ONLY USED FOR DEBUGGING

# Gholamreza Dar May 2023
# Resize all the images in the 'images' folder and save them in the 'resized_images' folder
# Supports parallel resizing of images
# Currently only works with .jpg images you can manually change the glob pattern to work with other image formats
# The resized images will be 40% of the original size, you can change the PERCENT variable to resize the images to a different size
# 40 percent was chosen because for the images taken with my phone (4000px by 3000px) it was the best size/quality tradeoff, change as needed

from math import e
import pathlib
from joblib import Parallel, delayed
from PIL import Image, ExifTags
import time

PERCENT = 0.4
# SRC_FOLDER = 'images'
# DEST_FOLDER = 'resized_images'
SRC_FOLDER = '/media/ghd/Data/_Backup/Galaxy S8 Backup/12-15-2022/pics'
DEST_FOLDER = '/media/ghd/Data/_Backup/resized_photos/Galaxy S8 Backup/12-15-2022/pics'

# Check if images folder exists otherwise exit
if not pathlib.Path(SRC_FOLDER).exists():
    print("The 'images' folder does not exist. Please create it and insert the images you want to resize into it.")
    exit()

# Path to the folder containing the images
path = pathlib.Path(SRC_FOLDER)

# Check if the resized_images folder exists, if not create it
if not pathlib.Path(DEST_FOLDER).exists():
    pathlib.Path(DEST_FOLDER).mkdir(parents=True)

result_path = pathlib.Path(DEST_FOLDER)
images_count = len(list(path.glob("*.jpg")))

def resize_image(image_path, percent=PERCENT):
    print(f"Resizing {image_path.name}...")

    # Open the image using PIL
    image = Image.open(image_path)

    # Load the EXIF data
    exif_data = None
    try:
        for key, value in image.info.items():
            if key == 'exif':
                exif_data = value
                break
    except:
        #TODO: handle exception
        pass

    # Calculate the new size
    width = int(image.width * percent)
    height = int(image.height * percent)
    new_size = (width, height)

    # Resize the image
    resized_image = image.resize(new_size)

    # Save the resized image with the original EXIF data
    if exif_data is None:
        resized_image.save(result_path / image_path.name, quality=85)
    else:
        resized_image.save(result_path / image_path.name, exif=exif_data, quality=85)


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
