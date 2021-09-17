#!/usr/bin/python

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog, QDialog

from gui.windows_parameters_description import axis_dialog_wight, axis_dialog_height

# open dialog window to directory choosing and return chosen path
class ChooseAxisData(QDialog):
    def __init__(self):
        super().__init__()
        self.data = 'im from dialog'
        self.setGeometry(0, 0, axis_dialog_wight, axis_dialog_height)
        self.setWindowTitle('Choose axis data')
        self.center()

        dialog_window_label = QLabel('Choose data to display it on axis')
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(['Accessible messages'])
        self.fill_tree()

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(dialog_window_label)
        self.layout.addWidget(self.tree)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def fill_tree(self):
        for i in range(3):
            parent = QTreeWidgetItem(self.tree)
            parent.setText(0, "Message {}".format(i))
            # parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            for x in range(5):
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, "Msg field {}".format(x))
                child.setCheckState(0, Qt.Unchecked)
                child.setData(0, Qt.UserRole, 'hii')

    def get_checked_items(self):
        self.selected_items = list()
        iterator = QTreeWidgetItemIterator(self.tree, QTreeWidgetItemIterator.Checked)
        while iterator.value():
            item = iterator.value()
            self.selected_items.append([item.text(0), item.data(0, Qt.UserRole)])
            iterator += 1

    # put window to the middle of screen
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
