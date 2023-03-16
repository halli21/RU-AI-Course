import math

class Search:
    def __init__(self, size, board, domains):
        self.size = size
        self.block_size = int(math.sqrt(size))
        self.board = board
        self.domains = domains

    def get_move(self):
        pass
        

    def checkIfSafe(self, i, j, num):
        return (self.unUsedInRow(i, num) and self.unUsedInCol(j, num) and self.unUsedInBox(i - i % self.block_size, j - j % self.block_size, num))
    

    def unUsedInBox(self, rowStart, colStart, num):
        for i in range(self.block_size):
            for j in range(self.block_size):
                if self.board[rowStart + i][colStart + j] == num:
                    return False
        return True
    
    def unUsedInRow(self, i, num):
        for j in range(self.size):
            if self.board[i][j] == num:
                return False
        return True
     
    def unUsedInCol(self, j, num):
        for i in range(self.size):
            if self.board[i][j] == num:
                return False
        return True


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



    def backtracking_brute_search(self, i = 0, j = 0):
        if i == self.size - 1 and j == self.size:
            return True
     
        if j == self.size:
            i += 1
            j = 0
     
        if self.board[i][j] != " ":
            return self.backtracking_brute_search(i, j + 1)
     
        for num in range(1, self.size + 1):
            if self.checkIfSafe(i, j, num):
                self.board[i][j] = num
                if self.backtracking_brute_search(i, j + 1):
                    return True
                self.board[i][j] = " "
        return False
    

    def backtracking_forward_check_search(self, i = 0, j = 0):
        if i == self.size - 1 and j == self.size:
            return True
     
        if j == self.size:
            i += 1
            j = 0
     
        if self.board[i][j] != " ":
            return self.backtracking_forward_check_search(i, j + 1)
     
        for num in range(1, self.size + 1):
            if self.checkIfSafe(i, j, num):
                self.board[i][j] = num
                if self.backtracking_forward_check_search(i, j + 1):
                    return True
                self.board[i][j] = " "
        return False