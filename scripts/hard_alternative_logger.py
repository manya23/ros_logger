# coding=utf8
from rcl_interfaces import msg
import argparse
import rclpy
import time
import os
import json
from pydoc import locate
import re
import sys
from datetime import date

from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
import std_msgs.msg
import gis_rtk_msgs.msg
import rtp_msgs.msg
import marker_msgs.msg
import nav_msgs.msg
import geometry_msgs.msg
import sensor_msgs.msg
import visualization_msgs.msg
from copy import deepcopy
from rtp_communication import rtp_analyzer
import threading

from rosidl_runtime_py import message_to_ordereddict


class MyTopic():
    def __init__(self, node, topic_name, topic_type, topic_qos, date_time, logs_path):
        self.sub = node.create_subscription(topic_type, topic_name, self.__callback, topic_qos)
        self.topic_name = topic_name
        self.topic_type = topic_type
        self.static_data_time = date_time
        self.msg_list = list()
        self.logs_path = logs_path
        print("topic %s init witch type %s" % (self.topic_name, self.topic_type))

        self._topic_name_copy = self.topic_name
        self._topic_name_copy = self._topic_name_copy.replace('/', '_')

        self.__init_log_file()

        # timer = node.create_timer(1.0, self.timer_callback)
        threading.Thread(target=self.thread_log_writer, args=()).start()

    def __init_log_file(self):
        folder_name = self.logs_path + '/' + str(self.static_data_time) + "_json"
        if not os.path.isdir(folder_name):
            os.makedirs(folder_name)

        # в начало файла с логами из топика заполняются поля с именем топика и типом сообщений, которые туда публикуются
        with open('{0}/{1}.txt'.format(folder_name, self.static_data_time + self._topic_name_copy), 'a') as file:
            str_type = str(self.topic_type).split("'")[1]
            str_type = re.sub(r'[.]_\w+[.]', '.', str_type)
            # str_type = re.findall(r'\w+[.]\w+[.]\w+', str_type)[0]
            file.write('{}: {}\n'.format('topic_name', self.topic_name))
            file.write('{}: {}\n'.format('msg_type', str_type))
            file.close()

    def __callback(self, msg):
        """
        :param msg:
        :return: nothing
        cb. is writing msg to file
        """
        try:
            self.msg_list.append((time.time(), msg))
        except:
            pass

    def thread_log_writer(self):
        while True:
            try:
                temp_msg_list = deepcopy(self.msg_list)
                self.msg_list.clear()
            except:
                continue
            self.__dump_topic_data_to_file(temp_msg_list)
            time.sleep(1.0)

    def timer_callback(self):
        temp_msg_list = deepcopy(self.msg_list)
        self.msg_list.clear()
        self.__dump_topic_data_to_file(temp_msg_list)

    def __dump_topic_data_to_file(self, msg_list):
        if len(msg_list) == 0:
            return

        folder_name = self.logs_path + '/' + str(self.static_data_time) + "_json"
        if not os.path.isdir(folder_name):
            os.makedirs(folder_name)

        with open('{0}/{1}.txt'.format(folder_name, self.static_data_time + self._topic_name_copy), 'a') as file:

            # сообщения типа OccupancyGrid зписываются с частотой 1/10
            if self.topic_type == nav_msgs.msg.OccupancyGrid:
                pass
                for msg_num, msg in enumerate(msg_list):
                    if (msg_num % 10) == 0:
                        msg_attr_in_json = json.dumps({msg[0]: message_to_ordereddict(msg[1])})
                        file.write(msg_attr_in_json)

            else:
                for msg in msg_list:
                    msg_attr_in_json = json.dumps({msg[0]: message_to_ordereddict(msg[1])})
                    file.write(msg_attr_in_json)


def get_date_time_str(time_s):
    res_date_time = ''
    day = str(time_s.tm_mday)
    if time_s.tm_mday < 10:
        day = '0' + day
    month = str(time_s.tm_mon)
    if time_s.tm_mon < 10:
        month = '0' + month
    year = str(time_s.tm_year)
    hour = str(time_s.tm_hour)
    if time_s.tm_hour < 10:
        hour = '0' + hour
    minutes = str(time_s.tm_min)
    if time_s.tm_min < 10:
        minutes = '0' + minutes
    seconds = str(time_s.tm_sec)
    if time_s.tm_sec < 10:
        seconds = '0' + seconds
    res_date_time = day + "" + month + "" + year + "_" + hour + "_" + minutes + "_" + seconds
    return res_date_time


