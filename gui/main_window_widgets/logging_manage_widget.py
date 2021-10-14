from PyQt5.QtWidgets import *

from gui.logging_task_widgets import logging_setup_widget, get_topic_list_widget, logging_start_widget,\
    logging_process_display_widget, logging_finish_widget
from gui.widgets_indexes import LoggerWidgetIndexes


class LoggingManageWidget(QWidget):
    """
    Widget to control switching between logging processes widgets:
            1. Widget to get list of accessible topic list - choose_topic_list_widget
            2. Widget to choose topics to log their data - setup_logging_widget
            3. Widget to choose directory to save topics data and start logging process - logging_start_widget
            4. Widget to control logging process: pause, play and stop - logging_process_display_widget
            5. Final widget to quit app or go to main menu - logging_finished_widget
    """
    def __init__(self, main_app_object):
        """
        :param main_app_object:  variable with main application object
        """
        super(LoggingManageWidget, self).__init__()
        self.current_widget_enum = LoggerWidgetIndexes.CHOOSE_TOPIC_LAYOUT
        self.choose_topic_list_widget = get_topic_list_widget.GetTopicListWidget(main_app_object, self)
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
        # self.choose_topic_list_widget.logging_start_layout = self.log_manage_widget_layout
        self.choose_topic_list_widget.setup_widget_fill_table_func = self.setup_logging_widget.fill_table

        # self.setup_logging_widget.logging_start_widget_index = self.current_widget_enum
        # self.setup_logging_widget.logging_start_layout = self.log_manage_widget_layout

        # self.logging_start_widget.selected_topic_list = self.setup_logging_widget.selected_topics

        self.setLayout(self.log_manage_widget_layout)

    # Functions to switch between current widget's layouts and perform data exchange if necessary:
    def go_to_get_topic_list_widget(self):
        # set new layout for current widget
        self.log_manage_widget_layout.setCurrentIndex(LoggerWidgetIndexes.CHOOSE_TOPIC_LAYOUT.value)

    def go_to_logging_setup_widget(self):
        # set new layout for current widget
        self.log_manage_widget_layout.setCurrentIndex(LoggerWidgetIndexes.SETUP_LOGGING_LAYOUT.value)

    def go_to_logging_start_widget(self):
        # pass to logging start widget list with selected topic
        self.logging_start_widget.selected_topic_list = self.setup_logging_widget.selected_topics
        # and display it in QPlainTextEdit widget
        self.logging_start_widget.display_selected_topic_list()
        # set new layout for current widget
        self.log_manage_widget_layout.setCurrentIndex(LoggerWidgetIndexes.START_LOGGING_LAYOUT.value)

    def go_to_logging_process_display_widget(self):
        # display log store directory path
        self.logging_process_display_widget.log_save_directory_display.setPlainText(self.logging_start_widget.log_save_directory)
        # pass to logging process widget list of dictionaries with info about selected topics and directory to save log files
        self.logging_process_display_widget.selected_topic_list = self.logging_start_widget.selected_topic_list
        self.logging_process_display_widget.directory_to_save_logs = self.logging_start_widget.log_save_directory
        # start logging process
        self.logging_process_display_widget.run_logging_process()
        # set new layout for current widget
        self.log_manage_widget_layout.setCurrentIndex(LoggerWidgetIndexes.LOGGING_PROCESS_DISPLAY_LAYOUT.value)

    def go_to_logging_finish_widget(self):
        # display in new widget path to log store folder
        self.logging_finished_widget.log_save_directory_display.setPlainText(self.logging_start_widget.log_save_directory)
        # set new layout for current widget
        self.log_manage_widget_layout.setCurrentIndex(LoggerWidgetIndexes.LOGGING_FINISH_LAYOUT.value)

