from game.board import Board

class Game:
    def __init__(self, player1, player2):
        self.board = Board()
        self.players = [player1, player2]
        self.current_turn = 0

    def play_turn(self):
        player = self.players[self.current_turn]
        move = player.get_move(self.board.grid)
        if self.board.is_valid_move(move):
            self.board.drop_piece(move, player.player_id)
            if self.board.check_winner(player.player_id):
                return f"{player.name} wins!"
            elif self.board.is_full():
                return "Draw!"
            self.current_turn = 1 - self.current_turn
        return None