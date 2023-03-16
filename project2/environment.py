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

    def backtracking_forward_check(self):
        s = Search(self.size, self.current_state.board, self.current_state.domains)
        start_time = time.time()
        s.reduce_all_domains()
        s.backtracking_forward_check_search()
        elapsed_time = time.time() - start_time
        print(elapsed_time)




if __name__ == "__main__":
    """
    env = Environment(16, 100)
    print(env.current_state)
    env.backtracking_brute()
    print(env.current_state)"""

    board = [[" " for _ in range(4)] for _ in range(4)]

    board[1][0] = 4
    board[1][1] = 2
    board[1][2] = 1
    board[2][0] = 3
    board[3][1] = 1

    env2 = Environment(4, 5)
    env2.current_state.board = board
    env2.current_state.domains = [[list(range(1, 4 + 1)) for _ in range(4)] for _ in range(4)]
    env2.current_state.update_domain()
    print(env2.current_state)
    env2.backtracking_forward_check()
    print(env2.current_state)
    

 