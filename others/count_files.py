# Counts the number of files of different types in a folder

from pathlib import Path
import argparse

def count_files_and_size(root_folder, extension):
    count = 0
    total_size = 0

    for path in root_folder.glob('**/*.' + extension):
        if path.is_file():
            count += 1
            total_size += path.stat().st_size

    return count, total_size

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Count the number of images and videos in a folder')
    parser.add_argument('root_folder', type=str, help='The root folder to count the images and videos in')

    args = parser.parse_args()

    root_folder = Path(args.root_folder)

    jpg_count, jpg_size = count_files_and_size(root_folder, 'jpg')
    mp4_count, mp4_size = count_files_and_size(root_folder, 'mp4')
    JPG_count, JPG_size = count_files_and_size(root_folder, 'JPG')
    MOV_count, MOV_size = count_files_and_size(root_folder, 'MOV')
    MKV_count, MKV_size = count_files_and_size(root_folder, 'mkv')
    RAR_count, RAR_size = count_files_and_size(root_folder, 'rar')

    print(f"jpg Images: Count = {jpg_count}, Size = {jpg_size / (1024 * 1024 * 1024):.3f} GB")
    print(f"JPG Images: Count = {JPG_count}, Size = {JPG_size / (1024 * 1024 * 1024):.3f} GB")
    print(f"mp4 Videos: Count = {mp4_count}, Size = {mp4_size / (1024 * 1024 * 1024):.3f} GB")
    print(f"MOV Videos: Count = {MOV_count}, Size = {MOV_size / (1024 * 1024 * 1024):.3f} GB")
    print(f"MKV Videos: Count = {MKV_count}, Size = {MKV_size / (1024 * 1024 * 1024):.3f} GB")
    print(f"RAR Files: Count = {RAR_count}, Size = {RAR_size / (1024 * 1024 * 1024):.3f} GB")

    print(f"Total: Count = {jpg_count + JPG_count + mp4_count + MOV_count}, Size = {(jpg_size + JPG_size + mp4_size + MOV_size) / (1024 * 1024 * 1024):.3f} GB")
