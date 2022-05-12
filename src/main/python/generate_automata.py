import sys

import dpkt as dpkt


def generate_automata(pcap_path, automata_path):
    """
    自动生成模型自动机
    :param pcap_path: 待分析pcap文件路径
    :return:
    """
    # scapy解析pcap一直报错，选择使用dpkt解析pcap
    top = 'import sys\n' \
          'from utils.send_packets import send_tcp_syn, send_tcp_synack, send_tcp_ack, send_tcp_pshack_data, send_tcp_ack_data, send_tcp_finack\n' \
          '\n' \
          '\n' \
          'def simulate(source_ip, target_ip, source_port, target_port):\n'
    completion = '    '
    bottom = 'if __name__ == \'__main__\':\n' \
             '    # simulate(\'101.132.158.80\', \'101.132.158.100\', 63315, 80)\n' \
             '    source_ip = sys.argv[1]\n' \
             '    target_ip = sys.argv[2]\n' \
             '    source_port = sys.argv[3]\n' \
             '    target_port = sys.argv[4]\n' \
             '    simulate(source_ip, target_ip, int(source_port), int(target_port))'
    f = open(pcap_path, 'rb')
    pcap = dpkt.pcap.Reader(f)
    all_command = ''
    all_command = all_command + top
    for ts, buf in pcap:
        protocol_map = {'syn': 2, 'synack': 18, 'ack': 16, 'pshack_data': 24, 'finack': 17}  # ack和ack_data后续再判断
        server_port_list = [80, 25, 110, 143, 22, 23]
        method_list = ['send_tcp_syn', 'send_tcp_synack', 'send_tcp_ack', 'send_tcp_ack_data', 'send_tcp_finack',
                       'send_tcp_pshack_data']
        command = 'send_tcp_'
        eth = dpkt.ethernet.Ethernet(buf)  # eth包
        ip = eth.data  # ip包
        tcp = ip.data  # tcp包
        raw = tcp.data  # raw包

        # source_ip = ip.src
        # target_ip = ip.dst
        source_port = tcp.sport
        # target_port = tcp.dport
        source_seq = tcp.seq
        target_seq = tcp.ack
        flags = tcp.flags
        data = raw

        for protocol_key, protocol_value in protocol_map.items():
            if protocol_value == flags:
                command = command + protocol_key  # 加上protocol
                if len(data) != 0 and protocol_key == 'ack':  # ack的需要判断需不需要加上data
                    command = command + '_data'
        command = command + '('
        if source_port in server_port_list:  # 加上ip和port
            command = command + 'target_ip, source_ip, target_port, source_port, '
        else:
            command = command + 'source_ip, target_ip, source_port, target_port, '
        command = command + str(source_seq) + ', ' + str(target_seq)  # 加上seq和ackseq
        if len(data) != 0:  # 加上data
            command = command + ', '
            command = command + str(data) + ')'
        else:
            command = command + ')'
        for method in method_list:  # 优化：去掉一些pacap中失败的包
            if method in command:
                all_command = all_command + completion + command + '\n'
                break
    all_command = all_command + '\n\n' + bottom
    # print(all_command)
    file = open(automata_path, 'w', encoding='UTF-8')
    file.write(all_command)
    file.close()


if __name__ == '__main__':
    # generate_automata(r'C:\Users\10636\graduationDesign\simulation-flow-generation\src\main\python\pcap\过滤后http.pcap',
    #                   r'C:\Users\10636\graduationDesign\simulation-flow-generation\src\main\python\automata\httpAutomata.txt')
    pcap_path = sys.argv[1]
    automata_path = sys.argv[2]
    generate_automata(pcap_path, automata_path)


