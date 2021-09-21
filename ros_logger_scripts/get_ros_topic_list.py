# coding=utf8
# from rcl_interfaces import msg
import rclpy
import time

from rclpy.node import Node


class TopicList:
    def __init__(self):
        self.run()

    def run(self):
        rclpy.init()
        self.topic_list = get_topic_list()
        for info in self.topic_list:
            print(info[0])
        rclpy.shutdown()

    # def destroy(self):
    #     self.logger.destroy_node()
    #     rclpy.shutdown()
    #     print('everything are destroyed ;) ')


def get_topic_list():
    rclpy.init()

    node_dummy = Node("node_to_show_topic_list")
    topic_list = node_dummy.get_topic_names_and_types()
    node_dummy.destroy_node()
    for info in topic_list:
        print(info[0])
    rclpy.shutdown()

    return topic_list


def get_topic_list_via_nodes():
    topic_info_list = list()
    rclpy.init()
    node = rclpy.create_node('node_to_show_topic_list')

    time.sleep(3)

    names = node.get_node_names()
    print('names: {}'.format(names))

    for item in names:

        info = node.get_publisher_names_and_types_by_node(item, "")
        print('info: {}'.format(info), '\n')
        for topic in info:
            topic_info_dict = dict()
            topic_info_dict.update({'name': topic[0]})
            msg_type = ''.join(topic[1]).replace('/','.')
            # msg_type = str(topic[1]).replace('/','.').replace('[','').replace(']','').replace('\'','')
            topic_info_dict.update({'type': msg_type})
            # TODO: изменить или дополнить принцип заполнения qos
            topic_info_dict.update({'qos': 10})

            topic_info_list.append(topic_info_dict)

    node.destroy_node()
    rclpy.shutdown()

    return topic_info_list

