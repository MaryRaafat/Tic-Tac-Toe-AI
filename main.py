import tkinter as tk
from tkinter import messagebox
import math

HUMAN = 'X'
AI = 'O'
EMPTY = ' '

WIN_LINES = [
    (0,1,2), (3,4,5), (6,7,8),
    (0,3,6), (1,4,7), (2,5,8),
    (0,4,8), (2,4,6)
]

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        root.title("Tic Tac Toe")


        self.bg_color = "#141421"
        self.button_color = "#222238"
        self.button_active = "#35355a"
        self.text_color = "#ffffff"
        self.win_color = "#15d177"

        root.configure(bg=self.bg_color)

        self.board = [EMPTY] * 9
        self.buttons = []
        self.human_starts = True
        # Scoreboard
        self.human_score = 0
        self.ai_score = 0
        self.draw_score = 0

        
        title = tk.Label(root, text="Tic Tac Toe", font=("Arial", 26, "bold"),
                         fg=self.text_color, bg=self.bg_color)
        title.pack(pady=10)

        # Scoreboard
        score_frame = tk.Frame(root, bg=self.bg_color)
        score_frame.pack(pady=5)

        self.score_label = tk.Label(score_frame,
            text=self.get_score_text(),
            font=("Arial", 14, "bold"),
            fg=self.text_color, bg=self.bg_color)
        self.score_label.pack()

        # Grid
        grid = tk.Frame(root, bg=self.bg_color)
        grid.pack(pady=10)

        for i in range(9):
            b = tk.Button(
                grid,
                text=' ',
                font=('Arial', 26, "bold"),
                width=4,
                height=1,
                fg=self.text_color,
                bg=self.button_color,
                activebackground=self.button_active,
                command=lambda i=i: self.on_click(i)
            )
            b.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(b)

        # Controls
        bot = tk.Frame(root, bg=self.bg_color)
        bot.pack(pady=10)

        self.make_btn(bot, "Restart", self.restart).pack(side='left', padx=5)
        self.make_btn(bot, "Computer Starts", self.computer_start).pack(side='left', padx=5)
        self.make_btn(bot, "Human starts", self.human_start).pack(side='left', padx=5)

    def make_btn(self, parent, text, cmd):
        return tk.Button(
            parent,
            text=text,
            font=("Arial", 12, "bold"),
            bg="#2f2f4f",
            fg=self.text_color,
            activebackground="#47476d",
            width=12,
            command=cmd
        )

    def get_score_text(self):
        return f" (X): Human {self.human_score}   |    (O): Computer   {self.ai_score}   |    : Draw  {self.draw_score} "

    def update_scoreboard(self):
        self.score_label.config(text=self.get_score_text())

    def human_start(self):
        self.human_starts = True
        self.restart()

    def computer_start(self):
        self.human_starts = False
        self.restart()
        self.root.after(300, self.ai_move)

    def restart(self):
        self.board = [EMPTY] * 9
        for b in self.buttons:
            b.config(text=' ', state='normal', bg=self.button_color)
        self.update_scoreboard()

    def check_winner(self):
        for a, b, c in WIN_LINES:
            if self.board[a] == self.board[b] == self.board[c] != EMPTY:
                return (self.board[a], (a, b, c))
        if EMPTY not in self.board:
            return ('Draw', None)
        return None

    def color_win_line(self, line):
        for i in line:
            self.buttons[i].config(bg=self.win_color)

    def on_click(self, i):
        if self.board[i] != EMPTY:
            return

        self.board[i] = HUMAN
        self.buttons[i].config(text=HUMAN, state='disabled')

        winner = self.check_winner()
        if winner:
            self.handle_end(winner)
            return

        self.root.after(200, self.ai_move)

    def handle_end(self, result):
        winner, line = result

        if winner == 'Draw':
            self.draw_score += 1
            messagebox.showinfo("Result", "Draw!")
        else:
            if winner == HUMAN:
                self.human_score += 1
                messagebox.showinfo("Result", "Win! 🎉")
            else:
                self.ai_score += 1
                messagebox.showinfo("Result", "Computer win 😈")

            self.color_win_line(line)

        self.update_scoreboard()

        for b in self.buttons:
            b.config(state='disabled')

    def available_moves(self, board):
        return [i for i, v in enumerate(board) if v == EMPTY]

    def minimax(self, board, is_maximizing, alpha, beta):
        winner = self.check_winner_board(board)
        if winner == AI:
            return 1
        elif winner == HUMAN:
            return -1
        elif winner == 'Draw':
            return 0

        if is_maximizing:
            best = -math.inf
            for mv in self.available_moves(board):
                board[mv] = AI
                val = self.minimax(board, False, alpha, beta)
                board[mv] = EMPTY
                best = max(best, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
            return best
        else:
            best = math.inf
            for mv in self.available_moves(board):
                board[mv] = HUMAN
                val = self.minimax(board, True, alpha, beta)
                board[mv] = EMPTY
                best = min(best, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break
            return best

    def check_winner_board(self, board):
        for a, b, c in WIN_LINES:
            if board[a] == board[b] == board[c] != EMPTY:
                return board[a]
        if EMPTY not in board:
            return 'Draw'
        return None

    def best_move(self):
        best_val = -math.inf
        best_mv = None
        for mv in self.available_moves(self.board):
            self.board[mv] = AI
            val = self.minimax(self.board, False, -math.inf, math.inf)
            self.board[mv] = EMPTY
            if val > best_val:
                best_val = val
                best_mv = mv
        return best_mv

    def ai_move(self):
        mv = self.best_move()
        if mv is None:
            return

        self.board[mv] = AI
        self.buttons[mv].config(text=AI, state='disabled')

        winner = self.check_winner()
        if winner:
            self.handle_end(winner)


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
