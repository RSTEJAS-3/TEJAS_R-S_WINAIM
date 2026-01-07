# ...existing code...
import tkinter as tk
from tkinter import messagebox
import random

# optional Windows sound support; safe fallback if not available
try:
    import winsound
except Exception:
    winsound = None

class TicTacToeApp:
    def __init__(self, master):
        self.master = master
        master.title("Tic Tac Toe")

        # game state
        self.current_player = "X"
        self.board = [" " for _ in range(9)]
        self.buttons = []

        # mode, score, and sound controls
        self.mode_var = tk.StringVar(value="PvP")  # "PvP" or "PvC"
        self.sound_var = tk.BooleanVar(value=True)
        self.scores = {"X": 0, "O": 0, "Draws": 0}

        # top control frame
        ctrl = tk.Frame(master)
        ctrl.grid(row=0, column=0, columnspan=3, pady=(6, 0))

        tk.Radiobutton(ctrl, text="2 Players", variable=self.mode_var, value="PvP",
                       command=self.on_mode_change).pack(side="left", padx=4)
        tk.Radiobutton(ctrl, text="Single Player", variable=self.mode_var, value="PvC",
                       command=self.on_mode_change).pack(side="left", padx=4)
        tk.Checkbutton(ctrl, text="Sound", variable=self.sound_var).pack(side="left", padx=8)
        tk.Button(ctrl, text="Reset Board", command=self.reset).pack(side="left", padx=6)
        tk.Button(ctrl, text="Reset Scores", command=self.reset_scores).pack(side="left", padx=6)

        # status and score labels
        self.status = tk.Label(master, text=f"Player {self.current_player}'s turn", font=("Arial", 14))
        self.status.grid(row=1, column=0, columnspan=3, pady=(6, 0))

        self.score_label = tk.Label(master, text=self.score_text(), font=("Arial", 10))
        self.score_label.grid(row=2, column=0, columnspan=3, pady=(0, 6))

        # board buttons
        for i in range(9):
            btn = tk.Button(master, text=" ", width=6, height=3, font=("Arial", 20),
                            command=lambda i=i: self.on_click(i))
            btn.grid(row=3 + i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        # ensure a fresh start
        self.reset()

    def score_text(self):
        return f"X: {self.scores['X']}    O: {self.scores['O']}    Draws: {self.scores['Draws']}"

    def on_mode_change(self):
        # switching mode resets the board and keeps scores
        self.reset()

    def play_sound(self, kind):
        if not self.sound_var.get() or not winsound:
            return
        try:
            if kind == "move":
                winsound.MessageBeep(winsound.MB_OK)
            elif kind == "win":
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            elif kind == "draw":
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
        except Exception:
            # fallback: try a beep
            try:
                winsound.Beep(800, 100)
            except Exception:
                pass

    def on_click(self, index):
        if self.board[index] != " ":
            return
        self.make_move(index, self.current_player)
        self.play_sound("move")

        if self.check_win(self.current_player):
            self.end_game(f"Player {self.current_player} wins!")
            return
        if self.check_draw():
            self.end_game("It's a draw!")
            return

        # switch player
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status.config(text=f"Player {self.current_player}'s turn")

        # if single player and it's O (computer), schedule computer move
        if self.mode_var.get() == "PvC" and self.current_player == "O":
            # short delay so user sees the move and button state change
            self.master.after(250, self.computer_move)

    def make_move(self, index, player):
        self.board[index] = player
        self.buttons[index].config(text=player, state="disabled")

    def computer_move(self):
        if self.check_win("X") or self.check_win("O") or self.check_draw():
            return
        # perfect play via minimax
        best_score = -999
        best_move = None
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                score = self.minimax(False)
                self.board[i] = " "
                if score > best_score:
                    best_score = score
                    best_move = i
        # if best_move none (shouldn't happen), pick random
        if best_move is None:
            choices = [i for i in range(9) if self.board[i] == " "]
            if choices:
                best_move = random.choice(choices)
        if best_move is not None:
            self.make_move(best_move, "O")
            self.play_sound("move")
            if self.check_win("O"):
                self.end_game("Computer wins!")
                return
            if self.check_draw():
                self.end_game("It's a draw!")
                return
            self.current_player = "X"
            self.status.config(text=f"Player {self.current_player}'s turn")

    def minimax(self, is_maximizing):
        if self.check_win("O"):
            return 1
        if self.check_win("X"):
            return -1
        if self.check_draw():
            return 0

        if is_maximizing:
            best = -999
            for i in range(9):
                if self.board[i] == " ":
                    self.board[i] = "O"
                    val = self.minimax(False)
                    self.board[i] = " "
                    best = max(best, val)
            return best
        else:
            best = 999
            for i in range(9):
                if self.board[i] == " ":
                    self.board[i] = "X"
                    val = self.minimax(True)
                    self.board[i] = " "
                    best = min(best, val)
            return best

    def check_win(self, player):
        win_positions = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        return any(self.board[a]==self.board[b]==self.board[c]==player for a,b,c in win_positions)

    def check_draw(self):
        return all(cell != " " for cell in self.board)

    def end_game(self, message):
        # update scores
        if "wins" in message:
            winner = "X" if "Player X" in message else ("O" if "Player O" in message else "O")
            self.scores[winner] += 1
            self.play_sound("win")
        else:
            self.scores["Draws"] += 1
            self.play_sound("draw")

        self.score_label.config(text=self.score_text())

        # prompt for replay
        if messagebox.askyesno("Game Over", f"{message}\n\nPlay again?"):
            # keep mode and scores, reset board
            self.reset(keep_scores=True)
        else:
            self.master.destroy()

    def reset(self, keep_scores=False):
        self.board = [" " for _ in range(9)]
        for btn in self.buttons:
            btn.config(text=" ", state="normal")
        self.current_player = "X"
        self.status.config(text=f"Player {self.current_player}'s turn")
        if not keep_scores:
            self.score_label.config(text=self.score_text())

    def reset_scores(self):
        self.scores = {"X":0, "O":0, "Draws":0}
        self.score_label.config(text=self.score_text())

if __name__ == "__main__":
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()