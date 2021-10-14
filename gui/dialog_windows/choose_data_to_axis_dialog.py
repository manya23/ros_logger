#!/usr/bin/python
import copy

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog

from pydoc import locate

from gui.windows_parameters_description import axis_dialog_wight, axis_dialog_height
from ros_logger_scripts.data_display_modules.get_msg_field_type import get_common_types_list

common_field_type = get_common_types_list()


# open dialog window to directory choosing and return chosen path
class ChooseAxisData(QDialog):
    def __init__(self, topic_dict):
        super().__init__()
        self.topic_dict = topic_dict
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
        import_msg_lib(self.topic_dict)

        for topic_name in self.topic_dict:
            parent = QTreeWidgetItem(self.tree)
            parent.setText(0, "Messages from {}".format(topic_name))
            # parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)

            child = QTreeWidgetItem(parent)
            child.setText(0, "{}".format(self.topic_dict[topic_name]))

            # TODO: тут заполнять поля сообщения, которые есть у сообщения с типом self.topic_dict[topic_name]
            # print(self.topic_dict[topic_name])
            fill_ros_msg_to_tree_branch(child, self.topic_dict[topic_name], topic_name, path_to_field = [], branch_depth=0,
                                        parent_msg_types=list())
            # for x in range(5):
            #     sub_child = QTreeWidgetItem(child)
            #     sub_child.setFlags(sub_child.flags() | Qt.ItemIsUserCheckable)
            #     sub_child.setText(0, "Msg field {}".format(x))
            #     sub_child.setCheckState(0, Qt.Unchecked)
            #     sub_child.setData(0, Qt.UserRole, 'hii')

    def get_checked_items(self):
        self.selected_items = list()
        iterator = QTreeWidgetItemIterator(self.tree, QTreeWidgetItemIterator.Checked)
        while iterator.value():
            item = iterator.value()
            self.selected_items.append({'field name': item.text(0), 'field data': item.data(0, Qt.UserRole)})
            iterator += 1

    # put window to the middle of screen
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def fill_ros_msg_to_tree_branch(parent_branch, ros_msg_type, topic_name, path_to_field, branch_depth, parent_msg_types):
    msg_object = locate(ros_msg_type)()
    parent_msg_types.append(ros_msg_type)
    parent_path_to_field = copy.deepcopy(path_to_field)
    msg_fields_list = msg_object.get_fields_and_field_types()  # msg_object.__slots__
    for field in msg_fields_list:
        child = QTreeWidgetItem(parent_branch)
        child.setText(0, "{}".format(field))
        field_type = msg_fields_list[field]
        # if branch_depth != 0:
        #     path_to_field += '.' + field
        # else:
        #     path_to_field += field
        path_to_field.append(field)
        # TODO: будет ли это стабильно работать -> в случае ошибки сделать запрос ручного ввода
        if 'sequence' in field_type:
            field_type = field_type.replace('sequence', '').replace('<', '').replace('>', '').replace('/', '.msg.')
            # print('field with seq type: ', field_type)
            if field_type not in common_field_type:
                branch_depth += 1
                fill_ros_msg_to_tree_branch(child, field_type, topic_name, path_to_field, branch_depth, parent_msg_types)
            else:
                data = {'name': topic_name, 'types': parent_msg_types, 'path': path_to_field}
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setCheckState(0, Qt.Unchecked)
                child.setData(0, Qt.UserRole, data)
        elif field_type not in common_field_type:
            branch_depth += 1
            field_type = field_type.replace('/', '.msg.')
            # print('field with not common type: ', field_type)
            fill_ros_msg_to_tree_branch(child, field_type, topic_name, path_to_field, branch_depth, parent_msg_types)
        else:
            data = {'name': topic_name, 'types': parent_msg_types, 'path': path_to_field}
            child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
            child.setCheckState(0, Qt.Unchecked)
            child.setData(0, Qt.UserRole, data)
            # [topic_name, path_to_field, f'{ros_msg_type}.{field}']
        path_to_field = copy.deepcopy(parent_path_to_field)


def import_msg_lib(topic_dict):
    msg_to_import = list()
    for topic_name, msg_type in topic_dict.items():
        msg_type_module_name = str()
        for char in msg_type:
            if char != '.':
                msg_type_module_name += char
            else:
                break
        msg_to_import.append(msg_type_module_name)
    # import required modules
    for module in msg_to_import:
        globals()[module] = __import__(module)

