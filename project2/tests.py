
from environment import Environment

              # 4x4, 9x9, 16x16
EASY = 0.46   # 7, 38, 118
MEDIUM = 0.39 # 6, 32, 100
HARD = 0.3    # 5, 25, 77

DIFFICULTIES = [EASY, MEDIUM, HARD]
DIFFICULTIES_STR = ["EASY", "MEDIUM", "HARD"]

TESTS_4x4 = ["4x4_EASY.txt", "4x4_MEDIUM.txt", "4x4_HARD.txt"]
TESTS_9x9 = ["9x9_EASY.txt", "9x9_MEDIUM.txt", "9x9_HARD.txt"]
TESTS_16x16 = ["16x16_EASY.txt", "16x16_MEDIUM.txt", "16x16_HARD.txt"]



def generate_boards():
    size = 16

    iterations = 0
    seed = 1

    f = open("16x16_HARD.txt", "a")


    while iterations < 100:
        output = ""
        env = Environment(size, round((size * size) * HARD), seed)
        env.current_state.get_board()
        if env.current_state.board != None:
            for y in range(size):
                for x in range(size):
                    output += str(env.current_state.board[y][x]) + "-"
        else:
            seed += 1
            continue

        seed += 1
        iterations += 1

        print(f"Iteration: {iterations}, SEED: {seed}")
        output += "\n"
        f.write(output)
    
    f.close()



def get_boards(file_name, size):
    boards_list = []

    f = open(file_name)

    for _ in range(100):
        board = [[" " for _ in range(size)] for _ in range(size)]
        line = f.readline()
        values = line.split("-")
        index = 0

        for y in range(size):
            for x in range(size):
                board[y][x] = values[index]
                index += 1
        
        boards_list.append(board)

    f.close()

    return boards_list
 






# SOME SEEDS RESULT IN A FAILED GENERATION OF BOARD SO WE US WHILE LOOPS TO SKIP BAD SEEDS

def test(size, search, tests):

    if search == "backtracking_forward_check":
        print(f"\n\n----TESTING BACKTRACKING WITH FORWARD CHECK ALGORTIHM AT SIZE {size}----")
    elif search == "backtracking": 
        print(f"\n\n----TESTING BACKTRACKING ALGORTIHM AT SIZE {size}----")
    elif search == "backtracking_brute": 
        print(f"\n\n----TESTING BACKTRACKING BRUTE ALGORTIHM AT SIZE {size}----")
    elif search == "backtracking_brute_mrv":
        print(f"\n\n----TESTING BACKTRACKING WITH MRV HEURISTIC ALGORTIHM AT SIZE {size}----")
    elif search == "backtracking_forward_check_mrv":
        print(f"\n\n----TESTING BACKTRACKING WITH FORWARD CHECK AND MRV HEURISTIC ALGORTIHM AT SIZE {size}----")

    

    for count, level in enumerate(DIFFICULTIES):
        expansion_sum = 0
        expansion_ps_sum = 0
        elapsed_time_sum = 0
        
        iterations = 0
        
        boards_list = get_boards(tests[count], size)
    
        while iterations < 100:
            env = Environment(size, round((size * size) * level))
            env.current_state.board = boards_list[iterations]
            env.current_state.update_domain()

            
            if search == "backtracking_forward_check":
                expansions, elapsed_time = env.backtracking_forward_check()
            elif search == "backtracking": 
                expansions, elapsed_time = env.backtracking()
            elif search == "backtracking_brute": 
                expansions, elapsed_time = env.backtracking_brute()
            elif search == "backtracking_brute_mrv":
                expansions, elapsed_time = env.backtracking_brute_mrv()
            elif search == "backtracking_forward_check_mrv":
                expansions, elapsed_time = env.backtracking_forward_check_mrv()
            elif search == "backtracking_random":
                expansions, elapsed_time = env.backtracking_random()
            expansion_sum += expansions
            try:
                expansion_ps_sum += expansions / elapsed_time
            except ZeroDivisionError:
                pass
            elapsed_time_sum += elapsed_time
            
            
            
            iterations += 1

        print(f"\n\n--{iterations} TESTS AT DIFFICULTY LEVEL {DIFFICULTIES_STR[count]}--")

        print(f"Average total expansions: {expansion_sum / iterations}")
        print(f"Average expansions per second: {expansion_ps_sum / iterations}")
        print(f"Average search run-time: {elapsed_time_sum / iterations}")




if __name__ == "__main__":
    test(4, "backtracking", TESTS_4x4)
    #test(9, "backtracking", TESTS_9x9)
   
    """
    backtracking_brute

    backtracking

    backtracking_forward_check

    backtracking_brute_mrv
   
    backtracking_forward_check_mrv
            
    """
    

   