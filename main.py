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

suit = ['h', 's', 'c', 'd']


class Card(pygame.sprite.Sprite):
    def __init__(self, value, suit):
        super(Card, self).__init__()
        self.value = value
        self.suit = suit


    @property
    def image(self):
        return pygame.image.load('/Users/adrian_yemin/PycharmProjects/Poker/res/' + str(self.value) + str(self.suit) + '.png')

    def print_self(self):
        print(self.value, self.suit, self.image)


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

    screen.blit(card1.image, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    pygame.display.flip()

pygame.quit()
