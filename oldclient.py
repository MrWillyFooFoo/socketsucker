import socket, sys, threading, button, pygame, pickle, player

# -----CLIENT CONSTANTS -----#
HEADER = 16                                         # Header of the packets.
PORT = 6050                                         # This is the port number.
FORMAT = "utf-8"                                    # Format which we are encoding in.
DISCONNECT_MESSAGE = "!DISCONNECTED"                # If this message is sent we disconnect from the server.
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)                                               # stores the port and ip in a tuple.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          # Gets the clients ipv4.
conn = SERVER

# -----GAME CONSTANTS-----
pygame.init()                                                       # Initializes pygame.
S_WIDTH, S_HEIGHT = 1200, 800                                       # Height and width of the screen.
Screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))               # the display with set height and width.
clock = pygame.time.Clock()                                         # the clock object.

RUNNING = True                                      # The game is running.
FPS = 60                                            # The frames per second.
JustOpened = True                                   # Whether or not the program was just opened.
PLAYER_INPUT = []                                   # Stores player keyboard input.
NAME_INPUT = []                                     # Stores specifically the name.
CLIENT_CHAT = []
MAX_INPUT = 50                                      # Max ammount of characters allowed in input.
global CONNECT_RESPONSE
PLAYERS = []                                        # Global variable.
CHAT = []
CONNECT_RESPONSE = ""                               # used to display responses to connection issues (debug).
CHAT_REQ = "!CHAT"


def chat_request(message):
    thing = "!CHAT"
    return thing+""+message


def ping():
    global PLAYERS                                  # Pings the server, will be used in loops to check for updates
    msg = ""                                        # Variable used to store the message
    while RUNNING:                                  # Constantly checking

        clock.tick(FPS)

        msg_length = client.recv(HEADER).decode(FORMAT)
        # recv the size of the incoming message
        if msg_length:                                              # If the message = to something
            msg_length = int(msg_length)
            obj = False                                             # Converts to integer
            msg = client.recv(msg_length)
            try:
                newmessage = msg.decode(FORMAT)          # Decodes the message using utf-8
            except:
                newmessage = pickle.loads(msg)
                obj = True

            if not obj:

                if CHAT_REQ in newmessage:
                    msg = newmessage.split(";")
                    message = msg[0]
                    message.removeprefix(CHAT_REQ)
                    sender = msg[1]

                    print(f"{sender} Said: {message}...")

            elif type(newmessage) == pygame.rect.Rect:
                rect = newmessage
                Player_Pos = rect.x, rect.y

                if len(PLAYERS) == 0:
                    pass
                elif len(PLAYERS) == 1:

                    OtherPlayer = player.Player("Name", rect)

                    PLAYERS.append(OtherPlayer)

                elif len(PLAYERS) == 2:

                    Other = PLAYERS[1]
                    Other.changex(Player_Pos[0])
                    Other.changey(Player_Pos[1])

                elif len(PLAYERS) < 2:
                    Temp = PLAYERS[0]
                    PLAYERS = [Temp]


def send(msg):                                      # The send function believe it or not, sends a message
    try:                                            #
        message = msg.encode(FORMAT)
        print(f"Sending a message, no rect {type(message)}")
    except:
        message = pickle.dumps(msg)
        print("SENDING RECT TO SERVER")

    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def get_font(size):
    return pygame.font.SysFont("Press-Start-2p", size, False, False)


# send("Hello, this is a test")

def Identity():
    thread = threading.Thread(target=ping)
    thread.start()

    while True:
        clock.tick(FPS)
        NAME_STRING = "".join(NAME_INPUT)
        Screen.fill((0, 0, 0))
        IDENTITY_MOUSE = pygame.mouse.get_pos()

        NAME_TEXT = get_font(45).render(NAME_STRING, True, "White")
        NAME_RECT = NAME_TEXT.get_rect(center=(S_WIDTH / 2, (S_HEIGHT / 2) - 50))
        Screen.blit(NAME_TEXT, NAME_RECT)

        IDENTITY_CONFIRM = button.Button(image=None, pos=(S_WIDTH / 2, S_HEIGHT / 2), text_input="Connect",
                                         font=get_font(75))

        IDENTITY_CONFIRM.changeColor(IDENTITY_MOUSE)
        IDENTITY_CONFIRM.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                send(DISCONNECT_MESSAGE)
                pygame.quit()
                sys.exit()
            if event.type == pygame.TEXTINPUT:
                char = event.text
                if len(NAME_INPUT) < MAX_INPUT:
                    NAME_INPUT.append(char)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(NAME_INPUT) > 0:
                        del NAME_INPUT[-1]
            if event.type == pygame.MOUSEBUTTONDOWN and IDENTITY_CONFIRM.checkForInput(IDENTITY_MOUSE):
                if not len(NAME_STRING) < 3:
                    send(f"!NAME:{NAME_STRING}")
                    Gameplay(NAME_STRING)
                    break

        pygame.display.update()


