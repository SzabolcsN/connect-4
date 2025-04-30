from game.player import Player
import time
import copy

class IterativeDeepeningBot(Player):
    builtin = True

    def get_move(self, board_state, time_limit=None):
        start_time = time.time()
        best_move = 0
        depth = 1

        while True:
            if time_limit and (time.time() - start_time) > time_limit * 0.9:
                break
            move = self.minimax(board_state, depth)
            if move is not None:
                best_move = move
            depth += 1

        return best_move

    def minimax(self, board, depth):
        valid_moves = [c for c in range(7) if board[0][c] == 0]
        best_score = float('-inf')
        best_move = None
        for move in valid_moves:
            score = self.evaluate_move(board, move)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def evaluate_move(self, board, col):
        new_board = copy.deepcopy(board)
        for row in reversed(range(6)):
            if new_board[row][col] == 0:
                new_board[row][col] = self.player_id
                break
        # Very simple evaluation: count own pieces
        return sum(cell == self.player_id for row in new_board for cell in row)
