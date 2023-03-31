from model import Game, Player, Card
from UI import UI

players = [Player('Adrian'), Player('Zach'), Player('Aditya')]
ui = UI()
game = Game(players, ui)


# game.play_game()

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
    print(counts)
    print(values)
    print(suits)

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
            return 7, high_card
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
        for c in counts:
            if counts[c] == 3:
                triples += 1
                high_card = values[x]
            x += 1
        if triples == 1:
            return 3, high_card
        return False

    def two_pair():
        pairs = 0
        high_card = 0
        x = 0
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
        for c in counts:
            if counts[c] == 2:
                pairs += 1
                high_card = list(counts.keys())[x]
            x += 1
        if pairs == 1:
            return 1, high_card
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


card1 = Card(5, 's', 'Five')
card2 = Card(11, 's', 'Jack')
card3 = Card(2, 'c', 'Two')
card4 = Card(7, 's', 'Seven')
card5 = Card(9, 'h', 'Nine')
card6 = Card(9, 'c', 'Nine')
card7 = Card(4, 'h', 'Four')
complete_hand = [card1, card2, card3, card4, card5, card6, card7]
evaluate_hand(complete_hand)
