from typing import List, Optional, Tuple
from cubic.board import Board


class GameRules:
    def __init__(self, board: Board):
        self.board = board
        self.winning_lines = self._generate_winning_lines()
    
    def _generate_winning_lines(self) -> List[List[int]]:
        lines = []
        
        for layer in range(4):
            for row in range(4):
                line = [Board._to_flat_index(layer, row, col) for col in range(4)]
                lines.append(line)
        
        for layer in range(4):
            for col in range(4):
                line = [Board._to_flat_index(layer, row, col) for row in range(4)]
                lines.append(line)
        
        for row in range(4):
            for col in range(4):
                line = [Board._to_flat_index(layer, row, col) for layer in range(4)]
                lines.append(line)
        
        for layer in range(4):
            line1 = [Board._to_flat_index(layer, i, i) for i in range(4)]
            lines.append(line1)
            line2 = [Board._to_flat_index(layer, i, 3-i) for i in range(4)]
            lines.append(line2)
        
        for row in range(4):
            line1 = [Board._to_flat_index(i, row, i) for i in range(4)]
            lines.append(line1)
            line2 = [Board._to_flat_index(i, row, 3-i) for i in range(4)]
            lines.append(line2)
        
        for col in range(4):
            line1 = [Board._to_flat_index(i, i, col) for i in range(4)]
            lines.append(line1)
            line2 = [Board._to_flat_index(i, 3-i, col) for i in range(4)]
            lines.append(line2)
        
        lines.append([Board._to_flat_index(i, i, i) for i in range(4)])
        lines.append([Board._to_flat_index(i, i, 3-i) for i in range(4)])
        lines.append([Board._to_flat_index(i, 3-i, i) for i in range(4)])
        lines.append([Board._to_flat_index(i, 3-i, 3-i) for i in range(4)])
        
        return lines
    
    def check_winner(self) -> Optional[int]:
        for line in self.winning_lines:
            positions = [self.board.get_position(pos) for pos in line]
            
            if positions[0] != Board.EMPTY and all(p == positions[0] for p in positions):
                return positions[0]
        
        return None
    
    def get_winner_line(self) -> Optional[List[int]]:
        for line in self.winning_lines:
            positions = [self.board.get_position(pos) for pos in line]
            
            if positions[0] != Board.EMPTY and all(p == positions[0] for p in positions):
                return line
        
        return None
    
    def is_game_over(self) -> bool:
        return self.check_winner() is not None or self.board.is_full()
    
    def get_game_state(self) -> str:
        winner = self.check_winner()
        if winner == Board.PLAYER_X:
            return "x_wins"
        elif winner == Board.PLAYER_O:
            return "o_wins"
        elif self.board.is_full():
            return "draw"
        else:
            return "ongoing"