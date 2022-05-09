import binascii
import random
import sys

from utils.send_packets import send_tcp_syn, send_tcp_synack, send_tcp_ack, send_tcp_pshack_data, send_tcp_ack_data, \
    send_tcp_finack
from time import sleep


# import threading


def http_simulate(source_ip, target_ip, source_port, target_port):
    """
    http协议仿真流量生成
    http自动机：
    0:BEGIN
    1:SHAKEHAND1_SYN_SENT（一次握手）
    2:SHAKEHAND2_SYN_ACK_SENT（两次握手）
    3:SHAKEHAND3_ACK_SENT（三次握手）
    4:HTTP_REQUEST_SENT
    5:HTTP_RESPONSE_SENT
    6:SHAKEHAND1_FIN_SENT（一次挥手）
    7:SHAKEHAND2_ACK_SENT（两次挥手）
    8:SHAKEHAND3_FIN_SENT（三次挥手）
    9:SHAKEHAND4_ACK_SENT（四次挥手）
    10:CLOSED
    """
    request = 'GET / HTTP/1.1\r\n' \
              'Host: hituc.hit.edu.cn\r\n' \
              'Connection: keep-alive\r\n' \
              'Cache-Control: max-age=0\r\n' \
              'Upgrade-Insecure-Requests: 1\r\n' \
              'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0\r\n' \
              'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n' \
              'Referer: https://www.baidu.com/link?url=DkmQaPNDGHdttCDJfhj3yDVYG25jkiOQ3IhVc7ZF1XmuEpkgrVsVUHbn7-b_AlVM&wd=&eqid=c52dfd6f009e961c000000036223bd01\r\n' \
              'Accept-Encoding: gzip, deflate\r\n' \
              'Accept-Language: zh-CN,zh;q=0.9\r\n' \
              'Cookie: _ga=GA1.3.647229436.1629704630; JSESSIONID=BF3F3C6B7A5E7C804BB734476291A8FA\r\n' \
              '\r\n'

    # 以哈工大本科生院为例提取数据流

    state = {'describe': 'BEGIN', 'num': 0, 'source_ip': source_ip, 'target_ip': target_ip, 'source_port': source_port,
             'target_port': target_port}
    print(str(state['num']) + ":" + state['describe'])

    begin_time = 2.883577  # 哈工大本科生院发送第一个包的初始时间

    # 一次握手
    send_tcp_syn(source_ip, target_ip, source_port, target_port, 0, 0)
    state['describe'] = 'SHAKEHAND1_SYN_SENT'
    state['num'] = 1
    print(str(state['num']) + ":" + state['describe'])

    # 两次握手
    sleep(2.888538 - begin_time)
    send_tcp_synack(target_ip, source_ip, target_port, source_port, 0, 1)
    state['describe'] = 'SHAKEHAND2_SYN_ACK_SENT'
    state['num'] = 2
    print(str(state['num']) + ":" + state['describe'])

    # 三次握手
    sleep(2.888625 - 2.888538)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 1, 1)
    state['describe'] = 'SHAKEHAND3_ACK_SENT'
    state['num'] = 3
    print(str(state['num']) + ":" + state['describe'])

    # 发送HTTP请求
    sleep(2.888872 - 2.888625)
    send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, 1, 1, request)
    state['describe'] = 'HTTP_REQUEST_SENT'
    state['num'] = 4
    print(str(state['num']) + ":" + state['describe'])

    sleep(2.892255 - 2.888872)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 1, 696)

    sleep(2.901121 - 2.892255)

    # 在真实的环境中，服务器回复的五个response和一个fin包是同时发送的，也就是并发发送的，所以尝试了使用并发的方式执行
    # 但会出现以下问题：1.发送这六个包的顺序会乱掉，导致乱序，模拟失败
    #                   2.无法实现六个包同时发送
    # 解决办法：查资料，找能够同时执行多个线程且满足fifo的多线程方法
    # 使用了多种线程方法，都无法实现同时执行发送者六个包，暂时放弃
    #
    # threads = []
    # threads.append(threading.Thread(
    #     target=send_tcp_ack_data(target_ip, source_ip, target_port, source_port, 1, 696, response)))
    # threads.append(threading.Thread(
    #     target=send_tcp_ack_data(target_ip, source_ip, target_port, source_port, 1361, 696,
    #     generate_random_str(1360))))
    # threads.append(threading.Thread(
    #     target=send_tcp_ack_data(target_ip, source_ip, target_port, source_port, 1361, 696,
    #     generate_random_str(1360))))
    # threads.append(threading.Thread(
    #     target=send_tcp_ack_data(target_ip, source_ip, target_port, source_port, 1361, 696,
    #     generate_random_str(1360))))
    # threads.append(threading.Thread(
    #     target=send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 1361, 696,
    #     generate_random_str(1071))))
    # threads.append(threading.Thread(
    #     target=send_tcp_finack(target_ip, source_ip, target_port, source_port, 6512, 696)))
    #
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()

    # response1 = "HTTP/1.1 200 OK\r\n" \
    #            "Date: Sat, 05 Mar 2022 19:43:51 GMT\r\n" \
    #            "Server: Server\r\n" \
    #            "X-Frame-Options: SAMEORIGIN \r\n" \
    #            "Frame-Options: SAMEORIGIN\r\n" \
    #            "Accept-Ranges: bytes\r\n" \
    #            "Vary: Accept-Encoding\r\n" \
    #            "Content-Encoding: gzip\r\n" \
    #            "Content-Length: 6247\r\n" \
    #            "Connection: close\r\n" \
    #            "Content-Type: text/html\r\n" \
    #            "\r\n" + generate_random_str(1096)
    # # 本科生院的len=1360，我们定义的头部长度为264，加上补充位1096构成第一个拆分包，并且所有包总长度为6248

    # # 拆分的第一个包，即上面构建的response1
    # send_tcp_ack_data(target_ip, source_ip, target_port, source_port, 1, 696, response1)
    #
    # # 第二个包
    # send_tcp_ack_data(target_ip, source_ip, target_port, source_port, 1361, 696, generate_random_str(1360))
    #
    # # 第三个包
    # send_tcp_ack_data(target_ip, source_ip, target_port, source_port, 2721, 696, generate_random_str(1360))
    #
    # # 第四个包
    # send_tcp_ack_data(target_ip, source_ip, target_port, source_port, 4081, 696, generate_random_str(1360))
    #
    # # 第五个包，此时满足总长度为1097 + 1360 * 3 + 1071 = 6248，所有拆分的包已经发送，回复200
    # send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 5441, 696, generate_random_str(1071))

    # 拆分的第一个包
    # 由于包使用了gzip压缩，所以不能直接传输原始ascii数据流，需要传输十六进制数据流
    # binascii.unhexlify方法将ffffff转化为\xff\xff\xff
    send_tcp_ack_data(target_ip, source_ip, target_port, source_port, 1, 696,
                      binascii.unhexlify(
                          '485454502f312e3120323030204f4b0d0a446174653a205361742c203035204d6172203230323'
                          '22031393a34333a353120474d540d0a5365727665723a205365727665720d0a582d4672616d65'
                          '2d4f7074696f6e733a2053414d454f524947494e200d0a4672616d652d4f7074696f6e733a205'
                          '3414d454f524947494e0d0a4163636570742d52616e6765733a2062797465730d0a566172793a'
                          '204163636570742d456e636f64696e670d0a436f6e74656e742d456e636f64696e673a20677a6'
                          '9700d0a436f6e74656e742d4c656e6774683a20363234370d0a436f6e6e656374696f6e3a2063'
                          '6c6f73650d0a436f6e74656e742d547970653a20746578742f68746d6c0d0a0d0a1f8b0800000'
                          '000000003ed5d7b731347b6ff7fabf63b4c94bd111419cd53f330b6b758c2adcbde6c6e2a4b2a'
                          '7b6b2be51acdf4d863468f8c46d8bea954998089cd23908d8118cc33101c92d824e4616430df2'
                          '5ab19497fe52bdcee999134d2686c3d410109cad2cc749feed3e7d7a74f9f3edd33faca1bff73'
                          'f0c8ffbe7d089b32933af6f6bb7f79f3f0412c8213c47bcc418278e3c81bd83ffeebc8dfdec4a'
                          '818891d31a4545633b5744ad209e2d05b112c32659a99118298999989cd30b1b431491c798798'
                          '45b42894d9fb899bbe9c31c55422e37ffcc3a853e26c524f65c79ad0a1445174b3bb8981a4a0e'
                          'f2430250ca5c6c10739edd858e4603a658294891f99cb800826bb57631113cc9a04cabd1f93a7'
                          '24230bccb19ca9e242a429917fe0ef1ec00fa69319c9d412ba9fcee143637c0423502e5333753'
                          '06eaf7e5bbcf75971f94679e5f628e1defbe31fe0635d4b1dc54c580baf70399b8d60530650c7'
                          '22c404bc2026b27359132409f72be63c37803e16c99a733ac84e0160469c8276a494cbe869492'
                          '1606b0282229cac044330bd204792042513b4e051e5082e9c2ae67e46df3cfcd67fd771696674'
                          'ba8ec5c6921ba98d63bbd5711ab65d266dc09636dfd6739359229b53e6de928e692859e5a2795'
                          '5b1ddebaa0055cae926e1954028e6b44908ce97d022071d31706816224cf1fddc818376c96bc9'
                          '8c0ede023359b7859ccb14bcecba91bcefd6250beb9e950d2d6362ba949acc499330c7b4744c7'
                          '26f46b0ac217b2c4c7f9003c65c2ca9a562d390186a177c26833b3d7116f6c4da2d04d6c3ca58'
                          '8486bd799470298db75d10a2169bc9c48e69909e9ccea54c546e33823e3e9b530c41a7af2004d'
                          '0de510f42a791b68397863e0e0589ba3823131c49c0ee99d12513c09f8ec44290d12062449aa8'
                          'a8e2445a99ab9625e7b2663a0933035d8d60fd29da4193a21dc334287c840b494b01632203651'
                          'df1105c7d8c2a19a9c11a1b3525a8d8b1194d31a7c6221449fe47044ba40d0518631112ea7ba0'
                          'eb194951b4d464f53a9b91e4ca7542928f4e1a10244a0b5c694958a3acd34e344993b14c6a127'
                          '656a04d4e4118d314e3af975b37af29b186cfa86934b9eb3e513028705369968b086483b71a8a'
                          '80775083549a8d80edd6d88429e958ef5ab0072cbf82e388ed4a05d85a9bb201fa7519b5e464a'
                          '53bb526b92448e52674a09ab1494df50f778deddcacf95d2e948e20830a76ca1cc7f1508e1ce2'
                          '93725a4fc3967f959769864a44201a90dc544382cd5dbe76dbbef694daa9511c42b51cc5fb97a'
                          'df35fee9aa39a0be16326330121323143798a1e8de3391d9375299bad3c8d608a644a38fc8514'
                          'b9aac1a23e548c7466e2d8081655d233a9e8eb98733d03af0d244d744333e0d51cfc95460032e'
                          '72692b0a7c35b38e5bb97cd252ab794f71026e01519fda8c682f70df553a54ea81a70ec48621a'
                          '853995ae3125792acb3344a7343327c7e0df185072313945a01ac4a03d09f51232f9601b7f75a'
                          '97ceb2778291993d0b88c4c38'
                      ))

    # 第二个包
    send_tcp_ack_data(target_ip, source_ip, target_port, source_port, 1361, 696,
                      binascii.unhexlify(
                          '9a6f7c14623e55290f9505794f42f5e426872a1a3e861d571a1fadd62a29194791f6d6ea6a54a'
                          'd3ea1fb1eecc4131dc61341d39048d6acafffca6debd44f85ad33c5ad73ad73e1cbd4575e9870'
                          '5e98202ff66adebe7eb2b4be5d7cb2de322ffe4c7de5850de5e503fd03a50937d74e58a7afda9'
                          'b0bd6b98bad73e3cbd4576ee2a1dca833d9d9ecf4b4dc4c3ee7acd3b70af933e55b8feccb3f97'
                          '2fff587a7ab5b876a60d593527d0034e47899cee5cbbfffd2361d867b7343b3d0f1f34d0f886f'
                          '90638b10f639aa361771fd49a0e3ebd322b6a869b37c91e2823a3d6fe5c24ccc0aa243c26e9da'
                          '640adaa8e9cc8eb2da9d27bfa9d9c0e36e580ce3b1759e9bb156b1acf848ab5c3e53ae8385b5d'
                          '80ac18cadb64a30a7bf957682ca8e54829daa852c6d325bdf295bf90cc55ccbf9028bb9a7da76'
                          'f7c23a175e65685735236bbe939e69b7ec1aa9aa7a6749b263dd16201b987ab534936a91a43b3'
                          '763e86e493a649fa5c4c32bd12112c20976dabdc32976d2cd77a5dab6d5e6386d91bd561119c3'
                          '903ebf87106ac7755cc5ce14dc8e24fbd396b50e629f5d2aff6bbde231b4affe68ddb9d22bac0'
                          '68aad4d4439df44a7e2f460e88964da80339640f5ac530bd6faa37e55cba95afb730258d53a74'
                          'f1fd0557b5a6cebc00cddafa808b162670edd3ec29843bb0067620d5235ddabef5104ae9599a8'
                          '4e195f83d8c31d5ce46c53bb62d43c90f513644593dca8421c8baa48c7c74d0bab0ae6e17f277'
                          'ecab4f050cfe2c2e7d82598b9fd8e76e638ee7cc19fb3d8bc0092398803726e0e81cc19c054e6'
                          '82738eb15700a9299ddef0a6784e63878515dc74463b9b3c8c2d0f0e7dfa7e09c0743bed0fa3b'
                          'e994ac6bf251e7663a0352ef6929253db367effe6a49ff79f8cd2387de19c10c700c48ba13c1b'
                          '347c919128ac519a35faf05e68cd1e4defd5e0f1ac1c8fd989c33b269f83393d6522630f65796'
                          'a46331a21a18508d0bf00c0a6474c01e566753385cfad63f119f70e6853a27f075c58a7f30eaf'
                          '2f7562e990046b4ea7f762e117cddd1bdfa1d58f3ffab744cfabbb786ee658e605e19c7240373'
                          'c9ff359b4e65b131ec9fee831a52ea31f361fd6504b640041bc16a069664989aac830aff09959'
                          '01922410a144dcb3c1b176891e31939ced12a1b8fab4c1c105c220e3809b0b8128f277016083c'
                          '2eb22289d33cc9a82aa90a80a563d399c9c8eb0d65e70cdd2d9b26698aa0685220642a2ed2126'
                          'c519ae309b40cee18a3f5f93e7abd91b95e312bb0b0160445c980911489e549564a48715a62a4'
                          '84080495132882a3e2400692880316a838cb28222e81b88c4b0a4df309815579a03acbe3bb304'
                          'b915495598666e867cfaccc137c8260544e042c9f603985154556511441a04459a5244e200005'
                          '444ae6699c4b0009670541c10519b22d72142b4a0a45f114d33eb374fcd9330b2842e1081aa86'
                          '49ca65996853c022050524250589261e38c40902a25a812abe08aa2ca382b27e2b8a08a34aef2'
                          '748222b938927c07cc72cf9e5988619e26188a27454990599216244a9115890634a32a0a1357f'
                          'bc52cf3ec99654902b08420c822cdd20a0b283a418344424900854ff0121fe70899144811501c'
                          '4e020020b31285271401765c4651795516e23427b7a2a048aaa6a0289a0a97ecfbfb9b708754f'
                          'c0e915d3e2def1be66bfafd5d4387da3d0566b0038621cdc111b159aa3751e45263b240422736'
                          '0c262383348c5c2a05c73bf85095f42c6852484a01b3cdf3a6c0ac794039a225e1d81a7878b42'
                          '18f9a4bc96894ae65dc0387c4bd8df2d7540cddc7c6616eecb5d730f47b74acc6048e51813ce8'
                          'e3ab29ccb23f9800424832505dd339734f7de5f73624ff0803b0299a95826a33562dab315b909'
                          '36aadc6dbe280dc9df22b35d9'
                      ))

    # 第三个包
    send_tcp_ack_data(target_ip, source_ip, target_port, source_port, 2721, 696,
                      binascii.unhexlify(
                          '8551ab89d63472a00e173e2e1131252de7922065c6245d0fad9b6bb1c5544d87b65436e633c76'
                          '2b5b06a5858bcb1f62d10903219bd1ee22d66cce852305f437355b99b04e6211da09f7f993bac'
                          'ec89d66847f7c6a0def144ebf4bd7f56c4f1fefeb6a87956dfde98964a01c3093c1fc32291062'
                          '24dfa07faa86903db83fa8fe63c845fa355dcc0ab7dfbc2847374dfbe266d8744ab61af8cd510'
                          'db347f675ced1bc3a25557622dec73a4d6bda3d83ec8c13e2cbab76ac7a6d249498f8ca3274e1'
                          '3c087c887166d52f9f04ef80ceb0b671086b3bedf528d77446145040149797ac2550ee3e1cac1'
                          'a7b0203ab2c0ac28b3488d059cda1b791d83f31572873ef1915f13f8d5b27ffed5580984cae95'
                          'c32e30e4bb5c1a7da4f905e6bec2b88b54a26a8cb2b3f5f81a2883667d3293d862a52c9d82a23'
                          '7fdab3176a064999db536129c88469cc352b15f1964e4c67ab8c3973abe6caa83294a2f4311da'
                          '426cda9909e574b0cfb72a71dafa29c9c286345cb227d87144a2a9d028d4aa54592d5bed11651'
                          '03983923b53bead1a7991af3b757a826f3dad8d3c0dafb5e3bc35f483d87d4cc87c5ba1cd0986'
                          'badba75dd27600ac892294f617b40a0c27e20a26c3e6bcf9fac3b174eb76b015de7f739821c0b'
                          'aae6c0e898e4f3747bf6ccddd93b37677fdc9b3d706b76efceecde8d198c4be83a88201897c0f'
                          '6242ec11f540e66b2133388ae1b93591f54ee4d6827d0da6b64a790559460c28bf66e0859f575'
                          '4b5503ba92c532c684fbab3ea593da17931a3de0957e180ddad171ca0b406d29cf11140c1b1da'
                          'f9851d1dd1c79d14a746c74220167be47a35e386dd45adab06fde2a5f7c6affb0686f2c58ab6b'
                          'c5fc53ebfcc7d6e99bbfceaf22aad6a31f0b9bdfd9db0fad3bf7acefbeb22faec0bfd6c30785c'
                          '7577e9dbf161def968213701b64dd556ebb3435980d6dea969af1ed5c028a76ea0dc9848d89aa'
                          '8a53344e0a219208afde6e21cf3efcd0fdc20fdd03fc84fa4643f1e3c9174ada5a58b3ae3e714'
                          '55c5cbe619d7a607df973219fb77eb96bafe44b279ed8673fb317bf28fd74150addfa7c11de87'
                          '892174ac530be5f925fbcc327c649d7a08ffda8b17acd3370a9bdba55b675db9745f442c161b3'
                          '0a4513819d6e77b8234a65f48637a8e349f633a1469ff9ebf00855f5e59402a6475a3b49eb7ae'
                          '5dfdf7fc67885ee9ccf7f6d239f8006d2a09242a3c3a53d85cc2711c42c85e5d2aaf5cb0164ed'
                          '80f2f5aff3aeb5e169e7c5ebcb701efd8df7f5cbaf7a575fcbcb5bd6e2d9eb22f3d2aae9d8158'
                          '2aadff60e5efd5c3b207f579f930c9f60b936cef31c9ed8e49bf9cfff6eedf0f1f3c60addf41d'
                          '1591716ade5efadab48f856fe94f5f49bf2e5fbf68f5bd6e9b57a107549e025434fbc5fe889f7'
                          '1e3dcc103d03861eae5fe8e17a809ed015ae3e8d87f9b3ee78685df8d4feec6bebc1b2b57ec5d'
                          'a3e635ffeb9b0f565f1cac95fe7bfb016967e9d5fb1bff8d45a3a67af6cf4651874aa3178c320'
                          '8953dd4f022abb01aba97ebf0ea82e5c21fe6df664574e9536b6c9ed4aaad1994177efcf0a383'
                          '3026733744476b8c9a2458a03b2c9220d950a18eeb3684ef5b9efb3e09bedb36086fb2c5aa8e9'
                          '709fc50b1c9c3c8c806f95e23002be734a4390b548d1b799a73b9bb929f9171c65c1e53fe6655'
                          '9fea35c17148396ff18916d61f96fe16121ffa97b0ea9bb2e575cbf55bc70aab0f9a97b4e8ef5'
                          'e8a175fe41f1bba5c2d35bf6f18de2c3ade2d60dfbcac7d6f1553741f1cac9f2fc95e28dbbd1f'
                          '15e111b3c7f008d537d754d0df8a260bc8a2ab6a54541170885cd6debf4f5bf1c3872e4cd4307'
                          '0e1e721d40c56faedba7e7ed9b8fed4b97edd5bcb5b256c8e7cbcb5fd9373f7196ed968b4b8fa'
                          'cc56fca1fcf97367e817702f0'
                      ))

    # 第四个包
    send_tcp_ack_data(target_ip, source_ip, target_port, source_port, 4081, 696,
                      binascii.unhexlify(
                          'ea92eae0618bc2c930f7f38bbf0c48524c155ba4d08ac6eac2dff8f84a697dbd82a6ded019302'
                          'c9138152695177ff9ae1e4b420b2e7457a3948fff589e5f42348af97bdee875e9018a2f387dd3'
                          '5ab8eb0783bd7adfbe7617a99ad50d7bed9675ed72403f754b6df01454bf4135d0ab7aa4cfa42'
                          '2057aa8a0bac6d24bbcc64772352c71b438c452975822c3a4d2132cf1fdc212df132cf9063b56'
                          '6c014bbb070be44f59e78e1736e70b9b9f5bab79fbf1b2f549be82a06e720f1e6efa3a9e09fdc'
                          '24dd892741bb821453884557143f1ad4408fba65d5e286635b47287084cfbca5aebe19a0d51a0'
                          '2193bece4b1f38a38a14713acce6ed0908c57e8150ec0108055aa880302ed294d01e08cb5f5db'
                          '2be3fed0abcf875debaf375f9cbeba55b67e1acdf5abc6a9f3c8ffe5e7a00251f0ea5ce680c18'
                          '86049cee6ba83af23df7c9d949f6004534c5575144b154cbdecee2d6c9e2d627156592ffca551'
                          '4f6c595d2c73fc0d91a5417a57b27adc57f9536b6cbb7bf282e3fb44fdf851aa6f0643500a66e'
                          '490d9e5ea2712acc3ce90da6fae740efda834ea20d34d5e91e2b724c0b98428eeed3b7ac3b27a'
                          'd852bf6f246f9c4dabfe78fc39bc59bcbfe9be5aba70a9bdf4140141edd8437a1f891b5f4e81a'
                          'd44285fc327ab4b0066dede20fdbc5bbd7a3e3bda23a6000239dfd357d9d01527df3a5535d3bd'
                          '321c0a89ad262a12dd682dd8ecc9d07cbf6d61a521c9b575c83c6553fd6e379ebfb8bee585655'
                          '3df6b50bd656beb4be6dddbd54da805a66a9a6716ed7f4578fa80e1ec0a87e6bb0be39d443dd6'
                          'c6d008c1419b20ab0b820740a30440c8d6955e3ddb587d6af977ef9c9ba91b7561fb870287e83'
                          'dea3011161addf2a6e7d6e5f5fb516be2ddec98720ac6db203872f68b93361d64b6ff0d537273'
                          'bd5b5971de18ba66bf88a778c2fbfaaa9d84fbfdc2dae9d718da7d2fa9dd2c671683095367e09'
                          'da5e3d213888c8a2c38698de20ab6f9e76aa6b577b0059620b1b683c23fce672f1eb9fa132f19'
                          '44be1e97a6963cb5d7a296d2fc0cbc2e6e71027bf3d5e4496d29373bf3d5ec25c242073fcc2b9'
                          'a059df15c59710587d73bb535dfbdd03c06adde7e519425b9f95b757ecef6f14578f87cdec503'
                          '985cd33d6b9d3102d701884b7caf7cfdacb3fa32da68b17e0a8585efa11edb0693e8decb6a097'
                          '10717d73ce871a8f6d21ce67e5c759b675c42d7c6b6d9ea8d33a61faa6faee68a8c0ac7317839'
                          '8ea92d42062aa0786fd0bb429cbc9dfdb538106669f57859240f7f6c53a5e531dcd49e83dbafe'
                          '1d604c1f7680f52468791835dd2ac55ad4f4f00d08ed52f2750e2f2cda7ba32216c1c61df2d53'
                          '2ea0a0b943c9a196f7c01eef48c99f5bfffd6f7aa4e671074dfc6ae6a3ac025d384b0fe30ea8c'
                          '8ad191a875febebdbc619f3d5e9e5f2a6c7ee72c2fdf2f7fbe6d7f7ad7be8c2c74fbe2227a4fa'
                          'fb38fca793db02ecda19e91994a9be948c3d6aac613d645222e123cb40969958cb332430b82a4'
                          'ca9ca89214234871562044818e2b224fe38c9ae0719693243c21f3702492138a48b2122f29a2b'
                          'b1b2b6d68935a4ad227dc93f5a7d2498006fd097a8264dc1484fb6e512233debc05dd56eec55e'
                          'a89ed00868b3f8509b85131c6ab397479bc903a9cde02417b0840828992439c0ca3c9320e11f9'
                          '189ab20c1513c29a30d220cc725485c964574f63c3a899da2795c95e3a2aa008553e2ee2b1476'
                          'd2667137c5ef5c9bb1436db603c1a1367b59b459767a7ad6a7cd064599712cc10904477332c59'
                          '2321be7988492205556a2148e8f4b34cb1042429125568156194dd138abc6295c906915e714a8'
                          'd212715e1619f7152995d717a9b02073041dadbc7f07b6fcaa8ec3f6d07b110dc8c7ef5de131f'
                          'c50e185131c2abc9745e1354c'
                      ))

    # 第五个包，此时满足总长度为1096 + 1360 * 3 + 1071 = 6247，所有拆分的包已经发送，回复200
    send_tcp_pshack_data(target_ip, source_ip, target_port, source_port, 5441, 696,
                         binascii.unhexlify(
                             '460745e191242128d08053a16a53199655488111685595048e063c23f1241167394e14f904'
                             '2e7122d47a6282c513095ec56946a539059002c5aa5d293c92e22892162648fef7a7f38667'
                             'a1bb848667a1b742a11767a1efe04aa6aa5dd0c308ae03d51c89fb5ecad855d175e37ad7af'
                             '8777c80e8f196b91e2601c33a66ba9a3f5878c394b25951e0b4131e0878cbde826ccd04e6e'
                             '91e2f03ca5ce29b920db054c0d96340aa2a027cc848e555f658b56c32b751ac499ab309cb9'
                             '86131cf6c841ea913ec3104db870679c8e38c751d5aef119c6b747d41ffe12719f23a77b64'
                             'dc3a7fc63eb1e04e301be25efce578240d29e3d06c72fc95f0a21f7fe54dedff2f9bf0cdec'
                             'c377ec54c29dec33579d7339aea358a9f53bd1f1b027cf2010ea053b3aca93c8ec642b02f1'
                             'b60238b191e5136b2834edcec9df1e2f45c7c39e3c778184859155af6b3fbcf70dbb07dd9a'
                             '60d6246aefbcac55e14f752f4bf457e44f7b22af36e88ebd317403bd682fbbe7c34626a6a4'
                             '94a283112c12f32993d71b53217d514be3688f401ad3d0262781019325d3b92c00291318c1'
                             '544055816cc244d9a9f44cf07136038032823124197834a529e06d09521ec10492f43ffd68'
                             'effeca25fa89f9dee9f7dc43f61c1a81e5c461a8d70e048736caefd04661c9166c14efe086'
                             'ae6d944a612fae8d424c1840d10ca82aff9c85f53cac8cd1c26b725acf2553f037151785d7'
                             '3c66d12352a4e36cf880b9b9888c14e7c84cb4fff7e909385406ee3df7417207190da6d5d2'
                             'ae8c488e0c9551750f5179e57674dc7f35c87219ccc3223d6b5233d3fec0abf0a67ff25971'
                             '6bb5b0f9a97bcc6ca58734bdfddc85f11c2d49a874879664179ffe78bbc4a125194eb0af47'
                             'ad0f0335daa534700e68acdbd7bcfbd81a769e5d290ea7611d52797ec12e1d4aa90369b4df'
                             'eaedb7ee33edaa1d77c9cebb5e6fbad85078dd09af66f71b59f31d689b76214d6f33abecda'
                             'c0dd2881e0be147f5ce378fb4125d0c09635499fa0ea034bc4782db084632244172f01eb72'
                             '5770ffda6eae576d47f7b7ed3a356ffada7a53e954daa8df13d5450bb22f1ffae4d944af5a'
                             '2ffe72b55e36b0ecdb55eb791b4606a9f586a3fdd054db35cb800b0f4b4cca693d0dd3beaa'
                             '265441adc547bb3470339d19a132b35836ad6b0af6aae27cda8e957ece42e7d9488396ab1e'
                             '5d92d414450755ae9dc6187955e0d1bf6e74e1c17466ce40a563bf3d5e3cf8dbe3259aa418'
                             'ace9f978d5d896f2ca6dacb8b4685f3b612fcddbab4b187aef4325d2e5b7c7570a9bf36855'
                             'ef6cbe74ebacbdfcd4befb982179f8082b1d5f466f6c5bfea9b4710da62359b4e38e632986'
                             'e6f8d184418c7b6fb271f6c834af445317fccb3e8f6d9193166abe7b4d77ae59484d9a941c'
                             '2ca99e72c54351f946ff46092fcb283165267594d23f521fd3b29a29a77329ffe29bb3d641'
                             'f9d7e078a6da8d142d0bc7f13967875375d0f6bd0d998423f6ff034aa6801595c60000'
                         ))

    state['describe'] = 'HTTP_RESPONSE_SENT'
    state['num'] = 5
    print(str(state['num']) + ":" + state['describe'])

    # 第一次挥手
    send_tcp_finack(target_ip, source_ip, target_port, source_port, 6512, 696)
    state['describe'] = 'SHAKEHAND1_FIN_SENT'
    state['num'] = 6
    print(str(state['num']) + ":" + state['describe'])

    # 第二次挥手
    sleep(2.901221 - 2.901121)
    send_tcp_ack(source_ip, target_ip, source_port, target_port, 696, 6513)
    state['describe'] = 'SHAKEHAND2_ACK_SENT'
    state['num'] = 7
    print(str(state['num']) + ":" + state['describe'])

    # 第三次挥手
    sleep(2.902224 - 2.901221)
    send_tcp_finack(source_ip, target_ip, source_port, target_port, 696, 6513)
    state['describe'] = 'SHAKEHAND3_FIN_SENT'
    state['num'] = 8
    print(str(state['num']) + ":" + state['describe'])

    # 第四次挥手，断开连接
    sleep(2.906513 - 2.902224)
    send_tcp_ack(target_ip, source_ip, target_port, source_port, 6513, 697)
    state['describe'] = 'SHAKEHAND4_ACK_SENT'
    state['num'] = 9
    print(str(state['num']) + ":" + state['describe'])

    state['describe'] = 'CLOSED'
    state['num'] = 10
    print(str(state['num']) + ":" + state['describe'])

    return state


# def generate_random_str(randomlength=20):
#     """
#     生成一个指定长度的随机字符串
#     """
#     random_str = ''
#     base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz'
#     length = len(base_str) - 1
#     for i in range(randomlength):
#         random_str += base_str[random.randint(0, length)]
#     return random_str


if __name__ == '__main__':
    # state = http_simulate('101.132.158.80', '101.132.158.100', 63315, 80)
    source_ip = sys.argv[1]
    target_ip = sys.argv[2]
    source_port = sys.argv[3]
    target_port = sys.argv[4]
    state = http_simulate(source_ip, target_ip, int(source_port), int(target_port))
    if state['describe'] == 'CLOSED':
        print("Successfully simulate HTTP protocol once")
        print("source_ip:" + state['source_ip'])
        print("target_ip:" + state['target_ip'])
        print("source_port:" + str(state['source_port']))
        print("target_port:" + str(state['target_port']))
