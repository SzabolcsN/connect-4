from game.player import Player
import copy

class OneStepBlockerBot(Player):
    builtin = True
    def get_move(self, board_state):
        opponent_id = 1 if self.player_id == 2 else 2

        def is_winning_move(board, col, pid):
            temp_board = copy.deepcopy(board)
            for row in reversed(range(6)):
                if temp_board[row][col] == 0:
                    temp_board[row][col] = pid
                    break
            return self.check_win(temp_board, pid)

        for c in range(7):
            if board_state[0][c] == 0 and is_winning_move(board_state, c, opponent_id):
                return c

        for c in range(7):
            if board_state[0][c] == 0:
                return c

    def check_win(self, board, pid):
        for row in range(6):
            for col in range(4):
                if all(board[row][col+i] == pid for i in range(4)):
                    return True
        for col in range(7):
            for row in range(3):
                if all(board[row+i][col] == pid for i in range(4)):
                    return True
        for row in range(3):
            for col in range(4):
                if all(board[row+i][col+i] == pid for i in range(4)):
                    return True
        for row in range(3, 6):
            for col in range(4):
                if all(board[row-i][col+i] == pid for i in range(4)):
                    return True
        return False