class Wordle:
    """Represents a class of games with a set of possible solutions."""

    def __init__(self, solutions):
        """
        Args:
            solutions: List of possible solutions
        """
        self.solutions = solutions

    def start_game(self, hard_mode=False, solution=None):
        """
        Args:
            hard_mode: True if previous known letters must be used.
            solution: Optionally provide the solution for the game.

        Returns:
            A Game instance.
        """
        pass

    def __repr__(self):
        pass
