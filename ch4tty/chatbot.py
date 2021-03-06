"""
Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the
License. A copy of the License is located at
    http://aws.amazon.com/apache2.0/
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and
limitations under the License.
"""

import irc.bot
import requests

from ch4tty import cktools
from k4thy import dbcon
from k4thy import viewermngr
from k4thy import cmdmngr
from threading import Lock


class TwitchBot(irc.bot.SingleServerIRCBot):
    """
    Modified the provided example from Twitch.
    """
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

        self.lock = Lock()

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connections
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:' + token)], username, username)

        self.bucket = dbcon.DatabaseConnection(cktools.DB_PATH)

        self.cmdmgr = cmdmngr.CommandManager(self, self.channel_id, self.client_id,
                                             self.bucket, self.lock)
        self.cmdmgr.start()

        self.vmgr = viewermngr.ViewerManager(self.bucket, channel, self.lock, headers)
        self.vmgr.start()

    def on_welcome(self, c, e):
        print('Joining ' + self.channel)

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        # If a chat message starts with an exclamation point, try to run it as a command
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            self.__do_command(e, cmd)
        return

    def send_message(self, string, target=''):
        if target != '':
            self.connection.privmsg(self.channel, '/w ' + target + ' ' + string)
        else:
            self.connection.privmsg(self.channel, string)

    #
    # ---- 'Private Methods' ----
    #

    def __do_command(self, e, cmd):
        self.cmdmgr.enqueue(cmd, e)
