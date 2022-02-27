# Functional Specification

## Background

Wordle is a word guessing game developed by Josh Wardle which gained
substantial popularity in January 2022. The goal is to guess the hidden word.
With each guess you learn whether each letter was in the right location, in
the wrong location, or not in the word. This game has led to a series of 
spinoffs that used themed sets of words or modified gameplay like having to
guess multiple words at the same time. The game was purchased by The New York
Times which now runs the official game. 

## Data

The main pieces of data used by this application are the lists of valid guesses
and possible solutions. In the original game, any five letter word was a valid
guess. When The New York Times took over the game, they removed certain slurs
from the set of valid guesses. The set of possible solutions for the original
game was a subset of valid words that are more common. In spinoff games, this
set of words might be following a specific theme.

## Users

* Word game enthusiats
* Game developers

## Use Cases

1. Developer wants to build Wordle with custom words
   1. User passes in a list of custom words
   2. User creates a game
   3. User guesses words
   4. Program responds with feedback on which letters are correct
2. Developer wants to build a Wordle solver
   1. User creates game instances to represent all possible solutions
   2. User tests different guesses
   3. Program responds with feedback on which letters are correct
3. Word game enthusiat wants to play unlimited Wordle
   1. User passes in the list of possible solutions from the official Wordle
   2. User creates a game
   3. User guesses words
   4. Program responds with feedback on which letters are correct 