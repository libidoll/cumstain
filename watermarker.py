import os

from appdirs import user_config_dir
from PyQt5 import QtWidgets
import json
from ui.mainwindow import Ui_MainWindow
from ui import filebrowser
from watermarker import file_ops
from watermarker.file_ops import backup_image
from watermarker.image_ops import add_watermark


class Watermarker(Ui_MainWindow):
    def __init__(self):
        MainWindow = QtWidgets.QDialog()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        self.ui = ui
        MainWindow.show()
        ui.file_browser.clicked.connect(
            lambda: filebrowser.select_file(allow_directories=True, allow_multiple=True, allow_videos=True,
                                            text_field=ui.file_line))
        ui.watermark_browser.clicked.connect(
            lambda: filebrowser.select_file(allow_directories=False, allow_multiple=False, allow_videos=False,
                                            text_field=ui.watermark_line))
        ui.process.clicked.connect(self.process)
        ui.save_settings.clicked.connect(self.save_settings)

        self.load_settings()

        sys.exit(app.exec_())

    def save_settings(self):
        settings = {
            "files": self.ui.file_line.text(),
            "recursive": self.ui.recursive_checkbox.isChecked(),
            "backup": self.ui.backup_checkbox.isChecked(),
            "skip_if_backup_exists": self.ui.skip_if_backup_exists.isChecked(),
            "watermark": self.ui.watermark_line.text(),
            "opacity": self.ui.opacity_input.value(),
            "position": self.ui.watermark_position.currentText(),
            "margin": self.ui.margin_input.value(),
            "scale": self.ui.scale_input.value()
        }

        os.makedirs(user_config_dir("watermarker"), exist_ok=True)
        with open(f'{user_config_dir("watermarker")}/settings.json', "w") as f:
            json.dump(settings, f)

    def load_settings(self):
        try:
            with open(f'{user_config_dir("watermarker")}/settings.json', "r") as f:
                settings = json.load(f)
        except FileNotFoundError:
            settings = {}

        self.ui.file_line.setText(settings.get("files", ""))
        self.ui.recursive_checkbox.setChecked(settings.get("recursive", False))
        self.ui.backup_checkbox.setChecked(settings.get("backup", True))
        self.ui.skip_if_backup_exists.setChecked(settings.get("skip_if_backup_exists", True))
        self.ui.watermark_line.setText(settings.get("watermark", ""))
        self.ui.opacity_input.setValue(settings.get("opacity", 50))
        self.ui.opacity_input.setValue(settings.get("opacity", 50))
        self.ui.watermark_position.setCurrentText(settings.get("position", "Top Left"))
        self.ui.margin_input.setValue(settings.get("margin", 15))
        self.ui.scale_input.setValue(settings.get("scale", 25))

    def process(self):
        files = self.ui.file_line.text()
        if files.startswith("["):
            files = json.loads(files)

        recursive = self.ui.recursive_checkbox.isChecked()
        backup = self.ui.backup_checkbox.isChecked()
        skip_if_backup_exists = self.ui.skip_if_backup_exists.isChecked()

        watermark = self.ui.watermark_line.text()
        opacity = self.ui.opacity_input.value()
        position = self.ui.watermark_position.currentText()
        margin = self.ui.margin_input.value()
        scale = self.ui.scale_input.value()
        print(files, recursive, backup, skip_if_backup_exists, watermark, opacity, position, margin, scale)

        to_process = file_ops.find_files(files, recursive=recursive, allow_videos=True)

        for file in to_process:
            # Get path of image
            path = os.path.dirname(file)
            # Get filename of image
            filename = os.path.basename(file)

            output_file = file

            if backup:
                backup_file = os.path.dirname(file) + "/.unwatermarked/" + os.path.basename(file)
                if not backup_image(file, backup_file):
                    if skip_if_backup_exists:
                        continue
                    else:
                        print("Backup already exists, using it as source")
                        file = backup_file

            add_watermark(file, output_file, watermark, opacity, position, margin, scale)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Watermarker()
