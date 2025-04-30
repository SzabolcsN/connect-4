use std::io::{self, Read};
use serde::Deserialize;
use std::thread;
use std::time::Duration;

#[derive(Deserialize)]
struct Input {
    board: Vec<Vec<u8>>,
    player_id: u8,
    time_limit: u64,  // in milliseconds
}

fn main() {
    // Read the full stdin input
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).unwrap();

    // Parse input JSON into struct
    let input: Input = match serde_json::from_str(&buffer) {
        Ok(i) => i,
        Err(e) => {
            eprintln!("Failed to parse input: {}", e);
            return;
        }
    };

    let board = input.board;

    // Optional: simulate 20% delay of allowed time
    thread::sleep(Duration::from_millis(input.time_limit / 5));

    // Center-first column preference
    let preferred = [3, 2, 4, 1, 5, 0, 6];

    for &col in &preferred {
        if board[0][col] == 0 {
            println!("{}", col);
            return;
        }
    }

    // fallback
    println!("0");
}