def Gameplay(local_name):
    global CLIENT_CHAT
    global PLAYERS
    global CHAT
    local_pos = 250, 250
    LOCAL_PLAYER = player.Player(local_name, local_pos)
    send(LOCAL_PLAYER.get_rect())

    PLAYERS.append(LOCAL_PLAYER)

    previousrect = LOCAL_PLAYER.get_rect()
    PreviousPosition = previousrect.x, previousrect.y

    while RUNNING:

        clock.tick(FPS)
        GAMEPLAY_MOUSE = pygame.mouse.get_pos()
        bg_color = (76, 176, 81)
        Screen.fill(bg_color)

        CurrentRect = LOCAL_PLAYER.get_rect()
        CurrentPosition = CurrentRect.x, CurrentRect.y

        if PreviousPosition != CurrentPosition:
            send(CurrentRect)
            PreviousPosition = CurrentPosition

        for x in PLAYERS:
            x.update(Screen)

            TEXTCHAT = get_font(35).render("--CHAT ROOM--", True, "Black")
            TEXTCHATRECT = TEXTCHAT.get_rect(center=(S_WIDTH / 2, (S_HEIGHT / 2) - 375))
            Screen.blit(TEXTCHAT, TEXTCHATRECT)


        keys = pygame.key.get_pressed()
        movement = (keys[ord("d")] - keys[ord("a")]), (keys[ord("s")] - keys[ord("w")])
        if movement[0] != 0 or movement[1] != 0:
            if PLAYERS[0].getstate() == "normal":
                PLAYERS[0].move(movement)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                send(DISCONNECT_MESSAGE)
                pygame.quit()
                sys.exit("GameClosed")
            if keys[ord("t")] and PLAYERS[0].getstate() == "normal":
                PLAYERS[0].changestate()
            if event.type == pygame.TEXTINPUT:
                if PLAYERS[0].getstate() == "talking":
                    char = event.text
                    CLIENT_CHAT.append(char)
            if keys[pygame.K_RETURN] and PLAYERS[0].getstate() == "talking":
                LOCAL_PLAYER.changestate()
                clientmessage = "".join(CLIENT_CHAT)
                clientmessage = chat_request(clientmessage)
                clientmessage = "".join(clientmessage)

                senderinfo = clientmessage+";"+local_name
                send(senderinfo)
                clientmessage = clientmessage.removeprefix(CHAT_REQ)
                clientmessage = "You: " + clientmessage
                CHAT.append(clientmessage)

        pygame.display.update()



def Connect(address):
    global CONNECT_RESPONSE
    print(f"started {address}")

    localstring = ""

    if address.lower() == localstring:
        address = SERVER
    else:
        try:
            address = (address, PORT)
            client.connect(address)
            CONNECT_RESPONSE = f"Connecting to {address}"
        except:
            CONNECT_RESPONSE = "Connection Timed Out"
            Play()
    address = (address, PORT)
    client.connect(address)
    Identity()


def Play():
    global CONNECT_RESPONSE
    print(CONNECT_RESPONSE)
    while True:
        clock.tick(FPS)
        PLAY_MENU_MOUSE = pygame.mouse.get_pos()
        Screen.fill((50, 0, 0))  # Makes screen black so previous "screen" will not show its previous stuff
        INPUT_TEXT = "".join(PLAYER_INPUT)

        PLAY_TEXT = get_font(45).render(INPUT_TEXT, True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(S_WIDTH / 2, (S_HEIGHT / 2) - 50))
        Screen.blit(PLAY_TEXT, PLAY_RECT)

        DIRECTION_TEXT = get_font(75).render("Enter Address", True, "White")
        DIRECTION_RECT = DIRECTION_TEXT.get_rect(center=(S_WIDTH / 2, (S_HEIGHT / 2) - 100))
        Screen.blit(DIRECTION_TEXT, DIRECTION_RECT)

        CONSOLE_TEXT = get_font(45).render(CONNECT_RESPONSE, True, "purple")
        CONSOLE_RECT = CONSOLE_TEXT.get_rect(center=(S_WIDTH / 2, (S_HEIGHT / 2) + 75))
        Screen.blit(CONSOLE_TEXT, CONSOLE_RECT)

        PLAY_TEXTBOX = button.Button(image=None, pos=(S_WIDTH / 2, S_HEIGHT / 2), text_input="Connect",
                                     font=get_font(75))

        PLAY_TEXTBOX.changeColor(PLAY_MENU_MOUSE)
        PLAY_TEXTBOX.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # send(DISCONNECT_MESSAGE)
                pygame.quit()
                sys.exit()
            if event.type == pygame.TEXTINPUT:
                char = event.text
                if len(PLAYER_INPUT) < MAX_INPUT:
                    PLAYER_INPUT.append(char)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(PLAYER_INPUT) > 0:
                        del PLAYER_INPUT[-1]
            if event.type == pygame.MOUSEBUTTONDOWN and PLAY_TEXTBOX.checkForInput(PLAY_MENU_MOUSE):
                Connect(INPUT_TEXT)
                break

        pygame.display.update()


# Main Menu Constants
MAIN_MENU_PLAY = button.Button(image=None, pos=(S_WIDTH / 2, S_HEIGHT / 2), text_input="Play", font=get_font(75))


def MainMenu():
    while True:
        clock.tick(FPS)
        MAIN_MENU_MOUSE = pygame.mouse.get_pos()
        clock.tick(FPS)
        Screen.fill((0, 0, 50))

        MAIN_MENU_TEXT = get_font(45).render("SocketSucker!", True, "White")
        MAIN_MENU_RECT = MAIN_MENU_TEXT.get_rect(center=(S_WIDTH / 2, (S_HEIGHT / 2) - 50))
        Screen.blit(MAIN_MENU_TEXT, MAIN_MENU_RECT)

        MAIN_MENU_PLAY.changeColor(MAIN_MENU_MOUSE)
        MAIN_MENU_PLAY.update(Screen)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # send(DISCONNECT_MESSAGE)
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and MAIN_MENU_PLAY.checkForInput(MAIN_MENU_MOUSE):
                print("going to play screen...")
                Play()
                break

        pygame.display.update()


if JustOpened:
    MainMenu()
    JustOpened = False
