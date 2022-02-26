import unittest

from game import Game, Status
from termcolor import colored
from words import VALID_WORDS


class TestGame(unittest.TestCase):

    def test_guess(self):
        game = Game("point", False)

        game.guess("slits")

        self.assertSetEqual(game._absent_letters, {"s", "l"})
        self.assertDictEqual(game._correct_letters, {"i": [2]})
        self.assertDictEqual(game._moved_letters, {"t": ([3], 1)})

    def test_guess_handles_casing(self):
        game = Game("point", False)

        game.guess("SliTs")

        self.assertSetEqual(game._absent_letters, {"s", "l"})
        self.assertDictEqual(game._correct_letters, {"i": [2]})
        self.assertDictEqual(game._moved_letters, {"t": ([3], 1)})

    def test_guess_hard_mode_exception(self):
        game = Game("point", True)
        game._correct_letters["o"] = [1]

        self.assertRaises(Exception, game.guess, "treat")

    def test_guess_invalid_word(self):
        game = Game("foist", False)

        self.assertRaises(Exception, game.guess, "aaaaa")

    def test_guess_wrong_length(self):
        game = Game("spill", False)

        self.assertRaises(Exception, game.guess, "cat")

    def test_guess_game_already_won(self):
        game = Game("spill", False)

        game.guess("spill")

        self.assertRaises(Exception, game.guess, "treat")

    def test_is_valid(self):
        game = Game("cause", False)
        game._absent_letters = {"i", "l", "n"}
        game._correct_letters = {"a": [1]}
        game._moved_letters = {"a": ([0], 1), "s": ([1, 4], 1)}

        self.assertTrue(game.is_valid("spill"))
        self.assertFalse(game.is_valid("aaaaa"))

    def test_is_valid_hard_mode(self):
        game = Game("cause", True)
        game._absent_letters = {"i", "l", "n"}
        game._correct_letters = {"a": [1]}
        game._moved_letters = {"a": ([0], 1), "s": ([1, 4], 1)}

        self.assertTrue(game.is_valid("taper"))
        self.assertTrue(game.is_valid("cause"))
        self.assertFalse(game.is_valid("treat"))
        self.assertFalse(game.is_valid("spill"))
        self.assertFalse(game.is_valid("aaaaa"))

    def test_get_game_status_won(self):
        game = Game("cause", False)

        game.guess("cause")

        self.assertEqual(game.get_game_status(), Status.WON)

    def test_get_game_status_lost(self):
        game = Game("cause", False)

        for x in range(6):
            game.guess("treat")

        self.assertEqual(game.get_game_status(), Status.LOST)

    def test_get_game_status_in_progress(self):
        game = Game("cause", False)

        game.guess("treat")

        self.assertEqual(game.get_game_status(), Status.IN_PROGRESS)

    def test_get_valid_guesses(self):
        game = Game("cause", False)
        game._absent_letters = {"i", "l", "n"}
        game._correct_letters = {"a": [1]}
        game._moved_letters = {"a": ([0], 1), "s": ([1, 4], 1)}

        self.assertListEqual(game.get_valid_guesses(), VALID_WORDS)

    def test_get_valid_guesses_hard_mode(self):
        game = Game("cause", True)
        game._absent_letters = {"i", "l", "n"}
        game._correct_letters = {"a": [1]}
        game._moved_letters = {"a": ([0], 1), "s": ([1, 4], 1)}

        self.assertListEqual(
            game.get_valid_guesses().sort(),
            ["cause", "pause"].sort())

    def test_str(self):
        game = Game("spill", False)

        game.guess("foils")
        game.guess("swirl")
        game.guess("spill")

        expected = "\n".join([
            (
                colored("F", "grey", "on_white") +
                colored("O", "grey", "on_white") +
                colored("I", "grey", "on_green") +
                colored("L", "grey", "on_green") +
                colored("S", "grey", "on_yellow")
            ),
            (
                colored("S", "grey", "on_green") +
                colored("W", "grey", "on_white") +
                colored("I", "grey", "on_green") +
                colored("R", "grey", "on_white") +
                colored("L", "grey", "on_green")
            ),
            (
                colored("S", "grey", "on_green") +
                colored("P", "grey", "on_green") +
                colored("I", "grey", "on_green") +
                colored("L", "grey", "on_green") +
                colored("L", "grey", "on_green")
            ),
        ])

        self.assertEqual(str(game), expected)

    def test_repr(self):
        game = Game("boast", True)

        self.assertEqual(repr(game), "Game(\"boast\", True)")


if __name__ == '__main__':
    unittest.main()
