'''
This will handle the connection to the database
I will use sqlite. And so far it will hold viewers
and their loyalty point values.
'''

import os
import sqlite3


class DBCon:
    def __init__(self):
        d = os.path.dirname(__file__)
        docs_path = os.path.join(d, '../docs/')

        self.db = sqlite3.connect(docs_path + "kettlebase.db")
        self.db.row_factory = sqlite3.Row
        self.cur = self.db.cursor()

    def add_new_viewer(self, name):
        n = name.lower()  # Make sure the name passed in is all lowercase.
        try:
            with self.db:
                self.db.execute("insert into viewers(name, points) values (?, ?)", (n, 0,))
        except sqlite3.IntegrityError:
            print("Don't insert a viewer twice")

    def update_points(self, name, amount):
        self.db.execute("update viewers set points=? where name=?", (amount, name,))
        self.db.commit()

    def get_points(self, name):
        p = self.cur.execute("select points from viewers where name=?", (name,)).fetchone()[0]
        return p

    def add_points(self, name, amount):
        p = self.get_points(name)
        p += amount
        self.update_points(name, p)

    def subtract_points(self, name, amount):
        p = self.get_points(name)
        if amount > p:
            p = 0
        else:
            p -= amount
        self.update_points(name, p)

    def transfer_points(self, donator, receiver, amount):
        p = self.get_points(donator)
        if amount > p:
            print("Send message to chat saying donator cannot donate that amount")
        else:
            self.subtract_points(donator, amount)
            self.add_points(receiver, amount)
