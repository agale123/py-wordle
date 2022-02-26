import unittest

from wordle import Wordle


class TestWordle(unittest.TestCase):

    def test_value(self):
        wordle = Wordle(["foo", "bar", "baz"])
        self.assertListEqual(wordle.solutions, ["foo", "bar", "baz"])


if __name__ == '__main__':
    unittest.main()
