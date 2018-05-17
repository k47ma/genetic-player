A simple jumper game implemented with genetic algorithm. To start the program, run `main.py`.

This program uses `pygame` library for graphical display.

The program will use genetic algorithm to play the game and find the best solution. After each generation, it displays the best solution so far. When the game is played by the algorithm, user can press `D` to toggle the graphical display for solution (program can run faster when display is disabled).

The game can also be played independently from the algorithm by running `game.py`.
Keys:
  - `space` or `up`: jump
  - `left`: move left
  - `right`: move right
  - `R`: restart game
  - `Q` or `ESC`: quit game

TODO list:
  - tune parameters for the algorithm
  - refine the file structures
  - use multiprocessing so that the algorithm can calculate the next generation while displaying the current best solution
  - generalize `algorithm.py` for other games
