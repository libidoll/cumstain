import json
from PyQt5 import QtWidgets


def file_browser(parent=None, caption='', directory='',
                 filter='', initialFilter='', options=None, allow_multiple=False, allow_directories=False):
    def updateText():
        # update the contents of the line edit widget with the selected files
        selected = []
        for index in view.selectionModel().selectedRows():
            selected.append('"{}"'.format(index.data()))
        lineEdit.setText(' '.join(selected))

    dialog = QtWidgets.QFileDialog(parent, windowTitle=caption)
    if allow_multiple:
        dialog.setFileMode(dialog.ExistingFiles)
    else:
        dialog.setFileMode(dialog.ExistingFile)

    if options:
        dialog.setOptions(options)
    dialog.setOption(dialog.DontUseNativeDialog, True)
    if directory:
        dialog.setDirectory(directory)
    if filter:
        dialog.setNameFilter(filter)
        if initialFilter:
            dialog.selectNameFilter(initialFilter)

    if allow_directories:
        dialog.accept = lambda: QtWidgets.QDialog.accept(dialog)

    # there are many item views in a non-native dialog, but the ones displaying
    # the actual contents are created inside a QStackedWidget; they are a
    # QTreeView and a QListView, and the tree is only used when the
    # viewMode is set to QFileDialog.Details, which is not this case
    stackedWidget = dialog.findChild(QtWidgets.QStackedWidget)
    view = stackedWidget.findChild(QtWidgets.QListView)
    view.selectionModel().selectionChanged.connect(updateText)

    lineEdit = dialog.findChild(QtWidgets.QLineEdit)
    # clear the line edit contents whenever the current directory changes
    dialog.directoryEntered.connect(lambda: lineEdit.setText(''))

    dialog.exec_()
    return dialog.selectedFiles()


def select_file(allow_directories=False, allow_multiple=False, allow_videos=False, text_field=None):
    if allow_videos:
        file_filter = "Media Files (*.png *.jpg *.jpeg *.bmp *.mp4 *.avi *.mov *.mkv *.flv *.wmv *.webm);;" \
                      "Image Files (*.png *.jpg *.jpeg *.bmp);;" \
                    "Video Files (*.mp4 *.avi *.mov *.mkv *.flv *.wmv *.webm);;"
    else:
        file_filter = "Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;"

    if allow_multiple:
        files = file_browser(None, "Select Files", "", file_filter, allow_directories=allow_directories, allow_multiple=allow_multiple)
    else:
        files = file_browser(None, "Select File", "", file_filter, allow_directories=allow_directories, allow_multiple=allow_multiple)

    if text_field is not None:
        if len(files) > 0:
            if isinstance(files, list):
                if allow_multiple:
                    text_field.setText(json.dumps(files))
                else:
                    text_field.setText(files[0])

        else:
            text_field.setText("")

    return files
