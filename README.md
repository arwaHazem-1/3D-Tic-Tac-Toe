# Cubic: 4x4x4 3D Tic-Tac-Toe with AI

An intelligent player for the Cubic game, a variant of Tic-Tac-Toe played on a 4x4x4 three-dimensional grid. This project implements an AI player using the Minimax algorithm, Alpha-Beta Pruning, and heuristic functions to make strategic moves.

## 🎮 Game Description

Cubic is an engaging board game that introduces an additional layer of complexity compared to traditional Tic-Tac-Toe. Played on a 4x4x4 grid (64 positions), each player takes turns placing their markers (X or O) in an attempt to create a line of four in any direction within the three dimensions. The challenge lies in the spatial nature of the game, requiring players to think strategically in three dimensions to secure a winning position.

**Winning Condition:** A player wins by placing four markers in a row along any of the 76 possible winning lines:
- Lines parallel to X, Y, or Z axes (48 lines)
- Diagonals in XY, XZ, and YZ planes (24 lines)
- Space diagonals through the cube (4 lines)

## ✨ Features

### 1. Minimax Algorithm Implementation
- Full implementation of the Minimax algorithm tailored for the Cubic game
- Traverses the three-dimensional game space efficiently
- Evaluates possible moves and selects optimal moves that maximize winning chances
- Configurable search depth for balancing performance and intelligence

### 2. Alpha-Beta Pruning Integration
- Integrated Alpha-Beta Pruning alongside Minimax for enhanced computational efficiency
- Eliminates unnecessary evaluations in the game tree
- Significantly reduces computation time while maintaining optimal decision-making
- Reduces nodes explored by up to 90% in many positions

### 3. Heuristic Functions Design
- **Simple Heuristic:** Counts open lines for each player
- **Advanced Heuristic:** Pattern-based evaluation with:
  - Threat detection (3 in a row with 1 empty = immediate win threat)
  - Two-in-a-row pattern recognition
  - Center control bonus (strategic position evaluation)
  - Opponent threat blocking (defensive play)
- Provides quick assessment of board states without full game tree search

### 4. User Interface Development
- Modern, user-friendly GUI built with Tkinter
- Clear visualization of the 4x4x4 board (4 layers displayed in 2x2 grid)
- **Clear AI Decision Display:**
  - Shows AI's chosen position (Layer, Row, Column)
  - Displays evaluation score
  - Shows nodes explored (demonstrating Minimax + Alpha-Beta)
  - Displays computation time
  - Indicates algorithm and heuristic used
- Turn indicators and game status
- Move counter
- Winning line highlighting (positions highlighted in green)
- New game functionality

### 5. Optimization
- **Transposition Table:** Caches evaluated positions to avoid redundant calculations
- **Alpha-Beta Pruning:** Reduces search space dramatically
- **Efficient Board Representation:** 3D coordinates converted to flat indices for fast access
- **Threading:** AI moves computed in background thread to keep UI responsive
- Configurable search depth for performance tuning

## 📋 Requirements

- Python 3.7 or higher
- Tkinter (usually included with Python)

## 🚀 Installation

1. Clone or download this repository
2. Ensure Python 3.7+ is installed
3. No additional packages required (uses only standard library)

## 🎯 Usage

### Running the Game

```bash
python main.py
```

### How to Play

1. **Start the Game:** Run `main.py` to launch the GUI
2. **Make Your Move:** Click on any empty cell in the 4x4x4 grid
   - The board is displayed as 4 layers (Layer 0, 1, 2, 3)
   - Each layer is a 4x4 grid
3. **AI Response:** After your move, the AI will automatically calculate and make its move
4. **View AI Analysis:** The right panel shows:
   - AI's chosen position
   - Evaluation score
   - Nodes explored (demonstrating Minimax search)
   - Computation time
5. **Win Condition:** First player to get 4 in a row (in any direction) wins
6. **New Game:** Click "New Game" button to restart

