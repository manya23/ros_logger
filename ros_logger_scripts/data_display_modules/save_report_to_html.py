import os
from ros_logger_scripts.folder_pathes import report_html_template_path, interactive_plot_scripts_folder_path


def write_js_scripts_folder(target_dir_path):
    js_files_list = list([[interactive_plot_scripts_folder_path + '/d3.v5.js', 'd3.v5.js'],
                          [interactive_plot_scripts_folder_path + '/mpld3.v0.5.2.js', 'mpld3.v0.5.2.js']])
    if not os.path.exists(target_dir_path + '/scripts/'):
        os.makedirs(target_dir_path + '/scripts/')
    for js_file in js_files_list:
        if not os.path.exists(target_dir_path + '/scripts/' + js_file[1]):
            with open(js_file[0]) as f:
                lines = f.readlines()
            with open(target_dir_path + '/scripts/' + js_file[1], 'w') as f:
                for line in lines:
                    f.write("%s\n" % line)


def gather_report_parts_to_html(plot_to_save_list, meta_data_folder, report_file_name):
    """
    Saves report with all created plots to meta data folder
    :param report_file_name:
    :param meta_data_folder:
    :param plot_to_save_list: list of html strings
    :return: path to html report file stored at meta data folder
    """
    # all_plots = str()
    # for plot in plot_to_save_list:
    #     all_plots += plot['plot']

    report_name = '{folder_name}{name}'.format(folder_name=meta_data_folder, name=report_file_name)

    report_lines = __fill_report_template(plot_to_save_list, report_file_name)

    __save_report(report_name, report_lines)

    return report_name


def __fill_report_template(all_plots_info, report_title):
    """
    Fill report template with plots and its data.

    :param all_plots_info: dictionary with plot, plot title and plot description
    :return: nothing
    """

    template_lines = __read_template_report(report_html_template_path)

    all_plots = str()
    for plot in all_plots_info:
        all_plots += __fill_one_plot_data(plot)

    plot_lines = str()
    for line in all_plots:
        plot_lines += '{line}'.format(line=str(line))

    report_lines = list()
    for line in template_lines:
        line = line.replace('$Title$', report_title)
        line = line.replace('$Plots$', plot_lines)
        report_lines.append(line)

    return report_lines


def __fill_one_plot_data(plot_data_dict):
    """
    Fills one pert of report with all plot data

    :param plot_data_dict: dictionary with all info for one plot
    :type plot_data_dict: dict
    :return: report part with one plot
    :type return: str
    """
    plot = plot_data_dict['plot']
    plot_title = plot_data_dict['title']
    axis_description = plot_data_dict['axes']

    # fill info table for plot
    report_part_info = '<br>'
    report_part_info += '<table id="t01">'
    report_part_info += '<tr>'
    report_part_info += '<th>Axis name</th><th>Axis data</th><th>Axis data storage</th>'
    report_part_info += '</tr>'
    for key, value in axis_description.items():
        report_part_info += '<tr>'
        report_part_info += '<td>{axis}</td><td>{axis_data}</td><td>{data_dir}</td>'.format(axis=key, axis_data=value[0],
                                                                                            data_dir=value[1])
        report_part_info += '</tr>'
    report_part_info += '</table>'

    # fill main report part
    report_part = str()
    report_part += '<h3>Plot: {title}</h3><br>'.format(title=plot_title)
    report_part += '<table>'
    report_part += '<tr>'
    report_part += '<td>{plot}</td>'.format(plot=plot)
    report_part += '<td>{plot_info}</td>'.format(plot_info=report_part_info)
    report_part += '</tr>'
    report_part += '</table><br>'

    return report_part


def __read_template_report(path):
    with open(path) as f:
        lines = f.readlines()
    return lines


def __save_report(name, report_lines):
    path = name + '.html'
    with open(path, 'w') as f:
        for line in report_lines:
            f.write('%s\n' % line)
