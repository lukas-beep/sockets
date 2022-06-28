from concurrent.futures import thread
import socket
import threading

HEADER = 64
PORT = 5050
SERVER = "192.168.0.109"
ADDR = (SERVER, PORT)
DISCONNECT_MSG = "!DISCONNECT"
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

msgs = []
def msg_colector():
    while True:
        msg = client.recv(1024).decode()
        msgs.append(msg)
        print(msg)

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)


thread = threading.Thread(target=msg_colector)
thread.start()

# send("Hello")
# input()
# send("World")
# input()
# send("!")
# input()
# send(DISCONNECT_MSG)

while True:
    send(input(""))