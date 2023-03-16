from environment import Environment


def main():
    env = Environment(16, 55)
    print(env.current_state)
    env.backtracking_brute()
    print(env.current_state)





if __name__ == "__main__":
    main()