import math
import heapq

from copy import deepcopy



class Search:
    def __init__(self, size, board, domains):
        self.size = size
        self.block_size = int(math.sqrt(size))
        self.board = board
        self.domains = domains
        self.mrv_queue = []
        


    # ------------- HELPER FUNCITONS

    # Helper function that is called in beginning of the search to set up domains and/or other values

    def set_up_search(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] != " ":
                    reduced = self.reduce_domains_value(int(self.board[x][y]), x, y)
    
    def set_up_search_mrv(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] != " ":
                    reduced = self.reduce_domains_value_mrv(int(self.board[x][y]), x, y)
                
        

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
    



# ------------- BACKTRACKING (BRUTE)

    def backtracking_brute_search(self, i = 0, j = 0, expansions = 0):
        expansions += 1

        if i == self.size - 1 and j == self.size:
            return True, expansions
     
        if j == self.size:
            i += 1
            j = 0
     
        if self.board[i][j] != " ":
            return self.backtracking_brute_search(i, j + 1, expansions)
     
        for num in range(1, self.size + 1):
            if self.checkIfSafe(i, j, num):
                self.board[i][j] = num
                success, expansions = self.backtracking_brute_search(i, j + 1, expansions)
                if success:
                    return True, expansions
                self.board[i][j] = " "
        return False, expansions
    


# ------------- BACKTRACKING WITH FORWARD CHECK

    def reduce_domains_value(self, value, ycord, xcord):
        # reduce domain of cells in the same row
        for x in range(self.size):
            if x != xcord and value in self.domains[ycord][x]:
                if len(self.domains[ycord][x]) > 1:
                    self.domains[ycord][x].remove(value) 
                else:
                    return False

        # reduce domain of cells in the same column
        for y in range(self.size):
            if y != ycord and value in self.domains[y][xcord]:
                if len(self.domains[y][xcord]) > 1:
                    self.domains[y][xcord].remove(value)
                else:
                    return False
        
        block_x = (xcord // self.block_size) * self.block_size
        block_y = (ycord // self.block_size) * self.block_size
        for x in range(block_y, block_y + self.block_size):
            for y in range(block_x, block_x + self.block_size):
                if y != xcord and x != ycord and value in self.domains[x][y]:
                    if len(self.domains[x][y]) > 1:
                        self.domains[x][y].remove(value)
                    else:
                        return False
        return True
    


    def backtracking_forward_check_search(self, i = 0, j = 0, expansions = 0):
        expansions += 1

        if i == self.size - 1 and j == self.size:
            return True, expansions
     
        if j == self.size:
            i += 1
            j = 0
     
        if self.board[i][j] != " ":
            return self.backtracking_forward_check_search(i, j + 1, expansions)
     
        domain_list = deepcopy(self.domains[i][j])
        for num in domain_list:
            #if self.checkIfSafe(i, j, num):
            self.board[i][j] = num
            temp = deepcopy(self.domains)

            forward_check = self.reduce_domains_value(num, i, j)

            if forward_check:
                success, expansions = self.backtracking_forward_check_search(i, j + 1, expansions)
                if success:
                    return True, expansions
            self.domains = temp
            self.board[i][j] = " "

        return False, expansions
    




# ------------- MRV Heuristic implemented

    def update_mrv_value(self, old_y, old_x, new_mrv_value):
        new_tuple = (new_mrv_value, old_y, old_x)
        new_queue = []
        updated = False

        while len(self.mrv_queue) > 0:
            item = heapq.heappop(self.mrv_queue)
            if item[1] == old_y and item[2] == old_x:
                heapq.heappush(new_queue, new_tuple)
                updated = True
            else:
                heapq.heappush(new_queue, item)

        if not updated:
            heapq.heappush(new_queue, new_tuple)

        self.mrv_queue = new_queue
        heapq.heapify(self.mrv_queue)


    def reduce_domains_value_mrv(self, value, ycord, xcord):
        # reduce domain of cells in the same row
        for x in range(self.size):
            if x != xcord and value in self.domains[ycord][x]:
                if len(self.domains[ycord][x]) > 1:
                    self.domains[ycord][x].remove(value)
                    if self.board[ycord][x] == " ":
                        self.update_mrv_value(ycord, x, len(self.domains[ycord][x]))
                else:
                    return False

        # reduce domain of cells in the same column
        for y in range(self.size):
            if y != ycord and value in self.domains[y][xcord]:
                if len(self.domains[y][xcord]) > 1:
                    self.domains[y][xcord].remove(value)
                    if self.board[y][xcord] == " ":
                        self.update_mrv_value(y, xcord, len(self.domains[y][xcord]))
                else:
                    return False
        
        block_x = (xcord // self.block_size) * self.block_size
        block_y = (ycord // self.block_size) * self.block_size
        for x in range(block_y, block_y + self.block_size):
            for y in range(block_x, block_x + self.block_size):
                if y != xcord and x != ycord and value in self.domains[x][y]:
                    if len(self.domains[x][y]) > 1:
                        self.domains[x][y].remove(value)
                        if self.board[x][y] == " ":
                            self.update_mrv_value(x, y, len(self.domains[x][y]))
                    else:
                        return False
        return True
    

# ------ BACKTRACKING MRV (BRUTE)
                             
    def backtracking_brute_search_mrv(self, expansions = 0):
        expansions += 1

        if not self.mrv_queue:
            return True, expansions
        
        mrv_value, y, x = heapq.heappop(self.mrv_queue)

        domain_list = deepcopy(self.domains[y][x])

        for num in domain_list:
            self.board[y][x] = num
            temp = deepcopy(self.domains)
            forward_check = self.reduce_domains_value_mrv(num, y, x)
            success, expansions = self.backtracking_brute_search_mrv(expansions)
            if success:
                return True, expansions
            self.domains = temp
            self.board[y][x] = " "
        return False, expansions

    


# ------ BACKTRACKING WITH FORWARD CHECK MRV


    def backtracking_forward_check_search_mrv(self, expansions = 0):
        expansions += 1
        
        if not self.mrv_queue:
            return True, expansions
    
        mrv_value, y, x = heapq.heappop(self.mrv_queue)

        domain_list = deepcopy(self.domains[y][x])
    
        for num in domain_list:
            self.board[y][x] = num
            temp = deepcopy(self.domains)
            forward_check = self.reduce_domains_value_mrv(num, y, x)
            if forward_check:
                success, expansions = self.backtracking_forward_check_search_mrv(expansions)
                if success:
                    return True, expansions
            self.domains = temp
            self.board[y][x] = " "
        return False, expansions


