import math
import time

from mrv_queue import MRV_Queue
from copy import deepcopy
import random



class Search:
    def __init__(self, size, board, domains):
        self.size = size
        self.block_size = int(math.sqrt(size))
        self.board = board
        self.domains = domains
        self.mrv_queue = MRV_Queue()
        self.rand_queue = {4: [], 9: [], 16: []}

        # For testing
        self.start_time = None

        


    # ------------- HELPER FUNCTIONS

    # Helper function that is called in beginning of the search to set up domains and/or other values

    def set_up_search(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] != " ":
                    reduced = self.reduce_domains_value(int(self.board[y][x]), y, x)
    
    def set_up_search_mrv(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] != " ":
                    reduced = self.reduce_domains_value_mrv(int(self.board[y][x]), y, x)

    def set_up_search_rand(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] == " ":
                    tup = (x, y)
                    self.rand_queue[self.size].append(tup)
        
                
        
    #Functions that check if you can place a number in a specified location 

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
    
    #Backtracking brute search just goes through the grid linearly and tries every number possible from 1 to the size selected (4, 9, 16)
    def backtracking_brute_search(self, i = 0, j = 0, expansions = 0):

        elapsed_time = time.time() - self.start_time

        if elapsed_time > 29.999999:
            return True, expansions

        #if we have reached the end of the grid we return True meaning the sudoku is finished.
        if i == self.size - 1 and j == self.size:
            return True, expansions
     
        #if you reach the end of a row we go down to the next row
        if j == self.size:
            i += 1
            j = 0
     
        #If the cell is already filled we move on to the next cell
        if self.board[i][j] != " ":
            return self.backtracking_brute_search(i, j + 1, expansions)
     
        #goes through all numbers in range
        for num in range(1, self.size + 1):
            expansions += 1
            #if current num can be placed it places it and moves on to the next cell
            if self.checkIfSafe(i, j, num):
                self.board[i][j] = num
                success, expansions = self.backtracking_brute_search(i, j + 1, expansions)
                #If the recursive call returns True that means this is the right num and you dont need to backtrack
                if success:
                    return True, expansions
                #clears the cell if we have backtracked to this cell
                self.board[i][j] = " "
        #if no possible number is safe then we return False, a.k.a. we backtrack
        return False, expansions
    


