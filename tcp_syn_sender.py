from pkgs.pkt_sender import *
from pkgs.sender_syn_tcp import *

with open('info.txt', 'r') as file:
    lines = [':'.join(line.split(':')[1:]).strip() for line in file.readlines()]
    dest_ip = lines[0]
    dest_port = int(lines[1])
    src_ip = lines[2]
    src_port = int(lines[3])
    interface = lines[4]
    src_mac = lines[5].replace(':', '')
    dest_mac = lines[6].replace(':', '')
    send_syn(dest_ip, dest_port, src_ip, src_port, dest_mac, src_mac, interface)
    print('54 bytes sent on ' + interface)