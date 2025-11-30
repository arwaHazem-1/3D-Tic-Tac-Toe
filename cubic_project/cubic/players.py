"""
Player classes for Cubic game.
"""

from cubic.board import Board


class HumanPlayer:
    """Represents a human player."""
    
    def __init__(self, player_id: int):
        """
        Initialize human player.
        
        Args:
            player_id: PLAYER_X or PLAYER_O
        """
        self.player_id = player_id
        self.name = "Human"
    
    def __repr__(self):
        symbol = "X" if self.player_id == Board.PLAYER_X else "O"
        return f"HumanPlayer({symbol})"


class AIPlayer:
    """Represents an AI player."""
    
    def __init__(self, player_id: int, depth: int = 4):
        """
        Initialize AI player.
        
        Args:
            player_id: PLAYER_X or PLAYER_O
            depth: Search depth for minimax
        """
        self.player_id = player_id
        self.depth = depth
        self.name = f"AI (Depth {depth})"
    
    def __repr__(self):
        symbol = "X" if self.player_id == Board.PLAYER_X else "O"
        return f"AIPlayer({symbol}, depth={self.depth})"


class RandomPlayer:
    """Represents a random player (for testing)."""
    
    def __init__(self, player_id: int):
        """
        Initialize random player.
        
        Args:
            player_id: PLAYER_X or PLAYER_O
        """
        self.player_id = player_id
        self.name = "Random"
    
    def __repr__(self):
        symbol = "X" if self.player_id == Board.PLAYER_X else "O"
        return f"RandomPlayer({symbol})"