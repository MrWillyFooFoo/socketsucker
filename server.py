import socket
import threading


HEADER = 64
PORT = 5050  # This is the port number
SERVER = socket.gethostbyname(socket.gethostname())  # This gets my local IPV4 Address
ADDR = (SERVER, PORT)  # When we bind our socket to a specific address it needs to be in a tuple
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECTED"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # What type of addresses we are looking for
server.bind(ADDR)  # Binding the address to the socket

# Listening


def handle_client(conn, addr):
    print(f"[New connection] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        print(msg_length)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"{addr} {msg}")
            send("Test", conn)

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
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"ACTIVE CONNECTIONS : {threading.activeCount() -1}")

print("Server is starting")
start()

send("Hello", conn)
input()
