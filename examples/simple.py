from pywordle import Wordle, Game, Status

animals = [
    "zebra",
    "whale",
    "bison",
    "rhino",
    "otter",
    "koala",
    "horse",
    "llama",
]

wordle = Wordle(animals)
game = wordle.start_game()

game.guess("hippo")
game.guess("adieu")
game.guess("llama")
print(game)
print(game.get_status())