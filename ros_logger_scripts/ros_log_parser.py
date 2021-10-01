import _io
import copy

import json
import yaml
import os
import re
from pydoc import locate
import array
import numpy
import time

from rosidl_runtime_py import set_message_fields

import std_msgs.msg
import geometry_msgs.msg
import gis_rtk_msgs.msg
import builtin_interfaces.msg
import sensor_msgs.msg
import tf2_msgs.msg
import rtp_msgs.msg
import nav_msgs.msg
import visualization_msgs.msg
import rcl_interfaces.msg
import marker_msgs.msg


def __get_line(file_handle, line_num):
    """
    Возвращает строку из файла с заданным номером

    :param file_handle: объект файла
    :type file_handle: class '_io.TextIOWrapper'
    :param line_num: номер строки (нумерация с 1)
    :type line_num: int
    :return: строка
    :rtype: str
    """
    for i, line in enumerate(file_handle):
        if i == line_num - 1:
            return line
    return None


def __get_last_line(file_handle):
    """
    Возвращает последнюю строку из файла

    :param file_handle: объект файла
    :type file_handle: class '_io.TextIOWrapper'
    :return: строка
    :rtype: str
    """
    file_handle.seek(-2, os.SEEK_END)
    while file_handle.read(1) != b'\n':
        file_handle.seek(-2, os.SEEK_CUR)
    return file_handle.readline().decode()


def __get_topic_type_from_handle(file_handle):
    """
    Возвращает тип топика лог-файла

    :param file_handle: объект файла
    :type file_handle: class '_io.TextIOWrapper'
    :return: тип топика
    :rtype: str
    """
    try:
        yaml_line = yaml.load(file_handle.readline(), Loader=yaml.FullLoader)
        return yaml_line.get('msg_type')
    except IOError:
        print('Error while open file ' % file_handle.name)
    except yaml.YAMLError:
        print('Error while parsing topic type in file ' % file_handle.name)
    return None


def __get_topic_name_from_handle(file_handle):
    """
    Возвращает имя топика лог-файла

    :param file_handle: объект файла
    :type file_handle: class '_io.TextIOWrapper'
    :return: имя топика
    :rtype: str
    """
    try:
        yaml_line = yaml.load(file_handle.readline(), Loader=yaml.FullLoader)
        return yaml_line.get('topic_name')
    except IOError:
        print('Error while open file ' % file_handle.name)
    except yaml.YAMLError:
        print('Error while parsing topic name in file ' % file_handle.name)
    return None


def __get_all_files_from_dir(dir_path):
    """
    Возвращает список лог-файлов из директории

    :param dir_path: путь к директории
    :type dir_path: str
    :return: список лог-файлов
    :rtype: list
    """
    files_list = list()
    # print('dir_path: ', dir_path)
    print('dir path', dir_path)
    for file in os.listdir(dir_path):
        if os.path.isdir(dir_path + file):
            files_list += __get_all_files_from_dir(dir_path + file)
        else:
            if file.endswith('.txt'):
                files_list.append(dir_path + '/' + file)
    return files_list


def __get_all_files_from_dir_list(log_dir_list):
    """
    Возвращает список всех лог-файлов из списка директорий

    :param log_dir_list: список директорий с лог-файлами
    # :type log_dir_list: list
    :return: список лог-файлов
    :rtype: list
    """
    if type(log_dir_list) is str:
        files_list = __get_all_files_from_dir(log_dir_list)
        return files_list

    files_list = list()
    for log_dir in log_dir_list:
        files_list += __get_all_files_from_dir(log_dir)
    return files_list


# def __remove_rtp_prefix(topic_name):
#     patern = r'/rtp_\d'
#     res_list = re.findall(patern, topic_name)
#     for res in res_list:
#         topic_name = topic_name.replace(res, '')
#     return topic_name


