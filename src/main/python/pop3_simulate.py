import sys
from time import sleep

from utils.send_packets import send_tcp_syn, send_tcp_synack, send_tcp_ack, send_tcp_pshack_data, send_tcp_ack_data, send_tcp_finack


def pop3_simulate(source_ip, target_ip, source_port, target_port):
    """
    pop3协议仿真流量生成
    pop3自动机：
    0:BEGIN
    1:SHAKEHAND1_SYN_SENT（一次握手）
    2:SHAKEHAND2_SYN_ACK_SENT（两次握手）
    3:SHAKEHAND3_ACK_SENT（三次握手）
    4:SERVER_READY_SENT
    5:CLIENT_USER_SENT
    6:SERVER_OK_SENT1
    7:CLIENT_PASS_SENT
    8:SERVER_OK_SENT2
    9:CLIENT_STAT_SENT
    10.SERVER_OK_SENT3
    11:CLIENT_LIST_SENT
    12:SERVER_OK_SENT4
    13:CLIENT_UIDL_SENT
    14:SERVER_OK_SENT5
    15:CLIENT_RETR_SENT
    16:SERVER_DATA_SENT
    17:CLIENT_OK_SENT
    18:CLIENT_QUIT_SENT
    19:SERVER_OK_SENT6
    20:SHAKEHAND1_FIN_SENT（一次挥手）
    21:SHAKEHAND2_ACK_SENT（两次挥手）
    22:SHAKEHAND3_FIN_SENT（三次挥手）
    23:SHAKEHAND4_ACK_SENT（四次挥手）
    24:CLOSED
    """

    state = {'describe': 'BEGIN', 'num': 0, 'source_ip': source_ip, 'target_ip': target_ip, 'source_port': source_port,
             'target_port': target_port}
    print(str(state['num']) + ":" + state['describe'])

    begin_time = 55.497125

    # 建立连接
    # 一次握手
    send_tcp_syn(source_ip, target_ip, source_port, target_port, 0, 0)
    state['describe'] = 'SHAKEHAND1_SYN_SENT'
    state['num'] = 1
    print(str(state['num']) + ":" + state['describe'])

    # 两次握手
    sleep(55.559096 - begin_time)
    send_tcp_synack(target_ip, source_ip, target_port, source_port, 0, 1)
    state['describe'] = 'SHAKEHAND2_SYN_ACK_SENT'
    state['num'] = 2
    print(str(state['num']) + ":" + state['describe'])

    # 三次握手
    sleep(55.559176 - 55.559096)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 1, 1)
    state['describe'] = 'SHAKEHAND3_ACK_SENT'
    state['num'] = 3
    print(str(state['num']) + ":" + state['describe'])

    # pop3服务器准备就绪
    sleep(55.621101 - 55.559176)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 1, 1,
                     '+OK XMail POP3 Server v1.0 Service Ready(XMail v1.0)\r\n')
    state['describe'] = 'SERVER_READY_SENT'
    state['num'] = 4
    print(str(state['num']) + ":" + state['describe'])

    # 客户端输入用户名
    sleep(55.621320 - 55.621101)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1, 55,
                     'USER 3268130899@qq.com\r\n')
    state['describe'] = 'CLIENT_USER_SENT'
    state['num'] = 5
    print(str(state['num']) + ":" + state['describe'])

    sleep(55.681103 - 55.621320)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 55, 25)

    sleep(55.687058 - 55.681103)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 55, 25,
                     '+OK\r\n')
    state['describe'] = 'SERVER_OK_SENT1'
    state['num'] = 6
    print(str(state['num']) + ":" + state['describe'])

    # 客户端输入密码
    sleep(55.687290 - 55.687058)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 25, 60,
                     'PASS bigyhlolsfzycjdb\r\n')
    state['describe'] = 'CLIENT_PASS_SENT'
    state['num'] = 7
    print(str(state['num']) + ":" + state['describe'])

    sleep(55.787663 - 55.687290)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 60, 48)

    sleep(56.293125 - 55.787663)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 60, 48,
                     '+OK\r\n')
    state['describe'] = 'SERVER_OK_SENT2'
    state['num'] = 8
    print(str(state['num']) + ":" + state['describe'])

    # 客户端查看邮箱中的统计信息
    sleep(56.293922 - 56.293125)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 48, 65,
                     'STAT\r\n')
    state['describe'] = 'CLIENT_STAT_SENT'
    state['num'] = 9
    print(str(state['num']) + ":" + state['describe'])

    sleep(56.355062 - 56.293922)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 65, 54)

    sleep(56.393068 - 56.355062)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 65, 54,
                     '+OK 6 26402\r\n')
    state['describe'] = 'SERVER_OK_SENT3'
    state['num'] = 10
    print(str(state['num']) + ":" + state['describe'])

    # 客户端列出邮箱中的邮件信息
    sleep(56.393238 - 56.393068)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 54, 78,
                     'LIST\r\n')
    state['describe'] = 'CLIENT_LIST_SENT'
    state['num'] = 11
    print(str(state['num']) + ":" + state['describe'])

    sleep(56.479125 - 56.393238)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 78, 60,
                     '+OK\r\n'
                     '1 2251\r\n'
                     '2 8535\r\n'
                     '3 8535\r\n'
                     '4 2395\r\n'
                     '5 2291\r\n'
                     '6 2395\r\n'
                     '.\r\n')
    state['describe'] = 'SERVER_OK_SENT4'
    state['num'] = 12
    print(str(state['num']) + ":" + state['describe'])

    # 客户端查询某封邮件的标志符
    sleep(56.479480 - 56.479125)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 60, 134,
                     'UIDL\r\n')
    state['describe'] = 'CLIENT_UIDL_SENT'
    state['num'] = 13
    print(str(state['num']) + ":" + state['describe'])

    sleep(56.561130 - 56.479480)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 134, 66,
                     '+OK\r\n'
                     '1 ZC0017_N2TNDLSMM_gue7kAJEeNJc3\r\n'
                     '2 ZC0018_5bbN4lqMLeYuOPoAZMi0Vc3\r\n'
                     '3 ZC0018_OWrN0mqMNf4uwAIAbN4Vbc3\r\n'
                     '4 ZC0018_uunNrhaMj0QuyAoAkskyfc3\r\n'
                     '5 ZC0018_azjNvASMnVYu3x0AF2cfWc3\r\n'
                     '6 ZC0018_eCvNizOMaKMu9DYAPe_tWc3\r\n'
                     '.\r\n')
    state['describe'] = 'SERVER_OK_SENT5'
    state['num'] = 14
    print(str(state['num']) + ":" + state['describe'])

    # 客户端获取某封邮件
    sleep(56.564278 - 56.561130)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 66, 346,
                     'RETR 6\r\n')
    state['describe'] = 'CLIENT_RETR_SENT'
    state['num'] = 15
    print(str(state['num']) + ":" + state['describe'])

    sleep(56.662063 - 56.564278)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 346, 74)

    # 服务器发送邮件给客户端
    sleep(56.691941 - 56.662063)
    send_tcp_ack_data(target_ip, source_ip, target_port, source_port, 346, 74,
                     '+OK 2395\r\n'
                     'Received: from LAPTOP-OUDFRK43 ([111.42.148.139])\r\n'
                     '\tby newxmesmtplogicsvrszb7.qq.com (NewEsmtp) with SMTP\r\n'
                     '\tid 7E38E045; Fri, 18 Mar 2022 16:31:35 +0800\r\n'
                     'X-QQ-mid: xmsmtpt1647592295ticnj924a\r\n'
                     'Message-ID: <tencent_24D942D72AEEB1271D52541E6DC3D7873307@qq.com>\r\n'
                     'X-QQ-XMAILINFO: Mdc3TkmnJyI/BRmH05+BtqEAwkz3H7lxmsrwpyJ+fp79SU7ypIYsvQYuXg7H6L\r\n'
                     '\t jLjHQCJGi3OjO44F+jg+Q0wn144vfuHF5I5nOreqMg0/LKMea5OHNbhln7s7cHGO74aOUGFaPO+F\r\n'
                     '\t s/iacNQHnFYf3zZKac2vhb5E7ez1J1uwQNb69AW52dShWELaizxUE9JGgd2keiAmb1KLwt6eO2pw\r\n'
                     '\t FLHzdltL615eqZfVRfhHpIXsPIWNWDKx9cfMA85dlGo29veFmLwagR/FpwjnVo9kk3yUKDbCRfGp\r\n'
                     '\t wlaDX1j9AlSq+2q/5jlX1zqzhXiG7Od60BPZ0nscVfRED/BL9m6W4/5sKAGHmWchTwSnY7t8ydLj\r\n'
                     '\t 8ugqUxVjqGrJW+hOVYuNtEQcso5cCL8ifcB5LzsZQz+PlgCj0Dzg8O7vxA/z/DRhlhqfwZOk+bw8\r\n'
                     '\t 3mRvRdauYMYbNeHLF+/2j40yY6gFK7IZwP3yNaCzePWJ1XhAWkBOaWwNGf7iIafBHa7hYn01Ffm6\r\n'
                     '\t FHKjZ8DuPmldoLNifblvVpakczuV81quyrqP2UwoOrvZA9aJnyaA0BG5wKpRZ6gTX/MYimnJXRhR\r\n'
                     '\t cRIx3Kuzqw2WXqE/kKLpbNRV6INUatIL+M7M5tv+2eTPnNa5abNjIY/3puMil94Dg8EsypnjAkx3\r\n'
                     '\t KXuGDZi8jsQMZcCWaWsLn/0MTy5s7bwEHYNQnrllQJ+KUhDNmkFyPKeAis0Aufa/Yuxebl1KS/3t\r\n'
                     '\t J0I5c4hPPBkdd5zncJt8366qGet3tk+toof81jlzyk8Z9T7QeupeWCEXEaiXABXJCKblFnhzkmIf\r\n'
                     '\t Bw6GVdIZTD4yUlV/yPnFEnerFi2zWCjrrQtXdzgdQrMu7a57yc+PZyPLezi/HsYYq9IqzHIME+KX\r\n'
                     '\t gldT1hglDuSRmc+Vt4t/6nLeioaqICXli4Y4bieEhpIs+wUo19xZFRiZRTnR6SQ5z+rAXY9H2oSj\r\n'
                     '\t FuILJkg5E=\r\n'
                     'Date: Fri, 18 Mar 2022 16:31:31 +0800')

    sleep(56.692463 - 56.691941)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 1706, 74,
                     '\r\nFrom: "1063695334@qq.com" <1063695334@qq.com>\r\n'
                     'To: 3268130899 <3268130')

    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 1778, 74,
                     '899@qq.com>\r\n'
                     'Subject: PopTheme\r\n'
                     'X-Priority: 3\r\n'
                     'X-GUID: 096D5C66-F5A9-47D3-B5A7-DFAAB226F404\r\n'
                     'X-Has-Attach: no\r\n'
                     'X-Mailer: Foxmail 7.2.23.116[cn]\r\n'
                     'Mime-Version: 1.0\r\n'
                     'X-OQ-MSGID: <202203181631310967556@qq.com>\r\n'
                     'Content-Type: multipart/alternative;\r\n'
                     '\tboundary="----=_001_NextPart047566706231_=----"\r\n'
                     '\r\n'
                     'This is a multi-part message in MIME format.\r\n'
                     '\r\n'
                     '------=_001_NextPart047566706231_=----\r\n'
                     'Content-Type: text/plain;\r\n'
                     '\tcharset="us-ascii"\r\n'
                     'Content-Transfer-Encoding: base64\r\n'
                     '\r\n'
                     'UG9wQ29udGVudA0K\r\n'
                     '\r\n'
                     '------=_001_NextPart047566706231_=----\r\n'
                     'Content-Type: text/html;\r\n'
                     '\tcharset="us-ascii"\r\n'
                     'Content-Transfer-Encoding: quoted-printable\r\n'
                     '\r\n'
                     '<html><head><meta http-equiv=3D"content-type" content=3D"text/html; charse=\r\n'
                     't=3Dus-ascii"><style>body { line-height: 1.5; }body { font-size: 14px; fon=\r\n'
                     't-family: "Microsoft YaHei UI"; color: rgb(0, 0, 0); line-height: 1.5; }</=\r\n'
                     'style></head><body>=0A<div><span></span>PopContent</div>=0A</body></html>\r\n'
                     '------=_001_NextPart047566706231_=------\r\n'
                     '\r\n'
                     '.\r\n')
    state['describe'] = 'SERVER_DATA_SENT'
    state['num'] = 16
    print(str(state['num']) + ":" + state['describe'])

    # 客户端收到邮件，回复ack
    sleep(56.692531 - 56.692463)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 74, 2756)
    state['describe'] = 'CLIENT_OK_SENT'
    state['num'] = 17
    print(str(state['num']) + ":" + state['describe'])

    # 客户端结束邮件接收，断开连接
    sleep(56.714497 - 56.692531)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 74, 2756,
                     'QUIT\r\n')
    state['describe'] = 'CLIENT_QUIT_SENT'
    state['num'] = 18
    print(str(state['num']) + ":" + state['describe'])

    sleep(56.773914 - 56.714497)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 2756, 80)

    sleep(56.840068 - 56.773914)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 2756, 80,
                     '+OK Bye\r\n')
    state['describe'] = 'SERVER_OK_SENT6'
    state['num'] = 19
    print(str(state['num']) + ":" + state['describe'])

    # 一次挥手
    sleep(56.850089 - 56.840068)
    send_tcp_finack(target_ip, source_ip, target_port, source_port, 2765, 80)
    state['describe'] = 'SHAKEHAND1_FIN_SENT'
    state['num'] = 20
    print(str(state['num']) + ":" + state['describe'])

    # 二次挥手
    sleep(56.850146 - 56.850089)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 80, 2766)
    state['describe'] = 'SHAKEHAND2_ACK_SENT'
    state['num'] = 21
    print(str(state['num']) + ":" + state['describe'])

    # 三次挥手
    sleep(57.731955 - 56.850146)
    send_tcp_finack(source_ip, target_ip, source_port, target_port, 80, 2766)
    state['describe'] = 'SHAKEHAND3_FIN_SENT'
    state['num'] = 22
    print(str(state['num']) + ":" + state['describe'])

    # 四次挥手
    sleep(57.792134 - 57.731955)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 2766, 81)
    state['describe'] = 'SHAKEHAND4_ACK_SENT'
    state['num'] = 23
    print(str(state['num']) + ":" + state['describe'])

    state['describe'] = 'CLOSED'
    state['num'] = 24
    print(str(state['num']) + ":" + state['describe'])

    return state


if __name__ == '__main__':
    # state = pop3_simulate('101.132.158.80', '101.132.158.100', 58999, 110)
    source_ip = sys.argv[1]
    target_ip = sys.argv[2]
    source_port = sys.argv[3]
    target_port = sys.argv[4]
    state = pop3_simulate(source_ip, target_ip, int(source_port), int(target_port))
    if state['describe'] == 'CLOSED':
        print("Successfully simulate POP3 protocol once")
        print("source_ip:" + state['source_ip'])
        print("target_ip:" + state['target_ip'])
        print("source_port:" + str(state['source_port']))
        print("target_port:" + str(state['target_port']))