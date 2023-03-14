import math

from generator import Sudoku

class State():
    def __init__(self, size, hints):
        self.size = size
        self.block_size = int(math.sqrt(size))  # math.sqrt returns float
      
        self.domains = [[list(range(1, size + 1)) for _ in range(size)] for _ in range(size)]

        self.generator = Sudoku(size, hints)
        self.board = self.generator.fillValues()
        self.update_domain()

    def update_domain(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] != " ":
                    self.domains[x][y] = [self.board[x][y]]

    def get_value(self, value):
        value_dict = {10 : "A", 11 : "B", 12 : "C", 13 : "D", 14 : "E", 15 : "F", 16 : "G"}

        if (value == " "):
            return value
        
        elif (int(value) > 9):
            return value_dict[value]

        return value


    def __str__(self):
        output = ""

        edge_color = "\033[34m"  # blue
        grid_color = "\033[32m"  # green

        plus = "+"
        dashes = "---"
        
        for x in range(self.size):
            if x % self.block_size == 0 or x == 0:
                output += f"{edge_color}{plus}{dashes}" * self.size + f"{edge_color}{plus}\n"
            else:
                for i in range(int(self.block_size)):
                    output += f"{edge_color}{plus}{grid_color}{dashes}" + f"{grid_color}{plus}{dashes}" * (self.block_size - 1)
                    if i == self.block_size - 1:
                        output += f"{edge_color}{plus}\n"

            for y in range(self.size):
                if y % self.block_size == 0 or y == 0:
                    output += f"{edge_color}| {grid_color}{self.get_value(self.board[x][y])} "
                else:
                    output += f"{grid_color}| {grid_color}{self.get_value(self.board[x][y])} "

                if y == self.size - 1:
                    output += f"{edge_color}|\n"

        output += f"{edge_color}{plus}{dashes}" * self.size + f"{edge_color}{plus}"

        return output
