import unittest

from game import Game, Status, MovedLetter
from termcolor import colored
from words import VALID_WORDS


class TestGame(unittest.TestCase):

    def test_guess(self):
        game = Game("POINT", False)

        game.guess("SLITS")

        self.assertSetEqual(game._absent_letters, {"S", "L"})
        self.assertDictEqual(game._correct_letters, {"I": {2}})
        self.assertDictEqual(game._moved_letters, {
                             "T": MovedLetter(1, 5, {3})})

    def test_guess_handles_casing(self):
        game = Game("pOInt", False)

        game.guess("SliTs")

        self.assertSetEqual(game._absent_letters, {"S", "L"})
        self.assertDictEqual(game._correct_letters, {"I": {2}})
        self.assertDictEqual(game._moved_letters, {
                             "T": MovedLetter(1, 5, {3})})

    def test_guess_duplicate_letters(self):
        game = Game("SLITS", False)

        game.guess("BOSSY")

        self.assertSetEqual(game._absent_letters, {"B", "O", "Y"})
        self.assertDictEqual(game._correct_letters, {})
        self.assertDictEqual(game._moved_letters, {
                             "S": MovedLetter(2, 5, {2, 3})})

    def test_guess_duplicate_letters_guess(self):
        game = Game("POINT", False)

        game.guess("HAPPY")

        self.assertSetEqual(game._absent_letters, {"H", "A", "Y"})
        self.assertDictEqual(game._correct_letters, {})
        self.assertDictEqual(game._moved_letters, {
                             "P": MovedLetter(1, 1, {2, 3})})

    def test_guess_duplicate_letters_answer(self):
        game = Game("HAPPY", False)

        game.guess("POINT")

        self.assertSetEqual(game._absent_letters, {"O", "I", "N", "T"})
        self.assertDictEqual(game._correct_letters, {})
        self.assertDictEqual(game._moved_letters, {
                             "P": MovedLetter(1, 5, {0})})

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
        game._absent_letters = {"I", "L", "N"}
        game._correct_letters = {"A": {1}}
        game._moved_letters = {"A": MovedLetter(
            1, 5, {0}), "S": MovedLetter(1, 5, {1, 4})}

        self.assertTrue(game.is_valid("SPILL"))
        self.assertFalse(game.is_valid("AAAAA"))

    def test_is_valid_hard_mode(self):
        game = Game("CAUSE", True)
        game._absent_letters = {"I", "L", "N"}
        game._correct_letters = {"A": {1}}
        game._moved_letters = {"A": MovedLetter(
            1, 5, {0}), "S": MovedLetter(1, 5, {1, 4})}

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

        self.assertSetEqual(
            set(game.get_possible_solutions()),
            set(["CAUSE", "PAUSE", "HAUSE"]))

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
