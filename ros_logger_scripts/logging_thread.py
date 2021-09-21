from PyQt5.QtCore import *
from PyQt5 import QtCore
from ros_logger_scripts import run_ros_logger


class RunLogging(QObject):
    running = False

    # определяется сигнал, который будет возвращать вывод потока
    # logging_process_signal = pyqtSignal(bool)

    def __init__(self, logger):
        super(RunLogging, self).__init__()
        # self.config = cfg
        # self.log_file_store_dir = dir_to_save
        self.logger = logger

    def start_logging_process(self):
        self.logger.run()
        # run_ros_logger.run(self.config, self.log_file_store_dir)
        # self.logging_process_signal.emit(True)


class StartLoggingThread(QObject):
    thread_done_mark_signal = pyqtSignal(list)

    def __init__(self, logger):
        super(StartLoggingThread, self).__init__()
        self.thread_done_mark = False
        # self.config = cfg
        # self.log_file_store_dir = log_dir
        self.logger = logger
        # print('STartThread object created')
        self.start_thread()

    def start_thread(self):
        self.logging_thread = QThread(parent=self)
        self.working_process_object = RunLogging(self.logger)
        self.working_process_object.moveToThread(self.logging_thread)
        # self.working_process_object.logging_process_signal.connect(self.thread_done)
        self.logging_thread.started.connect(self.working_process_object.start_logging_process)
        self.logging_thread.start()

    @QtCore.pyqtSlot(bool)
    def thread_done(self, thread_done_signal):
        print(thread_done_signal)
