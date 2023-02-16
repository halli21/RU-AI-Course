from agent import Agent

from environment import Environment

import time
from copy import deepcopy


WHITE, BLACK, EMPTY = "W", "B", " "

class DefaultMyAgent(Agent):
    def __init__(self):
        self.role = None
        self.play_clock = None
        self.my_turn = False
        self.width = 0
        self.height = 0

        self.env = None
        self.start_time = None
        self.expansions = 0
        self.elapsed_time = 0

    # start() is called once before you have to select the first action. Use it to initialize the agent.
    # role is either "white" or "black" and play_clock is the number of seconds after which nextAction must return.
    def start(self, role, width, height, play_clock):
        self.play_clock = play_clock
        self.role = role
        self.my_turn = role != 'white'
        # we will flip my_turn on every call to next_action, so we need to start with False in case
        #  our action is the first
        self.width = width
        self.height = height
        # TODO: add your own initialization code here

        self.env = Environment(width, height)
        

    def next_action(self, last_action):
        if last_action:
            if self.my_turn and self.role == 'white' or not self.my_turn and self.role != 'white':
                last_player = 'white'
            else:
                last_player = 'black'
            print("%s moved from %s to %s" % (last_player, str(last_action[0:2]), str(last_action[2:4])))
            # TODO: 1. update your internal world model according to the action that was just executed
            
            x1, y1, x2, y2 = last_action
            last_action_adjusted = (x1 - 1, y1 - 1, x2 - 1, y2 - 1)

            self.env.move(self.env.current_state, last_action_adjusted)

        else:
            print("first move!")

        # update turn (above that line it myTurn is still for the previous state)
        self.my_turn = not self.my_turn
        if self.my_turn:
            # TODO: 2. run alpha-beta search to determine the best move
 
            x1, y1, x2, y2 = self.get_best_move()

            x1, y1, x2, y2 = x1 + 1, y1 + 1, x2 + 1, y2 + 1

            return "(move " + " ".join(map(str, [x1 , y1, x2, y2])) + ")"
        else:
            return "noop"

    


    def get_best_move(self):
        self.start_time = time.time()
        depth = 1
        beta = 100
        alpha = -100
        best_move = None
        self.expansions = 0

        state_copy = deepcopy(self.env.current_state)

        while True:
            try:
                best_move = self.alpha_beta_root(state_copy, depth, alpha, beta)
                depth += 1
            except TimeoutError:
                print("\nTIME OUT ERROR")
                break

        print("Total expansions: ", self.expansions)
        print("Expansions per second: ", self.expansions / self.elapsed_time)
        print("Current depth limit: ", depth)
        print("Search run-time: ", self.elapsed_time, "\n")

        
        return best_move

    

    def alpha_beta_root(self, state, depth, alpha, beta):
        moves = self.env.get_legal_moves(state)

        best_score = float('-inf')
        best_move = None
    
        for move in moves:
            self.env.move(state, move)

            score = self.minimax(state, depth - 1, True, alpha, beta)


            self.env.undo_move(state, move)

            if score > best_score:
                best_score = score
                best_move = move


            self.expansions += 1

            alpha = max(alpha, best_score)

            if alpha >= beta:
                break

        
        return best_move



    # 4. Implement iterative deepening alpha-beta search and use this state evaluation function to evaluate the leaf nodes of the tree.

    def minimax(self, state, depth, isMaxmizing, alpha, beta):

        self.elapsed_time = time.time() - self.start_time

        if self.play_clock - 0.01 < self.elapsed_time:
            raise TimeoutError

        moves = self.env.get_legal_moves(state)

        if depth <= 0 or self.game_over(state):
        
            if self.env.current_state.white_turn:
                return self.state_evaluation(state, depth)
            else:
                return -self.state_evaluation(state, depth)
        


        if isMaxmizing:
            best_score = float('-inf')

            for move in moves:
                self.env.move(state, move)
                

                score = self.minimax(state, depth - 1, False, alpha, beta)


                self.env.undo_move(state, move)


                best_score = max(score, best_score)


                self.expansions += 1

                alpha = max(alpha, best_score)

                if alpha >= beta:
                    break

            return best_score

        else:
            best_score = float('inf')
            for move in moves:
                self.env.move(state, move)

                score  = self.minimax(state, depth - 1, True, alpha, beta)

              
                self.env.undo_move(state, move)

                best_score = min(score, best_score)

                self.expansions += 1

                beta = min(beta, best_score)

                if alpha >= beta:
                    break


             
            return best_score




    # 3. Implement a state evaluation function (heuristic) for the game

    def state_evaluation(self, state, depth=0):
        moves = self.env.get_legal_moves(state)

        win = self.check_win(state)

        if win != False:
            return win
        elif len(moves) == 0:
            return 0
        else:
       
            return self.most_advanced(state)


    
    # HELPER FUNCTIONS

    def game_over(self, state):
        for tile in state.board[0]:
            if tile == BLACK:
                return True
        for tile in state.board[self.env.height - 1]:
            if tile == WHITE:
                return True
        return False


    def check_win(self, state):
        # WHITE
        for tile in state.board[self.env.height - 1]:
            if tile == WHITE:
                return 100

        # BLACK
        for tile in state.board[0]:
            if tile == BLACK:
                return -100

        return False

    
    def most_advanced(self, state):
        white_dist = 0
        black_dist = 0


        for i in range(self.env.height):
            for j in range(self.env.width):
                if state.board[i][j] == WHITE:
                    white_dist = max(white_dist, i)
                elif state.board[i][j] == BLACK:
                    black_dist = max(black_dist, self.env.height - 1 - j)


        return black_dist - white_dist
       

