from pywordle import Wordle, Status

ANIMALS = [
    "zebra",
    "whale",
    "bison",
    "rhino",
    "otter",
    "koala",
    "horse",
    "llama",
]

wordle = Wordle(ANIMALS)
game = wordle.start_game()

game.guess("hippo")
game.guess("adieu")
game.guess("llama")
print(game)
print(game.get_status() == Status.IN_PROGRESS)

game.plot_progress()
