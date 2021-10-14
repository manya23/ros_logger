from PyQt5.QtWidgets import QFileDialog, QDialog


# open dialog window to file choosing and return chosen path
def choose_file():
    dialog = QFileDialog()
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    options |= QFileDialog.DontUseCustomDirectoryIcons
    dialog.setOptions(options)
    dialog.setAcceptMode(QFileDialog.AcceptOpen)
    dialog.setFileMode(QFileDialog.AnyFile)
    if dialog.exec_() == QDialog.Accepted:
        return dialog.selectedFiles()[0]  # returns a list
    else:
        return str()
