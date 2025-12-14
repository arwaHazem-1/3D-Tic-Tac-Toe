__version__ = "1.0.0"
__author__ = "Your Name"

from cubic.board import Board
from cubic.rules import GameRules
from cubic.players import HumanPlayer, AIPlayer, RandomPlayer
from cubic.minimax import Minimax
from cubic.heuristics import HeuristicEvaluator

__all__ = [
    'Board',
    'GameRules',
    'HumanPlayer',
    'AIPlayer',
    'RandomPlayer',
    'Minimax',
    'HeuristicEvaluator',
]

