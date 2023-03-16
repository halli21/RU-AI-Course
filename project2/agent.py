import math

from copy import deepcopy

class Search:
    def __init__(self, size, board, domains):
        self.size = size
        self.block_size = int(math.sqrt(size))
        self.board = board
        self.domains = domains

    #Called in beginning of search to reduce initial domains
    def reduce_all_domains(self):
        temp = deepcopy(self.domains)
        for x in range(self.size):
            for y in range(self.size):
                if len(temp[x][y]) == 1:
                    self.reduce_domains_value(temp[x][y][0], x, y)



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
    





# ------ BACKTRACKING (BRUTE)

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
    


# ------ BACKTRACKING WITH FORWARD CHECK

    def reduce_domains_value(self, value, ycord, xcord):
        # reduce domain of cells in the same row
        for x in range(self.size):
            if x != xcord and value in self.domains[ycord][x]:
                self.domains[ycord][x].remove(value)

        # reduce domain of cells in the same column
        for y in range(self.size):
            if y != ycord and value in self.domains[y][xcord]:
                self.domains[y][xcord].remove(value)

        block_x = (xcord // self.block_size) * self.block_size
        block_y = (ycord // self.block_size) * self.block_size
        for x in range(block_y, block_y + self.block_size):
            for y in range(block_x, block_x + self.block_size):
                if y != xcord and x != ycord and value in self.domains[x][y]:
                    self.domains[x][y].remove(value)
    

    def forward_check(self):
        for x in range(self.size):
            for y in range(self.size):
                if len(self.domains[x][y]) == 0:
                    return False
        return True
    

    def backtracking_forward_check_search(self, i = 0, j = 0):
        if i == self.size - 1 and j == self.size:
            return True
     
        if j == self.size:
            i += 1
            j = 0
     
        if self.board[i][j] != " ":
            return self.backtracking_forward_check_search(i, j + 1)
     
        for num in self.domains[i][j]:
            if self.checkIfSafe(i, j, num):
                self.board[i][j] = num
                temp = deepcopy(self.domains)
                self.reduce_domains_value(num, i, j)
                if self.forward_check():
                    if self.backtracking_forward_check_search(i, j + 1):
                        return True
                self.domains = temp
                self.board[i][j] = " "
        return False
    