class PrimitiveIdlTypes:
    """
    Описывает страндартные типы переменных IDL
    """
    # Basic types as defined by the IDL specification
    # 7.4.1.4.4.2 Basic Types
    SIGNED_NONEXPLICIT_INTEGER_TYPES = (  # rules (26)
        'short',  # rule (27)
        'long',  # rule (28)
        'long long',  # rule (29)
    )
    UNSIGNED_NONEXPLICIT_INTEGER_TYPES = (  # rules (30)
        'unsigned short',  # rule (31)
        'unsigned long',  # rule (32)
        'unsigned long long',  # rule (33)
    )
    FLOATING_POINT_TYPES = (  # rule (24)
        'float',
        'double',
        'long double',
    )
    CHARACTER_TYPES = (
        'char',  # rule (34)
        'wchar',  # rule (35)
    )
    BOOLEAN_TYPE = (
        'boolean',  # rule (36)
    )
    OCTET_TYPE = (
        'octet',  # rule (37)
    )
    # 7.4.13.4.4 Integers restricted to holding 8-bits of information
    # 7.4.13.4.5 Explicitly-named Integer Types
    SIGNED_EXPLICIT_INTEGER_TYPES = (
        'int8',  # rule (208)
        'int16',  # rule (210)
        'int32',  # rule (211)
        'int64',  # rule (212)
    )
    UNSIGNED_EXPLICIT_INTEGER_TYPES = (
        'uint8',  # rule (209)
        'uint16',  # rule (213)
        'uint32',  # rule (214)
        'uint64',  # rule (215)
    )
    STRING = (
        'string',
    )


def __get_python_type(var_type):
    """
    Возвращает тип переменной python по типу переменной IDL

    :param var_type: тип переменной IDL
    :type var_type: str
    :return: тип переменной python
    :rtype: str
    """
    if var_type in PrimitiveIdlTypes.SIGNED_NONEXPLICIT_INTEGER_TYPES:
        return 'int'
    if var_type in PrimitiveIdlTypes.UNSIGNED_NONEXPLICIT_INTEGER_TYPES:
        return 'int'
    if var_type in PrimitiveIdlTypes.SIGNED_EXPLICIT_INTEGER_TYPES:
        return 'int'
    if var_type in PrimitiveIdlTypes.UNSIGNED_EXPLICIT_INTEGER_TYPES:
        return 'int'
    if var_type in PrimitiveIdlTypes.FLOATING_POINT_TYPES:
        return 'float'
    if var_type in PrimitiveIdlTypes.CHARACTER_TYPES:
        return 'str'
    if var_type in PrimitiveIdlTypes.OCTET_TYPE:
        return 'bytes'
    if var_type in PrimitiveIdlTypes.STRING:
        return 'str'
    if var_type in PrimitiveIdlTypes.BOOLEAN_TYPE:
        return 'bool'
    if 'sequence' in var_type:
        return 'list'
    if 'msgs' in var_type:
        return 'msgs'
    return None


def __get_message_var_types(yaml_dict):
    """
    Возвращает словарь с типами переменных ROS сообщения

    :param yaml_dict: YAML структура с ROS сообщением
    :type yaml_dict: dict
    :return: словарь со структурой имя_переменной: тип переменной
    :rtype: dict
    """
    var_types = dict()
    for key, val in yaml_dict.items():
        pure_key = key.replace("&'_", "").replace("&'", "")
        if pure_key == 'fields_and_field_types':
            val_dict = yaml.load(val, Loader=yaml.FullLoader)
            for var, var_t in val_dict.items():
                var_types.update({var: __get_python_type(var_t)})
    return var_types


def __convert_to_ros_msg(msg_type, dict_msg):
    """
    Преобразует YAML структуру в ROS сообщение

    :param msg_type: тип ROS сообщения
    :type msg_type: str
    :param dict_msg: YAML структура
    :return: ROS сообщение
    """
    ros_msg = locate(msg_type)()
    # print('dict msg type: ', type(dict_msg))
    set_message_fields(ros_msg, dict_msg)

    return ros_msg


def __get_all_mission_tasks(logs_dirs):
    """
    Возвращает список всех найденных маршрутных заданий

    :param logs_dirs: список директорий с лог-файлами
    :type logs_dirs: list
    :return: список МЗ типа marker_msgs.msg.MissionTask
    :rtype: dict
    """
    task_files, topic_files_with_topic_names = __get_all_topic_files(logs_dirs, '/sgru/cur_mission_task')
    task_msgs = dict()
    for task_file in task_files:
        task_msgs.update(__read_all_msgs_from_file(task_file))
    return task_msgs


def __get_topic_type_from_file(file_path):
    """
    Возвращает тип топика лог-файла

    :param file_path: путь к лог-файлу
    :type file_path: str
    :return: тип топика
    :rtype: str
    """
    with open(file_path) as handle:
        handle.readline()
        return __get_topic_type_from_handle(handle)


def __get_topic_name_from_file(file_path):
    """
    Возвращает имя топика лог-файла

    :param file_path: путь к лог-файлу
    :type file_path: str
    :return: имя топика
    :rtype: str
    """
    try:
        with open(file_path) as handle:
            return __get_topic_name_from_handle(handle)
    except IOError:
        print('Error while open file ', file_path)
    return None


