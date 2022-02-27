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
        self.solution = solution.upper()
        self.hard_mode = hard_mode

        # Set of guessed letters not in the solution.
        self._absent_letters = set()

        # Map from guessed letters to a list of indices.
        self._correct_letters = defaultdict(set)

        # Map from guessed letters to an object containing a set of indices
        # where the letter isn't and the minimum number of instances.
        self._moved_letters = defaultdict(
            lambda: MovedLetter(0, WORD_LEN, set()))

        self.status = Status.IN_PROGRESS
        self.guesses = []
        self.possible_solutions = VALID_WORDS

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
        for i in range(WORD_LEN):
            if self.solution[i] == word[i]:
                self._correct_letters[word[i]].add(i)
            elif word[i] in self.solution:
                self._moved_letters[word[i]].add(i)
                # If we learn the maximum number of times a letter appears
                # then update the max_count
                if word.count(word[i]) > self.solution.count(word[i]):
                    self._moved_letters[word[i]].max_count = self.solution.count(
                        word[i])

                # If we learn the minimum number of times a letter appears
                # then update the min_count
                self._moved_letters[word[i]].min_count = max(
                    self._moved_letters[word[i]].min_count,
                    min(
                        word.count(word[i]),
                        self.solution.count(word[i])))
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

        # For hard mode check if correct letters are included
        if self.hard_mode:
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
        return self.status

    def _is_possible(self, word):
        """
        Returns:
            Whether the word can possibly be a solution given the state. This
            is more strict than is_valid which takes into account exact match
            letters while in hard mode.
        """
        word = word.upper()

        # Check if word is in the list of valid words
        if word not in VALID_WORDS:
            return False

        # Check if word contains an absent letter
        for letter in self._absent_letters:
            if letter in word:
                return False

        # Check if word contains all correct letters
        for letter, indices in self._correct_letters.items():
            for i in indices:
                if word[i] != letter:
                    return False

        # Check if word matches
        for letter, details in self._moved_letters.items():
            letter_count = self.solution.count(letter)
            if letter_count < details.min_count or letter_count > details.max_count:
                return False
            for i in details.indices:
                if word[i] == letter:
                    return False

        return True

    def get_possible_solutions(self):
        """
        Returns:
            List of possible solutions given all information from the state.
        """

        # Cache the list of valid words, knowing that as the game progresses,
        # words can only be removed from the list
        self.possible_solutions = list(
            filter(lambda x: self._is_possible(x), self.possible_solutions))
        return self.possible_solutions

    def __str__(self):
        words = []
        for guess in self.guesses:
            word = ""
            for i in range(WORD_LEN):
                letter = guess[i]
                if self.solution[i] == letter:
                    # Exact match has a green background
                    word += colored(letter, "grey", "on_green")
                elif letter in self.solution:
                    # For inexact matches, we need to color at most the number
                    # of instances in the solution with priority given to exact
                    # matches.
                    actual_count = self.solution.count(letter)
                    guessed_extra_letters = actual_count < guess.count(letter)
                    solution_indices = {i for i, c in enumerate(
                        self.solution) if c == letter}
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
        return "Game(\"{0}\", {1})".format(self.solution, self.hard_mode)
