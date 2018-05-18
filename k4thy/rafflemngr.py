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
        self.open = False
        self.winner = ""

    def set_options(self, cmd, m, t):
        self._max_tickets = int(m)
        self._time_limit = int(t)*60
        self.cmd = cmd

    def run(self):
        self.open = True
        self.bot.send_message("THE RAFFLE IS NOW OPEN!")
        counter = 0
        while counter < self._time_limit:
            time.sleep(1)
            if counter == self._time_limit-60:
                self.bot.send_message("THE RAFFLE HAS 60 SECONDS LEFT!")
            counter += 1
        self.bot.send_message("RAFFLE IS NOW CLOSED!")
        self.open = False
        self.pick_winner()

    def submit_tickets(self, viewer, tickets):
        if self.open:
            if tickets > self._max_tickets:
                self.bot.send_message("You have tried to submit too many tickets, \
                                       please submit at most " + str(self._max_tickets),
                                      True, viewer)
            else:
                self._floating_points.append([viewer, tickets])
        else:
            self.bot.send_message("There is no raffle open right now")

    # TODO: Implement logic to randomly pick a winner based on weights
    def pick_winner(self):
        pass

    # TODO: Implement logic to redraw in the even the winner isn't there.
    def redraw_winner(self):
        pass

    def get_winner(self):
        return self.winner

    # TODO: Take away each users tickets that they submitted. They are not refunded if they lost.
    def take_user_tickets(self):
        pass
