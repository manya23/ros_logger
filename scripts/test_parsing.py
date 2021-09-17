import rtp_log_parser

if __name__ == '__main__':
    logs_dirs = ['/home/op/RTP_LOGS/01092021/RTP_1/01092021_12_28_48_json/']
    topic_name = '/rtp_1/sgru/mission_task'
    msg_list = rtp_log_parser.get_all_topic_msgs(logs_dirs, topic_name)

    print('messages: ', msg_list)

    # j = json.loads(self.j)
    # for ts in j.keys():
    #     msg = locate('marker_msgs.msg.MissionTask')()
    #     set_message_fields(msg, j[ts])
    #     print('msg: ', msg)