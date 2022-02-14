import unittest

from pywordle import Game


class TestGame(unittest.TestCase):

    def test_value(self):
        game = Game()
        self.assertTrue(game.value)


if __name__ == '__main__':
    unittest.main()
