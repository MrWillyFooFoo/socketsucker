import pygame, random, math, pickle

PLAYER_SIZE = 128, 128                              # The size of the player sprite
SPEED = 0.1                                         # Speed constant for player movement


class Player:                                       # The player class

    def __init__(self, _name: str, _pos: tuple):    # Constructor

        self.Name = _name                           # Name attribute

        self.x_pos = _pos[0]                        # Attribute stores X position
        self.y_pos = _pos[1]                        # Attribute stores Y position

        self.rect = pygame.Rect((self.x_pos, self.y_pos), PLAYER_SIZE) # Stores the players rect
        self.color = (random.randrange(255), random.randrange(100), random.randrange(255)) # Generates random color

        pickle.dumps(self.rect)                     # Serializes the rect to be sent later

    def update(self, surface):                                          # Updates the rect on the clients screen
        self.rect = pygame.Rect((self.x_pos, self.y_pos), PLAYER_SIZE)  # Sets the old ract with new values
        pygame.draw.rect(surface, self.color, self.rect)                # Draws the rect to the surface provided

    def move(self, movement):                                           # Moves the client, takes keyboard input
        hinput, vinput = movement[0], movement[1]                       # takes tuple movement and turns it into two
                                                                        # seperate variables which is easier to read
        '''
        Summary: Converts movement to degrees
        This part of the code gets the direction of the vector between two points,
        I made it so the distance x, y, is either -1, 0 or 1 and the starting
        points as 0, 0, just to make things more simple, it also can be easier 
        to understand if you think of it as a unit circle, the angle we are
        getting is between the positive x and the direction of movement, tan2 
        takes into account of the negative quadrants and all that annoying
        stuff making it easier.
        '''

        degdir = math.degrees(math.atan2(0 - vinput, hinput))           # Refer to the block above
        pntdir = (degdir + 360) % 360                                   # I forgot what this does but its important

        lendir = [                                                      # Converts the radians into degrees stores
            math.degrees(SPEED * math.cos(math.radians(pntdir))),       # as a list cause why the hell not.
            math.degrees(SPEED * -math.sin(math.radians(pntdir)))
            ]

        self.x_pos += lendir[0]                                         # += lendir to the x pos
        self.y_pos += lendir[1]                                         # += lendir to the y pos

    def player_input(self, key):
        pass

    @property
    def name(self):
        return self.Name

    @name.setter
    def name(self, value):
        self.Name = value

    def get_rect(self):
        return self.rect
