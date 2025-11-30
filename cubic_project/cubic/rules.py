"""
Game rules and win detection for 4x4x4 Cubic.
Detects all 76 possible winning lines.
"""

from typing import List, Optional, Tuple
from cubic.board import Board


class GameRules:
    """Handles game rules and win detection for Cubic."""
    
    def __init__(self, board: Board):
        """Initialize with a board."""
        self.board = board
        self.winning_lines = self._generate_winning_lines()
    
    def _generate_winning_lines(self) -> List[List[int]]:
        """Generate all 76 winning lines in the 4x4x4 cube."""
        lines = []
        
        # 1. Lines parallel to X-axis (16 lines)
        for layer in range(4):
            for row in range(4):
                line = [Board._to_flat_index(layer, row, col) for col in range(4)]
                lines.append(line)
        
        # 2. Lines parallel to Y-axis (16 lines)
        for layer in range(4):
            for col in range(4):
                line = [Board._to_flat_index(layer, row, col) for row in range(4)]
                lines.append(line)
        
        # 3. Lines parallel to Z-axis (16 lines)
        for row in range(4):
            for col in range(4):
                line = [Board._to_flat_index(layer, row, col) for layer in range(4)]
                lines.append(line)
        
        # 4. Diagonals in XY planes (8 lines)
        for layer in range(4):
            # Main diagonal
            line1 = [Board._to_flat_index(layer, i, i) for i in range(4)]
            lines.append(line1)
            # Anti-diagonal
            line2 = [Board._to_flat_index(layer, i, 3-i) for i in range(4)]
            lines.append(line2)
        
        # 5. Diagonals in XZ planes (8 lines)
        for row in range(4):
            # Main diagonal
            line1 = [Board._to_flat_index(i, row, i) for i in range(4)]
            lines.append(line1)
            # Anti-diagonal
            line2 = [Board._to_flat_index(i, row, 3-i) for i in range(4)]
            lines.append(line2)
        
        # 6. Diagonals in YZ planes (8 lines)
        for col in range(4):
            # Main diagonal
            line1 = [Board._to_flat_index(i, i, col) for i in range(4)]
            lines.append(line1)
            # Anti-diagonal
            line2 = [Board._to_flat_index(i, 3-i, col) for i in range(4)]
            lines.append(line2)
        
        # 7. Space diagonals (4 lines)
        # Main space diagonal (0,0,0) to (3,3,3)
        lines.append([Board._to_flat_index(i, i, i) for i in range(4)])
        # (0,0,3) to (3,3,0)
        lines.append([Board._to_flat_index(i, i, 3-i) for i in range(4)])
        # (0,3,0) to (3,0,3)
        lines.append([Board._to_flat_index(i, 3-i, i) for i in range(4)])
        # (0,3,3) to (3,0,0)
        lines.append([Board._to_flat_index(i, 3-i, 3-i) for i in range(4)])
        
        return lines
    
    def check_winner(self) -> Optional[int]:
        """Check if there's a winner. Returns PLAYER_X, PLAYER_O, or None."""
        for line in self.winning_lines:
            positions = [self.board.get_position(pos) for pos in line]
            
            # Check if all positions in line are same and not empty
            if positions[0] != Board.EMPTY and all(p == positions[0] for p in positions):
                return positions[0]
        
        return None
    
    def get_winner_line(self) -> Optional[List[int]]:
        """Get the winning line positions if there's a winner."""
        for line in self.winning_lines:
            positions = [self.board.get_position(pos) for pos in line]
            
            if positions[0] != Board.EMPTY and all(p == positions[0] for p in positions):
                return line
        
        return None
    
    def is_game_over(self) -> bool:
        """Check if game is over (win or draw)."""
        return self.check_winner() is not None or self.board.is_full()
    
    def get_game_state(self) -> str:
        """Get current game state."""
        winner = self.check_winner()
        if winner == Board.PLAYER_X:
            return "x_wins"
        elif winner == Board.PLAYER_O:
            return "o_wins"
        elif self.board.is_full():
            return "draw"
        else:
            return "ongoing"