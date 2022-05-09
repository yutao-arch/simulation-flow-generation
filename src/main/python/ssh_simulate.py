import binascii
import sys
from time import sleep

from utils.send_packets import send_tcp_syn, send_tcp_synack, send_tcp_ack, send_tcp_pshack_data, send_tcp_ack_data, send_tcp_finack


def ssh_simulate(source_ip, target_ip, source_port, target_port):
    """
    ssh协议仿真流量生成
    ssh自动机：
    0:BEGIN
    1:SHAKEHAND1_SYN_SENT（一次握手）
    2:SHAKEHAND2_SYN_ACK_SENT（两次握手）
    3:SHAKEHAND3_ACK_SENT（三次握手）
    4:CLIENT_PROTOCOL_SENT
    5:SERVER_PROTOCOL_SENT
    6:CLIENT_KEY_EXCHANGE_INIT_SENT
    7:SERVER_KEY_EXCHANGE_INIT_SENT
    8:CLIENT_DH_KEY_EXCHANGE_INIT_SENT
    9:SERVER_DH_KEY_EXCHANGE_REPLY_NEW_KEYS_SENT
    10:CLIENT_NEW_KEYS_SENT
    11:CLIENT_SERVER_DATA_EXCHANGE
    12:SHAKEHAND1_FIN_SENT（一次挥手）
    13:SHAKEHAND2_ACK_SENT（两次挥手）
    14:SHAKEHAND3_FIN_SENT（三次挥手）
    15:SHAKEHAND4_ACK_SENT（四次挥手）
    16:CLOSED
    """

    state = {'describe': 'BEGIN', 'num': 0, 'source_ip': source_ip, 'target_ip': target_ip, 'source_port': source_port,
             'target_port': target_port}
    print(str(state['num']) + ":" + state['describe'])

    begin_time = 26.274818

    # 建立连接
    # 一次握手
    send_tcp_syn(source_ip, target_ip, source_port, target_port, 0, 0)

    # 两次握手
    sleep(26.324364 - 26.274818)
    send_tcp_synack(target_ip, source_ip, target_port, source_port, 0, 1)
    state['describe'] = 'SHAKEHAND2_SYN_ACK_SENT'
    state['num'] = 2
    print(str(state['num']) + ":" + state['describe'])

    # 三次握手
    sleep(26.324518 - 26.324364)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 1, 1)
    state['describe'] = 'SHAKEHAND3_ACK_SENT'
    state['num'] = 3
    print(str(state['num']) + ":" + state['describe'])

    # SSH版本协商
    # 客户端将自己的SSH协议版本发送到服务器
    sleep(26.329985 - 26.324518)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1, 1,
                         'SSH-2.0-OpenSSH_for_Windows_8.1\r\n')
    state['describe'] = 'CLIENT_PROTOCOL_SENT'
    state['num'] = 4
    print(str(state['num']) + ":" + state['describe'])

    sleep(26.378402 - 26.329985)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 1, 34)

    # 服务器将自己的SSH协议版本发送到客户端
    sleep(26.380381 - 26.378402)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 1, 34,
                         'SSH-2.0-OpenSSH_8.0\r\n')
    state['describe'] = 'SERVER_PROTOCOL_SENT'
    state['num'] = 5
    print(str(state['num']) + ":" + state['describe'])

    # 密钥交换阶段
    # 由于是加密数据，所以不能直接使用原始的ascii数据流，选用16进制数据流传输
    sleep(26.383685 - 26.380381)
    send_tcp_ack_data(source_ip, target_ip, source_port, target_port, 34, 22,
                      binascii.unhexlify(
                          '0000056c0414c89f73ffe8f55c83514da6684ee259750000010d637572766532353531392d73'
                          '68613235362c637572766532353531392d736861323536406c69627373682e6f72672c656364'
                          '682d736861322d6e697374703235362c656364682d736861322d6e697374703338342c656364'
                          '682d736861322d6e697374703532312c6469666669652d68656c6c6d616e2d67726f75702d65'
                          '786368616e67652d7368613235362c6469666669652d68656c6c6d616e2d67726f757031362d'
                          '7368613531322c6469666669652d68656c6c6d616e2d67726f757031382d7368613531322c64'
                          '69666669652d68656c6c6d616e2d67726f757031342d7368613235362c6469666669652d6865'
                          '6c6c6d616e2d67726f757031342d736861312c6578742d696e666f2d63000001666563647361'
                          '2d736861322d6e697374703235362d636572742d763031406f70656e7373682e636f6d2c6563'
                          '6473612d736861322d6e697374703338342d636572742d763031406f70656e7373682e636f6d'
                          '2c65636473612d736861322d6e697374703532312d636572742d763031406f70656e7373682e'
                          '636f6d2c65636473612d736861322d6e697374703235362c65636473612d736861322d6e6973'
                          '74703338342c65636473612d736861322d6e697374703532312c7373682d656432353531392d'
                          '636572742d763031406f70656e7373682e636f6d2c7273612d736861322d3531322d63657274'
                          '2d763031406f70656e7373682e636f6d2c7273612d736861322d3235362d636572742d763031'
                          '406f70656e7373682e636f6d2c7373682d7273612d636572742d763031406f70656e7373682e'
                          '636f6d2c7373682d656432353531392c7273612d736861322d3531322c7273612d736861322d'
                          '3235362c7373682d7273610000006c63686163686132302d706f6c7931333035406f70656e73'
                          '73682e636f6d2c6165733132382d6374722c6165733139322d6374722c6165733235362d6374'
                          '722c6165733132382d67636d406f70656e7373682e636f6d2c6165733235362d67636d406f70'
                          '656e7373682e636f6d0000006c63686163686132302d706f6c7931333035406f70656e737368'
                          '2e636f6d2c6165733132382d6374722c6165733139322d6374722c6165733235362d6374722c'
                          '6165733132382d67636d406f70656e7373682e636f6d2c6165733235362d67636d406f70656e'
                          '7373682e636f6d000000d5756d61632d36342d65746d406f70656e7373682e636f6d2c756d61'
                          '632d3132382d65746d406f70656e7373682e636f6d2c686d61632d736861322d3235362d6574'
                          '6d406f70656e7373682e636f6d2c686d61632d736861322d3531322d65746d406f70656e7373'
                          '682e636f6d2c686d61632d736861312d65746d406f70656e7373682e636f6d2c756d61632d36'
                          '34406f70656e7373682e636f6d2c756d61632d313238406f70656e7373682e636f6d2c686d61'
                          '632d736861322d3235362c686d61632d736861322d3531322c686d61632d73686131000000d5'
                          '756d61632d36342d65746d406f70656e7373682e636f6d2c756d61632d3132382d65746d406f'
                          '70656e7373682e636f6d2c686d61632d736861322d3235362d65746d406f70656e7373682e63'
                          '6f6d2c686d61632d736861322d3531322d65746d406f70656e7373682e636f6d2c686d61632d'
                          '736861312d65746d406f70656e7373682e636f6d2c756d61632d3634406f70656e7373682e63'
                          '6f6d2c756d61632d313238406f70656e7373682e636f6d2c686d61632d736861322d3235362c'
                          '686d61632d736861322d3531322c686d61632d736861310000001a6e6f6e652c7a6c6962406f'
                          '70656e7373682e636f6d2c7a6c69620000001a6e6f6e652c7a6c6962406f'
                      ))

    # 客户端告诉服务器自己支持的相关加密算法列表、MAC算法列表等
    # sleep(26.383685 - 26.383685)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1394, 22,
                         binascii.unhexlify(
                             '70656e7373682e636f6d2c7a6c69620000000000000000000000000000000000'
                         ))
    state['describe'] = 'CLIENT_KEY_EXCHANGE_INIT_SENT'
    state['num'] = 6
    print(str(state['num']) + ":" + state['describe'])

    # 服务器告诉客户端自己支持的相关加密算法列表、MAC算法列表等
    sleep(26.432345 - 26.383685)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 22, 1426,
                         binascii.unhexlify(
                             '000004140514c08ee69c194f2d86e6c8a879876fc2ae00000125637572766532353531392d7368613235362c6'
                             '37572766532353531392d736861323536406c69627373682e6f72672c656364682d736861322d6e6973747032'
                             '35362c656364682d736861322d6e697374703338342c656364682d736861322d6e697374703532312c6469666'
                             '669652d68656c6c6d616e2d67726f75702d65786368616e67652d7368613235362c6469666669652d68656c6c'
                             '6d616e2d67726f757031342d7368613235362c6469666669652d68656c6c6d616e2d67726f757031362d73686'
                             '13531322c6469666669652d68656c6c6d616e2d67726f757031382d7368613531322c6469666669652d68656c'
                             '6c6d616e2d67726f75702d65786368616e67652d736861312c6469666669652d68656c6c6d616e2d67726f757'
                             '031342d73686131000000417273612d736861322d3531322c7273612d736861322d3235362c7373682d727361'
                             '2c65636473612d736861322d6e697374703235362c7373682d65643235353139000000776165733235362d676'
                             '36d406f70656e7373682e636f6d2c63686163686132302d706f6c7931333035406f70656e7373682e636f6d2c'
                             '6165733235362d6374722c6165733235362d6362632c6165733132382d67636d406f70656e7373682e636f6d2'
                             'c6165733132382d6374722c6165733132382d636263000000776165733235362d67636d406f70656e7373682e'
                             '636f6d2c63686163686132302d706f6c7931333035406f70656e7373682e636f6d2c6165733235362d6374722'
                             'c6165733235362d6362632c6165733132382d67636d406f70656e7373682e636f6d2c6165733132382d637472'
                             '2c6165733132382d636263000000a9686d61632d736861322d3235362d65746d406f70656e7373682e636f6d2'
                             'c686d61632d736861312d65746d406f70656e7373682e636f6d2c756d61632d3132382d65746d406f70656e73'
                             '73682e636f6d2c686d61632d736861322d3531322d65746d406f70656e7373682e636f6d2c686d61632d73686'
                             '1322d3235362c686d61632d736861312c756d61632d313238406f70656e7373682e636f6d2c686d61632d7368'
                             '61322d353132000000a9686d61632d736861322d3235362d65746d406f70656e7373682e636f6d2c686d61632'
                             'd736861312d65746d406f70656e7373682e636f6d2c756d61632d3132382d65746d406f70656e7373682e636f'
                             '6d2c686d61632d736861322d3531322d65746d406f70656e7373682e636f6d2c686d61632d736861322d32353'
                             '62c686d61632d736861312c756d61632d313238406f70656e7373682e636f6d2c686d61632d736861322d3531'
                             '32000000156e6f6e652c7a6c6962406f70656e7373682e636f6d000000156e6f6e652c7a6c6962406f70656e7'
                             '373682e636f6d000000000000000000000000000000000000'
                         ))
    state['describe'] = 'SERVER_KEY_EXCHANGE_INIT_SENT'
    state['num'] = 7
    print(str(state['num']) + ":" + state['describe'])

    # 客户端发送D-H公钥
    sleep(26.434327 - 26.432345)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1426, 1070,
                         binascii.unhexlify(
                             '0000002c061e000000202976f8a91e57f41b4d6ee64519335f48a10fe903d4403aee75a20ea1a8208f0d0000'
                             '00000000'
                         ))
    state['describe'] = 'CLIENT_DH_KEY_EXCHANGE_INIT_SENT'
    state['num'] = 8
    print(str(state['num']) + ":" + state['describe'])

    # 服务端回复，服务端与客户端使用D-H算法生成会话密码key
    # DH回复包：
    # 一个服务端的公钥，即证书，客户端会将该公钥与本地公钥对比，看是否是被信任的服务器，如果是第一次访问则会询问用户是否信任这样的公钥
    # 服务端回复的DH公钥
    # 签名
    # 服务端还会回复一个new Key包 用于表明服务端可以使用会话密码key加密消息了
    sleep(26.486441 - 26.434327)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 1070, 1474,
                         binascii.unhexlify(
                             '000001040a1f000000680000001365636473612d736861322d6e69737470323536000000086e6973747032353'
                             '60000004104c6d8d4650113588b7e2fb0a615c50953b162f174c97c24be7c851c599c95f9b4de5a99dab9e8eb'
                             'c0ff5d8ebb915779ccbdb2e34068199ea168b8b069311c4446000000209f6f1e0e549ec17ac5b043bd63aa606'
                             'b58cef94ee9e161664ecffb94a551c37d000000640000001365636473612d736861322d6e6973747032353600'
                             '0000490000002100f80d0787a112e986583e08299e2540a04fbd45c9a5904e755d5dacba5e7c8d4d000000204'
                             '5c0a19ffa64c5967a213f6c82244c5213077dd4417513a960401eb0af2860cf00000000000000000000000000'
                             '0c0a150000000000000000000020c52ff7c326f65c96b52ae3ed4ce5b099ac2585f3a447f6bdd7e7ed53f205c'
                             '80a140a89e48255336f9aac2d90bd2acfeaf6431bec640c5bbff06bb43acf243a9859417bf28b61c722209b59'
                             '1f326077e031cfbd3a8a6450f851869655fb35e3f400eae7042e940c739702c3a0d479455911dbcc375281180'
                             '00e089c8f929c786625fff766d07fa0341a043fc6dc1bda6cec72becad67e4074cef923dab09771761b90efad'
                             '68de7eaaaac5ec'
                         ))
    state['describe'] = 'SERVER_DH_KEY_EXCHANGE_REPLY_NEW_KEYS_SENT'
    state['num'] = 9
    print(str(state['num']) + ":" + state['describe'])

    # 客户端要回复服务端的new key包
    sleep(26.492290 - 26.486441)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1474, 1522,
                         binascii.unhexlify(
                             '0000000c0a1500000000000000000000'
                         ))
    state['describe'] = 'CLIENT_NEW_KEYS_SENT'
    state['num'] = 10
    print(str(state['num']) + ":" + state['describe'])

    # 加密信道构建完毕，然后双方通过key加密传输数据
    # SSH-AUTH阶段，主要是客户端和服务器之间用于身份认证的
    sleep(26.581955 - 26.492290)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 1522, 1490)

    sleep(26.582125 - 26.581955)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1490, 1522,
                         binascii.unhexlify(
                             '57b307d03ec6b37fdf6802edada4b0103da4e380b53dbed5d0ca8f49048b191fb27534d53b649030ef8cd8c7'
                         ))

    sleep(26.630416 - 26.582125)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 1522, 1534)

    sleep(26.630669 - 26.630416)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 1522, 1534,
                         binascii.unhexlify(
                             '2c400c55c3309d1d970154561373bca475e697cbd4b9c3fc9a08bf5e883481e28fdb4741569c7b26e35dc79a'
                         ))

    sleep(26.630936 - 26.630669)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1534, 1566,
                         binascii.unhexlify(
                             'c34e1835a986fd83d2ebf623ee5fbd298cabb30e700feb124edd9ca3a6d458597d490f54f2ba170fe66b707da'
                             '1bb235c58c25580da896035127db936'
                         ))

    sleep(26.686403 - 26.630936)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 1566, 1594,
                         binascii.unhexlify(
                             '248a0dc30d59a8ed5d5725ccb6c2b8136400d44d72a24a24aa63cf5630362ec41f99367d89a7d2415a4a87a5e'
                             'c490db678ee115b2e51961e93f2ea1ab512df0a302c520308149f8ea09adbda299eb388b53d9b80'
                         ))

    sleep(26.686742 - 26.686403)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1594, 1650,
                         binascii.unhexlify(
                             'cc5a3ee5f4157ec7b443d49e90c8a3cf09517ec05bbeedbbe9f42f31f32ad0891f730ef900eef56027a3b91b'
                             '388031bc342c7eccbc81eb4b4ed87da8b865d6a178b60171effe01e4aea08f56d0a31600367d3df6472fce40'
                             '632a7b2eb92a23c131573ee03b1c74ac24759bf850df03a0ccf2a4c73b174e1d425187a3f34372aa16e3f36f'
                             '85603a60f68a0d4ce79fefd313bf03f9101a82d681fe4eebcea381eec7c7cabccdd171e804c4f131c4dab307'
                             'b3dfa09bb5de6f8c3ba4778430a0dc976af69fa8bd54e1b43100ceada2394c3b7055a1347bec60db66b1fffd'
                             'a69c23ba15dd03684be2fa07499688d4f40d62fbb11b27180a706b1ea281f021b321f56c6b3b9883178c11bb'
                             '0efa413d6d6e368826ca201e10bfc5439b7763dcde6c93de56ed66b9b9a1d25d1fae5acc2357bdca8363f941'
                             '154bbdbf06598e4cd64964e3ee121086edfc9a2d0844029517c7839e5781afde87198361c4cf7766f813108d'
                             '6e2223136fd296a1cc1986d4ddcccfbddb83ff74cf94b136f83d99c7be6c36ae84bd48b8d4fa22d285f3e55f'
                             '2bfbb9ea07fb6d0ad3d7751a62866475254eeff3350637d437089fdf82e7682eebe952024a91a3e2fdc8862d'
                             '81fcf56c7f3ee9dfa8d3666b20d3e2b27a5c46103efd21005fda4cc2b78ae06e5391bedff39edb00feff353f'
                             '86dad1323ed0c7ea6e7d6ba60ed48042'
                         ))

    sleep(26.740595 - 26.686742)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 1650, 2094,
                         binascii.unhexlify(
                             'b90680b04dcebcc75647a298bcf4f1080a36650b700a1b4c3e86e83c71a68499cc8b81462d432f7c98fa9c75'
                             '8f7492804091af540fb120d4ec7fbb86be3765bf6096558db8bbf288868972f14e20307cfafd4e23'
                         ))

    sleep(26.784157 - 26.740595)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 2094, 1734)

    sleep(31.726797 - 30.784157)  # 此处时间太长，自己将26.784157修改为30.784157
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 2094, 1734,
                         binascii.unhexlify(
                             'ce09d2411b48f696cd10941af629155df99a47f0e745da1f5ac7fe0968900bbe7f6ff831a2516db7a9ad2487'
                             'eef78aa0fce6c78008e9d499e2e697886a984d21c3a60d809e9d0a765341a2c937dc77b917dc389c8a6698c2'
                             '248aa543701cf47dfb0834099be4dd649cba0bb9bf81239ef4c2f84f614516d124fd3bfab388fcde407533c7'
                             'd94e6aeab0e1e4c32d15ddb3b34874b2'
                         ))

    sleep(31.787390 - 31.726797)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 1734, 2242,
                         binascii.unhexlify(
                             '99517e9057a76f50293c2d4bf8e3b8aa8f8b539463043846282744a7'
                         ))

    sleep(31.789756 - 31.787390)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 2242, 1762,
                         binascii.unhexlify(
                             '0672d50ee549d19f8054bf2e9fb1466c31bc24914c2bd73312907843e59b83b03db8e753d0057e4041a2d4ac'
                             'dd7c39d322c7e81720bfd24d5323c77f9fc44e7adcddf618baea98e85f43f7946ddba806c4ee0e70c962c39d'
                             '96b514cc87ba3dacda8938e7c6f48bedb89418f0c3785858'
                         ))

    sleep(31.872849 - 31.789756)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 1762, 2354,
                         binascii.unhexlify(
                             '1142e3c5d6f299bdee6af17f91845c3cf5d93194d42b5f2c593a28c7e1eef9a9a15cf33cd78b9cc87b188add'
                             '75f3ffe1a97075be778d69e305be41aa402dd8cad9503a3e4e741c5248ca96a404f5903a09249b2a2c7a0ed3'
                             'a911e0307580385869024f6e73437774a00aa17241216af19523ccecbbe7ab5aa36704bd28245d9df66209eb'
                             '9b4d4c08022a9ba792f292136d543cc3b5460652cb76aec7997b11977c44774104af3b952468e8dccb00e353'
                             '70142b0c6f7401fca2b0966caf899a4c41fe48f4d4893908544967ddaf71c669ac58dff937decd4510b488de'
                             'd5b980961586b48d69662825f26d8d329f99cc5131525acece9fe1edde8c6879f25246574469c010d7817e62'
                             '1fbd88936ada101955fecc9babe99364311f1f3fa8acb6590f4bef9e65cff03825b83d9377ac67909a62656e'
                             'cedccf90317cd838c3f116fc0d1415359c0bb73c138d9c391e2ab1f385d52fd786399f9985fad7b62eb26535'
                             'da0011eb183abc6c60eccf4a93559748e8037d951bf5d1b624b1d997468f62cc7d8c48ec68ebc9995478d7d6'
                             '252ae8204108122fdacdfe76a4d3c178198ebff4eb6878ad7f6de685370f45ea9414da2d10313f8697a045e1'
                             'ff80b72831c31fbe8e58a122156faeae3ad93bf57072a894f362b8b08c1441034fb45a610840f497b4ab1566'
                             '3c865fc3983ce57543d39feeb9dc0fbd1448feb2bd90911bf519da88372288f1542cb224e12b360db09b0a1e'
                             '69bea5818fc6d65271b34d4b0984646bac4c9a97f899e509e2710d412b6d2714aff2686226968e273b5fd25a'
                             '8668b550612d20a8383f7745604e149f01134579c0e0d186f8980f854a1203f8ad3d81ae817dc401806f1d84'
                             'b749d3aa009e6861b55af3fc'
                         ))

    sleep(31.915470 - 31.872849)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 2354, 2390)

    sleep(31.965482 - 31.915470)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 2390, 2354,
                         binascii.unhexlify(
                             '1641f361882111dc58aa2bd3eb5563e528d378b3cce5f0496b177d0eba82e5f4c294f47a03ede160aea9153e'
                         ))

    sleep(31.965782 - 31.965482)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 2354, 2434,
                         binascii.unhexlify(
                             '13b4dab8f925b638db8c62e637f87fa91ba1a6b188194b84379ef9803de2e5698ab46254db11b486a01a0311'
                             '73f648b193ffe897c5169d6fca29d3b69eaa65029414f1c4e8394674e427592bd2782f58becb42dd14d1f30e'
                             '6589eb9f189616feedf9a94de7f212f18177f00768567d1997c7d9175a5294df713f1b3aedf9fa47341c8714'
                             'aaf0f959'
                         ))

    sleep(32.015480 - 31.965782)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 2434, 2490,
                         binascii.unhexlify(
                             'df1d611b812cd8c8a2e9bf8af4e208da12586391c9d1d63775405d9f123a54ac5e7a46c4fd0b393eca78c8d2'
                             'ca7d69404bc68da35cedc579b73aa9eb2257607a14579e17beb35580afe54652ce4a85724828c0d173704d81'
                             '23c0de739c19c6598692d36a4c580bb23e3425ec'
                         ))

    sleep(32.015713 - 32.015480)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 2542, 2490,
                         binascii.unhexlify(
                             '908456247cb36da8d3039736faa3a23be412b08fdb97a52a686df9371c353222057e504bdaa334665df94dc0'
                             'e9c170dd5063f0e01f19f3a084ad251beb0de1a9693c9166008d85b77ecf37a1d34eabe439df4bc38691c696'
                             'b10471b04475ac3aa4218e7d841244d75a14a11044fe8342fb95023652c2cb67c26ecfd7214686e114791328'
                             '457f895ab09d201ce2201babe29be7c1d5c2db5facdafe4e52da941029c978debc578e7f1e7aa97dc2a8bad1'
                             '14a62fc7790cc9d3cf83c7d92cc6db860134b7306a5618795eb750544c86c49d6ba3a17f75a4ff954a0f8875'
                             '0c0b183f4f355507d0aa3727930ead2a5c1e455363295da563d0a60723f3aa6488ba2f5f94e2b3c15c919892'
                             '97acef476cae3a440df1babcdee3da651a8833b0c6851b04271610bc2f8172880786dcc94526f600f9c7ad14'
                             'd2063714eee9c70b73e08252e91c272d630b9059f988281d3d55c2a24c8be3d5e1cd8ba8f646f434d8330337'
                             '0c0c493d938ca3b0ee31f8c019f28f4e1a760ae1'
                         ))

    sleep(32.015824 - 32.015713)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 2490, 2914)

    sleep(32.057397 - 32.015824)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 2914, 2490,
                         binascii.unhexlify(
                             '85ac5c93e7dc708619abf32569958f9a770cdd29e346e001b7d01fd6e04785b7f1f07cc048f107a3b07537ca'
                             '4333df9eb6b3822b4a8942218b1113ed8d3f67484f27ae4d652b8b58dde0066b'
                         ))

    sleep(32.057633 - 32.057397)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 2990, 2490,
                         binascii.unhexlify(
                             'c166266d1a711232423833534341c1ddb2396e5970fb72b222fdf15cae461494e88e6eb8864c9f39e6e96dba'
                             '1ab541b7acb4dd532b90d88e66291d925baeafa67bddcb4d'
                         ))

    sleep(32.057673 - 32.057633)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 2490, 3058)

    # 对源数据流的时间进行了处理，源文件为763开头，修改为32秒开头
    sleep(32.502376 - 32.457673)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 2490, 3058,
                         binascii.unhexlify(
                             '53c9c855a5ac18e3530ec4ae58995a837fc0faceb6604e249f9a6ca5f6d2017c2a78dc74'
                         ))

    sleep(32.550969 - 32.502376)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 3058, 2526,
                         binascii.unhexlify(
                             'f33c7a1e982431728282c371202a972c742bfb6e1068ad7a2fd5a639771084b6f2681560'
                         ))

    sleep(32.596743 - 32.550969)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 2526, 3094)

    sleep(32.837297 - 32.596743)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 2526, 3094,
                         binascii.unhexlify(
                             'd4777ebef4334e4aa5d39d1cefa7d3a241e0909070bd2453c6b8f32f8d5accc3eb2a6ab6'
                         ))

    sleep(32.884938 - 32.837297)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 3094, 2562,
                         binascii.unhexlify(
                             '02299cca76d85384b6e9639de52b192404337689125c7c8c697706fb84c2a141ae60191d'
                         ))

    sleep(32.926255 - 32.884938)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 2562, 3130)

    sleep(33.090595 - 32.926255)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 2562, 3130,
                         binascii.unhexlify(
                             'b7d4ece1f6b4862a9f4bfc6999dc1984dbf3298e82988084749e875d42bc1a209564e138'
                         ))

    sleep(33.138901 - 33.090595)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 3130, 2598,
                         binascii.unhexlify(
                             '695f2613b495cc8e9f7ecb15aee45790dd2a305990a7bfc378bb0091eb9ce521d9622092'
                         ))

    sleep(33.182394 - 33.138901)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 2598, 3166)

    sleep(33.365494 - 33.182394)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 2598, 3166,
                         binascii.unhexlify(
                             '89429cd7b5aab241e85ac0c72530346abc5c393b1539e80763cf7daf6473f005d1a93076'
                         ))

    sleep(33.413028 - 33.365494)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 3166, 2634,
                         binascii.unhexlify(
                             'e2b4ea1b702eab4dd068d035040f8d2ba5f974526834082155eb3b664a2123e4a7db9d6d'
                         ))

    sleep(33.459885 - 33.413028)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 2634, 3202)

    sleep(33.893753 - 33.459885)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 2634, 3202,
                         binascii.unhexlify(
                             '5f5bd4abe3a5e1ff133b4f07526a9bc64f0095718da2db048ba0ae6ca2988c48e463dcfb'
                         ))

    sleep(33.940941 - 33.893753)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 3202, 2670,
                         binascii.unhexlify(
                             'db17c0f49a619bc612613ba69c593f61286a6c89dd2c77bb729f10db60d21d8314d8566d'
                         ))

    sleep(33.941150 - 33.940941)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 3238, 2670,
                         binascii.unhexlify(
                             'cba91da788f3c3e1825c0f52b1359093a73f2a607c0f67fb526f0457c3e9a4b50f9a2bdf1c88506af699dfce'
                         ))

    # sleep(33.941150 - 33.941150)
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 3282, 2670,
                         binascii.unhexlify(
                             'cf26f4f50386e9257238ca0fde33f656363cd12c96e9b62131d7a52ea70cf7d0754dd6aee6a4feb68b8851ff'
                             '8f1379f0ee74229075dc4743c4c503a0eaded5d69b8b55068dde4790adab8fbe218c6a3b1a48c8ccec8af672'
                             '64903691da296b379c2623bfeb569f23cc083db240cc4124ed08aa4d238a6f6bba0997f9fc99b803db1cd8ac'
                             'f8b1ace4f1c0899b7d91fa5623fcd44ba42f3360133e993d3505fca52e9c04e7c39485eb1ba3f418f9d828ac'
                         ))

    sleep(33.941197 - 33.941150)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 2670, 3458)

    sleep(33.943565 - 33.941197)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 2670, 3458,
                         binascii.unhexlify(
                             'ac226b0c6ba3e6e46fed896b5a57c3d2e59c6882548af37e4c9b387559d5b87f87f9f3a3'
                         ))

    sleep(33.943646 - 33.943565)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 2706, 3458,
                         binascii.unhexlify(
                             '972e772cf139ac7e9d385f183ee1da851d53bc533f9ed3a8d8b939922dc55bb5f01b6b563638d5b360698eff'
                             '008127b235add0da3778cbbd4d24e276'
                         ))
    state['describe'] = 'CLIENT_SERVER_DATA_EXCHANGE'
    state['num'] = 11
    print(str(state['num']) + ":" + state['describe'])

    # 使用pop3的时间来模拟三次握手的时间
    # 补全四次挥手
    # 一次挥手
    sleep(56.850089 - 56.840068)
    send_tcp_finack(source_ip, target_ip, source_port, target_port, 2766, 3458)
    state['describe'] = 'SHAKEHAND1_FIN_SENT'
    state['num'] = 12
    print(str(state['num']) + ":" + state['describe'])

    # 二次挥手
    sleep(56.850146 - 56.850089)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 3458, 2767)
    state['describe'] = 'SHAKEHAND2_ACK_SENT'
    state['num'] = 13
    print(str(state['num']) + ":" + state['describe'])

    # 三次挥手
    sleep(57.731955 - 56.850146)
    send_tcp_finack(target_ip, source_ip, target_port, source_port, 3458, 2767)
    state['describe'] = 'SHAKEHAND3_FIN_SENT'
    state['num'] = 14
    print(str(state['num']) + ":" + state['describe'])

    # 四次挥手
    sleep(57.792134 - 57.731955)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 2767, 3459)
    state['describe'] = 'SHAKEHAND4_ACK_SENT'
    state['num'] = 15
    print(str(state['num']) + ":" + state['describe'])

    state['describe'] = 'CLOSED'
    state['num'] = 16
    print(str(state['num']) + ":" + state['describe'])

    return state


if __name__ == '__main__':
    # state = ssh_simulate('101.132.158.80', '101.132.158.100', 62724, 22)
    source_ip = sys.argv[1]
    target_ip = sys.argv[2]
    source_port = sys.argv[3]
    target_port = sys.argv[4]
    state = ssh_simulate(source_ip, target_ip, int(source_port), int(target_port))
    if state['describe'] == 'CLOSED':
        print("Successfully simulate SSH protocol once")
        print("source_ip:" + state['source_ip'])
        print("target_ip:" + state['target_ip'])
        print("source_port:" + str(state['source_port']))
        print("target_port:" + str(state['target_port']))
