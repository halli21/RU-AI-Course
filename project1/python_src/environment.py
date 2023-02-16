from state import State

WHITE, BLACK, EMPTY = "W", "B", " "

class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_state = State(width, height)


    def can_move_n_steps_forward(self, state, y, max_height_black, max_height_white):
        if state.white_turn and y <= max_height_white: return True
        if not state.white_turn and y >= max_height_black: return True
        return False


    def get_moves(self, state, moves, captures, y, x):
        opponent = BLACK if state.white_turn else WHITE

        one_step = 1 if state.white_turn else -1
        two_step = 2 if state.white_turn else -2
        

        # TWO STEPS FORWARD AND ONE STEP L / R
        if self.can_move_n_steps_forward(state, y, 2, self.height - 3):
            if x > 0 and state.board[y + two_step][x - 1] == EMPTY:
                moves.append((x, y, x - 1, y + two_step))

            if x < self.width - 1 and state.board[y + two_step][x + 1] == EMPTY:
                moves.append((x, y, x + 1, y + two_step))
        



        if self.can_move_n_steps_forward(state, y, 1, self.height - 2):
            if x > 1 and state.board[y + one_step][x - 2] == EMPTY:
                moves.append((x, y, x - 2, y + one_step))

            if x < self.width - 2 and state.board[y + one_step][x + 2] == EMPTY:
                moves.append((x, y, x + 2, y + one_step))



            if x > 0 and state.board[y + one_step][x - 1] == opponent:
                captures.append((x, y, x - 1, y + one_step))

            if x < self.width - 1 and state.board[y + one_step][x + 1] == opponent:
                captures.append((x, y, x + 1, y + one_step))

        


    
    def get_legal_moves(self, state):
        moves = []
        captures = []

        friendly = WHITE if state.white_turn else BLACK

        start_idx = self.height - 1 if state.white_turn else 0
        end_idx = - 1 if state.white_turn else self.height
        step = - 1 if state.white_turn else 1

        for y in range(start_idx, end_idx, step):
            for x in range(self.width):
                if state.board[y][x] == friendly:
                    self.get_moves(state, moves, captures, y, x)

        return captures + moves


    def move(self, state, move):
        x1, y1, x2, y2 = move
        state.board[y2][x2], state.board[y1][x1] = state.board[y1][x1], EMPTY
        state.white_turn = not state.white_turn


    def was_diagonal_move(self, move):
        x1, y1, x2, y2 = move

        if y2 - 1 == y1 and x2 - 1 == x1:
            return True
        if y2 - 1 == y1 and x2 + 1 == x1:
            return True
        if y2 + 1 == y1 and x2 - 1 == x1:
            return True
        if y2 + 1 == y1 and x2 + 1 == x1:
            return True
        return False


    def undo_move(self, state, move):
        x1, y1, x2, y2 = move

        if self.was_diagonal_move(move):
            if state.white_turn:
                state.board[y1][x1], state.board[y2][x2] = state.board[y2][x2], WHITE
            else:
                state.board[y1][x1], state.board[y2][x2] = state.board[y2][x2], BLACK

        else:
            state.board[y1][x1], state.board[y2][x2] = state.board[y2][x2], state.board[y1][x1]

        state.white_turn = not state.white_turn

    
