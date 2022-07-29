import socket
from concurrent.futures import *

def try_tcp_connection(target, port):
    print(f'Trying to connect on port {port}')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(False)
    s.connect((target, port))
    s.close()

target = input('Target: ')
start_port, end_port = [int(x) for x in input('Port range(1-1000): ').split('-')]

executor = ThreadPoolExecutor(max_workers=10)
futures = [executor.submit(try_tcp_connection, target, port) for port in range(start_port, end_port + 1)]
wait(futures, return_when=ALL_COMPLETED)