import socket
import sys

HOST, PORT = '192.168.208.77', 34444
connected = True

def recvall(sock):
    BUFF_SIZE = 4096
    data = bytearray()
    while True:
        packet = sock.recv(BUFF_SIZE)
        if not packet:
            break
        data.extend(packet)
    return data

while connected:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        try:
            d = recvall(sock)
            print(f'{d}')
        except KeyboardInterrupt:
            print('smth wrong')
            sock.close()