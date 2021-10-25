import json
import time


def save_new_config(selected_topic_list, target_directory):
    """
    Puts all selected topics settings to config file's dictionary. And saves config dictionary to .json to selected directory.
    Dictionary item template:
    { "name": "TOPIC_NAME",
      "type": "TOPIC_TYPE",
      "qos": "QOS_TYPE"
    }
    :param target_directory: directory to save .json file
    :type target_directory: str
    :param selected_topic_list: list with dictionaries that describes topic settings
    :return: nothing
    """
    # TODO: add ability to set QOS type (now its default: rclpy.qos.qos_profile_sensor_data)
    topic_to_config_list = list()
    for topic in selected_topic_list:
        current_topic_dict = dict()
        current_topic_dict.update({"name": topic["name"]})
        current_topic_dict.update({"type": topic["type"]})
        current_topic_dict.update({"qos": topic["qos"]})
        topic_to_config_list.append(current_topic_dict)

    json_config_file_name = 'Config_from_' + str(time.strftime("%H:%M:%S", time.localtime(time.time()))) + \
                            '_with_{num}_topics'.format(num=len(selected_topic_list)) + '.json'

    json_path = target_directory + '/' + json_config_file_name
    with open(json_path, 'w') as json_line:
        json.dump(topic_to_config_list, json_line)

    print('Config file wrote down to ', json_path)
