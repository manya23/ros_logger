import matplotlib.pyplot as plt, mpld3
import os

import sys
import matplotlib

matplotlib.use('Qt5Agg')

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from ros_logger_scripts.data_display_modules import preview_plot_update_thread


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=13, height=10, dpi=200):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


class PlotPreviewWidget(QWidget):
    """
    Widget to display preview of collecting plot
    """

    def __init__(self, meta_data_folder_path):
        super(PlotPreviewWidget, self).__init__()
        self.update_thread = preview_plot_update_thread.StartThread()

        self.set_main_plot()

        self.meta_data_folder = meta_data_folder_path
        self.axis_description = str()
        self.plot_title = str()

        # Create toolbar, passing canvas as first parameter, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.main_plot, self)

        plot_widget_layout = QVBoxLayout()
        plot_widget_layout.addWidget(self.main_plot)
        plot_widget_layout.addWidget(toolbar)

        self.setLayout(plot_widget_layout)

    # TODO: запускать его в отдельном потоке
    def update_plot(self, axis_description, plot_title, axis_data=None, x_axis_data=None, y_axis_data=None):
        """
        Updates plot fields and fill variables that stores plot's data

        :param axis_description: dictionary with info about axis: 'param_name from topic_name' and 'topic_logs_directory'
        :type axis_description: dict
        :param plot_title: custom or default plot title from gui
        :type plot_title: str
        :param axis_data: data from message with timestamp dictionary
        :type axis_data: dict
        :param x_axis_data: data from message with timestamp dictionary
        :type x_axis_data: dict
        :param y_axis_data: data from message with timestamp dictionary
        :type y_axis_data: dict
        :return: nothing
        """

        self.axis_description = axis_description
        self.plot_title = plot_title
        # TODO: start updating in thread
        # self.update_thread.widget_running_thread.update_plot(self.main_plot, axis_data, x_axis_data, y_axis_data)

        # if specific x and y data doesn't declare - display at x axis timestamps, at y axis data from message field
        if x_axis_data is None and y_axis_data is None:
            x_axis = list()
            y_axis = list()
            for timestamp, msg in axis_data.items():
                x_axis.append(timestamp)
                y_axis.append(msg)
        else:
            x_timestamp = list(x_axis_data.keys())
            y_timestamp = list(y_axis_data.keys())
            if len(x_timestamp) != len(y_timestamp):
                min_ts = max([min(x_timestamp), min(y_timestamp)])
                max_ts = min([max(x_timestamp), max(y_timestamp)])
                x_axis = [msg for ts, msg in x_axis_data.items() if min_ts <= ts <= max_ts]
                y_axis = [msg for ts, msg in y_axis_data.items() if min_ts <= ts <= max_ts]
            else:
                x_axis = [msg for ts, msg in x_axis_data.items()]
                y_axis = [msg for ts, msg in y_axis_data.items()]

        self.main_plot.axes.cla()  # Clear the canvas.
        if len(x_axis) == 1 and len(y_axis) == 1:
            # print('x_axis[0], y_axis[0]: ', x_axis[0], y_axis[0])
            # print('x_axis, y_axis: ', x_axis, y_axis)
            self.main_plot.axes.scatter(x_axis, y_axis, color='r')
        else:
            self.main_plot.axes.plot(x_axis, y_axis, 'r')
        # Trigger the canvas to update and redraw.
        self.main_plot.draw()

    def add_plot(self, axis_description, plot_title, axis_data=None, x_axis_data=None, y_axis_data=None):
        # if specific x and y data doesn't declare - display at x axis timestamps, at y axis data from message field
        if x_axis_data is None and y_axis_data is None:
            x_axis = list()
            y_axis = list()
            for timestamp, msg in axis_data.items():
                x_axis.append(timestamp)
                y_axis.append(msg)
        else:
            x_timestamp = list(x_axis_data.keys())
            y_timestamp = list(y_axis_data.keys())
            if len(x_timestamp) != len(y_timestamp):
                min_ts = max([min(x_timestamp), min(y_timestamp)])
                max_ts = min([max(x_timestamp), max(y_timestamp)])
                x_axis = [msg for ts, msg in x_axis_data.items() if min_ts <= ts <= max_ts]
                y_axis = [msg for ts, msg in y_axis_data.items() if min_ts <= ts <= max_ts]
            else:
                x_axis = [msg for ts, msg in x_axis_data.items()]
                y_axis = [msg for ts, msg in y_axis_data.items()]

        # draw new plot
        if len(x_axis) == 1 and len(y_axis) == 1:
            # print('x_axis[0], y_axis[0]: ', x_axis[0], y_axis[0])
            # print('x_axis, y_axis: ', x_axis, y_axis)
            self.main_plot.axes.scatter(x_axis, y_axis, color='r')
        else:
            self.main_plot.axes.plot(x_axis, y_axis)
        # Trigger the canvas to update and redraw.
        self.main_plot.draw()

    def get_current_plot_object(self):
        """
        Translate plot object to interactive plot object
        :return: interactive plot object
        """
        fig = self.main_plot.axes.get_figure()
        plot_object = mpld3.fig_to_html(fig)
        return plot_object

    def get_plot_info(self):
        plot_description_object = dict()
        plot_description_object.update({'plot': self.get_current_plot_object()})
        plot_description_object.update({'axes': self.axis_description})
        plot_description_object.update(({'title': self.plot_title}))

        return plot_description_object

    def set_main_plot(self):
        """
        Create empty plot object
        :return: nothing
        """
        self.x_data = list()
        self.y_data = list()
        self.main_plot = MplCanvas(self, width=5, height=4, dpi=100)
        self.main_plot.axes.plot(self.x_data, self.y_data)
        self.main_plot.axes.set_title('Plot preview')

        self.main_plot.draw()

    def clear_plot(self):
        self.main_plot.axes.cla()
        self.main_plot.draw()
