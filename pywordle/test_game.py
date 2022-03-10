import unittest

from termcolor import colored

from game import Game, Status


class TestGame(unittest.TestCase):

    def test_guess(self):
        game = Game("POINT", False)

        game.guess("SLITS")

        self.assertDictEqual(game._correct_letters, {"I": {2}})

    def test_guess_handles_casing(self):
        game = Game("pOInt", False)

        game.guess("SliTs")

        self.assertDictEqual(game._correct_letters, {"I": {2}})

    def test_guess_hard_mode_exception(self):
        game = Game("POINT", True)
        game._correct_letters["o"] = [1]

        self.assertRaises(Exception, game.guess, "TREAT")

    def test_guess_invalid_word(self):
        game = Game("FOIST", False)

        self.assertRaises(Exception, game.guess, "AAAAA")

    def test_guess_wrong_length(self):
        game = Game("SPILL", False)

        self.assertRaises(Exception, game.guess, "CAT")

    def test_guess_game_already_won(self):
        game = Game("SPILL", False)

        game.guess("SPILL")

        self.assertRaises(Exception, game.guess, "TREAT")

    def test_is_valid(self):
        game = Game("CAUSE", False)
        game._correct_letters = {"A": {1}}

        self.assertTrue(game.is_valid("SPILL"))
        self.assertFalse(game.is_valid("AAAAA"))

    def test_is_valid_hard_mode(self):
        game = Game("CAUSE", True)
        game._correct_letters = {"A": {1}}

        self.assertTrue(game.is_valid("TAPER"))
        self.assertTrue(game.is_valid("CAUSE"))
        self.assertFalse(game.is_valid("TREAT"))
        self.assertFalse(game.is_valid("SPILL"))
        self.assertFalse(game.is_valid("AAAAA"))

    def test_get_status_won(self):
        game = Game("CAUSE", False)

        game.guess("CAUSE")

        self.assertEqual(game.get_status(), Status.WON)

    def test_get_status_lost(self):
        game = Game("CAUSE", False)

        for x in range(6):
            game.guess("TREAT")

        self.assertEqual(game.get_status(), Status.LOST)

    def test_get_status_in_progress(self):
        game = Game("CAUSE", False)

        game.guess("TREAT")

        self.assertEqual(game.get_status(), Status.IN_PROGRESS)

    def test_plot_progress(self):
        game = Game("SPILL", False)

        game.guess("FOILS")
        game.guess("SWIRL")
        game.guess("IDIOM")
        game.guess("SPILL")

        self.assertListEqual(game.plot_progress(), [12972, 59, 4, 4, 1])

    def test_str(self):
        game = Game("SPILL", False)

        game.guess("FOILS")
        game.guess("SWIRL")
        game.guess("IDIOM")
        game.guess("SPILL")

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
                colored("I", "grey", "on_white") +
                colored("D", "grey", "on_white") +
                colored("I", "grey", "on_green") +
                colored("O", "grey", "on_white") +
                colored("M", "grey", "on_white")
            ),
            (
                colored("S", "grey", "on_green") +
                colored("P", "grey", "on_green") +
                colored("I", "grey", "on_green") +
                colored("L", "grey", "on_green") +
                colored("L", "grey", "on_green")
            ),
        ])

        self.maxDiff = None
        self.assertEqual(str(game), expected)

    def test_repr(self):
        game = Game("BOAST", True)

        self.assertEqual(repr(game), "Game(\"BOAST\", True)")


if __name__ == '__main__':
    unittest.main()
