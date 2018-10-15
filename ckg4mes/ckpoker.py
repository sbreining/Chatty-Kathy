"""
This file will  contain 5 card draw poker. The  users will be whispered a hand
of cards. They  will use commands to say which cards they  want to replace and
be dealt  new cards. All the while this involves  stages of betting. They will
lose and gain points based who wins the pot. There is potential for split pots
if two  or more players  have equal hands. I  will require a minimum number of
points to join poker which will be the combined max bets.
"""


# Name 5 card draw in case I find a way to implement more types of poker
import random
from ch4tty import cktools
from threading import Thread

from ckg4mes.ckpokerplayer import PokerPlayer


class FiveCardDraw(Thread):
    """
    Handles the game of 5 card draw in poker. Will need a hierarchy of winning
    hands.
    """
    def __init__(self, bot, bucket):
        super().__init__()

        self.bot = bot
        self.bucket = bucket

        self.__players__ = []  # Max number of players is 5.
        self.__players_in_game__ = 0
        self.__all_players_bet__ = False

        self.__is_game_running__ = False

        self.__deck__ = []  # This holds the deck of cards.
        self.__current_pot__ = 0

        self.__cooldown_count__ = 0

    def determine_winner(self):
        winning_hand = self.__players__[0].get_player_hand()
        for i in range(5):
            winning_hand = self.compare_hands(
                winning_hand,
                self.__players__[i].get_player_hande()
            )
        pass

    def deal_the_cards(self):
        """
        Step 1: Remove random card from the deck and put it in first players hand.
        Step 2: Remove second random card and give it to the next player.
        Step 3: Repeat until max players each have one card.
        Step 4: Repeat those steps until each player has 5 cards.
        :return:
        """
        while len(self.__players__[0].get_hand_size()) < cktools.MAX_HAND_SIZE_5_CARD:
            for player in self.__players__:
                player.add_card_to_hand(self.__deck__.pop())

    def second_deal(self):
        """
        Step 1: Deal off the top 5 cards minus the first players tossed cards.
        Step 2: Repeat until all players hands are filled again.
        :return:
        """
        # TODO
        pass

    def join_the_game(self, viewer):
        """
        Have the viewers enter the game. This will check to see if the game
        is full or not.

        :param viewer:
        :return:
        """
        if self.__is_game_running__:
            if len(self.__players__) < cktools.MAX_NUMBER_5_CARD_PLAYERS:
                self.__players__[self.__players_in_game__] = PokerPlayer(viewer)
                self.__players_in_game__ += 1
            else:
                self.bot.send_message("The game is full.")

    def place_bet(self, viewer, bet):
        # There is more to this condition. There must be no existing bet.
        if 0 == bet and 0 == self.__current_pot__:
            self.__pass_bet__(viewer)

    def is_player_in_game(self, viewer):
        list_of_players = []
        for player in self.__players__:
            list_of_players.append(player.get_player_name())
        return viewer in list_of_players

    def run(self):
        self.__cooldown_count__ = 0
        self.__is_game_running__ = True
        self.__reset_the_deck__()
        random.shuffle(self.__deck__)

        while True:
            if cktools.MAX_NUMBER_5_CARD_PLAYERS == len(self.__players__):
                break

        cktools.is_poker_off_cooldown = False

        self.__run_game__()

    def is_running(self):
        return self.__is_game_running__

    def __reset_the_deck__(self):
        # Is this how I want to hold the deck of cards?
        self.__deck__ = [
            '1S', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', '11S', '12S', '13S',
            '1H', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', '11H', '12H', '13H',
            '1C', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', '11C', '12C', '13C',
            '1D', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', '11D', '12D', '13D'
        ]

    def __reset_game__(self):
        # Reset the players hands
        self.__players__ = []
        self.__current_pot__ = 0
        self.__players_in_game__ = 0
        self.__reset_the_deck__()

    def __reward_winner__(self):
        prize_pool = 0
        for player in self.__players__:
            bet = player.get_bet()
            self.bucket.subtract_points(player.get_player_name(), bet)
            prize_pool += bet
        self.bucket.add_points(self.determine_winner(), prize_pool)

        self.__reset_game__()
        self.__cooldown_count__ = cktools.start_timer()

    def __pass_bet__(self, viewer):
        # TODO
        pass

    def __run_game__(self):
        # TODO
        """
        This will control the flow of the game. Wait for certain players to bet
        and only proceed with the second dealing of cards once appropriate, and
        then further call for a winner to be picked and so on.
        :return:
        """
        self.__first_round_betting__()
        self.__reward_winner__()  # The last thing to be called.

    def get_cooldown_start(self):
        return self.__cooldown_count__

    def compare_hands(self, hand1, hand2):
        if hand1 > hand2:
            return hand1
        return hand2

    def __first_round_betting__(self):
        # TODO Utilize recursion to make sure all players have bet
        for player in self.__players__:
            while True:
                if player.get_has_bet():
                    break

        if not self.__all_players_bet__:
            self.__first_round_betting__()

    # TODO: Need an order of betting around the table. Can't just let everyone bet at the same time.