def __get_first_and_last_timestamps_from_file(file_path):
    """
    Возвращает первую и последнюю метку времени лог-файла

    :param file_path: путь к файлу
    :type file_path: str
    :return: первая и последняя метки времени (first_t, last_t)
    :return: tuple
    """
    with open(file_path, "rb") as handle:
        try:
            handle.readline()
            handle.readline()
            first_timestamp_line = __get_line(handle, 3)  # first timestamp in 3rd line
            last_timestamp_line = __get_last_line(handle)
            first_yaml = yaml.load(first_timestamp_line, Loader=yaml.FullLoader)
            last_yaml = yaml.load(last_timestamp_line, Loader=yaml.FullLoader)
            return float(list(first_yaml.keys())[0]), float(list(last_yaml.keys())[0])
        except AttributeError:
            return 0.0, 0.0


def __get_all_topic_files(logs_dirs, topic_name, allow_rtp_id=False):
    """
    Возвращает все лог-файлы для указанного топика

    :param logs_dirs: список директорий с лог-файлами
    :type logs_dirs: list
    :param topic_name: имя топика
    :type topic_name: str
    :param allow_rtp_id: учитывать ли префикс РТП в имени топика
    :type allow_rtp_id: bool
    :return: список путей к лог-фалам
    :rtype: list
    """
    topic_files = list()
    topic_files_with_topic_names = dict()
    files_list = __get_all_files_from_dir_list(logs_dirs)
    for file in files_list:
        topic_name_in_file = __get_topic_name_from_file(file)
        # if not allow_rtp_id:
        #     topic_name = __remove_rtp_prefix(topic_name)
        #     topic_name_in_file = __remove_rtp_prefix(topic_name_in_file)
        if topic_name == topic_name_in_file:
            topic_files.append(file)
            topic_files_with_topic_names.update({topic_name: file})

    return topic_files, topic_files_with_topic_names


def __get_ts_from_line(line):
    ts_list = re.findall(r'[0.0-9.0]+"', line)
    if len(ts_list) > 0:
        return float(ts_list[0].split('"')[0])
    else:
        return 0.0


def __get_ros_msg_from_line(line, msg_type):
    # print('line: ', line, '\n', 'msg type: ', msg_type)
    json_line = json.loads(line)
    for ts, msg in json_line.items():
        return ts, __convert_to_ros_msg(msg_type, msg)


def __read_all_msgs_from_file(file_path, ts_min=None, ts_max=None):
    """
    Возвращает список всех ROS сообщений из лог-файла

    :param file_path: путь к лог-файлу
    :type file_path: str
    :return: список ROS сообщений
    :rtype: dict
    """
    msg_list = dict()
    topic_type = __get_topic_type_from_file(file_path)
    line_num = 0
    with open(file_path, encoding='utf8') as handle:
        for line in handle:
            if line_num < 2:
                line_num += 1
                continue
            try:
                ts, ros_msg = __get_ros_msg_from_line(line, topic_type)
                # msg_list.update({ts: ros_msg})
                if ts_min is None and ts_max is None:
                    msg_list.update({ts: ros_msg})
                elif ts_min <= float(ts) < ts_max:
                    msg_list.update({ts: ros_msg})
                elif float(ts) == ts_max:
                    msg_list.update({ts: ros_msg})
                    return msg_list
            except AttributeError:
                continue
    return msg_list


def __read_all_ts_from_file(file_path):
    """
    Возвращает все метки времени из файла

    :param file_path: путь к лог-файлу
    :type file_path: str
    :return: список меток времени сообщений
    :rtype: list
    """
    ts_list = list()  # set()
    line_num = 1
    with open(file_path, encoding='utf8') as handle:
        for line in handle:
            if line_num < 2:
                line_num += 1
                continue
            try:
                ts_list.append(__get_ts_from_line(line))  # add(__get_ts_from_line(line))
            except AttributeError:
                continue
    return ts_list  # list(ts_list)


