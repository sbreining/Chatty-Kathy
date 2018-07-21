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
        self.__raffle_manager__ = rafflemngr.RaffleMngr(bot, bucket)
        self.__command_queue = []

    def enqueue(self, cmd, e):
        """
        enqueue pushes the command into the command queue for the thread to pop
        one command at a time.

        :param cmd:
        :param e:
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
            self.__do_command_game__()

        # Poll the API to get current stream info
        elif cmd[0] == "title":
            self.__do_command_title__()

        #
        # ----- Here begins point based commands -----
        #
        elif cmd[0] == "kernels":
            self.__do_command_kernels__(cmd[1])

        #
        # ----- Here begins mod commands -----
        #
        elif cmd[0] == "addcom":
            self.__do_command_addcom__(cmd[1])

        elif cmd[0] == "rmvcom":
            self.__do_command_rmvcom__(cmd[1])

        elif cmd[0] == "updatecom":
            self.__do_command_updatecom__(cmd[1])

        #
        # ----- Here beings raffle commands
        #
        elif cmd[0] == "beginraf":
            self.__do_command_beginraf__(cmd[1])

        elif cmd[0] == "redraw":
            self.__do_command_redraw__(cmd[1])

        elif cmd[0] == "cancelraf":
            self.__do_command_cancelraf__(cmd[1])

        elif cmd[0] == "closeraf":
            self.__do_command_closeraf__(cmd[1])

        elif cmd[0] == "here":
            self.__do_command_here__(cmd[1])

        elif cmd[0] == "ticket":
            self.__do_command_ticket__(cmd[1])

        #
        # ---- Here begins poker commands
        #
        elif cmd[0] == "poker":
            pass

        #
        # ------------ The command was not recognized
        #
        else:
            self.bot.send_message(self.bucket.get_command_response(cmd[0]))

    #
    # ------ Here starts miscellaneous helper functions and private functions
    #
    def __no_permission__(self):
        """
        This just informs the user that they don't have permission to run the
        command they entered.

        :return:
        """
        self.bot.send_message("You don't have permission to use that command")

    def __get_streamer_info__(self):
        """
        API call collecting the streamers info. A lot of info actually.

        :return:
        """
        url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
        headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        return requests.get(url, headers=headers).json()

    def __do_command_game__(self):
        r = self.__get_streamer_info__()
        self.bot.send_message(r['display_name'] +
                              ' is currently playing ' +
                              r['game'])

    def __do_command_title__(self):
        r = self.__get_streamer_info__()
        self.bot.send_message(r['display_name'] +
                              ' channel title is currently ' +
                              r['status'])

    def __do_command_kernels__(self, chatter):
        self.bot.send_message("You have " + str(self.bucket.get_points(chatter.source.nick))
                              + " kernels", chatter.source.nick)

    def __do_command_addcom__(self, mod):
        if mod.tags[0]['value'][:-2] != 'moderator' \
                and mod.tags[0]['value'][:-2] != 'broadcaster':
            self.__no_permission__()
            return
        args = mod.arguments[0].split('\"')
        if len(args) != 3:
            self.bot.send_message("Incorrect use of addcom")
            return
        commands = args[0].split(' ')
        if self.bucket.add_command(commands[1], args[1]):
            self.bot.send_message("Command was added successfully")
        else:
            self.bot.send_message("Command was NOT added, could already exist")

    def __do_command_rmvcom__(self, mod):
        if mod.tags[0]['value'][:-2] != 'moderator' \
                and mod.tags[0]['value'][:-2] != 'broadcaster':
            self.__no_permission__()
            return
        args = mod.arguments[0].split(' ')
        if len(args) != 2:
            self.bot.send_message("Incorrect use of rmvcom")
            return
        if self.bucket.remove_command(args[1]):
            self.bot.send_message("Command was removed successfully")
        else:
            self.bot.send_message("Command was NOT removed, might not exist?")

    def __do_command_updatecom__(self, mod):
        if mod.tags[0]['value'][:-2] != 'moderator' \
                and mod.tags[0]['value'][:-2] != 'broadcaster':
            self.__no_permission__()
            return
        args = mod.arguments[0].split('\"')
        if len(args) != 3:
            self.bot.send_message("Incorrect use of updatecom")
            return
        commands = args[0].split(' ')
        if self.bucket.update_command(commands[1], args[1]):
            self.bot.send_message("Command was updated successfully")
        else:
            self.bot.send_message("Command didn't update, does it exist?")

    def __do_command_beginraf__(self, broadcaster):
        if broadcaster.tags[0]['value'][:-2] == 'broadcaster':
            mt, t = parse_flags(broadcaster.arguments[0])
            if not cktools.is_integer(mt) or not cktools.is_integer(t):
                self.bot.send_message("The raffle needs whole number values for the options")
                return
            self.__raffle_manager__.set_options(mt, t)
            self.__raffle_manager__.start()
        else:
            return

    def __do_command_redraw__(self, broadcaster):
        if broadcaster.tags[0]['value'][:-2] == 'broadcaster':
            self.__raffle_manager__.redraw_winner()
        else:
            return

    def __do_command_cancelraf__(self, broadcaster):
        if broadcaster.tags[0]['value'][:-2] == 'broadcaster':
            self.__raffle_manager__.interrupt()

    def __do_command_closeraf__(self, broadcaster):
        if broadcaster.tags[0]['value'][:-2] == 'broadcaster':
            self.__raffle_manager__.manual_close_raffle()

    def __do_command_here__(self, viewer):
        if viewer.source.nick == self.__raffle_manager__.get_winner():
            self.__raffle_manager__.winner_found()

    def __do_command_ticket__(self, viewer):
        args = viewer.arguments[0].split(' ')
        user_total_tickets = self.bucket.get_points(viewer.source.nick)
        try:
            t = int(args[1])
        except ValueError:
            self.bot.send_message("To enter a drawing, you must enter with\
                                              a whole number of tickets.", viewer.source.nick)
            return
        if t > user_total_tickets:
            self.bot.send_message("You don't have that many tickets to submit. Your \
                                               total tickets are " + str(user_total_tickets), viewer.source.nick)
        elif t < 0:
            self.bot.send_message("Don't be an idiot trying to submit less than \
                                              0 tickets", viewer.source.nick)
        else:
            self.__raffle_manager__.submit_tickets(viewer.source.nick, t)
        return
