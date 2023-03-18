from agent import Agent

from environment import Environment

import time
from copy import deepcopy


WHITE, BLACK, EMPTY = "W", "B", " "

class MyAgent(Agent):
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
        
            #if self.env.current_state.white_turn:
            return self.state_evaluation(state)
            #else:
            #    return -self.state_evaluation(state)
        


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

    def state_evaluation(self, state):
        moves = self.env.get_legal_moves(state)

        win = self.check_win(state)

        if win != False:
            return win
        elif len(moves) == 0:
            return 0
        else:
            return self.win_openings(state) + self.piece_value(state)


    
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
                if self.env.current_state.white_turn:
                    return 100
                else:
                    return -100

        # BLACK
        for tile in state.board[0]:
            if tile == BLACK:
                if self.env.current_state.white_turn:
                    return -100
                else:
                    return 100
    
        return False




    def win_openings(self, state):

        friendly = WHITE if self.env.current_state.white_turn else BLACK
        opponent = BLACK if self.env.current_state.white_turn else WHITE

        start_idx = 2 if self.env.current_state.white_turn else self.env.height - 3     # CHECK TILES THAT COULD HAVE AN OPPONENT PIECE
        end_idx = 0 if self.env.current_state.white_turn else self.env.height - 1       # THAT IS POSSIBLY BE 1 MOVE FROM WIN
        step = - 1 if self.env.current_state.white_turn else 1                       # WHITE = LINES 1 AND 2
                                                                    # BLACK = LINE H-2 AND H-3

        two_step = - 2 if self.env.current_state.white_turn else 2  

        for y in range(start_idx, end_idx, step):
            for x in range(self.env.width):
                if state.board[y][x] == opponent:
                    
                    if y == start_idx:

                        if x > 0 and state.board[y + two_step][x - 1] == EMPTY:
                            return -90

                        if x < self.env.width - 1 and state.board[y + two_step][x + 1] == EMPTY:
                            return -90

                    else:

                        if x > 0 and state.board[y + step][x - 1] == friendly:
                            return -90

                    
                        if x < self.env.width - 1 and state.board[y + step][x + 1] == friendly:
                            return -90

                        
                        if x > 1 and state.board[y + step][x - 2] == EMPTY:
                            return -90


                        if x < self.env.width - 2 and state.board[y + step][x + 2] == EMPTY:
                            return -90
        return 0

    


    def piece_value(self, state):
        value = 0

        friendly = WHITE if self.env.current_state.white_turn else BLACK

        protected = 5
        can_attack = 2

        for y in range(self.env.height):
            for x in range(self.env.width):
                if state.board[y][x] == friendly:
                    if self.protected(x, y, state):
                        value += protected
                    pos = self.can_attack(x, y, state)
                    if pos != False:
                    
                        self.env.current_state.white_turn = not self.env.current_state.white_turn

                        opp_not_protected = self.can_attack(pos[0], pos[1], state)
                        if opp_not_protected != False:
                            value += can_attack * 15
                        else:
                            value += can_attack

                        self.env.current_state.white_turn = not self.env.current_state.white_turn
        return value



    def can_attack(self, x, y, state):
        opponent = BLACK if self.env.current_state.white_turn else WHITE
        
        step = 1 if self.env.current_state.white_turn else -1

        if x > 0 and (0 < y < self.env.height - 1) and state.board[y + step][x - 1] == opponent:
            return (x - 1, y + step)

        if x < self.env.width - 1 and (0 < y < self.env.height - 1) and state.board[y + step][x + 1] == opponent:
            return (x - 1, y + step)
        
        return False

    

    def protected(self, x, y, state):
        friendly = WHITE if self.env.current_state.white_turn else BLACK
       
        step = -1 if self.env.current_state.white_turn else 1

        if x > 0 and (0 < y < self.env.height - 1) and state.board[y + step][x - 1] == friendly:
            return True

        if x < self.env.width - 1 and (0 < y < self.env.height - 1) and state.board[y + step][x + 1] == friendly:
            return True
        
        return False

  


if __name__ == "__main__":
    agent = MyAgent()
    env = Environment(3, 5)
    agent.env = env
    agent.play_clock = 5

    agent.get_best_move()

