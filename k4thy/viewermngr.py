"""
This is probably inappropriately named. It should probably be called
time manager, as it adds one point to each viewer every five
minutes. It doesn't really manager the viewers all that much.
So my name is poor, but I'm not going to change it.
"""

import time
import json
import requests
from threading import Thread


class ViewerManager(Thread):
    """
    This class gets the list of viewers that are in the channel of a streamer
    every 5 minutes, and then it attempts to add them to the database of all
    viewers, otherwise it just adds a point to their total points.
    """
    def __init__(self, db, streamer, l):
        super().__init__()
        self.db = db
        self.lock = l

        self.__is_online = False
        self.__url = "https://tmi.twitch.tv/group/user/" + streamer + "/chatters"
        self.__is_live_url = 'https://api.twitch.tv/helix/streams?user_login=' + streamer

    def run(self):

        while True:

            try:
                r = requests.get(self.__url).json()
            except json.JSONDecodeError:
                continue

            viewers = []
            chatters = r["chatters"]
            for group in chatters:
                viewers += chatters[group]

            self.lock.acquire()
            for v in viewers:
                if self.db.add_new_viewer(v):
                    continue
                else:
                    self.db.add_points(v, 1)
            self.lock.release()

            del r  # Delete the request for a clean refresh next loop.

            if self.__is_online:
                time.sleep(300)
            else:
                time.sleep(900)

            self.__check_is_streaming()

    def __check_is_streaming(self):
        """
        Checks if the streamer is currently online to see if people in the chat
        room get 1 point per 5 minutes, or 1 point per 15 minutes.

        :return:
        """
        r = requests.get(self.__is_live_url).json()
        if r['data']:
            self.__is_online = True
        else:
            self.__is_online = False
