# pywordle

Game Engine for the popular Wordle game.

## Installing the package

To install the package, run

```
python setup.py install
```

## Usage

This package provides two classes: `Wordle` and `Game`. The `Wordle` class
allows you to provide a set of possible solutions from which a game can be
created. The `Game` class represents a single game with a specific solution.
You are allowed six guesses to solve the game. Here is a quick example of
how you might interact with the game:

```py
wordle = Wordle(WORD_LIST)
game = wordle.create_game()
game.guess("SPILL")
print(str(game))
```

## Package structure

<pre>
py-wordle
├── LICENSE
├── README.md
├── TODO.md
├── docs
│   ├── design-spec.md
│   └── functional-spec.md
├── examples
│   ├── interactive.py
│   ├── simple.py
│   └── solutions.py
├── pywordle
│   ├── __init__.py
│   ├── game.py
│   ├── test_game.py
│   ├── test_wordle.py
│   ├── wordle.py
│   └── words.py
└── setup.py
</pre>
