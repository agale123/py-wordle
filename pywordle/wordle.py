from words import VALID_WORDS


class Wordle:
    """Represents a class of games with a set of possible solutions."""

    def __init__(self, solutions):
        """
        Args:
            solutions: List of possible solutions
        """
        self.solutions = solutions

    def start_game(hard_mode=False, solution=None):
        """
        Args:
            hard_mode: True if previous known letters must be used.
            solution: Optionally provide the solution for the game.

        Returns:
            A Game instance.
        """
        pass

    def get_valid_guesses(game):
        """
        Args:
            game: To check for valid guesses

        Returns:
            List of valid guesses for the game.
        """
        pass

    def get_possible_solutions(game):
        """
        Args:
            game: To check for valid guesses

        Returns:
            The subset of solutions are are still valid.
        """
        pass
