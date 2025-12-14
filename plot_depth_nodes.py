import matplotlib.pyplot as plt
from cubic.board import Board
from cubic.rules import GameRules
from cubic.minimax import Minimax

depths = [1, 2, 3, 4]
nodes = []

for d in depths:
    board = Board()
    rules = GameRules(board)
    minimax = Minimax(search_depth=d, verbose=False)
    
    _, _, stats = minimax.get_best_move(
        board,
        rules,
        Board.PLAYER_X
    )
    
    nodes.append(stats['nodes_explored'])

plt.figure()
plt.plot(depths, nodes, marker='o')
plt.xlabel("Search Depth")
plt.ylabel("Nodes Explored")
plt.title("Search Depth vs Nodes Explored (Minimax with Alpha-Beta)")
plt.grid(True)
plt.show()
