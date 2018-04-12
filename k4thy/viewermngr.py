import time
import requests
from threading import Thread


class Vmanager(Thread):
    def __init__(self, db, s):
        super().__init__()
        self.db = db
        self.streamer = s

    def run(self):
        url = "https://tmi.twitch.tv/group/user/" + self.streamer + "/chatters"
        while True:
            r = requests.get(url).json()
            viewers = []
            chatters = r["chatters"]
            for group in chatters:
                viewers += chatters[group]

            print(viewers)

            for v in viewers:
                if self.db.add_new_viewer(v):
                    continue
                else:
                    self.db.add_points(v, 1)
            time.sleep(10)
            del r
            print('finished iteration')
