from environment import Environment
import os
import time
import platform


def main():
    env = Environment(16, 55)
    print(env.current_state)
    env.backtracking_brute()
    print(env.current_state)


#menu that asks for the size of the sudoku
def size_menu():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
        print()
    sizes = [0, 4, 9, 16]
    choice = int
    print("\n----Choose the size of the Sudoku----\n1) 4x4\n2) 9x9\n3) 16x16\n0) Quit")
    choice = input("Enter option: ")

    try:
        return sizes[int(choice)]
    except:
        print("Invalid input!\nPlease enter a number from the options list")
        time.sleep(3)
        return None


#menu that asks for the difficulty of the sudoku
def dif_menu():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
        print()
    difficulties = [0, "Easy", "Medium", "Hard"]
    print("\n----Choose a difficulty----\n1) Easy\n2) Medium\n3) Hard\n0) Go back")
    choice = input("Enter option: ")

    try:
        return difficulties[int(choice)]
    except:
        print("Invalid input!\nPlease enter a number from the options list")
        time.sleep(3)
        return


#menu that asks for the algorithm for the sudoku
def alg_menu():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
        print()
    algorithms = [0, "BacktrackBF", "Backtrack", "FwdCheck"]
    print("\n----Choose an algortihm----\n1) Backtracking (Brute force)\n2) Backtracking\n3) Backtracking with forward checking\n0) Go back")
    choice = input("Enter option: ")

    try:
        return algorithms[int(choice)]
    except:
        print("Invalid input!\nPlease enter a number from the options list")
        time.sleep(3)
        return


#menu that asks for the heuristic for the sudoku
def heu_menu(alg_choice):
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
        print()
    if alg_choice == "Backtrack":
        heuristics = [0, "MRV", "MRVDegree", "Random", "None"]
        print("\n----Choose a heuristic----\n1) MRV\n2) MRV with degree\n3) Random\n4) None\n0) Go back")
    elif alg_choice == "FwdCheck":
        heuristics = [0, "MRV", "MRVDegree", "None"]
        print("\n----Choose a heuristic----\n1) MRV\n2) MRV with degree\n3) None\n0) Go back")
    
    choice = input("Enter option: ")

    try:
        return heuristics[int(choice)]
    except:
        print("Invalid input!\nPlease enter a number from the options list")
        time.sleep(3)
        return




if __name__ == "__main__":

    size = None
    
    while size == None:
        difficulty = None
        alg_choice = None
        heu_choice = None
        size = size_menu()
        if size == None:
            continue
        elif size == 0:
            break
        while difficulty == None:
            difficulty = dif_menu()
            if difficulty == 0:
                size = None
                break
            while alg_choice == None:
                alg_choice = alg_menu()
                if alg_choice == 0:
                    difficulty = None
                    break
                elif alg_choice == "BacktrackBF":
                    break
                heu_choice = None
                while heu_choice == None:
                    heu_choice = heu_menu(alg_choice)
                    if heu_choice == 0:
                        alg_choice = None
                        break

    
    # if not quit then go to correct algorithm
    if heu_choice != None or alg_choice == "BacktrackBF":
        dif_choose = {"Easy": [7, 38, 118], "Medium": [6, 32, 100], "Hard": [5, 25, 77]}
        indexes = {4: 0, 9: 1, 16: 2}

        env = Environment(size, dif_choose[difficulty][indexes[size]])
        env.current_state.get_board()

        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
            print()
        print(env.current_state)
        print()

        if alg_choice == "BacktrackBF":
            expansions, elapsed_time = env.backtracking_brute()
            env.print_results(expansions, elapsed_time)


        elif alg_choice == "Backtrack":
            if heu_choice == "MRV":
                expansions, elapsed_time = env.backtracking_mrv()
                env.print_results(expansions, elapsed_time)
            elif heu_choice == "MRVDegree":
                expansions, elapsed_time = env.backtracking_mrv_deg()
                env.print_results(expansions, elapsed_time)
            elif heu_choice == "Random":
                expansions, elapsed_time = env.backtracking_random()
                env.print_results(expansions, elapsed_time)
            elif heu_choice == "None":
                expansions, elapsed_time = env.backtracking()
                env.print_results(expansions, elapsed_time)

        elif alg_choice == "FwdCheck":
            if heu_choice == "None":
                expansions, elapsed_time = env.backtracking_forward_check()
                env.print_results(expansions, elapsed_time)
            elif heu_choice == "MRV":
                expansions, elapsed_time = env.backtracking_forward_check_mrv()
                env.print_results(expansions, elapsed_time)
            elif heu_choice == "MRVDegree":
                expansions, elapsed_time = env.backtracking_forward_check_mrv_deg()
                env.print_results(expansions, elapsed_time)
        