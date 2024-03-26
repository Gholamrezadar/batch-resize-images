# Gholamreza Dar May 2023
# Resize all the images in the 'images' folder and save them in the 'resized_images' folder
# Supports parallel resizing of images
# Currently only works with .jpg images you can manually change the glob pattern to work with other image formats
# The resized images will be 40% of the original size, you can change the PERCENT variable to resize the images to a different size
# 40 percent was chosen because for the images taken with my phone (4000px by 3000px) it was the best size/quality tradeoff, change as needed

import argparse
from email.mime import image
import time
import pathlib

from PIL import Image, ExifTags
from joblib import Parallel, delayed

def resize_image(image_path, src_path, dest_path, percent, min_width, debug=True, quality=85):
    """Resize an image and save it in the corresponding destination folder. the corresponding destination folder
    is calculated by removing the src_path from the image_path and prepending the dest_path to the image path.

    Args:
        image_path (pathlib.Path): The path to the image to resize
        src_path (pathlib.Path): The path to the source folder
        dest_path (pathlib.Path): The path to the destination folder
        percent (float): The percentage to resize the image to
        min_width (int): The minimum width of the resulting image(here width means the longer side of the image)
        debug (bool, optional): Whether to print debug messages or not. Defaults to True.
        quality (int, optional): The quality of the resized image. Defaults to 85.
    """
    if debug:
        print(f"resizing {image_path}...")

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
        #TODO handle exception
        pass

    # Calculate the new size
    width = int(image.width * percent)
    height = int(image.height * percent)
    new_size = (width, height)

    # Skipping images with width less than min_width
    resized_image = image 
    if max(width, height) >= min_width:
        resized_image = image.resize(new_size)
    else:
        if debug:
            print(f"> Skipping {image_path.name} because it's longer side is less than {min_width}px")
        
    # Create any needed subdir in dest_path(get from image_path.relative_to)
    if not pathlib.Path(dest_path / image_path.relative_to(src_path).parent).exists():
        pathlib.Path(dest_path / image_path.relative_to(src_path).parent).mkdir(parents=True, exist_ok=True)

    # Save the resized image with the original EXIF data
    if exif_data is None:
        resized_image.save(dest_path / image_path.relative_to(src_path), quality=quality)
    else:
        resized_image.save(dest_path / image_path.relative_to(src_path), exif=exif_data, quality=quality)

def human_readable_time(time_in_ns: int) -> str:
    """Converts time in nanoseconds to a human readable format"""
    time_in_seconds = time_in_ns / 1e9

    # if time is less than 60 seconds display in seconds
    if time_in_seconds < 60:
        return f"{time_in_seconds:.2f} seconds"
    
    # if time is less than 60 minutes display in minutes and remainder seconds
    if time_in_seconds < 3600:
        return f"{time_in_seconds // 60:.0f} minutes and {time_in_seconds % 60:.0f} seconds"
    
    # if time is less than 24 hours display in hours and remainder minutes
    if time_in_seconds < 86400:
        return f"{time_in_seconds // 3600:.0f} hours and {(time_in_seconds % 3600) // 60:.0f} minutes"
    
    return "more than 24 hours"

if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Resize all the images in the source folder and save them in the destination folder')
    parser.add_argument('src_folder', type=str, help='The source folder containing the images to resize')
    parser.add_argument('dest_folder', type=str, help='The destination folder to save the resized images in')
    parser.add_argument('-p', '--percent', type=float, default=0.4, help='The percentage to resize the images to, default is 0.4')
    parser.add_argument('-j', '--jobs', type=int, default=-1, help='The number of jobs to run in parallel, default is -1 or all cores')
    parser.add_argument('-w', '--min_width', type=int, default=1000, help='The minimum resulting image width or height which ever is bigger required for resizing, default is 1000px')
    parser.add_argument('-d', '--debug', action='store_true', help='Print debug messages')
    parser.add_argument('-q', '--quality', type=int, default=85, help='The quality of the resized image, default is 85')
    args = parser.parse_args()

    SRC_FOLDER: str = args.src_folder
    DEST_FOLDER: str = args.dest_folder
    PERCENT: float = args.percent
    JOBS: int = args.jobs
    MIN_WIDTH: int = args.min_width
    DEBUG: bool = args.debug
    QUALITY: int = args.quality
    EXTENSION_SET: set = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}

    # Make sure the percentage is between 0 and 1
    if PERCENT <= 0 or PERCENT > 1:
        print("The percentage must be between 0 and 1")
        exit()
    
    # Make sure min_width is greater than 0
    if MIN_WIDTH <= 0:
        print("The minimum width must be greater than 0")
        exit()
    
    # Make sure quality is between 0 and 100
    if QUALITY < 0 or QUALITY > 100:
        print("The quality must be between 0 and 100")
        exit()

    # print(args)
    # exit()

    # Check if images folder exists otherwise exit
    if not pathlib.Path(SRC_FOLDER).exists():
        print(f"The '{SRC_FOLDER}' folder does not exist. Please create it and insert the images you want to resize into it.")
        exit()
    
    # Check if the resized_images folder exists, otherwise create it
    if not pathlib.Path(DEST_FOLDER).exists():
        if DEBUG or True:
            print(f"{DEST_FOLDER} doesn't exist. Creating the '{DEST_FOLDER}' folder...")
        pathlib.Path(DEST_FOLDER).mkdir(parents=True)

    # Paths to the source and destination folders    
    path = pathlib.Path(SRC_FOLDER)
    result_path = pathlib.Path(DEST_FOLDER)

    # Get the list of images to resize
    images = [p for p in path.glob("**/*") if p.suffix in EXTENSION_SET]
    images_count = len(images)
    images_size = sum([p.stat().st_size for p in images])

    # Start the timer
    start_time = time.perf_counter_ns()

    # Print some info
    if DEBUG or True:
        print(f"> Number of images: {images_count}")
        print(f"> Results will be saved in the '{DEST_FOLDER}' folder")
        print(f"\n> Resizing images in parallel using {args.jobs} jobs...")
    
    # a wrapper around resize_image
    def resize_image_wrapper(image_path):
        resize_image(image_path, path, result_path, PERCENT, MIN_WIDTH, DEBUG, QUALITY)
    
    # Resize all the images in parallel
    Parallel(n_jobs=JOBS, verbose=6)(delayed(resize_image_wrapper)(image_path) for image_path in images)

    # Stop the timer
    end_time = time.perf_counter_ns()

    # Print some info
    if DEBUG or True:
        result_images_count = len([p for p in result_path.glob('**/*') if p.suffix in EXTENSION_SET])
        result_images_size = sum([p.stat().st_size for p in result_path.glob('**/*') if p.suffix in EXTENSION_SET])

        print(f"\n> Done in {human_readable_time(end_time - start_time)}")
        print(f"Results saved in the '{DEST_FOLDER}' folder")
        print()
        print(f"> Source: {images_count} images, {images_size / 1e6:.2f} MB")
        print(f"> Result: {result_images_count} images, {result_images_size / 1e6:.2f} MB ({result_images_size / images_size * 100:.2f}%)")
        
        # This is wrong:
        # print(f"> {images_count - result_images_count} images were skipped because their longer side was less than {MIN_WIDTH}px" )
