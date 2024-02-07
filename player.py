import pygame
import random

PLAYER_SIZE = 128, 128


class Player:

    def __init__(self, _name: str, _pos: tuple):
        self.Name = _name

        self.x_pos = _pos[0]

        self.y_pos = _pos[1]

        self.rect = pygame.Rect((self.x_pos, self.y_pos), PLAYER_SIZE)

        self.color = (random.randrange(255), random.randrange(255), random.randrange(255))

        self.position = (self.x_pos, self.y_pos)

    def update(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def update_position(self, key):
        key = key.lower()
        match key:
            case "w":
                self.y_pos = 3
            case "a":
                self.x_pos -= 2
            case "s":
                self.y_pos += 2
            case "d":
                self.x_pos += 2


    @property
    def name(self):
        return self.Name

    @name.setter
    def name(self, value):
        self.Name = value

    @property
    def get_position(self):
        return self.position


