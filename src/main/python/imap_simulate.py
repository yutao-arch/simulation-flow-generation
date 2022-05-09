import sys
from time import sleep

from utils.send_packets import send_tcp_syn, send_tcp_synack, send_tcp_ack, send_tcp_pshack_data, send_tcp_ack_data, send_tcp_finack


def imap_simulate(source_ip, target_ip, source_port, target_port):
    """
    imap协议仿真流量生成
    imap自动机：
    0:BEGIN
    1:SHAKEHAND1_SYN_SENT（一次握手）
    2:SHAKEHAND2_SYN_ACK_SENT（两次握手）
    3:SHAKEHAND3_ACK_SENT（三次握手）
    4:SERVER_OK_SENT
    5:CLIENT_NOOP_SENT
    6:SERVER_OK_NOOP_SENT
    7:CLIENT_STATUS_INBOX_SENT
    8:SERVER_OK_STATUS_SENT
    9:CLIENT_NOOP_SENT2
    10.SERVER_OK_NOOP_SENT2
    11:CLIENT_CAPABILITY_SENT
    12:SERVER_OK_CAPABILITY_SENT
    13:CLIENT_ID_SENT
    14:SERVER_OK_ID_SENT
    15:CLIENT_SELECT_INBOX_SENT
    16:SERVER_OK_SELECT_SENT
    17:CLIENT_FETCH_SENT
    18:SERVER_OK_FETCH_SENT
    19:CLIENT_UID_FETCH_SENT
    20:SERVER_DATA_SENT
    21:SHAKEHAND1_FIN_SENT（一次挥手）
    22:SHAKEHAND2_ACK_SENT（两次挥手）
    23:SHAKEHAND3_FIN_SENT（三次挥手）
    24:SHAKEHAND4_ACK_SENT（四次挥手）
    25:CLOSED
    """
    # 邮件客户端是多线程收邮件的(在我的例子中有一个端口用于建立tcp连接，还有三个端口收取邮件)，
    # 所以对于单独的一个端口收取邮件需要补充三次握手和四次挥手（用一个端口实现所有功能）

    state = {'describe': 'BEGIN', 'num': 0, 'source_ip': source_ip, 'target_ip': target_ip, 'source_port': source_port,
             'target_port': target_port}
    print(str(state['num']) + ":" + state['describe'])

    begin_time = 55.497125  # 使用pop3的时间来模拟三次握手的时间

    # 补充三次握手
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

    # imap服务器准备就绪(源数据中是另外一个端口实现的，在这融合进来)
    sleep(55.621101 - 55.559176)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 1, 1,
                         '* OK [CAPABILITY IMAP4 IMAP4rev1 ID AUTH=PLAIN AUTH=LOGIN AUTH=XOAUTH2 NAMESPACE] QQMail XMIMAP4Server ready\r\n')
    state['describe'] = 'SERVER_OK_SENT'
    state['num'] = 4
    print(str(state['num']) + ":" + state['describe'])

    # 客户端向服务器发送NOOP命令，与服务器保持连接，可以随时获取新邮件或者消息状态更新
    sleep(55.621320 - 55.621101)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1, 111,
                         'C87 NOOP\r\n')
    state['describe'] = 'CLIENT_NOOP_SENT'
    state['num'] = 5
    print(str(state['num']) + ":" + state['describe'])

    sleep(25.956027 - 25.891995)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 111, 11)

    sleep(25.973686 - 25.956027)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 111, 11,
                         'C87 OK NOOP Completed\r\n')
    state['describe'] = 'SERVER_OK_NOOP_SENT'
    state['num'] = 6
    print(str(state['num']) + ":" + state['describe'])

    # 客户端向服务器发送STATUS命令，邮件服务器返回指定邮箱文件夹的状态
    sleep(25.975571 - 25.973686)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 11, 134,
                         'C88 STATUS "INBOX" (MESSAGES RECENT UIDVALIDITY)\r\n')
    state['describe'] = 'CLIENT_STATUS_INBOX_SENT'
    state['num'] = 7
    print(str(state['num']) + ":" + state['describe'])

    sleep(26.050307 - 25.975571)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 134, 61,
                         '* STATUS "INBOX" (MESSAGES 3 RECENT 0 UIDVALIDITY 1633979026)\r\n'
                         'C88 OK STATUS completed\r\n')
    state['describe'] = 'SERVER_OK_STATUS_SENT'
    state['num'] = 8
    print(str(state['num']) + ":" + state['describe'])

    sleep(26.052942 - 26.050307)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 61, 222,
                         'C89 NOOP\r\n')
    state['describe'] = 'CLIENT_NOOP_SENT2'
    state['num'] = 9
    print(str(state['num']) + ":" + state['describe'])

    sleep(26.124753 - 26.052942)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 222, 71,
                         'C89 OK NOOP Completed\r\n')
    state['describe'] = 'SERVER_OK_NOOP_SENT2'
    state['num'] = 10
    print(str(state['num']) + ":" + state['describe'])

    # 客户端向服务器发送capability命令，服务器进行响应，返回支持的功能列表
    sleep(26.126693 - 26.124753)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 71, 245,
                         'C90 CAPABILITY\r\n')
    state['describe'] = 'CLIENT_CAPABILITY_SENT'
    state['num'] = 11
    print(str(state['num']) + ":" + state['describe'])

    sleep(26.192689 - 26.126693)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 245, 87,
                         '* CAPABILITY IMAP4 IMAP4rev1 XLIST MOVE IDLE XAPPLEPUSHSERVICE NAMESPACE CHILDREN ID UIDPLUS\r\n'
                         'C90 OK CAPABILITY Completed\r\n')
    state['describe'] = 'SERVER_OK_CAPABILITY_SENT'
    state['num'] = 12
    print(str(state['num']) + ":" + state['describe'])

    sleep(26.195062 - 26.192689)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 87, 368,
                         'C91 ID ("name" "com.tencent.foxmail" "version" "7.2.23.116" "os" "windows" "os-version" "6.2" "vendor" "tencent limited" "contact" "foxmail@foxmail.com")\r\n')
    state['describe'] = 'CLIENT_ID_SENT'
    state['num'] = 13
    print(str(state['num']) + ":" + state['describe'])

    sleep(26.263716 - 26.195062)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 368, 242,
                         '* ID NIL\r\n'
                         'C91 OK ID completed\r\n')
    state['describe'] = 'SERVER_OK_ID_SENT'
    state['num'] = 14
    print(str(state['num']) + ":" + state['describe'])

    # 客户端向服务器发送SELECT命令，选择inbox文件夹
    sleep(26.264150 - 26.263716)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 242, 372,
                         'C92 SELECT "INBOX"\r\n')
    state['describe'] = 'CLIENT_SELECT_INBOX_SENT'
    state['num'] = 15
    print(str(state['num']) + ":" + state['describe'])

    sleep(26.364055 - 26.264150)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 399, 262)

    sleep(26.399867 - 26.364055)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 399, 262,
                         '* 3 EXISTS\r\n'
                         '* 0 RECENT\r\n'
                         '* OK [UNSEEN 1]\r\n'
                         '* OK [UIDVALIDITY 1633979026] UID validity status\r\n'
                         '* OK [UIDNEXT 20] Predicted next UID\r\n'
                         '* FLAGS (\Answered \Flagged \Deleted \Draft \Seen)\r\n'
                         '* OK [PERMANENTFLAGS (\* \Answered \Flagged \Deleted \Draft \Seen)] Permanent flags\r\n'
                         'C92 OK [READ-WRITE] SELECT complete\r\n')
    state['describe'] = 'SERVER_OK_SELECT_SENT'
    state['num'] = 16
    print(str(state['num']) + ":" + state['describe'])

    # 客户端向服务器发送FETCH命令，来检索与消息相关数据
    sleep(26.400965 - 26.364055)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 262, 703,
                         'C93 FETCH 1:3 (UID)\r\n')
    state['describe'] = ':CLIENT_FETCH_SENT'
    state['num'] = 17
    print(str(state['num']) + ":" + state['describe'])

    sleep(26.464768 - 26.400965)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 703, 283)

    sleep(26.560706 - 26.464768)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 703, 283,
                         '* 1 FETCH (UID 5)\r\n'
                         '* 2 FETCH (UID 12)\r\n'
                         '* 3 FETCH (UID 19)\r\n'
                         'C93 OK FETCH Completed\r\n')
    state['describe'] = ':SERVER_OK_FETCH_SENT'
    state['num'] = 18
    print(str(state['num']) + ":" + state['describe'])

    # 客户端向服务端发送UID命令，服务器返回用于fetch的UID列表（获取邮件数据）
    sleep(26.561356 - 26.560706)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 283, 786,
                         'C94 UID FETCH 19 (UID RFC822.SIZE FLAGS BODY.PEEK[HEADER])\r\n')
    state['describe'] = ':CLIENT_UID_FETCH_SENT'
    state['num'] = 19
    print(str(state['num']) + ":" + state['describe'])

    sleep(26.624683 - 26.561356)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 786, 343)

    sleep(26.868824 - 26.624683)
    send_tcp_ack_data(target_ip, source_ip, target_port, source_port, 786, 343,
                      '* 3 FETCH (UID 19 RFC822.SIZE 2400 FLAGS () BODY[HEADER] {1720}\r\n'
                      'Received: from LAPTOP-OUDFRK43 ([111.40.58.171])\r\n'
                      '\tby newxmesmtplogicsvrszb6.qq.com (NewEsmtp) with SMTP\r\n'
                      '\tid CB4298D2; Sun, 24 Apr 2022 17:50:52 +0800\r\n'
                      'X-QQ-mid: xmsmtpt1650793852t3vl05ru6\r\n'
                      'Message-ID: <tencent_184B91007CC9FAFB51033FCB00424A9CF707@qq.com>\r\n'
                      'X-QQ-XMAILINFO: NssJ/YX50roaVaA8WbaTgCiCczlPbrIjajUny5yTT1mzBx3ecm1JkD7aZeZ5bF\r\n'
                      '\t 0HgfXciX736Zt3ZZhFbJqs5MYCN7m861gq/2OIHlU+iEc9HjF7hHFhjNkErV4SVb8/uAUpavrPq3\r\n'
                      '\t NUvEgej89j8wUunDOE4wdSXb3yyqxpHibrWT9efj2fTSuKx7uDaBBhOoFNPZjwrWpOkm5Tz26FNm\r\n'
                      '\t GYWwRJyOTNeN3rY5JxK5eze3+/ee+Pv5VMxHXE98NJHOyd7YYjFQA0mVsfRw8mpQyUVaHgHZcfPo\r\n'
                      '\t OamORpEh7NSa6bUcGmioi9qW//S9jRcXVRFD4Fuloj/c8ucYE7c1Zft7yGPWhH3acQqBwZ2gSI+w\r\n'
                      '\t E9rkAjMb4tAN/KC5x8sH8o/ttziG90JTaysRElcMv/SYATs/XZ8iGL9h4139ib31pCAfXOXPvFjF\r\n'
                      '\t fDY6DzqU4iiEfuFdNBk7GjtDRE7iKhuP42tDxaE7vj0Mtbp/ztGlgvJvCyYESIS0BNt9NYMvGRK/\r\n'
                      '\t YzFGG9JlzNwvKNWuAun74pbfxJxZFXcIhS8hSoe6HXj6nI1NemKLEm/kFL5IZ0GohIZBURgYRN0u\r\n'
                      '\t 9WOwIqsmBwNM/s4aXVE34fZQ8mgzrRq+ojN/tkZTtPbryTGE53+kr/pQKf9Ad/bEymLQvFO3SjYp\r\n'
                      '\t ZNq/qhPm2dOgjGoT5P+gM2JUgSypVbsnFrFE+4CIiHQOkgTyclUGLQJvFZq0+PiD0CJVSLCmQay6\r\n'
                      '\t 19XzA1pskUZAsnAkNsmKV/xFBin/qjLoMXyn0Ul5QzyNTIrvQ97KbTQ4Xd/XpkqgIloz2i3XRJA5\r\n'
                      '\t GgS2gmjxT1VnCUWQ8ZzYLPrtphYVAAFFYkyHJqlirBxXZKIV+5N6UDP8hAAf9LS9TKHAv5bSQUnj\r\n'
                      '\t uKQDyrZLlFfQQlsFAG2UvZ6akiUEQH4uAjY1qkRyKHieBhbPjgQJoaDzkgR7aPFOJ0IU6QuVX3d')

    sleep(26.869041 - 26.868824)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 2146, 343,
                         'f\r\n'
                         '\t Z2mhAqdro=\r\n'
                         'Date: Sun, 24 Apr 2022 17:50:53 +0800\r\n'
                         'From: "3268130899@qq.com" <3268130899@qq.com>\r\n'
                         'To: 3268130899 <3268130899@qq.com>\r\n'
                         'Subject: ImapTheme\r\n'
                         'X-Priority: 3\r\n'
                         'X-GUID: 38E1340E-0E81-4D91-BE09-A6B1F76E7168\r\n'
                         'X-Has-Attach: no\r\n'
                         'X-Mailer: Foxmail 7.2.23.116[cn]\r\n'
                         'Mime-Version: 1.0\r\n'
                         'X-OQ-MSGID: <202204241750523823293@qq.com>\r\n'
                         'Content-Type: multipart/alternative;\r\n'
                         '\tboundary="----=_001_NextPart737203731106_=----"\r\n'
                         '\r\n'
                         ')\r\n'
                         'C94 OK UID FETCH Completed\r\n')
    state['describe'] = ':SERVER_DATA_SENT'
    state['num'] = 20
    print(str(state['num']) + ":" + state['describe'])

    sleep(26.869072 - 26.869041)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 343, 2602)

    # 使用pop3的时间来模拟三次握手的时间
    # 补全四次挥手
    # 一次挥手
    sleep(56.850089 - 56.840068)
    send_tcp_finack(target_ip, source_ip, target_port, source_port, 2602, 343)
    state['describe'] = 'SHAKEHAND1_FIN_SENT'
    state['num'] = 21
    print(str(state['num']) + ":" + state['describe'])

    # 二次挥手
    sleep(56.850146 - 56.850089)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 343, 2603)
    state['describe'] = 'SHAKEHAND2_ACK_SENT'
    state['num'] = 22
    print(str(state['num']) + ":" + state['describe'])

    # 三次挥手
    sleep(57.731955 - 56.850146)
    send_tcp_finack(source_ip, target_ip, source_port, target_port, 343, 2603)
    state['describe'] = 'SHAKEHAND3_FIN_SENT'
    state['num'] = 23
    print(str(state['num']) + ":" + state['describe'])

    # 四次挥手
    sleep(57.792134 - 57.731955)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 2603, 344)
    state['describe'] = 'SHAKEHAND4_ACK_SENT'
    state['num'] = 24
    print(str(state['num']) + ":" + state['describe'])

    state['describe'] = 'CLOSED'
    state['num'] = 25
    print(str(state['num']) + ":" + state['describe'])

    return state


if __name__ == '__main__':
    # state = imap_simulate('101.132.158.80', '101.132.158.100', 65012, 143)
    source_ip = sys.argv[1]
    target_ip = sys.argv[2]
    source_port = sys.argv[3]
    target_port = sys.argv[4]
    state = imap_simulate(source_ip, target_ip, int(source_port), int(target_port))
    if state['describe'] == 'CLOSED':
        print("Successfully simulate IMAP protocol once")
        print("source_ip:" + state['source_ip'])
        print("target_ip:" + state['target_ip'])
        print("source_port:" + str(state['source_port']))
        print("target_port:" + str(state['target_port']))