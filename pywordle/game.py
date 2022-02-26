from words import VALID_WORDS
from enum import Enum


class Game:
    """Represents an individual game of Wordle."""

    def __init__(self, solution, hard_mode):
        """
        Args:
            solution: The answer for the game.
            hard_mode: True if previous known letters must be used.
        """
        self.solution = solution
        self.hard_mode = hard_mode

        # Set of guessed letters not in the solution.
        self._absent_letters = {}

        # Map from guessed letters to a list of indices.
        self._correct_letters = {}

        # Map from guessed letters to a tuple containing a list of indices
        # where the letter isn't and the minimum number of instances.
        self._moved_letters = {}

    def guess(self, word):
        """
        Updates the game state to reflect the guessed word.

        Args:
            word: The desired guess for the game.

        Raises:
            Exception: When the guess is invalid.
        """
        pass

    def is_valid(self, word):
        """
        Args:
            word: A possible guess in the game.

        Returns:
            Whether the word is a valid guess.
        """
        pass

    def get_game_status(self):
        """
        Returns:
            whether the game is won, lost, or in progress.
        """
        pass

    def get_valid_guesses(self):
        """
        Returns:
            List of valid guesses for the game.
        """
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass


class Status(Enum):
    IN_PROGRESS = 1
    WON = 2
    LOST = 3
