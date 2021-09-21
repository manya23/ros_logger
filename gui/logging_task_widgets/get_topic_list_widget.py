from PyQt5.QtWidgets import *

from gui.dialog_windows import choose_file_dialog
import ros_logger_gui
# from gui.main_window_widgets import logging_manage_widget
from gui.widgets_indexes import LoggerWidgetIndexes
from ros_logger_scripts import get_ros_topic_list


class GetTopicListWidget(QWidget):
    def __init__(self, main_app_object):
        super(GetTopicListWidget, self).__init__()
        self.main_app_object = main_app_object

        self.logging_start_widget_index = LoggerWidgetIndexes.NONE_WIDGET
        self.logging_start_layout = QStackedLayout()
        self.setup_widget_fill_table_func = None

        self.__init_widget()

    def __init_widget(self):
        self.widget_info_label = QLabel('Choose path to config file with topics that have to be subscribed. Or choose '
                                        'to listen for topics that are available now')
        # Choose config file with description of those topics that has to be listened or choose from accessible now
        self.choose_config_file_button = QPushButton('Choose file')
        self.choose_config_file_button.clicked.connect(self.choose_config_file)

        self.display_visible_topics_button = QPushButton('Display accessible topics')
        self.display_visible_topics_button.clicked.connect(self.display_visible_topics)
        # self.display_visible_topics_button.setEnabled(False)

        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.go_to_previous_widget)

        self.action_buttons_layout = QHBoxLayout()
        self.action_buttons_layout.addWidget(self.choose_config_file_button)
        self.action_buttons_layout.addWidget(self.display_visible_topics_button)

        self.log_setup_widget_layout = QVBoxLayout()
        self.log_setup_widget_layout.addWidget(self.widget_info_label)
        self.log_setup_widget_layout.addLayout(self.action_buttons_layout)
        self.log_setup_widget_layout.addWidget(self.back_button)

        self.setLayout(self.log_setup_widget_layout)

    def choose_config_file(self):
        # call dialog window to choose directory path and save path to variable
        self.config_file_path = choose_file_dialog.choose_file()
        try:
            self.setup_widget_fill_table_func(self.config_file_path)
        except:
            pass
        self.logging_start_widget_index = LoggerWidgetIndexes.SETUP_LOGGING_LAYOUT
        self.logging_start_layout.setCurrentIndex(self.logging_start_widget_index.value)

    def display_visible_topics(self):
        self.topic_info_list = get_ros_topic_list.get_topic_list_via_nodes()
        print('CONFIG FROM LIST',self.topic_info_list)
        try:
            self.setup_widget_fill_table_func(self.topic_info_list)
        except:
            pass
        self.logging_start_widget_index = LoggerWidgetIndexes.SETUP_LOGGING_LAYOUT
        self.logging_start_layout.setCurrentIndex(self.logging_start_widget_index.value)
        print('im listening')

    def go_to_previous_widget(self):
        widget_index = ros_logger_gui.WidgetIndexes.CHOOSE_ACTIVITY_WIDGET
        self.main_app_object.set_current_main_window_widget(widget_index)
