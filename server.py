import socket
import threading
import datetime

HEADER = 64
PORT = 5050
SERVER = "192.168.0.109"
ADDR = (SERVER, PORT)
DISCONNECT_MSG = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []

def broadcast(msg, conn):
    for client in clients:
        if conn != client[1]:
            client[1].send(msg.encode("utf-8"))

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append((addr, conn))
    connected = True
    while connected:
        msg_len = conn.recv(HEADER).decode("utf-8")
        if msg_len:
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode("utf-8")
            if msg == DISCONNECT_MSG:
                connected = False

            print(f"[{addr}] {msg}")
            threadd = threading.Thread(target=broadcast, args=(msg, conn))
            threadd.start()

    conn.close()

def start():
    server.listen()
    print("[LISTENING] Server is listening on ", server)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print("[ACTIVE CONNECTIONS]", threading.active_count()-1)
        

print("[Starting...]")
start()