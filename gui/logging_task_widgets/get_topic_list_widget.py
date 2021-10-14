from PyQt5.QtWidgets import *

from gui.dialog_windows import choose_file_dialog
import ros_logger_gui
# from gui.main_window_widgets import logging_manage_widget
from ros_logger_scripts.logging_modules import get_ros_topic_list


class GetTopicListWidget(QWidget):
    """
    Widget with functional to get list of topics to log data that published there in two ways:
            1. Choose config file with info about topic: its name, type of messages published there, its qos
            2. Scan accessible topics and log data published there
    """
    def __init__(self, main_app_object, logging_manage_object):
        """
        :param main_app_object:  variable with main application object
        :param logging_manage_object: variable with logging process widgets manager object
        """
        super(GetTopicListWidget, self).__init__()
        self.main_app_object = main_app_object
        self.logging_manage_object = logging_manage_object
        self.setup_widget_fill_table_func = None

        self.__init_widget()

    def __init_widget(self):
        widget_info_label = QLabel('Choose path to config file with topics that have to be subscribed. Or choose '
                                        'to listen for topics that are available now')
        # Choose config file with description of those topics that has to be listened or choose from accessible now
        self.choose_config_file_button = QPushButton('Choose file')
        self.choose_config_file_button.clicked.connect(self.__choose_config_file)

        self.display_visible_topics_button = QPushButton('Display accessible topics')
        self.display_visible_topics_button.clicked.connect(self.__display_visible_topics)

        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.__go_to_previous_widget)

        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.addWidget(self.choose_config_file_button)
        action_buttons_layout.addWidget(self.display_visible_topics_button)

        log_setup_widget_layout = QVBoxLayout()
        log_setup_widget_layout.addWidget(widget_info_label)
        log_setup_widget_layout.addLayout(action_buttons_layout)
        log_setup_widget_layout.addWidget(self.back_button)

        self.setLayout(log_setup_widget_layout)

    def __choose_config_file(self):
        # when 'choose config file' button pressed opens file dialog window to choose config file
        self.config_file_path = choose_file_dialog.choose_file()
        try:
            self.setup_widget_fill_table_func(self.config_file_path)
        except:
            pass
        # and go to next widget
        self.logging_manage_object.go_to_logging_setup_widget()

    def __display_visible_topics(self):
        # get accessible topic list
        self.topic_info_list = get_ros_topic_list.get_topic_list_via_nodes()
        try:
            self.setup_widget_fill_table_func(self.topic_info_list)
        except:
            pass
        # and go to next widget
        self.logging_manage_object.go_to_logging_setup_widget()

    def __go_to_previous_widget(self):
        widget_index = ros_logger_gui.WidgetIndexes.CHOOSE_ACTIVITY_WIDGET
        self.main_app_object.set_current_main_window_widget(widget_index)
