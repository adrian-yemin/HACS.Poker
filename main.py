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


class Dealer:
    def __init__(self):
        self.self = self
        self.CardsPerPlayer = 2


def deal(numhands):
    n = 2
    hands = []
    for i in range(0, numhands):
        ncards = []
        for j in range(0, n):
            ncards.append(deck.pop())
        hands.append(ncards)
    return hands


class Card(pygame.sprite.Sprite):
    def __init__(self, value, suit, image):
        super(Card, self).__init__()
        self.value = value
        self.suit = suit
        self.image = image

    @property
    def image(self):
        return pygame.image.load(
            '/Users/adrian_yemin/PycharmProjects/Poker/res/' + str(self.value) + str(self.suit) + '.png')

    def print_self(self):
        print(self.value, self.suit, self.image)


suit = ['h', 's', 'c', 'd']

deck = []
for c in range(len(suit)):
    color = suit[c]
    for value in range(1, 14):
        deck.append(Card(value, color, str(value) + str(color) + '.png'))

card1 = Card(5, suit[0])


class Player:
    def __init__(self, name, image):
        self.name = name
        self.image = image
        self.stack = 1000
        self.chipsInPlay = 0
        self.turn = False
        self.inPlay = False

    def turn(self, number, hands):
        player1, player2, player3, player4, player4, player5, player6 = Player
        player1.turn = True
        for i in range(0, ncards):
            if (ncards[0].suit == ncards[1].suit)


class Button:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class GameStateManager:
    def __init__(self, pot, playerList):
        self.self = self
        self.pot = pot
        self.playerList = []


for i in range(0, 6)
    playerList.append


    def check(self, Player):


    def fold(self, Player):


    def bet(self, Player):


    print(deal(6))

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
