"""
This will hold a queue of the commands that can be executed by the bot.
This is how I will handle synchronization. Forcing all the commands to go
through here.
A user issues the command, the command is sent here to be queued up.
And the queue pops the commands one at a time and fully executes it before going
to the next item in the queue.
"""
import re
import time
import requests
from threading import Thread

from k4thy import rafflemngr


class Cmdmngr(Thread):
    def __init__(self, b, c_id, cl_id, bins, l):
        super().__init__()
        self.queue = []
        self.bot = b
        self.channel_id = c_id
        self.client_id = cl_id
        self.bucket = bins
        self.lock = l
        self._raffle_manager = rafflemngr.RaffleMngr(b, bins)

    def enqueue(self, cmd, e):
        self.queue.append([cmd, e])

    def run(self):
        while True:
            if not self.queue:
                continue
            else:
                self.exec_cmd(self.queue.pop())
            time.sleep(2)

    def exec_cmd(self, cmd):
        if cmd[0] == "game":
            r = self.get_streamer_info()
            self.bot.send_message(r['display_name'] +
                                  ' is currently playing ' +
                                  r['game'])

        # Poll the API to get current stream info
        elif cmd[0] == "title":
            r = self.get_streamer_info()
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
                self.no_permission()
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
                self.no_permission()
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
                self.no_permission()
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
                mt, t = self.parse_flags(cmd[1].arguments[0])
                self._raffle_manager.set_options(cmd, mt, t)
                self._raffle_manager.start()
            else:
                return

        elif cmd[0] == "redraw":
            if cmd[1].tags[0]['value'][:-2] == 'broadcaster':
                self._raffle_manager.redraw_winner()
            else:
                return

        elif cmd[0] == "cancelraf":
            if cmd[1].tags[0]['value'][:-2] == 'broadcaster':
                self._raffle_manager.interrupt()

        elif cmd[0] == "closeraf":
            if cmd[1].tags[0]['value'][:-2] == 'broadcaster':
                self._raffle_manager.manual_close_raffle()

        elif cmd[0] == "here" and cmd[1].source.nick == self._raffle_manager.get_winner():
            self._raffle_manager.winner_found()

        elif cmd[0] == "ticket":
            args = cmd[1].arguments[0].split(' ')
            user_total_tickets = self.bucket.get_points(cmd[1].source.nick)
            try:
                t = int(args[1])
            except ValueError:
                self.bot.send_message("To enter a drawing, you must enter with\
                                      a whole number of tickets.",
                                      True, cmd[1].source.nick)
                return
            if t > user_total_tickets:
                self.bot.send_message("You don't have that many tickets to submit. Your \
                                       total tickets are " + str(user_total_tickets),
                                      True, cmd[1].source.nick)
            elif t < 0:
                self.bot.send_message("Don't be an idiot trying to submit less than \
                                      0 tickets", True, cmd[1].source.nick)
            else:
                self._raffle_manager.submit_tickets(cmd[1].source.nick, t)
            return

        #
        # ------------ The command was not recognized
        #
        else:
            self.bot.send_message(self.bucket.get_command_response(cmd[0]))

    #
    # ------ Here starts miscellaneous helper functions
    #
    def no_permission(self):
        self.bot.send_message("You don't have permission to use that command")

    def get_streamer_info(self):
        url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
        headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        return requests.get(url, headers=headers).json()

    @staticmethod
    def parse_flags(s):
        mt = t = 0
        m = re.match(r'(\S+) (-m )*(?P<max_tick>\d+)*( )*(-t )*(?P<time>\d+)*', s)
        m.groupdict()
        if m['max_tick']:
            mt = m['max_tick']
        if m['time']:
            t = m['time']
        return mt, t
