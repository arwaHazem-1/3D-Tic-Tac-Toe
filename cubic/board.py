from typing import List, Tuple


class Board:
    EMPTY = 0
    PLAYER_X = 1
    PLAYER_O = 2
    
    def __init__(self):
        self.board: List[int] = [self.EMPTY] * 64
        self.move_history: List[int] = []
    
    def copy(self) -> 'Board':
        new_board = Board()
        new_board.board = self.board.copy()
        new_board.move_history = self.move_history.copy()
        return new_board
    
    @staticmethod
    def _to_flat_index(layer: int, row: int, col: int) -> int:
        return layer * 16 + row * 4 + col
    
    @staticmethod
    def _to_coordinates(flat_index: int) -> Tuple[int, int, int]:
        layer = flat_index // 16
        row = (flat_index % 16) // 4
        col = flat_index % 4
        return layer, row, col
    
    def get_position(self, flat_index: int) -> int:
        return self.board[flat_index]
    
    def set_position(self, flat_index: int, player: int) -> None:
        if self.board[flat_index] == self.EMPTY:
            self.board[flat_index] = player
            self.move_history.append(flat_index)
    
    def get_legal_moves(self) -> List[int]:
        return [i for i in range(64) if self.board[i] == self.EMPTY]
    
    def is_full(self) -> bool:
        return all(pos != self.EMPTY for pos in self.board)
    
    def count_moves(self) -> int:
        return len(self.move_history)