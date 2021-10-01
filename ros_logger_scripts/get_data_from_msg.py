from copy import deepcopy


def import_msg_lib(types_list):
    msg_to_import = list()
    for msg_type in types_list:
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


def get_data(data_info, parsed_topics_dict):
    topic_name = data_info['name']
    topic_types = data_info['types']
    path_in_msg_structure = data_info['path']
    # print('topic_name list: ', topic_types)

    print('topic name: ', data_info['name'], topic_name)
    topic_msgs = parsed_topics_dict[topic_name]
    print('topic dict keys: ', parsed_topics_dict.keys())
    print('topic dict items: ', parsed_topics_dict.items())
    print('msgs: ', parsed_topics_dict[topic_name])
    msg_w_timestamp_dict = dict()

    import_msg_lib(topic_types)

    for timestamp, msg in topic_msgs.items():
        # msg_path = 'msg.' + path_in_msg_structure
        # print('msg_path: ', path_in_msg_structure)
        required_field_data = msg
        required_field_data = get_field_attribute(path_in_msg_structure, required_field_data)
        # for attr in path_in_msg_structure:
        #     if type(required_field_data) is list:
        #         # тут себя нужно вызвать
        #         for item in required_field_data:
        #             meta_field_data = getattr(item, attr)
        #             required_field_data = deepcopy(meta_field_data)
        #     else:
        #         meta_field_data = getattr(required_field_data, attr)
        #         required_field_data = deepcopy(meta_field_data)
            # required_field_data = getattr(msg, path_in_msg_structure)  # eval(msg_path)  # locate(msg_type)
        msg_w_timestamp_dict.update({timestamp: required_field_data})

    return msg_w_timestamp_dict


def get_field_attribute(path_in_msg_structure, required_field_data):
    # print('path_in_msg_structure: ', path_in_msg_structure)
    for attr_index, attr in enumerate(path_in_msg_structure):
        if type(required_field_data) is list:
            new_required_field_data = list()
            new_path = path_in_msg_structure[attr_index:]
            # print('required data: ', required_field_data)
            for item in required_field_data:
                # print('Im call myself')
                new_required_field_data.append(get_field_attribute(new_path, item))
            required_field_data = deepcopy(new_required_field_data)

            return required_field_data
        else:
            meta_field_data = getattr(required_field_data, attr)
            required_field_data = deepcopy(meta_field_data)

    return required_field_data
