'''

def strong_pieces(self, state):
        value = 0

        friendly = WHITE if self.env.current_state.white_turn else BLACK

        start_idx = 0 if self.env.current_state.white_turn else self.env.height - 1
        end_idx = self.env.height if self.env.current_state.white_turn else - 1
        step = 1 if self.env.current_state.white_turn else - 1

        danger = -10 if self.env.current_state.white_turn else 10
        protected = 20 if self.env.current_state.white_turn else -20

        w_middle = (self.env.width // 2) - 1
        h_middle = (self.env.height // 2) - 1
        even = True if self.env.width % 2 == 0 else False

        for y in range(start_idx, end_idx, step):
            for x in range(self.env.width):
                if state.board[y][x] == friendly:
                    multiplier = 1

                    if self.in_danger(x, y, state):
                        value += danger
                        if self.protected(x, y, state):
                            value += protected

                    if even == False and x == w_middle:
                        multiplier = 1.7
                    if even == False and x == w_middle - 1 or x == w_middle + 1:
                        multiplier = 1.2
                    elif even == True and x == w_middle or x == w_middle + 1:
                        multiplier = 1.5

                    if self.env.current_state.white_turn:
                        if y < h_middle:
                            value += 1 * multiplier
                        else:
                            value += 2 * multiplier
                    else:
                        if y < h_middle:
                            value -= 1 * multiplier
                        else:
                            value -= 2 * multiplier
        return value
    
    

'''