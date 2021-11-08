from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

import json
from gui.dialog_windows import choose_directory_dialog
from ros_logger_scripts.logging_modules import create_logger_config_file


class LoggingSetupWidget(QWidget):
    """
    The widget displays table with available topics. Data from selected topics will be saved to logs. The widget also
    presents option to save selected topics to new config file.
    """
    def __init__(self, logging_manage_object):
        """
        :param logging_manage_object: variable with logging process widgets manager object
        """
        super(LoggingSetupWidget, self).__init__()
        self.logging_manage_object = logging_manage_object
        self.config_file_path = str()

        self.__init_widget()

    def __init_widget(self):
        # declare main window widgets
        table_info_label = QLabel('Choose topics to start write down messages published there')

        self.empty_config_warning_label = QLabel('Please, check your config file or your ROS environment. There are no topics here.')
        self.empty_config_warning_label.setVisible(False)

        # button to make all checkboxes selected
        self.select_all_button = QPushButton('Select all')
        self.select_all_button.clicked.connect(self.__select_all_checkboxes)
        # self.select_all_button.setVisible(False)

        # button to make all checkboxes unselected
        self.deselect_all_button = QPushButton('Deselect all')
        self.deselect_all_button.clicked.connect(self.__deselect_all_checkboxes)

        self.save_config_info_label = QLabel('You can save checked topics to config file')
        self.save_config_qos_option_info_label = QLabel('Topics will save to config file with default QOS profile: Sensor data')
        self.save_config_button = QPushButton('Save to file')
        self.save_config_button.clicked.connect(self.__save_new_config_file)
        # self.save_config_button.setEnabled(False)

        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.__go_to_logging_process)

        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.__go_to_previous_widget)

        # create table to display topic with checkboxes
        self.default_table_len = 0
        self.topic_list_display_table = QTableWidget(self.default_table_len, 2)
        topic_list_display_table_header = self.topic_list_display_table.horizontalHeader()
        topic_list_display_table_header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        topic_list_display_table_header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

        table_manage_buttons_layout = QHBoxLayout()
        table_manage_buttons_layout.addWidget(self.select_all_button)
        table_manage_buttons_layout.addWidget(self.deselect_all_button)

        widget_manage_buttons_layout = QHBoxLayout()
        widget_manage_buttons_layout.addWidget(self.back_button)
        widget_manage_buttons_layout.addStretch(1)
        widget_manage_buttons_layout.addWidget(self.next_button)

        log_writing_widget_layout = QVBoxLayout()
        log_writing_widget_layout.addWidget(table_info_label)
        log_writing_widget_layout.addWidget(self.topic_list_display_table)
        log_writing_widget_layout.addWidget(self.empty_config_warning_label, alignment=Qt.AlignCenter)
        log_writing_widget_layout.addLayout(table_manage_buttons_layout)
        log_writing_widget_layout.addWidget(self.save_config_info_label)
        log_writing_widget_layout.addWidget(self.save_config_button)
        log_writing_widget_layout.addWidget(self.save_config_qos_option_info_label)
        log_writing_widget_layout.addLayout(widget_manage_buttons_layout)

        self.setLayout(log_writing_widget_layout)

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
        """
        Filling table with checkbox - topic info pairs. Data in table cell is topic description dictionary
        :param config: list with dictionaries that contains topic info (name, messages type, qos)
        :type config: list
        :return:
        """
        self.table_len = int()
        topic_name_list = list()
        # fill table fields with info from config file
        for topic_describe_dict in config:
            # TODO: шо это такое ??
            if topic_describe_dict['name'] in topic_name_list:
                continue
            row_pose = self.topic_list_display_table.rowCount()
            self.topic_list_display_table.insertRow(row_pose)
            table_label = 'Topic ' + '\'' + topic_describe_dict['name'] + '\'' + ' with type ' \
                          + '\'' + topic_describe_dict['type'] + '\''
            self.__add_new_checkbox_point(row_pose, table_label, topic_describe_dict)
            topic_name_list.append(topic_describe_dict['name'])
            self.table_len += 1
        # in case when there are no topic in config data: displays warning and hide all unnecessary widgets
        if self.table_len < 1:
            self.topic_list_display_table.setVisible(False)
            self.empty_config_warning_label.setVisible(True)
            self.select_all_button.setVisible(False)
            self.deselect_all_button.setVisible(False)
            self.save_config_info_label.setVisible(False)
            self.save_config_button.setVisible(False)
            self.save_config_qos_option_info_label.setVisible(False)
            self.next_button.setVisible(False)

    def __get_checked_items(self):
        # gather data from selected table items to list
        self.selected_topics = list()
        for i in range(self.topic_list_display_table.rowCount()):
            current_state = self.topic_list_display_table.item(i, 0).checkState()
            if current_state == Qt.Checked:
                self.selected_topics.append(self.topic_list_display_table.item(i, 1).data(QtCore.Qt.UserRole))

    def __go_to_logging_process(self):
        self.__get_checked_items()
        # set new widget with choosing of directory to save logs start button
        self.logging_manage_object.go_to_logging_start_widget()

    def __go_to_previous_widget(self):
        """
        Set previous widget active. Clean and reset current widget
        :return: nothing
        """
        self.clean_table()
        self.empty_config_warning_label.setVisible(False)
        self.topic_list_display_table.setVisible(True)
        self.select_all_button.setVisible(True)
        self.deselect_all_button.setVisible(True)
        self.save_config_info_label.setVisible(True)
        self.save_config_button.setVisible(True)
        self.save_config_qos_option_info_label.setVisible(True)
        self.next_button.setVisible(True)
        self.logging_manage_object.go_to_get_topic_list_widget()

    def __save_new_config_file(self):
        self.__get_checked_items()
        new_config_file_directory = choose_directory_dialog.choose_directory()
        create_logger_config_file.save_new_config(self.selected_topics, new_config_file_directory)

    def fill_table(self, config_info):
        """
        Manage table filling.
        :param config_info: depend on user's choose, it can be path to .json file or list with dictionaries
        :return:
        """
        if type(config_info) == str:
            # when config info is path to config file, performs loading info from file
            with open(config_info) as json_file:
                config = json.load(json_file)
            self.__fill_topic_list_display_table(config)
        else:
            # in other way just pass config_file variable to fill table
            self.__fill_topic_list_display_table(config_info)

    def clean_table(self):
        # clear table
        for table_row in range(self.table_len, -1, -1):
            self.topic_list_display_table.removeRow(table_row)
