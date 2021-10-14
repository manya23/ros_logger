import os


def create_folder():
    """
    If not exist crates meta data store folder and saves there scripts to display interactive plots
    :return: path to meta data store folder
    """
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
