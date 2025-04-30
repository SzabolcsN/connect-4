from game.player import Player

class CenterFirstBot(Player):
    builtin = True
    def get_move(self, board_state):
        preferred_order = [3, 2, 4, 1, 5, 0, 6]
        for c in preferred_order:
            if board_state[0][c] == 0:
                return c
        return 0