#!/usr/bin/python
import time
import os
import webbrowser
import pdfkit

from PyQt5.QtWidgets import *

from gui.dialog_windows import choose_data_to_axis_dialog, choose_directory_dialog
from ros_logger_scripts import create_meta_data_folder
from ros_logger_scripts.data_display_modules import save_report_to_html, get_data_from_msg, get_plot_preview, preview_plot_update_thread


class PlotSetupWidget(QWidget):
    """
    The widget to set up plots that have to be added to report. It presents functions like:
            1. Choose data from logged messages to display on plot's axis (in case when one axis chosen, free axis displays chosen data's timestamps)
            2. Display setting plot preview
            3. Add few plot to final report
            4. Save report with data plots to PDF ot HTML(with interactive plots) formats
    """
    def __init__(self, log_display_manage_widget_object):
        super(PlotSetupWidget, self).__init__()
        self.log_display_manage_widget_object = log_display_manage_widget_object
        self.html_plot_path = str()
        self.x_axis_data = list()
        self.y_axis_data = list()
        self.parsed_topic_w_type_dict = list()
        self.parsed_topic_w_msgs_dict = dict()
        self.log_directory_path = str()

        self.plot_to_save_list = list()
        self.report_name = 'Report_' + str(time.strftime("%H:%M:%S", time.localtime(time.time()))) + '_with_data_'
        self.report_path = str()

        self.browser_view = False
        self.plot_save_flag = False
        self.__init_widget()

    def __init_widget(self):
        self.plot_title = 'Plot with data from '
        self.custom_title_field = QPlainTextEdit(self.plot_title)
        self.custom_title_field.setFixedHeight(35)

        self.meta_data_folder = create_meta_data_folder.create_folder()
        self.plot_preview = get_plot_preview.PlotPreviewWidget(self.meta_data_folder)
        # self.plot_preview_thread = plot_preview_thread.StartThread(self.meta_data_folder)
        # time.sleep(1.0)
        # self.plot_preview = self.plot_preview_thread.get_widget_object()

        self.choose_x_button = QPushButton('Choose X axis')
        self.choose_x_button.clicked.connect(self.__choose_x_axis)
        self.choose_y_button = QPushButton('Choose Y axis')
        self.choose_y_button.clicked.connect(self.__choose_y_axis)

        self.choose_one_more_x_button = QPushButton('Choose extra X data')
        self.choose_one_more_x_button.clicked.connect(self.__choose_extra_x)
        self.choose_one_more_x_button.setEnabled(False)
        self.choose_one_more_y_button = QPushButton('Choose extra Y data')
        self.choose_one_more_y_button.clicked.connect(self.__choose_extra_y)
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

        self.plot_setup_widget_info = QPlainTextEdit('Please, setup plot data parameters by choosing axis data from parsed files.')

        self.open_web_page_button = QPushButton('Open full report in browser')
        self.open_web_page_button.setVisible(False)
        self.open_web_page_button.clicked.connect(self.__open_report_in_browser)
        self.save_to_pdf_button = QPushButton('Save to PDF')
        self.save_to_pdf_button.clicked.connect(self.__save_report_to_pdf)
        self.save_to_html_button = QPushButton('Save to HTML')
        self.save_to_html_button.clicked.connect(self.__save_report_to_html)
        self.add_plot_button = QPushButton('Add one more plot')
        self.add_plot_button.clicked.connect(self.__add_plot_to_report)

        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.go_to_previous_widget)

        manage_plot_layout = QHBoxLayout()
        manage_plot_layout.addWidget(self.save_to_html_button)
        manage_plot_layout.addWidget(self.save_to_pdf_button)
        manage_plot_layout.addWidget(self.add_plot_button)

        plot_setup_layout = QVBoxLayout()
        plot_setup_layout.addWidget(self.custom_title_field)
        plot_setup_layout.addLayout(plot_layout)
        plot_setup_layout.addWidget(self.plot_setup_widget_info)
        plot_setup_layout.addLayout(manage_plot_layout)
        plot_setup_layout.addWidget(self.open_web_page_button)
        plot_setup_layout.addWidget(self.back_button)

        self.setLayout(plot_setup_layout)

    def __open_report_in_browser(self):
        """
        Gathers all plots to HTML file and displays it in browser.
        :return: nothing
        """
        self.__save_report()

        webbrowser.open('file://' + os.path.realpath(self.report_path + '.html'), new=2)
        print('open web page with html file: ', self.report_path)
        self.browser_view = True

    def __save_report_to_pdf(self):
        self.__save_report()
        self.pdf_dir_path = choose_directory_dialog.choose_directory()

        pure_report_file_name = str()
        for char in self.report_path[-2::-1]:
            if char != '/':
                pure_report_file_name += char
            else:
                break
        self.pdf_file_name = pure_report_file_name[::-1] + '.pdf'

        print('saving to pdf')
        pdfkit.from_file(self.report_path + '.html', self.pdf_dir_path + '/' + self.pdf_file_name)
        self.plot_setup_widget_info.appendPlainText('Report saved to {dir}'.format(dir=self.pdf_dir_path + '/' + self.pdf_file_name))

    def __save_report_to_html(self):
        """
        Gathers all plot scripts and save them to common report
        :return: nothing
        """
        self.__save_report()
        # choose directory to save report as .html file
        self.html_dir_path = choose_directory_dialog.choose_directory()
        pure_report_file_name = str()
        for char in self.report_path[-2::-1]:
            if char != '/':
                pure_report_file_name += char
            else:
                break
        self.html_file_name = pure_report_file_name[::-1] + '.html'

        target_dir_path = self.html_dir_path + '/' + self.html_file_name
        save_report_to_html.write_js_scripts_folder(self.html_dir_path)
        # writing report to target directory
        with open(self.report_path + '.html') as f:
            lines = f.readlines()
        with open(target_dir_path, 'w') as f:
            for line in lines:
                f.write("%s\n" % line)

        self.plot_setup_widget_info.appendPlainText('Report saved to {dir}'.format(dir=self.html_dir_path + '/' + self.html_file_name))

    def __save_report(self):
        """
        Save report to meta data folder and add plot to list of created plots
        :return: nothing
        """
        if not self.plot_save_flag:
            if self.browser_view:
                pass
            else:
                plot_description_object = self.plot_preview.get_plot_info()
                self.plot_to_save_list.append(plot_description_object)
            self.report_path = save_report_to_html.gather_report_parts_to_html(self.plot_to_save_list, self.meta_data_folder,
                                                                               self.report_name)
            self.plot_save_flag = True
        else:
            pass

    def __add_plot_to_report(self):
        # Тут сохранять объект графика в список
        plot_description_object = self.plot_preview.get_plot_info()
        self.plot_to_save_list.append(plot_description_object)
        # и чистить данные из виджета графика
        self.__reset_widgets_parameters()

        if len(self.plot_to_save_list) >= 1:
            self.open_web_page_button.setVisible(True)
        print('adding one more plot')
        self.browser_view = False

        self.plot_setup_widget_info.appendPlainText('Please, setup new plot axis')

    def go_to_previous_widget(self):
        # TODO: clean all filed widgets
        self.__reset_widgets_parameters()
        self.plot_to_save_list = list()
        self.log_display_manage_widget_object.go_to_get_display_data_layout()

    def __reset_widgets_parameters(self):
        """
        Set all widgets parameters to default. Except 'self.plot_to_save_list'
        :return: nothing
        """
        self.custom_title_field.setPlainText('Plot with data from ')
        self.display_x_axis.setPlainText('Here will be shown data to display on X axis')
        self.display_y_axis.setPlainText('Here will be shown data to display on Y axis')
        self.plot_setup_widget_info.setPlainText('Please, setup plot data parameters by choosing axis data from parsed files.')
        self.plot_title = 'Plot with data from '
        self.x_axis_data = list()
        self.y_axis_data = list()
        self.report_path = str()
        self.plot_preview.clear_plot()

    def __choose_x_axis(self):
        self.x_axis_data = self.__choose_axis(self.display_x_axis, 'X')

    def __choose_extra_x(self):
        self.__choose_extra_axis(self.x_axis_data, self.display_x_axis, 'X')

    def __choose_y_axis(self):
        self.y_axis_data = self.__choose_axis(self.display_y_axis, 'Y')

    def __choose_extra_y(self):
        self.__choose_extra_axis(self.y_axis_data, self.display_y_axis, 'Y')

    def __choose_axis(self, display_bar, axis_label):
        """
        Choose field from messages hierarchy tree to display on one plot axis
        :param display_bar: PlainText object to display info about users actions
        :param axis_label: on which data will be displayed
        :return: axis data object
        """
        dlg = choose_data_to_axis_dialog.ChooseAxisData(self.parsed_topic_w_type_dict)
        if dlg.exec():
            dlg.get_checked_items()
            axis_data = dlg.selected_items

            # set number of selected to manage visibility of axis choosing buttons
            if axis_label == 'X':
                self.__choose_number_of_selected_axes(axis_data, self.y_axis_data)
            elif axis_label == 'Y':
                self.__choose_number_of_selected_axes(self.x_axis_data, axis_data)

            display_bar.setPlainText('Data to display at {axis}: '.format(axis=axis_label))

            # form values with info to display in report
            axis_description = dict()
            plot_title = axis_data[0]['field name'] + ' field from topic: ' + axis_data[0]['field data']['name']

            # depend on chosen for edition axis, reset plot data
            if axis_label == 'X':
                # form axis description to display at report
                axis_description.update({'X': ['"' + axis_data[0]['field name'] + '"' + ' from ' + '"' + axis_data[0]['field data']['name'],
                                               self.log_directory_path]})
                if self.y_axis_data:
                    axis_description.update({'Y': ['"' + self.y_axis_data[0]['field name'] + '"' + ' from ' + '"' + self.y_axis_data[0]['field data']['name'],
                                                   self.log_directory_path]})
                else:
                    axis_description.update({'Y': ['"' + axis_data[0]['field name'] + '"' + ' timestamps', self.log_directory_path]})
                # then display plot preview
                self.__set_preview_plot(axis_data, self.y_axis_data, axis_description, plot_title)
            elif axis_label == 'Y':
                # form axis description to display at report
                axis_description.update({'Y': ['"' + axis_data[0]['field name'] + '"' + ' from ' + '"' + axis_data[0]['field data']['name'],
                                               self.log_directory_path]})
                if self.x_axis_data:
                    axis_description.update({'X': ['"' + self.x_axis_data[0]['field name'] + '"' + ' from ' + '"' + self.x_axis_data[0]['field data']['name'],
                                                   self.log_directory_path]})
                else:
                    axis_description.update({'X': ['"' + axis_data[0]['field name'] + '"' + ' timestamps', self.log_directory_path]})
                # then display plot preview
                self.__set_preview_plot(self.x_axis_data, axis_data, axis_description, plot_title)

            self.report_name += axis_data[0]['field name'].replace('/','_') + '_from_'\
                                + axis_data[0]['field data']['name'].replace('/','_') + '_'
            self.plot_title += axis_data[0]['field name'] + ' field from topic: ' + axis_data[0]['field data']['name'] + '\n'
            self.custom_title_field.setPlainText(self.plot_title)

            axis_data_info = '"' + axis_data[0]['field name'] + '"' + ' from ' + '"' + axis_data[0]['field data']['name']
            for path_part in axis_data[0]['field data']['path']:
                axis_data_info += '.' + path_part
            axis_data_info += '"'
            display_bar.appendPlainText(axis_data_info)

        else:
            self.__choose_number_of_selected_axes(self.x_axis_data, self.y_axis_data)
            axis_data = 'You didn\'t select anything'
            display_bar.setPlainText(axis_data[0])

        return axis_data

    def __choose_extra_axis(self, axis_data, display_bar, axis_label):
        dlg = choose_data_to_axis_dialog.ChooseAxisData(self.parsed_topic_w_type_dict)
        # dlg.topic_dict = self.parsed_topic_dict
        if dlg.exec():
            dlg.get_checked_items()
            axis_data.extend(dlg.selected_items)
            self.__choose_number_of_selected_axes(self.x_axis_data, self.y_axis_data)
            display_bar.setPlainText('Data to display at {axis}: '.format(axis=axis_label))
            for msg_field in axis_data:
                display_bar.appendPlainText(str(msg_field))
        else:
            pass

    def __choose_number_of_selected_axes(self, x_axis_data, y_axis_data):
        # print('data lists len (x,y) : ', len(x_axis_data), len(y_axis_data))
        if len(x_axis_data) < 1 and len(y_axis_data) < 1:
            self.choose_one_more_x_button.setEnabled(False)
            self.choose_one_more_y_button.setEnabled(False)

        if len(x_axis_data) == 1 and len(y_axis_data) == 1:
            # TODO: что тут происходит, когда выбираешь сначала x, потом y, setEnabled не срабатывает, хотя в условие входит
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

    def __set_preview_plot(self, x_axis_data, y_axis_data, axis_data_description, plot_title):
        """
        In case of number of filled data for each axis sets new plot to plot preview
        :param x_axis_data:
        :param y_axis_data:
        :param axis_data_description: contains two items: 'param_name from topic_name', 'topic_logs_directory'
        :type axis_data_description: dict
        :param plot_title: custom or default plot title from gui
        :type plot_title: str
        :return: nothing
        """
        print('data lists len (x,y) : ', len(x_axis_data), len(y_axis_data))
        self.plot_save_flag = False

        if len(x_axis_data) < 1 and len(y_axis_data) < 1:
            pass

        if len(x_axis_data) == 1 and len(y_axis_data) == 1:
            x_msg_data_dict = get_data_from_msg.get_data(x_axis_data[0]['field data'], self.parsed_topic_w_msgs_dict)
            y_msg_data_dict = get_data_from_msg.get_data(y_axis_data[0]['field data'], self.parsed_topic_w_msgs_dict)
            self.plot_setup_widget_info.appendPlainText('Please, wait. Plot preview is updating.')
            self.plot_preview.update_plot(axis_data_description, plot_title, x_axis_data=x_msg_data_dict, y_axis_data=y_msg_data_dict)

        if len(y_axis_data) >= 2 or len(x_axis_data) >= 2:
            pass

        if len(y_axis_data) == 1 and len(x_axis_data) < 1:
            msg_data_dict = get_data_from_msg.get_data(y_axis_data[0]['field data'], self.parsed_topic_w_msgs_dict)
            self.plot_setup_widget_info.appendPlainText('Please, wait. Plot preview is updating.')
            self.plot_preview.update_plot(axis_data_description, plot_title, axis_data=msg_data_dict)

        if len(y_axis_data) < 1 and len(x_axis_data) == 1:
            print('True')
            msg_data_dict = get_data_from_msg.get_data(x_axis_data[0]['field data'], self.parsed_topic_w_msgs_dict)
            self.plot_setup_widget_info.appendPlainText('Please, wait. Plot preview is updating.')
            self.plot_preview.update_plot(axis_data_description, plot_title, axis_data=msg_data_dict)


