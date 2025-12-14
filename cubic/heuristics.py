from cubic.board import Board
from cubic.rules import GameRules


class HeuristicEvaluator:
    def __init__(self, heuristic_type: str = 'advanced'):
        self.heuristic_type = heuristic_type
    
    def evaluate(self, board: Board, rules: GameRules, maximizing_player: int) -> float:
        winner = rules.check_winner()
        if winner == maximizing_player:
            return 10000.0
        elif winner is not None:
            return -10000.0
        elif board.is_full():
            return 0.0
        
        if self.heuristic_type == 'simple':
            return self._simple_heuristic(board, rules, maximizing_player)
        else:
            return self._advanced_heuristic(board, rules, maximizing_player)
    
    def _simple_heuristic(self, board: Board, rules: GameRules, player: int) -> float:
        opponent = Board.PLAYER_O if player == Board.PLAYER_X else Board.PLAYER_X
        
        player_score = 0
        opponent_score = 0
        
        for line in rules.winning_lines:
            positions = [board.get_position(pos) for pos in line]
            
            player_count = positions.count(player)
            opponent_count = positions.count(opponent)
            
            if opponent_count == 0 and player_count > 0:
                player_score += player_count ** 2
            
            if player_count == 0 and opponent_count > 0:
                opponent_score += opponent_count ** 2
        
        return player_score - opponent_score
    
    def _advanced_heuristic(self, board: Board, rules: GameRules, player: int) -> float:
        opponent = Board.PLAYER_O if player == Board.PLAYER_X else Board.PLAYER_X
        
        score = 0.0
        
        THREAT_3 = 500.0
        TWO_IN_ROW = 50.0
        ONE_IN_ROW = 5.0
        CENTER_BONUS = 10.0
        
        for line in rules.winning_lines:
            positions = [board.get_position(pos) for pos in line]
            
            player_count = positions.count(player)
            opponent_count = positions.count(opponent)
            empty_count = positions.count(Board.EMPTY)
            
            if opponent_count == 0:
                if player_count == 3 and empty_count == 1:
                    score += THREAT_3
                elif player_count == 2 and empty_count == 2:
                    score += TWO_IN_ROW
                elif player_count == 1 and empty_count == 3:
                    score += ONE_IN_ROW
            
            if player_count == 0:
                if opponent_count == 3 and empty_count == 1:
                    score -= THREAT_3 * 1.2
                elif opponent_count == 2 and empty_count == 2:
                    score -= TWO_IN_ROW
                elif opponent_count == 1 and empty_count == 3:
                    score -= ONE_IN_ROW
        
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