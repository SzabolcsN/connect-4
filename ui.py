import tkinter as tk
from game.game import Game
from game.player import HumanPlayer
import threading
import time
from loader import discover_bots

class Connect4UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect 4")
        self.canvas = tk.Canvas(self.root, width=700, height=600, bg="blue")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.bot_classes = discover_bots("bots")

        self.options = ["Human"] + [name for name, _ in self.bot_classes]

        self.bot1_var = tk.StringVar(value=self.options[0])
        self.bot2_var = tk.StringVar(value=self.options[1] if len(self.options) > 1 else self.options[0])

        self.ui_frame = tk.Frame(self.root)
        self.ui_frame.pack(pady=10)

        player1_frame = tk.Frame(self.ui_frame)
        player1_frame.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Label(player1_frame, text="● Player 1 (Red):", fg="red", font=("Arial", 10, "bold")).pack(side="left")
        tk.OptionMenu(player1_frame, self.bot1_var, *self.options).pack(side="left")

        player2_frame = tk.Frame(self.ui_frame)
        player2_frame.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Label(player2_frame, text="● Player 2 (Yellow):", fg="gold", font=("Arial", 10, "bold")).pack(side="left")
        tk.OptionMenu(player2_frame, self.bot2_var, *self.options).pack(side="left")

        time_frame = tk.Frame(self.ui_frame)
        time_frame.grid(row=3, column=0, pady=5)
        tk.Label(time_frame, text="⏱ Time per move (sec):", font=("Arial", 10)).pack(side="left")
        self.time_limit_var = tk.DoubleVar(value=2.0)
        tk.Spinbox(time_frame, from_=0.1, to=10.0, increment=0.1, textvariable=self.time_limit_var, width=5).pack(side="left")

        button_frame = tk.Frame(self.ui_frame)
        button_frame.grid(row=2, column=0, pady=10)
        tk.Button(button_frame, text="▶ Play", command=self.start_game, width=10).pack(side="left", padx=5)
        tk.Button(button_frame, text="↻ Replay", command=self.reset_ui, width=10).pack(side="left", padx=5)

        self.players = []
        self.game = None
        self.awaiting_input = False
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        if self.game:
            for r in range(6):
                for c in range(7):
                    x0 = c * 100
                    y0 = r * 100
                    x1 = x0 + 100
                    y1 = y0 + 100
                    val = self.game.board.grid[r][c]
                    color = "white" if val == 0 else ("red" if val == 1 else "yellow")
                    self.canvas.create_oval(x0+10, y0+10, x1-10, y1-10, fill=color)

    def on_click(self, event):
        if not self.game or not self.awaiting_input:
            return
        col = event.x // 100
        current_player = self.game.players[self.game.current_turn]
        if isinstance(current_player, HumanPlayer):
            current_player.get_move = lambda board: col
            self.awaiting_input = False

    def start_game(self):
        def create_player(selection, player_id):
            if selection == "Human":
                return HumanPlayer(f"Player {player_id}", player_id)
            else:
                cls = next(cls for name, cls in self.bot_classes if name == selection)
                return cls(f"Bot {player_id}", player_id)

        self.players = [
            create_player(self.bot1_var.get(), 1),
            create_player(self.bot2_var.get(), 2)
        ]
        time_limit = self.time_limit_var.get()
        self.game = Game(*self.players, time_limit=time_limit)
        self.draw_board()

        def run():
            while True:
                current_player = self.game.players[self.game.current_turn]
                if isinstance(current_player, HumanPlayer):
                    self.awaiting_input = True
                    while self.awaiting_input:
                        time.sleep(0.1)
                result = self.game.play_turn()
                self.draw_board()
                if result:
                    self.canvas.create_text(350, 300, text=result, fill="white", font=("Arial", 32))
                    break
                time.sleep(0.5)

        threading.Thread(target=run).start()

    def reset_ui(self):
        self.game = None
        self.awaiting_input = False
        self.draw_board()

    def run(self):
        self.root.mainloop()
