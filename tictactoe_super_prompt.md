# 🎯 SUPER PROMPT: Ultimate Tic Tac Toe Python Game

---

## DIMENSION 1 — CONTEXT AND ROLE

You are a **Senior Python Game Developer and UI/UX Engineer** with deep expertise in building production-quality desktop applications using Python's `tkinter` GUI framework. You specialize in crafting immersive, visually stunning game experiences that feel modern and polished — not like typical academic exercises. Your work bridges the gap between clean software architecture and delightful user experience.

You are tasked with designing and implementing a **complete, single-file Python Tic Tac Toe game** that meets production-level standards in code quality, visual design, user interaction, and intelligent gameplay. The game must feel like a premium desktop application — not a beginner's project.

The final deliverable must be a **single `.py` file** that can be run directly with no external dependencies beyond Python's standard library. It must be portable, self-contained, and immediately playable by any user with Python 3.8+ installed.

---

## DIMENSION 2 — OBJECTIVE

Develop a complete, full-featured Tic Tac Toe desktop game that achieves all of the following goals simultaneously:

1. **Implements a beautiful, modern dark-themed GUI** using `tkinter` with `Canvas`-based rendering, custom colors, hover effects, and smooth visual feedback.
2. **Supports two game modes**: Player vs. AI and Player vs. Player (2 humans on the same machine).
3. **Includes an unbeatable AI opponent** built using the **Minimax algorithm with Alpha-Beta Pruning**, with selectable difficulty levels (Easy, Medium, Hard).
4. **Tracks scores persistently** across rounds within the session, displaying live score updates with animated feedback.
5. **Provides animated move placement**, cell highlighting on win, turn indicators, and status messages throughout gameplay.
6. **Implements robust game state management** with clean separation between UI rendering, game logic, and AI computation.
7. **Delivers graceful error handling** for edge cases: clicking occupied cells, interacting during AI thinking time, restarting mid-game, and resetting scores.

The game should feel complete, satisfying, and replayable. Every interaction — from hovering over a cell to a winning animation — should feel intentional and polished.

---

## DIMENSION 3 — UI AND VISUAL DESIGN REQUIREMENTS

### Color System and Theme
The game must implement a **professional dark color palette** with carefully chosen accent colors:
- **Background**: Deep navy (`#1a1a2e`) — the primary canvas background
- **Card/Panel surface**: Slightly lighter navy (`#16213e`) — for framed sections
- **Accent/Interactive**: Rich indigo blue (`#0f3460`) — for borders, hover states, cell fills
- **Player X color**: Vibrant coral red (`#e94560`) — consistently used for all X markers and labels
- **Player O / AI color**: Electric cyan (`#00b4d8`) — consistently used for O markers and labels
- **Win highlight**: Gold (`#ffd700`) — used on winning cells to draw attention
- **Success / Active**: Teal green (`#4ecca3`) — for start buttons and positive confirmations
- **Primary text**: Pure white (`#ffffff`)
- **Secondary text**: Muted lavender (`#a8b2d8`) — for labels and less critical information

All colors must be applied **consistently** throughout every UI component.

### Animation Requirements
Implement the following animation behaviors:
- **Marker placement animation**: When X or O is placed, animate the font size from small → large → slightly smaller → settled (a "pop-in" bounce effect using `root.after()` scheduling, no external libraries).
- **Hover effects**: When a user hovers over an empty cell, the background transitions to the accent color. On leave, it reverts.
- **Win highlight animation**: The three winning cells must switch to gold background instantly upon game end, with text inverting to dark for contrast.
- **AI thinking delay**: A deliberate 400ms delay before the AI places its marker (using `root.after`), during which the turn label reads "AI is thinking..." — giving the illusion of thought.
- **Score increment feedback**: Score labels must visually update immediately after each round ends.

### Layout Structure
The window must be fixed at **520×720 pixels** and include these stacked sections top to bottom:

