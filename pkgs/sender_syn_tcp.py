from socket import inet_aton
from . import pkt_sender
from . import checksum


def send_syn(dest_ip, dest_port, src_ip, src_port, dest_mac, src_mac, interface):
    # total frame length: 20 + 20 + 14 = 54
    layer3_protocol_number = '0800'  # EtherType: 0800 for IPv4
    version = '45'  # 4: IPv4, 5: 5*32 bits (20 bytes)
    diff_serv = '10'  # for QoS
    total_length = '0028'  # 28: 40 bytes, 3c: 60 bytes
    id = '07c3'
    flags = '4000'  # don't fragment
    ttl = '40'
    layer4_protocol_number = '06'  # tcp
    seq_num = 'c039a735'
    ack = '00000000'
    tcp_header_length = '5002'  # 5: 20 bytes, a: 40 bytes, 002: SYN
    window_size = '7210'
    urgent_pointer = '0000'
    dest_ip = inet_aton(dest_ip).hex()
    dest_port = '%04x' % dest_port
    src_ip = inet_aton(src_ip).hex()
    src_port = '%04x' % src_port
    tcp_checksum = checksum.cs(src_ip + dest_ip + '00' + layer4_protocol_number + '0014' +
                               src_port + dest_port + seq_num + ack +
                               tcp_header_length + window_size + '0000' + urgent_pointer)
    ip_checksum = checksum.cs(version + diff_serv + total_length + id +
                              flags + ttl + layer4_protocol_number + '0000' + src_ip + dest_ip)
    packet = pkt_sender.pack(dest_mac + src_mac + layer3_protocol_number
                             + version + diff_serv + total_length + id
                             + flags + ttl + layer4_protocol_number + ip_checksum
                             + src_ip + dest_ip + src_port + dest_port
                             + seq_num + ack + tcp_header_length
                             + window_size + tcp_checksum + urgent_pointer)
    pkt_sender.send_packet(packet, interface)