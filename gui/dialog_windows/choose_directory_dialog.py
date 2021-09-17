from PyQt5.QtWidgets import QFileDialog, QDialog


# open dialog window to directory choosing and return chosen path
def choose_directory():
    dialog = QFileDialog()
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    options |= QFileDialog.DontUseCustomDirectoryIcons
    dialog.setOptions(options)
    dialog.setAcceptMode(QFileDialog.AcceptOpen)
    dialog.setFileMode(QFileDialog.DirectoryOnly)
    if dialog.exec_() == QDialog.Accepted:
        return dialog.selectedFiles()[0]  # returns a list
    else:
        return str()
