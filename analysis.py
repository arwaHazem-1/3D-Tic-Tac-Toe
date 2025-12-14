import time
from cubic.board import Board
from cubic.rules import GameRules
from cubic.minimax import Minimax


def test_configuration(name: str, heuristic: str = None, use_alpha_beta: bool = True,
                      use_symmetry: bool = False, use_heuristic_red: bool = False,
                      depth: int = 3, test_positions: int = 5):
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    
    config = Minimax(
        search_depth=depth,
        heuristic=heuristic,
        use_alpha_beta=use_alpha_beta,
        use_symmetry_reduction=use_symmetry,
        use_heuristic_reduction=use_heuristic_red,
        verbose=False
    )
    
    total_nodes = 0
    total_pruned = 0
    total_time = 0
    total_moves = 0
    
    for i in range(test_positions):
        board = Board()
        rules = GameRules(board)
        
        import random
        moves_made = random.randint(5, 15)
        current_player = Board.PLAYER_X
        
        for _ in range(moves_made):
            legal_moves = board.get_legal_moves()
            if not legal_moves:
                break
            move = random.choice(legal_moves)
            board.set_position(move, current_player)
            current_player = Board.PLAYER_O if current_player == Board.PLAYER_X else Board.PLAYER_X
        
        rules = GameRules(board)
        
        start_time = time.time()
        move, score, stats = config.get_best_move(
            board.copy(),
            rules,
            Board.PLAYER_O
        )
        elapsed = time.time() - start_time
        
        total_nodes += stats.get('nodes_explored', 0)
        total_pruned += stats.get('pruned_nodes', 0)
        total_time += elapsed
        total_moves += 1
        
        print(f"  Position {i+1}: {stats.get('nodes_explored', 0):,} nodes, "
              f"{stats.get('pruned_nodes', 0):,} pruned, {elapsed:.2f}s")
    
    avg_nodes = total_nodes / total_moves if total_moves > 0 else 0
    avg_pruned = total_pruned / total_moves if total_moves > 0 else 0
    avg_time = total_time / total_moves if total_moves > 0 else 0
    pruning_ratio = (avg_pruned / (avg_nodes + avg_pruned) * 100) if (avg_nodes + avg_pruned) > 0 else 0
    
    results = {
        'name': name,
        'avg_nodes': avg_nodes,
        'avg_pruned': avg_pruned,
        'avg_time': avg_time,
        'pruning_ratio': pruning_ratio,
        'heuristic': heuristic or 'none',
        'alpha_beta': use_alpha_beta,
        'symmetry': use_symmetry,
        'heuristic_red': use_heuristic_red
    }
    
    print(f"\n  Average Nodes: {avg_nodes:,.0f}")
    print(f"  Average Pruned: {avg_pruned:,.0f}")
    print(f"  Pruning Ratio: {pruning_ratio:.1f}%")
    print(f"  Average Time: {avg_time:.2f}s")
    
    return results


def main():
    print("\n" + "="*60)
    print("3D Tic-Tac-Toe Algorithm Performance Analysis")
    print("="*60)
    
    results = []
    
    configs = [
        ("Minimax (No Heuristic)", None, False, False, False, 2),
        ("Minimax + Simple Heuristic", 'simple', False, False, False, 3),
        ("Minimax + Advanced Heuristic", 'advanced', False, False, False, 3),
        ("Minimax + Simple + Alpha-Beta", 'simple', True, False, False, 3),
        ("Minimax + Advanced + Alpha-Beta", 'advanced', True, False, False, 3),
        ("Minimax + Advanced + Alpha-Beta + Symmetry", 'advanced', True, True, False, 3),
        ("Minimax + Advanced + Alpha-Beta + Heuristic Red", 'advanced', True, False, True, 3),
        ("Minimax + Advanced + Alpha-Beta + All Optimizations", 'advanced', True, True, True, 3),
    ]
    
    for config in configs:
        result = test_configuration(*config, test_positions=3)
        results.append(result)
        time.sleep(0.5)
    
    print("\n" + "="*60)
    print("PERFORMANCE COMPARISON SUMMARY")
    print("="*60)
    print(f"{'Configuration':<50} {'Nodes':<12} {'Time':<8} {'Pruning':<10}")
    print("-"*60)
    
    for r in results:
        print(f"{r['name']:<50} {r['avg_nodes']:>10,.0f} {r['avg_time']:>6.2f}s "
              f"{r['pruning_ratio']:>8.1f}%")
    
    print("\n" + "="*60)
    print("BEST CONFIGURATIONS")
    print("="*60)
    
    fastest = min(results, key=lambda x: x['avg_time'])
    most_efficient = min(results, key=lambda x: x['avg_nodes'])
    best_pruning = max([r for r in results if r['alpha_beta']], 
                       key=lambda x: x['pruning_ratio'])
    
    print(f"Fastest: {fastest['name']} ({fastest['avg_time']:.2f}s)")
    print(f"Most Efficient (Fewest Nodes): {most_efficient['name']} "
          f"({most_efficient['avg_nodes']:,.0f} nodes)")
    print(f"Best Pruning: {best_pruning['name']} ({best_pruning['pruning_ratio']:.1f}%)")
    
    print("\n" + "="*60)
    print("HEURISTIC COMPARISON")
    print("="*60)
    
    simple_results = [r for r in results if r['heuristic'] == 'simple' and r['alpha_beta']]
    advanced_results = [r for r in results if r['heuristic'] == 'advanced' and r['alpha_beta']]
    
    if simple_results and advanced_results:
        simple = simple_results[0]
        advanced = advanced_results[0]
        
        print(f"Simple Heuristic:")
        print(f"  Nodes: {simple['avg_nodes']:,.0f}, Time: {simple['avg_time']:.2f}s")
        print(f"Advanced Heuristic:")
        print(f"  Nodes: {advanced['avg_nodes']:,.0f}, Time: {advanced['avg_time']:.2f}s")
        
        time_diff = ((advanced['avg_time'] - simple['avg_time']) / simple['avg_time']) * 100
        print(f"\nAdvanced is {abs(time_diff):.1f}% {'slower' if time_diff > 0 else 'faster'} "
              f"than Simple")
    
    print("\n" + "="*60)
    print("Analysis Complete!")
    print("="*60)


if __name__ == "__main__":
    main()

