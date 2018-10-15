"""

"""


class PokerPlayer:
    """
    Utilized by the game of five card draw. Holds onto the players, and their
    contents. Like their hand, the amount they've bet.
    """
    def __init__(self, name):
        self.name = name
        self.bet = 50
        self.hand = []
        self.tossed = False
        self.has_bet = False

    def get_player_name(self):
        return self.name

    def get_player_bet(self):
        return self.bet

    def get_hand_size(self):
        return len(self.hand)

    def get_player_hand(self):
        return self.hand

    def get_has_bet(self):
        return self.has_bet

    def add_card_to_hand(self, card):
        self.hand.append(card)

    def add_to_bet(self, amount):
        self.bet += amount
