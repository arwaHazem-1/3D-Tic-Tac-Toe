import time
from typing import Tuple, Dict, Optional, List, Set
from cubic.board import Board
from cubic.rules import GameRules
from cubic.heuristics import HeuristicEvaluator


class Minimax:
    def __init__(
        self,
        search_depth: int = 4,
        heuristic: Optional[str] = 'advanced',
        use_alpha_beta: bool = True,
        use_transposition_table: bool = True,
        use_symmetry_reduction: bool = False,
        use_heuristic_reduction: bool = False,
        verbose: bool = False
    ):
        self.search_depth = search_depth
        self.use_heuristic = heuristic is not None
        self.heuristic = heuristic if heuristic else 'advanced'
        self.evaluator = HeuristicEvaluator(self.heuristic) if self.use_heuristic else None
        self.use_alpha_beta = use_alpha_beta
        self.use_transposition_table = use_transposition_table
        self.use_symmetry_reduction = use_symmetry_reduction
        self.use_heuristic_reduction = use_heuristic_reduction
        self.verbose = verbose
        
        self.nodes_explored = 0
        self.pruned_nodes = 0
        self.transposition_table: Dict[str, Tuple[float, int]] = {}
        
        if self.use_symmetry_reduction:
            self.symmetry_cache: Dict[str, List[int]] = {}
    
    def get_best_move(
        self,
        board: Board,
        rules: GameRules,
        player: int
    ) -> Tuple[Optional[int], float, Dict]:
        self.nodes_explored = 0
        self.pruned_nodes = 0
        if self.use_transposition_table:
            self.transposition_table.clear()
        if self.use_symmetry_reduction:
            self.symmetry_cache.clear()
        
        start_time = time.time()
        
        legal_moves = self._get_reduced_moves(board, player)
        if not legal_moves:
            return None, 0.0, {}
        
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        for move in legal_moves:
            test_board = board.copy()
            test_board.set_position(move, player)
            test_rules = GameRules(test_board)
            
            score = self._minimax(
                test_board,
                test_rules,
                self.search_depth - 1,
                alpha,
                beta,
                False,
                player
            )
            
            if score > best_score:
                best_score = score
                best_move = move
            
            if self.use_alpha_beta:
                alpha = max(alpha, best_score)
        
        end_time = time.time()
        
        stats = {
            'nodes_explored': self.nodes_explored,
            'pruned_nodes': self.pruned_nodes,
            'time_elapsed': end_time - start_time,
            'depth': self.search_depth,
            'heuristic': self.heuristic if self.use_heuristic else 'none',
            'alpha_beta': self.use_alpha_beta,
            'symmetry_reduction': self.use_symmetry_reduction,
            'heuristic_reduction': self.use_heuristic_reduction
        }
        
        if self.verbose:
            print(f"Minimax Search Complete:")
            print(f"  Nodes explored: {self.nodes_explored:,}")
            if self.use_alpha_beta:
                print(f"  Pruned nodes: {self.pruned_nodes:,}")
            print(f"  Time: {stats['time_elapsed']:.3f}s")
            print(f"  Best score: {best_score:.2f}")
            print(f"  Heuristic: {stats['heuristic']}")
            print(f"  Alpha-Beta: {self.use_alpha_beta}")
        
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
        self.nodes_explored += 1
        
        if self.use_transposition_table:
            board_key = self._board_hash(board)
            if board_key in self.transposition_table:
                cached_score, cached_depth = self.transposition_table[board_key]
                if cached_depth >= depth:
                    return cached_score
        
        winner = rules.check_winner()
        if winner is not None:
            if winner == original_player:
                score = 10000.0
            else:
                score = -10000.0
        elif board.is_full():
            score = 0.0
        elif depth == 0:
            if self.use_heuristic and self.evaluator:
                score = self.evaluator.evaluate(board, rules, original_player)
            else:
                score = 0.0
        else:
            legal_moves = self._get_reduced_moves(board, original_player if maximizing else (Board.PLAYER_O if original_player == Board.PLAYER_X else Board.PLAYER_X))
            
            if maximizing:
                max_eval = float('-inf')
                current_player = original_player
                
                for move in legal_moves:
                    test_board = board.copy()
                    test_board.set_position(move, current_player)
                    test_rules = GameRules(test_board)
                    
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
                    
                    if self.use_alpha_beta:
                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            self.pruned_nodes += len(legal_moves) - legal_moves.index(move) - 1
                            break
                
                score = max_eval
            else:
                min_eval = float('inf')
                opponent = Board.PLAYER_O if original_player == Board.PLAYER_X else Board.PLAYER_X
                
                for move in legal_moves:
                    test_board = board.copy()
                    test_board.set_position(move, opponent)
                    test_rules = GameRules(test_board)
                    
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
                    
                    if self.use_alpha_beta:
                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            self.pruned_nodes += len(legal_moves) - legal_moves.index(move) - 1
                            break
                
                score = min_eval
        
        if self.use_transposition_table:
            board_key = self._board_hash(board)
            self.transposition_table[board_key] = (score, depth)
        
        return score
    
    def _board_hash(self, board: Board) -> str:
        return ''.join(str(p) for p in board.board)
    
    def _get_reduced_moves(self, board: Board, player: int) -> List[int]:
        legal_moves = board.get_legal_moves()
        
        if not legal_moves:
            return []
        
        if self.use_symmetry_reduction:
            legal_moves = self._apply_symmetry_reduction(board, legal_moves)
        
        if self.use_heuristic_reduction and self.use_heuristic and self.evaluator:
            legal_moves = self._apply_heuristic_reduction(board, legal_moves, player)
        
        return legal_moves
    
    def _apply_symmetry_reduction(self, board: Board, moves: List[int]) -> List[int]:
        if not moves:
            return []
        
        canonical_board = self._get_canonical_board(board)
        board_key = self._board_hash(canonical_board)
        
        if board_key in self.symmetry_cache:
            cached_reps = self.symmetry_cache[board_key]
            return [m for m in moves if m in cached_reps]
        
        representatives = []
        processed = set()
        
        for move in moves:
            if move in processed:
                continue
            
            symmetric_moves = self._get_symmetric_positions(move)
            
            for sym_move in symmetric_moves:
                if sym_move in moves and sym_move not in processed:
                    representatives.append(sym_move)
                    processed.update(symmetric_moves)
                    break
        
        self.symmetry_cache[board_key] = representatives
        
        return representatives
    
    def _get_symmetric_positions(self, flat_index: int) -> List[int]:
        layer, row, col = Board._to_coordinates(flat_index)
        symmetric = set()
        
        symmetric.add(flat_index)
        
        for rot in range(1, 4):
            new_row, new_col = self._rotate_2d(row, col, rot)
            symmetric.add(Board._to_flat_index(layer, new_row, new_col))
        
        for rot in range(1, 4):
            new_layer, new_row = self._rotate_2d(layer, row, rot)
            symmetric.add(Board._to_flat_index(new_layer, new_row, col))
        
        for rot in range(1, 4):
            new_layer, new_col = self._rotate_2d(layer, col, rot)
            symmetric.add(Board._to_flat_index(new_layer, row, new_col))
        
        symmetric.add(Board._to_flat_index(layer, row, 3 - col))
        symmetric.add(Board._to_flat_index(layer, 3 - row, col))
        symmetric.add(Board._to_flat_index(3 - layer, row, col))
        
        return list(symmetric)
    
    def _rotate_2d(self, x: int, y: int, rotations: int) -> Tuple[int, int]:
        for _ in range(rotations % 4):
            x, y = y, 3 - x
        return x, y
    
    def _get_canonical_board(self, board: Board) -> Board:
        return board
    
    def _apply_heuristic_reduction(self, board: Board, moves: List[int], player: int) -> List[int]:
        if not moves or not self.evaluator:
            return moves
        
        move_scores = []
        rules = GameRules(board)
        
        for move in moves:
            test_board = board.copy()
            test_board.set_position(move, player)
            test_rules = GameRules(test_board)
            score = self.evaluator.evaluate(test_board, test_rules, player)
            move_scores.append((score, move))
        
        move_scores.sort(reverse=True, key=lambda x: x[0])
        keep_count = max(5, len(moves) // 2)
        
        return [move for _, move in move_scores[:keep_count]]