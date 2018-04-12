import time
import requests
from threading import Thread


class Vmanager(Thread):
    def __init__(self, s):
        super().__init__()
        self.streamer = s

    def run(self):
        url = "https://tmi.twitch.tv/group/user/" + "blizzheroes" + "/chatters"
        while True:
            r = requests.get(url).json()
            viewers = []
            chatters = r["chatters"]
            for group in chatters:
                viewers += chatters[group]

            print(len(viewers))
            time.sleep(15)
            print("Finished loop")
            del r
