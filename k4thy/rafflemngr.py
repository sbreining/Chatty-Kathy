"""
This class will handle raffles.
"""
import random
import time
from threading import Thread


class RaffleMngr(Thread):
    def __init__(self, b, bins):
        super().__init__()
        self._entered_users = {}
        self._time_limit = 0
        self._max_tickets = 0
        self.bot = b
        self.cmd = []
        self.open = False
        self.bucket = bins
        self._is_closed_manually = False
        self._is_thread_stopped = False
        self._winner = ""
        self._is_winner_present = False

    def set_options(self, cmd, m, t):
        self._reset_raffle()
        self._max_tickets = int(m)
        self._time_limit = int(t)*60
        self.cmd = cmd

    def run(self):
        self.open = True
        self.bot.send_message("THE RAFFLE IS NOW OPEN!")
        counter = 0

        while not self._is_thread_stopped:
            while counter < self._time_limit or self._time_limit == 0:
                time.sleep(1)
                if counter == self._time_limit-60:
                    self.bot.send_message("THE RAFFLE HAS 60 SECONDS LEFT!")
                counter += 1
                if self._is_closed_manually:
                    break
            self.bot.send_message("RAFFLE IS NOW CLOSED!")
            self.open = False
            self._is_thread_stopped = True

        self.pick_first_winner()

    def submit_tickets(self, viewer, tickets):
        if self.open:
            if tickets > self._max_tickets:
                self.bot.send_message("You have tried to submit too many tickets, \
                                       please submit at most " + str(self._max_tickets),
                                      True, viewer)
            else:
                if viewer in self._entered_users:
                    self._entered_users[viewer] = tickets
                else:
                    self._entered_users[viewer].append(tickets)
        else:
            self.bot.send_message("There is no raffle open right now")

    def pick_first_winner(self):
        self.take_user_tickets()
        self.pick_winner()

    def redraw_winner(self):
        del self._entered_users[self._winner]
        self.pick_winner()

    def pick_winner(self):
        tickets = self._entered_users.values()
        weights = [float(i)/sum(tickets) for i in tickets]
        self._winner = random.choices(self._entered_users.keys(), weights=weights, k=1)
        self.bot.send_message("And the winner is: " + self._winner + "!!! \n You have \
                               60 seconds to respond by typing into chat.")
        counter = 0
        while counter < 60:
            if self._is_winner_present:
                self.bot.send_message(self._winner + " responded! Congrats again!")
                break
            time.sleep(1)
            counter += 1
        if not self._is_winner_present:
            self.bot.send_message("No response from winner.")

    def take_user_tickets(self):
        for key, value in self._entered_users.items():
            self.bucket.subtract_points(key, value)

    def _reset_raffle(self):
        self._entered_users = []
        self._users_tickets = []

    def interrupt(self):
        self._is_thread_stopped = True
        self._reset_raffle()

    def manual_close_raffle(self):
        self._is_closed_manually = True

    def get_winner(self):
        return self._winner

    def winner_found(self):
        self._is_winner_present = True
