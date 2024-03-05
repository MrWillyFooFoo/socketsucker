import socket
import threading
import pickle

# Server Constants

HEADER = 16
PORT = 5050  # This is the port number
SERVER = socket.gethostbyname(socket.gethostname())  # This gets my local IPV4 Address
ADDR = (
    SERVER,
    PORT,
)  # When we bind our socket to a specific address it needs to be in a tuple
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECTED"
NAME_REQ = "!NAME:"
MOVE_REQ = "!MOVE"

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

                    send(client_name, conn)

                    print(client_name)
            else:
                dataclass = type(msg)
            print(f"{addr} said: {msg}")
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
        conn, addr = (server.accept())  # This line will wait, for a connection, then store the addr and port
        print(conn, addr)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"ACTIVE CONNECTIONS : {threading.active_count() - 1}")


print("Server is starting")
start()
