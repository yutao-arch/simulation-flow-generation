from _multiprocessing import send

from scapy.all import *
from scapy.layers.inet import TCP, IP


def send_tcp_syn(source_ip, target_ip, source_port, target_port, source_seq, target_seq):
    """
    第一次握手，发送SYN包：2
    """
    pkt = IP(src=source_ip, dst=target_ip) / TCP(dport=target_port, sport=source_port, seq=source_seq, flags='S')
    send(pkt, verbose=False)


def send_tcp_synack(source_ip, target_ip, source_port, target_port, source_seq, target_seq):
    """
    第二次握手，发送SYN+ACK包：18
    """
    pkt = IP(src=source_ip, dst=target_ip) / TCP(dport=target_port, sport=source_port, seq=source_seq, ack=target_seq,
                                                 flags='SA')
    send(pkt, verbose=False)


def send_tcp_ack(source_ip, target_ip, source_port, target_port, source_seq, target_seq):
    """
    发送ACK包：16
    """
    pkt = IP(src=source_ip, dst=target_ip) / TCP(dport=target_port, sport=source_port, seq=source_seq, ack=target_seq,
                                                 flags='A')
    send(pkt, verbose=False)


def send_tcp_ack_data(source_ip, target_ip, source_port, target_port, source_seq, target_seq, data):
    """
    发送ACK数据包：16
    """
    pkt = IP(src=source_ip, dst=target_ip) / TCP(dport=target_port, sport=source_port, seq=source_seq, ack=target_seq,
                                                 flags='A') / data
    send(pkt, verbose=False)


def send_tcp_finack(source_ip, target_ip, source_port, target_port, source_seq, target_seq):
    """
    发送FIN包：17
    """
    pkt = IP(src=source_ip, dst=target_ip) / TCP(dport=target_port, sport=source_port, seq=source_seq, ack=target_seq,
                                                 flags='FA')
    send(pkt, verbose=False)


def send_tcp_pshack_data(source_ip, target_ip, source_port, target_port, source_seq, target_seq, data):
    """
    发送PSHACK数据包：24
    """
    pkt = IP(src=source_ip, dst=target_ip) / TCP(dport=target_port, sport=source_port, seq=source_seq, ack=target_seq,
                                                 flags='PA') / data
    send(pkt, verbose=False)



