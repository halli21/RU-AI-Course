import math

def initalize_board(size = 9):
    board = [[" " for _ in range(size)] for _ in range(size)]
    print(board)


class State:
    def __init__(self, size):
        self.size = size
        self.block_size = int(math.sqrt(size))  # math.sqrt returns float
        #self.board = [[" " for _ in range(size)] for _ in range(size)]
        #self.domains = [[list(range(1, size + 1)) for _ in range(size)] for _ in range(size)]

        self.board = [[list(range(1, size + 1)) for _ in range(size)] for _ in range(size)]

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
                    output += f"{edge_color}|"
                else:
                    output += f"{grid_color}|"

                if len(self.board[x][y]) != 1:
                    output += "   "
                else:
                    output += f" {grid_color}{self.board[x][y][0]} "
                if y == self.size - 1:
                    output += f"{edge_color}|\n"

        output += f"{edge_color}{plus}{dashes}" * self.size + f"{edge_color}{plus}"

        return output
