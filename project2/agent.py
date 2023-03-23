import math
import heapq

from mrv_queue import MRV_Queue, MRV_Node
from copy import deepcopy



class Search:
    def __init__(self, size, board, domains):
        self.size = size
        self.block_size = int(math.sqrt(size))
        self.board = board
        self.domains = domains
        self.mrv_queue = MRV_Queue()
        


    # ------------- HELPER FUNCTIONS

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
        if i == self.size - 1 and j == self.size:
            return True, expansions
     
        if j == self.size:
            i += 1
            j = 0
     
        if self.board[i][j] != " ":
            return self.backtracking_brute_search(i, j + 1, expansions)
     
        for num in range(1, self.size + 1):
            expansions += 1
            if self.checkIfSafe(i, j, num):
                self.board[i][j] = num
                success, expansions = self.backtracking_brute_search(i, j + 1, expansions)
                if success:
                    return True, expansions
                self.board[i][j] = " "
        return False, expansions
    


# ------------- USING DOMAINS

    def reduce_domains_value(self, value, ycord, xcord):
        flag = True
        
        # reduce domain of cells in the same row
        for x in range(self.size):
            if x != xcord and value in self.domains[ycord][x]:
                if len(self.domains[ycord][x]) > 1:
                    self.domains[ycord][x].remove(value) 
                else:
                    flag = False

        # reduce domain of cells in the same column
        for y in range(self.size):
            if y != ycord and value in self.domains[y][xcord]:
                if len(self.domains[y][xcord]) > 1:
                    self.domains[y][xcord].remove(value)
                else:
                    flag = False
        
        block_x = (xcord // self.block_size) * self.block_size
        block_y = (ycord // self.block_size) * self.block_size
        for x in range(block_y, block_y + self.block_size):
            for y in range(block_x, block_x + self.block_size):
                if y != xcord and x != ycord and value in self.domains[x][y]:
                    if len(self.domains[x][y]) > 1:
                        self.domains[x][y].remove(value)
                    else:
                        flag = False
        return flag
    



    def backtracking_search(self, i = 0, j = 0, expansions = 0):

        if i == self.size - 1 and j == self.size:
            return True, expansions
     
        if j == self.size:
            i += 1
            j = 0
     
        if self.board[i][j] != " ":
            return self.backtracking_search(i, j + 1, expansions)
     
        domain_list = deepcopy(self.domains[i][j])
        for num in domain_list:
            if self.checkIfSafe(i, j, num):
                expansions += 1
                self.board[i][j] = num
                temp = deepcopy(self.domains)

                forward_check = self.reduce_domains_value(num, i, j)

                success, expansions = self.backtracking_search(i, j + 1, expansions)
                if success:
                    return True, expansions
                self.domains = temp
                self.board[i][j] = " "

        return False, expansions
    


    def backtracking_forward_check_search(self, i = 0, j = 0, expansions = 0):

        if i == self.size - 1 and j == self.size:
            return True, expansions
     
        if j == self.size:
            i += 1
            j = 0
     
        if self.board[i][j] != " ":
            return self.backtracking_forward_check_search(i, j + 1, expansions)
     
        domain_list = deepcopy(self.domains[i][j])
        for num in domain_list:
            expansions += 1
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

    """
    def update_mrv_value(self, old_y, old_x, new_mrv_value):
        node = MRV_Node(new_mrv_value, old_y, old_x)
        new_queue = []
        updated = False

        while len(self.mrv_queue) > 0:
            item = heapq.heappop(self.mrv_queue)
            if item[1] == old_y and item[2] == old_x:
                heapq.heappush(new_queue, node)
                updated = True
            else:
                heapq.heappush(new_queue, item)

        if not updated:
            heapq.heappush(new_queue, node)

        self.mrv_queue = new_queue
        heapq.heapify(self.mrv_queue)
    """


    def reduce_domains_value_mrv(self, value, ycord, xcord):
        flag = True
        
        # reduce domain of cells in the same row
        for x in range(self.size):
            if x != xcord and value in self.domains[ycord][x]:
                if len(self.domains[ycord][x]) > 1:
                    self.domains[ycord][x].remove(value)
                    if self.board[ycord][x] == " ":
                        self.mrv_queue.update_node(ycord, x, len(self.domains[ycord][x]))
                else:
                    flag = False

        # reduce domain of cells in the same column
        for y in range(self.size):
            if y != ycord and value in self.domains[y][xcord]:
                if len(self.domains[y][xcord]) > 1:
                    self.domains[y][xcord].remove(value)
                    if self.board[y][xcord] == " ":
                        self.mrv_queue.update_node(y, xcord, len(self.domains[y][xcord]))
                else:
                    flag = False
        
        block_x = (xcord // self.block_size) * self.block_size
        block_y = (ycord // self.block_size) * self.block_size
        for x in range(block_y, block_y + self.block_size):
            for y in range(block_x, block_x + self.block_size):
                if y != xcord and x != ycord and value in self.domains[x][y]:
                    if len(self.domains[x][y]) > 1:
                        self.domains[x][y].remove(value)
                        if self.board[x][y] == " ":
                            self.mrv_queue.update_node(x, y, len(self.domains[x][y]))
                    else:
                        flag = False
        return flag
    

# ------ BACKTRACKING MRV
                             
    def backtracking_search_mrv(self, expansions = 0):

        if self.mrv_queue.size == 0:
            return True, expansions
        
        node = self.mrv_queue.pop()

        domain_list = deepcopy(self.domains[node.ycord][node.xcord])

        for num in domain_list:
            if self.checkIfSafe(node.ycord, node.xcord, num):
                expansions += 1
                self.board[node.ycord][node.xcord] = num
                temp = deepcopy(self.domains)
                temp_mrv = deepcopy(self.mrv_queue)
                forward_check = self.reduce_domains_value_mrv(num, node.ycord, node.xcord)
                success, expansions = self.backtracking_search_mrv(expansions)
                if success:
                    return True, expansions
                
                self.mrv_queue = temp_mrv
                self.domains = temp
                self.board[node.ycord][node.xcord] = " "
        return False, expansions

    


# ------ BACKTRACKING WITH FORWARD CHECK MRV


    def backtracking_forward_check_search_mrv(self, expansions = 0):

        if self.mrv_queue.size == 0:
            return True, expansions
        
        node = self.mrv_queue.pop()

        domain_list = deepcopy(self.domains[node.ycord][node.xcord])
    
        for num in domain_list:
            expansions += 1
            self.board[node.ycord][node.xcord] = num
            temp = deepcopy(self.domains)
            temp_mrv = deepcopy(self.mrv_queue)
            forward_check = self.reduce_domains_value_mrv(num, node.ycord, node.xcord)
            if forward_check:
                success, expansions = self.backtracking_forward_check_search_mrv(expansions)
                if success:
                    return True, expansions
            self.domains = temp
            self.mrv_queue = temp_mrv
            self.board[node.ycord][node.xcord] = " "
        return False, expansions





# ------------- Degree Heuristic added on MRV


    def get_degree(self, ycord, xcord):
        degree = 0
        
        for x in range(self.size):
            if x == xcord:
                continue                
            if self.board[ycord][x] == " ":
                degree += 1

        for y in range(self.size):
            if y == ycord:
                continue
            if self.board[y][xcord] == " ":
                degree += 1

        block_x = (xcord // self.block_size) * self.block_size
        block_y = (ycord // self.block_size) * self.block_size
        for x in range(block_y, block_y + self.block_size):
            for y in range(block_x, block_x + self.block_size):         
                if y != xcord and x != ycord and self.board[x][y] == " ":
                    degree += 1

        return degree



    def get_next_box(self):
        node_lis = []

        mrv_value, y, x = self.mrv_queue.pop()
        node = MRV_Node(mrv_value, y, x)
        node_lis.append(node)

        while True:
            next_node = heapq.heappop(self.mrv_queue)
            node_lis.append(next_node)
            if node.value != next_node.value:
                break
                    
        max_degree = 0
        max_index = 0

        for index, node in enumerate(node_lis):
            degree = self.get_degree(node.ycord, node.xcord)
            if max_degree < degree:
                max_degree = degree
                max_index = index

        degree_tuple = node_lis.pop(max_index)

        for node in node_lis:
            heapq.heappush(self.mrv_queue, node)

        heapq.heapify(self.mrv_queue)

       

        return degree_tuple




# ------ BACKTRACKING MRV & DEGREE
                             
    def backtracking_search_mrv_deg(self, expansions = 0):

        if not self.mrv_queue:
            return True, expansions
        
        mrv_value, y, x = self.get_next_box()

        domain_list = deepcopy(self.domains[y][x])

        for num in domain_list:
            if self.checkIfSafe(y, x, num):
                expansions += 1
                self.board[y][x] = num
                temp = deepcopy(self.domains)
                temp_mrv = deepcopy(self.mrv_queue)
                forward_check = self.reduce_domains_value_mrv(num, y, x)
                success, expansions = self.backtracking_search_mrv_deg(expansions)
                if success:
                    return True, expansions
                self.domains = temp
                self.mrv_queue = temp_mrv

                self.board[y][x] = " "
        return False, expansions
            

        
        
