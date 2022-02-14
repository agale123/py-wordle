import unittest

from pywordle import Wordle


class TestWordle(unittest.TestCase):

    def test_value(self):
        wordle = Wordle()
        self.assertTrue(wordle.value)


if __name__ == '__main__':
    unittest.main()
