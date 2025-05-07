from game.player import Player
import math
import random

class EasyToUnderstandBot(Player):
    builtin = True
    MAX_DEPTH = 4

    def get_move(self, board):
        _, best_column = self.minimax(board, self.MAX_DEPTH, -math.inf, math.inf, True)
        return best_column

    def minimax(self, board, depth, alpha, beta, is_my_turn):
        available_columns = [col for col in range(7) if board[0][col] == 0]

        if depth == 0 or self.has_winner(board) or not available_columns:
            return self.evaluate_board(board), None

        best_column = random.choice(available_columns)

        if is_my_turn:
            best_score = -math.inf
            for col in self.prefer_center_columns(available_columns):
                row = self.find_row_for_column(board, col)
                board[row][col] = self.player_id
                score, _ = self.minimax(board, depth - 1, alpha, beta, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    best_column = col
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break
        else:
            best_score = math.inf
            opponent_id = 3 - self.player_id
            for col in self.prefer_center_columns(available_columns):
                row = self.find_row_for_column(board, col)
                board[row][col] = opponent_id
                score, _ = self.minimax(board, depth - 1, alpha, beta, True)
                board[row][col] = 0
                if score < best_score:
                    best_score = score
                    best_column = col
                beta = min(beta, best_score)
                if alpha >= beta:
                    break

        return best_score, best_column

    def find_row_for_column(self, board, column):
        for row in reversed(range(6)):
            if board[row][column] == 0:
                return row

    def prefer_center_columns(self, columns):
        return sorted(columns, key=lambda col: abs(3 - col))

    def evaluate_board(self, board):
        score = 0
        my_id = self.player_id
        opponent_id = 3 - my_id

        def score_group(group):
            if group.count(my_id) == 4:
                return 100
            elif group.count(my_id) == 3 and group.count(0) == 1:
                return 5
            elif group.count(my_id) == 2 and group.count(0) == 2:
                return 2
            elif group.count(opponent_id) == 3 and group.count(0) == 1:
                return -50
            return 0

        for row in range(6):
            for col in range(4):
                group = board[row][col:col+4]
                score += score_group(group)

        for col in range(7):
            for row in range(3):
                group = [board[row+i][col] for i in range(4)]
                score += score_group(group)

        for row in range(3):
            for col in range(4):
                group = [board[row+i][col+i] for i in range(4)]
                score += score_group(group)

        for row in range(3, 6):
            for col in range(4):
                group = [board[row-i][col+i] for i in range(4)]
                score += score_group(group)

        return score

    def has_winner(self, board):
        for pid in [1, 2]:
            if self.check_four_in_a_row(board, pid):
                return True
        return False

    def check_four_in_a_row(self, board, pid):
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
