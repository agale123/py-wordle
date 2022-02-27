# Design Specification

## Introduction

This project can be thought of as building a game engine for Wordle.

Goals:
* Generate Wordle games from a list of possible solutions
* Make guesses for a game and receive feedback
* Get feedback on whether guesses are valid
* Handle hard mode where known letters must be used

Non-Goals:
* Implement a fully interactive CLI
* Implement a solver

## Design Overview

There will be two main components to this library: the `Wordle` and `Game`
classes. The `Wordle` class will encapsulate a set of possible solutions that
can be used to create individual games. The `Game` class is an individual
instance of the word game with a specific solution. You interact with the
`Game` class to make guesses and receive feedback on how close you are to the
solution.

## Detailed Design

### Wordle

This class represents a class of games with a set of possible solutions.
Individual game boards can be generated and information about valid guesses
can be queried. This is a general purpose module because it has use cases for
creating games which is helpful for playing an interactive game as well as
methods for calculating valid solutions or guesses which might be helpful
when developing a solver.

Inputs:
* `solutions`: a list of 5-character strings

Methods:
* `start_game(hard_mode=False, solution=None)`: picks a random word from
  `solutions` if a solution isn't provided and returns a `Game`
  instance

### Game

This class represents an individual game with a specific solution. Guesses can
be made against the solution. The board can be printed at any time in order to
see all previous guesses. It would be possible to have guess return results of
just the most recent guess, but it is typically easiest to visualize all
previous guesses at once and this logic will be carefully printed in the string
representation of the class.

Data
* `valid_words`: a list of all valid 5-letter words

Inputs:
* `solution`: the final word
* `hard_mode`: whether hard mode is enabled

Methods:
* `guess(word)`: updates the game state to reflect the results of making the
  guess. Throws an error if the guess is invalid
* `is_valid(word)`: returns whether this is a valid guess given the game state
* `get_status()`: returns whether the game is won, lost or in progress
* `__str__()`: pretty prints the game board which includes all the guessed
  letters and colors representing if they were correct

## Testing Strategy

The examples directory contains sample uses of the library and can be thought
of as one-shot tests. Both the `Wordle` and `Game` classes will have both
smoke and unit tests. The smoke tests will ensure that expected input does
not throw errors. The unit tests will need to handle a variety of normal and
edge cases:

Normal cases:
* Wordle
  * Can create a game
  * Can create a hard mode game
* Game
  * Guessing a word with correct letters
  * Guessing a word with letters in the wrong location
  * Guessing the correct solution
  * Running out of guesses without getting the solution
  * Checking if a guess is valid

Edge cases:
* Wordle
  * Throws error when words are incorrect length
  * Handles possible solutions that aren't in valid word list
* Game
  * Guessing an invalid word
  * Guess that violates hard mode rules
  * Guessing words with duplicates of a letter
  * Does not accept guesses once the game is won