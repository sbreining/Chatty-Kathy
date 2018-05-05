"""
This will hold a queue of the commands that can be executed by the bot.
This is how I will handle synchronization. Forcing all the commands to go
through here.
Essentially, a user issues the command, the command is sent here to be queued up.
And the queue pops the commands one at a time and fully executes it before going
to the next item in the queue.
"""
import time
import requests
from threading import Thread, Lock


class Cmdmngr(Thread):
    def __init__(self, c_id, cl_id, chan, bins, l):
        super().__init__()
        self.queue = []
        self.channel_id = c_id
        self.client_id = cl_id
        self.channel = chan
        self.bucket = bins
        self.lock = l

    def enqueue(self, cmd, conn, e):
        self.queue.append([cmd, conn, e])

    def run(self):
        while True:
            if not self.queue:
                continue
            else:
                self.exec_cmd(self.queue.pop())
            time.sleep(2)

    def exec_cmd(self, cmd):
        if cmd[0] == "game":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            cmd[1].privmsg(self.channel, r['display_name'] + ' is currently playing ' + r['game'])

        # Poll the API the get the current status of the stream
        elif cmd[0] == "title":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            cmd[1].privmsg(self.channel, r['display_name'] + ' channel title is currently ' + r['status'])

        elif cmd[0] == "kernels":
            cmd[1].privmsg(self.channel, cmd[2].source.nick + ", you have " +
                           str(self.bucket.get_points(cmd[2].source.nick)) + " kernels")

        elif cmd[0] == "donate":
            args = cmd[2].arguments[0].split(' ')
            if len(args) != 3:
                message = 'Incorrect use of !donate, should be: "!donate [amount] [user]"'
                cmd[1].privmsg(self.channel, message)
            else:
                self.lock.acquire()
                cmd[1].privmsg(self.channel, self.bucket.transfer_points(cmd[2].source.nick, args[2], args[1]))
                self.lock.release()

        # TODO: Check if command was issued by a mod or channel owner.
        elif cmd[0] == "addcom":
            print(cmd[1])
            if cmd[2].tags[5]['value'] == '0':  # Is this right?
                self.no_permission(cmd[1])
                return
            args = cmd[2].arguments[0].split('\"')
            commands = args[0].split(' ')
            if self.bucket.add_command(commands[1], args[1]):
                cmd[1].privmsg(self.channel, "Command was added successfully")
            else:
                cmd[1].privmsg(self.channel, "Command was NOT added, could already exist")

        # TODO: Check if command was issued by a mod or channel owner.
        elif cmd[0] == "rmvcom":
            # 5 is the key-value pair 'key': 'mod' 'value': '0' or '1'
            if cmd[2].tags[5]['value'] == '0':
                self.no_permission(cmd[1])
                return
            args = cmd[2].arguments[0].split(' ')
            if self.bucket.remove_command(args[1]):
                cmd[1].privmsg(self.channel, "Command was removed successfully")
            else:
                cmd[1].privmsg(self.channel, "Command was NOT removed, might it not exist?")
        # The command was not recognized
        else:
            cmd[1].privmsg(self.channel, self.bucket.get_command_response(cmd[0]))

    def no_permission(self, c):
        c.privmsg(self.channel, "You don't have permission to use that command")
