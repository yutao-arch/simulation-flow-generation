from utils.send_packets import send_tcp_syn, send_tcp_synack, send_tcp_ack, send_tcp_pshack_data, send_tcp_ack_data, \
    send_tcp_finack


def simulate(source_ip, target_ip, source_port, target_port):
    send_tcp_syn(source_ip, target_ip, source_port, target_port, 1222042452, 0)
    send_tcp_synack(target_ip, source_ip, target_port, source_port, 2328140706, 1222042453)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 1222042453, 2328140707)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 2328140707, 1222042453,
                         b'+OK XMail POP3 Server v1.0 Service Ready(XMail v1.0)\r\n')
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1222042453, 2328140761,
                         b'USER 3268130899@qq.com\r\n')
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 2328140761, 1222042477)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 2328140761, 1222042477, b'+OK\r\n')
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1222042477, 2328140766,
                         b'PASS bigyhlolsfzycjdb\r\n')
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 2328140766, 1222042500)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 2328140766, 1222042500, b'+OK\r\n')
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1222042500, 2328140771, b'STAT\r\n')
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 2328140771, 1222042506)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 2328140771, 1222042506, b'+OK 6 26402\r\n')
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1222042506, 2328140784, b'LIST\r\n')
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 2328140784, 1222042512,
                         b'+OK\r\n1 2251\r\n2 8535\r\n3 8535\r\n4 2395\r\n5 2291\r\n6 2395\r\n.\r\n')
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1222042512, 2328140840, b'UIDL\r\n')
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 2328140840, 1222042518,
                         b'+OK\r\n1 ZC0017_N2TNDLSMM_gue7kAJEeNJc3\r\n2 ZC0018_5bbN4lqMLeYuOPoAZMi0Vc3\r\n3 ZC0018_OWrN0mqMNf4uwAIAbN4Vbc3\r\n4 ZC0018_uunNrhaMj0QuyAoAkskyfc3\r\n5 ZC0018_azjNvASMnVYu3x0AF2cfWc3\r\n6 ZC0018_eCvNizOMaKMu9DYAPe_tWc3\r\n.\r\n')
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1222042518, 2328141052, b'RETR 6\r\n')
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 2328141052, 1222042526)
    send_tcp_ack_data(target_ip, source_ip, target_port, source_port, 2328141052, 1222042526,
                      b'+OK 2395\r\nReceived: from LAPTOP-OUDFRK43 ([111.42.148.139])\r\n\tby newxmesmtplogicsvrszb7.qq.com (NewEsmtp) with SMTP\r\n\tid 7E38E045; Fri, 18 Mar 2022 16:31:35 +0800\r\nX-QQ-mid: xmsmtpt1647592295ticnj924a\r\nMessage-ID: <tencent_24D942D72AEEB1271D52541E6DC3D7873307@qq.com>\r\nX-QQ-XMAILINFO: Mdc3TkmnJyI/BRmH05+BtqEAwkz3H7lxmsrwpyJ+fp79SU7ypIYsvQYuXg7H6L\r\n\t jLjHQCJGi3OjO44F+jg+Q0wn144vfuHF5I5nOreqMg0/LKMea5OHNbhln7s7cHGO74aOUGFaPO+F\r\n\t s/iacNQHnFYf3zZKac2vhb5E7ez1J1uwQNb69AW52dShWELaizxUE9JGgd2keiAmb1KLwt6eO2pw\r\n\t FLHzdltL615eqZfVRfhHpIXsPIWNWDKx9cfMA85dlGo29veFmLwagR/FpwjnVo9kk3yUKDbCRfGp\r\n\t wlaDX1j9AlSq+2q/5jlX1zqzhXiG7Od60BPZ0nscVfRED/BL9m6W4/5sKAGHmWchTwSnY7t8ydLj\r\n\t 8ugqUxVjqGrJW+hOVYuNtEQcso5cCL8ifcB5LzsZQz+PlgCj0Dzg8O7vxA/z/DRhlhqfwZOk+bw8\r\n\t 3mRvRdauYMYbNeHLF+/2j40yY6gFK7IZwP3yNaCzePWJ1XhAWkBOaWwNGf7iIafBHa7hYn01Ffm6\r\n\t FHKjZ8DuPmldoLNifblvVpakczuV81quyrqP2UwoOrvZA9aJnyaA0BG5wKpRZ6gTX/MYimnJXRhR\r\n\t cRIx3Kuzqw2WXqE/kKLpbNRV6INUatIL+M7M5tv+2eTPnNa5abNjIY/3puMil94Dg8EsypnjAkx3\r\n\t KXuGDZi8jsQMZcCWaWsLn/0MTy5s7bwEHYNQnrllQJ+KUhDNmkFyPKeAis0Aufa/Yuxebl1KS/3t\r\n\t J0I5c4hPPBkdd5zncJt8366qGet3tk+toof81jlzyk8Z9T7QeupeWCEXEaiXABXJCKblFnhzkmIf\r\n\t Bw6GVdIZTD4yUlV/yPnFEnerFi2zWCjrrQtXdzgdQrMu7a57yc+PZyPLezi/HsYYq9IqzHIME+KX\r\n\t gldT1hglDuSRmc+Vt4t/6nLeioaqICXli4Y4bieEhpIs+wUo19xZFRiZRTnR6SQ5z+rAXY9H2oSj\r\n\t FuILJkg5E=\r\nDate: Fri, 18 Mar 2022 16:31:31 +0800')
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 2328142412, 1222042526,
                         b'\r\nFrom: "1063695334@qq.com" <1063695334@qq.com>\r\nTo: 3268130899 <3268130')
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 2328142484, 1222042526,
                         b'899@qq.com>\r\nSubject: PopTheme\r\nX-Priority: 3\r\nX-GUID: 096D5C66-F5A9-47D3-B5A7-DFAAB226F404\r\nX-Has-Attach: no\r\nX-Mailer: Foxmail 7.2.23.116[cn]\r\nMime-Version: 1.0\r\nX-OQ-MSGID: <202203181631310967556@qq.com>\r\nContent-Type: multipart/alternative;\r\n\tboundary="----=_001_NextPart047566706231_=----"\r\n\r\nThis is a multi-part message in MIME format.\r\n\r\n------=_001_NextPart047566706231_=----\r\nContent-Type: text/plain;\r\n\tcharset="us-ascii"\r\nContent-Transfer-Encoding: base64\r\n\r\nUG9wQ29udGVudA0K\r\n\r\n------=_001_NextPart047566706231_=----\r\nContent-Type: text/html;\r\n\tcharset="us-ascii"\r\nContent-Transfer-Encoding: quoted-printable\r\n\r\n<html><head><meta http-equiv=3D"content-type" content=3D"text/html; charse=\r\nt=3Dus-ascii"><style>body { line-height: 1.5; }body { font-size: 14px; fon=\r\nt-family: "Microsoft YaHei UI"; color: rgb(0, 0, 0); line-height: 1.5; }</=\r\nstyle></head><body>=0A<div><span></span>PopContent</div>=0A</body></html>\r\n------=_001_NextPart047566706231_=------\r\n\r\n.\r\n')
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 1222042526, 2328143462)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1222042526, 2328143462, b'QUIT\r\n')
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 2328143462, 1222042532)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 2328143462, 1222042532, b'+OK Bye\r\n')
    send_tcp_finack(target_ip, source_ip, target_port, source_port, 2328143471, 1222042532)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 1222042532, 2328143472)
    send_tcp_finack(source_ip, target_ip, source_port, target_port, 1222042532, 2328143472)


if __name__ == '__main__':
    simulate('101.132.158.80', '101.132.158.100', 63315, 143)
