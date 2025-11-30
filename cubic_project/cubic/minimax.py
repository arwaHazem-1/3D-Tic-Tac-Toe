"""
Minimax algorithm with Alpha-Beta Pruning for Cubic game.
"""

import time
from typing import Tuple, Dict, Optional
from cubic.board import Board
from cubic.rules import GameRules
from cubic.heuristics import HeuristicEvaluator


class Minimax:
    """
    Minimax search with Alpha-Beta Pruning.
    
    Implements:
    1. Minimax algorithm for optimal move selection
    2. Alpha-Beta pruning for efficiency
    3. Heuristic evaluation for non-terminal states
    """
    
    def __init__(
        self,
        search_depth: int = 4,
        heuristic: str = 'advanced',
        use_transposition_table: bool = True,
        verbose: bool = False
    ):
        """
        Initialize Minimax search.
        
        Args:
            search_depth: Maximum depth to search
            heuristic: 'simple' or 'advanced'
            use_transposition_table: Enable position caching
            verbose: Print search statistics
        """
        self.search_depth = search_depth
        self.evaluator = HeuristicEvaluator(heuristic)
        self.use_transposition_table = use_transposition_table
        self.verbose = verbose
        
        # Statistics
        self.nodes_explored = 0
        self.transposition_table: Dict[str, Tuple[float, int]] = {}
    
    def get_best_move(
        self,
        board: Board,
        rules: GameRules,
        player: int
    ) -> Tuple[Optional[int], float, Dict]:
        """
        Find the best move using Minimax with Alpha-Beta Pruning.
        
        Args:
            board: Current board state
            rules: Game rules
            player: Current player (PLAYER_X or PLAYER_O)
        
        Returns:
            Tuple of (best_move, best_score, statistics)
        """
        # Reset statistics
        self.nodes_explored = 0
        if self.use_transposition_table:
            self.transposition_table.clear()
        
        start_time = time.time()
        
        # Get legal moves
        legal_moves = board.get_legal_moves()
        if not legal_moves:
            return None, 0.0, {}
        
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        # Try each legal move
        for move in legal_moves:
            # Make move
            test_board = board.copy()
            test_board.set_position(move, player)
            test_rules = GameRules(test_board)
            
            # Evaluate using minimax (opponent's turn, so minimize)
            score = self._minimax(
                test_board,
                test_rules,
                self.search_depth - 1,
                alpha,
                beta,
                False,  # Opponent's turn (minimize)
                player
            )
            
            # Update best move
            if score > best_score:
                best_score = score
                best_move = move
            
            # Update alpha for pruning
            alpha = max(alpha, best_score)
        
        end_time = time.time()
        
        # Statistics
        stats = {
            'nodes_explored': self.nodes_explored,
            'time_elapsed': end_time - start_time,
            'depth': self.search_depth
        }
        
        if self.verbose:
            print(f"Minimax Search Complete:")
            print(f"  Nodes explored: {self.nodes_explored:,}")
            print(f"  Time: {stats['time_elapsed']:.3f}s")
            print(f"  Best score: {best_score:.2f}")
        
        return best_move, best_score, stats
    
    def _minimax(
        self,
        board: Board,
        rules: GameRules,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
        original_player: int
    ) -> float:
        """
        Minimax algorithm with Alpha-Beta Pruning.
        
        Args:
            board: Current board state
            rules: Game rules
            depth: Remaining search depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            maximizing: True if maximizing, False if minimizing
            original_player: The player we're finding best move for
        
        Returns:
            Evaluation score
        """
        self.nodes_explored += 1
        
        # Check transposition table
        if self.use_transposition_table:
            board_key = self._board_hash(board)
            if board_key in self.transposition_table:
                cached_score, cached_depth = self.transposition_table[board_key]
                if cached_depth >= depth:
                    return cached_score
        
        # Terminal conditions
        if rules.is_game_over() or depth == 0:
            score = self.evaluator.evaluate(board, rules, original_player)
            
            # Cache result
            if self.use_transposition_table:
                board_key = self._board_hash(board)
                self.transposition_table[board_key] = (score, depth)
            
            return score
        
        legal_moves = board.get_legal_moves()
        
        if maximizing:
            # Maximizing player's turn
            max_eval = float('-inf')
            current_player = original_player
            
            for move in legal_moves:
                # Make move
                test_board = board.copy()
                test_board.set_position(move, current_player)
                test_rules = GameRules(test_board)
                
                # Recursive call (switch to minimizing)
                eval_score = self._minimax(
                    test_board,
                    test_rules,
                    depth - 1,
                    alpha,
                    beta,
                    False,
                    original_player
                )
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                # Alpha-Beta Pruning
                if beta <= alpha:
                    break  # Beta cutoff
            
            return max_eval
        
        else:
            # Minimizing player's turn (opponent)
            min_eval = float('inf')
            opponent = Board.PLAYER_O if original_player == Board.PLAYER_X else Board.PLAYER_X
            
            for move in legal_moves:
                # Make move
                test_board = board.copy()
                test_board.set_position(move, opponent)
                test_rules = GameRules(test_board)
                
                # Recursive call (switch to maximizing)
                eval_score = self._minimax(
                    test_board,
                    test_rules,
                    depth - 1,
                    alpha,
                    beta,
                    True,
                    original_player
                )
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                # Alpha-Beta Pruning
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_eval
    
    def _board_hash(self, board: Board) -> str:
        """Create a hash key for the board state."""
        return ''.join(str(p) for p in board.board)