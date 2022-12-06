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
from enum import Enum

pygame.mixer.init()
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


class Card(object):
    def __init__(self, name, value, suit):
        self.value = value
        self.suit = suit
        self.name = name

    def __repr__(self):
        return str(self.name) + ' of ' + self.suit


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

    def pop(self):
        return self.cards.pop()


class Action:
    Call = 1
    Raise = 2
    Fold = 3

    @staticmethod
    def from_input(user_input):
        if user_input == 'r':
            return Action.Raise
        if user_input == 'c':
            return Action.Call
        if user_input == 'f':
            return Action.Fold
        return None


class Game:
    def __init__(self, players):
        self.players = players

    def is_over(self):
        length = len(self.players)
        remaining_players = length
        for player in self.players:
            if player.stack <= 0:
                remaining_players -= 1
        if remaining_players > 1:
            return False
        return True

    def play_game(self):
        deal = Deal(self, self.players)
        while self.is_over() is False:
            deal.play_deal()


class Deal:
    def __init__(self, game, players):
        self.pot = 0
        self.dealer = 0
        self.big_blind = 20
        self.small_blind = 40
        self.game = game
        self.player_deal_states = []
        self.pot = 0
        self.deck = Deck()
        for player in players:
            self.player_deal_states.append(PlayerDealState(player))

    def deal_is_over(self):
        remaining_players = len(self.player_deal_states)
        for player in self.player_deal_states:
            if player.get_fold_state() is True:
                remaining_players -= 1
        if remaining_players > 1:
            return False
        return True

    def play_pre_flop(self, bet_round):
        if self.deal_is_over() is True:
            return
        bet_round.execute_bet()
        for x in range(3):
            bet_round.community_cards.append(self.deck.pop())

    def play_post_flop(self, bet_round):
        if self.deal_is_over() is True:
            return
        bet_round.execute_bet()
        bet_round.community_cards.append(self.deck.pop())

    def play_deal(self):
        bet_round = BettingRound(self.player_deal_states, self.dealer, self)
        self.play_pre_flop(bet_round)
        for x in range(2):
            self.play_post_flop(bet_round)
        bet_round.execute_bet()


class BettingRound:
    def __init__(self, player_deal_states, dealer_index, deal):
        self.highest_bet = 0
        self.dealer_index = dealer_index
        self.deal = deal
        self.community_cards = []
        self.current_better_index = (dealer_index + 1) % (len(player_deal_states))
        self.player_round_states = []
        for player in player_deal_states:
            self.player_round_states.append(PlayerRoundState(player, self))

    def print_current_state(self):
        for player in self.player_round_states:
            print('Name: ' + player.player_deal_state.player.name)
            print('   Stack: ' + str(player.player_deal_state.player.stack))
            print('   Folded: ' + str(player.player_deal_state.folded))
            if player.player_deal_state.folded is False:
                print('   Current Bet: ' + str(player.total_bet))
        print('Pot: ' + str(self.deal.pot))
        print('Highest Bet: ' + str(self.highest_bet))

    def get_highest_bet(self):
        return self.highest_bet

    def get_player_round_states(self):
        return self.player_round_states

    def round_is_over(self):
        bet = self.player_round_states[0].get_bet()
        length = len(self.player_round_states)
        remaining_players = length
        for player in self.player_round_states:
            if player.get_last_action() == Action.Fold:
                remaining_players -= 1
        if remaining_players == 1:
            return True
        for player in self.player_round_states:
            if player.get_last_action() == Action.Fold:
                pass
            if player.get_bet() != bet:
                return False
        if bet != 0:
            return True
        if self.player_round_states[length - 1].get_last_action() is None:
            return False
        return True

    def get_input(self):
        self.print_current_state()
        name = self.player_round_states[self.current_better_index].player_deal_state.player.name
        action = Action.from_input(input('Action for ' + name + ': '))
        amount = None
        if action == Action.Raise:
            amount = int(input('How Much?'))
        return action, amount

    def execute_bet(self):
        while self.round_is_over() is False:
            action, amount = self.get_input()
            cur_player_round_state = self.player_round_states[self.current_better_index]
            if action == Action.Raise:
                cur_player_round_state.do_raise(amount)
                self.highest_bet += amount
            if action == Action.Call:
                cur_player_round_state.call()
            if action == Action.Fold:
                cur_player_round_state.fold()
            self.current_better_index = (self.current_better_index + 1) % len(self.player_round_states)


class Player:
    def __init__(self, name):
        self.stack = 2000
        self.name = name


class PlayerDealState:
    def __init__(self, player):
        self.folded = False
        self.player = player

    def fold(self):
        self.folded = True

    def get_fold_state(self):
        return self.folded


class PlayerRoundState:
    def __init__(self, player_deal_state, betting_round):
        self.total_bet = 0
        self.player_deal_state = player_deal_state
        self.last_action = None
        self.betting_round = betting_round

    def get_last_action(self):
        return self.last_action

    def get_bet(self):
        return self.total_bet

    def fold(self):
        self.last_action = Action.Fold
        self.player_deal_state.fold()

    def call(self):
        self.last_action = Action.Call
        self.total_bet = self.betting_round.get_highest_bet()


    def do_raise(self, amount):
        self.last_action = Action.Raise
        self.total_bet = self.betting_round.get_highest_bet() + amount
        self.player_deal_state.player.stack -= amount
        self.betting_round.highest_bet += amount





# def deal_card():
#     new_card = deck.cards.pop(0)
#     return new_card, deck.cards
#
#
# def deal_user():
#     card1, cards = deal_card()
#     card2, cards = deal_card()
#     user = [card1, card2]
#     return user
#
#
# def deal_opps():
#     opps = []
#     for x in range(num_opps):
#         card1, cards = deal_card()
#         card2, cards = deal_card()
#         opps.append([card1, card2])
#     return opps
#
#
# def opponent_list():
#     players = []
#     for player in range(num_opps):
#         players.append(Player(deal_opps()[player]))
#     return players
#
#
# opps = opponent_list()
# for hand in range(len(opps)):
#     print(opps[hand].user_cards)
#
# community_cards = []
#
#
# def deal_flop():
#     for x in range(3):
#         card, cards = deal_card()
#         community_cards.append(card)
#
#
# def deal_table():
#     card, cards = deal_card()
#     community_cards.append(card)
#
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
