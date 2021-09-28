from PyQt5.QtCore import *
from PyQt5 import QtCore
from ros_logger_scripts import ros_log_parser


class ThreadWorkTask(QObject):
    running = False

    # определяется сигнал, который будет возвращать вывод потока
    parsing_process_signal = pyqtSignal(list)

    def __init__(self, log_directory_path, topic_name):
        super(ThreadWorkTask, self).__init__()
        self.log_directory_path = log_directory_path
        self.topic_name = topic_name

    def start_parsing_process(self):
        topic_msgs = ros_log_parser.get_all_topic_msgs(list([self.log_directory_path]), self.topic_name)
        self.thread_result = [self.topic_name, topic_msgs]

        self.parsing_process_signal.emit([self.topic_name, True])


class StartThread(QObject):
    thread_done_mark_signal = pyqtSignal(str)

    def __init__(self, topic_from_dir_dict, log_directory_path, next_button, process_display_widget):
        super(StartThread, self).__init__()
        self.topic_from_dir_dict = topic_from_dir_dict
        self.log_directory_path = log_directory_path
        self.next_button_from_parsing_display_widget = next_button
        self.process_display_widget = process_display_widget

        self.run_thread_counter = int()
        self.done_thread_counter = int()

        self.thread_work_object_list = list()
        self.thread_object_list = list()
        self.parsed_msg_dict = dict()

        self.__start_parsing()

    def __start_parsing(self):
        for topic_name in self.topic_from_dir_dict:
            self.run_thread_counter += 1
            self.process_display_widget.appendPlainText(str(self.run_thread_counter) + '. ' + topic_name + ' in parsing process')
            self.__start_thread(self.log_directory_path, topic_name)

    def __start_thread(self, log_directory_path, topic_name):
        parsing_thread = QThread(parent=self)
        self.thread_object_list.append(parsing_thread)
        working_process_object = ThreadWorkTask(log_directory_path, topic_name)
        self.thread_work_object_list.append(working_process_object)
        working_process_object.moveToThread(parsing_thread)
        working_process_object.parsing_process_signal.connect(self.thread_done)
        parsing_thread.started.connect(working_process_object.start_parsing_process)
        parsing_thread.start()

    @QtCore.pyqtSlot(list)
    def thread_done(self, thread_done_signal):
        if thread_done_signal[1]:
            topic_name = thread_done_signal[0]
            self.done_thread_counter += 1
            self.process_display_widget.appendPlainText(str(self.done_thread_counter) + '. ' + topic_name + '  had parsed')

        # self.thread_done_mark_signal.emit(True)
        if self.done_thread_counter == len(self.topic_from_dir_dict):
            for thread_object in self.thread_work_object_list:
                self.parsed_msg_dict.update({thread_object.thread_result[0]: thread_object.thread_result[1]})
            self.process_display_widget.appendPlainText('Parsing is done')
            self.next_button_from_parsing_display_widget.setEnabled(True)

    def get_parsed_msg(self):
        return self.parsed_msg_dict

    def destroy_threads(self):
        for thread in self.thread_object_list:
            thread.quit()
