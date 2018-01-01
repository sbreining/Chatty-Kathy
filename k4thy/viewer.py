'''
This class monitors the viewers.
It will handle loyalty points mostly.
If other functions arise, I will update this description.
'''

import os


class ViewerContainer:
    def __init__(self):
        self.viewers = {}
        d = os.path.dirname(__file__)
        docs_path = os.path.join(d, '../docs/')
        try:
            self.savefile = open(docs_path + 'viewers.txt', 'r+')
        except FileNotFoundError:
            print("File not found")
            exit(1001)

    def add_viewer(self, name):
        if name not in self.viewers:
            self.viewers.update({name: 0})

    def save_viewers(self):
        self.savefile.seek(0, 0)
        for key in self.viewers:
            self.savefile.write(key + ' ' + str(self.viewers[key]) + '\n')

        self.savefile.close()

    def load_viewers(self):
        people = self.savefile.readlines()

        people = [x.strip('\n') for x in people]

        for p in people:
            index = p.find(' ')
            self.viewers.update({p[0:index]: int(p[index+1:])})

        print(self.viewers)

    def add_points(self, name, amount):
        self.viewers[name] += amount

    def subtract_points(self, name, amount):
        if amount > self.viewers[name]:
            self.viewers[name] = 0
        else:
            self.viewers[name] -= amount

    def transfer_points(self, donator, receiver, amount):
        if amount > self.viewers[donator]:
            print("Send message to chat that user cannot donate that much")
        else:
            self.subtract_points(donator, amount)
            self.add_points(receiver, amount)
