# Give it two folders, It will find the files that are not
# in the first folder but in the second folder.

from pathlib import Path
from collections import Counter

def count_similar_files(directory1, directory2):
    dir1_files = set(Path(directory1).glob('*'))
    dir2_files = set(Path(directory2).glob('*'))
    
    file_names1 = {file.name for file in dir1_files if file.is_file()}
    file_names2 = {file.name for file in dir2_files if file.is_file()}
    
    print(f"{dir1} files: {len(file_names1)}")
    print(f"{dir2} files: {len(file_names2)}")

    dissimilar_files = file_names2 - file_names1

    print(f"Dir2-Dir1: {len(dissimilar_files)}")

    for p in list(dissimilar_files)[:10]:
        print(p)

# Example usage:
dir1 = '/media/ghd/WD1TB/AX/S6 Edge p2/Camera'
dir2 = '/media/ghd/WD1TB/AX/S6 Edge p3/'

count_similar_files(dir1, dir2)