# ------------- USING DOMAINS

    def reduce_domains_value(self, value, ycord, xcord):
        flag = True
        
        # reduce domain of cells in the same row
        for x in range(self.size):
            if x != xcord and value in self.domains[ycord][x]:
                if len(self.domains[ycord][x]) != 1:
                    self.domains[ycord][x].remove(value) 
                else:
                    flag = False

        # reduce domain of cells in the same column
        for y in range(self.size):
            if y != ycord and value in self.domains[y][xcord]:
                if len(self.domains[y][xcord]) != 1:
                    self.domains[y][xcord].remove(value)
                else:
                    flag = False
        
        #reduce domains of cells in the same square
        block_x = (xcord // self.block_size) * self.block_size
        block_y = (ycord // self.block_size) * self.block_size
        for y in range(block_y, block_y + self.block_size):
            for x in range(block_x, block_x + self.block_size):
                if x != xcord or y != ycord:
                    if value in self.domains[y][x]:
                        if len(self.domains[y][x]) != 1:
                            self.domains[y][x].remove(value)
                        else:
                            flag = False
        #the flag is true if everything went well, but returns false if there is some domain that will become empty if the value is removed
        return flag
    



    def backtracking_search(self, i = 0, j = 0, expansions = 0):

        elapsed_time = time.time() - self.start_time

        if elapsed_time > 29.999999:
            return True, expansions
        

        #if we have reached the end of the grid we return True meaning the sudoku is finished.
        if i == self.size - 1 and j == self.size:
            return True, expansions
     
        #if you reach the end of a row we go down to the next row
        if j == self.size:
            i += 1
            j = 0
     
        #If the cell is already filled we move on to the next cell
        if self.board[i][j] != " ":
            return self.backtracking_search(i, j + 1, expansions)
     
        #Take a copy of the domains list for this cell so it doesnt change in the middle of the for loop
        domain_list = deepcopy(self.domains[i][j])

        #Go through all the numbers in the doamin for this cell.
        for num in domain_list:
            if self.checkIfSafe(i, j, num):
                expansions += 1
                self.board[i][j] = num
                #take a copy of the entire domains list to use if we have to backtrack
                temp = deepcopy(self.domains)

                #remove the current num from the appropriate cells' domains
                forward_check = self.reduce_domains_value(num, i, j)

                success, expansions = self.backtracking_search(i, j + 1, expansions)
                #If the recursive call returns True that means this is the right num and you dont need to backtrack
                if success:
                    return True, expansions
                
                #clears the cell and fixes the domains if we have backtracked to this cell
                self.domains = temp
                self.board[i][j] = " "

        #if no possible number is safe then we return False, a.k.a. we backtrack
        return False, expansions
    


    def backtracking_forward_check_search(self, i = 0, j = 0, expansions = 0):

        elapsed_time = time.time() - self.start_time

        if elapsed_time > 29.999999:
            return True, expansions

        #if we have reached the end of the grid we return True meaning the sudoku is finished.
        if i == self.size - 1 and j == self.size:
            return True, expansions

        #if you reach the end of a row we go down to the next row
        if j == self.size:
            i += 1
            j = 0
     
        #If the cell is already filled we move on to the next cell
        if self.board[i][j] != " ":
            return self.backtracking_forward_check_search(i, j + 1, expansions)
     
        #Take a copy of the domains list for this cell so it doesnt change in the middle of the for loop
        domain_list = deepcopy(self.domains[i][j])

        #Go through all the numbers in the doamin for this cell.
        for num in domain_list:
            expansions += 1
            self.board[i][j] = num
            #take a copy of the entire domains list to use if we have to backtrack
            temp = deepcopy(self.domains)

            forward_check = self.reduce_domains_value(num, i, j)

            #if the forward check (which is the flag in the reduce_domains_value function) returns True it means the forward check found an empty domain and therefore knows that this number is not correct
            if forward_check:
                success, expansions = self.backtracking_forward_check_search(i, j + 1, expansions)
                #If the recursive call returns True that means this is the right num and you dont need to backtrack
                if success:
                    return True, expansions
                
            #clears the cell and fixes the domains if we have backtracked to this cell
            self.domains = temp
            self.board[i][j] = " "

        #if no possible number is safe then we return False, a.k.a. we backtrack
        return False, expansions
    






# ------------- MRV Heuristic implemented


    def reduce_domains_value_mrv(self, value, ycord, xcord):
        flag = True
        
        # reduce domain of cells in the same row
        for x in range(self.size):
            if x != xcord and value in self.domains[ycord][x]:
                if len(self.domains[ycord][x]) != 1:
                    self.domains[ycord][x].remove(value)
                    if self.board[ycord][x] == " ":
                        self.mrv_queue.update_node(ycord, x, len(self.domains[ycord][x]))
                else:
                    flag = False

        # reduce domain of cells in the same column
        for y in range(self.size):
            if y != ycord and value in self.domains[y][xcord]:
                if len(self.domains[y][xcord]) != 1:
                    self.domains[y][xcord].remove(value)
                    if self.board[y][xcord] == " ":
                        self.mrv_queue.update_node(y, xcord, len(self.domains[y][xcord]))
                else:
                    flag = False
        
        # reduce domains of cells in the same square
        block_x = (xcord // self.block_size) * self.block_size
        block_y = (ycord // self.block_size) * self.block_size
        for x in range(block_y, block_y + self.block_size):
            for y in range(block_x, block_x + self.block_size):
                if y != xcord or x != ycord:
                    if value in self.domains[x][y]:
                        if len(self.domains[x][y]) != 1:
                            self.domains[x][y].remove(value)
                            if self.board[x][y] == " ":
                                self.mrv_queue.update_node(x, y, len(self.domains[x][y]))
                        else:
                            flag = False

        for y in range(block_y, block_y + self.block_size):
            for x in range(block_x, block_x + self.block_size):
                if x != xcord and y != ycord and value in self.domains[y][x]:
                    if len(self.domains[y][x]) > 1:
                        self.domains[y][x].remove(value)
                        if self.board[y][x] == " ":
                            self.mrv_queue.update_node(y, x, len(self.domains[y][x]))
                    else:
                        flag = False
        #the flag is true if everything went well, but returns false if there is some domain that will become empty if the value is removed
        return flag
    

# ------ BACKTRACKING MRV
                             
    def backtracking_search_mrv(self, expansions = 0):
        elapsed_time = time.time() - self.start_time

        if elapsed_time > 29.999999:
            return True, expansions

    #Instead of going linearly through the sudoku, this uses an mrv_queue to pick which cell to fill next 
    def backtracking_search_mrv(self, expansions = 0):
        #if mrv queue is empty then the sudoku is finsished
        if self.mrv_queue.size == 0:
            return True, expansions
        
        #take the first node from the queue
        node = self.mrv_queue.pop()

        #Take a copy of the domains list for this cell so it doesnt change in the middle of the for loop
        domain_list = deepcopy(self.domains[node.ycord][node.xcord])

        #Go through all the numbers in the doamin for this cell.
        for num in domain_list:
            if self.checkIfSafe(node.ycord, node.xcord, num):
                expansions += 1
                self.board[node.ycord][node.xcord] = num

                #take a copy of the entire domains list and the mrv queue to use if we have to backtrack
                temp = deepcopy(self.domains)
                temp_mrv = deepcopy(self.mrv_queue)

                forward_check = self.reduce_domains_value_mrv(num, node.ycord, node.xcord)
                success, expansions = self.backtracking_search_mrv(expansions)
                #If the recursive call returns True that means this is the right num and you dont need to backtrack
                if success:
                    return True, expansions
                
                #clears the cell, fixes the domains and fixes the mrv_queue if we have backtracked to this cell
                self.mrv_queue = temp_mrv
                self.domains = temp
                self.board[node.ycord][node.xcord] = " "
        #if no possible number is safe then we return False, a.k.a. we backtrack
        return False, expansions

    


# ------ BACKTRACKING WITH FORWARD CHECK MRV


    def backtracking_forward_check_search_mrv(self, expansions = 0):

        elapsed_time = time.time() - self.start_time

        if elapsed_time > 29.999999:
            return True, expansions

        #if mrv queue is empty then the sudoku is finsished
        if self.mrv_queue.size == 0:
            return True, expansions
        
        #take the first node from the queue
        node = self.mrv_queue.pop()

        #Take a copy of the domains list for this cell so it doesnt change in the middle of the for loop
        domain_list = deepcopy(self.domains[node.ycord][node.xcord])
    
        #Go through all the numbers in the doamin for this cell.
        for num in domain_list:
            expansions += 1
            self.board[node.ycord][node.xcord] = num

            #take a copy of the entire domains list and the mrv queue to use if we have to backtrack
            temp = deepcopy(self.domains)
            temp_mrv = deepcopy(self.mrv_queue)

            forward_check = self.reduce_domains_value_mrv(num, node.ycord, node.xcord)
            #if the forward check (which is the flag in the reduce_domains_value function) returns True it means the forward check found an empty domain and therefore knows that this number is not correct
            if forward_check:
                success, expansions = self.backtracking_forward_check_search_mrv(expansions)
                #If the recursive call returns True that means this is the right num and you dont need to backtrack
                if success:
                    return True, expansions
                
            #clears the cell, fixes the domains and fixes the mrv_queue if we have backtracked to this cell
            self.domains = temp
            self.mrv_queue = temp_mrv
            self.board[node.ycord][node.xcord] = " "
        #if no possible number is safe then we return False, a.k.a. we backtrack
        return False, expansions





# ------------- Degree Heuristic added on MRV


    def get_degree(self, ycord, xcord):
        degree = 0
        
        # adds the degree of the row to the overall degree
        for x in range(self.size):
            if x == xcord:
                continue                
            if self.board[ycord][x] == " ":
                degree += 1

        # adds the degree of the column to the overall degree
        for y in range(self.size):
            if y == ycord:
                continue
            if self.board[y][xcord] == " ":
                degree += 1

        # adds the degree of the square to the overall degree
        block_x = (xcord // self.block_size) * self.block_size
        block_y = (ycord // self.block_size) * self.block_size
        for y in range(block_y, block_y + self.block_size):
            for x in range(block_x, block_x + self.block_size):         
                if x != xcord or y != ycord:
                    if self.board[y][x] == " ":
                        degree += 1

        return degree


    # finds the next cell in the mrv and degree combo. Takes the first node in the queue, then all the other nodes with the same doamin length. Then it finds which of those has the biggest degree
    def get_next_square(self):
        node_lis = []

        node = self.mrv_queue.pop()
        node_lis.append(node)

        while self.mrv_queue.size != 0:
            next_node = self.mrv_queue.pop()
            node_lis.append(next_node)
            if node.value != next_node.value:
                break
                    
       
        if len(node_lis) > 1:
            # gets and removes the last value in lists
            last_node = node_lis.pop() # the last value will not have the lowest mrv value so we remove it
            self.mrv_queue.insert(last_node)

        max_degree = 0
        max_index = 0

        for index, node in enumerate(node_lis):
            degree = self.get_degree(node.ycord, node.xcord)
            if max_degree < degree: 
                max_degree = degree
                max_index = index

        degree_node = node_lis.pop(max_index)

        for node in node_lis:
            self.mrv_queue.insert(node)

        return degree_node




# ------ BACKTRACKING MRV & DEGREE
                             
    def backtracking_search_mrv_deg(self, expansions = 0):

        elapsed_time = time.time() - self.start_time

        if elapsed_time > 29.999999:
            return True, expansions

        #if mrv queue is empty then the sudoku is finsished
        if self.mrv_queue.size == 0:
            return True, expansions
        
        #take the first node from the queue
        node = self.get_next_square()

        #Take a copy of the domains list for this cell so it doesnt change in the middle of the for loop
        domain_list = deepcopy(self.domains[node.ycord][node.xcord])


        #Go through all the numbers in the doamin for this cell.
        for num in domain_list:
            if self.checkIfSafe(node.ycord, node.xcord, num):
                expansions += 1
                self.board[node.ycord][node.xcord] = num

                #take a copy of the entire domains list and the mrv queue to use if we have to backtrack
                temp = deepcopy(self.domains)
                temp_mrv = deepcopy(self.mrv_queue)

                forward_check = self.reduce_domains_value_mrv(num, node.ycord, node.xcord)
                success, expansions = self.backtracking_search_mrv_deg(expansions)
                #If the recursive call returns True that means this is the right num and you dont need to backtrack
                if success:
                    return True, expansions
                
                # if backtracked we empty the cell, fix domains, fix the queue
                self.domains = temp
                self.mrv_queue = temp_mrv
            
                self.board[node.ycord][node.xcord] = " "
        #if no possible number is safe then we return False, a.k.a. we backtrack
        return False, expansions
            






    def backtracking_forward_check_search_mrv_deg(self, expansions = 0):

            elapsed_time = time.time() - self.start_time

            if elapsed_time > 29.999999:
                return True, expansions

            if self.mrv_queue.size == 0:
                return True, expansions
            
            node = self.get_next_square()

            domain_list = deepcopy(self.domains[node.ycord][node.xcord])

        
            for num in domain_list:
                
                expansions += 1
                self.board[node.ycord][node.xcord] = num
                temp = deepcopy(self.domains)
                temp_mrv = deepcopy(self.mrv_queue)
                forward_check = self.reduce_domains_value_mrv(num, node.ycord, node.xcord)
                if forward_check:
                    success, expansions = self.backtracking_forward_check_search_mrv_deg(expansions)
                    if success:
                        return True, expansions
                self.domains = temp
                self.mrv_queue = temp_mrv
            
                self.board[node.ycord][node.xcord] = " "
            
            return False, expansions
            
        
        
# ------ BACKTRACKING RANDOM

    def backtracking_random(self, expansions = 0):

        elapsed_time = time.time() - self.start_time

        if elapsed_time > 29.999999:
            return True, expansions
        
        # helper values that make it more clear what is being called 
        x = 0
        y = 1

        #checks if the rand_queue is empty. If it is empty it sees if there are any cells that it missed and add them to the queue. If its still empty after trying to fill i the sudoku is finished
        if len(self.rand_queue[self.size]) == 0:
            self.set_up_search_rand()
            if len(self.rand_queue[self.size]) == 0:
                return True, expansions
        
        # finds a random cell to use
        length = len(self.rand_queue[self.size])
        rand_num = random.randrange(0, length)
        tup = self.rand_queue[self.size].pop(rand_num)

        # takes a copy of the domain list for that cell so it doesnt change in the middle of the for loop
        domain_list = deepcopy(self.domains[tup[y]][tup[x]])

        # Goes through every number in the domain
        for num in domain_list:
            if self.checkIfSafe(tup[y], tup[x], num):
                expansions += 1
                self.board[tup[y]][tup[x]] = num

                #take a copy of the entire domains list in case of a backtrack
                temp = deepcopy(self.domains)
                forward_check = self.reduce_domains_value(num, tup[y], tup[x])
                success, expansions = self.backtracking_random(expansions)

                #If the recursive call returns True that means this is the right num and you dont need to backtrack
                if success:
                    return True, expansions
                
                #if we backtrack to this then we empty the cell and fix the domains
                self.domains = temp
                self.board[tup[y]][tup[x]] = " "
        #if no possible number is safe then we return False, a.k.a. we backtrack
        return False, expansions
