import tkinter as tk
from tkinter import messagebox
import threading
from typing import List, Tuple
from cubic.board import Board
from cubic.rules import GameRules
from cubic.players import HumanPlayer, AIPlayer
from cubic.minimax import Minimax


class CubicGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Cubic: 4x4x4 3D Tic-Tac-Toe")
        self.root.geometry("1000x750")

        self.board = Board()
        self.rules = GameRules(self.board)
        self.player_x = HumanPlayer(Board.PLAYER_X)
        self.player_o = AIPlayer(Board.PLAYER_O, depth=3)
        self.current_player = Board.PLAYER_X
        self.game_over = False
        self.winning_line = None

        self.ai_thinking = False
        self.ai_thread = None
        
        self.ai_heuristic = tk.StringVar(value='advanced')
        self.ai_use_alpha_beta = tk.BooleanVar(value=True)
        self.ai_use_symmetry = tk.BooleanVar(value=False)
        self.ai_use_heuristic_reduction = tk.BooleanVar(value=False)
        self.ai_depth = tk.IntVar(value=3)

        self.canvas_buttons: List[Tuple[int, tk.Button]] = []

        self.setup_ui()
        self.update_display()

    def setup_ui(self):
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        title_frame.pack(fill=tk.X)
        tk.Label(
            title_frame,
            text="4x4x4 Cubic - Human vs AI",
            font=("Arial", 18, "bold"),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=10)

        content_frame = tk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        board_frame = tk.Frame(content_frame)
        board_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            board_frame,
            text="Game Board (4 Layers)",
            font=("Arial", 14, "bold")
        ).pack(pady=5)

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

        info_frame = tk.Frame(content_frame, bg='#2c3e50', width=280)
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        info_frame.pack_propagate(False)
        
        settings_frame = tk.LabelFrame(
            info_frame,
            text="AI Algorithm Settings",
            font=("Arial", 11, "bold"),
            bg='#2c3e50',
            fg='white',
            padx=5,
            pady=5
        )
        settings_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(
            settings_frame,
            text="Heuristic:",
            font=("Arial", 9),
            bg='#2c3e50',
            fg='white'
        ).pack(anchor=tk.W, pady=2)
        heuristic_frame = tk.Frame(settings_frame, bg='#2c3e50')
        heuristic_frame.pack(fill=tk.X, pady=2)
        tk.Radiobutton(
            heuristic_frame,
            text="None",
            variable=self.ai_heuristic,
            value='none',
            bg='#2c3e50',
            fg='white',
            selectcolor='#2c3e50',
            activebackground='#2c3e50',
            activeforeground='white',
            font=("Arial", 8)
        ).pack(side=tk.LEFT, padx=2)
        tk.Radiobutton(
            heuristic_frame,
            text="Simple",
            variable=self.ai_heuristic,
            value='simple',
            bg='#2c3e50',
            fg='white',
            selectcolor='#2c3e50',
            activebackground='#2c3e50',
            activeforeground='white',
            font=("Arial", 8)
        ).pack(side=tk.LEFT, padx=2)
        tk.Radiobutton(
            heuristic_frame,
            text="Advanced",
            variable=self.ai_heuristic,
            value='advanced',
            bg='#2c3e50',
            fg='white',
            selectcolor='#2c3e50',
            activebackground='#2c3e50',
            activeforeground='white',
            font=("Arial", 8)
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Checkbutton(
            settings_frame,
            text="Alpha-Beta Pruning",
            variable=self.ai_use_alpha_beta,
            bg='#2c3e50',
            fg='white',
            selectcolor='#2c3e50',
            activebackground='#2c3e50',
            activeforeground='white',
            font=("Arial", 9)
        ).pack(anchor=tk.W, pady=2)
        
        tk.Checkbutton(
            settings_frame,
            text="Symmetry Reduction",
            variable=self.ai_use_symmetry,
            bg='#2c3e50',
            fg='white',
            selectcolor='#2c3e50',
            activebackground='#2c3e50',
            activeforeground='white',
            font=("Arial", 9)
        ).pack(anchor=tk.W, pady=2)
        
        tk.Checkbutton(
            settings_frame,
            text="Heuristic Reduction",
            variable=self.ai_use_heuristic_reduction,
            bg='#2c3e50',
            fg='white',
            selectcolor='#2c3e50',
            activebackground='#2c3e50',
            activeforeground='white',
            font=("Arial", 9)
        ).pack(anchor=tk.W, pady=2)
        
        depth_frame = tk.Frame(settings_frame, bg='#2c3e50')
        depth_frame.pack(fill=tk.X, pady=2)
        tk.Label(
            depth_frame,
            text="Depth:",
            font=("Arial", 9),
            bg='#2c3e50',
            fg='white'
        ).pack(side=tk.LEFT)
        depth_spin = tk.Spinbox(
            depth_frame,
            from_=1,
            to=5,
            textvariable=self.ai_depth,
            width=5,
            font=("Arial", 9),
            bg='#2c3e50',
            fg='white',
            buttonbackground='#2c3e50'
        )
        depth_spin.pack(side=tk.LEFT, padx=5)
        
        tk.Frame(info_frame, bg='#7f8c8d', height=2).pack(fill=tk.X, pady=5)

        tk.Label(
            info_frame,
            text="Current Turn",
            font=("Arial", 12, "bold"),
            bg='#2c3e50',
            fg='white'
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

        tk.Frame(info_frame, bg='#7f8c8d', height=2).pack(fill=tk.X, pady=10)

        tk.Label(
            info_frame,
            text="AI Analysis",
            font=("Arial", 12, "bold"),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=5)

        self.ai_info_label = tk.Label(
            info_frame,
            text="Waiting for your move...",
            font=("Arial", 9),
            bg='white',
            fg='#2c3e50',
            wraplength=250,
            justify=tk.LEFT,
            relief=tk.SUNKEN,
            padx=8,
            pady=8,
            height=10
        )
        self.ai_info_label.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        self.move_label = tk.Label(
            info_frame,
            text="Moves: 0",
            font=("Arial", 10),
            bg='#2c3e50',
            fg='white'
        )
        self.move_label.pack(pady=10)

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
        for flat_index, btn in self.canvas_buttons:
            value = self.board.get_position(flat_index)
            is_winning = self.winning_line and flat_index in self.winning_line

            if value == Board.PLAYER_X:
                btn.config(
                    text="X",
                    fg='white',
                    bg='#27ae60' if is_winning else '#3498db',
                    disabledforeground='white',
                    relief=tk.RAISED if is_winning else tk.FLAT,
                    bd=3 if is_winning else 1
                )
            elif value == Board.PLAYER_O:
                btn.config(
                    text="O",
                    fg='white',
                    bg='#27ae60' if is_winning else '#e74c3c',
                    disabledforeground='white',
                    relief=tk.RAISED if is_winning else tk.FLAT,
                    bd=3 if is_winning else 1
                )
            else:
                btn.config(
                    text="",
                    bg='#f39c12' if is_winning else 'white',
                    state=tk.NORMAL if not self.game_over and not self.ai_thinking else tk.DISABLED,
                    relief=tk.FLAT,
                    bd=1
                )

        moves = self.board.count_moves()
        self.move_label.config(text=f"Moves: {moves}")

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

        self.board.set_position(flat_index, Board.PLAYER_X)
        layer, row, col = Board._to_coordinates(flat_index)
        
        self.ai_info_label.config(
            text=f"Your move:\nLayer {layer}, Row {row}, Col {col}\n\n"
                 f"Waiting for AI..."
        )
        
        self.update_display()

        if self.rules.is_game_over():
            self.end_game()
            return

        self.current_player = Board.PLAYER_O
        self.update_display()
        
        self.ai_thinking = True
        self.update_display()
        threading.Thread(target=self.ai_move, daemon=True).start()

    def ai_move(self):
        try:
            heuristic = self.ai_heuristic.get()
            use_heuristic = heuristic != 'none'
            heuristic_type = None if heuristic == 'none' else heuristic
            
            minimax = Minimax(
                search_depth=self.ai_depth.get(),
                heuristic=heuristic_type,
                use_alpha_beta=self.ai_use_alpha_beta.get(),
                use_transposition_table=True,
                use_symmetry_reduction=self.ai_use_symmetry.get(),
                use_heuristic_reduction=self.ai_use_heuristic_reduction.get(),
                verbose=False
            )

            best_move, score, stats = minimax.get_best_move(
                self.board.copy(),
                GameRules(self.board.copy()),
                Board.PLAYER_O
            )

            self.root.after(0, self.finalize_ai_move, best_move, score, stats)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("AI Error", str(e)))
            self.ai_thinking = False

    def finalize_ai_move(self, move: int, score: float, stats: dict):
        if self.game_over and self.board.count_moves() == 0:
            self.ai_thinking = False
            return
            
        if self.game_over:
            self.ai_thinking = False
            return

        self.board.set_position(move, Board.PLAYER_O)
        layer, row, col = Board._to_coordinates(move)

        nodes = stats.get('nodes_explored', 0)
        pruned = stats.get('pruned_nodes', 0)
        time_taken = stats.get('time_elapsed', 0)
        heuristic = stats.get('heuristic', 'none')
        alpha_beta = stats.get('alpha_beta', False)
        symmetry = stats.get('symmetry_reduction', False)
        heuristic_red = stats.get('heuristic_reduction', False)
        
        algo_parts = ["Minimax"]
        if alpha_beta:
            algo_parts.append("Alpha-Beta")
        if symmetry:
            algo_parts.append("Symmetry")
        if heuristic_red:
            algo_parts.append("Heuristic Red.")
        
        ai_decision = (
            f"AI Decision:\n"
            f"━━━━━━━━━━━━━━━━━\n"
            f"Position: Layer {layer}, Row {row}, Col {col}\n\n"
            f"Evaluation Score: {score:.2f}\n"
            f"(Higher = Better for AI)\n\n"
            f"Nodes Explored: {nodes:,}\n"
        )
        
        if alpha_beta and pruned > 0:
            ai_decision += f"Pruned Nodes: {pruned:,}\n"
        
        ai_decision += (
            f"Time: {time_taken:.2f}s\n"
            f"━━━━━━━━━━━━━━━━━\n"
            f"Algorithm: {' + '.join(algo_parts)}\n"
            f"Heuristic: {heuristic.title()}\n"
            f"Depth: {stats.get('depth', 3)}"
        )
        
        self.ai_info_label.config(text=ai_decision)

        self.update_display()

        if self.rules.is_game_over():
            self.end_game()
            return

        self.current_player = Board.PLAYER_X
        self.ai_thinking = False
        self.update_display()

    def end_game(self):
        self.game_over = True
        self.winning_line = self.rules.get_winner_line()
        self.update_display()

        state = self.rules.get_game_state()
        
        win_description = ""
        if self.winning_line:
            coords = [Board._to_coordinates(pos) for pos in self.winning_line]
            layers = [c[0] for c in coords]
            rows = [c[1] for c in coords]
            cols = [c[2] for c in coords]
            
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
        if self.ai_thinking and self.ai_thread and self.ai_thread.is_alive():
            messagebox.showinfo("Please Wait", "AI is still thinking. Please wait a moment...")
            return

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
    root = tk.Tk()
    gui = CubicGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()