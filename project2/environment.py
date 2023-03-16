import math

from state import State
from agent import Search

import time

class Environment:
    def __init__(self, size, hints):
        self.current_state = State(size, hints)
        self.size = size
        self.block_size = int(math.sqrt(size))  # math.sqrt returns float
    

    def backtracking_brute(self):
        s = Search(self.size, self.current_state.board, self.current_state.domains)
        start_time = time.time()
        s.backtracking_brute_search()
        elapsed_time = time.time() - start_time
        print(elapsed_time)

    def backtracking_forward_check_search(self):
        s = Search(self.size, self.current_state.board, self.current_state.domains)
        start_time = time.time()
        s.backtracking_forward_check_search()
        elapsed_time = time.time() - start_time
        print(elapsed_time)


 