"""
This will hold the tools and utilities of timers and parsers.
"""
import os
import re

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


def is_integer(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


def out_of_range(min_, max_, val):
    return min_ <= val <= max_
