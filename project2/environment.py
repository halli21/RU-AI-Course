import math

from state import State
#from agent import MyAgent

class Environment:
    def __init__(self, size, hints):
        self.current_state = State(size, hints)
        self.size = size
        self.block_size = int(math.sqrt(size))  # math.sqrt returns float


    def get_move(self):
        pass


    def reduce_domains(self):
        for i in range(self.size):
            for j in range(self.size):
                if len(self.current_state.domains[i][j]) == 1:
                    value = self.current_state.domains[i][j][0]
                    # reduce domain of cells in the same row
                    for k in range(self.size):
                        if k != j and value in self.current_state.domains[i][k]:
                            self.current_state.domains[i][k].remove(value)

                    # reduce domain of cells in the same column
                    for k in range(self.size):
                        if k != i and value in self.current_state.domains[k][j]:
                            self.current_state.domains[k][j].remove(value)

                    # reduce domain of cells in the same block
                    block_x = (i // self.block_size) * self.block_size
                    block_y = (j // self.block_size) * self.block_size
                    for x in range(block_x, block_x + self.block_size):
                        for y in range(block_y, block_y + self.block_size):
                            if x != i and y != j and value in self.current_state.domains[x][y]:
                                self.current_state.domains[x][y].remove(value)


 