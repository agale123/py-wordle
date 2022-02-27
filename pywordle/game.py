from collections import defaultdict
from enum import Enum
from termcolor import colored

from pywordle.words import VALID_WORDS

MAX_GUESSES = 6
WORD_LEN = 5


class Status(Enum):
    IN_PROGRESS = 1
    WON = 2
    LOST = 3


class MovedLetter:
    """Metadata about a letter that is correct but in the wrong location."""

    def __init__(self, min_count=0, max_count=WORD_LEN, indicies=set()):
        self.min_count = min_count
        self.max_count = max_count
        self.indices = indicies

    def add(self, index):
        self.indices.add(index)

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
        self._solution = solution.upper()
        self._hard_mode = hard_mode

        # Set of guessed letters not in the solution.
        self._absent_letters = set()

        # Map from guessed letters to a list of indices.
        self._correct_letters = defaultdict(set)

        # Map from guessed letters to an object containing a set of indices
        # where the letter isn't and the minimum number of instances.
        self._moved_letters = defaultdict(
            lambda: MovedLetter(0, WORD_LEN, set()))

        self._status = Status.IN_PROGRESS
        self._guesses = []
        self._possible_solutions = VALID_WORDS

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

        if not self._status == Status.IN_PROGRESS:
            raise Exception("Game is already over")

        # Update the game state
        for i in range(WORD_LEN):
            if self._solution[i] == word[i]:
                self._correct_letters[word[i]].add(i)
            elif word[i] in self._solution:
                self._moved_letters[word[i]].add(i)
                # If we learn the maximum number of times a letter appears
                # then update the max_count
                if word.count(word[i]) > self._solution.count(word[i]):
                    self._moved_letters[word[i]].max_count = self._solution.count(
                        word[i])

                # If we learn the minimum number of times a letter appears
                # then update the min_count
                self._moved_letters[word[i]].min_count = max(
                    self._moved_letters[word[i]].min_count,
                    min(
                        word.count(word[i]),
                        self._solution.count(word[i])))
            else:
                self._absent_letters.add(word[i])

        # Check if the game is over
        self._guesses.append(word)
        if self._solution == word:
            self._status = Status.WON
        elif len(self._guesses) == MAX_GUESSES:
            self._status = Status.LOST

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

        # For hard mode check if correct letters are included
        if self._hard_mode:
            for letter, indices in self._correct_letters.items():
                for i in indices:
                    if word[i] != letter:
                        return False

        return True

    def get_status(self):
        """
        Returns:
            Whether the game is won, lost, or in progress.
        """
        return self._status

    def __str__(self):
        words = []
        for guess in self._guesses:
            word = ""
            for i in range(WORD_LEN):
                letter = guess[i]
                if self._solution[i] == letter:
                    # Exact match has a green background
                    word += colored(letter, "grey", "on_green")
                elif letter in self._solution:
                    # For inexact matches, we need to color at most the number
                    # of instances in the solution with priority given to exact
                    # matches. Steps to calculate this:
                    # 1. See if we guessed more instances of a letter than the
                    #    solution has.
                    # 2. Find if any of those guesses were an exact match and
                    #    subtract that out from the count of letters to color.
                    # 3. Start from the beginning of the word to color the
                    #    right number of inexact matches.
                    actual_count = self._solution.count(letter)
                    guessed_extra_letters = actual_count < guess.count(letter)
                    solution_indices = {i for i, c in enumerate(
                        self._solution) if c == letter}
                    guess_indices = {
                        i for i, c in enumerate(guess) if c == letter}
                    exact_match_count = len(
                        solution_indices.intersection(guess_indices))
                    guess_inexact_indices = list(
                        guess_indices.difference(solution_indices))
                    not_colored_inexact = i not in guess_inexact_indices[0:max(
                        actual_count-exact_match_count, 0)]

                    if guessed_extra_letters and not_colored_inexact:
                        word += colored(letter, "grey", "on_white")
                    else:
                        word += colored(letter, "grey", "on_yellow")
                else:
                    # Non-match has a white backgroudn
                    word += colored(letter, "grey", "on_white")
            words.append(word)
        return "\n".join(words)

    def __repr__(self):
        return "Game(\"{0}\", {1})".format(self._solution, self._hard_mode)
