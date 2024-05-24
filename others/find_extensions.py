# This program crawls a directory and finds all file extensions
# Usage: python find_extensions.py <directory>

import argparse
from pathlib import Path

def get_file_extensions(directory):
    extensions = set()

    # Convert the directory path to a Path object
    path = Path(directory)

    # Iterate through all files and subdirectories recursively
    for file in path.glob('**/*'):
        if file.is_file():
            # Get the file extension
            extension = file.suffix
            extensions.add(extension)

    return extensions

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Crawl a directory and find file extensions')

    # Add the root directory argument
    parser.add_argument('directory', type=str, help='Root directory to crawl')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the function to get the file extensions
    extensions = get_file_extensions(args.directory)

    # Print the file extensions
    for extension in extensions:
        print(extension)

if __name__ == '__main__':
    main()
