import unittest

from wordle import Wordle

SOLUTIONS = ["raise", "treat", "spoil"]


class TestWordle(unittest.TestCase):

    def test_wordle_checks_word_legnth(self):
        self.assertRaises(Exception, Wordle, ["cat"])

    def test_start_game(self):
        wordle = Wordle(SOLUTIONS)

        game = wordle.start_game(False)
        self.assertIn(game.solution, SOLUTIONS)
        self.assertFalse(game.hard_mode)

    def test_start_game_with_solution(self):
        wordle = Wordle(SOLUTIONS)

        game = wordle.start_game(False, "raise")
        self.assertEqual(game.solution, "raise")

    def test_start_game_invalid_word(self):
        wordle = Wordle(SOLUTIONS)

        self.assertRaises(Exception, wordle.start_game, False, "foist")

    def test_repr(self):
        wordle = Wordle(SOLUTIONS)

        self.assertEqual(repr(wordle), "Wordle([\"raise\", \"treat\", \"spoil\"])")


if __name__ == '__main__':
    unittest.main()
