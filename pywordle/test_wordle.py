import unittest

from wordle import Wordle

SOLUTIONS = ["RAISE", "TREAT", "SPOIL"]


class TestWordle(unittest.TestCase):

    def test_wordle_checks_word_legnth(self):
        self.assertRaises(Exception, Wordle, ["CAT"])

    def test_start_game(self):
        wordle = Wordle(SOLUTIONS)

        game = wordle.start_game(False)
        self.assertIn(game._solution, SOLUTIONS)
        self.assertFalse(game._hard_mode)

    def test_start_game_with_solution(self):
        wordle = Wordle(SOLUTIONS)

        game = wordle.start_game(False, "RAISE")
        self.assertEqual(game._solution, "RAISE")

    def test_start_game_invalid_word(self):
        wordle = Wordle(SOLUTIONS)

        self.assertRaises(Exception, wordle.start_game, False, "FOIST")

    def test_repr(self):
        wordle = Wordle(SOLUTIONS)

        self.assertEqual(repr(wordle), "Wordle(['RAISE', 'TREAT', 'SPOIL'])")


if __name__ == '__main__':
    unittest.main()
