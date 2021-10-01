import matplotlib.pyplot as plt, mpld3
import os

import sys
import matplotlib

matplotlib.use('Qt5Agg')

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


# def form_plot(x_axis_data, y_axis_data, meta_data_folder_name):
#     """
#     Выводит на график путь каждой РТП из списка rtp_info_list. Сохраняет интерактивный график в html файл
#     :param rtp_info_list: список объектов, хранящих информацию про РТП
#     :param meta_data_folder_name: путь для сохранения графиков
#     :return: html с интерактивным графиком в формате строки
#     """
#     print('axis data', x_axis_data, y_axis_data)
#     fig, ax = plt.subplots(figsize=(10, 10))
#     rtp_list = list()
#     # x_plot_range = list()
#     # y_plot_range = list()
#     # for rtp in rtp_info_list:
#     #     rtp_list.append(rtp.rtp_id)
#     ax.plot(x_axis_data, y_axis_data, label='Plot preview')
#     # x_plot_range.extend([rtp.x_nav_coord_list[0], rtp.x_nav_coord_list[-1]])
#     # y_plot_range.extend([rtp.y_nav_coord_list[0], rtp.y_nav_coord_list[-1]])
#     ax.legend(loc=2)
#     ax.set_ylabel('Y')
#     ax.set_xlabel('X')
#     ax.grid(linestyle='--', linewidth=1)
#     ax.set_title('Plot preview')
#     plt.show()
#
#     img_name = ('rtp_{rtp_list}_path_plot.png'.format(rtp_list=rtp_list))
#     plot_path = '{folder_name}{image_name}'.format(folder_name=meta_data_folder_name, image_name=img_name)
#     plt.savefig(plot_path)
#
#     # save plot to .html script
#     # html_name = ('rtp_{rtp_list}_path_plot'.format(rtp_list=rtp_list))
#     # script_string = mpld3.fig_to_html(fig, "{folder_name}{script_name}.html".format(folder_name=meta_data_folder_name,
#     #                                                                                 script_name=html_name), )
#
#     return plot_path

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


class PlotPreviewWidget(QWidget):
    def __init__(self):
        super(PlotPreviewWidget, self).__init__()
        self.x_data = list()
        self.y_data = list()
        self.main_plot = MplCanvas(self, width=5, height=4, dpi=100)
        self.main_plot.axes.plot(self.x_data, self.y_data)
        self.main_plot.axes.set_title('Plot preview')

        self.meta_data_folder = create_meta_data_folder()

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.main_plot, self)

        plot_widget_layout = QVBoxLayout()
        plot_widget_layout.addWidget(self.main_plot)
        plot_widget_layout.addWidget(toolbar)

        self.setLayout(plot_widget_layout)

    def update_plot(self, axis_data=None, x_axis_data=None, y_axis_data=None):

        if x_axis_data is None and y_axis_data is None:
            x_axis = list()
            y_axis = list()
            for timestamp, msg in axis_data.items():
                x_axis.append(msg)
                y_axis.append(timestamp)
        else:
            # x_axis = list()
            # y_axis = list()
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
            print('x_axis[0], y_axis[0]: ', x_axis[0], y_axis[0])
            print('x_axis, y_axis: ', x_axis, y_axis)
            self.main_plot.axes.scatter(x_axis, y_axis, color='r')
        else:
            self.main_plot.axes.plot(x_axis, y_axis, 'r')
        # Trigger the canvas to update and redraw.
        self.main_plot.draw()


# def get_plot_preview(axis_data):
#     meta_data_folder = create_meta_data_folder()
#     x_axis_data = list()
#     y_axis_data = list()
#     for timestamp, msg in axis_data.items():
#         x_axis_data.append(msg)
#         y_axis_data.append(timestamp)
#
#     plot_path = form_plot(x_axis_data, y_axis_data, meta_data_folder)


def create_meta_data_folder():
    # создаю папку для хранения временных фийлов
    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(current_dir_path + '/meta_data/'):
        os.makedirs(current_dir_path + '/meta_data/')
    # сохраняю туда скрипты для просмотра интерактивных графиков
    target_dir_path = current_dir_path + '/meta_data/'
    js_storage_folder_name = current_dir_path + '/interactive_plot_support_scripts/'
    js_files_list = list([[js_storage_folder_name + 'd3.v5.js', 'd3.v5.js'],
                          [js_storage_folder_name + 'mpld3.v0.5.2.js', 'mpld3.v0.5.2.js']])
    if not os.path.exists(target_dir_path + '/scripts/'):
        os.makedirs(target_dir_path + '/scripts/')
    for js_file in js_files_list:
        if not os.path.exists(target_dir_path + '/scripts/' + js_file[1]):
            with open(js_file[0]) as f:
                lines = f.readlines()
            with open(target_dir_path + '/scripts/' + js_file[1], 'w') as f:
                for line in lines:
                    f.write("%s\n" % line)

    return target_dir_path
