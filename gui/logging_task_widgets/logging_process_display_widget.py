from PyQt5.QtWidgets import *

from ros_logger_scripts.logging_modules import run_ros_logger, logging_thread


class LoggingProcessDisplayWidget(QWidget):
    """
    The widget displays info about logging process and has control buttons that allows to stop, pause and play logging
    process.
    """
    def __init__(self, logging_manage_object):
        """
        :param logging_manage_object: variable with logging process widgets manager object
        """
        super(LoggingProcessDisplayWidget, self).__init__()
        self.logging_manage_object = logging_manage_object
        self.directory_to_save_logs = str()
        self.selected_topic_list = list()

        self.pause_pressed = False

        self.__init_widget()

    def __init_widget(self):
        widget_info_label = QLabel('Recording log files to: ')

        self.log_save_directory_display = QPlainTextEdit('')
        self.log_save_directory_display.setFixedHeight(30)
        self.log_save_directory_display.setReadOnly(True)

        self.pause_button = QPushButton('Pause')
        self.pause_button.clicked.connect(self.pause_log_recording)
        self.pause_button.setEnabled(True)
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
        """
        When pause button pressed it stop allowing writing down to file info published in topics
        :return: nothing
        """
        for topic in self.logger.logger.list_topics:
            topic.pause_pressed = True
        self.play_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        print('pause')

    def play_log_recording(self):
        """
        When play button pressed it begin allowing writing down to file info published in topics
        :return: nothing
        """
        for topic in self.logger.logger.list_topics:
            topic.pause_pressed = False
        self.play_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        print('play')

    def stop_log_recording(self):
        """
        Destroys node that listens for topics and destroys threads with logging process running
        :return: nothing
        """
        # TODO: stop running all processes from self.logger object
        # TODO: delete not Qt thread from self.logger object
        self.logger.destroy()
        self.logging_process_object.logging_thread.quit()
        self.logging_manage_object.go_to_logging_finish_widget()
        print('stop')

    def run_logging_process(self):
        """
        Runs "ros_logger_node" to start subscription to all required topics. And runs logger in separate thread
        :return: nothing
        """
        # TODO: define how much threads have to be run for this task
        self.logger = run_ros_logger.LoggerInit(self.selected_topic_list, self.directory_to_save_logs)
        self.logging_process_object = logging_thread.StartLoggingThread(self.logger)

