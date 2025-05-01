import subprocess
import json


class Player:
    def __init__(self, name, player_id):
        self.name = name
        self.player_id = player_id

    def get_move(self, board_state):
        raise NotImplementedError


class HumanPlayer(Player):
    def __init__(self, name, player_id):
        super().__init__(name, player_id)


class ExecutableBot(Player):
    def __init__(self, name, player_id, path):
        super().__init__(name, player_id)
        self.path = path

    def get_move(self, board_state, time_limit):
        try:
            input_data = {
                "board": board_state,
                "player_id": self.player_id,
                "time_limit": int(time_limit * 1000),  # milliseconds
            }
            result = subprocess.run(
                [self.path],
                input=json.dumps(input_data),
                capture_output=True,
                text=True,
                timeout=time_limit
                + 150,  # Alapbol kell egy kis ido a beinditashoz
            )
            print(result.stdout.strip())
            print(result.stderr)
            move = int(result.stdout.strip())
            return move

        except subprocess.TimeoutExpired:
            print(f"Bot {self.name} exceeded time limit!")
            return 0  # fallback move

        except Exception as e:
            print(f"Error running bot {self.name}: {e}")
            return 0  # fallback
