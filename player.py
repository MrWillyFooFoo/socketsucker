import pygame
import random
import math
import sympy

PLAYER_SIZE = 128, 128
SPEED = 0.1


class Player:

    def __init__(self, _name: str, _pos: tuple):
        self.Name = _name

        self.x_pos = _pos[0]

        self.y_pos = _pos[1]

        self.rect = pygame.Rect((self.x_pos, self.y_pos), PLAYER_SIZE)

        self.color = (random.randrange(255), random.randrange(100), random.randrange(255))

    def update(self, surface):
        self.rect = pygame.Rect((self.x_pos, self.y_pos), PLAYER_SIZE)
        pygame.draw.rect(surface, self.color, self.rect)

    def move(self, movement):
        hinput, vinput = movement[0], movement[1]
        raddir = math.atan2(0 - vinput, hinput)  # Direction in radians
        degdir = (raddir * (180 / math.pi))
        pntdir = (degdir + 360) % 360
        radlen = [(SPEED * math.cos(math.radians(pntdir))), (SPEED * -math.sin(math.radians(pntdir)))]
        radlen[0] = math.degrees(radlen[0])
        radlen[1] = math.degrees(radlen[1])
        print(radlen[0], radlen[1])

        self.x_pos += radlen[0]
        self.y_pos += radlen[1]

    def player_input(self, key):
        pass

    @property
    def name(self):
        return self.Name

    @name.setter
    def name(self, value):
        self.Name = value

    @property
    def get_position(self):
        return self.position
