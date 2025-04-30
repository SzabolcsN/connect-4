from game.player import Player
import random

class RandomBot(Player):
    builtin = True
    def get_move(self, board_state):
        valid_moves = [c for c in range(7) if board_state[0][c] == 0]
        return random.choice(valid_moves)