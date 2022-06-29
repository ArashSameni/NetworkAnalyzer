import socket
import re
from collections import namedtuple
from struct import unpack


def unpack_ethernet(data):
    # unpack first 14 bytes of ethernet header
    dest_mac, src_mac, protocol = unpack('! 6s 6s H', data[:14])

    dest_mac = ':'.join(re.findall('..', dest_mac.hex()))
    src_mac = ':'.join(re.findall('..', src_mac.hex()))

    return namedtuple('ethernet', 'dest_mac src_mac proto')(dest_mac, src_mac, hex(protocol))


def unpack_ip(data):
    # unpack 20 bytes of ip header after 14 bytes of ethernet
    ip_header = unpack('! B B H 2s 2s B B 2s 4s 4s', data[14:14 + 20])
    version = ip_header[0] >> 4
    header_length = (ip_header[0] & 0xF) * 4
    diff_serv = hex(ip_header[1])
    total_length = ip_header[2]
    id = '0x' + ip_header[3].hex()
    flags = '0x' + ip_header[4].hex()
    ttl = ip_header[5]
    protocol = ip_header[6]
    checksum = '0x' + ip_header[7].hex()
    src_ip = socket.inet_ntoa(ip_header[8])
    dest_ip = socket.inet_ntoa(ip_header[9])
    payload = data[14 + header_length:]

    return namedtuple('ip', 'version header_length diff_serv total_length id flags ttl protocol checksum src_ip dest_ip payload')(
        version, header_length, diff_serv, total_length, id, flags, ttl, protocol, checksum, src_ip, dest_ip, payload
    )


def unpack_tcp(data):
    # unpack 20 bytes of tcp header
    tcp_header = unpack('! H H 4s 4s H 2s 2s 2s', data[:20])
    src_port = tcp_header[0]
    dest_port = tcp_header[1]
    seq_num = '0x' + tcp_header[2].hex()
    ack = '0x' + tcp_header[3].hex()
    header_length = (tcp_header[4] >> 12) * 4
    reserved = (tcp_header[4] & 0xFFF) >> 6  # 6 bit reserved
    flags = tcp_header[4] & 0x3F  # 6 flag
    window_size = '0x' + tcp_header[5].hex()
    checksum = '0x' + tcp_header[6].hex()
    urgent_pointer = '0x' + tcp_header[7].hex()
    options = data[20:header_length]
    payload = data[header_length:]

    return namedtuple('tcp', 'src_port dest_port seq_num ack header_length reserved flags window_size checksum urgent_pointer options payload')(
        src_port, dest_port, seq_num, ack, header_length, reserved, flags, window_size, checksum, urgent_pointer, options, payload
    )


def parse_tcp_flags(flags):
    urg = (flags & 32) >> 5
    ack = (flags & 16) >> 4
    psh = (flags & 8) >> 3
    rst = (flags & 4) >> 2
    syn = (flags & 2) >> 1
    fin = flags & 1

    return namedtuple('flags', 'urg ack psh rst syn fin')(
        urg, ack, psh, rst, syn, fin
    )


conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(
    0x0003))  # 0x0003 gateway-gateway protocol (capture everything)
while True:
    data, address = conn.recvfrom(65535)
    ethernet_packet = unpack_ethernet(data)
    if ethernet_packet.proto == '0x800':  # 0x800 means IP
        ip_packet = unpack_ip(data)
        if ip_packet.protocol == 6:  # 6 for tcp
            tcp_packet = unpack_tcp(ip_packet.payload)
            flags = parse_tcp_flags(tcp_packet.flags)
            if flags.syn and flags.ack:
                print(
                    f'Port {tcp_packet.src_port} is open on {ip_packet.src_ip}')
