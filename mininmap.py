from pkgs.sender_syn_tcp import *

target = input('Target: ')
start_port, end_port = [int(x) for x in input('Ports range: ').split('-')]

f = open('info.txt', 'r')
lines = f.readlines()
src_ip = lines[2]
src_port = int(lines[3])
interface = lines[4].strip()
src_mac = lines[5].strip().replace(' ', '')
dest_mac = lines[6].strip().replace(' ', '')
for i in range(start_port, end_port + 1):
    send_syn(target, i, src_ip, src_port, dest_mac, src_mac, interface)
    print(f'Sent TCP SYN packet on port {i}')