"""
╔══════════════════════════════════════════════════════════════════╗
║          TIC TAC TOE — GOLDEN EDITION                            ║
║  Python 3.8+  ·  Zero external dependencies  ·  Single file     ║
╚══════════════════════════════════════════════════════════════════╝
Run:  python goldenresponse1.py
"""

import tkinter as tk
from tkinter import font as tkfont
import math, random

# ───────────────────────────────────────────────────────────────────
#  CONSTANTS
# ───────────────────────────────────────────────────────────────────
PLAYER_X   = "X"
PLAYER_O   = "O"
EMPTY      = ""

CELL       = 120          # px per cell
BOARD_PX   = CELL * 3     # 360 px total board

WIN_COMBOS = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)

# ───────────────────────────────────────────────────────────────────
#  COLOUR PALETTE
# ───────────────────────────────────────────────────────────────────
C = {
    "bg":      "#0d0d1a",
    "surface": "#16213e",
    "panel":   "#1a1a2e",
    "accent":  "#0f3460",
    "hover":   "#1e3a5f",
    "x":       "#e94560",
    "o":       "#00b4d8",
    "gold":    "#ffd700",
    "success": "#4ecca3",
    "white":   "#e8eaf6",
    "muted":   "#8892b0",
    "dark":    "#0d0d1a",
    "easy":    "#4ecca3",
    "medium":  "#f0a500",
    "hard":    "#e94560",
}


