from collections import defaultdict
from enum import Enum
import matplotlib.pyplot as plt
from termcolor import colored

from pywordle.words import VALID_WORDS

MAX_GUESSES = 6
WORD_LEN = 5


class Status(Enum):
    IN_PROGRESS = 1
    WON = 2
    LOST = 3


class Game:
    """Represents an individual game of Wordle."""

    def __init__(self, solution, hard_mode, max_guesses):
        """
        Args:
            solution: The answer for the game.
            hard_mode: True if previous known letters must be used.
            max_guesses: The number of guesses allowed.
        """
        self._solution = solution.upper()
        self._hard_mode = hard_mode

        # Map from guessed letters to a list of indices.
        self._correct_letters = defaultdict(set)

        self._status = Status.IN_PROGRESS
        self._guesses = []
        self._max_guesses = max_guesses or MAX_GUESSES

        # Keep track of how many words are left for plotting progress.
        self.words_left = VALID_WORDS
        self.progress = [len(self.words_left)]

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
        absent_letters = set()
        moved_letters = defaultdict(set)
        for i in range(WORD_LEN):
            if self._solution[i] == word[i]:
                self._correct_letters[word[i]].add(i)
            elif word[i] in self._solution:
                moved_letters[word[i]].add(i)
            else:
                absent_letters.add(word[i])

        def is_match(word):
            """
            Returns True if word might be the solution, given available info.
            """
            for i in range(WORD_LEN):
                for letter, indices in self._correct_letters.items():
                    for i in indices:
                        if word[i] != letter:
                            return False
                for letter, indices in moved_letters.items():
                    for i in indices:
                        if word[i] == letter:
                            return False
                for letter in absent_letters:
                    if letter in word:
                        return False
            return True

        self.words_left = list(filter(is_match, self.words_left))
        self.progress.append(len(self.words_left))

        # Check if the game is over
        self._guesses.append(word)
        if self._solution == word:
            self._status = Status.WON
        elif len(self._guesses) == self._max_guesses:
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

    def plot_progress(self):
        """
        Plots how the list of possible solutions has been narrowed down with
        each successive guess.
        """
        fig = plt.figure()
        plt.plot(self.progress)
        fig.gca().xaxis.get_major_locator().set_params(integer=True)
        plt.xlabel("Guess")
        plt.ylabel("Words Remaining")
        fig.savefig("progress.png")

        return self.progress

    def _color_guess(self, guess):
        """
        Returns:
            A color-coded representation of the guessed word. A letter is white
            if it is not in the final word, yellow if it is in the wrong
            location, and green if it is in the correct location.
        """
        word = ""
        for i in range(WORD_LEN):
            letter = guess[i]
            if self._solution[i] == letter:
                # Exact match has a green background.
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
                guess_indices = {i for i, c in enumerate(guess) if c == letter}
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
                # Non-match has a white background.
                word += colored(letter, "grey", "on_white")
        return word

    def __str__(self):
        """
        Returns:
            A string represention of the full game.
        """
        words = []
        for guess in self._guesses:
            words.append(self._color_guess(guess))

        for i in range(self._max_guesses - len(self._guesses)):
            words.append(self._color_guess("     "))
        return "\n".join(words)

    def __repr__(self):
        return "Game(\"{0}\", {1})".format(self._solution, self._hard_mode)
