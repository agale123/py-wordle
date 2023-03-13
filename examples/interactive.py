from solutions import SOLUTIONS
from pywordle import Wordle, Status


wordle = Wordle(SOLUTIONS)
game = wordle.start_game(True)

while game.get_status() == Status.IN_PROGRESS:
    guess = input("Enter your guess: ")
    if game.is_valid(guess):
        game.guess(guess)
        print(str(game))
    else:
        print("Guess is invalid")

if game.get_status() == Status.WON:
    print("Congrats! You won")
else:
    print("Sorry, you lost. Solution was: " + game._solution)
