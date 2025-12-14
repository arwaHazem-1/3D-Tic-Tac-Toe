#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

try:
    if 'seaborn-v0_8-darkgrid' in plt.style.available:
        plt.style.use('seaborn-v0_8-darkgrid')
    elif 'seaborn-darkgrid' in plt.style.available:
        plt.style.use('seaborn-darkgrid')
    else:
        plt.style.use('default')
except:
    plt.style.use('default')

plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


def generate_state_space_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(-1, 15)
    ax.set_ylim(-1, 5)
    ax.axis('off')
    ax.set_title('State Space Tree Diagram\n(First 3 Levels of Game Tree)', 
                 fontsize=16, fontweight='bold', pad=20)
    
    ax.text(7, 4.5, 'Initial State\n(Empty Board)', 
            ha='center', va='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', edgecolor='black', linewidth=2))
    
    positions = [3, 7, 11]
    for i, pos in enumerate(positions):
        ax.annotate('', xy=(pos, 3.2), xytext=(7, 4.2),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        
        ax.text(pos, 3, 'State S{}\nMove: Pos {}'.format(i+1, i*20), 
                ha='center', va='center', fontsize=10,
                bbox=dict(boxstyle='round,pad=0.4', facecolor='lightgreen', edgecolor='black'))
    
    level2_positions = [
        [1.5, 4.5],
        [6.5, 8.5],
        [10.5, 13.5]
    ]
    
    for parent_idx, (pos1, pos2) in enumerate(level2_positions):
        parent_x = positions[parent_idx]
        ax.annotate('', xy=(pos1, 1.7), xytext=(parent_x, 2.8),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='gray'))
        ax.annotate('', xy=(pos2, 1.7), xytext=(parent_x, 2.8),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='gray'))
        
        ax.text(pos1, 1.5, 'S{}1'.format(parent_idx+1), 
                ha='center', va='center', fontsize=9,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', edgecolor='black'))
        ax.text(pos2, 1.5, 'S{}2'.format(parent_idx+1), 
                ha='center', va='center', fontsize=9,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', edgecolor='black'))
    
    ax.text(7, 0.5, '... (exponential growth continues)', 
            ha='center', va='center', fontsize=11, style='italic',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='orange', linewidth=2))
    
    ax.text(7, -0.5, 'Note: Full state space has 3^64 ≈ 3.43 × 10^30 possible states\n' +
            'With 64 initial moves, branching factor is very high',
            ha='center', va='top', fontsize=9, style='italic', color='darkred')
    
    plt.tight_layout()
    plt.savefig('diagrams/state_space_diagram.png', dpi=300, bbox_inches='tight')
    print("✅ Generated: diagrams/state_space_diagram.png")
    plt.close()


def generate_board_visualization():
    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.set_title('4×4×4 Cubic Board Structure\n(64 Positions Total)', 
                 fontsize=16, fontweight='bold', pad=20)
    
    colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral']
    layer_names = ['Layer 0', 'Layer 1', 'Layer 2', 'Layer 3']
    
    for layer in range(4):
        for row in range(4):
            for col in range(4):
                x = col
                y = row
                z = layer
                
                ax.plot([x, x+1, x+1, x, x], [y, y, y+1, y+1, y], 
                       [z, z, z, z, z], color='black', linewidth=0.5, alpha=0.3)
                ax.plot([x, x+1, x+1, x, x], [y, y, y+1, y+1, y], 
                       [z+1, z+1, z+1, z+1, z+1], color='black', linewidth=0.5, alpha=0.3)
                ax.plot([x, x], [y, y], [z, z+1], color='black', linewidth=0.3, alpha=0.2)
                ax.plot([x+1, x+1], [y, y], [z, z+1], color='black', linewidth=0.3, alpha=0.2)
                ax.plot([x, x], [y+1, y+1], [z, z+1], color='black', linewidth=0.3, alpha=0.2)
                ax.plot([x+1, x+1], [y+1, y+1], [z, z+1], color='black', linewidth=0.3, alpha=0.2)
                
                if row == 0 and col == 0:
                    ax.scatter([x+0.5], [y+0.5], [z+0.5], 
                             c=colors[layer], s=100, alpha=0.6, edgecolors='black', linewidths=1)
    
    for layer in range(4):
        ax.text(-0.5, -0.5, layer + 0.5, layer_names[layer], 
               fontsize=11, fontweight='bold', color=colors[layer])
    
    ax.set_xlabel('Column (X-axis)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Row (Y-axis)', fontsize=12, fontweight='bold')
    ax.set_zlabel('Layer (Z-axis)', fontsize=12, fontweight='bold')
    
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.5, 4.5)
    ax.set_zlim(-0.5, 4.5)
    
    ax.text(4.2, 0, 0, 'X', fontsize=14, fontweight='bold', color='red')
    ax.text(0, 4.2, 0, 'Y', fontsize=14, fontweight='bold', color='green')
    ax.text(0, 0, 4.2, 'Z', fontsize=14, fontweight='bold', color='blue')
    
    ax.text2D(0.02, 0.98, 'Total Positions: 64 (4×4×4)\n' +
              'Coordinate System: (Layer, Row, Col)\n' +
              'Flat Index = Layer×16 + Row×4 + Col',
              transform=ax.transAxes, fontsize=10, verticalalignment='top',
              bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('diagrams/board_structure.png', dpi=300, bbox_inches='tight')
    print("✅ Generated: diagrams/board_structure.png")
    plt.close()


def generate_winning_lines_diagram():
    fig = plt.figure(figsize=(16, 12))
    
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    ax2 = fig.add_subplot(2, 2, 2, projection='3d')
    ax3 = fig.add_subplot(2, 2, 3, projection='3d')
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    
    axes = [ax1, ax2, ax3, ax4]
    titles = [
        'X-Axis Lines (16 lines)\nFixed Layer & Row, Varying Column',
        'Y-Axis Lines (16 lines)\nFixed Layer & Column, Varying Row',
        'Z-Axis Lines (16 lines)\nFixed Row & Column, Varying Layer',
        'Space Diagonals (4 lines)\nThrough the 3D Cube'
    ]
    
    for ax in axes:
        for layer in range(4):
            for row in range(4):
                for col in range(4):
                    x, y, z = col, row, layer
                    ax.plot([x, x+1, x+1, x, x], [y, y, y+1, y+1, y], 
                           [z, z, z, z, z], color='gray', linewidth=0.3, alpha=0.2)
    
    ax1.set_title(titles[0], fontsize=11, fontweight='bold')
    for col in range(4):
        ax1.scatter([col+0.5], [0.5], [0.5], c='red', s=200, marker='o', 
                   edgecolors='black', linewidths=2, zorder=5)
    ax1.plot([0.5, 1.5, 2.5, 3.5], [0.5, 0.5, 0.5, 0.5], 
            [0.5, 0.5, 0.5, 0.5], 'r-', linewidth=4, alpha=0.7, zorder=4)
    ax1.set_xlabel('Column')
    ax1.set_ylabel('Row')
    ax1.set_zlabel('Layer')
    ax1.set_xlim(-0.5, 4.5)
    ax1.set_ylim(-0.5, 4.5)
    ax1.set_zlim(-0.5, 4.5)
    
    ax2.set_title(titles[1], fontsize=11, fontweight='bold')
    for row in range(4):
        ax2.scatter([0.5], [row+0.5], [0.5], c='green', s=200, marker='o', 
                   edgecolors='black', linewidths=2, zorder=5)
    ax2.plot([0.5, 0.5, 0.5, 0.5], [0.5, 1.5, 2.5, 3.5], 
            [0.5, 0.5, 0.5, 0.5], 'g-', linewidth=4, alpha=0.7, zorder=4)
    ax2.set_xlabel('Column')
    ax2.set_ylabel('Row')
    ax2.set_zlabel('Layer')
    ax2.set_xlim(-0.5, 4.5)
    ax2.set_ylim(-0.5, 4.5)
    ax2.set_zlim(-0.5, 4.5)
    
    ax3.set_title(titles[2], fontsize=11, fontweight='bold')
    for layer in range(4):
        ax3.scatter([0.5], [0.5], [layer+0.5], c='blue', s=200, marker='o', 
                   edgecolors='black', linewidths=2, zorder=5)
    ax3.plot([0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5], 
            [0.5, 1.5, 2.5, 3.5], 'b-', linewidth=4, alpha=0.7, zorder=4)
    ax3.set_xlabel('Column')
    ax3.set_ylabel('Row')
    ax3.set_zlabel('Layer')
    ax3.set_xlim(-0.5, 4.5)
    ax3.set_ylim(-0.5, 4.5)
    ax3.set_zlim(-0.5, 4.5)
    
    ax4.set_title(titles[3], fontsize=11, fontweight='bold')
    for i in range(4):
        ax4.scatter([i+0.5], [i+0.5], [i+0.5], c='purple', s=200, marker='o', 
                   edgecolors='black', linewidths=2, zorder=5)
    ax4.plot([0.5, 1.5, 2.5, 3.5], [0.5, 1.5, 2.5, 3.5], 
            [0.5, 1.5, 2.5, 3.5], 'purple', linewidth=4, alpha=0.7, zorder=4)
    ax4.set_xlabel('Column')
    ax4.set_ylabel('Row')
    ax4.set_zlabel('Layer')
    ax4.set_xlim(-0.5, 4.5)
    ax4.set_ylim(-0.5, 4.5)
    ax4.set_zlim(-0.5, 4.5)
    
    fig.suptitle('Winning Lines Visualization\n(76 Total Winning Lines)', 
                fontsize=16, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('diagrams/winning_lines.png', dpi=300, bbox_inches='tight')
    print("✅ Generated: diagrams/winning_lines.png")
    plt.close()


def generate_minimax_flow_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 9)
    ax.axis('off')
    ax.set_title('Minimax Algorithm Flow with Alpha-Beta Pruning', 
                 fontsize=16, fontweight='bold', pad=20)
    
    start_box = FancyBboxPatch((4.5, 8), 2, 0.8, boxstyle='round,pad=0.1', 
                               facecolor='lightgreen', edgecolor='black', linewidth=2)
    ax.add_patch(start_box)
    ax.text(5.5, 8.4, 'Start: Current\nBoard State', ha='center', va='center', 
           fontsize=11, fontweight='bold')
    
    moves_box = FancyBboxPatch((4, 6.5), 3, 0.8, boxstyle='round,pad=0.1', 
                              facecolor='lightblue', edgecolor='black', linewidth=2)
    ax.add_patch(moves_box)
    ax.text(5.5, 6.9, 'Get Legal Moves', ha='center', va='center', 
           fontsize=11, fontweight='bold')
    
    ax.annotate('', xy=(5.5, 6.5), xytext=(5.5, 8),
               arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    
    for_box = FancyBboxPatch((3.5, 5), 4, 0.8, boxstyle='round,pad=0.1', 
                            facecolor='wheat', edgecolor='black', linewidth=2)
    ax.add_patch(for_box)
    ax.text(5.5, 5.4, 'For Each Move', ha='center', va='center', 
           fontsize=11, fontweight='bold')
    
    ax.annotate('', xy=(5.5, 5), xytext=(5.5, 6.5),
               arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    
    make_box = FancyBboxPatch((4, 3.5), 3, 0.8, boxstyle='round,pad=0.1', 
                             facecolor='lightyellow', edgecolor='black', linewidth=2)
    ax.add_patch(make_box)
    ax.text(5.5, 3.9, 'Make Move', ha='center', va='center', 
           fontsize=11, fontweight='bold')
    
    ax.annotate('', xy=(5.5, 3.5), xytext=(5.5, 5),
               arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    
    terminal_box = FancyBboxPatch((3, 2), 5, 0.8, boxstyle='round,pad=0.1', 
                                 facecolor='lightcoral', edgecolor='black', linewidth=2)
    ax.add_patch(terminal_box)
    ax.text(5.5, 2.4, 'Terminal State?', ha='center', va='center', 
           fontsize=11, fontweight='bold')
    
    ax.annotate('', xy=(5.5, 2), xytext=(5.5, 3.5),
               arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    
    yes_box = FancyBboxPatch((0.5, 0.5), 2.5, 0.8, boxstyle='round,pad=0.1', 
                            facecolor='lightgreen', edgecolor='black', linewidth=2)
    ax.add_patch(yes_box)
    ax.text(1.75, 0.9, 'Yes:\nReturn Score', ha='center', va='center', 
           fontsize=10, fontweight='bold')
    
    ax.annotate('', xy=(1.75, 1.3), xytext=(4, 2.4),
               arrowprops=dict(arrowstyle='->', lw=2, color='green'))
    ax.text(2.5, 1.8, 'Yes', ha='center', fontsize=9, color='green', fontweight='bold')
    
    depth_box = FancyBboxPatch((7.5, 0.5), 2.5, 0.8, boxstyle='round,pad=0.1', 
                              facecolor='lightblue', edgecolor='black', linewidth=2)
    ax.add_patch(depth_box)
    ax.text(8.75, 0.9, 'No:\nDepth = 0?', ha='center', va='center', 
           fontsize=10, fontweight='bold')
    
    ax.annotate('', xy=(8.75, 1.3), xytext=(7, 2.4),
               arrowprops=dict(arrowstyle='->', lw=2, color='red'))
    ax.text(7.8, 1.8, 'No', ha='center', fontsize=9, color='red', fontweight='bold')
    
    heuristic_box = FancyBboxPatch((7, -0.5), 3.5, 0.8, boxstyle='round,pad=0.1', 
                                  facecolor='plum', edgecolor='black', linewidth=2)
    ax.add_patch(heuristic_box)
    ax.text(8.75, -0.1, 'Yes: Use Heuristic', ha='center', va='center', 
           fontsize=10, fontweight='bold')
    
    ax.annotate('', xy=(8.75, 0.5), xytext=(8.75, 0.5),
               arrowprops=dict(arrowstyle='->', lw=2, color='purple'))
    
    recursive_box = FancyBboxPatch((0.5, -0.5), 3.5, 0.8, boxstyle='round,pad=0.1', 
                                  facecolor='orange', edgecolor='black', linewidth=2)
    ax.add_patch(recursive_box)
    ax.text(2.25, -0.1, 'No: Recursive Call', ha='center', va='center', 
           fontsize=10, fontweight='bold')
    
    ax.annotate('', xy=(2.25, 0.5), xytext=(4.5, 2.4),
               arrowprops=dict(arrowstyle='->', lw=2, color='orange', linestyle='--'))
    
    ax.text(5.5, -1.5, 'Alpha-Beta Pruning: If α ≥ β, prune remaining branches', 
           ha='center', fontsize=10, style='italic', color='darkblue',
           bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='darkblue', linewidth=2))
    
    plt.tight_layout()
    plt.savefig('diagrams/minimax_flow.png', dpi=300, bbox_inches='tight')
    print("✅ Generated: diagrams/minimax_flow.png")
    plt.close()


def main():
    import os
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    diagrams_dir = os.path.join(script_dir, 'diagrams')
    
    os.makedirs(diagrams_dir, exist_ok=True)
    
    print("Generating visual diagrams for the project report...")
    print(f"Working directory: {script_dir}")
    print(f"Diagrams will be saved to: {diagrams_dir}\n")
    
    try:
        original_cwd = os.getcwd()
        os.chdir(script_dir)
        
        try:
            generate_state_space_diagram()
            generate_board_visualization()
            generate_winning_lines_diagram()
            generate_minimax_flow_diagram()
        finally:
            os.chdir(original_cwd)
        
        print("\n" + "="*60)
        print("✅ All diagrams generated successfully!")
        print("="*60)
        print("\nGenerated files (absolute paths):")
        files = [
            'state_space_diagram.png',
            'board_structure.png',
            'winning_lines.png',
            'minimax_flow.png'
        ]
        for filename in files:
            filepath = os.path.join(diagrams_dir, filename)
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                print(f"  ✅ {filepath} ({size:,} bytes)")
            else:
                print(f"  ❌ {filepath} (NOT FOUND)")
        print("\nYou can now include these PNG files in your REPORT.md")
        print("or reference them in your report document.")
        
    except Exception as e:
        print("\n❌ Error generating diagrams: {}".format(e))
        import traceback
        traceback.print_exc()
        print("\nMake sure matplotlib is installed: pip install matplotlib")
        raise


if __name__ == "__main__":
    main()
