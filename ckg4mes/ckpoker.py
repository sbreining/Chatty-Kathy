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


class FiveCardDraw(Thread):
    """
    Handles the game of 5 card draw in poker. Will need a hierarchy of winning
    hands.
    """
    def __init__(self, bot):
        super().__init__()

        self.bot = bot

        # Key: 'viewer name', Value: dictionary {}
        self.__players = {}

        self.__is_game_running = False
        self.__player_1 = self.__player_2 = self.__player_3 = ''
        self.__player_4 = self.__player_5 = ''

        self.__deck = []  # This holds the deck of cards.
        self.__reset_the_deck__()

    def determine_winner(self):
        # TODO
        pass

    def deal_the_cards(self):
        """
        Step 1: Remove random card from the deck and put it in first players hand.
        Step 2: Remove second random card and give it to the next player.
        Step 3: Repeat until max players each have one card.
        Step 4: Repeat those steps until each player has 5 cards.
        :return:
        """
        while len(self.__players[self.__player_1]['hand']) < cktools.MAX_HAND_SIZE_5_CARD:
            for viewer in self.__players:
                pseudo_shuffled_card = random.choice(self.__deck)
                viewer['hand'].append(pseudo_shuffled_card)

    def second_deal(self):
        """
        Step 1: Deal off the top 5 cards minus the first players tossed cards.
        Step 2: Repeat until all players hands are filled again.
        :return:
        """
        # TODO
        pass

    def join_the_game(self, viewer, bet):
        """
        Have the viewers enter the game. This will check to see if the game
        is full or not.

        :param viewer:
        :param bet:
        :return:
        """
        if self.__is_game_running:
            if len(self.__players) < cktools.MAX_NUMBER_5_CARD_PLAYERS:
                self.__players[viewer] = {'bet': bet, 'hand': [], 'are_tossed': False, 'is_2nd_made': False}
                if self.__player_1 == '':
                    self.__player_1 = viewer
                elif self.__player_2 == '':
                    self.__player_2 = viewer
                elif self.__player_3 == '':
                    self.__player_3 = viewer
                elif self.__player_4 == '':
                    self.__player_4 = viewer
                elif self.__player_5 == '':
                    self.__player_5 = viewer
            else:
                self.bot.send_message("The game is full.")
            pass

    def place_bet(self, viewer, bet):
        if 0 == bet:
            self.__pass_bet__(viewer)

    def is_player_in_game(self, viewer):
        return viewer in self.__players.keys()

    def run(self):
        self.__is_game_running = True
        while True:
            if cktools.MAX_NUMBER_5_CARD_PLAYERS == len(self.__players):
                break
        self.__take_tickets__()
        self.__run_game__()
        self.__reward_winner__()  # This should be the last thing called.
        pass

    def is_running(self):
        return self.__is_game_running

    def __reset_the_deck__(self):
        # Is this how I want to hold the deck of cards?
        self.__deck = [
            '1S', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', '11S', '12S',
            '1H', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', '11H', '12H',
            '1C', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', '11C', '12C',
            '1D', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', '11D', '12D'
                      ]

    def __reset_game__(self):
        # Reset the players hands
        self.__player_1 = self.__player_2 = self.__player_3 = ''
        self.__player_4 = self.__player_5 = ''
        self.__reset_the_deck__()

    def __take_tickets__(self):
        # TODO
        pass

    def __reward_winner__(self):
        # TODO
        pass

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
        pass

    # TODO: Need an order of betting around the table. Can't just let everyone bet at the same time.
