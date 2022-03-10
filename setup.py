from distutils.core import setup

setup(name='pywordle',
      version='1.0',
      description='Wordle Game Engine',
      packages=['pywordle'],
      requires=[
          "termcolor",
          "enum",
          "matplotlib",
      ],)