def __read_msgs_from_file(file_path, dt):
    """
    Возвращает список всех ROS сообщений из лог-файла

    :param file_path: путь к лог-файлу
    :type file_path: str
    :param dt: шаг времени, с которым будут читаться сообщения
    :type dt: float
    :return: список ROS сообщений
    :rtype: dict
    """
    msg_list = dict()
    first_dt, last_dt = __get_first_and_last_timestamps_from_file(file_path)
    cur_dt = copy.deepcopy(first_dt)
    topic_type = __get_topic_type_from_file(file_path)
    line_num = 1
    with open(file_path, encoding='utf8') as handle:
        for line in handle:
            if line_num < 2:
                line_num += 1
                continue
            try:
                ts = __get_ts_from_line(line)
                if ts - cur_dt >= dt:
                    msg_list.update({ts: __get_ros_msg_from_line(line, topic_type)[1]})
                    cur_dt = copy.deepcopy(ts)
            except AttributeError:
                continue
    return msg_list


def get_all_topics_names(log_dir_list):
    """
    Возвращает список имен всех топиков лог-файлов

    :param log_dir_list: список директорий с лог-файлами
    :type log_dir_list: list
    :return: список топиков
    :rtype: list
    """
    topic_names = set()
    files_list = __get_all_files_from_dir_list(log_dir_list)
    for file in files_list:
        topic_names.add(__get_topic_name_from_file(file))
    return list(topic_names)


def import_all_required_libraries(dir_path):
    msg_to_import = list()
    # get list of modules that has to be imported from topic msg types
    topic_file_path = __get_all_files_from_dir_list(dir_path)
    for topic_path in topic_file_path:
        msg_type = __get_topic_type_from_file(topic_path)
        msg_type_module_name = str()
        for char in msg_type:
            if char != '.':
                msg_type_module_name += char
            else:
                break
        msg_to_import.append(msg_type_module_name)
    # import required modules
    for module in msg_to_import:
        globals()[module] = __import__(module)


def get_all_topic_ts(logs_dirs, topic_name):
    """
    Возвращает список месток времени для топика

    :param logs_dirs: список директорий с лог-файлами
    :type logs_dirs: list
    :param topic_name: имя топика
    :type topic_name: str
    :return: список меток времени сообщений
    :rtype: list
    """
    ts_list = list()
    topic_files, topic_files_with_name = __get_all_topic_files(logs_dirs, topic_name, allow_rtp_id=True)
    for file in topic_files:
        print('file from get_all_topic_ts: ', file)
        ts_list += __read_all_ts_from_file(file)
    return ts_list


def get_all_topic_msgs(logs_dirs, topic_name, ts_min, ts_max, allow_rtp_id=False, dt=None):
    """
    Возвращает все сообщения для указанного топика

    :param logs_dirs: список директорий с лог-файлами
    :type logs_dirs: list
    :param topic_name: имя топика
    :type topic_name: str
    :param ts_min:
    :param ts_max:
    :param allow_rtp_id: учитывать ли префикс РТП в названиии топика
    :type allow_rtp_id: bool
    :param dt: шаг времени между сообщениями
    :type dt: float
    :return: словарь с метками времени и сообщениями
    :rtype: dict
    """
    topic_msgs = dict()
    parsed_topic_list = list()

    import_all_required_libraries(logs_dirs)

    topic_files, topic_files_with_name = __get_all_topic_files(logs_dirs, topic_name, allow_rtp_id)
    for topic_file_name in topic_files_with_name:
        topic_file = topic_files_with_name[topic_file_name]
        if topic_file_name not in parsed_topic_list:
            # start = time.time()
            if dt is None:
                topic_msgs.update(__read_all_msgs_from_file(topic_file, ts_min, ts_max))
            else:
                topic_msgs.update(__read_msgs_from_file(topic_file, dt))
            # end = time.time()
            # print("get_all_topic_msgs, topic = ", topic_name, " , dt = ", end - start)
            parsed_topic_list.append(topic_file_name)
        else:
            pass
    return topic_msgs


def get_all_topic_msg_type_pair(dir_path):
    available_topic_dict = dict()
    # print('dir path ', dir_path)
    topic_file_path = __get_all_files_from_dir_list(dir_path)
    for topic in topic_file_path:
        topic_name = __get_topic_name_from_file(topic)
        topic_type = __get_topic_type_from_file(topic)
        available_topic_dict.update({topic_name: topic_type})

    return available_topic_dict


def get_all_ts_from_few_topic(log_dir, topic_names_list):
    """
    Возвращает список всех timestamp для выбранных топиков из директорий
    """
    all_available_ts = list()
    print(topic_names_list)
    for topic_name in topic_names_list:
        topic_ts_list = get_all_topic_ts(list([log_dir]), topic_name)
        all_available_ts.extend(topic_ts_list)

    final_list = list(set(all_available_ts))
    final_list.sort(key=float)
    print('msg list: ', final_list[1:])
    return final_list[1:]

