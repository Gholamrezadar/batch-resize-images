# Batch Resize Images

## Description

A simple python script that uses PIL and joblib to resize images in a directory to a specified fraction.

Crawls the source directory for images and resizes them to a specified fraction of the original size. The resized images are saved in the corresponding directory structure in the destination directory.

## Usage

```bash
python3 resize_images.py src/ dest/ --debug --quality 85 --percent 40 --min_width 1000 --jobs -1
```

`dest/ will be created if it does not exist`

## Performance

On an 8 core i7-6700HQ it takes about `15` seconds to resize `224` images of size ~`5000x3000` to `40%` of their original size.

- This results in a reduction from `1024 MB` to `102 MB` (10%)

- Or with 75 quality: `1024 MB` to `75 MB` (7.5%)

## Arguments

```txt

positional arguments:
  input_dir             Input directory containing images to resize
  output_dir            Output directory to save resized images

optional arguments:
     -h, --help                    show this help message and exit
     -d --debug                    Enable debug mode
     -q QUALITY --quality QUALITY  Quality of resized images (0 - 100)
     -p --percent PERCENT          Percent to resize images (0.0 - 1.0)
     -w --min_width MIN_WIDTH      Minimum width(or height which ever is bigger) of resized images
     -j --jobs JOBS                Number of jobs to run in parallel
```

## Requirements

joblib==1.2.0
