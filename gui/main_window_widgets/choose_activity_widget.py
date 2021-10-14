from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from gui.widgets_indexes import WidgetIndexes


class ChooseActivityWidget(QWidget):
    """
    Widget to switch between two App functions' widgets:
        1. Widget with logging process functional
        2. Widget with log's data display functional
    """
    def __init__(self):
        super(ChooseActivityWidget, self).__init__()
        self.main_window_layout = QStackedLayout()
        self.__init_widget()

    def __init_widget(self):
        self.app_label = QLabel('ROS messages logger')
        self.app_label.setAlignment(Qt.AlignCenter)

        self.widget_info_label = QLabel('Choose what action you want to perform')
        self.widget_info_label.setAlignment(Qt.AlignCenter)

        self.log_writing_menu_button = QPushButton('Open log writing menu')
        self.log_writing_menu_button.clicked.connect(self.open_log_writing_widget)

        self.log_analysis_menu_button = QPushButton('Open log analysis menu')
        self.log_analysis_menu_button.clicked.connect(self.open_log_analysis_widget)

        self.activity_buttons_layout = QHBoxLayout()
        self.activity_buttons_layout.addWidget(self.log_writing_menu_button)
        self.activity_buttons_layout.addWidget(self.log_analysis_menu_button)

        self.choose_activity_widget_layout = QVBoxLayout()
        self.choose_activity_widget_layout.addWidget(self.app_label)
        self.choose_activity_widget_layout.addStretch(1)
        self.choose_activity_widget_layout.addWidget(self.widget_info_label)
        self.choose_activity_widget_layout.addStretch(1)
        self.choose_activity_widget_layout.addLayout(self.activity_buttons_layout)

        self.setLayout(self.choose_activity_widget_layout)

    def open_log_writing_widget(self):
        # set new layout for current widget
        self.main_window_layout.setCurrentIndex(WidgetIndexes.LOG_WRITING_WIDGET.value)

    def open_log_analysis_widget(self):
        # set new layout for current widget
        self.main_window_layout.setCurrentIndex(WidgetIndexes.REPORT_COLLECT_WIDGET.value)
