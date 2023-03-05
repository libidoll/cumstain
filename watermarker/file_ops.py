import os
import shutil

image_extensions = [".png", ".jpg", ".jpeg", ".bmp"]
video_extensions = [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"]

def backup_image(file):
    backupfile = os.path.dirname(file) + "/unwatermarked/" + os.path.basename(file)

    if not os.path.exists(os.path.dirname(backupfile)):
        os.makedirs(os.path.dirname(backupfile))
    if os.path.exists(backupfile):
        print("Using backup file instead of original")
        shutil.copyfile(backupfile, file)
    else:
        shutil.copyfile(file, backupfile)


def find_files(files, allow_videos=False, recursive=False):
    for file in files:
        if os.path.isdir(file):
            if recursive:
                for root, dirs, files in os.walk(file):
                    for i in files:
                        if i.endswith(tuple(image_extensions)) or (allow_videos and i.endswith(tuple(video_extensions))):
                            yield os.path.join(root, i)
        else:
            yield file
