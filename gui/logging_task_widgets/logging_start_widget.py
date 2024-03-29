from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

from gui.dialog_windows import choose_directory_dialog
# import module with window params
# TODO: put all params to gui.windows_parameters_description
from gui.windows_parameters_description import plain_text_edit_wights, plain_text_edit_height


class LoggingStartWidget(QWidget):
    """
    The widget displays selected topic list. Presents functional to choose directory to save log files and button
    to start logging process.
    """
    def __init__(self, logging_manage_object):
        """
        selected_topic_list - list with dictionaries that contains info about topic that had to be listened
        log_save_directory - by default is current folder path. But can be changed by user
        :param logging_manage_object: variable with logging process widgets manager object
        """
        super(LoggingStartWidget, self).__init__()
        self.logging_manage_object = logging_manage_object
        self.selected_topic_list = list()
        self.log_save_directory = os.path.dirname(os.path.realpath(__file__))
        self.__init_widget()

    def __init_widget(self):
        widget_info_label = QLabel('Following topics will be listened to log messages that published there')
        choose_dir_info_label = QLabel('Choose directory to save log files')
        start_logging_info_label = QLabel('Now you can start write down messages from selected topics to log files')

        # Create the display widget
        self.topic_list_display = QPlainTextEdit()
        # Set some display's properties
        self.topic_list_display.setFixedWidth(plain_text_edit_wights)
        self.topic_list_display.setFixedHeight(plain_text_edit_height)
        self.topic_list_display.setReadOnly(True)

        self.log_save_directory_display = QPlainTextEdit(self.log_save_directory)
        self.log_save_directory_display.setFixedHeight(30)
        self.log_save_directory_display.setReadOnly(False)

        self.choose_dir_button = QPushButton('change directory')
        self.choose_dir_button.clicked.connect(self.__choose_directory_to_store_logs)

        self.get_log_save_dir_layout = QHBoxLayout()
        self.get_log_save_dir_layout.addWidget(self.log_save_directory_display)
        self.get_log_save_dir_layout.addWidget(self.choose_dir_button)

        self.next_button = QPushButton('Start')
        self.next_button.clicked.connect(self.__start_logging_process)

        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.__go_to_previous_widget)

        self.widget_manage_buttons_layout = QHBoxLayout()
        self.widget_manage_buttons_layout.addWidget(self.back_button)
        self.widget_manage_buttons_layout.addStretch(1)
        self.widget_manage_buttons_layout.addWidget(self.next_button)

        self.log_start_widget_layout = QVBoxLayout()
        self.log_start_widget_layout.addWidget(widget_info_label)
        self.log_start_widget_layout.addWidget(self.topic_list_display, alignment=Qt.AlignCenter)
        self.log_start_widget_layout.addWidget(choose_dir_info_label)
        self.log_start_widget_layout.addLayout(self.get_log_save_dir_layout)
        self.log_start_widget_layout.addStretch(1)
        self.log_start_widget_layout.addWidget(start_logging_info_label)
        self.log_start_widget_layout.addLayout(self.widget_manage_buttons_layout)

        self.setLayout(self.log_start_widget_layout)

    def __choose_directory_to_store_logs(self):
        self.log_save_directory = choose_directory_dialog.choose_directory()
        self.log_save_directory_display.setPlainText(self.log_save_directory)

    def __go_to_previous_widget(self):
        self.topic_list_display.setPlainText('')
        self.logging_manage_object.go_to_logging_setup_widget()

    def __start_logging_process(self):
        self.topic_list_display.setPlainText('')
        self.logging_manage_object.go_to_logging_process_display_widget()

    def display_selected_topic_list(self):
        """
        display in QPlainText widget topics selected on previous step
        :return: nothing
        """
        for i, topic in enumerate(self.selected_topic_list):
            self.topic_list_display.appendPlainText((str(i+1) + '. ' + topic["name"]))

        if len(self.selected_topic_list) < 1:
            self.next_button.setEnabled(True)
            self.topic_list_display.appendPlainText('You\'ve been selected no one topic from topic list. Please, '
                                                    'come back to previous stage and choose at least one')

    # method to get selected directory path
    def get_log_directory(self):
        return self.log_save_directory
