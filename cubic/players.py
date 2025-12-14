from cubic.board import Board


class HumanPlayer:
    def __init__(self, player_id: int):
        self.player_id = player_id
        self.name = "Human"
    
    def __repr__(self):
        symbol = "X" if self.player_id == Board.PLAYER_X else "O"
        return f"HumanPlayer({symbol})"


class AIPlayer:
    def __init__(self, player_id: int, depth: int = 4):
        self.player_id = player_id
        self.depth = depth
        self.name = f"AI (Depth {depth})"
    
    def __repr__(self):
        symbol = "X" if self.player_id == Board.PLAYER_X else "O"
        return f"AIPlayer({symbol}, depth={self.depth})"


class RandomPlayer:
    def __init__(self, player_id: int):
        self.player_id = player_id
        self.name = "Random"
    
    def __repr__(self):
        symbol = "X" if self.player_id == Board.PLAYER_X else "O"
        return f"RandomPlayer({symbol})"