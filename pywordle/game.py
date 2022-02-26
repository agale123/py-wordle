from collections import defaultdict
from email.policy import default
from words import VALID_WORDS
from enum import Enum

MAX_GUESSES = 6


class Status(Enum):
    IN_PROGRESS = 1
    WON = 2
    LOST = 3


class MovedLetter:
    """Metadata about a letter that is correct but in the wrong location."""

    def __init__(self, min_count=0, max_count=5, indicies=set()):
        self.min_count = min_count
        self.max_count = max_count
        self.indices = indicies

    def add(self, index):
        # TODO(agale): Make this more robust
        if index not in self.indices:
            self.indices.add(index)
            self.min_count += 1

    def __eq__(self, other):
        return (
            self.min_count == other.min_count
            and self.max_count == other.max_count
            and self.indices == other.indices)

    def __repr__(self):
        return "MovedLetter({0}, {1}, {2})".format(
            self.min_count, self.max_count, self.indices)


class Game:
    """Represents an individual game of Wordle."""

    def __init__(self, solution, hard_mode):
        """
        Args:
            solution: The answer for the game.
            hard_mode: True if previous known letters must be used.
        """
        self.solution = solution.upper()
        self.hard_mode = hard_mode

        # Set of guessed letters not in the solution.
        self._absent_letters = set()

        # Map from guessed letters to a list of indices.
        self._correct_letters = defaultdict(set)

        # Map from guessed letters to an object containing a set of indices
        # where the letter isn't and the minimum number of instances.
        self._moved_letters = defaultdict(lambda: MovedLetter(0, 5, set()))

        self.status = Status.IN_PROGRESS
        self.guesses = []

    def guess(self, word):
        """
        Updates the game state to reflect the guessed word.

        Args:
            word: The desired guess for the game.

        Raises:
            Exception: When the guess is invalid.
        """
        word = word.upper()

        if not self.is_valid(word):
            raise Exception("Invalid guess")

        if not self.status == Status.IN_PROGRESS:
            raise Exception("Game is already over")

        # Update the game state
        for i in range(5):
            if self.solution[i] == word[i]:
                self._correct_letters[word[i]].add(i)
            elif word[i] in self.solution:
                # TODO(agale): Handle multiple letters better
                self._moved_letters[word[i]].add(i)
            else:
                self._absent_letters.add(word[i])

        # Check if the game is over
        self.guesses.append(word)
        if self.solution == word:
            self.status = Status.WON
        elif len(self.guesses) == MAX_GUESSES:
            self.status = Status.LOST

    def is_valid(self, word):
        """
        Args:
            word: A possible guess in the game.

        Returns:
            Whether the word is a valid guess.
        """
        word = word.upper()

        # Check if word is in the list of valid words
        if word not in VALID_WORDS:
            return False

        # TODO(agale): Check if hard mode conditions are satisfied

        return True

    def get_game_status(self):
        """
        Returns:
            whether the game is won, lost, or in progress.
        """
        return self.status

    def get_valid_guesses(self):
        """
        Returns:
            List of valid guesses for the game.
        """
        pass

    def __str__(self):
        return "\n".join(self.guesses)

    def __repr__(self):
        return "Game(\"{0}\", {1})".format(self.solution, self.hard_mode)
