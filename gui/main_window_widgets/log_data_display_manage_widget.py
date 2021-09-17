from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from gui.widgets_indexes import DataDisplayWidgetIndexes
from gui.log_data_display_widgets import get_display_data_widget, plot_setup_widget


class LogDataDisplayWidget(QWidget):
    def __init__(self, main_app_object):
        super(LogDataDisplayWidget, self).__init__()
        self.get_display_data_widget = get_display_data_widget.GetDataDisplayWidget(main_app_object, self)
        self.plot_setup_widget = plot_setup_widget.PlotSetupWidget(self)
        self.__init_widget()

    def __init_widget(self):
        self.log_data_display_layout = QStackedLayout()
        self.log_data_display_layout.addWidget(self.get_display_data_widget)
        self.log_data_display_layout.addWidget(self.plot_setup_widget)

        self.setLayout(self.log_data_display_layout)

    def go_to_get_display_data_layout(self):
        self.log_data_display_layout.setCurrentIndex(DataDisplayWidgetIndexes.GET_DISPLAY_LAYOUT.value)

    def go_to_plot_setup_layout(self):
        log_data_directory = self.get_display_data_widget.log_data_directory
        self.log_data_display_layout.setCurrentIndex(DataDisplayWidgetIndexes.PLOT_SETUP_LAYOUT.value)
