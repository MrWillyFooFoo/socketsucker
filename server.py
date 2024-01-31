import socket
import threading
import pickle

# Server Constants
HEADER = 16
PORT = 5050  # This is the port number
SERVER = socket.gethostbyname(socket.gethostname())  # This gets my local IPV4 Address
ADDR = (SERVER, PORT)  # When we bind our socket to a specific address it needs to be in a tuple
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECTED"
NAME_REQ = "!NAME:"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # What type of addresses we are looking for
server.bind(ADDR)  # Binding the address to the socket
local_name = "--EmptyData--"

# Game Constants


# Listening

def get_player():
    pass


def handle_client(conn, addr):
    print(f"[New connection] {addr} connected, assigning a rect.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            elif NAME_REQ in msg:
                local_name = (msg[len(NAME_REQ)::])
                send(local_name, conn)

                get_player()

            print(f"{addr} {msg}")

    conn.close()


def send(msg, conn):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


def start():  # Used to start listening to connections
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()  # This line will wait, for a connection, then store the addr and port
        print(conn, addr)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"ACTIVE CONNECTIONS : {threading.active_count() - 1}")


print("Server is starting")
start()
