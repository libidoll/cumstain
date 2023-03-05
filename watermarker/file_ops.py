import os
import shutil

image_extensions = [".png", ".jpg", ".jpeg", ".bmp"]
video_extensions = [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"]

def backup_image(file, backup_file):
    if not os.path.exists(os.path.dirname(backup_file)):
        os.makedirs(os.path.dirname(backup_file))
    if os.path.exists(backup_file):
        return False
    else:
        shutil.copyfile(file, backup_file)
        return True


def find_files(files, allow_videos=False, recursive=False):
    for file in files:
        if os.path.isdir(file):
            if recursive:
                for root, dirs, files in os.walk(file):
                    for i in files:
                        if i.endswith(tuple(image_extensions)) or (allow_videos and i.endswith(tuple(video_extensions))):
                            if "/.unwatermarked/" not in os.path.join(root, i):
                                yield os.path.join(root, i)
        else:
            yield file
