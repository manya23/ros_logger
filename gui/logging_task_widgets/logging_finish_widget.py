from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# import ros_logger_gui
from gui.widgets_indexes import WidgetIndexes


class LoggingProcessDisplayWidget(QWidget):
    def __init__(self, main_app_object, logging_manage_object):
        super(LoggingProcessDisplayWidget, self).__init__()
        self.main_app_object = main_app_object
        self.logging_manage_object = logging_manage_object
        self.log_dir_path = list()
        self.__init_widget()

    def __init_widget(self):
        widget_info_label = QLabel('Recording of log files is complete. Log files saved to: ')

        self.log_save_directory_display = QPlainTextEdit('')
        self.log_save_directory_display.setFixedHeight(30)
        self.log_save_directory_display.setReadOnly(True)

        self.back_button = QPushButton('Back to start menu')
        self.back_button.clicked.connect(self.go_to_choose_activity_widget)

        self.quit_button = QPushButton('Quit')
        self.quit_button.clicked.connect(self.quit_app)

        manage_buttons_layout = QHBoxLayout()
        manage_buttons_layout.addWidget(self.quit_button, alignment=Qt.AlignRight)
        manage_buttons_layout.addWidget(self.back_button, alignment=Qt.AlignRight)

        self.log_finish_layout = QVBoxLayout()
        self.log_finish_layout.addWidget(widget_info_label)
        self.log_finish_layout.addWidget(self.log_save_directory_display)
        self.log_finish_layout.addStretch(1)
        self.log_finish_layout.addLayout(manage_buttons_layout)

        self.setLayout(self.log_finish_layout)

    def go_to_choose_activity_widget(self):
        widget_index = WidgetIndexes.CHOOSE_ACTIVITY_WIDGET
        self.main_app_object.set_current_main_window_widget(widget_index)

        self.logging_manage_object.setup_logging_widget.clean_table()
        self.logging_manage_object.go_to_get_topic_list_widget()

    def quit_app(self):
        self.main_app_object.quit_app()