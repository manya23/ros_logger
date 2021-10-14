from PyQt5.QtWidgets import *

from gui.widgets_indexes import DataDisplayWidgetIndexes
from gui.log_data_display_widgets import get_display_data_widget, parsing_process_display_widget, plot_setup_widget
from ros_logger_scripts.data_display_modules.ros_log_parser import get_all_ts_from_few_topic


class LogDataDisplayWidget(QWidget):
    """
    Widget to control switching between log's data analysis processes widgets:
            1. Widget to select log data store folder - get_display_data_widget
            2. Widget to setup and run log data parsing process - parsing_display_widget
            3. Widget to set and save plots displayed logs data - plot_setup_widget
    """
    def __init__(self, main_app_object):
        """
        :param main_app_object:  variable with main application object
        """
        super(LogDataDisplayWidget, self).__init__()
        self.get_display_data_widget = get_display_data_widget.GetDataDisplayWidget(main_app_object, self)
        self.parsing_display_widget = parsing_process_display_widget.ParsingDisplayWidget(self)
        self.plot_setup_widget = plot_setup_widget.PlotSetupWidget(self)
        self.__init_widget()

    def __init_widget(self):
        self.log_data_display_layout = QStackedLayout()
        self.log_data_display_layout.addWidget(self.get_display_data_widget)
        self.log_data_display_layout.addWidget(self.parsing_display_widget)
        self.log_data_display_layout.addWidget(self.plot_setup_widget)

        self.setLayout(self.log_data_display_layout)

    # Functions to switch between current widget's layouts and perform data exchange if necessary:
    def go_to_get_display_data_layout(self):
        # set new layout for current widget
        self.log_data_display_layout.setCurrentIndex(DataDisplayWidgetIndexes.GET_DISPLAY_LAYOUT.value)

    def go_to_parsing_display_layout(self):
        # get data from previous widget
        log_data_directory = self.get_display_data_widget.log_data_directory
        topic_list = list()
        # form list of log data timestamps to display it on parsing process setup timeline
        for topic_name in self.get_display_data_widget.topic_from_dir_dict:
            topic_list.append(topic_name)
        all_ts_list = get_all_ts_from_few_topic(log_data_directory, topic_list)
        # and put them to object of next widget
        self.parsing_display_widget.log_directory_path = log_data_directory
        self.parsing_display_widget.topic_from_dir_dict = topic_list
        self.parsing_display_widget.msg_ts_list = all_ts_list
        # init slider with timestamp range settings
        self.parsing_display_widget.init_slider_range()
        # set new layout for current widget
        self.log_data_display_layout.setCurrentIndex(DataDisplayWidgetIndexes.PARSING_PROCESS_DISPLAY_LAYOUT.value)

    def go_to_plot_setup_layout(self):
        # get data from previous widget
        self.plot_setup_widget.parsed_topic_w_type_dict = self.get_display_data_widget.topic_from_dir_dict
        self.plot_setup_widget.parsed_topic_w_msgs_dict = self.parsing_display_widget.parsing_process_object.get_parsed_msg()
        self.plot_setup_widget.log_directory_path = self.parsing_display_widget.log_directory_path
        # destroy parsing process threads
        self.parsing_display_widget.parsing_process_object.destroy_threads()
        # set new layout for current widget
        self.log_data_display_layout.setCurrentIndex(DataDisplayWidgetIndexes.PLOT_SETUP_LAYOUT.value)