# ───────────────────────────────────────────────────────────────────
#  APPLICATION
# ───────────────────────────────────────────────────────────────────
class TicTacToe:

    # ── INIT ────────────────────────────────────────────────────────
    def __init__(self):
        self.board:          list = [EMPTY] * 9
        self.current_player: str  = PLAYER_X
        self.game_active:    bool = False
        self.animating:      bool = False
        self.scores:         dict = {PLAYER_X: 0, PLAYER_O: 0, "draws": 0}

        # Tkinter root
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe — Golden Edition")
        self.root.geometry("500x780")
        self.root.minsize(500, 780)
        self.root.resizable(False, False)
        self.root.configure(bg=C["bg"])

        # Tk vars (after root creation)
        self.game_mode     = tk.StringVar(value="ai")
        self.ai_difficulty = tk.StringVar(value="medium")

        # Canvas item registries
        self.cell_rects: list = []
        self.cell_texts: list = []

        self._build_ui()
        self.root.mainloop()

    # ── UI BUILD ────────────────────────────────────────────────────
    def _build_ui(self):

        # ── Title ──────────────────────────────────────────────────
        tf = tk.Frame(self.root, bg=C["bg"])
        tf.pack(pady=(20, 6))
        tk.Label(tf, text="TIC  TAC  TOE",
                 font=("Helvetica", 26, "bold"),
                 bg=C["bg"], fg=C["white"]).pack()
        tk.Label(tf, text="G O L D E N   E D I T I O N",
                 font=("Helvetica", 9, "bold"),
                 bg=C["bg"], fg=C["muted"]).pack(pady=(2, 0))

        # ── Mode panel ─────────────────────────────────────────────
        mode_panel = tk.Frame(self.root, bg=C["accent"],
                              bd=0, highlightthickness=0)
        mode_panel.pack(padx=30, pady=8, fill="x")

        tk.Label(mode_panel, text="GAME MODE",
                 font=("Helvetica", 8, "bold"),
                 bg=C["accent"], fg=C["muted"]).pack(pady=(10, 4))

        mode_row = tk.Frame(mode_panel, bg=C["accent"])
        mode_row.pack(pady=(0, 10))

        self.mode_btns: dict = {}
        for mode_val, label in (("ai", "🤖  vs AI"), ("human", "👥  2 Players")):
            btn = tk.Button(
                mode_row, text=label,
                font=("Helvetica", 10, "bold"),
                relief="flat", padx=20, pady=7,
                cursor="hand2", bd=0,
                command=lambda m=mode_val: self.set_mode(m)
            )
            btn.pack(side="left", padx=6)
            self.mode_btns[mode_val] = btn
        self._refresh_mode_buttons()

        # ── Difficulty row ─────────────────────────────────────────
        self.diff_frame = tk.Frame(self.root, bg=C["bg"])
        self.diff_frame.pack(pady=(4, 0))

        tk.Label(self.diff_frame, text="DIFFICULTY:",
                 font=("Helvetica", 9, "bold"),
                 bg=C["bg"], fg=C["muted"]).pack(side="left", padx=(0, 8))

        for level in ("easy", "medium", "hard"):
            tk.Radiobutton(
                self.diff_frame,
                text=level.capitalize(),
                variable=self.ai_difficulty,
                value=level,
                font=("Helvetica", 10, "bold"),
                fg=C[level], bg=C["bg"],
                activebackground=C["bg"],
                activeforeground=C[level],
                selectcolor=C["accent"],
                cursor="hand2",
                command=self._on_difficulty_change,
            ).pack(side="left", padx=5)

        # ── Scoreboard ─────────────────────────────────────────────
        score_card = tk.Frame(self.root, bg=C["surface"],
                              bd=0, highlightthickness=0)
        score_card.pack(padx=30, pady=10, fill="x")
        score_card.columnconfigure((0, 1, 2), weight=1)

        self.score_vals:   dict = {}
        self.score_titles: dict = {}
        score_defs = (
            (PLAYER_X, "Player X", C["x"]),
            ("draws",  "Draws",    C["muted"]),
            (PLAYER_O, "AI",       C["o"]),
        )
        for col, (key, title, color) in enumerate(score_defs):
            cell_f = tk.Frame(score_card, bg=C["surface"])
            cell_f.grid(row=0, column=col, padx=10, pady=12, sticky="nsew")
            t_lbl = tk.Label(cell_f, text=title,
                             font=("Helvetica", 9, "bold"),
                             bg=C["surface"], fg=color)
            t_lbl.pack()
            v_lbl = tk.Label(cell_f, text="0",
                             font=("Helvetica", 28, "bold"),
                             bg=C["surface"], fg=color)
            v_lbl.pack()
            self.score_titles[key] = t_lbl
            self.score_vals[key]   = v_lbl

        # ── Turn indicator ─────────────────────────────────────────
        self.turn_label = tk.Label(
            self.root,
            text="Press  ▶  START  to begin",
            font=("Helvetica", 12, "bold"),
            bg=C["bg"], fg=C["muted"]
        )
        self.turn_label.pack(pady=(4, 6))

        # ── Canvas ─────────────────────────────────────────────────
        canvas_frame = tk.Frame(self.root, bg=C["accent"], bd=2)
        canvas_frame.pack()
        self.canvas = tk.Canvas(
            canvas_frame,
            width=BOARD_PX, height=BOARD_PX,
            bg=C["surface"],
            highlightthickness=0,
        )
        self.canvas.pack()
        self._draw_grid()
        self._create_cells()

        # ── Status bar ─────────────────────────────────────────────
        self.status_label = tk.Label(
            self.root, text="",
            font=("Helvetica", 11, "bold"),
            bg=C["bg"], fg=C["success"]
        )
        self.status_label.pack(pady=(6, 2))

        # ── Control buttons ────────────────────────────────────────
        ctrl = tk.Frame(self.root, bg=C["bg"])
        ctrl.pack(pady=10)

        self.start_btn = tk.Button(
            ctrl,
            text="▶   START GAME",
            font=("Helvetica", 13, "bold"),
            bg=C["success"], fg=C["dark"],
            relief="flat", padx=26, pady=10,
            cursor="hand2", bd=0,
            command=self.start_game,
        )
        self.start_btn.pack(side="left", padx=8)
        self._add_hover(self.start_btn, C["success"], "#3ab88a", C["dark"])

        reset_btn = tk.Button(
            ctrl,
            text="↺   RESET SCORES",
            font=("Helvetica", 13, "bold"),
            bg=C["accent"], fg=C["white"],
            relief="flat", padx=26, pady=10,
            cursor="hand2", bd=0,
            command=self.reset_scores,
        )
        reset_btn.pack(side="left", padx=8)
        self._add_hover(reset_btn, C["accent"], C["hover"], C["white"])

    # ── CANVAS SETUP ────────────────────────────────────────────────
    def _draw_grid(self):
        self.canvas.delete("grid")
        pad = 10
        for i in (CELL, CELL * 2):
            self.canvas.create_line(i, pad, i, BOARD_PX - pad,
                                    fill=C["accent"], width=2, tags="grid")
            self.canvas.create_line(pad, i, BOARD_PX - pad, i,
                                    fill=C["accent"], width=2, tags="grid")

    def _create_cells(self):
        PAD = 4
        for i in range(9):
            row, col = divmod(i, 3)
            x0 = col * CELL + PAD
            y0 = row * CELL + PAD
            x1 = x0 + CELL - PAD * 2
            y1 = y0 + CELL - PAD * 2
            cx = col * CELL + CELL // 2
            cy = row * CELL + CELL // 2

            r_tag = f"rect_{i}"
            t_tag = f"text_{i}"

            rect = self.canvas.create_rectangle(
                x0, y0, x1, y1,
                fill=C["surface"], outline="", tags=r_tag
            )
            text = self.canvas.create_text(
                cx, cy, text="",
                font=("Helvetica", 44, "bold"),
                fill=C["white"], tags=t_tag
            )
            self.cell_rects.append(rect)
            self.cell_texts.append(text)

            for tag in (r_tag, t_tag):
                self.canvas.tag_bind(tag, "<Button-1>",
                                     lambda e, idx=i: self.make_move(idx))
                self.canvas.tag_bind(tag, "<Enter>",
                                     lambda e, idx=i: self._hover_in(idx))
                self.canvas.tag_bind(tag, "<Leave>",
                                     lambda e, idx=i: self._hover_out(idx))

    # ── GAME FLOW ───────────────────────────────────────────────────
    def start_game(self):
        if self.animating:
            return
        self.board          = [EMPTY] * 9
        self.current_player = PLAYER_X
        self.game_active    = True
        self.animating      = False
        self.status_label.config(text="")
        self.start_btn.config(text="↺   NEW GAME")

        for i in range(9):
            self.canvas.itemconfig(self.cell_rects[i], fill=C["surface"])
            self.canvas.itemconfig(self.cell_texts[i],
                                   text="",
                                   font=("Helvetica", 44, "bold"),
                                   fill=C["white"])
        self._draw_grid()
        self._update_turn_label()

    def make_move(self, idx: int):
        if not self.game_active:       return
        if self.animating:             return
        if self.board[idx] != EMPTY:   return
        if self.game_mode.get() == "ai" and self.current_player == PLAYER_O:
            return
        self._place_marker(idx, self.current_player)

    def _place_marker(self, idx: int, player: str):
        self.animating  = True
        self.board[idx] = player
        color = C["x"] if player == PLAYER_X else C["o"]
        self.canvas.itemconfig(self.cell_texts[idx],
                               text=player, fill=color)
        self.canvas.itemconfig(self.cell_rects[idx], fill=C["accent"])
        self._animate_marker(idx)

    def _animate_marker(self, idx: int):
        sizes = (8, 16, 28, 40, 50, 46, 44)

        def step(n: int = 0):
            if n < len(sizes):
                self.canvas.itemconfig(
                    self.cell_texts[idx],
                    font=("Helvetica", sizes[n], "bold")
                )
                self.root.after(30, lambda: step(n + 1))
            else:
                self.canvas.itemconfig(
                    self.cell_texts[idx],
                    font=("Helvetica", 44, "bold")
                )
                self.animating = False
                self._evaluate_board()

        step()

    def _evaluate_board(self):
        combo = self._winning_combo(self.board)
        if combo:
            self._highlight_win(combo)
            self._game_over(self.board[combo[0]])
            return
        if EMPTY not in self.board:
            self._game_over(None)
            return
        self.current_player = self._opponent(self.current_player)
        self._update_turn_label()
        if self.game_mode.get() == "ai" and self.current_player == PLAYER_O:
            self.root.after(420, self._ai_move)

    # ── AI ENGINE ───────────────────────────────────────────────────
    def _ai_move(self):
        if not self.game_active:
            return
        d = self.ai_difficulty.get()
        if d == "easy":
            idx = self._random_move()
        elif d == "medium":
            idx = self._best_move() if random.random() < 0.65 else self._random_move()
        else:
            idx = self._best_move()
        if idx is not None:
            self._place_marker(idx, PLAYER_O)

    def _random_move(self):
        empty = [i for i, v in enumerate(self.board) if v == EMPTY]
        return random.choice(empty) if empty else None

    def _best_move(self):
        best_score, best_idx = -math.inf, None
        for i in range(9):
            if self.board[i] == EMPTY:
                self.board[i] = PLAYER_O
                score = self._minimax(self.board, 0, False, -math.inf, math.inf)
                self.board[i] = EMPTY
                if score > best_score:
                    best_score, best_idx = score, i
        return best_idx

    def _minimax(self, board, depth, is_max, alpha, beta):
        combo = self._winning_combo(board)
        if combo:
            w = board[combo[0]]
            return (10 - depth) if w == PLAYER_O else (depth - 10)
        if EMPTY not in board:
            return 0
        if is_max:
            best = -math.inf
            for i in range(9):
                if board[i] == EMPTY:
                    board[i] = PLAYER_O
                    best  = max(best, self._minimax(board, depth+1, False, alpha, beta))
                    board[i] = EMPTY
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
            return best
        else:
            best = math.inf
            for i in range(9):
                if board[i] == EMPTY:
                    board[i] = PLAYER_X
                    best  = min(best, self._minimax(board, depth+1, True, alpha, beta))
                    board[i] = EMPTY
                    beta  = min(beta, best)
                    if beta <= alpha:
                        break
            return best

    # ── WIN / DRAW DETECTION ────────────────────────────────────────
    def _winning_combo(self, board):
        for combo in WIN_COMBOS:
            a, b, c_ = combo
            if board[a] == board[b] == board[c_] != EMPTY:
                return combo
        return None

    # ── GAME OVER ───────────────────────────────────────────────────
    def _highlight_win(self, combo):
        for idx in combo:
            self.canvas.itemconfig(self.cell_rects[idx], fill=C["gold"])
            self.canvas.itemconfig(self.cell_texts[idx],
                                   fill=C["dark"],
                                   font=("Helvetica", 48, "bold"))

    def _game_over(self, winner):
        self.game_active = False
        self.start_btn.config(text="▶   PLAY AGAIN")
        if winner == PLAYER_X:
            self.scores[PLAYER_X] += 1
            msg, fg = "🎉  Player X Wins!", C["x"]
        elif winner == PLAYER_O:
            self.scores[PLAYER_O] += 1
            label = "AI" if self.game_mode.get() == "ai" else "Player O"
            msg, fg = f"🏆  {label} Wins!", C["o"]
        else:
            self.scores["draws"] += 1
            msg, fg = "🤝  It's a Draw!", C["gold"]

        self.turn_label.config(text=msg, fg=fg)
        self.status_label.config(
            text="Press  ▶  PLAY AGAIN  to continue",
            fg=C["muted"]
        )
        self._update_scores()

    # ── SCORE DISPLAY ───────────────────────────────────────────────
    def _update_scores(self):
        for key, lbl in self.score_vals.items():
            lbl.config(text=str(self.scores[key]))

    def reset_scores(self):
        self.scores = {PLAYER_X: 0, PLAYER_O: 0, "draws": 0}
        self._update_scores()
        self.status_label.config(text="✓  Scores reset", fg=C["success"])
        self.root.after(1200, lambda: self.status_label.config(text=""))
        self.start_game()

    # ── MODE & DIFFICULTY ───────────────────────────────────────────
    def set_mode(self, mode: str):
        self.game_mode.set(mode)
        self._refresh_mode_buttons()
        o_title = "AI" if mode == "ai" else "Player O"
        self.score_titles[PLAYER_O].config(text=o_title)
        if mode == "ai":
            self.diff_frame.pack(pady=(4, 0))
        else:
            self.diff_frame.pack_forget()

    def _refresh_mode_buttons(self):
        cur = self.game_mode.get()
        for m, btn in self.mode_btns.items():
            if m == cur:
                color = C["x"] if m == "ai" else C["o"]
                btn.config(bg=color, fg=C["white"])
            else:
                btn.config(bg=C["accent"], fg=C["muted"])

    def _on_difficulty_change(self):
        pass  # Radiobutton variable handles it automatically

    # ── HOVER ───────────────────────────────────────────────────────
    def _hover_in(self, idx: int):
        if (self.game_active and not self.animating
                and self.board[idx] == EMPTY
                and not (self.game_mode.get() == "ai"
                         and self.current_player == PLAYER_O)):
            self.canvas.itemconfig(self.cell_rects[idx], fill=C["hover"])

    def _hover_out(self, idx: int):
        if self.board[idx] == EMPTY:
            self.canvas.itemconfig(self.cell_rects[idx], fill=C["surface"])

    # ── TURN LABEL ──────────────────────────────────────────────────
    def _update_turn_label(self):
        if not self.game_active:
            return
        if self.current_player == PLAYER_X:
            self.turn_label.config(text="Player X's Turn  ✦", fg=C["x"])
        else:
            if self.game_mode.get() == "ai":
                self.turn_label.config(text="🤖  AI is thinking…", fg=C["o"])
            else:
                self.turn_label.config(text="Player O's Turn  ✦", fg=C["o"])

    # ── UTILITIES ───────────────────────────────────────────────────
    @staticmethod
    def _opponent(player: str) -> str:
        return PLAYER_O if player == PLAYER_X else PLAYER_X

    def _add_hover(self, widget, normal: str, hover: str, fg: str):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover,  fg=fg))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal, fg=fg))


# ───────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    TicTacToe()
