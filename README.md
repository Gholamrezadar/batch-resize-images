# Batch Resize Images

## Description

A simple python script that uses PIL and joblib to resize images in a directory to a specified fraction.

## Usage

Have a directory of images named 'images' and a directory named 'resized_images'. Run the script from the parent of both of this directories.

```txt
parent/
|
|--- images/
     | image1.jpg
     | image2.jpg
     | etc
|--- resized_images/
|--- resize_images.py
```

## Requirements

joblib==1.2.0
