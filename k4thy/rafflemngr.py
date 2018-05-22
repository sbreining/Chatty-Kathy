"""
This class will handle raffles.
"""
import random
import time
from threading import Thread


class RaffleMngr(Thread):
    def __init__(self, b, bins):
        super().__init__()
        self._entered_users = []
        self._users_tickets = []
        self._time_limit = 0
        self._max_tickets = 0
        self._total_tickets_entered = 0
        self.bot = b
        self.cmd = []
        self.open = False
        self.bucket = bins
        self._is_closed_manually = False
        self._thread_is_stopped = False

    def set_options(self, cmd, m, t):
        self._max_tickets = int(m)
        self._time_limit = int(t)*60
        self.cmd = cmd

    def run(self):
        self.open = True
        self.bot.send_message("THE RAFFLE IS NOW OPEN!")
        counter = 0
        while not self._thread_is_stopped:
            while counter < self._time_limit or self._time_limit == 0:
                time.sleep(1)
                if counter == self._time_limit-60:
                    self.bot.send_message("THE RAFFLE HAS 60 SECONDS LEFT!")
                counter += 1
                if self._is_closed_manually:
                    break
            self.bot.send_message("RAFFLE IS NOW CLOSED!")
            self.open = False
            self.pick_winner()
            self._reset_raffle()
            self._thread_is_stopped = True

    # TODO: Need to check if user is already in raffle. Don't want to add the twice.
    def submit_tickets(self, viewer, tickets):
        if self.open:
            if tickets > self._max_tickets:
                self.bot.send_message("You have tried to submit too many tickets, \
                                       please submit at most " + str(self._max_tickets),
                                      True, viewer)
            else:
                self._entered_users.append([viewer, tickets])
                self._users_tickets.append(tickets)
                self._total_tickets_entered += tickets
        else:
            self.bot.send_message("There is no raffle open right now")

    # TODO: Need to listen for winner now, and redraw if no response.
    def pick_winner(self):
        self.take_user_tickets()
        _user_weights = []
        for i in range(0, len(self._users_tickets)):
            _user_weights.append(self._users_tickets[i] / self._total_tickets_entered)
        winner = random.choices(self._entered_users, weights=_user_weights, k=1)
        self.bot.send_message("And the winner is: " + winner + "!!! \n You have \
                               60 seconds to respond by typing into chat.")
        counter = 0
        while counter < 60:
            time.sleep(1)
            counter += 1

        pass

    # TODO: Implement logic to redraw in the event the winner isn't present.
    def redraw_winner(self):
        pass

    def take_user_tickets(self):
        for u in self._entered_users:
            self.bucket.subtract_points(u[0], u[1])
        pass

    def _reset_raffle(self):
        self._entered_users = []
        self._users_tickets = []
        self._total_tickets_entered = 0

    def interrupt(self):
        self._thread_is_stopped = True
        self._reset_raffle()

    def manual_close_raffle(self):
        self._is_closed_manually = True
