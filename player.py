import pygame
import random

PLAYER_SIZE = 128, 128
SPEED = 3


class Player:

    def __init__(self, _name: str, _pos: tuple):
        self.Name = _name

        self.x_pos = _pos[0]

        self.y_pos = _pos[1]

        self.rect = pygame.Rect((self.x_pos, self.y_pos), PLAYER_SIZE)

        self.color = (random.randrange(255), random.randrange(255), random.randrange(255))

    def update(self, surface):
        self.rect = pygame.Rect((self.x_pos, self.y_pos), PLAYER_SIZE)
        pygame.draw.rect(surface, self.color, self.rect)

    def move(self, movement):
        hinput, vinput = movement[0], movement[1]

        self.x_pos += hinput * SPEED
        self.y_pos += vinput * SPEED

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
