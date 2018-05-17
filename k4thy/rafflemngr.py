"""
This class will handle raffles.
"""
import time
from threading import Thread


class RaffleMngr(Thread):
    def __init__(self, b):
        super().__init__()
        self._floating_points = []
        self._time_limit = 0
        self._max_tickets = 0
        self.bot = b
        self.cmd = []

    def set_options(self, cmd, m, t):
        self._max_tickets = int(m)
        self._time_limit = int(t)*60
        self.cmd = cmd

    # TODO: Finish the run loop. Need to implement helper functions.
    def run(self):
        self.bot.send_message("THE RAFFLE IS NOW OPEN!")
        counter = 0
        while counter < self._time_limit:
            time.sleep(1)
            if counter == self._time_limit-60:
                self.bot.send_message("THE RAFFLE HAS 60 SECONDS LEFT!")
            counter += 1
        self.bot.send_message("RAFFLE IS NOW CLOSED!")
