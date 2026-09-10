import tkinter as tk
from tkinter import font as tkfont

# Color Palette (Modern Dark Theme)
BG_COLOR = "#1e1e24"          # Deep dark background
CARD_BG = "#2b2d42"           # Dark slate for cell cards
CARD_HOVER = "#3d405b"        # Slightly lighter slate for hover
TEXT_COLOR = "#edf2f4"        # Crisp light text
MUTED_TEXT = "#abb2bf"        # Muted grey text
COLOR_X = "#00f5d4"           # Vibrant teal/cyan for Player X
COLOR_O = "#ff6b6b"           # Vibrant coral/red for Player O
WIN_BG = "#2a9d8f"            # Highlight color for winning cells
TIE_BG = "#4a4e69"            # Highlight color for tie cells
BTN_RESET_BG = "#8338ec"      # Vibrant purple for Reset buttons
BTN_HOVER_BG = "#9b5de5"

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe: 2 Players")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)
        
        # Center the window on the screen
        window_width = 420
        window_height = 580
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height/2 - window_height/2)
        position_right = int(screen_width/2 - window_width/2)
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        # Game State Variables
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.scores = {"X": 0, "O": 0, "Ties": 0}
        self.game_active = True
        self.winning_cells = []

        # Define Fonts
        self.title_font = tkfont.Font(family="Helvetica", size=22, weight="bold")
        self.status_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
        self.score_font = tkfont.Font(family="Helvetica", size=12, weight="normal")
        self.cell_font = tkfont.Font(family="Helvetica", size=32, weight="bold")
        self.btn_font = tkfont.Font(family="Helvetica", size=11, weight="bold")

        # Create Layout Components
        self.create_header()
        self.create_scoreboard()
        self.create_grid()
        self.create_controls()

        # Update initial turn status
        self.update_status()

    def create_header(self):
        # Header Container
        header_frame = tk.Frame(self.root, bg=BG_COLOR)
        header_frame.pack(fill="x", pady=15)

        # Main Title Label
        title_label = tk.Label(
            header_frame, 
            text="TIC-TAC-TOE", 
            font=self.title_font, 
            bg=BG_COLOR, 
            fg=TEXT_COLOR
        )
        title_label.pack()

        # Status Label (Shows whose turn or who won)
        self.status_label = tk.Label(
            header_frame, 
            text="", 
            font=self.status_font, 
            bg=BG_COLOR, 
            fg=COLOR_X,
            pady=5
        )
        self.status_label.pack()

    def create_scoreboard(self):
        # Scoreboard Frame
        score_frame = tk.Frame(self.root, bg=BG_COLOR)
        score_frame.pack(fill="x", pady=(0, 10))

        # Config columns to expand evenly
        score_frame.columnconfigure(0, weight=1)
        score_frame.columnconfigure(1, weight=1)
        score_frame.columnconfigure(2, weight=1)

        # Player X Score Label
        self.score_x_label = tk.Label(
            score_frame, 
            text="Player X\n0", 
            font=self.score_font, 
            bg=BG_COLOR, 
            fg=COLOR_X,
            justify="center"
        )
        self.score_x_label.grid(row=0, column=0, sticky="nsew")

        # Ties Score Label
        self.score_ties_label = tk.Label(
            score_frame, 
            text="Ties\n0", 
            font=self.score_font, 
            bg=BG_COLOR, 
            fg=MUTED_TEXT,
            justify="center"
        )
        self.score_ties_label.grid(row=0, column=1, sticky="nsew")

        # Player O Score Label
        self.score_o_label = tk.Label(
            score_frame, 
            text="Player O\n0", 
            font=self.score_font, 
            bg=BG_COLOR, 
            fg=COLOR_O,
            justify="center"
        )
        self.score_o_label.grid(row=0, column=2, sticky="nsew")

    def create_grid(self):
        # Main Grid container with padding
        self.grid_container = tk.Frame(self.root, bg=BG_COLOR)
        self.grid_container.pack(fill="both", expand=True, padx=25, pady=5)

        self.cells = [[None for _ in range(3)] for _ in range(3)]

        # Constructing the 3x3 Grid
        for r in range(3):
            self.grid_container.rowconfigure(r, weight=1)
            for c in range(3):
                self.grid_container.columnconfigure(c, weight=1)
                
                # Outer border effect using a sub-frame
                cell_frame = tk.Frame(self.grid_container, bg=BG_COLOR)
                cell_frame.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)
                cell_frame.rowconfigure(0, weight=1)
                cell_frame.columnconfigure(0, weight=1)

                # Cell Label (acting as interactive button)
                cell_lbl = tk.Label(
                    cell_frame, 
                    text="", 
                    font=self.cell_font, 
                    bg=CARD_BG, 
                    fg=TEXT_COLOR, 
                    cursor="hand2", 
                    anchor="center",
                    relief="flat"
                )
                cell_lbl.grid(row=0, column=0, sticky="nsew")
                
                # Event Bindings
                cell_lbl.bind("<Button-1>", lambda event, row=r, col=c: self.on_cell_click(row, col))
                cell_lbl.bind("<Enter>", lambda event, lbl=cell_lbl, row=r, col=c: self.on_cell_hover(lbl, row, col))
                cell_lbl.bind("<Leave>", lambda event, lbl=cell_lbl, row=r, col=c: self.on_cell_leave(lbl, row, col))
                
                self.cells[r][c] = cell_lbl

    def create_controls(self):
        # Controls Frame
        controls_frame = tk.Frame(self.root, bg=BG_COLOR)
        controls_frame.pack(fill="x", pady=20)

        # Next Round Button
        self.btn_next = tk.Button(
            controls_frame,
            text="Next Round",
            font=self.btn_font,
            bg=BTN_RESET_BG,
            fg=TEXT_COLOR,
            activebackground=BTN_HOVER_BG,
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.next_round
        )
        self.btn_next.pack(side="left", expand=True, padx=(30, 10), fill="x")

        # Reset All Button
        self.btn_reset = tk.Button(
            controls_frame,
            text="Reset Game",
            font=self.btn_font,
            bg=CARD_BG,
            fg=MUTED_TEXT,
            activebackground=CARD_HOVER,
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.reset_all
        )
        self.btn_reset.pack(side="right", expand=True, padx=(10, 30), fill="x")

        # Platform check for background color styling on Mac
        try:
            self.btn_next.configure(highlightbackground=BG_COLOR)
            self.btn_reset.configure(highlightbackground=BG_COLOR)
        except Exception:
            pass

    # Game Loop Logic Interactions
    def on_cell_click(self, row, col):
        if not self.game_active or self.board[row][col] != "":
            return

        # Place the mark
        self.board[row][col] = self.current_player
        cell_lbl = self.cells[row][col]
        cell_lbl.configure(
            text=self.current_player,
            fg=COLOR_X if self.current_player == "X" else COLOR_O,
            cursor=""
        )

        # Check for Win or Tie
        win_found, winning_coords = self.check_win()
        if win_found:
            self.game_active = False
            self.winning_cells = winning_coords
            self.scores[self.current_player] += 1
            self.highlight_win()
            self.update_scores()
            self.status_label.configure(
                text=f"Player {self.current_player} Wins!", 
                fg=COLOR_X if self.current_player == "X" else COLOR_O
            )
        elif self.check_tie():
            self.game_active = False
            self.scores["Ties"] += 1
            self.highlight_tie()
            self.update_scores()
            self.status_label.configure(text="It's a Tie!", fg=MUTED_TEXT)
        else:
            # Switch Turn
            self.current_player = "O" if self.current_player == "X" else "X"
            self.update_status()

    def on_cell_hover(self, label, row, col):
        # Hover effect if the game is active and cell is empty
        if self.game_active and self.board[row][col] == "":
            label.configure(bg=CARD_HOVER)

    def on_cell_leave(self, label, row, col):
        # Restore normal bg if the cell is not in a winning highlights state
        if (row, col) not in self.winning_cells and not (not self.game_active and self.board[row][col] == ""):
            label.configure(bg=CARD_BG)

    def check_win(self):
        # Check rows
        for r in range(3):
            if self.board[r][0] == self.board[r][1] == self.board[r][2] != "":
                return True, [(r, 0), (r, 1), (r, 2)]
        
        # Check columns
        for c in range(3):
            if self.board[0][c] == self.board[1][c] == self.board[2][c] != "":
                return True, [(0, c), (1, c), (2, c)]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True, [(0, 0), (1, 1), (2, 2)]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True, [(0, 2), (1, 1), (2, 0)]
            
        return False, []

    def check_tie(self):
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == "":
                    return False
        return True

    def highlight_win(self):
        # Highlight only winning cells
        for r, c in self.winning_cells:
            self.cells[r][c].configure(bg=WIN_BG, fg=TEXT_COLOR)

    def highlight_tie(self):
        # Highlight all cells in tie color
        for r in range(3):
            for c in range(3):
                self.cells[r][c].configure(bg=TIE_BG, fg=MUTED_TEXT)

    def update_status(self):
        if self.current_player == "X":
            self.status_label.configure(text="Player X's Turn", fg=COLOR_X)
        else:
            self.status_label.configure(text="Player O's Turn", fg=COLOR_O)

    def update_scores(self):
        self.score_x_label.configure(text=f"Player X\n{self.scores['X']}")
        self.score_ties_label.configure(text=f"Ties\n{self.scores['Ties']}")
        self.score_o_label.configure(text=f"Player O\n{self.scores['O']}")

    def next_round(self):
        # Reset game board logic, keep the score
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_active = True
        self.winning_cells = []
        self.current_player = "X"
        self.update_status()

        # Reset board GUI
        for r in range(3):
            for c in range(3):
                cell_lbl = self.cells[r][c]
                cell_lbl.configure(text="", bg=CARD_BG, cursor="hand2")

    def reset_all(self):
        # Reset scores
        self.scores = {"X": 0, "O": 0, "Ties": 0}
        self.update_scores()
        # Reset round
        self.next_round()

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
