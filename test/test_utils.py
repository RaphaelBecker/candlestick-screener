import unittest
import utils.helpers as helpers


class TestUntils(unittest.TestCase):

    def test_time(self):
        print(helpers.get_current_date())

