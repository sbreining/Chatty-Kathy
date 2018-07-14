"""
This class will handle raffles.
"""
import random
import time
from threading import Thread


class RaffleMngr(Thread):
    """
    Manages raffles created by the streamer, and the streamer only. Viewers enter
    with tickets they've earned by staying in the channel, and the number of
    tickets they enter with affects their chances of winning.
    """
    def __init__(self, b, bins):
        super().__init__()
        self.__entered_users = {}
        self.__time_limit = 0
        self.__max_tickets = 0
        self.__winner = ""

        self.__bot = b
        self.__bucket = bins

        self.__is_open = False
        self.__is_thread_stopped = False
        self.__is_winner_present = False
        self.__is_closed_manually = False

    def set_options(self, m=0, t=0):
        """
        This function sets the raffle options where m is the max number of
        tickets a user can enter, and t is the time limit to enter (0 for manual
        close).

        :param m:
        :param t:
        :return:
        """
        self.__reset_raffle()
        self.__max_tickets = int(m)      # Expected that it is integer in string form
        self.__time_limit = int(t) * 60  # Also expected as integer in string form

    def run(self):
        self.__is_open = True
        self.__bot.send_message("THE RAFFLE IS NOW OPEN!")
        counter = 0

        while not self.__is_thread_stopped:
            while counter < self.__time_limit or self.__time_limit == 0:
                time.sleep(1)
                if counter == self.__time_limit-60:
                    self.__bot.send_message("THE RAFFLE HAS 60 SECONDS LEFT!")
                counter += 1
                if self.__is_closed_manually:
                    break
            self.__bot.send_message("RAFFLE IS NOW CLOSED!")
            self.__is_open = False
            self.__is_thread_stopped = True

        self.__pick_first_winner()

    def submit_tickets(self, viewer, tickets):
        """
        This is how the viewers enter the raffle with the command !ticket ##.
        It'll enter `viewer` into the dictionary with `tickets` as the value.

        :param viewer:
        :param tickets:
        :return:
        """
        if self.__is_open:
            if tickets > self.__max_tickets != 0:
                self.__bot.send_message("You have tried to submit too many tickets, \
                                       please submit at most " + str(self.__max_tickets), viewer)
                return False
            else:
                self.__entered_users[viewer] = tickets
            return True
        else:
            self.__bot.send_message("There is no raffle open right now")
            return False

    def __pick_first_winner(self):
        """
        Selects the first winner once the raffle is either closed manually or
        the timer runs out.

        :return:
        """
        self.take_user_tickets()
        self.__pick_winner()

    def redraw_winner(self):
        """
        If for whatever reason the streamer wants to re-draw the winner, this
        allows them to pick again after removing the previous winner. The
        previous winner does not get their tickets back.

        :return:
        """
        del self.__entered_users[self.__winner]
        self.__pick_winner()

    def __pick_winner(self):
        """
        This selects the winner based on entered viewers and the number of
        tickets they entered with. Utilising the random module, it creates the
        weights of chances to win for each viewer in the dictionary and then
        promptly reports the winner and waits for a response. If the winner
        doesn't speak it up, it notifies the chat room.

        :return:
        """
        tickets = self.__entered_users.values()
        weights = [float(i)/sum(tickets) for i in tickets]
        self.__winner = random.choices(self.__entered_users.keys(), weights=weights, k=1)
        self.__bot.send_message("And the winner is: " + self.__winner + "!!! \n You have \
                               60 seconds to respond by typing into chat.")
        counter = 0
        while counter < 60:
            if self.__is_winner_present:
                self.__bot.send_message(self.__winner + " responded! Congrats again!")
                break
            time.sleep(1)
            counter += 1
        if not self.__is_winner_present:
            self.__bot.send_message("No response from winner.")

    def take_user_tickets(self):
        """
        This removes all the tickets from each user that entered the drawing
        with. The tickets do not come back unless the user adjusted their
        raffle entry to 0 tickets.

        :return:
        """
        for key, value in self.__entered_users.items():
            self.__bucket.subtract_points(key, value)

    def __reset_raffle(self):
        """
        Reset the raffle data for either fresh raffle or new raffle.

        :return:
        """
        self.__entered_users = {}

    def interrupt(self):
        """
        This interrupts the raffle all together. User tickets are not lost,
        and the dictionary is set back to an empty dictionary.

        :return:
        """
        self.__is_thread_stopped = True
        self.__reset_raffle()

    def manual_close_raffle(self):
        """
        Manually close the raffle. This closes it early if a timer was set,
        or closes it if the timer was set to 0 meaning the streamer wanted to
        close the raffle themselves.

        :return:
        """
        self.__is_closed_manually = True

    def get_winner(self):
        """
        Returns the winner of the raffle.

        :return:
        """
        return self.__winner

    def winner_found(self):
        """
        Determines if the winner is present.

        :return:
        """
        self.__is_winner_present = True

    def get_max_tickets(self):
        """
        Returns the max number of tickets a viewer and enter with.

        :return:
        """
        return self.__max_tickets

    def get_raffle_duration(self):
        """
        Returns the duration of the raffle. NOT TIME REMAINING

        :return:
        """
        return self.__time_limit

    def get_viewers_submitted_tickets(self, name):
        """
        Returns the viewers current tickets entered into the drawing

        :param name:
        :return:
        """
        return self.__entered_users[name]

    def __open_raffle__(self):
        self.__is_open = True
