from pkgs.pkt_sender import *
from pkgs.sender_syn_tcp import *

f = open('info.txt', 'r')
lines = f.readlines()
dest_ip = lines[0]
dest_port = int(lines[1])
src_ip = lines[2]
src_port = int(lines[3])
interface = lines[4].strip()
src_mac = lines[5].strip().replace(' ', '')
dest_mac = lines[6].strip().replace(' ', '')
send_syn(dest_ip, dest_port, src_ip, src_port, dest_mac, src_mac, interface)
print('54 bytes sent on ' + interface)