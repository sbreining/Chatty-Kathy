"""
This will hold a queue of the commands that can be executed by the bot.
This is how I will handle synchronization. Forcing all the commands to go
through here.
A user issues the command, the command is sent here to be queued up.
And the queue pops the commands one at a time and fully executes it before going
to the next item in the queue.
"""
import time
import requests
from threading import Thread

from ch4tty import parse_flags, cktools
from ckg4mes import ckpoker
from k4thy import rafflemngr


class CommandManager(Thread):
    """
    This class handles all command input. It queues up the commands as they
    come in to better handle each command. I have put a 2 second delay for now
    so that commands can be handled without issue. It calls on the TwitchBot
    class to send the messages, utilizing the whisper system.
    """

    def __init__(self, bot, channel_id, client_id, bucket, lock):
        super().__init__()
        self.bot = bot
        self.channel_id = channel_id
        self.client_id = client_id
        self.bucket = bucket
        self.lock = lock

        # Private attributes
        self.__raffle_manager = rafflemngr.RaffleMngr(bot, bucket)
        self.__ckfivecard = ckpoker.FiveCardDraw(bot)
        self.__command_queue = []

    def enqueue(self, e, cmd):
        """
        enqueue pushes the command into the command queue for the thread to pop
        one command at a time.

        :param e:
        :param cmd:
        :return:
        """
        self.__command_queue.append([cmd, e])

    def run(self):
        while True:
            if not self.__command_queue:
                continue
            else:
                self.__exec_cmd(self.__command_queue.pop())
            time.sleep(2)

    #
    # ---- 'Private Methods' ----
    #

    def __exec_cmd(self, cmd):
        """
        Executes commands that are popped out of the queue. Handled by a giant
        if-elif-else block that I really don't like. And finally checking the
        database for text-only responses that moderators or the streamer might
        have added.

        :param cmd:
        :return:
        """

        if cmd[0] == "game":
            r = self.__get_streamer_info()
            self.bot.send_message(r['display_name'] +
                                  ' is currently playing ' +
                                  r['game'])

        # Poll the API to get current stream info
        elif cmd[0] == "title":
            r = self.__get_streamer_info()
            self.bot.send_message(r['display_name'] +
                                  ' channel title is currently ' +
                                  r['status'])

        #
        # ----- Here begins point based commands -----
        #

        elif cmd[0] == "kernels":
            self.bot.send_message("You have " + str(self.bucket.get_points(cmd[1].source.nick))
                                  + " kernels", whisper=True, target=cmd[1].source.nick)

        #
        # ----- Here begins mod commands -----
        #

        elif cmd[0] == "addcom":
            if cmd[1].tags[0]['value'][:-2] != 'moderator'\
                    and cmd[1].tags[0]['value'][:-2] != 'broadcaster':
                self.__no_permission()
                return
            args = cmd[1].arguments[0].split('\"')
            if len(args) != 3:
                self.bot.send_message("Incorrect use of addcom")
                return
            commands = args[0].split(' ')
            if self.bucket.add_command(commands[1], args[1]):
                self.bot.send_message("Command was added successfully")
            else:
                self.bot.send_message("Command was NOT added, could already exist")

        elif cmd[0] == "rmvcom":
            if cmd[1].tags[0]['value'][:-2] != 'moderator'\
                    and cmd[1].tags[0]['value'][:-2] != 'broadcaster':
                self.__no_permission()
                return
            args = cmd[1].arguments[0].split(' ')
            if len(args) != 2:
                self.bot.send_message("Incorrect use of rmvcom")
                return
            if self.bucket.remove_command(args[1]):
                self.bot.send_message("Command was removed successfully")
            else:
                self.bot.send_message("Command was NOT removed, might not exist?")

        elif cmd[0] == "updatecom":
            if cmd[1].tags[0]['value'][:-2] != 'moderator'\
                    and cmd[1].tags[0]['value'][:-2] != 'broadcaster':
                self.__no_permission()
                return
            args = cmd[1].arguments[0].split('\"')
            if len(args) != 3:
                self.bot.send_message("Incorrect use of updatecom")
                return
            commands = args[0].split(' ')
            if self.bucket.update_command(commands[1], args[1]):
                self.bot.send_message("Command was updated successfully")
            else:
                self.bot.send_message("Command didn't update, does it exist?")

        #
        # ----- Here beings raffle commands
        #
        elif cmd[0] == "beginraf":
            if cmd[1].tags[0]['value'][:-2] == 'broadcaster':
                mt, t = parse_flags(cmd[1].arguments[0])
                self.__raffle_manager.set_options(mt, t)
                self.__raffle_manager.start()
            else:
                return

        elif cmd[0] == "redraw":
            if cmd[1].tags[0]['value'][:-2] == 'broadcaster':
                self.__raffle_manager.redraw_winner()
            else:
                return

        elif cmd[0] == "cancelraf":
            if cmd[1].tags[0]['value'][:-2] == 'broadcaster':
                self.__raffle_manager.interrupt()

        elif cmd[0] == "closeraf":
            if cmd[1].tags[0]['value'][:-2] == 'broadcaster':
                self.__raffle_manager.manual_close_raffle()

        elif cmd[0] == "here" and cmd[1].source.nick == self.__raffle_manager.get_winner():
            self.__raffle_manager.winner_found()

        elif cmd[0] == "ticket":
            args = cmd[1].arguments[0].split(' ')
            user_total_tickets = self.bucket.get_points(cmd[1].source.nick)
            max_tickets = self.__raffle_manager.get_max_tickets()
            if user_total_tickets < max_tickets:
                max_tickets = user_total_tickets

            if not cktools.is_integer(args[1]) or cktools.out_of_range(0, max_tickets, args[1]):
                self.bot.send_message("To enter a drawing, you must enter with a valid number of tickets.",
                                      True, cmd[1].source.nick)
            else:
                self.__raffle_manager.submit_tickets(cmd[1].source.nick, args[1])
            return

        #
        # ---- Here begins poker commands
        #
        elif cmd[0] == "poker":
            if cktools.is_poker_off_cooldown:
                if not self.__ckfivecard.is_running():
                    self.__ckfivecard.start()
                    time.sleep(2)  # Sleep for 2 seconds to allow poker thread to start.
                viewer = cmd[1].source.nick

                # In order to play poker, you need minimum of of SUM_MAX_BETS
                if self.bucket.get_points(viewer) < cktools.SUM_MAX_BETS:
                    self.bot.send_message("Sorry, you don't have enough tickets"
                                          " to join the poker game.",
                                          whisper=True, target=viewer)

                self.__ckfivecard.join_the_game(viewer, cktools.ANTE)
            else:
                self.bot.send_message("Five Card Draw is on cooldown. Try again later.")

        elif cmd[0] == "bet":
            # TODO
            # Make sure it is not more than 100 tickets.
            # Make sure it is not less than 0 tickets.
            # Send it to the prize pool.
            pass

        elif cmd[0] == "pass":
            # TODO
            # Move the turn to the next person.
            pass

        #
        # ------------ The command was not recognized
        #
        else:
            self.bot.send_message(self.bucket.get_command_response(cmd[0]))

    #
    # ------ Here starts miscellaneous helper functions
    #
    def __no_permission(self):
        """
        This just informs the user that they don't have permission to run the
        command they entered.

        :return:
        """
        self.bot.send_message("You don't have permission to use that command")

    def __get_streamer_info(self):
        """
        API call collecting the streamers info. A lot of info actually.

        :return:
        """
        url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
        headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        return requests.get(url, headers=headers).json()
