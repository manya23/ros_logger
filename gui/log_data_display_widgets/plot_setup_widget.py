#!/usr/bin/python
import copy

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

from gui.windows_parameters_description import plot_preview_wight, plot_preview_height
from gui.dialog_windows import choose_data_to_axis_dialog
from ros_logger_scripts import get_data_from_msg, get_plot_preview


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
        self.plot_title = 'Plot with data from '
        self.custom_title_field = QPlainTextEdit(self.plot_title)
        self.custom_title_field.setFixedHeight(35)

        # self.html_plot_view = QWebEngineView()
        # self.html_plot_view.setFixedHeight(plot_preview_height)
        # self.html_plot_view.setFixedWidth(plot_preview_wight)
        self.plot_preview = get_plot_preview.PlotPreviewWidget()

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
        plot_layout.addWidget(self.plot_preview)
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
        self.x_axis_data = self.choose_axis(self.display_x_axis, 'X')
        # self.x_axis_data = list()
        # dlg = choose_data_to_axis_dialog.ChooseAxisData(self.parsed_topic_w_type_dict)
        # # dlg.topic_dict = self.parsed_topic_dict
        # if dlg.exec():
        #     dlg.get_checked_items()
        #     self.x_axis_data = dlg.selected_items
        #     self.choose_number_of_selected_axes()
        #     self.display_x_axis.setPlainText('here is X:')
        #     msg_data_dict = get_data_from_msg.get_data(self.x_axis_data[0][1], self.parsed_topic_w_msgs_dict)
        #     print('required messages: ', msg_data_dict)
        #     for msg_field in self.x_axis_data:
        #         self.display_x_axis.appendPlainText(str(msg_field))
        # else:
        #     self.choose_number_of_selected_axes()
        #     self.x_axis_data = ['You didn\'t select anything']
        #     self.display_x_axis.setPlainText(self.x_axis_data[0])

    def choose_extra_x(self):
        self.choose_extra_axis(self.x_axis_data, self.display_x_axis, 'X')

    def choose_y_axis(self):
        self.y_axis_data = self.choose_axis(self.display_y_axis, 'Y')

    def choose_extra_y(self):
        self.choose_extra_axis(self.y_axis_data, self.display_y_axis, 'Y')

    def choose_axis(self, display_bar, axis_label):
        """
        Choose field from messages hierarchy tree to display oa one plot axis
        :param display_bar: PlainText object to display info about users actions
        :param axis_label: on which data will be displayed
        :return: axis data object
        """
        dlg = choose_data_to_axis_dialog.ChooseAxisData(self.parsed_topic_w_type_dict)
        if dlg.exec():
            dlg.get_checked_items()
            axis_data = dlg.selected_items

            if axis_label == 'X':
                self.choose_number_of_selected_axes(axis_data, self.y_axis_data)
            elif axis_label == 'Y':
                self.choose_number_of_selected_axes(self.x_axis_data, axis_data)

            display_bar.setPlainText('Data to display at {axis}: '.format(axis=axis_label))
            # msg_data_dict = get_data_from_msg.get_data(axis_data[0]['field data'], self.parsed_topic_w_msgs_dict)
            # print('required messages: ', msg_data_dict)

            if axis_label == 'X':
                self.set_preview_plot(axis_data, self.y_axis_data)
            elif axis_label == 'Y':
                self.set_preview_plot(self.x_axis_data, axis_data)

            self.plot_title += axis_data[0]['field name'] + ' field from topic: ' + axis_data[0]['field data']['name'] + '\n'
            self.custom_title_field.setPlainText(self.plot_title)

            axis_data_info = '"' + axis_data[0]['field name'] + '"' + ' from ' + '"' + axis_data[0]['field data']['name']
            for path_part in axis_data[0]['field data']['path']:
                axis_data_info += '.' + path_part
            axis_data_info += '"'
            display_bar.appendPlainText(axis_data_info)

        else:
            self.choose_number_of_selected_axes(self.x_axis_data, self.y_axis_data)
            axis_data = 'You didn\'t select anything'
            display_bar.setPlainText(axis_data[0])

        return axis_data

    def choose_extra_axis(self, axis_data, display_bar, axis_label):
        dlg = choose_data_to_axis_dialog.ChooseAxisData(self.parsed_topic_w_type_dict)
        # dlg.topic_dict = self.parsed_topic_dict
        if dlg.exec():
            dlg.get_checked_items()
            axis_data.extend(dlg.selected_items)
            self.choose_number_of_selected_axes(self.x_axis_data, self.y_axis_data)
            display_bar.setPlainText('Data to display at {axis}: '.format(axis=axis_label))
            for msg_field in axis_data:
                display_bar.appendPlainText(str(msg_field))
        else:
            pass

    def choose_number_of_selected_axes(self, x_axis_data, y_axis_data):
        # print('data lists len (x,y) : ', len(x_axis_data), len(y_axis_data))
        if len(x_axis_data) < 1 and len(y_axis_data) < 1:
            self.choose_one_more_x_button.setEnabled(False)
            self.choose_one_more_y_button.setEnabled(False)

        if len(x_axis_data) == 1 and len(y_axis_data) == 1:
            # TODO: что тут происходит,  когда выбираешь сначала x, потом y, setEnabled не срабатывает, хотя в условие входит
            self.choose_one_more_x_button.setEnabled(True)
            self.choose_one_more_y_button.setEnabled(True)
            # print('True')

        if len(y_axis_data) >= 2 or len(x_axis_data) >= 2:
            self.choose_one_more_x_button.setEnabled(False)
            self.choose_one_more_y_button.setEnabled(False)

        if len(y_axis_data) == 1 and len(x_axis_data) < 1:
            self.choose_one_more_x_button.setEnabled(False)
            self.choose_one_more_y_button.setEnabled(True)

        if len(y_axis_data) < 1 and len(x_axis_data) == 1:
            self.choose_one_more_x_button.setEnabled(True)
            self.choose_one_more_y_button.setEnabled(False)

    def set_preview_plot(self, x_axis_data, y_axis_data):
        print('data lists len (x,y) : ', len(x_axis_data), len(y_axis_data))

        if len(x_axis_data) < 1 and len(y_axis_data) < 1:
            pass

        if len(x_axis_data) == 1 and len(y_axis_data) == 1:
            x_msg_data_dict = get_data_from_msg.get_data(x_axis_data[0]['field data'], self.parsed_topic_w_msgs_dict)
            y_msg_data_dict = get_data_from_msg.get_data(y_axis_data[0]['field data'], self.parsed_topic_w_msgs_dict)
            self.plot_preview.update_plot(x_axis_data=x_msg_data_dict, y_axis_data=y_msg_data_dict)

        if len(y_axis_data) >= 2 or len(x_axis_data) >= 2:
            pass

        if len(y_axis_data) == 1 and len(x_axis_data) < 1:
            msg_data_dict = get_data_from_msg.get_data(y_axis_data[0]['field data'], self.parsed_topic_w_msgs_dict)
            self.plot_preview.update_plot(axis_data=msg_data_dict)

        if len(y_axis_data) < 1 and len(x_axis_data) == 1:
            print('True')
            msg_data_dict = get_data_from_msg.get_data(x_axis_data[0]['field data'], self.parsed_topic_w_msgs_dict)
            self.plot_preview.update_plot(axis_data=msg_data_dict)
