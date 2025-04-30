from game.player import Player

class LeftmostBot(Player):
    builtin = True
    def get_move(self, board_state):
        for c in range(7):
            if board_state[0][c] == 0:
                return c
        return 0