import random
from enum import Enum
import pygame


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
        suits = ['d', 'h', 's', 'c']
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
            print('New Deal!')


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
            card1 = self.deck.pop()
            card2 = self.deck.pop()
            cards = [card1, card2]
            self.player_deal_states.append(PlayerDealState(player, cards))

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
        print('Next Round of Betting!\n')

    def play_post_flop(self, bet_round):
        if self.deal_is_over() is True:
            return
        bet_round.execute_bet()
        print('Next Round of Betting!\n')

    def play_deal(self):
        bet_round = BettingRound(self.player_deal_states, self.dealer, self)
        self.play_pre_flop(bet_round)
        bet_round.play_flop()
        for x in range(2):
            self.play_post_flop(bet_round)
            bet_round.play_table()
        bet_round.execute_bet()
        for player in range(len(self.player_deal_states)):
            self.player_deal_states[player].folded = False


class BettingRound:
    def __init__(self, player_deal_states, dealer_index, deal):
        self.dealer_index = dealer_index
        self.deal = deal
        self.community_cards = []
        self.current_better_index = (dealer_index + 1) % (len(player_deal_states))
        self.player_round_states = []
        for player in player_deal_states:
            self.player_round_states.append(PlayerRoundState(player, self))
        self.highest_bet = 0

    def print_current_state(self):
        for player in self.player_round_states:
            print('Name: ' + player.player_deal_state.player.name)
            print('   Stack: ' + str(player.player_deal_state.player.stack))
            print('   Folded: ' + str(player.player_deal_state.folded))
            if player.player_deal_state.folded is False:
                print('   Current Bet: ' + str(player.total_bet))
        print('Pot: ' + str(self.deal.pot))
        print('Highest Bet: ' + str(self.highest_bet) + '\n')
        if len(self.community_cards) > 0:
            print('Community Cards: ')
            for x in range(len(self.community_cards)):
                print(self.community_cards[x])

    def play_flop(self):
        for x in range(3):
            self.community_cards.append(self.deal.deck.pop())

    def play_table(self):
        self.community_cards.append(self.deal.deck.pop())

    def get_highest_bet(self):
        return self.highest_bet

    def get_player_round_states(self):
        return self.player_round_states

    def round_is_over(self):
        length = len(self.player_round_states)
        remaining_players = length
        for player in self.player_round_states:
            if player.get_last_action() == Action.Fold:
                remaining_players -= 1
        if remaining_players == 1:
            return True
        for player in self.player_round_states:
            if player.get_last_action() == Action.Fold:
                continue
            if player.get_bet() != self.highest_bet:
                return False
        if self.highest_bet != 0:
            return True
        for player in range(len(self.player_round_states)):
            if self.player_round_states[player].get_last_action() is None:
                return False
        return True

    def get_input(self):
        self.print_current_state()
        name = self.player_round_states[self.current_better_index].player_deal_state.player.name
        action = Action.from_input(input('Action for ' + name + ': '))
        amount = None
        if action == Action.Raise:
            amount = int(input('How Much?: '))
        return action, amount

    def execute_bet(self):
        while self.round_is_over() is False:
            cur_player_round_state = self.player_round_states[self.current_better_index]
            if cur_player_round_state.player_deal_state.folded is True:
                self.current_better_index = (self.current_better_index + 1) % len(self.player_round_states)
                print('SKIPPED FOLDED PLAYER')
                continue
            action, amount = self.get_input()
            if action == Action.Raise:
                cur_player_round_state.do_raise(amount)
            if action == Action.Call:
                cur_player_round_state.call()
            if action == Action.Fold:
                cur_player_round_state.fold()
            self.current_better_index = (self.current_better_index + 1) % len(self.player_round_states)
        self.highest_bet = 0
        for player in self.player_round_states:
            player.total_bet = 0
            player.last_action = None

    def create_player_hand(self, player):
        complete_player_hand = []
        for card in range(2):
            complete_player_hand.append(player.player_deal_state.get_hand[card])
        for card in range(len(self.community_cards)):
            complete_player_hand.append(self.community_cards[card])
        return complete_player_hand


class Player:
    def __init__(self, name):
        self.stack = 2000
        self.name = name


class PlayerDealState:
    def __init__(self, player, hand):
        self.folded = False
        self.player = player
        self.hand = hand

    def fold(self):
        self.folded = True

    def get_fold_state(self):
        return self.folded

    def get_hand(self):
        return self.hand


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
        self.player_deal_state.player.stack -= (self.betting_round.get_highest_bet() - self.total_bet)
        self.total_bet = self.betting_round.get_highest_bet()
        self.betting_round.deal.pot += (self.betting_round.get_highest_bet() - self.total_bet)

    def do_raise(self, amount):
        self.last_action = Action.Raise
        self.total_bet = self.betting_round.get_highest_bet() + amount
        self.player_deal_state.player.stack -= amount
        self.betting_round.highest_bet += amount
        self.betting_round.deal.pot += ((self.betting_round.get_highest_bet() + amount) - self.total_bet)

    def evaluate_hand(complete_player_hand):

        high_card = 1
        pair = 2
        two_pair = 3
        three_of_a_kind = 4
        straight = 5
        flush = 6
        full_house = 7
        four_of_a_kind = 8
        straight_flush = 9
        royal_flush = 10

        complete_player_hand.sort(key=lambda x: x[0], reverse=True)

        counts = [complete_player_hand.count(card) for card in complete_player_hand]

        flush = all(card[1] == complete_player_hand[0][1] for card in complete_player_hand)

        straight = all(complete_player_hand[i][0] == complete_player_hand[i + 1][0] - 1 for i in range(len(complete_player_hand) - 1))

        four_of_a_kind = 4 in counts

        three_of_a_kind = 3 in counts


        pairs = [i for i in counts if i == 2]

        if straight and flush:
            return straight_flush
        elif four_of_a_kind:
            return four_of_a_kind
        elif three_of_a_kind and len(pairs) == 1:
            return full_house
        elif flush:
            return flush
        elif straight:
            return straight
        elif three_of_a_kind:
            return three_of_a_kind
        elif len(pairs) == 2:
            return two_pair
        elif len(pairs) == 1:
            return pair
        else:
            return high_card
