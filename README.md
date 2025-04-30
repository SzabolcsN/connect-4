# Connect 4 Bot Development Guide

This document explains how to create AI players (bots) for the Connect 4 project and outlines the features added to support external executable bots and timed thinking constraints.

---

## Bot Directories

- **Python bots** go in: `bots/`
- **Executable bots** (C, Rust, etc.): `bots_exe/`  
  These are automatically discovered if they are executable files.

---

## Bot Types

### 1. Python Bots

Each bot must:

1. Inherit from `game.player.Player`
2. Implement the method:
```python
def get_move(self, board_state, time_limit=None):
    # return an integer between 0 and 6
```

#### Constructor

```python
def __init__(self, name, player_id):
    super().__init__(name, player_id)
```

#### Method Details

- `board_state` is a 6x7 list of integers:
  - `0`: empty cell
  - `1`: Player 1
  - `2`: Player 2
- `time_limit`: seconds remaining for the move (optional, float)
- Return the index (0–6) where the bot wants to play.

> If your bot doesn’t use `time_limit`, you can safely ignore it.

---

### 2. Executable Bots

Executable bots are external programs (e.g., C or Rust binaries) that communicate via **STDIN/STDOUT**.

#### Input (to bot)

One line of JSON:
```json
{
  "board": [[...]],
  "player_id": 1,
  "time_limit": 2000
}
```

- `board`: a 6x7 matrix
- `player_id`: 1 or 2
- `time_limit`: milliseconds remaining for the move

#### Output (from bot)

Single line:
```
3
```

> Just print the chosen column number.

---

## Time Control

- Bots (Python or executables) are given a time limit per move.
- This is configured in the GUI before the game starts.
- Executables are forcibly terminated if they exceed the time.
- Python bots are trusted to obey the soft time limit.

---

## Example Python Bot

```python
from game.player import Player

class MyBot(Player):
    def __init__(self, name, player_id):
        super().__init__(name, player_id)

    def get_move(self, board_state, time_limit=None):
        for col in range(7):
            if board_state[0][col] == 0:
                return col
        return 0
```

---

## Example Executable Bot in C

```c

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int main() {
    char buffer[4096];
    fgets(buffer, sizeof(buffer), stdin);
    int board[6][7] = {{0}};
    int r = 0, c = 0;
    char *p = strchr(buffer, '[');
    while (p && r < 6) {
        p++;
        if (*p == '[') {
            c = 0; p++;
            while (*p && *p != ']') {
                if (*p >= '0' && *p <= '9') board[r][c++] = *p - '0';
                p++;
            }
            r++;
        }
    }
    for (int col = 0; col < 7; col++) if (board[0][col] == 0) return printf("%d\n", col), 0;
    return printf("0\n"), 0;
}

```

---

## Example Executable Bot in Rust

```rust

use std::io::Read;
use serde::Deserialize;

#[derive(Deserialize)]
struct Input {
    board: Vec<Vec<u8>>,
    player_id: u8,
    time_limit: u64
}

fn main() {
    let mut buffer = String::new();
    std::io::stdin().read_to_string(&mut buffer).unwrap();
    let input: Input = serde_json::from_str(&buffer).unwrap();
    for col in 0..7 {
        if input.board[0][col] == 0 {
            println!("{}", col);
            return;
        }
    }
    println!("0");
}

```

---

## Testing

- Select any two bots (Python or executable) from the dropdowns in the GUI.
- You can adjust the allowed time per move using the GUI before starting.

---

## Tips for Smarter Bots

- Use simulation, evaluation, or search (e.g., Minimax).
- Add time-awareness to limit depth based on `time_limit`.
- Block winning moves and prioritize center control.

---

## Naming Conventions

- **Files**: use `snake_case` → `my_bot.py`, `center_priority_bot.c`
- **Classes**: use `PascalCase` → `CenterPriorityBot`
- Executables will appear as `[Exec] filename` in the UI.

---

Enjoy building smart (and sneaky) Connect 4 bots!