1. **Title Bar** — "TIC TAC TOE" in large bold font, with subtitle "ULTIMATE EDITION" in small spaced caps
2. **Mode Selector Panel** — Toggle buttons for "vs AI" and "2 Players" with active state highlighted
3. **Difficulty Selector** — Radio buttons for Easy / Medium / Hard (visible only in AI mode)
4. **Scoreboard** — Three columns: Player X score | Draws | Player O / AI score, each color-coded
5. **Turn Indicator Label** — Dynamic label showing whose turn it is, color-coded to the player
6. **Game Board Canvas** — 360×360 pixel canvas with a 3×3 grid rendered via lines and Canvas items
7. **Status Label** — Shows contextual messages: "Game in progress", "Player X Wins!", "It's a Draw!"
8. **Control Buttons** — "START GAME" / "PLAY AGAIN" and "RESET SCORES" buttons

---

## DIMENSION 4 — GAME BOARD AND INTERACTION REQUIREMENTS

### Board Rendering
The game board must be rendered entirely on a **`tk.Canvas` widget** — not using `tk.Button` grid layout. This gives full control over:
- Custom cell hover states via canvas rectangle fills
- Text items for markers with animated font resizing
- Win highlight overlays via rectangle color changes
- Clean line-based grid separators

Each cell must be both a rectangle item and a text item, both bound to the same click handler via `canvas.tag_bind()`.

### Cell Interaction Rules
- Clicking an occupied cell must be silently ignored (no error, no feedback)
- Clicking any cell during AI's turn must be silently ignored
- Clicking any cell when no game is active (before START) must be silently ignored
- All three cases handled via a single guard at the top of the move handler

### Player Move Flow
```
User clicks cell → Guard checks (active? empty? human turn?) → place_marker() →
animate_marker() → check_winner() → if no winner: switch player → update_turn_label() →
if AI mode and AI's turn: root.after(400, ai_move)
```

### AI Move Flow
```
ai_move() called after 400ms → select move based on difficulty →
place_marker() → animate_marker() → check_winner() → if no winner: switch to Player X → update_turn_label()
```

---

## DIMENSION 5 — AI ENGINE REQUIREMENTS

### Architecture
The AI system must implement three difficulty tiers using a shared codebase:

**Easy Mode**: The AI selects a completely random empty cell. No strategy. Beatable by any player.

**Medium Mode**: The AI uses a probabilistic blend — 60% of the time it plays the optimal Minimax move, 40% of the time it picks randomly. This creates a challenging but imperfect opponent.

**Hard Mode**: The AI runs **full Minimax with Alpha-Beta Pruning**, making it mathematically unbeatable. The best a human can achieve is a draw with perfect play.

### Minimax Algorithm Specification
```
minimax(board, depth, is_maximizing, alpha, beta):
    check terminal state → return score (10-depth for AI win, depth-10 for player win, 0 for draw)
    if maximizing (AI):
        iterate empty cells, recurse as minimizing, track max score
        apply alpha pruning
    if minimizing (Player):
        iterate empty cells, recurse as maximizing, track min score
        apply beta pruning
    return best score
```

The depth adjustment (`10 - depth` and `depth - 10`) ensures the AI prefers **faster wins** and **slower losses**, producing more natural-feeling gameplay even in Hard mode.

The AI always plays as `PLAYER_O`. The scoring convention:
- AI wins: positive score (higher = faster win preferred)
- Player wins: negative score (lower = faster loss avoided)
- Draw: 0

### get_best_move() Logic
Iterate all 9 cells. For each empty cell: temporarily place the AI marker, run minimax, undo the move, track the highest-scoring move. Return the index of the best move.

---

## DIMENSION 6 — GAME STATE AND DATA MANAGEMENT REQUIREMENTS

### State Variables
Maintain the following state within the main game class:
| Variable | Type | Purpose |
|---|---|---|
| `board` | `list[str]` (len 9) | Current board state, each cell is `""`, `"X"`, or `"O"` |
| `current_player` | `str` | `"X"` or `"O"` — whose turn it is |
| `game_mode` | `tk.StringVar` | `"ai"` or `"human"` |
| `ai_difficulty` | `tk.StringVar` | `"easy"`, `"medium"`, or `"hard"` |
| `game_active` | `bool` | Whether the game is currently in play |
| `scores` | `dict` | `{X: int, O: int, draws: int}` persisted across rounds |
| `buttons` | `list` | Canvas rectangle item IDs for each cell |
| `cell_texts` | `list` | Canvas text item IDs for each cell |

### Win Detection
Check all 8 winning combinations after every move:
- 3 rows: `[0,1,2], [3,4,5], [6,7,8]`
- 3 columns: `[0,3,6], [1,4,7], [2,5,8]`
- 2 diagonals: `[0,4,8], [2,4,6]`

