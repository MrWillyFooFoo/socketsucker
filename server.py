import socket
import threading
import pickle
import pygame

# Server Constants

HEADER = 16
PORT = 6050  # This is the port number
SERVER = socket.gethostbyname(socket.gethostname())  # This gets my local IPV4 Address
ADDR = (
    SERVER,
    PORT,
)  # When we bind our socket to a specific address it needs to be in a tuple

Clients = []

FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECTED"
NAME_REQ = "!NAME:"
MOVE_REQ = "!MOVE"
CHAT_REQ = "!CHAT"

server = socket.socket(
    socket.AF_INET,         # What type of addresses we are looking for
    socket.SOCK_STREAM
    )
server.bind(ADDR)  # Binding the address to the socket

# Game constants
PLAYER_SIZE = 128
S_WIDTH, S_HEIGHT = 1200, 800
FPS = 60


def handle_client(conn, addr):
    global Clients
    print(f"[New connection] {addr} connected, assigning a rect.")

    connected = True

    while connected:

        msg_length = conn.recv(HEADER).decode(FORMAT)

        if msg_length:  # if recieving data

            msg_length = int(msg_length)
            data = conn.recv(msg_length)
            obj = False

            try:
                msg = data.decode(FORMAT)
            except:
                msg = pickle.loads(data)
                obj = True

            if not obj:  # If msg was not an object

                if msg == DISCONNECT_MESSAGE:

                    connected = False
                    print(f"Player disconnected, : {threading.active_count() - 1}")
                elif NAME_REQ in msg:

                    client_name = msg[len(NAME_REQ) : :]

                    for x in Clients:
                        if x != conn:
                            send(client_name, x)

                    print(client_name)

                if CHAT_REQ in msg:

                    msg1 = msg.split(";")
                    message = msg1[0]
                    sender = msg1[1]

                    print(f"The ready to send message is...{msg}")

                    print(f"Sending message {message} from {sender} aka {conn} to other clients...")
                    for x in Clients:
                        if x != conn:
                            send(msg, x)
            else:
                dataclass = type(msg)

                if dataclass == pygame.rect.Rect:
                    for x in Clients:
                        if x != conn:
                            send(msg, x)
                            print("sending rect to the other player")

            print(f"LOG:   ---{addr} said:---{msg}")
    conn.close()


def send(msg, conn):
    global Clients

    try:
        message = msg.encode(FORMAT)
    except:
        message = pickle.dumps(msg)

    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


def start():  # Used to start listening to connections
    global Clients
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = (server.accept())  # This line will wait, for a connection, then store the addr and port
        print(conn, addr)
        client = conn
        Clients.append(client)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"ACTIVE CONNECTIONS : {threading.active_count() - 1}")


print("Server is starting")
start()
