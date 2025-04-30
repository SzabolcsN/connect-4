ROWS = 6
COLS = 7

class Board:
    def __init__(self):
        self.grid = [[0] * COLS for _ in range(ROWS)]

    def drop_piece(self, col, player_id):
        for row in reversed(range(ROWS)):
            if self.grid[row][col] == 0:
                self.grid[row][col] = player_id
                return True
        return False

    def is_valid_move(self, col):
        return self.grid[0][col] == 0

    def get_valid_moves(self):
        return [c for c in range(COLS) if self.is_valid_move(c)]

    def check_winner(self, player_id):
        for row in range(ROWS):
            for col in range(COLS - 3):
                if all(self.grid[row][col + i] == player_id for i in range(4)):
                    return True

        for col in range(COLS):
            for row in range(ROWS - 3):
                if all(self.grid[row + i][col] == player_id for i in range(4)):
                    return True

        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                if all(self.grid[row + i][col + i] == player_id for i in range(4)):
                    return True

        for row in range(3, ROWS):
            for col in range(COLS - 3):
                if all(self.grid[row - i][col + i] == player_id for i in range(4)):
                    return True

        return False

    def is_full(self):
        return all(self.grid[0][col] != 0 for col in range(COLS))

