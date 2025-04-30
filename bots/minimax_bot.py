from game.player import Player
import random
import copy

class MinimaxBot(Player):
    builtin = True
    def get_move(self, board_state):
        _, move = self.minimax(board_state, 3, True)
        return move

    def minimax(self, board, depth, maximizing):
        valid_moves = [c for c in range(7) if board[0][c] == 0]
        if depth == 0 or not valid_moves:
            return self.evaluate(board), None
        if maximizing:
            max_eval = float('-inf')
            best_move = random.choice(valid_moves)
            for move in valid_moves:
                new_board = self.simulate_move(board, move, self.player_id)
                eval_score, _ = self.minimax(new_board, depth - 1, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            opp_id = 1 if self.player_id == 2 else 2
            best_move = random.choice(valid_moves)
            for move in valid_moves:
                new_board = self.simulate_move(board, move, opp_id)
                eval_score, _ = self.minimax(new_board, depth - 1, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
            return min_eval, best_move

    def simulate_move(self, board, col, player_id):
        new_board = copy.deepcopy(board)
        for row in reversed(range(6)):
            if new_board[row][col] == 0:
                new_board[row][col] = player_id
                break
        return new_board

    def evaluate(self, board):
        return sum(cell == self.player_id for row in board for cell in row)