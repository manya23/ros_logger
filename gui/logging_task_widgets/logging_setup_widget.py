from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

import json


class LoggingSetupWidget(QWidget):
    def __init__(self, logging_manage_object):
        super(LoggingSetupWidget, self).__init__()
        self.logging_manage_object = logging_manage_object
        self.config_file_path = str()

        self.__init_widget()

    def __init_widget(self):
        # declare main window widgets
        self.table_info_label = QLabel('Choose topics to start write down messages published there')
        # self.table_info_label.setVisible(False)

        # button to make all checkboxes selected
        self.select_all_button = QPushButton('Select all')
        self.select_all_button.clicked.connect(self.__select_all_checkboxes)
        # self.select_all_button.setVisible(False)

        # button to make all checkboxes unselected
        self.deselect_all_button = QPushButton('Deselect all')
        self.deselect_all_button.clicked.connect(self.__deselect_all_checkboxes)
        # self.deselect_all_button.setVisible(False)

        save_config_info_label = QLabel('You can save checked topics to config file')
        self.save_config_button = QPushButton('Save to file')
        self.save_config_button.setEnabled(False)

        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.__go_to_logging_process)
        # self.next_button.setVisible(False)

        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.__go_to_previous_widget)

        # create table to display topic with checkboxes
        self.default_table_len = 0
        self.topic_list_display_table = QTableWidget(self.default_table_len, 2)
        topic_list_display_table_header = self.topic_list_display_table.horizontalHeader()
        topic_list_display_table_header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        topic_list_display_table_header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # self.topic_list_display_table.setVisible(False)

        self.table_manage_buttons_layout = QHBoxLayout()
        self.table_manage_buttons_layout.addWidget(self.select_all_button)
        self.table_manage_buttons_layout.addWidget(self.deselect_all_button)

        self.widget_manage_buttons_layout = QHBoxLayout()
        self.widget_manage_buttons_layout.addWidget(self.back_button)
        self.widget_manage_buttons_layout.addStretch(1)
        self.widget_manage_buttons_layout.addWidget(self.next_button)

        self.log_writing_widget_layout = QVBoxLayout()
        self.log_writing_widget_layout.addWidget(self.table_info_label)
        self.log_writing_widget_layout.addWidget(self.topic_list_display_table)
        self.log_writing_widget_layout.addLayout(self.table_manage_buttons_layout)
        self.log_writing_widget_layout.addWidget(save_config_info_label)
        self.log_writing_widget_layout.addWidget(self.save_config_button)
        self.log_writing_widget_layout.addLayout(self.widget_manage_buttons_layout)
        # self.log_writing_widget_layout.addWidget(self.next_button, alignment=Qt.AlignCenter)

        self.setLayout(self.log_writing_widget_layout)

        self.setGeometry(500, 500, 500, 700)
        self.setWindowTitle('Log writing window')
        self.show()

    # data is report describe structure
    def __add_new_checkbox_point(self, row_num, label, data):
        check_item = QTableWidgetItem()
        check_item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        check_item.setCheckState(QtCore.Qt.Unchecked)
        check_item.setData(QtCore.Qt.UserRole, check_item.checkState())
        check_item.setTextAlignment(1)
        self.topic_list_display_table.setItem(row_num, 0, check_item)

        struct_item = QTableWidgetItem()
        struct_item.setText(label)
        struct_item.setData(QtCore.Qt.UserRole, data)
        self.topic_list_display_table.setItem(row_num, 1, struct_item)

    def __select_all_checkboxes(self):
        for row in range(self.topic_list_display_table.rowCount()):
            self.topic_list_display_table.item(row, 0).setCheckState(QtCore.Qt.Checked)

    def __deselect_all_checkboxes(self):
        for row in range(self.topic_list_display_table.rowCount()):
            self.topic_list_display_table.item(row, 0).setCheckState(QtCore.Qt.Unchecked)

    def __fill_topic_list_display_table(self, config):
        self.table_len = int()
        topic_name_list = list()
        # fill table fields with info from config file
        for topic_describe_dict in config:
            if topic_describe_dict['name'] in topic_name_list:
                continue
            row_pose = self.topic_list_display_table.rowCount()
            self.topic_list_display_table.insertRow(row_pose)
            table_label = 'Topic ' + '\'' + topic_describe_dict['name'] + '\'' + ' with type ' \
                          + '\'' + topic_describe_dict['type'] + '\''
            self.__add_new_checkbox_point(row_pose, table_label, topic_describe_dict)
            topic_name_list.append(topic_describe_dict['name'])
            self.table_len += 1
        print('table len', self.table_len)

    def fill_table(self, config_file):
        # in case when config file is path to json file, first we have to read config file
        if type(config_file) == str:
            # load info from config file
            with open(config_file) as json_file:
                config = json.load(json_file)
            self.__fill_topic_list_display_table(config)
        # in other way we just pass config_file variable to fill table
        else:
            self.__fill_topic_list_display_table(config_file)

    def clean_table(self):
        # clear table
        for table_row in range(self.table_len, -1, -1):
            self.topic_list_display_table.removeRow(table_row)

    def __get_checked_items(self):
        self.selected_topics = list()
        for i in range(self.topic_list_display_table.rowCount()):
            current_state = self.topic_list_display_table.item(i, 0).checkState()
            if current_state == Qt.Checked:
                self.selected_topics.append(self.topic_list_display_table.item(i, 1).data(QtCore.Qt.UserRole))

        print('Выбраны топики: ', self.selected_topics)

    def __go_to_logging_process(self):
        self.__get_checked_items()
        # set new widget with choosing of directory to save logs start button
        self.logging_manage_object.go_to_logging_start_widget(self.selected_topics)

    def __go_to_previous_widget(self):
        self.clean_table()
        self.logging_manage_object.go_to_get_topic_list_widget()

# if __name__ == '__main__':
#     import sys
#
#     # Create the Qt Application
#     app = QApplication(sys.argv)
#     # Create and show the form
#     app_main_window = ChooseTopicWidget()
#     # Run the main Qt loop
#     sys.exit(app.exec_())

