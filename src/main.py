from math import ceil
import os
import sys
import pathlib
import shutil
from turtle import pu

def main():
    reference_frame_rate = 30.0
    target_frame_rate = 15.0

    if len(sys.argv) != 3:
        print('parent folder not specified')
        return
    entity_parent_folder = sys.argv[1]
    out_parent_folder = sys.argv[2]
    print('entity parent folder:', entity_parent_folder)

    animation_subdirs = [f.path for f in os.scandir(
        entity_parent_folder) if f.is_dir()]
    for dir in animation_subdirs:
        direction_subdirs = [f.path for f in os.scandir(dir) if f.is_dir()]
        for direction_subdir in direction_subdirs:
            print(direction_subdir)
            for path, _, files in os.walk(direction_subdir):
                images = [image for image in files if pathlib.Path(
                    image).suffix == '.png']
                selected_images = []
                count = len(images)
                duration = count / reference_frame_rate
                to_select = ceil(duration * target_frame_rate)
                print(f'initial count {count}  -> select {to_select}')
                marker_increment = float(to_select) / count
                count_marker = 1.0
                for i in range(len(images)):
                    if count_marker >= 1.0 or i == len(images)-1:
                        selected_images.append(images[i])
                        count_marker = 0.0
                    else:
                        count_marker += marker_increment
                print(f'selected {len(selected_images)} :\n', selected_images)
                target_folder = os.path.join(out_parent_folder,os.path.basename(entity_parent_folder),os.path.basename(dir),os.path.basename(direction_subdir))
                print('save to', target_folder)
                os.makedirs(target_folder, exist_ok=True)
                for image in selected_images:
                    shutil.copy(pathlib.Path(path,image), pathlib.Path(target_folder,image))
            print()
        print()


if __name__ == "__main__":
    main()
