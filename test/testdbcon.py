import os
import sys
import unittest
sys.path.append('../')
from k4thy.dbcon import DatabaseConnection

dir_ = os.path.dirname(__file__)
db_path = dir_ + '/testkettlebase.db'


def set_up_viewers_table():
    db = DatabaseConnection(db_path)
    cursor, connection = db.__get_cursor_and_connection__()
    cursor.execute("CREATE TABLE viewers("
                   "name STRING, points INT, PRIMARY KEY (name))")
    cursor.execute("INSERT INTO viewers(name, points) VALUES (?, ?)", ('john', 5))
    connection.commit()
    return db, cursor, connection


def set_up_commands_table():
    db = DatabaseConnection(db_path)
    cursor, connection = db.__get_cursor_and_connection__()
    cursor.execute("CREATE TABLE textcommands("
                   "command STRING, response STRING, PRIMARY KEY (command))")
    cursor.execute("INSERT INTO textcommands(command, response) VALUES (?, ?)", ('test', 'This is test text'))
    connection.commit()
    return db, cursor, connection


def drop_viewers(cursor, connection):
    cursor.execute("DROP TABLE viewers")
    connection.commit()


def drop_commands(cursor, connection):
    cursor.execute("DROP TABLE textcommands")
    connection.commit()


class TestDatabaseConnection(unittest.TestCase):
    """
    Test the command and viewer-point database.
    """

    def test_add_new_viewer(self):
        #  Set up the table for the test.
        db, cursor, connection = set_up_viewers_table()

        #  Running tests and assertions.
        self.assertTrue(db.add_new_viewer('bill'))
        self.assertFalse(db.add_new_viewer('john'))

        #  Drop tables for next test.
        drop_viewers(cursor, connection)

    def test_get_points(self):
        #  Set up the table for the test.
        db, cursor, connection = set_up_viewers_table()

        #  Running tests and assertions.
        actual = db.get_points('john')
        expected = 5
        self.assertEqual(expected, actual)

        #  Drop tables for next test.
        drop_viewers(cursor, connection)

    def test_update_points(self):
        #  Set up the table for the test.
        db, cursor, connection = set_up_viewers_table()

        #  Running tests and assertions.
        db.update_points('john', 10)
        actual = db.get_points('john')
        expected = 10
        self.assertEqual(expected, actual)

        #  Drop tables for next test.
        drop_viewers(cursor, connection)

    def test_add_points(self):
        #  Set up the table for the test.
        db, cursor, connection = set_up_viewers_table()

        #  Running tests and assertions.
        db.add_points('john', 10)
        actual = db.get_points('john')
        expected = 15
        self.assertEqual(expected, actual)

        #  Drop tables for next test.
        drop_viewers(cursor, connection)

    def test_subtract_points(self):
        #  Set up the table for the test.
        db, cursor, connection = set_up_viewers_table()

        #  Running tests and assertions.
        db.subtract_points('john', 1)
        actual = db.get_points('john')
        expected = 4
        self.assertEqual(expected, actual)

        db.subtract_points('john', 5)
        actual = db.get_points('john')
        expected = 0
        self.assertEqual(expected, actual)

        db.subtract_points('john', -5)
        actual = db.get_points('john')
        expected = 5
        self.assertEqual(expected, actual)

        #  Drop tables for next test.
        drop_viewers(cursor, connection)

    def test_get_command_response(self):
        #  Set up commands table
        db, cursor, connection = set_up_commands_table()

        #  Running tests and assertions.
        actual = db.get_command_response('test')
        expected = 'This is test text'
        self.assertEqual(expected, actual)

        #  Drop commands table
        drop_commands(cursor, connection)

    def test_add_command(self):
        #  Set up commands table
        db, cursor, connection = set_up_commands_table()

        #  Running tests and assertions.
        self.assertTrue(db.add_command('something', 'This is add command response'))
        self.assertFalse(db.add_command('test', 'This is new test text'))

        actual = db.get_command_response('something')
        expected = 'This is add command response'
        self.assertEqual(expected, actual)

        #  Drop commands table
        drop_commands(cursor, connection)

    def test_update_command(self):
        #  Set up commands table
        db, cursor, connection = set_up_commands_table()

        #  Running tests and assertions.
        db.update_command('test', 'This is the new test text, different from old')
        actual = db.get_command_response('test')
        expected = 'This is the new test text, different from old'
        self.assertEqual(expected, actual)

        #  Drop commands table
        drop_commands(cursor, connection)

    def test_remove_command(self):
        #  Set up commands table
        db, cursor, connection = set_up_commands_table()

        #  Running tests and assertions.
        self.assertFalse(db.remove_command('not_in_db'))
        self.assertTrue(db.remove_command('test'))

        actual = db.get_command_response('test')
        expected = "Not a valid command"
        self.assertEqual(expected, actual)

        self.assertFalse(db.remove_command('test'))

        #  Drop commands table
        drop_commands(cursor, connection)

    def tearDown(self):
        #  Destroy db file after tests complete
        os.remove(db_path)


if __name__ == '__main__':
    unittest.main()
