import sys

from PyQt5.QtWidgets import *
from gui.windows_parameters_description import main_window_wight, main_window_height

from gui.main_window_widgets import choose_activity_widget, logging_manage_widget, log_data_display_manage_widget
from gui.widgets_indexes import WidgetIndexes


class MainApp (QMainWindow):
    def __init__(self, app_main_process):
        super().__init__()
        self.app_main_process = app_main_process
        # create objects of 3 main widgets
        self.choose_activity_widget = choose_activity_widget.ChooseActivityWidget()
        # self.log_writing_widget = log_writing_widget.LogWritingWidget()
        self.logging_start_widget = logging_manage_widget.LoggingManageWidget(self)
        # set current displayed widget
        self.log_data_display_widget = log_data_display_manage_widget.LogDataDisplayWidget(self)
        self.current_widget_enum = WidgetIndexes.CHOOSE_ACTIVITY_WIDGET

        self.init_main_widget()

    def init_main_widget(self):
        """
        Формирование основного окна приложения
        :return:
        """
        main_widget = QWidget()
        self.setGeometry(0, 0, main_window_wight, main_window_height)
        self.center()

        # setup main layout
        main_layout = QVBoxLayout()

        self.switch_layout = QStackedLayout()
        self.switch_layout.addWidget(self.choose_activity_widget)
        self.switch_layout.addWidget(self.logging_start_widget)
        self.switch_layout.addWidget(self.log_data_display_widget)

        main_layout.addLayout(self.switch_layout)
        main_widget.setLayout(main_layout)

        # fill custom widget objects parameters
        self.choose_activity_widget.current_widget_index = self.current_widget_enum
        self.choose_activity_widget.main_window_layout = self.switch_layout

        self.setWindowTitle('ROS messages logger')
        self.setCentralWidget(main_widget)
        self.show()

    def set_current_main_window_widget(self, desired_widget_index):
        self.switch_layout.setCurrentIndex(desired_widget_index.value)

    def quit_app(self):
        self.app_main_process.quit_app()

    # put window to the middle of screen
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class RosLoggerApplication:
    def __init__(self):
        # Create the Qt Application
        self.app = QApplication(sys.argv)
        # Create and show the form
        self.app_main_window = MainApp(self)
        # Run the main Qt loop
        sys.exit(self.app.exec_())

    def quit_app(self):
        self.app.quit()

if __name__ == '__main__':
    # Create the Ros Logger Application
    app = RosLoggerApplication()