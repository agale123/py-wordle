from words import VALID_WORDS


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

    def guess(word):
        """
        Updates the game state to reflect the guessed word.

        Args:
            word: The desired guess for the game.

        Raises:
            Exception: When the guess is invalid.
        """
        pass

    def is_valid(word):
        """
        Args:
            word: A possible guess in the game.

        Returns:
            Whether the word is a valid guess.
        """
        pass

    def get_game_status():
        """
        Returns:
            whether the game is won, lost, or in progress.
        """
        pass

    def __str__():
        pass
