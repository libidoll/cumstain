import PyQt5

from PyQt5 import QtWidgets
import json
from ui.mainwindow import Ui_MainWindow
from ui import filebrowser
from watermarker import file_ops
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
        ui.bottom_buttons.accepted.connect(self.process)
        sys.exit(app.exec_())

    def process(self):
        files = self.ui.file_line.text()
        if files.startswith("["):
            files = json.loads(files)

        recursive = self.ui.recursive_checkbox.isChecked()
        backup = self.ui.backup_checkbox.isChecked()

        watermark = self.ui.watermark_line.text()
        opacity = self.ui.opacity_input.value()
        position = self.ui.watermark_position.currentText()
        margin = self.ui.margin_input.value()
        scale = self.ui.scale_input.value()
        print(files, recursive, backup, watermark, opacity, position, margin, scale)

        to_process = file_ops.find_files(files, recursive=recursive, allow_videos=True)
        for file in to_process:
            add_watermark(file, watermark, opacity, position, margin, scale)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Watermarker()
