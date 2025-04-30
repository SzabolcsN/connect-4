class Player:
    def __init__(self, name, player_id):
        self.name = name
        self.player_id = player_id

    def get_move(self, board_state):
        raise NotImplementedError


class HumanPlayer(Player):
    def __init__(self, name, player_id):
        super().__init__(name, player_id)