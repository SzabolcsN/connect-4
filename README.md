# Connect 4 Bot Development Guide

This document explains how to create new AI players (bots) for the Connect 4 project.

---

## Where to Add Bots

All bot files must be placed in the `bots/` directory. Each file should contain a single Python class that inherits from the `Player` base class.

---

## Bot Class Requirements

Each bot must:

1. Inherit from `game.player.Player`
2. Implement the method:

```python
def get_move(self, board_state):
    # return an integer between 0 and 6
```

### Constructor
You should also define a constructor that accepts `name` and `player_id`:

```python
def __init__(self, name, player_id):
    super().__init__(name, player_id)
```

### Method Details
- `get_move(board_state)`
  - `board_state` is a 6x7 list of integers:
    - `0`: empty cell
    - `1`: Player 1
    - `2`: Player 2
  - Return the index (0–6) of the column where the bot wants to place a token.

---

## Constraints and Expectations

- Bots must not modify `board_state` directly.
- Return values must be valid columns (where the top cell is `0`).
- If you simulate or evaluate moves, use a deep copy of the board.
- You can use any strategy (random, rule-based, search-based, etc.).

---

## Example Structure

```python
from game.player import Player

class MyBot(Player):
    def __init__(self, name, player_id):
        super().__init__(name, player_id)

    def get_move(self, board_state):
        for col in range(7):
            if board_state[0][col] == 0:
                return col
        return 0  # fallback
```

---

## Dynamic Loading

Bots are automatically discovered by the app using Python reflection. You don’t need to register them manually. Just add your file to `bots/` and restart the app.

Premade bots included in the project are marked with [Builtin] in the dropdown menu. Custom bots you create will appear without that tag.
To enable this, each premade bot class includes a special attribute:
```python
builtin = True
```
---

## Testing

You can select any two bots from the dropdowns in the app to test them against each other or against a human.

---

## Tips for Advanced Bots

- Use simulation (e.g., try moves and evaluate board).
- Implement minimax or other search algorithms.
- Block opponent's winning moves or prioritize winning paths.
- Consider performance if using deeper search.

---

## Naming Conventions

- File name should be snake_case (e.g., `greedy_bot.py`)
- Class name should be PascalCase (e.g., `GreedyBot`)
