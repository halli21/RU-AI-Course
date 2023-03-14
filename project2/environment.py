import math

from state import State


class Environment:
    def __init__(self, size, inital_values):
        self.current_state = State(size)
        self.size = size
        self.block_size = int(math.sqrt(size))  # math.sqrt returns float

        self.inital_values = inital_values

    def place_number(self, state, move):
        x, y, value = move
        state.board[x][y] = value

    def update_domains(self):
        for x, y, value in self.inital_values:
            self.current_state.board[x][y] = [value]

    def reduce_domains(self):
        for i in range(self.size):
            for j in range(self.size):
                if len(self.current_state.board[i][j]) == 1:
                    value = self.current_state.board[i][j][0]
                    # reduce domain of cells in the same row
                    for k in range(self.size):
                        if k != j and value in self.current_state.board[i][k]:
                            self.current_state.board[i][k].remove(value)

                    # reduce domain of cells in the same column
                    for k in range(self.size):
                        if k != i and value in self.current_state.board[k][j]:
                            self.current_state.board[k][j].remove(value)

                    # reduce domain of cells in the same block
                    block_x = (i // self.block_size) * self.block_size
                    block_y = (j // self.block_size) * self.block_size
                    for x in range(block_x, block_x + self.block_size):
                        for y in range(block_y, block_y + self.block_size):
                            if x != i and y != j and value in self.current_state.board[x][y]:
                                self.current_state.board[x][y].remove(value)

 


initial_list = [(0, 0, 1), (1, 3, 8), (1, 4, 5), (1, 5, 9), (4, 1, 1), (5, 1, 2), (8, 2, 1)]
env = Environment(9, initial_list)

print(env.current_state)

env.update_domains()
env.reduce_domains()

print(env.current_state)