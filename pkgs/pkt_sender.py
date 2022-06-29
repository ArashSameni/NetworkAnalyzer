import socket
from binascii import unhexlify


def pack(content):
    return unhexlify(content)


def send_packet(pkt, interface="lo"):
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    s.bind((interface, 0))
    return s.send(pkt)
