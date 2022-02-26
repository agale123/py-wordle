import unittest

from game import Game


class TestGame(unittest.TestCase):

    def test_solution(self):
        game = Game("foo", False)
        self.assertEqual(game.solution, "foo")


if __name__ == '__main__':
    unittest.main()
