import pygame


class Button:
    def __init__(self, image, pos, text_input, font):
        self.image = image
        self.text_input = text_input
        self.text = font.render(self.text_input, True, "white")
        if self.image is None:
            self.image = self.text
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.font = font

    def update(self, screen):
        if self.image is None:
            screen.blit(self.text, self.text_rect)
        screen.blit(self.image, self.rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.image = self.font.render(self.text_input, True, (0, 255, 0))
        else:
            self.image = self.font.render(self.text_input, True, (255, 255, 255))
