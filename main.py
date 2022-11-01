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


class Card:

    def __init__(self, value, suit, image):
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

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((34, 139, 34))

    pygame.display.flip()

pygame.quit()
