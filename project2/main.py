from environment import Environment
import os
import time
import platform


def main():
    env = Environment(16, 55)
    print(env.current_state)
    env.backtracking_brute()
    print(env.current_state)



def size_menu():
    os.system('cls')
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


def dif_menu():
    os.system('cls')
    difficulties = [0, "Easy", "Medium", "Hard"]
    print("\n----Choose a difficulty----\n1) Easy\n2) Medium\n3) Hard\n0) Go back")
    choice = input("Enter option: ")

    try:
        return difficulties[int(choice)]
    except:
        print("Invalid input!\nPlease enter a number from the options list")
        time.sleep(3)
        return

def alg_menu():
    os.system('cls')
    algorithms = [0, "BacktrackBF", "Backtrack", "FwdCheck"]
    print("\n----Choose an algortihm----\n1) Backtracking (Brute force)\n2) Backtracking\n3) Backtracking with forward checking\n0) Go back")
    choice = input("Enter option: ")

    try:
        return algorithms[int(choice)]
    except:
        print("Invalid input!\nPlease enter a number from the options list")
        time.sleep(3)
        return


def heu_menu(alg_choice):
    os.system('cls')
    if alg_choice == "Backtrack":
        heuristics = [0, "MRV", "MRVDegree", "None"]
        print("\n----Choose a heuristic----\n1) MRV\n2) MRV with degree\n3) None\n0) Go back")
    elif alg_choice == "FWDCheck":
        heuristics = [0, "MRV", "None"]
        print("\n----Choose a heuristic----\n1) MRV\n2) None\n0) Go back")
    
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

    
    if heu_choice != None or alg_choice == "BacktrackBF":
        dif_choose = {"Easy": [7, 38, 118], "Medium": [6, 32, 100], "Hard": [5, 25, 77]}
        indexes = {4: 0, 9: 1, 16: 2}

        env = Environment(size, dif_choose[difficulty][indexes[size]])
        env.current_state.get_board()

        os.system('cls')
        print(env.current_state)
        print()

        if alg_choice == "BacktrackBF":
            env.backtracking_brute()

        elif alg_choice == "Backtrack":
            if heu_choice == "MRV":
                env.backtracking_mrv()
            elif heu_choice == "MRVDegree":
                env.backtracking_mrv_deg()
            elif heu_choice == "None":
                env.backtracking()

        elif alg_choice == "FwdCheck":
            if heu_choice == "None":
                env.backtracking_forward_check()
            elif heu_choice == "MRV":
                env.backtracking_forward_check_mrv()
            
    """if platform.system() == "Windows":
        os.system("pause")
    else:
        os.system("/bin/bash -c 'read -s -n 1 -p \"Press any key to continue...\"'")
        print()"""