"""
This will hold a queue of the commands that can be executed by the bot.
This is how I will handle synchronization. Forcing all the commands to go
through here.
Essentially, a user issues the command, the command is sent here to be queued up.
And the queue pops the commands one at a time and fully executes it before going
to the next item in the queue.
"""
import time
from threading import Thread


class Cmdmngr(Thread):
    def __init__(self):
        super().__init__()
        self.queue = []

    def enqueue(self, cmd):
        self.queue.append(cmd)

    def run(self):
        while True:
            if not self.queue:
                continue
            else:
                self.exec_cmd(self.queue.pop())
            time.sleep(1)

    def exec_cmd(self, c):
        # I need to get these commands working from this file, rather than
        # chatbot.py.
        '''
        # Poll the API to get current game.
        if cmd == "game":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' is currently playing ' + r['game'])

        # Poll the API the get the current status of the stream
        elif cmd == "title":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' channel title is currently ' + r['status'])

        # Provide basic information to viewers for specific commands
        elif cmd == "raffle":
            message = "This is an example bot, replace this text with your raffle text."
            c.privmsg(self.channel, message)
        elif cmd == "schedule":
            message = "This is an example bot, replace this text with your schedule text."
            c.privmsg(self.channel, message)
        elif cmd == "kernels":
            c.privmsg(self.channel, e.source.nick + ", you have " +
                      str(self.bucket.get_points(e.source.nick)) + " kernels")
        elif cmd == "hw":
            c.privmsg(self.channel, "Hello World!")
        elif cmd == "donate":
            args = e.arguments[0].split(' ')
            if len(args) != 3:
                message = 'Incorrect use of !donate, should be: "!donate [amount] [user]"'
                c.privmsg(self.channel, message)
            else:
                c.privmsg(self.channel, self.bucket.transfer_points(e.source.nick, args[2], args[1]))

        # The command was not recognized
        else:
            c.privmsg(self.channel, "Did not understand command: " + cmd)
        '''
        return c
