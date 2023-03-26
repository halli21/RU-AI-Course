import math
import time

from state import State
from agent import Search


class Environment:
    def __init__(self, size, hints, seed=None):
        self.current_state = State(size, hints, seed)
        self.size = size
        self.block_size = int(math.sqrt(size))  # math.sqrt returns float


    def print_results(self, expansions, elapsed_time):
        print(self.current_state)
        output = f"\nTotal expansions: {expansions}"
        output += f"\nExpansions per second: {expansions / (elapsed_time + 0.000000000000000000000000001)}"
        output += f"\nSearch run-time: {elapsed_time}"
        print(output)
    
    #test for bakctracking brute search
    def backtracking_brute(self):
        s = Search(self.size, self.current_state.board, self.current_state.domains)

        s.start_time = time.time()

        start_time = time.time()
        success, expansions = s.backtracking_brute_search()
        elapsed_time = time.time() - start_time
        return expansions, elapsed_time
        #self.print_results(expansions, elapsed_time)

    #test for normal bakctracking search
    def backtracking(self):
        s = Search(self.size, self.current_state.board, self.current_state.domains)

        s.start_time = time.time()

        start_time = time.time()
        s.set_up_search()
        success, expansions = s.backtracking_search()
        elapsed_time = time.time() - start_time
        return expansions, elapsed_time
        #self.print_results(expansions, elapsed_time)

    #test for bakctracking search with forward checking
    def backtracking_forward_check(self):
        s = Search(self.size, self.current_state.board, self.current_state.domains)

        s.start_time = time.time()

        start_time = time.time()
        s.set_up_search()
        success, expansions = s.backtracking_forward_check_search()
        elapsed_time = time.time() - start_time
        return expansions, elapsed_time
        
        #self.print_results(expansions, elapsed_time)

    #test for backtracking with mrv
    def backtracking_mrv(self):
        s = Search(self.size, self.current_state.board, self.current_state.domains)

        s.start_time = time.time()

        start_time = time.time()
        s.set_up_search_mrv()
        success, expansions = s.backtracking_search_mrv()
        elapsed_time = time.time() - start_time
        return expansions, elapsed_time
        #self.print_results(expansions, elapsed_time)


    #test for backtracking with foward checking and mrv
    def backtracking_forward_check_mrv(self):
        s = Search(self.size, self.current_state.board, self.current_state.domains)

        s.start_time = time.time()

        start_time = time.time()
        s.set_up_search_mrv()
        success, expansions = s.backtracking_forward_check_search_mrv()
        elapsed_time = time.time() - start_time
        return expansions, elapsed_time
        #self.print_results(expansions, elapsed_time)
     

    #test for backtracking with mrv and degree
    def backtracking_mrv_deg(self):
        s = Search(self.size, self.current_state.board, self.current_state.domains)

        s.start_time = time.time()
        
        start_time = time.time()
        s.set_up_search_mrv()
        success, expansions = s.backtracking_search_mrv_deg()
        elapsed_time = time.time() - start_time
        return expansions, elapsed_time
        #self.print_results(expansions, elapsed_time)



    def backtracking_forward_check_mrv_deg(self):
        s = Search(self.size, self.current_state.board, self.current_state.domains)

        s.start_time = time.time()
        
        start_time = time.time()
        s.set_up_search_mrv()
        success, expansions = s.backtracking_forward_check_search_mrv_deg()
        elapsed_time = time.time() - start_time
        return expansions, elapsed_time
        #self.print_results(expansions, elapsed_time)

    #test for backtracking random search
    def backtracking_random(self):
        s = Search(self.size, self.current_state.board, self.current_state.domains)

        s.start_time = time.time()

        start_time = time.time()
        s.set_up_search_rand()
        success, expansions = s.backtracking_random()
        elapsed_time = time.time() - start_time
        
        return expansions, elapsed_time
        #self.print_results(expansions, elapsed_time)






if __name__ == "__main__":
    
    env = Environment(16, 118, 1)
    env.current_state.get_board()
  
    print(env.current_state)
    env.backtracking_mrv_deg()



    


   
    

 