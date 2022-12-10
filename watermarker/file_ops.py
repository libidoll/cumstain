import os
import shutil


def backup_image(file):
    backupfile = os.path.dirname(file) + "/unwatermarked/" + os.path.basename(file)

    if not os.path.exists(os.path.dirname(backupfile)):
        os.makedirs(os.path.dirname(backupfile))
    if os.path.exists(backupfile):
        print("Using backup file instead of original")
        shutil.copyfile(backupfile, file)
    else:
        shutil.copyfile(file, backupfile)


def get_files(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if
            file.endswith(".jpg") or file.endswith(".png")]
