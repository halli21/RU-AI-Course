import random
import math
 
class Sudoku:
    def __init__(self, size, hints):
        self.size = size 
        self.block_size = int(math.sqrt(size))
        self.hints = hints
        self.board = [[" " for _ in range(size)] for _ in range(size)]


    def check_valid(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == " ":
                    return False    
        return True
     

    def fillValues(self):
        complete = False
        # Fill the diagonal of block_size x block_size matrices
        self.fillDiagonal()
 
        # Fill remaining blocks
        self.fillRemaining(0, self.block_size)
 
        # Remove Randomly K digits to make game
        if self.check_valid():
            self.get_hints()
            complete = True
        else:
            #RESET
            self.board = [[" " for _ in range(self.size)] for _ in range(self.size)]

        return self.board, complete
     


    def fillDiagonal(self):
        for i in range(0, self.size, self.block_size):
            self.fillBox(i, i)
     


    def unUsedInBox(self, rowStart, colStart, num):
        for i in range(self.block_size):
            for j in range(self.block_size):
                if self.board[rowStart + i][colStart + j] == num:
                    return False
        return True
     


    def fillBox(self, row, col):
        num = 0
        for i in range(self.block_size):
            for j in range(self.block_size):
                while True:
                    num = self.randomGenerator(self.size)
                    if self.unUsedInBox(row, col, num):
                        break
                self.board[row + i][col + j] = num
     


    def randomGenerator(self, num):
        return math.floor(random.random() * num + 1)
     


    def checkIfSafe(self, i, j, num):
        return (self.unUsedInRow(i, num) and self.unUsedInCol(j, num) and self.unUsedInBox(i - i % self.block_size, j - j % self.block_size, num))
     


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
     

    
    def fillRemaining(self, i, j):
        # Check if we have reached the end of the matrix
        if i == self.size - 1 and j == self.size:
            return True
     
        # Move to the next row if we have reached the end of the current row
        if j == self.size:
            i += 1
            j = 0
     
        # Skip cells that are already filled
        if self.board[i][j] != " ":
            return self.fillRemaining(i, j + 1)
     
        # Try filling the current cell with a valid value
        for num in range(1, self.size + 1):
            if self.checkIfSafe(i, j, num):
                self.board[i][j] = num
                if self.fillRemaining(i, j + 1):
                    return True
                self.board[i][j] = " "
         
        # No valid value was found, so backtrack
        return False
 


    def get_hints(self):
        count = (self.size * self.size) - self.hints
 
        while (count != 0):
            i = self.randomGenerator(self.size) - 1
            j = self.randomGenerator(self.size) - 1
            if (self.board[i][j] != " "):
                count -= 1
                self.board[i][j] = " "
        return
    


    def printSudoku(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.board[i][j], end=" ")
            print()
 



if __name__ == "__main__":
    N = 4
    K = 2
    sudoku = Sudoku(N, K)
    sudoku.fillValues()
    sudoku.printSudoku()