import pygame
import random
import math
import pickle

PLAYER_SIZE = 128, 128
SPEED = 0.1


class Player:

    def __init__(self, _name: str, _pos: tuple):
        self.Name = _name

        self.x_pos = _pos[0]

        self.y_pos = _pos[1]

        self.rect = pygame.Rect((self.x_pos, self.y_pos), PLAYER_SIZE)

        self.color = (random.randrange(255), random.randrange(100), random.randrange(255))

        pickle.dumps(self.rect)

    def update(self, surface):
        self.rect = pygame.Rect((self.x_pos, self.y_pos), PLAYER_SIZE)
        pygame.draw.rect(surface, self.color, self.rect)

    def move(self, movement):
        hinput, vinput = movement[0], movement[1]
        degdir = math.degrees(math.atan2(0 - vinput, hinput))  # Direction in degrees
        pntdir = (degdir + 360) % 360
        radlen = [math.degrees(SPEED * math.cos(math.radians(pntdir))), math.degrees(SPEED * -math.sin(math.radians(pntdir)))]

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

    def get_rect(self):
        return self.rect
