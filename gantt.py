import matplotlib.pyplot as plt
import os

def plot_gantt_grid(results_dict, filename="comparison.png"):
    plt.switch_backend('Agg') # Headless mode for safety
    
    n = len(results_dict)
    fig, axes = plt.subplots(n, 1, figsize=(12, 2.5 * n), constrained_layout=True)
    if n == 1: axes = [axes]
    
    # Standard Tab10 colors
    colors = plt.cm.tab10.colors
    
    for ax, (name, timeline) in zip(axes, results_dict.items()):
        ax.set_title(name, fontsize=12, fontweight='bold', loc='left')
        
        # Collect all PIDs to determine unique processes
        pids = sorted(list(set(t['pid'] for t in timeline)))
        
        # Y-Axis configuration (Single Row style)
        y_pos = 10
        height = 8
        
        for slice in timeline:
            pid = slice['pid']
            start = slice['start']
            duration = slice['finish'] - start
            
            # Color based on PID
            color = colors[(pid - 1) % 10] 
            
            ax.broken_barh([(start, duration)], (y_pos, height), facecolors=color, edgecolor='black', linewidth=0.5)
            
            # Label inside the bar
            if duration > 0.5: # Only label if wide enough
                ax.text(start + duration/2, y_pos + height/2, f"P{pid}", 
                        ha='center', va='center', fontsize=9, color='white', fontweight='bold')

        ax.set_yticks([]) # Hide Y axis numbers
        ax.set_xlim(0, max(t['finish'] for t in timeline) + 2)
        ax.set_xlabel("Time Units")
        ax.grid(True, axis='x', linestyle='--', alpha=0.5)

    # Save
    if not os.path.exists("results"): os.makedirs("results")
    output_path = os.path.join("results", filename)
    plt.savefig(output_path, dpi=150)
    print(f"📊 Gantt Chart saved to: {output_path}")
    plt.close()