import random

from pywordle.game import Game, WORD_LEN


class Wordle:
    """Represents a class of games with a set of possible solutions."""

    def __init__(self, solutions):
        """
        Args:
            solutions: List of possible solutions
        """
        if not all(len(s) == WORD_LEN for s in solutions):
            raise Exception("Solutions are the wrong length")

        self.solutions = list(map(lambda x: x.upper(), solutions))

    def start_game(self, hard_mode=False, solution=None, max_guesses=None):
        """
        Args:
            hard_mode: True if previous known letters must be used.
            solution: Optionally provide the solution for the game.
            max_guesses: The number of guesses allowed.

        Returns:
            A Game instance.
        """
        if not solution:
            solution = random.choice(self.solutions)
        elif solution not in self.solutions:
            raise Exception("Solution isn't a valid word")

        return Game(solution, hard_mode, max_guesses)

    def __repr__(self):
        return "Wordle({0})".format(self.solutions)
