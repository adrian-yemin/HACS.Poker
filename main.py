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
    def __init__(self, value, suit, image):
        super(Card, self).__init__()
        self.value = value
        self.suit = suit
        self.image = image


    def printSelf(self):
        print(self.value, self.suit, self.image)


suit = ['h', 's', 'c', 'd']

deck = []
for c in range(len(suit)):
    color = suit[c]
    for value in range(1, 14):
        deck.append(Card(value, color, str(value) + str(color) + '.png'))

for x in range(len(deck)):
    print(deck[x].printSelf())



class Player1:
    def __init__(self, name, image):
        self.name = name
        self.image = image
        self.stack = 1000
        self.chipsInPlay = 0
        self.turn = False
        self.a = 1

    def turn(self, c1, c2):
        Player1.turn = True

class Button:
    def __init__(self, x, y):
        self.x = x
        self.y = y

running = True

while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((34, 139, 34))

    pygame.display.flip()

pygame.quit()
