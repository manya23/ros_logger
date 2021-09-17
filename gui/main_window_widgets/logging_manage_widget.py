from PyQt5.QtWidgets import *
from enum import Enum

from gui.logging_task_widgets import logging_setup_widget, get_topic_list_widget, logging_start_widget,\
    logging_process_display_widget, logging_finish_widget
from gui.widgets_indexes import LoggerWidgetIndexes


class LoggingManageWidget(QWidget):
    def __init__(self, main_app_object):
        super(LoggingManageWidget, self).__init__()
        self.current_widget_enum = LoggerWidgetIndexes.CHOOSE_TOPIC_LAYOUT
        self.choose_topic_list_widget = get_topic_list_widget.GetTopicListWidget(main_app_object)
        self.setup_logging_widget = logging_setup_widget.LoggingSetupWidget(self)
        self.logging_start_widget = logging_start_widget.LoggingStartWidget(self)
        self.logging_process_display_widget = logging_process_display_widget.LoggingProcessDisplayWidget(self)
        self.logging_finished_widget = logging_finish_widget.LoggingProcessDisplayWidget(main_app_object, self)
        self.__init_widget()

    def __init_widget(self):

        self.log_manage_widget_layout = QStackedLayout()
        self.log_manage_widget_layout.addWidget(self.choose_topic_list_widget)
        self.log_manage_widget_layout.addWidget(self.setup_logging_widget)
        self.log_manage_widget_layout.addWidget(self.logging_start_widget)
        self.log_manage_widget_layout.addWidget(self.logging_process_display_widget)
        self.log_manage_widget_layout.addWidget(self.logging_finished_widget)

        # fill custom widget objects parameters
        self.choose_topic_list_widget.logging_start_widget_index = self.current_widget_enum
        self.choose_topic_list_widget.logging_start_layout = self.log_manage_widget_layout
        self.choose_topic_list_widget.setup_widget_fill_table_func = self.setup_logging_widget.fill_table

        self.setup_logging_widget.logging_start_widget_index = self.current_widget_enum
        self.setup_logging_widget.logging_start_layout = self.log_manage_widget_layout

        # self.logging_start_widget.selected_topic_list = self.setup_logging_widget.selected_topics

        self.setLayout(self.log_manage_widget_layout)

    def go_to_get_topic_list_widget(self, set_data=False):
        self.log_manage_widget_layout.setCurrentIndex(LoggerWidgetIndexes.CHOOSE_TOPIC_LAYOUT.value)

    def go_to_logging_setup_widget(self, set_data=False):
        self.log_manage_widget_layout.setCurrentIndex(LoggerWidgetIndexes.SETUP_LOGGING_LAYOUT.value)

    def go_to_logging_start_widget(self, set_data=False):
        print('data is', set_data)
        self.logging_start_widget.selected_topic_list = set_data
        self.logging_start_widget.display_selected_topic_list()
        self.log_manage_widget_layout.setCurrentIndex(LoggerWidgetIndexes.START_LOGGING_LAYOUT.value)

    def go_to_logging_process_display_widget(self, set_data=False):
        print('im go to logging process')
        self.logging_process_display_widget.log_save_directory_display.setPlainText(self.logging_start_widget.log_save_directory)
        self.logging_process_display_widget.selected_topic_list = self.logging_start_widget.selected_topic_list
        self.log_manage_widget_layout.setCurrentIndex(LoggerWidgetIndexes.LOGGING_PROCESS_DISPLAY_LAYOUT.value)

    def go_to_logging_finish_widget(self, set_data=False):
        self.logging_finished_widget.log_save_directory_display.setPlainText(self.logging_start_widget.log_save_directory)
        self.log_manage_widget_layout.setCurrentIndex(LoggerWidgetIndexes.LOGGING_FINISH_LAYOUT.value)

