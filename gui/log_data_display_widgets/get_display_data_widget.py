from PyQt5.QtWidgets import *

from gui.dialog_windows import choose_directory_dialog
from gui.widgets_indexes import WidgetIndexes
from gui.windows_parameters_description import plain_text_edit_wights
from ros_logger_scripts.data_display_modules import ros_log_parser


class GetDataDisplayWidget(QWidget):
    """
    Widget to choose directory contained log files
    """
    def __init__(self, main_app_object, log_display_manage_widget_object):
        """

        :param main_app_object: variable with main application object
        :param log_display_manage_widget_object: variable with logging process widgets manager object
        """
        super(GetDataDisplayWidget, self).__init__()
        self.main_app_object = main_app_object
        self.log_display_manage_widget_object = log_display_manage_widget_object
        self.log_data_directory = str()
        self.__init_widget()

    def __init_widget(self):
        widget_info_label = QLabel('Choose log file directory')

        self.log_data_directory_display = QPlainTextEdit(self.log_data_directory)
        self.log_data_directory_display.setFixedHeight(30)
        self.log_data_directory_display.setReadOnly(False)

        self.choose_dir_button = QPushButton('Choose directory')
        self.choose_dir_button.clicked.connect(self.get_log_dir_path)

        log_directory_activity_layout = QHBoxLayout()
        log_directory_activity_layout.addWidget(self.log_data_directory_display)
        log_directory_activity_layout.addWidget(self.choose_dir_button)

        parsed_log_info_label = QLabel('Selected directories contain next messages types')

        self.topic_msg_display = QPlainTextEdit('')
        self.topic_msg_display.setFixedWidth(plain_text_edit_wights)


        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.go_to_choose_activity_window)

        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.go_to_next_widget)

        back_next_buttons_layout = QHBoxLayout()
        back_next_buttons_layout.addWidget(self.back_button)
        back_next_buttons_layout.addWidget(self.next_button)

        self.get_data_display_layout = QVBoxLayout()
        self.get_data_display_layout.addWidget(widget_info_label)
        self.get_data_display_layout.addLayout(log_directory_activity_layout)
        self.get_data_display_layout.addWidget(parsed_log_info_label)
        self.get_data_display_layout.addWidget(self.topic_msg_display)
        self.get_data_display_layout.addLayout(back_next_buttons_layout)

        self.setLayout(self.get_data_display_layout)

    def get_log_dir_path(self):
        """
        Opens dialog window to choose directory and displays it in PlainText widget.
        :return: nothing
        """
        self.log_data_directory = choose_directory_dialog.choose_directory()
        self.log_data_directory_display.setPlainText(self.log_data_directory)
        # Распарсить только типы сообщений и в соответствии с ними вывести список с названием топика, типом сообщений в нем,
        # и полями этих сообщений
        try:
            self.topic_from_dir_dict = ros_log_parser.get_all_topic_msg_type_pair(self.log_data_directory)
            i = 1
            for topic_name, topic_type in self.topic_from_dir_dict.items():
                self.topic_msg_display.appendPlainText('{num}. Topic "{topic}" with messages type: "{type}"'.format(num=i,
                                                                                                          topic=topic_name,
                                                                                                          type=topic_type))
                i += 1
        except:
            self.topic_msg_display.setPlainText('Some trouble with \'{dir}\'. No such directory.'.format(dir=self.log_data_directory))

    def go_to_choose_activity_window(self):
        """
        Resets all widgets from window to default state and sets Choose Activity widget
        :return: nothing
        """
        self.log_data_directory_display.setPlainText('')
        self.topic_msg_display.setPlainText('')
        self.main_app_object.set_current_main_window_widget(WidgetIndexes.CHOOSE_ACTIVITY_WIDGET)

    def go_to_next_widget(self):
        """
        Resets all widgets from window to default state and call for parsing widget settings function
        :return: nothing
        """
        self.log_display_manage_widget_object.go_to_parsing_display_layout()
        self.log_data_directory_display.setPlainText('')
        self.topic_msg_display.setPlainText('')


