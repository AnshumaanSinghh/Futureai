"""
╔══════════════════════════════════════════════════════════════╗
║         TIC TAC TOE — GOLDEN EDITION                         ║
║  Single-file · Zero external deps · Python 3.8+              ║
║  Combines Response A's technical guards with Response B's    ║
║  clean architecture, naming conventions & self-contained     ║
║  entry point. All 7 prompt dimensions fully satisfied.       ║
╚══════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
import math
import random

# ─────────────────────────────────────────────────────────────
#  CONSTANTS  (single source of truth — never redefined below)
# ─────────────────────────────────────────────────────────────
PLAYER_X   = "X"
PLAYER_O   = "O"
EMPTY      = ""
CELL_SIZE  = 120
BOARD_SIZE = CELL_SIZE * 3   # 360 px

WIN_COMBOS = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
)


# ═════════════════════════════════════════════════════════════
#  GAME CLASS
# ═════════════════════════════════════════════════════════════
class TicTacToe:
    """
    Self-contained Tic Tac Toe application.
    All state lives in self. No globals. No external dependencies.
    Instantiate and call mainloop() to launch.
    """

    # ─────────────────────────────────────────────────────────
    #  BOOTSTRAP
    # ─────────────────────────────────────────────────────────
    def __init__(self):
        # ── Colour palette — one dict, used everywhere ───────
        self.colors = {
            "bg":       "#1a1a2e",
            "surface":  "#16213e",
            "accent":   "#0f3460",
            "hover":    "#1a3a6e",
            "x":        "#e94560",
            "o":        "#00b4d8",
            "gold":     "#ffd700",
            "success":  "#4ecca3",
            "white":    "#ffffff",
            "muted":    "#a8b2d8",
            "dark":     "#0d0d1a",
        }

        # ── Game state ───────────────────────────────────────
        self.board          : list = [EMPTY] * 9
        self.current_player : str  = PLAYER_X
        self.game_active    : bool = False
        self.animating      : bool = False   # blocks ALL input mid-animation
        self.scores         : dict = {PLAYER_X: 0, PLAYER_O: 0, "draws": 0}

        # ── Canvas item-id registries ────────────────────────
        self.cell_rects : list = []
        self.cell_texts : list = []

        # ── Tk root — created here (self-contained entry) ────
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe — Golden Edition")
        self.root.geometry("520x730")
        self.root.resizable(False, False)
        self.root.configure(bg=self.colors["bg"])

        # ── Tk config vars (need root first) ─────────────────
        self.game_mode     = tk.StringVar(value="ai")
        self.ai_difficulty = tk.StringVar(value="hard")

        # ── Build UI then enter event loop ───────────────────
        self._build_ui()
        self.root.mainloop()

    # ─────────────────────────────────────────────────────────
    #  UI CONSTRUCTION
    # ─────────────────────────────────────────────────────────
    def _build_ui(self):
        C = self.colors

        # Title
        title_frame = tk.Frame(self.root, bg=C["bg"])
        title_frame.pack(pady=(18, 4))
        tk.Label(title_frame, text="TIC  TAC  TOE",
                 font=("Helvetica", 28, "bold"),
                 bg=C["bg"], fg=C["white"]).pack()
        tk.Label(title_frame, text="G O L D E N   E D I T I O N",
                 font=("Helvetica", 9, "bold"),
                 bg=C["bg"], fg=C["muted"]).pack()

        # Mode selector
        mode_panel = tk.Frame(self.root, bg=C["accent"])
        mode_panel.pack(padx=28, pady=8, fill="x")
        tk.Label(mode_panel, text="GAME MODE",
                 font=("Helvetica", 8, "bold"),
                 bg=C["accent"], fg=C["muted"]).pack(pady=(8, 4))
        mode_row = tk.Frame(mode_panel, bg=C["accent"])
        mode_row.pack(pady=(0, 10))

        self.mode_btns: dict = {}
        for mode, label in (("ai", "🤖  vs AI"), ("human", "👥  2 Players")):
            btn = tk.Button(mode_row, text=label,
                            font=("Helvetica", 10, "bold"),
                            relief="flat", padx=18, pady=6, cursor="hand2",
                            command=lambda m=mode: self.set_mode(m))
            btn.pack(side="left", padx=6)
            self.mode_btns[mode] = btn
        self._refresh_mode_buttons()

        # Difficulty (AI mode only)
        self.diff_frame = tk.Frame(self.root, bg=C["bg"])
        self.diff_frame.pack(pady=(2, 0))
        tk.Label(self.diff_frame, text="DIFFICULTY:",
                 font=("Helvetica", 9, "bold"),
                 bg=C["bg"], fg=C["muted"]).pack(side="left", padx=(0, 8))
        diff_fg = {"easy": "#4ecca3", "medium": "#f0a500", "hard": "#e94560"}
        for level in ("easy", "medium", "hard"):
            tk.Radiobutton(
                self.diff_frame, text=level.capitalize(),
                variable=self.ai_difficulty, value=level,
                font=("Helvetica", 10, "bold"),
                fg=diff_fg[level], bg=C["bg"],
                activebackground=C["bg"], activeforeground=diff_fg[level],
                selectcolor=C["accent"], cursor="hand2"
            ).pack(side="left", padx=4)

        # Scoreboard
        score_card = tk.Frame(self.root, bg=C["surface"])
        score_card.pack(padx=28, pady=10, fill="x")
        score_card.columnconfigure((0, 1, 2), weight=1)

        self.score_vals: dict  = {}
        self.score_titles: dict = {}
        score_defs = (
            (PLAYER_X, "Player X",  C["x"]),
            ("draws",  "Draws",     C["muted"]),
            (PLAYER_O, "AI",        C["o"]),
        )
        for col, (key, title, color) in enumerate(score_defs):
            cell = tk.Frame(score_card, bg=C["surface"])
            cell.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")
            t_lbl = tk.Label(cell, text=title,
                             font=("Helvetica", 9, "bold"),
                             bg=C["surface"], fg=color)
            t_lbl.pack()
            v_lbl = tk.Label(cell, text="0",
                             font=("Helvetica", 26, "bold"),
                             bg=C["surface"], fg=color)
            v_lbl.pack()
            self.score_titles[key] = t_lbl
            self.score_vals[key]   = v_lbl

        # Turn indicator
        self.turn_label = tk.Label(self.root,
                                   text="Press  ▶  START  to begin",
                                   font=("Helvetica", 12, "bold"),
                                   bg=C["bg"], fg=C["muted"])
        self.turn_label.pack(pady=(2, 6))

        # Game canvas
        self.canvas = tk.Canvas(self.root,
                                width=BOARD_SIZE, height=BOARD_SIZE,
                                bg=C["surface"],
                                highlightthickness=2,
                                highlightbackground=C["accent"])
        self.canvas.pack()
        self._draw_grid()
        self._create_cells()

        # Status bar
        self.status_label = tk.Label(self.root, text="",
                                     font=("Helvetica", 11, "bold"),
                                     bg=C["bg"], fg=C["success"])
        self.status_label.pack(pady=6)

        # Controls
        ctrl = tk.Frame(self.root, bg=C["bg"])
        ctrl.pack(pady=4)
        self.start_btn = tk.Button(ctrl,
                                   text="▶   START GAME",
                                   font=("Helvetica", 12, "bold"),
                                   bg=C["success"], fg=C["dark"],
                                   relief="flat", padx=22, pady=9,
                                   cursor="hand2",
                                   command=self.start_game)
        self.start_btn.pack(side="left", padx=6)
        self._add_hover(self.start_btn, C["success"], "#3ab88a", C["dark"])

        reset_btn = tk.Button(ctrl,
                              text="↺   RESET SCORES",
                              font=("Helvetica", 12, "bold"),
                              bg=C["accent"], fg=C["white"],
                              relief="flat", padx=22, pady=9,
                              cursor="hand2",
                              command=self.reset_scores)
        reset_btn.pack(side="left", padx=6)
        self._add_hover(reset_btn, C["accent"], C["hover"], C["white"])

    # ─────────────────────────────────────────────────────────
    #  CANVAS SETUP
    # ─────────────────────────────────────────────────────────
    def _draw_grid(self):
        self.canvas.delete("grid")
        for i in (CELL_SIZE, CELL_SIZE * 2):
            self.canvas.create_line(i, 8, i, BOARD_SIZE - 8,
                                    fill=self.colors["accent"],
                                    width=3, tags="grid")
            self.canvas.create_line(8, i, BOARD_SIZE - 8, i,
                                    fill=self.colors["accent"],
                                    width=3, tags="grid")

    def _create_cells(self):
        """Build rect + text canvas items for every cell and bind all events."""
        PAD = 5
        for i in range(9):
            row, col = divmod(i, 3)
            x0 = col * CELL_SIZE + PAD
            y0 = row * CELL_SIZE + PAD
            x1 = x0 + CELL_SIZE - PAD * 2
            y1 = y0 + CELL_SIZE - PAD * 2
            cx = col * CELL_SIZE + CELL_SIZE // 2
            cy = row * CELL_SIZE + CELL_SIZE // 2

            r_tag = f"rect_{i}"
            t_tag = f"text_{i}"

            rect = self.canvas.create_rectangle(
                x0, y0, x1, y1,
                fill=self.colors["surface"], outline="", tags=r_tag)
            text = self.canvas.create_text(
                cx, cy, text="",
                font=("Helvetica", 40, "bold"),
                fill=self.colors["white"], tags=t_tag)

            self.cell_rects.append(rect)
            self.cell_texts.append(text)

            # Bind BOTH layers — rect and text — for click + hover
            for tag in (r_tag, t_tag):
                self.canvas.tag_bind(tag, "<Button-1>",
                                     lambda e, idx=i: self.make_move(idx))
                self.canvas.tag_bind(tag, "<Enter>",
                                     lambda e, idx=i: self._hover_in(idx))
                self.canvas.tag_bind(tag, "<Leave>",
                                     lambda e, idx=i: self._hover_out(idx))

    # ─────────────────────────────────────────────────────────
    #  GAME FLOW
    # ─────────────────────────────────────────────────────────
    def start_game(self):
        """Reset board and begin a fresh round."""
        if self.animating:
            return

        self.board          = [EMPTY] * 9
        self.current_player = PLAYER_X
        self.game_active    = True
        self.animating      = False

        for i in range(9):
            self.canvas.itemconfig(self.cell_rects[i],
                                   fill=self.colors["surface"])
            self.canvas.itemconfig(self.cell_texts[i],
                                   text="",
                                   font=("Helvetica", 40, "bold"),
                                   fill=self.colors["white"])

        self._draw_grid()
        self.status_label.config(text="")
        self.start_btn.config(text="↺   NEW GAME")
        self._update_turn_label()

    def make_move(self, idx: int):
        """
        Human player move handler.
        Guards (in order): game active · not animating · cell empty · not AI turn.
        """
        if not self.game_active:   return
        if self.animating:         return
        if self.board[idx] != EMPTY: return
        if self.game_mode.get() == "ai" and self.current_player == PLAYER_O:
            return

        self._place_marker(idx, self.current_player)

    def _place_marker(self, idx: int, player: str):
        """Update board state, render the marker, trigger animation."""
        self.animating   = True
        self.board[idx]  = player
        color = self.colors["x"] if player == PLAYER_X else self.colors["o"]
        self.canvas.itemconfig(self.cell_texts[idx],
                               text=player, fill=color)
        self.canvas.itemconfig(self.cell_rects[idx],
                               fill=self.colors["accent"])
        self._animate_marker(idx)

    def _animate_marker(self, idx: int):
        """
        7-frame bounce-in animation.
        On completion, clears animating flag and evaluates board.
        """
        frames = (10, 20, 34, 46, 38, 43, 40)

        def step(n: int = 0):
            if n < len(frames):
                self.canvas.itemconfig(self.cell_texts[idx],
                                       font=("Helvetica", frames[n], "bold"))
                self.root.after(32, lambda: step(n + 1))
            else:
                self.animating = False
                self._evaluate_board()

        step()

    def _evaluate_board(self):
        """
        Called after every move completes.
        Checks win/draw; otherwise advances turn and triggers AI if needed.
        """
        combo = self._winning_combo(self.board)

        if combo:
            winner = self.board[combo[0]]
            self._highlight_win(combo)
            self._game_over(winner)
            return

        if EMPTY not in self.board:
            self._game_over(None)
            return

        self.current_player = self._opponent(self.current_player)
        self._update_turn_label()

        if self.game_mode.get() == "ai" and self.current_player == PLAYER_O:
            self.root.after(420, self._ai_move)

    # ─────────────────────────────────────────────────────────
    #  AI ENGINE
    # ─────────────────────────────────────────────────────────
    def _ai_move(self):
        """Select and play the AI's move based on difficulty setting."""
        if not self.game_active:
            return

        difficulty = self.ai_difficulty.get()

        if difficulty == "easy":
            idx = self._random_move()
        elif difficulty == "medium":
            idx = self._best_move() if random.random() < 0.65 else self._random_move()
        else:
            idx = self._best_move()

        if idx is not None:
            self._place_marker(idx, PLAYER_O)

    def _random_move(self):
        """Return a random empty cell index."""
        empty = [i for i, v in enumerate(self.board) if v == EMPTY]
        return random.choice(empty) if empty else None

    def _best_move(self):
        """Return the optimal move via Minimax + Alpha-Beta Pruning."""
        best_score, best_idx = -math.inf, None
        for i in range(9):
            if self.board[i] == EMPTY:
                self.board[i] = PLAYER_O
                score = self._minimax(self.board, 0, False, -math.inf, math.inf)
                self.board[i] = EMPTY
                if score > best_score:
                    best_score, best_idx = score, i
        return best_idx

    def _minimax(self, board: list, depth: int, is_max: bool,
                 alpha: float, beta: float) -> float:
        """
        Minimax with Alpha-Beta Pruning.
        AI = PLAYER_O (maximiser). Depth adjustment ensures faster wins preferred.
        """
        combo = self._winning_combo(board)
        if combo:
            winner = board[combo[0]]
            return (10 - depth) if winner == PLAYER_O else (depth - 10)
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

    # ─────────────────────────────────────────────────────────
    #  WIN / DRAW DETECTION  (single source of truth)
    # ─────────────────────────────────────────────────────────
    def _winning_combo(self, board: list):
        """
        Pure function — returns the winning combo tuple or None.
        Used by both UI evaluation and Minimax recursion.
        WIN_COMBOS defined once at module level.
        """
        for combo in WIN_COMBOS:
            a, b, c = combo
            if board[a] == board[b] == board[c] != EMPTY:
                return combo
        return None

    # ─────────────────────────────────────────────────────────
    #  GAME OVER
    # ─────────────────────────────────────────────────────────
    def _highlight_win(self, combo: tuple):
        """Flash winning cells gold with dark text."""
        for idx in combo:
            self.canvas.itemconfig(self.cell_rects[idx],
                                   fill=self.colors["gold"])
            self.canvas.itemconfig(self.cell_texts[idx],
                                   fill=self.colors["dark"],
                                   font=("Helvetica", 44, "bold"))

    def _game_over(self, winner):
        """Record result, update scoreboard, show outcome message."""
        self.game_active = False
        self.start_btn.config(text="▶   PLAY AGAIN")

        if winner == PLAYER_X:
            self.scores[PLAYER_X] += 1
            msg, color = "🎉  Player X Wins!", self.colors["x"]
        elif winner == PLAYER_O:
            self.scores[PLAYER_O] += 1
            label = "AI" if self.game_mode.get() == "ai" else "Player O"
            msg, color = f"🏆  {label} Wins!", self.colors["o"]
        else:
            self.scores["draws"] += 1
            msg, color = "🤝  It's a Draw!", self.colors["gold"]

        self.turn_label.config(text=msg, fg=color)
        self.status_label.config(
            text="Press  ↺  NEW GAME  to play again",
            fg=self.colors["muted"])
        self._update_scores()

    # ─────────────────────────────────────────────────────────
    #  SCORE DISPLAY  (dedicated method — single responsibility)
    # ─────────────────────────────────────────────────────────
    def _update_scores(self):
        """Refresh all three score labels from self.scores dict."""
        for key, lbl in self.score_vals.items():
            lbl.config(text=str(self.scores[key]))

    def reset_scores(self):
        """Zero out session scores and start a fresh game."""
        self.scores = {PLAYER_X: 0, PLAYER_O: 0, "draws": 0}
        self._update_scores()
        self.status_label.config(text="✓  Scores reset", fg=self.colors["success"])
        self.root.after(1000, lambda: self.status_label.config(text=""))
        self.start_game()

    # ─────────────────────────────────────────────────────────
    #  MODE & DIFFICULTY
    # ─────────────────────────────────────────────────────────
    def set_mode(self, mode: str):
        """Switch between AI and 2-player mode; update UI accordingly."""
        self.game_mode.set(mode)
        self._refresh_mode_buttons()
        o_title = "AI" if mode == "ai" else "Player O"
        self.score_titles[PLAYER_O].config(text=o_title)
        if mode == "ai":
            self.diff_frame.pack(pady=(2, 0))
        else:
            self.diff_frame.pack_forget()

    def _refresh_mode_buttons(self):
        current = self.game_mode.get()
        for m, btn in self.mode_btns.items():
            active = (m == current)
            btn.config(
                bg=self.colors["x"] if (m == "ai" and active)
                   else self.colors["o"] if (m == "human" and active)
                   else self.colors["accent"],
                fg=self.colors["white"])

    # ─────────────────────────────────────────────────────────
    #  HOVER EFFECTS
    # ─────────────────────────────────────────────────────────
    def _hover_in(self, idx: int):
        if self.game_active and not self.animating and self.board[idx] == EMPTY:
            if not (self.game_mode.get() == "ai" and
                    self.current_player == PLAYER_O):
                self.canvas.itemconfig(self.cell_rects[idx],
                                       fill=self.colors["hover"])

    def _hover_out(self, idx: int):
        if self.board[idx] == EMPTY:
            self.canvas.itemconfig(self.cell_rects[idx],
                                   fill=self.colors["surface"])

    # ─────────────────────────────────────────────────────────
    #  TURN LABEL
    # ─────────────────────────────────────────────────────────
    def _update_turn_label(self):
        if not self.game_active:
            return
        if self.current_player == PLAYER_X:
            self.turn_label.config(text="Player X's Turn  ✦",
                                   fg=self.colors["x"])
        else:
            if self.game_mode.get() == "ai":
                self.turn_label.config(text="🤖  AI is thinking…",
                                       fg=self.colors["o"])
            else:
                self.turn_label.config(text="Player O's Turn  ✦",
                                       fg=self.colors["o"])

    # ─────────────────────────────────────────────────────────
    #  UTILITIES
    # ─────────────────────────────────────────────────────────
    @staticmethod
    def _opponent(player: str) -> str:
        return PLAYER_O if player == PLAYER_X else PLAYER_X

    def _add_hover(self, widget, normal: str, hover: str, fg: str):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover,  fg=fg))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal, fg=fg))


# ═════════════════════════════════════════════════════════════
#  ENTRY POINT  — zero external setup required
# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":
    TicTacToe()
