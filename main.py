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

big_blind = 40
small_blind = 20
max_bet = big_blind
num_opps = 1


class Card(object):
    def __init__(self, name, value, suit):
        self.value = value
        self.suit = suit
        self.name = name

    def __repr__(self):
        return str(self.name) + ' of ' + self.suit

    # @property
    # def image(self):
    #     return pygame.image.load('/Users/adrian_yemin/PycharmProjects/Poker/res/' + str(self.value) + str(self.suit) + '.png')


class Deck(object):
    def __init__(self):
        super().__init__()
        self.cards = []
        suits = ['Diamonds', 'Hearts', 'Spades', 'Clubs']
        values = {'Two': 2,
                  'Three': 3,
                  'Four': 4,
                  'Five': 5,
                  'Six': 6,
                  'Seven': 7,
                  'Eight': 8,
                  'Nine': 9,
                  'Ten': 10,
                  'Jack': 11,
                  'Queen': 12,
                  'King': 13}

        for name in values:
            for suit in suits:
                self.cards.append(Card(name, values[name], suit))
        random.shuffle(self.cards)


class Player:
    def __init__(self, user_cards):
        self.stack = 1000
        self.chipsInPlay = 0
        self.bet = 0
        self.user_cards = user_cards
        self.folded = False


class PlayerDealState:
    def __init__(self, player):
        self.folded = False
        self.hand = hand


deck = Deck()


# print(deck.cards)


def deal_card():
    new_card = deck.cards.pop(0)
    return new_card, deck.cards


def deal_user():
    card1, cards = deal_card()
    card2, cards = deal_card()
    user = [card1, card2]
    return user


def deal_opps():
    opps = []
    for x in range(num_opps):
        card1, cards = deal_card()
        card2, cards = deal_card()
        opps.append([card1, card2])
    return opps


def opponent_list():
    players = []
    for player in range(num_opps):
        players.append(Player(deal_opps()[player]))
    return players


opps = opponent_list()
for hand in range(len(opps)):
    print(opps[hand].user_cards)

community_cards = []


def deal_flop():
    for x in range(3):
        card, cards = deal_card()
        community_cards.append(card)


def deal_table():
    card, cards = deal_card()
    community_cards.append(card)


community_cards.append(deal_flop())
# print('Cards After Flop: ' + str(community_cards))
community_cards.append(deal_table())
# print('Cards After Turn: ' + str(community_cards))
community_cards.append(deal_table())


# print('Cards After River: ' + str(community_cards))


#     def round_betting(self):
#         num_players = len(self.players)
#         dealer = 0
#         current_better = dealer + 1
#         num_called = 0
#         while num_players != num_called:
#             if self.players[current_better].folded is False:

class Game:
    def __init__(self):
        self.deck = Deck()
        self.opps = opponent_list()
        self.user = Player(deal_user())

# running = True
# while running:
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     screen.fill((34, 139, 34))
#
#     pygame.display.flip()
#
# pygame.quit()
