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


class Vmanager(Thread):
    def __init__(self, db, s, l):
        super().__init__()
        self.streamer = s
        self.db = db
        self.lock = l

    def run(self):
        url = "https://tmi.twitch.tv/group/user/" + self.streamer + "/chatters"
        while True:
            try:
                r = requests.get(url).json()
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
            time.sleep(300)
            del r
