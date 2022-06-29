from pkgs.pkt_sender import *

content = input('Content of your packet: ')
interface = input('Interface: ')
try:
    send_packet(pack(content), interface)
    print(f'Sent {len(content)//2}-byte packet on {interface}')
except Exception as e:
    print('Error: ' + str(e))