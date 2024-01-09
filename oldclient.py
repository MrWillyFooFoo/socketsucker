import socket
import threading
import clientplayer

import pygame

# Client constants
HEADER = 64
PORT = 5050  # This is the port number
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECTED"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
conn = SERVER

# Game constants
pygame.init()
S_WIDTH, S_HEIGHT = 600, 400
screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
clock = pygame.time.Clock()
RUNNING = True
FPS = 30


# This
def ping():
    while RUNNING:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
        print(f"Server said : {msg}")


# The send function believe it or not, but it sends a message
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


send("Hello, this is a test")
thread = threading.Thread(target=ping)
thread.start()

while RUNNING:
    clock.tick(FPS)
    screen.fill((50, 50, 100))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            send(DISCONNECT_MESSAGE)
            RUNNING = False
    pygame.display.update()
pygame.quit()
