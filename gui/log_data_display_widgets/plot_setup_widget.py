#!/usr/bin/python

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

from gui.windows_parameters_description import plot_preview_wight, plot_preview_height
from gui.dialog_windows import choose_data_to_axis_dialog
from ros_logger_scripts import get_data_from_msg


class PlotSetupWidget(QWidget):
    def __init__(self, log_display_manage_widget_object):
        super(PlotSetupWidget, self).__init__()
        self.log_display_manage_widget_object = log_display_manage_widget_object
        self.html_plot_path = str()
        self.x_axis_data = list()
        self.y_axis_data = list()
        self.parsed_topic_w_type_dict = list()

        self.parsed_topic_w_msgs_dict = dict()
        self.__init_widget()

    def __init_widget(self):
        self.custom_title_field = QPlainTextEdit('Please, enter plot title')
        self.custom_title_field.setFixedHeight(35)

        self.html_plot_view = QWebEngineView()
        self.html_plot_view.setFixedHeight(plot_preview_height)
        self.html_plot_view.setFixedWidth(plot_preview_wight)

        self.choose_x_button = QPushButton('Choose X axis')
        self.choose_x_button.clicked.connect(self.choose_x_axis)
        self.choose_y_button = QPushButton('Choose Y axis')
        self.choose_y_button.clicked.connect(self.choose_y_axis)

        self.choose_one_more_x_button = QPushButton('Choose extra X data')
        self.choose_one_more_x_button.clicked.connect(self.choose_extra_x)
        self.choose_one_more_x_button.setEnabled(False)
        self.choose_one_more_y_button = QPushButton('Choose extra Y data')
        self.choose_one_more_y_button.clicked.connect(self.choose_extra_y)
        self.choose_one_more_y_button.setEnabled(False)

        add_x_buttons_layout = QHBoxLayout()
        add_x_buttons_layout.addWidget(self.choose_x_button)
        add_x_buttons_layout.addWidget(self.choose_one_more_x_button)
        add_y_buttons_layout = QHBoxLayout()
        add_y_buttons_layout.addWidget(self.choose_y_button)
        add_y_buttons_layout.addWidget(self.choose_one_more_y_button)

        self.display_x_axis = QPlainTextEdit('Here will be shown data to display on X axis')
        self.display_x_axis.setReadOnly(True)
        self.display_y_axis = QPlainTextEdit('Here will be shown data to display on Y axis')
        self.display_y_axis.setReadOnly(True)

        plot_setup_layout = QVBoxLayout()
        plot_setup_layout.addLayout(add_x_buttons_layout)
        plot_setup_layout.addWidget(self.display_x_axis)
        plot_setup_layout.addLayout(add_y_buttons_layout)
        plot_setup_layout.addWidget(self.display_y_axis)

        plot_layout = QHBoxLayout()
        plot_layout.addWidget(self.html_plot_view)
        plot_layout.addLayout(plot_setup_layout)

        self.open_web_page_button = QPushButton('Open in browser')
        self.save_to_pdf_button = QPushButton('Save to PDF')
        self.save_to_html_button = QPushButton('Save to HTML')
        self.add_plot_button = QPushButton('Add one more plot')

        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.go_to_previous_widget)

        manage_plot_layout = QHBoxLayout()
        manage_plot_layout.addWidget(self.open_web_page_button)
        manage_plot_layout.addWidget(self.save_to_html_button)
        manage_plot_layout.addWidget(self.save_to_pdf_button)
        manage_plot_layout.addWidget(self.add_plot_button)

        plot_setup_layout = QVBoxLayout()
        plot_setup_layout.addWidget(self.custom_title_field)
        plot_setup_layout.addLayout(plot_layout)
        plot_setup_layout.addLayout(manage_plot_layout)
        plot_setup_layout.addWidget(self.back_button)

        self.setLayout(plot_setup_layout)

    def load_page(self):
        with open(self.html_plot_path, 'r') as f:
            html = f.read()
            self.webEngineView.setHtml(html)

    def go_to_previous_widget(self):
        # TODO: clean all filed widgets
        self.log_display_manage_widget_object.go_to_get_display_data_layout()

    def choose_x_axis(self):
        self.x_axis_data = list()
        dlg = choose_data_to_axis_dialog.ChooseAxisData(self.parsed_topic_w_type_dict)
        # dlg.topic_dict = self.parsed_topic_dict
        if dlg.exec():
            dlg.get_checked_items()
            self.x_axis_data = dlg.selected_items
            self.choose_number_of_selected_axes()
            self.display_x_axis.setPlainText('here is X:')
            # print('self.x_axis_data[0][1]: ', self.x_axis_data[0][1])
            msg_data_dict = get_data_from_msg.get_data(self.x_axis_data[0][1], self.parsed_topic_w_msgs_dict)
            print('required messages: ', msg_data_dict)
            for msg_field in self.x_axis_data:
                self.display_x_axis.appendPlainText(str(msg_field))
        else:
            self.choose_number_of_selected_axes()
            self.x_axis_data = ['You didn\'t select anything']
            self.display_x_axis.setPlainText(self.x_axis_data[0])

    def choose_extra_x(self):
        dlg = choose_data_to_axis_dialog.ChooseAxisData(self.parsed_topic_w_type_dict)
        # dlg.topic_dict = self.parsed_topic_dict
        if dlg.exec():
            dlg.get_checked_items()
            self.x_axis_data.extend(dlg.selected_items)
            self.choose_number_of_selected_axes()
            self.display_x_axis.setPlainText('here is X:')
            for msg_field in self.x_axis_data:
                self.display_x_axis.appendPlainText(str(msg_field))
        else:
            pass

    def choose_y_axis(self):
        self.y_axis_data = list()
        dlg = choose_data_to_axis_dialog.ChooseAxisData(self.parsed_topic_w_type_dict)
        # dlg.topic_dict = self.parsed_topic_dict
        if dlg.exec():
            dlg.get_checked_items()
            self.y_axis_data = dlg.selected_items
            self.choose_number_of_selected_axes()
            self.display_y_axis.setPlainText('here is Y:')
            for msg_field in self.y_axis_data:
                self.display_y_axis.appendPlainText(str(msg_field))
        else:
            self.choose_number_of_selected_axes()
            self.y_axis_data = 'You didn\'t select anything'
            self.display_y_axis.setPlainText(self.y_axis_data[0])

    def choose_extra_y(self):
        dlg = choose_data_to_axis_dialog.ChooseAxisData(self.parsed_topic_w_type_dict)
        # dlg.topic_dict = self.parsed_topic_dict
        if dlg.exec():
            dlg.get_checked_items()
            self.y_axis_data.extend(dlg.selected_items)
            self.choose_number_of_selected_axes()
            self.display_y_axis.setPlainText('here is Y:')
            for msg_field in self.y_axis_data:
                self.display_y_axis.appendPlainText(str(msg_field))
        else:
            pass

    def choose_number_of_selected_axes(self):
        if len(self.x_axis_data) < 1 and len(self.y_axis_data) < 1:
            self.choose_one_more_x_button.setEnabled(False)
            self.choose_one_more_y_button.setEnabled(False)

        if len(self.x_axis_data) == 1 and len(self.y_axis_data) == 1:
            self.choose_one_more_x_button.setEnabled(True)
            self.choose_one_more_y_button.setEnabled(True)

        if len(self.y_axis_data) >= 2 or len(self.x_axis_data) >= 2:
            self.choose_one_more_x_button.setEnabled(False)
            self.choose_one_more_y_button.setEnabled(False)

        if len(self.y_axis_data) == 1 and len(self.x_axis_data) < 1:
            self.choose_one_more_x_button.setEnabled(False)
            self.choose_one_more_y_button.setEnabled(True)

        if len(self.y_axis_data) < 1 and len(self.x_axis_data) == 1:
            self.choose_one_more_x_button.setEnabled(True)
            self.choose_one_more_y_button.setEnabled(False)
