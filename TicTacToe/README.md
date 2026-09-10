# Tic-Tac-Toe (2 Players GUI)

A modern, visually polished two-player Tic-Tac-Toe game built in Python using `tkinter`.

## Features
- **Sleek Theme**: Modern dark theme with custom styling for macOS and Windows.
- **Scoreboard**: Tracks Player X wins, Player O wins, and Ties.
- **Status bar**: Dynamic text showing current turn and game outcomes.
- **Round controls**:
  - `Next Round` clears the grid and lets you play again while retaining scores.
  - `Reset Game` resets the entire board and score records.

## How to Play
1. Player X starts. Click any grid cell to place an "X".
2. Turn switches to Player O. Click any empty grid cell to place an "O".
3. The game checks for a win (3 marks in a line: horizontal, vertical, or diagonal) or a tie.
4. Winning cells will highlight, or the board will color-code a tie.
5. Click **Next Round** to play again, or **Reset Game** to restart scores.

## Running the Game

Run the Python script directly using your terminal:

```bash
python TicTacToe/game.py
```
or inside the `TicTacToe` directory:
```bash
python game.py
```
