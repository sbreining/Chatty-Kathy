"""
This will handle the connection to the database
I will use sqlite. And so far it will hold viewers
and their loyalty point values.
"""
import os
import sqlite3


class DatabaseConnection:
    """
    This class handles the Database connection. It directly modifies the tables
    involved with the program.
    """
    def __init__(self):
        d = os.path.dirname(__file__)
        docs_path = os.path.join(d, '../docs/')

        self.db = sqlite3.connect(docs_path + "kettlebase.db",
                                  check_same_thread=False)
        self.cur = self.db.cursor()

    def add_new_viewer(self, name):
        """
        Adds a new viewer to the table that keeps track of viewers that enter
        the chat room. The viewer is added with one point.

        :param name:
        :return:
        """
        n = name.lower()  # Make sure the name passed in is all lowercase.
        try:
            with self.db:
                self.db.execute("INSERT INTO viewers(name, points) VALUES (?, ?)", (n, 1,))
        except sqlite3.IntegrityError:
            return False
        return True

    def update_points(self, name, amount):
        """
        This updates the points of a given named viewer. Usually involved with
        adding or subtracting the points of a viewer based on raffle entries,
        gambles, or time in channel.

        :param name:
        :param amount:
        :return:
        """
        self.db.execute("UPDATE viewers SET points=? WHERE name=?", (amount, name,))
        self.db.commit()

    def get_points(self, name):
        """
        Pulls the points from the table for the given viewer.

        :param name:
        :return:
        """
        p = self.cur.execute("SELECT points FROM viewers WHERE name=?", (name,)).fetchone()[0]
        return p

    def add_points(self, name, amount):
        """
        Adds `amount` points to `name` viewer.

        :param name:
        :param amount:
        :return:
        """
        p = self.get_points(name)
        p += int(amount)
        self.update_points(name, p)

    def subtract_points(self, name, amount):
        """
        Subtracts `amount` points from `name` viewer.

        :param name:
        :param amount:
        :return:
        """
        p = self.get_points(name)
        v = int(amount)
        if v > p:
            p = 0
        else:
            p -= v
        self.update_points(name, p)

    '''
    ------------------ Begin functions for textcommands table ------------------
    
    These functions access the textcommands table, which is a table of text-only commands.
    This will allow mods to add informational text-only response commands to the channel
    at any time.
    '''

    def get_command_response(self, cmd):
        """
        Gets the response for the given command and returns the response to the
        bot can send the message to the chat room.

        :param cmd:
        :return:
        """
        command = cmd.lower()
        response = self.cur.execute("SELECT response FROM textcommands WHERE command=?", (command,)).fetchone()
        if response is None:
            return "Not a valid command"
        else:
            return response[0]

    def add_command(self, cmd, response):
        """
        This allows a command be added to the table with a text-only response.
        The user is assumed to be a moderator or streamer, but those permissions
        are checked in the command manager module.

        :param cmd:
        :param response:
        :return:
        """
        c = cmd.lower()  # Make sure the name passed in is all lowercase.
        try:
            with self.db:
                self.db.execute("INSERT INTO textcommands(command, response) VALUES (?, ?)", (c, response,))
        except sqlite3.IntegrityError:
            return False
        return True

    def update_command(self, cmd, response):
        """
        Will update the named command to have a different response. The response
        can only be text responses.

        :param cmd:
        :param response:
        :return:
        """
        c = cmd.lower()
        try:
            with self.db:
                self.db.execute("UPDATE textcommands SET response=? WHERE command=?", (response, c,))
        except sqlite3.IntegrityError:
            return False
        return True

    def remove_command(self, cmd):
        """
        Removes a command from the table all together. Cannot be undone, once
        the command is removed, it is gone and must be recreated to be seen
        again.

        :param cmd:
        :return:
        """
        c = cmd.lower()
        try:
            with self.db:
                self.db.execute("DELETE FROM textcommands WHERE command=?", (c,))
        except sqlite3.IntegrityError:
            return False
        return True