def get_date_str(time_s):
    day = str(time_s.tm_mday)
    if time_s.tm_mday < 10:
        day = '0' + day
    month = str(time_s.tm_mon)
    if time_s.tm_mon < 10:
        month = '0' + month
    year = str(time_s.tm_year)
    return day + "" + month + "" + year


class alternative_logger(Node):
    def __init__(self, node_name, cfg):
        self.node_name = node_name
        self.configs = cfg
        super().__init__(self.node_name, allow_undeclared_parameters=True,
                         automatically_declare_parameters_from_overrides=True)
        self.get_logger().info("init node with name: %s" % self.node_name)

        self.start_logger_time = get_date_time_str(time.localtime(time.time()))
        print("Time: " + self.start_logger_time)

        # TODO: что с определением rtp_id ?
        print('namespace: ', self.get_namespace())
        self.cur_rtp_id = rtp_analyzer.get_rtp_id(self.get_namespace())
        self.cur_rtp_id = 1
        # print('cur rtp id: ', self.cur_rtp_id)
        self.all_rtp_id_list = [self.cur_rtp_id, ]
        # список топиков заполняется топиками из конфигурационного файла
        self.list_topics = list()

        home_path = os.getenv('HOME')
        date = get_date_str(time.localtime(time.time()))
        self.logs_path = rtp_analyzer.try_get(lambda: self.get_parameter('logs_dir'),
                                              str('{home}/RTP_LOGS/{date}/RTP_{id}'.format(home=home_path, date=date,
                                                                                           id=self.cur_rtp_id)))
        print('Logs directory: ', self.logs_path)

        time.sleep(0.2)

        self.create_subscription(marker_msgs.msg.RtpSelfie, '/sgru/group_rtp_chat', self.group_chat_cb,
                                 qos_profile_sensor_data)

        self.__init_internal_network_subs()
        self.__init_external_network_subs(self.cur_rtp_id)

        # rtp_id_list = rtp_analyzer.get_active_rtp_list(self.get_node_names_and_namespaces())
        # for rtp in rtp_id_list:

    def group_chat_cb(self, msg):
        """
        :type msg: marker_msgs.msg.RtpSelfie
        """
        if msg.rtp_id in self.all_rtp_id_list:
            return

        if msg.rtp_action == marker_msgs.msg.RtpSelfie.CHECK_OUT:
            return

        self.__init_external_network_subs(msg.rtp_id)
        self.all_rtp_id_list.append(msg.rtp_id)

    def __init_internal_network_subs(self):
        for topic_describe_dict in self.configs["traced_internal_topic_list"]:
            if 'rtp_' in topic_describe_dict["name"]:
                topic_name = topic_describe_dict["name"].format(id=self.cur_rtp_id)
            else:
                topic_name = topic_describe_dict["name"]
            if topic_describe_dict["qos"] == 1:
                self.list_topics.append(MyTopic(self, topic_name, locate(topic_describe_dict["type"]), qos_profile_sensor_data,
                                            self.start_logger_time, self.logs_path))
            else:
                self.list_topics.append(MyTopic(self, topic_name, locate(topic_describe_dict["type"]), 10,
                                                self.start_logger_time, self.logs_path))

    def __init_external_network_subs(self, rtp_id):
        for topic_describe_dict in self.configs["traced_external_topic_list"]:
            if 'rtp_' in topic_describe_dict["name"]:
                topic_name = topic_describe_dict["name"].format(id=self.cur_rtp_id)
            else:
                topic_name = topic_describe_dict["name"]
            if topic_describe_dict["qos"] == 1:
                self.list_topics.append(MyTopic(self, topic_name, locate(topic_describe_dict["type"]), qos_profile_sensor_data,
                                            self.start_logger_time, self.logs_path))
            else:
                self.list_topics.append(MyTopic(self, topic_name, locate(topic_describe_dict["type"]), 10,
                                                self.start_logger_time, self.logs_path))


def get_rtp_list(args):
    """
    Возвращает список id РТП, полученный из аргументов программы

    :param args: список аргументов программы
    :type args: list
    :return: список id РТП
    :rtype: list
    """
    rtp_id_list = list()
    for arg in args:
        if arg.isdigit():
            rtp_id_list.append(int(arg))
    return list(rtp_id_list)


def run_logger(args=None):
    # загрузка конфигурационного файла
    with open(args.cfg) as json_file:
        cfg = json.load(json_file)
    rclpy.init()

    logger = alternative_logger("alternative_logger_node", cfg)

    rclpy.spin(logger)

    logger.destroy_node()
    rclpy.shutdown()

