"""
Heuristic evaluation functions for Cubic game.
Provides quick assessment of board states.
"""

from cubic.board import Board
from cubic.rules import GameRules


class HeuristicEvaluator:
    """Evaluates board positions using heuristic functions."""
    
    def __init__(self, heuristic_type: str = 'advanced'):
        """
        Initialize evaluator.
        
        Args:
            heuristic_type: 'simple' or 'advanced'
        """
        self.heuristic_type = heuristic_type
    
    def evaluate(self, board: Board, rules: GameRules, maximizing_player: int) -> float:
        """
        Evaluate board state from perspective of maximizing player.
        
        Args:
            board: Current board state
            rules: Game rules instance
            maximizing_player: Player to maximize for (PLAYER_X or PLAYER_O)
        
        Returns:
            Score (positive = good for maximizing player)
        """
        # Check terminal states first
        winner = rules.check_winner()
        if winner == maximizing_player:
            return 10000.0  # Win
        elif winner is not None:
            return -10000.0  # Loss
        elif board.is_full():
            return 0.0  # Draw
        
        # Use selected heuristic
        if self.heuristic_type == 'simple':
            return self._simple_heuristic(board, rules, maximizing_player)
        else:
            return self._advanced_heuristic(board, rules, maximizing_player)
    
    def _simple_heuristic(self, board: Board, rules: GameRules, player: int) -> float:
        """
        Simple heuristic: Count open lines for each player.
        
        An open line is one that contains only one player's marks (no opponent).
        """
        opponent = Board.PLAYER_O if player == Board.PLAYER_X else Board.PLAYER_X
        
        player_score = 0
        opponent_score = 0
        
        for line in rules.winning_lines:
            positions = [board.get_position(pos) for pos in line]
            
            player_count = positions.count(player)
            opponent_count = positions.count(opponent)
            
            # Line is "open" for player if opponent has no marks in it
            if opponent_count == 0 and player_count > 0:
                player_score += player_count ** 2  # Weight by square
            
            # Line is "open" for opponent if player has no marks in it
            if player_count == 0 and opponent_count > 0:
                opponent_score += opponent_count ** 2
        
        return player_score - opponent_score
    
    def _advanced_heuristic(self, board: Board, rules: GameRules, player: int) -> float:
        """
        Advanced heuristic: Pattern-based evaluation with spatial awareness.
        
        Considers:
        - Threats (3 in a row with 1 empty)
        - Two in a row patterns
        - Center control
        - Blocking opponent threats
        """
        opponent = Board.PLAYER_O if player == Board.PLAYER_X else Board.PLAYER_X
        
        score = 0.0
        
        # Weight factors
        THREAT_3 = 500.0      # Three in a row (immediate threat)
        TWO_IN_ROW = 50.0     # Two in a row
        ONE_IN_ROW = 5.0      # Single piece in line
        CENTER_BONUS = 10.0   # Center positions
        
        for line in rules.winning_lines:
            positions = [board.get_position(pos) for pos in line]
            
            player_count = positions.count(player)
            opponent_count = positions.count(opponent)
            empty_count = positions.count(Board.EMPTY)
            
            # Player's potential
            if opponent_count == 0:  # Line open for player
                if player_count == 3 and empty_count == 1:
                    score += THREAT_3  # Winning threat
                elif player_count == 2 and empty_count == 2:
                    score += TWO_IN_ROW
                elif player_count == 1 and empty_count == 3:
                    score += ONE_IN_ROW
            
            # Opponent's threats (must block)
            if player_count == 0:  # Line open for opponent
                if opponent_count == 3 and empty_count == 1:
                    score -= THREAT_3 * 1.2  # Blocking is slightly more important
                elif opponent_count == 2 and empty_count == 2:
                    score -= TWO_IN_ROW
                elif opponent_count == 1 and empty_count == 3:
                    score -= ONE_IN_ROW
        
        # Center control bonus
        center_positions = [
            Board._to_flat_index(1, 1, 1),
            Board._to_flat_index(1, 1, 2),
            Board._to_flat_index(1, 2, 1),
            Board._to_flat_index(1, 2, 2),
            Board._to_flat_index(2, 1, 1),
            Board._to_flat_index(2, 1, 2),
            Board._to_flat_index(2, 2, 1),
            Board._to_flat_index(2, 2, 2),
        ]
        
        for pos in center_positions:
            if board.get_position(pos) == player:
                score += CENTER_BONUS
            elif board.get_position(pos) == opponent:
                score -= CENTER_BONUS
        
        return score