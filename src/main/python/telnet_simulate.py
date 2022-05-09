import binascii
import sys
from time import sleep

from utils.send_packets import send_tcp_syn, send_tcp_synack, send_tcp_ack, send_tcp_pshack_data,  send_tcp_finack


def telnet_simulate(source_ip, target_ip, source_port, target_port):
    """
    telnet协议仿真流量生成
    telnet自动机：
    0:BEGIN
    1:SHAKEHAND1_SYN_SENT（一次握手）
    2:SHAKEHAND2_SYN_ACK_SENT（两次握手）
    3:SHAKEHAND3_ACK_SENT（三次握手）
    4:SERVER_CLIENT_EXCHANGE_MESSAGE
    5:SERVER_WAIT_INPUT_NAME
    6:CLIENT_INPUT_NAME_AND_SERVER_AUTH
    7:SERVER_WAIT_INPUT_PASSWORD
    8:CLIENT_INPUT_PASSWORD
    9:SERVER_LAST_LOGIN_AND_WELCOME
    10:SERVER_WAIT_COMMAND
    11:SHAKEHAND1_FIN_SENT（一次挥手）
    12:SHAKEHAND2_ACK_SENT（两次挥手）
    13:SHAKEHAND3_FIN_SENT（三次挥手）
    14:SHAKEHAND4_ACK_SENT（四次挥手）
    15:CLOSED
    """

    state = {'describe': 'BEGIN', 'num': 0, 'source_ip': source_ip, 'target_ip': target_ip, 'source_port': source_port,
             'target_port': target_port}
    print(str(state['num']) + ":" + state['describe'])

    begin_time = 40.094536

    # 建立连接
    # 一次握手
    send_tcp_syn(source_ip, target_ip, source_port, target_port, 0, 0)
    state['describe'] = 'SHAKEHAND1_SYN_SENT'
    state['num'] = 1
    print(str(state['num']) + ":" + state['describe'])

    # 两次握手
    sleep(40.456943 - begin_time)
    send_tcp_synack(target_ip, source_ip, target_port, source_port, 0, 1)
    state['describe'] = 'SHAKEHAND2_SYN_ACK_SENT'
    state['num'] = 2
    print(str(state['num']) + ":" + state['describe'])

    # 三次握手
    sleep(40.457071 - 40.456943)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 1, 1)
    state['describe'] = 'SHAKEHAND3_ACK_SENT'
    state['num'] = 3
    print(str(state['num']) + ":" + state['describe'])

    # TCP连接建立后,主机和虚拟机相互交换一些信息,包括服务端的配置信息,主机的应答,是否需要登录等等,并且间断使用TCP
    sleep(41.467972 - 40.457071)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 1, 1,
                         binascii.unhexlify(
                             'fffd18fffd20fffd23fffd27'
                         ))

    sleep(41.468240 - 41.467972)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1, 13,
                         binascii.unhexlify(
                             'fffb18fffb1f'
                         ))

    sleep(41.509976 - 41.468240)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 13, 7)

    # sleep(41.509976 - 41.509976)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 13, 7,
                         binascii.unhexlify(
                             'fffd1f'
                         ))

    sleep(41.510098 - 41.509976)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 7, 16,
                         binascii.unhexlify(
                             'fffc20fffc23fffb27'
                         ))

    sleep(41.552308 - 41.510098)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 16, 16,
                         binascii.unhexlify(
                             'fffa2701fff0fffa1801fff0'
                         ))

    sleep(41.552452 - 41.552308)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 16, 28,
                         binascii.unhexlify(
                             'fffa1f0078001efff0'
                         ))

    sleep(41.634112 - 41.552452)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 28, 25)

    sleep(41.634170 - 41.634112)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 25, 28,
                         binascii.unhexlify(
                             'fffa2700fff0fffa1800414e5349fff0'
                         ))

    sleep(41.675776 - 41.634170)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 28, 41)

    # sleep(41.675776 - 41.675776)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 28, 41,
                         binascii.unhexlify(
                             'fffb03fffd01fffb05fffd21'
                         ))

    sleep(41.676169 - 41.675776)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 41, 40,
                         binascii.unhexlify(
                             'fffd03'
                         ))

    sleep(41.759463 - 41.676169)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 40, 44)

    sleep(41.759529 - 41.759463)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 44, 40,
                         binascii.unhexlify(
                             'fffb01fffe05fffc21'
                         ))

    sleep(41.801983 - 41.759529)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 40, 53)

    sleep(41.802193 - 41.801983)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 40, 53,
                         binascii.unhexlify(
                             'fffe01fffb010d0a4b65726e656c20342e31382e302d3139332e31342e322e656c385f322e7838365f363420'
                             '6f6e20616e207838365f36340d0a'
                         ))

    sleep(41.802434 - 41.802193)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 53, 98,
                         binascii.unhexlify(
                             'fffc01'
                         ))
    state['describe'] = 'SERVER_CLIENT_EXCHANGE_MESSAGE'
    state['num'] = 4
    print(str(state['num']) + ":" + state['describe'])

    sleep(41.844218 - 41.802434)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 98, 56,
                         binascii.unhexlify(
                             '695a75663666667038616c6f6c756575716c743071775a206c6f67696e3a20'
                         ))

    # 服务器等待输入name
    sleep(41.844287 - 41.844218)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 56, 129,
                         binascii.unhexlify(
                             'fffd01'
                         ))
    state['describe'] = 'SERVER_WAIT_INPUT_NAME'
    state['num'] = 5
    print(str(state['num']) + ":" + state['describe'])

    sleep(41.926130 - 41.844287)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 129, 59)

    # 客户端一个一个字节输入name服务器同时进行确认
    sleep(44.749599 - 41.926130)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 59, 129,
                         'r')

    sleep(44.800310 - 44.749599)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 129, 60)

    sleep(44.800972 - 44.800310)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 129, 60,
                         'r')

    sleep(44.841182 - 44.800972)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 60, 130)

    sleep(44.922273 - 44.841182)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 60, 130,
                         'o')

    sleep(44.965992 - 44.922273)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 130, 61,
                         'o')

    sleep(45.015854 - 44.965992)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 61, 131)

    sleep(45.088307 - 45.015854)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 61, 131,
                         'o')

    sleep(45.132564 - 45.088307)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 131, 62,
                         'o')

    sleep(45.173963 - 45.088307)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 62, 132)

    sleep(45.237353 - 45.173963)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 62, 132,
                         't')

    sleep(45.282989 - 45.237353)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 132, 63,
                         't')
    state['describe'] = 'CLIENT_INPUT_NAME_AND_SERVER_AUTH'
    state['num'] = 6
    print(str(state['num']) + ":" + state['describe'])

    sleep(45.331941 - 45.282989)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 63, 133)

    sleep(45.516874 - 45.331941)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 63, 133,
                         '\r\n')

    sleep(45.558160 - 45.516874)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 133, 65,
                         '\r\n')

    sleep(45.609886 - 45.558160)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 65, 135)

    # 服务器等待客户端输入密码
    sleep(45.654068 - 45.609886)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 135, 65,
                         'Password: ')
    state['describe'] = 'SERVER_WAIT_INPUT_PASSWORD'
    state['num'] = 7
    print(str(state['num']) + ":" + state['describe'])

    # 客户端一个一个字节输入密码
    sleep(45.703801 - 45.654068)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 65, 145)

    sleep(46.712870 - 45.703801)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 65, 145,
                         'Y')

    sleep(46.794482 - 46.712870)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 145, 66)

    sleep(47.080075 - 46.794482)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 66, 145,
                         't')

    sleep(47.122016 - 47.080075)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 145, 67)

    sleep(47.409934 - 47.122016)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 67, 145,
                         '1')

    sleep(47.451409 - 47.409934)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 145, 68)

    sleep(47.983687 - 47.451409)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 68, 145,
                         '9')

    sleep(48.029514 - 47.983687)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 145, 69)

    sleep(48.150448 - 48.029514)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 69, 145,
                         '9')

    sleep(48.192997 - 48.150448)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 145, 70)

    sleep(48.343291 - 48.192997)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 70, 145,
                         '8')

    sleep(48.386224 - 48.343291)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 145, 71)

    sleep(48.705533 - 48.386224)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 71, 145,
                         '1')

    sleep(48.750121 - 48.705533)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 145, 72)

    sleep(48.905562 - 48.750121)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 72, 145,
                         '1')

    sleep(48.948191 - 48.905562)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 145, 73)

    sleep(49.195398 - 48.948191)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 73, 145,
                         '1')

    sleep(49.237141 - 49.195398)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 145, 74)

    sleep(49.453682 - 49.237141)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 74, 145,
                         '9')
    state['describe'] = 'CLIENT_INPUT_PASSWORD'
    state['num'] = 8
    print(str(state['num']) + ":" + state['describe'])

    sleep(49.494970 - 49.453682)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 145, 75)

    sleep(49.981541 - 49.494970)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 75, 145,
                         '\r\n')

    sleep(50.022960 - 49.981541)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 145, 77)

    sleep(50.023181 - 50.022960)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 145, 77,
                         '\r\n')

    sleep(50.077871 - 50.023181)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 77, 147)

    # 登录成功，服务器响应Last Login和welcome信息
    sleep(50.119097 - 50.077871)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 147, 77,
                         'Last login: Wed Apr 27 19:48:35 from ::ffff:111.40.58.241\r\n'
                         '\r\n'
                         'Welcome to Alibaba Cloud Elastic Compute Service !\r\n'
                         '\r\n')
    state['describe'] = 'SERVER_LAST_LOGIN_AND_WELCOME'
    state['num'] = 9
    print(str(state['num']) + ":" + state['describe'])

    sleep(50.170104 - 50.119097)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 77, 262)

    # 服务器等待客户端的新命令
    sleep(50.213279 - 50.170104)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 262, 77,
                         '[root@iZuf6ffp8alolueuqlt0qwZ ~]# ')
    state['describe'] = 'SERVER_WAIT_COMMAND'
    state['num'] = 10
    print(str(state['num']) + ":" + state['describe'])

    sleep(50.262039 - 50.213279)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 77, 296)

    # 使用pop3的时间来模拟三次握手的时间
    # 补全四次挥手
    # 一次挥手
    sleep(56.850089 - 56.840068)
    send_tcp_finack(source_ip, target_ip, source_port, target_port, 77, 296)
    state['describe'] = 'SHAKEHAND1_FIN_SENT'
    state['num'] = 11
    print(str(state['num']) + ":" + state['describe'])

    # 二次挥手
    sleep(56.850146 - 56.850089)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 296, 78)
    state['describe'] = 'SHAKEHAND2_ACK_SENT'
    state['num'] = 12
    print(str(state['num']) + ":" + state['describe'])

    # 三次挥手
    sleep(57.731955 - 56.850146)
    send_tcp_finack(target_ip, source_ip, target_port, source_port, 296, 78)
    state['describe'] = 'SHAKEHAND3_FIN_SENT'
    state['num'] = 13
    print(str(state['num']) + ":" + state['describe'])

    # 四次挥手
    sleep(57.792134 - 57.731955)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 78, 297)
    state['describe'] = 'SHAKEHAND4_ACK_SENT'
    state['num'] = 14
    print(str(state['num']) + ":" + state['describe'])

    state['describe'] = 'CLOSED'
    state['num'] = 15
    print(str(state['num']) + ":" + state['describe'])

    return state


if __name__ == '__main__':
    # state = telnet_simulate('101.132.158.80', '101.132.158.100', 59443, 23)
    source_ip = sys.argv[1]
    target_ip = sys.argv[2]
    source_port = sys.argv[3]
    target_port = sys.argv[4]
    state = telnet_simulate(source_ip, target_ip, int(source_port), int(target_port))
    if state['describe'] == 'CLOSED':
        print("Successfully simulate TELNET protocol once")
        print("source_ip:" + state['source_ip'])
        print("target_ip:" + state['target_ip'])
        print("source_port:" + str(state['source_port']))
        print("target_port:" + str(state['target_port']))
