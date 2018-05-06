"""
This class will handle raffles.
"""
import time
from threading import Thread


class RaffleMngr(Thread):
    def __init__(self, c_id, cl_id, chan):
        super().__init__()
        self._floating_points = []
        self._time_limit = 0
        self._max_tickets = 0
        self.channel_id = c_id
        self.client_id = cl_id
        self.channel = chan
        self.cmd = []

    def set_options(self, args, cmd):
        self._max_tickets = args['mt']
        self._time_limit = args['time']*60
        self.cmd = cmd

    # TODO: Finish the run loop. Need to implement helper functions.
    def run(self):
        self.cmd[1].privmsg(self.channel, "Raffle has been started")
        counter = 0
        while counter < self._time_limit:
            time.sleep(1)
            if counter == self._time_limit-60:
                self.cmd[1].privmsg(self.channel, "60 seconds left!")
        self.cmd[1].privmsg(self.channel, "Raffle is closed!")