### Game Controls

- **Click on empty cells** to place your marker (X)
- **New Game button** to restart
- **AI moves automatically** after your move

## 🏗️ Project Structure

```
3D-Tic-Tac-Toe/
│
├── main.py                 # Entry point - launches the GUI
│
└── cubic/                  # Main package
    ├── __init__.py         # Package initialization
    ├── board.py            # Board representation (4x4x4 grid)
    ├── rules.py            # Game rules and win detection (76 winning lines)
    ├── players.py          # Player classes (Human, AI, Random)
    ├── minimax.py          # Minimax algorithm with Alpha-Beta Pruning
    ├── heuristics.py       # Heuristic evaluation functions
    └── gui.py              # User interface (Tkinter)
```

## 🔧 Technical Details

### Minimax Algorithm
- **Location:** `cubic/minimax.py`
- **Search Depth:** Configurable (default: 3-4 for responsiveness)
- **Algorithm:** Minimax with Alpha-Beta Pruning
- **Optimization:** Transposition table for position caching

### Alpha-Beta Pruning
- **Implementation:** Integrated in `_minimax()` method
- **Efficiency:** Reduces nodes explored by eliminating branches that cannot affect the final decision
- **Beta Cutoff:** For maximizing player (lines 197-199)
- **Alpha Cutoff:** For minimizing player (lines 228-230)

### Heuristic Functions
- **Location:** `cubic/heuristics.py`
- **Types:**
  - `simple`: Counts open lines
  - `advanced`: Pattern-based with threat detection and center control
- **Usage:** Evaluates non-terminal board states quickly

### Board Representation
- **Structure:** 64-element flat array (4×4×4 = 64)
- **Indexing:** 3D coordinates (layer, row, col) converted to flat indices
- **Conversion:** `_to_flat_index()` and `_to_coordinates()` methods

## 📊 Performance

- **Search Depth:** 3-4 levels (configurable)
- **Typical Response Time:** 2-5 seconds per AI move
- **Nodes Explored:** Varies (typically 1,000-50,000 with Alpha-Beta pruning)
- **Without Pruning:** Would explore millions of nodes

## 🎓 Algorithm Explanation

### Minimax Algorithm
The Minimax algorithm is a decision-making algorithm used in game theory. It assumes both players play optimally:
- **Maximizing Player:** Tries to maximize their score
- **Minimizing Player:** Tries to minimize the opponent's score
- The algorithm explores all possible moves to a certain depth and chooses the move with the best outcome

### Alpha-Beta Pruning
Alpha-Beta Pruning is an optimization technique for Minimax:
- **Alpha (α):** Best value the maximizing player can guarantee
- **Beta (β):** Best value the minimizing player can guarantee
- **Pruning:** If α ≥ β, we can stop exploring that branch (it won't affect the final decision)

### Heuristic Evaluation
Since exploring all moves to the end is computationally expensive, heuristic functions provide quick estimates:
- Evaluates board patterns (threats, two-in-a-row, center control)
- Returns a score indicating how favorable the position is
- Higher score = better position for the maximizing player

## 🐛 Troubleshooting

**Issue:** GUI doesn't open
- **Solution:** Ensure Python 3.7+ is installed and Tkinter is available

**Issue:** AI takes too long to move
- **Solution:** Reduce search depth in `cubic/gui.py` line 36 (change `depth=3` to `depth=2`)

**Issue:** Import errors
- **Solution:** Ensure you're running from the project root directory

## 📝 License

This project is provided as-is for educational purposes.

## 👤 Author

Your Name

## 🙏 Acknowledgments

- Minimax algorithm and Alpha-Beta Pruning concepts from game theory
- Tkinter for GUI framework
- 4x4x4 Cubic game rules and winning line calculations

---

**Enjoy playing Cubic against an intelligent AI opponent!** 🎮🤖

