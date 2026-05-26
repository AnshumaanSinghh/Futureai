# Tic Tac Toe — Golden Edition

> A production-quality, single-file Python desktop game built with `tkinter`.  
> Implements Minimax + Alpha-Beta Pruning AI, scroll-animated UI, full dark theme, and session scoreboard — zero external dependencies.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [Running the Code](#running-the-code)
4. [Testing the Code](#testing-the-code)
5. [Evaluation Methodology](#evaluation-methodology)
6. [Response Comparison Summary](#response-comparison-summary)
7. [Technology Stack](#technology-stack)

---

## Project Overview

This project delivers a complete Tic Tac Toe game as a **single Python file** requiring no pip installs, no virtual environments, and no configuration. It was developed against a structured 7-dimension prompt specification and evaluated across three generated responses — Response A, Response B, and the final **Golden Response** — with the golden implementation satisfying all 7 dimensions at a perfect score.

### Key Features

- **Dark theme UI** — full colour palette defined in one `self.colors` dict; no hardcoded hex values inline
- **Canvas-based game board** — rendered via `tk.Canvas` for full control over hover states, animations, and win highlights
- **7-frame bounce animation** — marker placement uses a recursive `root.after()` chain for a smooth elastic pop-in effect
- **Unbeatable AI** — Hard mode uses Minimax with Alpha-Beta Pruning; Medium blends optimal and random; Easy is fully random
- **Race condition guard** — `animating` boolean blocks all input during animation frames, preventing double-move bugs
- **Session scoreboard** — Player X, Player O / AI, and Draws tracked across rounds without resetting between games
- **2-Player mode** — toggle between vs AI and local 2-player; scoreboard label updates dynamically
- **Self-contained entry point** — `TicTacToe()` creates its own `tk.Tk()` root internally; run with one command

---

## Repository Structure

```
tictactoe-golden/
│
├── tictactoe_golden.py          # ← Main game file (the golden response)
│
├── tictactoe_response_a.py      # Response A — technically strong, architecture issues
├── tictactoe_response_b.py      # Response B — clean architecture, technical gaps
│
├── tictactoe_super_prompt.md    # The 7-dimension super prompt used to generate all responses
├── golden_justification.md      # Dimension-by-dimension justification of the golden response
│
└── README.md                    # This file
```

### File Roles

| File | Purpose |
|---|---|
| `tictactoe_golden.py` | The final deliverable — all 7 dimensions satisfied |
| `tictactoe_response_a.py` | Comparative baseline — strong guards, weak naming and portability |
| `tictactoe_response_b.py` | Comparative baseline — clean naming, weak guards and DRY violations |
| `tictactoe_super_prompt.md` | The structured prompt covering Context, Objective, UI, Board, AI, State, and Architecture |
| `golden_justification.md` | Written justification explaining every specific improvement over A and B |
| `README.md` | Project overview, setup, and evaluation methodology |

---

## Running the Code

### Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.8 or higher |
| tkinter | Included in standard Python distributions |
| External packages | **None** |

> **Note:** `tkinter` ships with Python on Windows and macOS by default.  
> On Linux (Debian/Ubuntu), install it if missing:  
> ```bash
> sudo apt-get install python3-tk
> ```

### Run the Golden Response

```bash
python tictactoe_golden.py
```

### Run Response A (for comparison)

```bash
python tictactoe_response_a.py
```

### Run Response B (for comparison)

```bash
python tictactoe_response_b.py
```

### Verify Python and tkinter availability

```bash
python --version
python -c "import tkinter; print('tkinter OK')"
```

---

## Testing the Code

There is no external test framework dependency. All validation is done through **syntax checks** and **manual gameplay testing** using the scenarios below.

### Syntax Verification

Run this for any file to confirm it is syntactically valid before launching the GUI:

```bash
python -c "import ast; ast.parse(open('tictactoe_golden.py').read()); print('Syntax OK')"
```

### Manual Test Scenarios

Work through these scenarios after launching the game to verify all features:

#### Core Gameplay
| Scenario | Expected Result |
|---|---|
| Launch the file | Window opens at 520×730px with dark theme, no errors |
| Click START GAME | Board clears, Player X's Turn label appears in red |
| Click an empty cell | X marker appears with bounce animation |
| Click the same cell again | Nothing happens (silent guard) |
| Click rapidly during animation | Only the first click registers |
| Fill three in a row | Winning cells highlight gold, score increments |
| Fill all 9 cells with no winner | "It's a Draw!" message, draws score increments |

#### AI Mode
| Scenario | Expected Result |
|---|---|
| Set difficulty to Hard, play optimally | Best result is a draw — AI never loses |
| Set difficulty to Easy | AI plays randomly, beatable easily |
| Set difficulty to Medium | AI plays well but makes occasional mistakes |
| Click a cell during AI's 420ms delay | Click is blocked — `animating` guard active |
| Observe turn label during AI delay | Shows "🤖 AI is thinking…" in cyan |

#### Mode Switching
| Scenario | Expected Result |
|---|---|
| Switch to 2 Players | Difficulty selector hides, O score label reads "Player O" |
| Switch back to vs AI | Difficulty selector reappears, O score label reads "AI" |
| Switch mode mid-game | Takes effect on next game start |

#### Scoreboard & Reset
| Scenario | Expected Result |
|---|---|
| Win 3 games as X | X score shows 3 |
| Click RESET SCORES | All scores return to 0, new game starts |
| Draws accumulate correctly | Draw counter increments only on full-board no-winner |

#### Hover Effects
| Scenario | Expected Result |
|---|---|
| Hover over empty cell | Cell background changes to `#1a3a6e` |
| Move mouse away | Cell returns to surface colour |
| Hover over occupied cell | No colour change |
| Hover during AI turn | No colour change (hover guard active) |
| Hover over marker text directly | Hover still triggers (both layers bound) |

---

## Evaluation Methodology

All three responses were evaluated against the same **7-dimension prompt specification**. Each dimension was scored as **Pass**, **Partial**, or **Fail** based on whether the implementation fully, partially, or did not satisfy the stated requirement.

### The 7 Dimensions

| # | Dimension | What was evaluated |
|---|---|---|
| 1 | **Context & Role** | Single-file portability, self-contained entry point, no external deps |
| 2 | **Objective** | All 7 stated goals present: AI, 2P mode, animations, scoreboard, guards, theme, architecture |
| 3 | **UI & Visual Design** | Full colour dict, canvas-based board, animation frames, hover on both layers, gold win highlight |
| 4 | **Board & Interaction** | All click guards in correct order, hover blocking during AI/animation turns |
| 5 | **AI Engine** | Easy/Medium/Hard tiers, correct Minimax + Alpha-Beta, depth-adjusted scoring, 420ms delay |
| 6 | **State & Data Management** | Single WIN_COMBOS source, dedicated score updater, pure win-detection function, no DRY violations |
| 7 | **Architecture & Code Quality** | Private method convention, `@staticmethod` for pure utilities, single-responsibility methods, clean naming |

### Scoring Rubric

Each dimension was awarded a score between 0 and 1:

- **1.0 — Pass:** Requirement fully met with no gaps or workarounds
- **0.5 — Partial:** Core requirement met but with a specific identifiable flaw
- **0.0 — Fail:** Requirement missing or broken

### Scores

| Response | D1 | D2 | D3 | D4 | D5 | D6 | D7 | **Total** |
|---|---|---|---|---|---|---|---|---|
| Response A | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.5 | **5.4 / 7** |
| Response B | 1.0 | 1.0 | 0.5 | 0.5 | 1.0 | 0.5 | 0.5 | **5.0 / 7** |
| Golden Response | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | **7.0 / 7** |

### Key Discriminating Criteria

The three criteria that most clearly separated the responses were:

**1. Self-contained entry point (D1)**  
Response A failed here by requiring `TicTacToe(app_root)` — an externally created root object. This breaks the single-file contract. The golden response and Response B both create `tk.Tk()` internally.

**2. Animation race condition guard (D4)**  
Response B only guarded on `ai_thinking`, leaving a small window where rapid clicks during animation frames could register double moves. Response A and the golden response use an `animating` boolean that is set at the start of `_place_marker()` and only cleared at the final animation frame — making double-moves physically impossible.

**3. WIN_COMBOS single source of truth (D6)**  
Response B defined the win combinations list twice in two separate methods — a DRY violation. Response A improved this by delegating from `check_winner` to `check_winner_board`, but still defined the list at the method level on every call. The golden response defines `WIN_COMBOS` once as a module-level immutable constant, shared by both UI evaluation and every recursive minimax call.

---

## Technology Stack

| Layer | Technology | Reason |
|---|---|---|
| Language | Python 3.8+ | Wide compatibility, standard library sufficient |
| GUI Framework | `tkinter` (stdlib) | Zero install, cross-platform, Canvas API for custom rendering |
| AI Algorithm | Minimax + Alpha-Beta Pruning | Mathematically optimal for a 9-cell game tree |
| Randomisation | `random` (stdlib) | Easy and Medium difficulty blending |
| Math utilities | `math` (stdlib) | `math.inf` for Minimax score initialisation |
| External packages | **None** | Fully self-contained, no pip required |

---

## Authors & Credits

- **Prompt Design:** 7-dimension structured specification covering UI, AI, architecture, and interaction requirements
- **Evaluation:** Comparative analysis of Response A vs Response B against all 7 dimensions
- **Golden Implementation:** Synthesised from the strongest elements of both responses with additional improvements

---

*Run `python tictactoe_golden.py` to launch. No setup required.*
