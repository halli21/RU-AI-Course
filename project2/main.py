from environment import Environment


def main():
    pass




if __name__ == "__main__":
    env = Environment(4, 2)

    print(env.current_state)

    print(env.current_state.domains)

    env.reduce_domains()

    print(env.current_state)

    print(env.current_state.domains)