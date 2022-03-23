import numpy as np
import time as time
import random as rand

# Global
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
MOVES = [UP, DOWN, LEFT, RIGHT]

# check board if empty
EMPTY = 0


class Game:

    def __init__(self, size, num_player, players, display=False, max_turns=100):
        self.size = size  # board size x size
        self.num_player = num_player
        self.players = players
        self.display = display
        self.max_turns = max_turns  # in case spin around

        self.turn = 0  # start turn
        self.cube_size = 1  # cube
        self.territory = [set() for _ in range(self.num_player)] ##

        # position
        self.cubes = [[((j + 1) * self.size // (2 * self.num_player), self.size // 2 + 1)
                      for i in range(self.cube_size)]
                      for j in range(self.num_player)]

        self.player_ids = [i for i in range(self.num_player)]

        # board size
        self.board = [[EMPTY] * self.size for _ in range(self.size)]
        # cube path drawing
        for i in self.player_ids:
            for tup in self.cubes[i]:
                self.board[tup[0]][tup[1]] = str(i+1) + "H"  # set Head
                self.territory[i].add(tup)                   # add in territory

    ## player have 2 parts, the territory and the cube that move to expend territory

    # get Circle with path
    def getPath(self, player_id):
        prev = {}
        
        st = self.cubes[player_id][-1]
        en = self.cubes[player_id][0]
     
        path = []

        for v in self.cubes[player_id]:
            path.append(v)
        # bfs algorithm
        queue = [st]
        check = []
        while True:
            v = queue.pop(0)
         
            flag = False
            for move in MOVES:
                ch = (v[0] + move[0], v[1] + move[1])
                prev[ch] = v
                if ch == en:
                    flag = True
                    break
                if ch in check:
                    continue
                if not(ch in self.territory[player_id]):
                    continue                
                check.append(ch)
                queue.append(ch)
            if flag:
                break
        
        while prev[en] != st:
            path.insert(0, prev[en])
            en = prev[en]
        return path

    # check v in polygon(path = Circle)
    def pointInPolygon(self, path, v):
        res = False
        end = path[-1]
        for i in range(len(path)):
            if (path[i][1] < v[1] <= end[1] or end[1] < v[1] <= path[i][1]) and (path[i][0] <= v[0] or end[0] <= v[0]):
                if path[i][0] + (v[1] - path[i][1]) / (end[1] - path[i][1]) * (end[0] - path[i][0]) < v[0]:
                    res = not res
            end = path[i]
        return res
    
    # cube movement
    @property
    def move(self):
        moves = []

        for i in self.player_ids:
            cube_i = self.cubes[i]
            move_i = self.players[i].get_move(self.board, cube_i)
            moves.append(move_i)
            movePath = (cube_i[-1][0] + move_i[0], cube_i[-1][1] + move_i[1])

            # check out of bounds
            if movePath[0] >= self.size or movePath[1] >= self.size or movePath[0] < 0 or movePath[1] < 0:
                self.player_ids.remove(i)
                break
            # update territory in board
            if cube_i[-1] in self.territory[i]:
                self.board[cube_i[-1][0]][cube_i[-1][1]] = str(i + 1) + "T"
                cube_i = [movePath, ]
            # path
            else:
                self.board[cube_i[-1][0]][cube_i[-1][1]] = str(i + 1) + "C"
                cube_i.append(movePath)
            # update i's Head in board
            self.board[movePath[0]][movePath[1]] = str(i + 1) + "H"
            self.cubes[i] = cube_i

        # update territory
        for i in self.player_ids:
            head_i = self.cubes[i][-1]
            cube_i = self.cubes[i]
            if head_i in self.territory[i]:
                if len(cube_i) > 1:
                    circle = self.getPath(i)
                    # update the state of new territory
                    for x in range(self.size):
                        for y in range(self.size):
                            if self.pointInPolygon(circle, (x, y)):
                                self.board[x][y] = str(i+1) + "T"
                    for v in self.cubes[i]:
                        self.board[v[0]][v[1]] = str(i+1) + "T"
                    self.cubes[i] = [head_i, ]
                    self.board[head_i[0]][head_i[1]] = str(i + 1) + "H"          

        # check for collisions
        for i in self.player_ids:
            head_i = self.cubes[i][-1]
            for j in range(self.num_player):
                if i == j:
                    if head_i in self.cubes[i][:-2]:
                        self.player_ids.remove(i)
                else:
                    if head_i in self.cubes[j] and j in self.player_ids:
                        self.player_ids.remove(j)
        return moves

    def play(self, display, termination=False):
        if display:
            self.display_board()
        while True:
            if termination:
                for i in self.player_ids:
                    if len(self.territory[i]) - self.turn/10 <= 0:
                        self.player_ids.remove(i)

                        return -2
            if len(self.player_ids) == 0:
                return -1
            if self.turn >= self.max_turns:
                return 0
            moves = self.move
            self.turn += 1
            if display:
                for move in moves:
                    if move == UP:
                        print("UP")
                    elif move == DOWN:
                        print("DOWN")
                    elif move == LEFT:
                        print("LEFT")
                    else:
                        print("RIGHT")
                self.display_board()

    def display_board(self):
        for i in range(self.size):
            print(" __", end="")
        print("")
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == EMPTY:
                    print("|__", end="")
                else:
                    print("|" + self.board[i][j], end="")
            print("|")
