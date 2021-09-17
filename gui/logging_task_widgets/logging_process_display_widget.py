from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from ros_logger_scripts import run_ros_logger

class LoggingProcessDisplayWidget(QWidget):
    def __init__(self, logging_manage_object):
        super(LoggingProcessDisplayWidget, self).__init__()
        self.logging_manage_object = logging_manage_object
        self.directory_to_save_logs = str()
        self.selected_topic_list = list()
        self.__init_widget()

    def __init_widget(self):
        widget_info_label = QLabel('Recording log files to: ')

        self.log_save_directory_display = QPlainTextEdit('')
        self.log_save_directory_display.setFixedHeight(30)
        self.log_save_directory_display.setReadOnly(True)

        self.pause_button = QPushButton('Pause')
        self.pause_button.clicked.connect(self.pause_log_recording)
        self.play_button = QPushButton('Play')
        self.play_button.clicked.connect(self.play_log_recording)
        self.play_button.setEnabled(False)
        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_log_recording)

        self.log_process_control_buttons_layout = QHBoxLayout()
        self.log_process_control_buttons_layout.addWidget(self.pause_button)
        self.log_process_control_buttons_layout.addWidget(self.play_button)
        self.log_process_control_buttons_layout.addWidget(self.stop_button)

        self.log_process_display_layout = QVBoxLayout()
        self.log_process_display_layout.addWidget(widget_info_label)
        self.log_process_display_layout.addWidget(self.log_save_directory_display)
        self.log_process_display_layout.addStretch(1)
        self.log_process_display_layout.addLayout(self.log_process_control_buttons_layout)

        self.setLayout(self.log_process_display_layout)

    def pause_log_recording(self):
        self.play_button.setEnabled(True)
        print('pause')

    def play_log_recording(self):
        print('play')
        self.play_button.setEnabled(False)

    def stop_log_recording(self):
        self.logging_manage_object.go_to_logging_finish_widget()
        print('stop')

    def run_logging_process(self):
        run_ros_logger.run(self.selected_topic_list, self.directory_to_save_logs)