If a winner is found: call `highlight_win(combo, winner)` → `game_over(winner)`.  
If no empty cells remain and no winner: `game_over(None)` (draw).

### Game Reset Behavior
`start_game()` must:
- Reset `board` to 9 empty strings
- Set `current_player` to `PLAYER_X`
- Set `game_active = True`
- Clear all canvas text items and cell background colors
- Redraw the grid lines
- Update turn label
- Update start button text to "PLAY AGAIN"

`reset_scores()` must reset the `scores` dict, update all score labels, and optionally auto-start a new game.

---

## DIMENSION 7 — ARCHITECTURE, CODE QUALITY, AND DELIVERABLE REQUIREMENTS

### Architecture Pattern
Implement the entire game as a **single class `TicTacToe`** with clear method responsibility separation:

```
TicTacToe
├── __init__()              → Initialize state and launch UI
├── setup_ui()              → Build all widgets and layout
├── draw_board_lines()      → Canvas grid rendering
├── create_cell_buttons()   → Canvas cell items + event bindings
├── set_mode(mode)          → Toggle game mode, update UI
├── start_game()            → Reset and begin a new round
├── make_move(idx)          → Handle human player clicks
├── place_marker(idx, p)    → Update board + canvas
├── animate_marker(idx)     → Bounce-in font animation
├── hover_enter/leave(idx)  → Cell hover effects
├── ai_move()               → Trigger AI decision
├── get_random_move()       → Easy AI
├── get_best_move()         → Hard AI (calls minimax)
├── minimax(...)            → Alpha-beta pruning engine
├── check_winner()          → Game state evaluation (modifies UI)
├── check_winner_board(b)   → Pure function used by minimax
├── highlight_win(combo, w) → Gold cell highlight on win
├── game_over(winner)       → End state: scores, labels
├── update_turn_label()     → Dynamic turn/thinking indicator
└── reset_scores()          → Session score reset
```

### Code Quality Standards
- All methods must have single, clearly defined responsibilities
- No global variables — all state lives in `self`
- Canvas tag naming convention: `f"cell{i}"` and `f"text{i}"` for all 9 cells
- Colors defined once in a `self.colors` dictionary — never hardcoded inline
- Event bindings via `canvas.tag_bind()` using lambda with default argument capture (`idx=i`)
- AI computation must use the pure-function `check_winner_board(board)` — never the UI-coupled `check_winner()`

### Single-File Deliverable Requirements
The final output must be:
- **One `.py` file** — zero external dependencies, zero pip installs required
- Runnable via: `python tictactoe.py`
- Compatible with Python 3.8+
- Works on Windows, macOS, and Linux (tkinter is included in standard Python distributions)
- No imports beyond: `tkinter`, `math`, `random` (all standard library)

### Error Handling and Edge Cases
Handle all of the following gracefully (silent guard, no crash, no error dialog):
- Click on occupied cell during active game
- Click during AI's turn (400ms delay window)
- Click when game has not been started
- Mode/difficulty change while a game is in progress (apply on next game start)
- Rapid repeated clicks on the Start button

---

## SUMMARY CHECKLIST

Before finalizing, verify every item:

- [ ] Single `.py` file, no external dependencies
- [ ] Dark theme with full color system from `self.colors` dict
- [ ] Canvas-based board (not button grid)
- [ ] Hover effects on empty cells
- [ ] Bounce-in animation on marker placement
- [ ] Gold win highlight on 3 winning cells
- [ ] AI mode with Easy / Medium / Hard difficulty
- [ ] Unbeatable Minimax + Alpha-Beta Pruning on Hard
- [ ] 400ms AI thinking delay with "AI is thinking..." label
- [ ] 2-Player (human vs human) mode toggle
- [ ] Live scoreboard persisting across rounds
- [ ] Score reset button
- [ ] Clean class architecture with single-responsibility methods
- [ ] All edge cases silently handled (no crashes)
- [ ] Works on Python 3.8+ on Windows / macOS / Linux

---

*Generate the complete, runnable Python file now. Include every feature listed above. Do not truncate, summarize, or omit any section. The output must be fully functional when saved as a `.py` file and executed.*
