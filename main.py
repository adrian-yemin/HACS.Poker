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

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

class Card(pygame.sprite.Sprite):
    def __init__(self, value, suit):
        super(Card, self).__init__()
        self.value = value
        self.suit = suit

    @property
    def image(self):
        return pygame.image.load('/Users/aditya_weling/PycharmProjects/HACS.Poker/res' + str(self.value) + str(self.suit) + '.png')

    def print_self(self):
        print(self.value, self.suit, self.image)


suit = ['h', 's', 'c', 'd']

class Deck:
    def __init__(self):
        self.cards = []
        for c in range(len(suit)):
            color = suit[c]
            for value in range(1, 14):
                self.cards.append(Card(value, color))
        random.shuffle(self.cards)

    def print_deck(self):
        for x in range(len(self.cards)):
            print(self.cards[x].print_self())


card1 = Card(5, suit[0])

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((34, 139, 34))

    screen.blit(card1.image, (SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2))

    pygame.display.flip()

pygame.quit()
