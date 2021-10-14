from PyQt5.QtCore import *
from PyQt5 import QtCore
from ros_logger_scripts.data_display_modules import get_plot_preview


class ThreadWorkTask(QObject):
    running = False

    # определяется сигнал, который будет возвращать вывод потока
    plot_fill_process_signal = pyqtSignal(bool)

    def __init__(self):
        super(ThreadWorkTask, self).__init__()

    def update_plot(self, main_plot, axis_data=None, x_axis_data=None, y_axis_data=None):
        """
        Updates plot fields and fill variables that stores plot's data

        :param main_plot: plot object from widget
        :param axis_data: data from message with timestamp dictionary
        :type axis_data: dict
        :param x_axis_data: data from message with timestamp dictionary
        :type x_axis_data: dict
        :param y_axis_data: data from message with timestamp dictionary
        :type y_axis_data: dict
        :return: nothing
        """

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

        main_plot.axes.cla()  # Clear the canvas.
        if len(x_axis) == 1 and len(y_axis) == 1:
            # print('x_axis[0], y_axis[0]: ', x_axis[0], y_axis[0])
            # print('x_axis, y_axis: ', x_axis, y_axis)
            main_plot.axes.scatter(x_axis, y_axis, color='r')
        else:
            main_plot.axes.plot(x_axis, y_axis, 'r')
        # Trigger the canvas to update and redraw.
        main_plot.draw()

        self.plot_fill_process_signal.emit(True)


class StartThread(QObject):
    # thread_done_mark_signal = pyqtSignal(str)

    def __init__(self):
        super(StartThread, self).__init__()

        self.__init_thread()

    def __init_thread(self):
        self.update_plot_thread = QThread(parent=self)
        self.widget_running_thread = ThreadWorkTask()
        self.widget_running_thread.moveToThread(self.update_plot_thread)
        # self.widget_running_thread.plot_fill_process_signal.connect(self.thread_done)
        # self.update_plot_thread.started.connect(self.widget_running_thread.update_plot)
        self.update_plot_thread.start()

    def destroy_thread(self):
        self.update_plot_thread.quit()
