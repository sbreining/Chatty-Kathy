import sys
sys.path.append('../')

import unittest
from k4thy.databasecon import DBCon


class TestDataBaseCon(unittest.TestCase):

    def __init__(self):
        super(TestDataBaseCon, self).__init__()
        self.db = DBCon()

    def test_add_new_viewer(self):
        self.assertTrue(self.db.add_new_viewer('John'))
        self.assertFalse(self.db.add_new_viewer('John'))

    def test_get_points(self):
        self.assertEqual(self.db.get_points('disneyprincess0293'), 13)


def main():
    test = TestDataBaseCon()
    test.test_add_new_viewer()
    test.test_get_points()


if __name__ == "__main__":
    main()
