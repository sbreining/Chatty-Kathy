"""
This file will contain 5 card draw poker. The users will be whispered a hand
of cards. They will use commands to say which cards they want to replace and
be dealt new cards. All the while this involves stages of betting. They will
lose and gain points based who wins the pot. There is potential for split pots
if two or more players have equal hands.
"""

from threading import Thread


# Name 5 card draw in case I find a way to implement more types of poker
class FiveCardDraw(Thread):
    """
    Handles the game of 5 card draw in poker. Will need a hierarchy of winning
    hands.
    """
    def __init__(self, bot):
        super().__init__()

        self.bot = bot

        self.__is_game_running = False
        self.__gamers = {}  # This will hold viewers and their gambled tickets.
        self.__hands = {}  # This holds viewer and their current hand?
        self.__deck = []  # This holds the deck of cards?

    def deal_the_cards(self):
        pass

    def reset_the_deck(self):
        # Is this how I want to hold the deck of cards?
        self.__deck = [
            '1S', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', '11S', '12S',
            '1H', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', '11H', '12H',
            '1C', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', '11C', '12C',
            '1D', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', '11D', '12D'
                      ]

    def second_deal(self):
        pass

    def determine_winner(self):
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
            if len(self.__gamers) == 5:
                self.__gamers[viewer] = bet
            else:
                self.bot.send_message("The game is full.")
            pass

    def run(self):
        pass
