import sys
from time import sleep

from utils.send_packets import send_tcp_syn, send_tcp_synack, send_tcp_ack, send_tcp_pshack_data, send_tcp_ack_data, send_tcp_finack


def smtp_simulate(source_ip, target_ip, source_port, target_port):
    """
    smtp协议仿真流量生成
    smtp自动机：
    0:BEGIN
    1:SHAKEHAND1_SYN_SENT（一次握手）
    2:SHAKEHAND2_SYN_ACK_SENT（两次握手）
    3:SHAKEHAND3_ACK_SENT（三次握手）
    4:SERVER_220_SENT
    5:CLIENT_EHLO_SENT
    6:SERVER_250_SENT1
    7:CLIENT_AUTH_SENT
    8:SERVER_235_SENT
    9:CLIENT_MAIL_FROM_SENT
    10:SERVER_250_SENT2
    11:CLIENT_RCPT_TO_SENT
    12:SERVER_250_SENT3
    13:CLIENT_DATA_SENT
    14:SERVER_354_SENT
    15:CLIENT_MESSAGE_SENT
    16:SERVER_250_SENT4
    17:CLIENT_QUIT_SENT
    18:SERVER_221_SENT
    19:SHAKEHAND1_FIN_SENT（一次挥手）
    20:SHAKEHAND2_ACK_SENT（两次挥手）
    21:SHAKEHAND3_FIN_SENT（三次挥手）
    22:SHAKEHAND4_ACK_SENT（四次挥手）
    23:CLOSED
    """

    state = {'describe': 'BEGIN', 'num': 0, 'source_ip': source_ip, 'target_ip': target_ip, 'source_port': source_port,
             'target_port': target_port}
    print(str(state['num']) + ":" + state['describe'])

    begin_time = 50.709346  # 发送邮件的第一个包的初始时间

    # 建立连接
    # 一次握手
    send_tcp_syn(source_ip, target_ip, source_port, target_port, 0, 0)
    state['describe'] = 'SHAKEHAND1_SYN_SENT'
    state['num'] = 1
    print(str(state['num']) + ":" + state['describe'])

    # 两次握手
    sleep(50.770175 - begin_time)
    send_tcp_synack(target_ip, source_ip, target_port, source_port, 0, 1)
    state['describe'] = 'SHAKEHAND2_SYN_ACK_SENT'
    state['num'] = 2
    print(str(state['num']) + ":" + state['describe'])

    # 三次握手
    sleep(50.770249 - 50.770175)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 1, 1)
    state['describe'] = 'SHAKEHAND3_ACK_SENT'
    state['num'] = 3
    print(str(state['num']) + ":" + state['describe'])

    # tcp连接建立后，服务端返回应答码220，并提供服务端的域名
    sleep(50.854170 - 50.770249)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 1, 1,
                     '220 newxmesmtplogicsvrszc6.qq.com XMail Esmtp QQ Mail Server.\r\n')
    state['describe'] = 'SERVER_220_SENT'
    state['num'] = 4
    print(str(state['num']) + ":" + state['describe'])

    # 客户端发送EHLO命令，启动SMTP会话
    sleep(50.859849 - 50.854170)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1, 64,
                     'EHLO LAPTOP-OUDFRK43\r\n')
    state['describe'] = 'CLIENT_EHLO_SENT'
    state['num'] = 5
    print(str(state['num']) + ":" + state['describe'])

    sleep(50.920172 - 50.859849)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 64, 23)

    # 服务端响应应答码250，通知客户端建立会话成功
    sleep(50.922184 - 50.920172)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 64, 23,
                     '250-newxmesmtplogicsvrszc6.qq.com\r\n'
                     '250-PIPELINING\r\n'
                     '250-SIZE 73400320\r\n'
                     '250-STARTTLS\r\n'
                     '250-AUTH LOGIN PLAIN XOAUTH XOAUTH2\r\n'
                     '250-AUTH=LOGIN\r\n'
                     '250-MAILCOMPRESS\r\n'
                     '250 8BITMIME\r\n')
    state['describe'] = 'SERVER_250_SENT1'
    state['num'] = 6
    print(str(state['num']) + ":" + state['describe'])

    # 客户端发送身份确认请求AUTH
    sleep(50.922516 - 50.922184)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 23, 233,
                     'AUTH XOAUTH2 dXNlcj0xMDYzNjk1MzM0QHFxLmNvbQFhdXRoPUJlYXJlciBBQVRKSlk0RUFBQUJBQUFBQUFBYjFvNndWR2I2SkxuVUpmUXlZaUFBQUFCTk1SMk5OUXJjVENmOFFUV2NJTWg1cEtZejdpSVdTR3czUWlHMlNnK25EQ0VudWtQYjhjWERBRkd2anhmcEUrVmRCS1o3VlNhUTJSZ1h5aitGMmtFQS9hTFFva21zdDdUTy93ZkRIbzJXRVBqTnNzNHFuQkx0bGdOakpXYklRdEwvMGtjMndiVTRXcG9KK29BK0ZsVG5tZXJTTXk0U2R6SzdGMWpTL0s1cwEB\r\n')
    state['describe'] = 'CLIENT_AUTH_SENT'
    state['num'] = 7
    print(str(state['num']) + ":" + state['describe'])

    sleep(51.020120 - 50.922516)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 233, 370)

    # 服务端响应应答码235，通知客户端身份验证成功
    sleep(51.172180 - 51.020120)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 233, 370,
                     '235 2.7.0 Accepted\r\n')
    state['describe'] = 'SERVER_235_SENT'
    state['num'] = 8
    print(str(state['num']) + ":" + state['describe'])

    # 邮件传送
    # 客户端发送“MAIL FROM”通知服务端发信人的邮箱与域名
    sleep(51.175518 - 51.172180)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 370, 253,
                     'MAIL FROM: <1063695334@qq.com> SIZE=1042\r\n')
    state['describe'] = 'CLIENT_MAIL_FROM_SENTT'
    state['num'] = 9
    print(str(state['num']) + ":" + state['describe'])

    sleep(51.234191 - 51.175518)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 253, 412)

    # 服务端向客户端响应“250”
    sleep(51.278196 - 51.234191)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 253, 412,
                     '250 OK\r\n')
    state['describe'] = 'SERVER_250_SENT2'
    state['num'] = 10
    print(str(state['num']) + ":" + state['describe'])

    # 客户端发送“RCPT TO”命令向服务端告知收信人的邮箱与域名
    sleep(51.278379 - 51.278196)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 412, 261,
                     'RCPT TO: <3268130899@qq.com>\r\n')
    state['describe'] = 'CLIENT_RCPT_TO_SENT'
    state['num'] = 11
    print(str(state['num']) + ":" + state['describe'])

    sleep(51.338145 - 51.278379)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 261, 442)

    # 服务端向客户端响应“250”
    sleep(51.426133 - 51.338145)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 261, 442,
                     '250 OK\r\n')
    state['describe'] = 'SERVER_250_SENT3'
    state['num'] = 12
    print(str(state['num']) + ":" + state['describe'])

    # 客户端发送“DATA”命令进行报文传送初始化
    sleep(51.426493 - 51.426133)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 442, 269,
                     'DATA\r\n')
    state['describe'] = 'CLIENT_DATA_SENT'
    state['num'] = 13
    print(str(state['num']) + ":" + state['describe'])

    sleep(51.486182 - 51.426493)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 269, 448)

    # 服务端响应“354”，表示可以进行邮件输入了
    sleep(51.494184 - 51.486182)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 269, 448,
                     '354 End data with <CR><LF>.<CR><LF>.\r\n')
    state['describe'] = 'SERVER_354_SENT'
    state['num'] = 14
    print(str(state['num']) + ":" + state['describe'])

    # 客户端发送报文内容，每行以CR与LF终止，报文以只有一个“.”的行终止
    sleep(51.494337 - 51.494184)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 448, 307,
                     'Date: Thu, 17 Mar 2022 17:12:57 +0800\r\n'
                     'From: "1063695334@qq.com" <1063695334@qq.com>\r\n'
                     'To: 3268130899 <3268130899@qq.com>\r\n'
                     'Subject: theme\r\n'
                     'X-Priority: 3\r\n'
                     'X-GUID: D5B8E636-7962-45EA-97DD-3DF7455E0A90\r\n'
                     'X-Has-Attach: no\r\n'
                     'X-Mailer: Foxmail 7.2.23.116[cn]\r\n'
                     'Mime-Version: 1.0\r\n'
                     'Message-ID: <202203171712565875013@qq.com>\r\n'
                     'Content-Type: multipart/alternative;\r\n'
                     '\tboundary="----=_001_NextPart364880214656_=----"\r\n'
                     '\r\n')
    state['describe'] = 'CLIENT_MESSAGE_SENT'
    state['num'] = 15
    print(str(state['num']) + ":" + state['describe'])

    sleep(51.592188 - 51.494337)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 307, 852)

    sleep(51.592246 - 51.592188)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 852, 307,
                     'This is a multi-part message in MIME format.\r\n'
                     '\r\n'
                     '------=_001_NextPart364880214656_=----\r\n'
                     'Content-Type: text/plain;\r\n'
                     '\tcharset="us-ascii"\r\n'
                     'Content-Transfer-Encoding: base64\r\n'
                     '\r\n'
                     'Y29udGVudA==\r\n'
                     '\r\n'
                     '------=_001_NextPart364880214656_=----\r\n'
                     'Content-Type: text/html;\r\n'
                     '\tcharset="us-ascii"\r\n'
                     'Content-Transfer-Encoding: quoted-printable\r\n'
                     '\r\n'
                     '<html><head><meta http-equiv=3D"content-type" content=3D"text/html; charse=\r\n'
                     't=3Dus-ascii"><style>body { line-height: 1.5; }body { font-size: 14px; fon=\r\n'
                     't-family: "Microsoft YaHei UI"; color: rgb(0, 0, 0); line-height: 1.5; }</=\r\n'
                     'style></head><body>content</body></html>\r\n'
                     '------=_001_NextPart364880214656_=------\r\n'
                     '\r\n'
                     '.\r\n')

    sleep(51.650761 - 51.592246)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 307, 1495)

    # 服务端向客户端响应“250”
    sleep(52.004184 - 51.650761)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 307, 1495,
                     '250 OK: queued as.\r\n')
    state['describe'] = 'SERVER_250_SENT4'
    state['num'] = 16
    print(str(state['num']) + ":" + state['describe'])

    # 连接释放
    # SMTP客户端发送“QUIT”命令,释放连接
    sleep(52.004906 - 52.004184)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1495, 327,
                     'QUIT\r\n')
    state['describe'] = 'CLIENT_QUIT_SENT'
    state['num'] = 17
    print(str(state['num']) + ":" + state['describe'])

    sleep(52.062313 - 52.004906)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 327, 1501)

    # 服务端响应“221”
    sleep(52.066183 - 52.062313)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 327, 1501,
                     '221 Bye.\r\n')
    state['describe'] = 'SERVER_221_SENT'
    state['num'] = 18
    print(str(state['num']) + ":" + state['describe'])

    # 第一次挥手
    sleep(52.068206 - 52.066183)
    send_tcp_finack(target_ip, source_ip, target_port, source_port, 337, 1501)
    state['describe'] = 'SHAKEHAND1_FIN_SENT'
    state['num'] = 19
    print(str(state['num']) + ":" + state['describe'])

    # 第二次挥手
    sleep(52.068258 - 52.068206)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 1501, 338)
    state['describe'] = 'SHAKEHAND2_ACK_SENT'
    state['num'] = 20
    print(str(state['num']) + ":" + state['describe'])

    # 第三次挥手
    sleep(52.404639 - 52.068258)
    send_tcp_finack(source_ip, target_ip, source_port, target_port, 1501, 338)
    state['describe'] = 'SHAKEHAND3_FIN_SENT'
    state['num'] = 21
    print(str(state['num']) + ":" + state['describe'])

    # 第四次挥手，断开连接
    sleep(2.906513 - 2.902224)  # 捕获的包中没有第四次挥手，所以使用http协议的时间间隔进行模拟
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 338, 1502)
    state['describe'] = 'SHAKEHAND4_ACK_SENT'
    state['num'] = 22
    print(str(state['num']) + ":" + state['describe'])

    state['describe'] = 'CLOSED'
    state['num'] = 23
    print(str(state['num']) + ":" + state['describe'])

    return state


if __name__ == '__main__':
    # state = smtp_simulate('101.132.158.80', '101.132.158.100', 52037, 25)
    source_ip = sys.argv[1]
    target_ip = sys.argv[2]
    source_port = sys.argv[3]
    target_port = sys.argv[4]
    state = smtp_simulate(source_ip, target_ip, int(source_port), int(target_port))
    if state['describe'] == 'CLOSED':
        print("Successfully simulate SMTP protocol once")
        print("source_ip:" + state['source_ip'])
        print("target_ip:" + state['target_ip'])
        print("source_port:" + str(state['source_port']))
        print("target_port:" + str(state['target_port']))
