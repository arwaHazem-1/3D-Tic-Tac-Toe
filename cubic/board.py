"""
Board representation for 4x4x4 Cubic game.
Handles 3D to flat indexing conversion.
"""

from typing import List, Tuple


class Board:
    """Represents a 4x4x4 Cubic game board."""
    
    # Player constants
    EMPTY = 0
    PLAYER_X = 1
    PLAYER_O = 2
    
    def __init__(self):
        """Initialize empty 4x4x4 board (64 positions)."""
        self.board: List[int] = [self.EMPTY] * 64
        self.move_history: List[int] = []
    
    def copy(self) -> 'Board':
        """Create a deep copy of the board."""
        new_board = Board()
        new_board.board = self.board.copy()
        new_board.move_history = self.move_history.copy()
        return new_board
    
    @staticmethod
    def _to_flat_index(layer: int, row: int, col: int) -> int:
        """Convert 3D coordinates to flat index."""
        return layer * 16 + row * 4 + col
    
    @staticmethod
    def _to_coordinates(flat_index: int) -> Tuple[int, int, int]:
        """Convert flat index to 3D coordinates."""
        layer = flat_index // 16
        row = (flat_index % 16) // 4
        col = flat_index % 4
        return layer, row, col
    
    def get_position(self, flat_index: int) -> int:
        """Get the value at a position."""
        return self.board[flat_index]
    
    def set_position(self, flat_index: int, player: int) -> None:
        """Set a position to a player's mark."""
        if self.board[flat_index] == self.EMPTY:
            self.board[flat_index] = player
            self.move_history.append(flat_index)
    
    def get_legal_moves(self) -> List[int]:
        """Get all legal (empty) positions."""
        return [i for i in range(64) if self.board[i] == self.EMPTY]
    
    def is_full(self) -> bool:
        """Check if board is completely filled."""
        return all(pos != self.EMPTY for pos in self.board)
    
    def count_moves(self) -> int:
        """Count total moves made."""
        return len(self.move_history)