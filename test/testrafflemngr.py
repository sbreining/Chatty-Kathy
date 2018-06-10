import unittest

from mock import Mock

from k4thy.rafflemngr import RaffleMngr


class TestRaffleMngr(unittest.TestCase):

    def test_set_options(self):
        """
        There is verification in the command entry process making sure that
        the values passed in are ints but they are in string form. So we do not
        need to test passing in float or non-number values.
        :return:
        """
        rm = RaffleMngr(None, None)

        rm.set_options(500, 5)
        actual_tickets = rm.get_max_tickets()
        expected_tickets = 500
        self.assertEqual(expected_tickets, actual_tickets)
        actual_time = rm.get_raffle_duration()
        expected_time = 300
        self.assertEqual(expected_time, actual_time)

    def test_submit_tickets(self):
        mock_bot = Mock()
        rm = RaffleMngr(mock_bot, None)

        # Raffle not open yet, so user cannot submit.
        self.assertFalse(rm.submit_tickets('Steve', 500))

        # Open the raffle to allow ticket submissions.
        rm.__open_raffle__()
        self.assertTrue(rm.submit_tickets('Steve', 500))
        actual = rm.get_viewers_submitted_tickets('Steve')
        expected = 500
        self.assertEqual(expected, actual)

        # Test a max ticket limit.
        rm.set_options(m=50)
        self.assertFalse(rm.submit_tickets('Joey', 51))
        self.assertTrue(rm.submit_tickets('Stan', 49))
        actual_1 = rm.get_viewers_submitted_tickets('Stan')
        expected_1 = 49
        self.assertEqual(expected_1, actual_1)

        # Test a user updating the amount of their tickets they've entered with.
        self.assertTrue(rm.submit_tickets('Alice', 25))
        actual_2 = rm.get_viewers_submitted_tickets('Alice')
        expected_2 = 25
        self.assertEqual(expected_2, actual_2)
        self.assertTrue(rm.submit_tickets('Alice', 5))
        actual_3 = rm.get_viewers_submitted_tickets('Alice')
        expected_3 = 5
        self.assertEqual(expected_3, actual_3)


if __name__ == '__main__':
    unittest.main()
