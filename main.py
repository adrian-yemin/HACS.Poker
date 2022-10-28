import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import random

pygame.mixer.init()
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


class Card(pygame.sprite.Sprite):
    def __init__(self):
        super(Card, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()



class Player1:
    def __init__(self, name, image):
        self.name = name
        self.image = image
        self.stack = 1000
        self.chipsInPlay = 0
        self.turn = False


    def turn(self, c1, c2):
        Player1.turn = True

class Button:
    def __init__(self, x, y):
        self.x = x
        self.y = y





SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

running = True

while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((20, 70, 30))

    pygame.display.flip()

pygame.quit()
