"""
This will hold the tools and utilities of timers and parsers.
"""
import re

is_poker_on_cooldown = False

MAX_NUMBER_5_CARD_PLAYERS = 5
MAX_HAND_SIZE_5_CARD = 5


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
    pass


def end_timer():
    pass


# TODO: Figure out the number zero. Returning it is true, but will eval false.
def is_integer(n):
    try:
        return int(n)
    except ValueError:
        return False


def out_of_range(min_, max_, val):
    return min_ <= val <= max_
