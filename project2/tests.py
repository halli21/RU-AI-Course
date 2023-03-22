import time
import threading

from environment import Environment

              # 4x4, 9x9, 16x16
EASY = 0.46   # 7, 38, 118
MEDIUM = 0.39 # 6, 32, 100
HARD = 0.3    # 5, 25, 77

DIFFICULTIES = [EASY, MEDIUM, HARD]
DIFFICULTIES_STR = ["EASY", "MEDIUM", "HARD"]




# SOME SEEDS RESULT IN A FAILED GENERATION OF BOARD SO WE US WHILE LOOPS TO SKIP BAD SEEDS

def test_backtracking_brute(size):
    print(f"\n\n----TESTING BACKTRACKING BRUTE ALGORTIHM AT SIZE {size}----")

    for count, level in enumerate(DIFFICULTIES):
        expansion_sum = 0
        expansion_ps_sum = 0
        elapsed_time_sum = 0
        
        iterations = 0
        seed = 1
    
        while iterations < 100:
            env = Environment(size, round((size * size) * level), seed)
            if env.current_state.board != None:
                expansions, elapsed_time = env.backtracking_brute()
                expansion_sum += expansions
                expansion_ps_sum += expansions / elapsed_time
                elapsed_time_sum += elapsed_time
            else:
                seed += 1
                continue

            seed += 1
            iterations += 1

        print(f"\n\n--{iterations} TESTS AT DIFFICULT LEVEL {DIFFICULTIES_STR[count]}--")

        print(f"Average total expansions: {expansion_sum / iterations}")
        print(f"Average expansions per second: {expansion_ps_sum / iterations}")
        print(f"Average search run-time: {elapsed_time_sum / iterations}")



def test_backtracking_forward_check(size):
    print(f"\n\n----TESTING BACKTRACKING WITH FORWARD CHECK ALGORTIHM AT SIZE {size}----")

    for count, level in enumerate(DIFFICULTIES):
        expansion_sum = 0
        expansion_ps_sum = 0
        elapsed_time_sum = 0
        
        iterations = 0
        seed = 1
    
        while iterations < 100:
            env = Environment(size, round((size * size) * level), seed)
            if env.current_state.board != None:
                expansions, elapsed_time = env.backtracking_forward_check()
                expansion_sum += expansions
                expansion_ps_sum += expansions / elapsed_time
                elapsed_time_sum += elapsed_time
            else:
                seed += 1
                continue
            
            seed += 1
            iterations += 1

        print(f"\n\n--{iterations} TESTS AT DIFFICULT LEVEL {DIFFICULTIES_STR[count]}--")

        print(f"Average total expansions: {expansion_sum / iterations}")
        print(f"Average expansions per second: {expansion_ps_sum / iterations}")
        print(f"Average search run-time: {elapsed_time_sum / iterations}")




def test_backtracking_brute_mrv(size):
    print(f"\n\n----TESTING BACKTRACKING WITH MRV HEURISTIC ALGORTIHM AT SIZE {size}----")

    for count, level in enumerate(DIFFICULTIES):
        expansion_sum = 0
        expansion_ps_sum = 0
        elapsed_time_sum = 0
        
        iterations = 0
        seed = 1
    
        while iterations < 100:
            env = Environment(size, round((size * size) * level), seed)
            if env.current_state.board != None:
                expansions, elapsed_time = env.backtracking_brute_mrv()
                expansion_sum += expansions
                expansion_ps_sum += expansions / elapsed_time
                elapsed_time_sum += elapsed_time
            else:
                seed += 1
                continue
            
            seed += 1
            iterations += 1

        print(f"\n\n--{iterations} TESTS AT DIFFICULT LEVEL {DIFFICULTIES_STR[count]}--")

        print(f"Average total expansions: {expansion_sum / iterations}")
        print(f"Average expansions per second: {expansion_ps_sum / iterations}")
        print(f"Average search run-time: {elapsed_time_sum / iterations}")



def test_backtracking_forward_check_mrv(size):
    print(f"\n\n----TESTING BACKTRACKING WITH FORWARD CHECK AND MRV HEURISTIC ALGORTIHM AT SIZE {size}----")

    for count, level in enumerate(DIFFICULTIES):
        expansion_sum = 0
        expansion_ps_sum = 0
        elapsed_time_sum = 0
        
        iterations = 0
        seed = 1
    
        while iterations < 10:
            env = Environment(size, round((size * size) * level), seed)
            if env.current_state.board != None:
                expansions, elapsed_time = env.backtracking_forward_check_mrv()
                expansion_sum += expansions
                expansion_ps_sum += expansions / elapsed_time
                elapsed_time_sum += elapsed_time
            else:
                seed += 1
                continue
            
            seed += 1
            iterations += 1

        print(f"\n\n--{iterations} TESTS AT DIFFICULT LEVEL {DIFFICULTIES_STR[count]}--")

        print(f"Average total expansions: {expansion_sum / iterations}")
        print(f"Average expansions per second: {expansion_ps_sum / iterations}")
        print(f"Average search run-time: {elapsed_time_sum / iterations}")




if __name__ == "__main__":
    test_backtracking_forward_check_mrv(16)

   