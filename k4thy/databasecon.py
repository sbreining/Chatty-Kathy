"""
This will handle the connection to the database
I will use sqlite. And so far it will hold viewers
and their loyalty point values.
"""

import os
import sqlite3


class DBCon:
    def __init__(self):
        d = os.path.dirname(__file__)
        docs_path = os.path.join(d, '../docs/')

        self.db = sqlite3.connect(docs_path + "kettlebase.db", check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.cur = self.db.cursor()

    def add_new_viewer(self, name):
        n = name.lower()  # Make sure the name passed in is all lowercase.
        try:
            with self.db:
                self.db.execute("INSERT INTO viewers(name, points) VALUES (?, ?)", (n, 1,))
        except sqlite3.IntegrityError:
            return False
        return True

    def update_points(self, name, amount):
        self.db.execute("UPDATE viewers SET points=? WHERE name=?", (amount, name,))
        self.db.commit()

    def get_points(self, name):
        p = self.cur.execute("SELECT points FROM viewers WHERE name=?", (name,)).fetchone()[0]
        return p

    def add_points(self, name, amount):
        p = self.get_points(name)
        p += int(amount)
        self.update_points(name, p)

    def subtract_points(self, name, amount):
        p = self.get_points(name)
        v = int(amount)
        if v > p:
            p = 0
        else:
            p -= v
        self.update_points(name, p)

    def transfer_points(self, donator, receiver, amount):
        p = self.get_points(donator)
        try:
            v = int(amount)
        except ValueError:
            return "Donations must be whole numbers"

        if v > p:
            return donator + ", you cannot donate that much."
        elif v < 0:
            return donator + ", don't try to steal, you bastard."
        else:
            self.cur.execute("SELECT count(*) FROM viewers WHERE name=?", (receiver,))
            data = self.cur.fetchone()[0]
            if data == 0:
                return "There is no viewer named " + receiver + " to give points to."
            else:
                self.subtract_points(donator, v)
                self.add_points(receiver, v)
        return donator + " gave " + str(v) + " kernels to " + receiver
