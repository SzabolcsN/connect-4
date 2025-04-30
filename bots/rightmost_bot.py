from game.player import Player

class RightmostBot(Player):
    builtin = True
    def get_move(self, board_state):
        for c in reversed(range(7)):
            if board_state[0][c] == 0:
                return c
        return 6