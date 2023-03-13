from solutions import SOLUTIONS
from pywordle import Wordle, Status


wordle = Wordle(SOLUTIONS)
games = [
    wordle.start_game(max_guesses=9),
    wordle.start_game(max_guesses=9),
    wordle.start_game(max_guesses=9),
    wordle.start_game(max_guesses=9)
]
unused_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def print_side_by_side(first_board, second_board):
    for f, s in zip(first_board.split("\n"), second_board.split("\n")):
        print(f + " " + s)


while any(map(lambda x: x.get_status() == Status.IN_PROGRESS, games)):
    guess = input("Enter your guess: ")
    if games[0].is_valid(guess):
        for x in guess:
            unused_letters = unused_letters.replace(x.upper(), "")
        for game in games:
            if game.get_status() == Status.IN_PROGRESS:
                game.guess(guess)
        print_side_by_side(str(games[0]), str(games[1]))
        print("")
        print_side_by_side(str(games[2]), str(games[3]))
        print("Unused letters: " + unused_letters)

        
    else:
        print("Guess is invalid")

if all(map(lambda x: x.get_status() == Status.WON, games)):
    print("Congrats! You won")
else:
    solutions = map(lambda x: x._solution, games)
    print("Sorry, you lost. Solutions were: " + ", ".join(solutions))
