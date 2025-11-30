"""
Basic GUI for Cubic: 4x4x4 3D Tic-Tac-Toe using tkinter.

Core Requirements Only:
1. Minimax Algorithm Implementation
2. Alpha-Beta Pruning Integration
3. Heuristic Functions Design
4. User Interface Development

No Advanced Features - Just the Requirements.
"""

import tkinter as tk
from tkinter import messagebox
import threading
from typing import List, Tuple
from cubic.board import Board
from cubic.rules import GameRules
from cubic.players import HumanPlayer, AIPlayer
from cubic.minimax import Minimax


class CubicGUI:
    """Basic GUI for Cubic - Requirements Only."""

    def __init__(self, root: tk.Tk):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Cubic: 4x4x4 3D Tic-Tac-Toe")
        self.root.geometry("900x750")

        # Game state
        self.board = Board()
        self.rules = GameRules(self.board)
        self.player_x = HumanPlayer(Board.PLAYER_X)  # Human plays X
        self.player_o = AIPlayer(Board.PLAYER_O, depth=3)  # AI plays O (reduced to 3 for speed)
        self.current_player = Board.PLAYER_X
        self.game_over = False
        self.winning_line = None

        # AI state
        self.ai_thinking = False
        self.ai_thread = None

        # GUI elements
        self.canvas_buttons: List[Tuple[int, tk.Button]] = []

        self.setup_ui()
        self.update_display()

    def setup_ui(self):
        """Set up the user interface."""
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        title_frame.pack(fill=tk.X)
        tk.Label(
            title_frame,
            text="4x4x4 Cubic - Human vs AI",
            font=("Arial", 18, "bold"),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=10)

        # Main content
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left: 4x4x4 Board (4 layers in 2x2 grid)
        board_frame = tk.Frame(content_frame)
        board_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            board_frame,
            text="Game Board (4 Layers)",
            font=("Arial", 14, "bold")
        ).pack(pady=5)

        # Create 4 layers in 2x2 arrangement
        for layer in range(4):
            if layer % 2 == 0:
                row_frame = tk.Frame(board_frame)
                row_frame.pack()

            layer_frame = tk.LabelFrame(
                row_frame,
                text=f"Layer {layer}",
                font=("Arial", 10, "bold"),
                padx=5,
                pady=5
            )
            layer_frame.pack(side=tk.LEFT, padx=8, pady=8)

            # Create 4x4 grid for each layer
            for row in range(4):
                for col in range(4):
                    flat_index = Board._to_flat_index(layer, row, col)
                    btn = tk.Button(
                        layer_frame,
                        text="",
                        font=("Arial", 16, "bold"),
                        width=3,
                        height=1,
                        command=lambda idx=flat_index: self.make_human_move(idx)
                    )
                    btn.grid(row=row, column=col, padx=1, pady=1)
                    self.canvas_buttons.append((flat_index, btn))

        # Right: Info Panel
        info_frame = tk.Frame(content_frame, bg='#ecf0f1', width=240)
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        info_frame.pack_propagate(False)

        # Current Turn
        tk.Label(
            info_frame,
            text="Current Turn",
            font=("Arial", 12, "bold"),
            bg='#ecf0f1'
        ).pack(pady=10)

        self.turn_label = tk.Label(
            info_frame,
            text="Your Turn (X)",
            font=("Arial", 14, "bold"),
            bg='#3498db',
            fg='white',
            width=18,
            height=2
        )
        self.turn_label.pack(pady=5)

        # Separator
        tk.Frame(info_frame, bg='#bdc3c7', height=2).pack(fill=tk.X, pady=10)

        # AI Information
        tk.Label(
            info_frame,
            text="AI Analysis",
            font=("Arial", 12, "bold"),
            bg='#ecf0f1'
        ).pack(pady=5)

        self.ai_info_label = tk.Label(
            info_frame,
            text="Waiting for your move...",
            font=("Arial", 9),
            bg='white',
            fg='#2c3e50',
            wraplength=210,
            justify=tk.LEFT,
            relief=tk.SUNKEN,
            padx=8,
            pady=8,
            height=12
        )
        self.ai_info_label.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        # Move Counter
        self.move_label = tk.Label(
            info_frame,
            text="Moves: 0",
            font=("Arial", 10),
            bg='#ecf0f1'
        )
        self.move_label.pack(pady=10)

        # New Game Button
        tk.Button(
            info_frame,
            text="New Game",
            command=self.new_game,
            font=("Arial", 11, "bold"),
            bg='#27ae60',
            fg='white',
            width=15,
            height=2
        ).pack(pady=10)

    def update_display(self):
        """Update the board and status display."""
        # Update board buttons
        for flat_index, btn in self.canvas_buttons:
            value = self.board.get_position(flat_index)
            is_winning = self.winning_line and flat_index in self.winning_line

            if value == Board.PLAYER_X:
                btn.config(
                    text="X",
                    fg='white',
                    bg='#27ae60' if is_winning else '#3498db',  # Green for winning X
                    disabledforeground='white',
                    relief=tk.RAISED if is_winning else tk.FLAT,
                    bd=3 if is_winning else 1
                )
            elif value == Board.PLAYER_O:
                btn.config(
                    text="O",
                    fg='white',
                    bg='#27ae60' if is_winning else '#e74c3c',  # Green for winning O
                    disabledforeground='white',
                    relief=tk.RAISED if is_winning else tk.FLAT,
                    bd=3 if is_winning else 1
                )
            else:
                btn.config(
                    text="",
                    bg='#f39c12' if is_winning else 'white',  # Orange highlight for winning empty spots
                    state=tk.NORMAL if not self.game_over and not self.ai_thinking else tk.DISABLED,
                    relief=tk.FLAT,
                    bd=1
                )

        # Update move counter
        moves = self.board.count_moves()
        self.move_label.config(text=f"Moves: {moves}")

        # Update turn indicator
        if self.game_over:
            state = self.rules.get_game_state()
            if state == "x_wins":
                self.turn_label.config(text="You Win!", bg='#27ae60')
            elif state == "o_wins":
                self.turn_label.config(text="AI Wins!", bg='#c0392b')
            else:
                self.turn_label.config(text="Draw!", bg='#f39c12')
        elif self.ai_thinking:
            self.turn_label.config(text="AI Thinking...", bg='#95a5a6')
        elif self.current_player == Board.PLAYER_X:
            self.turn_label.config(text="Your Turn (X)", bg='#3498db')
        else:
            self.turn_label.config(text="AI's Turn (O)", bg='#e74c3c')

    def make_human_move(self, flat_index: int):
        """Handle human player move."""
        # Validation
        if self.game_over:
            messagebox.showinfo("Game Over", "Game has ended. Start a new game.")
            return

        if self.ai_thinking:
            messagebox.showinfo("Please Wait", "AI is thinking...")
            return

        if self.current_player != Board.PLAYER_X:
            return

        if self.board.get_position(flat_index) != Board.EMPTY:
            messagebox.showwarning("Invalid Move", "Position already occupied.")
            return

        # Make move
        self.board.set_position(flat_index, Board.PLAYER_X)
        layer, row, col = Board._to_coordinates(flat_index)
        
        # Display human move
        self.ai_info_label.config(
            text=f"Your move:\nLayer {layer}, Row {row}, Col {col}\n\n"
                 f"Waiting for AI..."
        )
        
        self.update_display()

        # Check game over
        if self.rules.is_game_over():
            self.end_game()
            return

        # Switch to AI
        self.current_player = Board.PLAYER_O
        self.update_display()
        
        # Start AI thinking
        self.ai_thinking = True
        self.update_display()
        threading.Thread(target=self.ai_move, daemon=True).start()

    def ai_move(self):
        """Execute AI move using Minimax with Alpha-Beta Pruning."""
        try:
            # Create minimax instance
            # Uses Alpha-Beta Pruning internally
            minimax = Minimax(
                search_depth=3,  # Reduced to 3 for faster response (2-5 seconds)
                heuristic='advanced',  # Uses heuristic function
                use_transposition_table=True,
                verbose=False
            )

            # Get best move using Minimax + Alpha-Beta + Heuristic
            best_move, score, stats = minimax.get_best_move(
                self.board.copy(),
                GameRules(self.board.copy()),
                Board.PLAYER_O
            )

            # Schedule UI update on main thread
            self.root.after(0, self.finalize_ai_move, best_move, score, stats)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("AI Error", str(e)))
            self.ai_thinking = False

    def finalize_ai_move(self, move: int, score: float, stats: dict):
        """Finalize AI move and display decision information."""
        # Check if game was reset while AI was thinking
        if self.game_over and self.board.count_moves() == 0:
            self.ai_thinking = False
            return
            
        if self.game_over:
            self.ai_thinking = False
            return

        # Make AI move
        self.board.set_position(move, Board.PLAYER_O)
        layer, row, col = Board._to_coordinates(move)

        # Display AI decision clearly (Requirement 4)
        nodes = stats.get('nodes_explored', 0)
        time_taken = stats.get('time_elapsed', 0)
        
        ai_decision = (
            f"AI Decision:\n"
            f"━━━━━━━━━━━━━━━━━\n"
            f"Position: Layer {layer}, Row {row}, Col {col}\n\n"
            f"Evaluation Score: {score:.2f}\n"
            f"(Higher = Better for AI)\n\n"
            f"Nodes Explored: {nodes:,}\n"
            f"(Using Minimax + Alpha-Beta)\n\n"
            f"Time: {time_taken:.2f}s\n"
            f"━━━━━━━━━━━━━━━━━\n"
            f"Algorithm: Minimax with\nAlpha-Beta Pruning\n"
            f"Heuristic: Advanced"
        )
        
        self.ai_info_label.config(text=ai_decision)

        self.update_display()

        # Check game over
        if self.rules.is_game_over():
            self.end_game()
            return

        # Switch back to human
        self.current_player = Board.PLAYER_X
        self.ai_thinking = False
        self.update_display()

    def end_game(self):
        """Handle game ending."""
        self.game_over = True
        self.winning_line = self.rules.get_winner_line()
        self.update_display()

        state = self.rules.get_game_state()
        
        # Get winning line description
        win_description = ""
        if self.winning_line:
            coords = [Board._to_coordinates(pos) for pos in self.winning_line]
            layers = [c[0] for c in coords]
            rows = [c[1] for c in coords]
            cols = [c[2] for c in coords]
            
            # Describe the winning line
            if len(set(layers)) == 1:
                win_description = f"\n\nWinning line on Layer {layers[0]}"
            elif len(set(rows)) == 1:
                win_description = f"\n\nWinning line on Row {rows[0]}"
            elif len(set(cols)) == 1:
                win_description = f"\n\nWinning line on Column {cols[0]}"
            else:
                win_description = "\n\nWinning 3D diagonal!"
        
        if state == "x_wins":
            messagebox.showinfo("Game Over", f"🎉 Congratulations! You Win!{win_description}\n\nThe winning positions are highlighted in GREEN.")
        elif state == "o_wins":
            messagebox.showinfo("Game Over", f"🤖 AI Wins!{win_description}\n\nBetter luck next time!\n\nThe winning positions are highlighted in GREEN.")
        else:
            messagebox.showinfo("Game Over", "🤝 It's a Draw!\n\nNo more moves available.")

    def new_game(self):
        """Start a new game."""
        # Wait for AI thread to finish if it's running
        if self.ai_thinking and self.ai_thread and self.ai_thread.is_alive():
            messagebox.showinfo("Please Wait", "AI is still thinking. Please wait a moment...")
            return

        # Reset everything
        self.board = Board()
        self.rules = GameRules(self.board)
        self.current_player = Board.PLAYER_X
        self.game_over = False
        self.winning_line = None
        self.ai_thinking = False
        self.ai_thread = None

        self.ai_info_label.config(text="New game started!\n\nMake your first move...")
        self.update_display()


def main():
    """Entry point for the GUI."""
    root = tk.Tk()
    gui = CubicGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()