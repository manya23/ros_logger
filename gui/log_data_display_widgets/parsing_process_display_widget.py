import time
import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from ros_logger_scripts import parsing_thread


class ParsingDisplayWidget(QWidget):
    def __init__(self, log_display_manage_widget_object):
        super().__init__()
        self.log_display_manage_widget_object = log_display_manage_widget_object
        self.log_directory_path = list()
        self.topic_from_dir_dict = list()
        self.msg_ts_list = list()
        self.__init_widget()

    def __init_widget(self):

        self.common_ts_label = QLabel('Установаите временной диапазон, в рамках которого будет сформирован отчет. ')
        self.max_ts_label = QLabel('Конечное время: ')
        self.max_ts_slider = QSlider(Qt.Horizontal, self)
        self.max_ts_slider.setGeometry(30, 40, 300, 30)
        self.max_ts_slider.valueChanged[int].connect(self.__change_max_value)

        self.min_ts_label = QLabel('Начальное время: ')
        self.min_ts_slider = QSlider(Qt.Horizontal, self)
        self.min_ts_slider.setGeometry(30, 70, 300, 30)
        self.min_ts_slider.valueChanged[int].connect(self.__change_min_value)

        # задание горизонтального layout для отображения временного диапазона
        ts_display_layout = QHBoxLayout()
        min_label = QLabel('Отчет будет собран по данным, записанным с ')
        max_label = QLabel('до ')
        self.min_ts_display = QLineEdit()
        self.max_ts_display = QLineEdit()
        ts_display_layout.addWidget(min_label)
        ts_display_layout.addWidget(self.min_ts_display)
        ts_display_layout.addWidget(max_label)
        ts_display_layout.addWidget(self.max_ts_display)

        # Create the display widget
        self.process_display = QPlainTextEdit()
        # Set some display's properties
        self.process_display.setFixedWidth(800)
        # self.process_display.setAlignment(Qt.AlignCenter)
        self.process_display.setReadOnly(True)

        self.start_parsing_button = QPushButton('Start parsing')
        self.start_parsing_button.clicked.connect(self.run_parsing)

        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.go_to_next_widget)
        self.next_button.setEnabled(False)

        manage_buttons_layout = QHBoxLayout()
        manage_buttons_layout.addWidget(self.start_parsing_button, alignment=Qt.AlignCenter)
        manage_buttons_layout.addWidget(self.next_button, alignment=Qt.AlignRight)

        self.report_collect_widget_layout = QVBoxLayout()
        self.report_collect_widget_layout.addWidget(self.common_ts_label)
        self.report_collect_widget_layout.addWidget(self.min_ts_label)
        self.report_collect_widget_layout.addWidget(self.min_ts_slider)
        self.report_collect_widget_layout.addWidget(self.max_ts_label)
        self.report_collect_widget_layout.addWidget(self.max_ts_slider)
        self.report_collect_widget_layout.addLayout(ts_display_layout)
        self.report_collect_widget_layout.addWidget(self.process_display)
        self.report_collect_widget_layout.addLayout(manage_buttons_layout)

        self.setLayout(self.report_collect_widget_layout)

    def init_slider_range(self):
        self.max_ts_slider.setMinimum(1)
        self.max_ts_slider.setMaximum(len(self.msg_ts_list) - 1)
        self.max_ts_slider.setValue(len(self.msg_ts_list) - 1)
        self.min_ts_slider.setMinimum(0)
        self.min_ts_slider.setMaximum(len(self.msg_ts_list) - 1)
        self.min_ts_slider.setValue(0)

        min_timestamp = str(time.strftime("%H:%M:%S", time.localtime(self.msg_ts_list[0])))
        max_timestamp = str(time.strftime("%H:%M:%S", time.localtime(self.msg_ts_list[-1])))
        self.min_ts_display.setText(min_timestamp)
        self.max_ts_display.setText(max_timestamp)


    #
    def __change_min_value(self, value):
        print(self.msg_ts_list[value], ' and its index: ', value)
        msg_timestamp = str(time.strftime("%H:%M:%S", time.localtime(self.msg_ts_list[value])))
        self.min_ts_display.setText(msg_timestamp)

    #
    def __change_max_value(self, value):
        print(self.msg_ts_list[value])
        msg_timestamp = str(time.strftime("%H:%M:%S", time.localtime(self.msg_ts_list[value])))
        self.max_ts_display.setText(msg_timestamp)

    def run_parsing(self):
        start_time = float(self.msg_ts_list[self.min_ts_slider.value()])
        end_time = float(self.msg_ts_list[self.max_ts_slider.value()])

        self.start_parsing_button.setEnabled(False)
        self.parsing_process_object = parsing_thread.StartThread(self.topic_from_dir_dict, self.log_directory_path,
                                                                 self.next_button, self.process_display,
                                                                 start_time, end_time)


    def go_to_next_widget(self):
        self.process_display.setPlainText('')
        self.start_parsing_button.setEnabled(True)
        self.next_button.setEnabled(False)
        self.log_display_manage_widget_object.go_to_plot_setup_layout()