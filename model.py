import random


class Card(object):
    def __init__(self, value, suit, name):
        self.value = value
        self.suit = suit
        self.name = name

    def __repr__(self):
        return self.name + ' of ' + str(self.suit)


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
    def __init__(self, players, ui):
        self.players = players
        self.ui = ui

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

        def create_player_hand(player):
            complete_player_hand = []
            for card in range(2):
                complete_player_hand.append(player.get_hand[card])
            for card in range(len(bet_round.community_cards)):
                complete_player_hand.append(bet_round.community_cards[card])
            return complete_player_hand

        def evaluate_hand(complete_player_hand):
            complete_player_hand = sorted(complete_player_hand, key=lambda x: x.value, reverse=False)
            counts = {}
            values = []
            suits = []
            for card in complete_player_hand:
                values.append(card.value)
                suits.append(card.suit)
            for c in range(len(complete_player_hand)):
                counts[values[c]] = values.count(values[c])
            single_values = list(counts.keys())
            print(counts)
            print(values)
            print(suits)
            print(single_values)

            def straight_flush():
                for a in range(3):
                    order_count = 0
                    suit_count = 0
                    high_card = values[0]
                    for c in range(a, a + 4):
                        if values[c] == values[c + 1] - 1:
                            order_count += 1
                            high_card = values[c + 1]
                        if suits[c] == suits[c + 1]:
                            suit_count += 1
                    if order_count == 4 and suit_count == 4:
                        return 8, high_card
                return False

            def four_kind():
                quads = 0
                high_card = 0
                x = 0
                for c in counts:
                    if counts[c] == 4:
                        quads += 1
                        high_card = list(counts.keys())[x]
                    x += 1
                if quads == 1:
                    if max(single_values) == high_card:
                        kicker = single_values[len(single_values) - 2]
                    else:
                        kicker = max(single_values)
                    return 7, high_card, kicker
                return False

            def full_house():
                triples = 0
                high_card = 0
                x = 0
                for c in counts:
                    if counts[c] == 3:
                        triples += 1
                        high_card = list(counts.keys())[x]
                        print(high_card)
                    x += 1
                if triples == 1:
                    for c in counts:
                        if counts[c] == 2:
                            return 6, high_card
                return False

            def flush():
                high_card = values[0]
                for suit in set(suits):
                    if suits.count(suit) >= 5:
                        for card in range(len(values) - 1):
                            if values[card + 1] > values[card] and suits[card + 1] == suit:
                                high_card = values[card + 1]
                        return 5, high_card
                return False

            def straight():
                high_card = 0
                for card in range(3):
                    order_count = 0
                    for c in range(card + 4):
                        if order_count == 4:
                            return 4, high_card
                        if values[c] == values[c + 1] - 1:
                            order_count += 1
                            high_card = values[c + 1]
                return False

            def three_kind():
                triples = 0
                high_card = 0
                x = 0
                kicker = [-1, 0]
                for c in counts:
                    if counts[c] == 3:
                        triples += 1
                        high_card = values[x]
                    x += 1
                if triples == 1:
                    for c in range(len(single_values)):
                        if single_values[c] != high_card and single_values[c] > min(kicker):
                            kicker[kicker.index(min(kicker))] = single_values[c]
                    return 3, high_card, kicker
                return False

            def two_pair():
                pairs = 0
                high_card = 0
                x = 0
                kicker = 0
                for c in counts:
                    if counts[c] == 2:
                        pairs += 1
                        high_card = list(counts.keys())[x]
                    x += 1
                if pairs >= 2:
                    return 2, high_card
                return False

            def pair():
                pairs = 0
                high_card = 0
                x = 0
                kicker = [-2, -1, 0]
                for c in counts:
                    if counts[c] == 2:
                        pairs += 1
                        high_card = list(counts.keys())[x]
                    x += 1
                if pairs == 1:
                    for c in range(len(single_values)):
                        if single_values[c] != high_card and single_values[c] > min(kicker):
                            kicker[kicker.index(min(kicker))] = single_values[c]
                    return 1, high_card, kicker
                return False

            if straight_flush():
                print(straight_flush())
                return straight_flush()

            if four_kind():
                print(four_kind())
                return four_kind()

            if full_house():
                print(full_house())
                return full_house()

            if flush():
                print(flush())
                return flush()

            if straight():
                print(straight())
                return straight()

            if three_kind():
                print(three_kind())
                return three_kind()

            if two_pair():
                print(two_pair())
                return two_pair()

            if pair():
                print(pair())
                return pair()

            return 0, max(complete_player_hand)

        winner_index = 0
        second_winner_index = None
        for player in range(len(self.game.player_deal_states - 1)):
            x = self.player_deal_states[player]
            y = self.player_deal_states[player + 1]
            if evaluate_hand(create_player_hand(y)) > evaluate_hand(create_player_hand(x)):
                winner_index = player + 1
                second_winner_index = None
            elif evaluate_hand(create_player_hand(y)) == evaluate_hand(create_player_hand(x)):
                winner_index = player + 1
                second_winner_index = player
        if second_winner_index is None:
            self.player_deal_states[winner_index].player.stack += self.pot
        else:
            self.player_deal_states[winner_index].player.stack += (self.pot/2)
            self.player_deal_states[second_winner_index].player.stack += (self.pot / 2)


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
        # self.deal.game.ui.render(self)
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
