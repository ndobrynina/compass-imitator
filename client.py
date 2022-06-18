import socket
import sys

HOST, PORT = '192.168.208.77', 34458
connected = False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")


print("Received: {}".format(received))