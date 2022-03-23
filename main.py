from AIplayer import *
from gameBase import *

size = 8
step_size = size ** 2
num_player = 1

num_generations = 20
num_trails = 5
window_size = 6   # board size for brain size x size for head surround
hidden_size = 200  # brain size
players = [GeneticPlayer(step_size, num_generations, num_trails, window_size, hidden_size, size)
           for i in range(num_player)]
game = Game(size, num_player, players, display=True, max_turns=step_size)

game.play(True, termination=False)

