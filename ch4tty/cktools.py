"""
This will hold the tools and utilities of timers and parsers.
"""
import os
import re
import time

#
# ----- Poker related values
#
is_poker_off_cooldown = True
POKER_COOLDOWN_TIME = 900
MAX_NUMBER_5_CARD_PLAYERS = 5
MAX_HAND_SIZE_5_CARD = 5
SUM_MAX_BETS = 250
MAX_BET = 100
# Hands of poker
ROYAL_FLUSH = 10
STRAIGHT_FLUSH = 9
FOUR_OF_A_KIND = 8
FULL_HOUSE = 7
FLUSH = 6
STRAIGHT = 5
THREE_OF_A_KIND = 4
TWO_PAIR = 3
PAIR = 2
HIGH_CARD = 1

DIR_ = os.path.dirname(__file__)
DB_PATH = os.path.join(DIR_, '../docs/kettlebase.db')


def parse_flags(s):
    """
    Parses the flags for the raffle timer and the max number of tickets
    viewers are allowed to enter with.

    :param s:
    :return:
    """
    mt = t = 0
    m = re.match(r'(\S+) (-m )*(?P<max_tick>\d+)*( )*(-t )*(?P<time>\d+)*', s)
    m.groupdict()
    if m['max_tick']:
        mt = m['max_tick']
    if m['time']:
        t = m['time']
    return mt, t


def start_timer():
    return time.time()


def check_timer(the_past):
    return time.time() - the_past


def is_integer(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


def in_range_inclusive(min_, max_, val):
    return min_ <= val <= max_


def out_of_range(min_, max_, val):
    return min_ <= val <= max_
