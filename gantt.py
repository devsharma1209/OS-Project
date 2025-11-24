import matplotlib.pyplot as plt
import os

def plot_gantt_grid(results_dict, filename="comparison.png"):
    plt.switch_backend('Agg') 
    
    n = len(results_dict)
    fig, axes = plt.subplots(n, 1, figsize=(12, 2.5 * n), constrained_layout=True)
    if n == 1: axes = [axes]
    
    colors = plt.cm.tab10.colors
    
    for ax, (name, timeline) in zip(axes, results_dict.items()):
        ax.set_title(name, fontsize=12, fontweight='bold', loc='left')
        
        y_pos = 10
        height = 8
        
        for slice in timeline:
            pid = slice['pid']
            start = slice['start']
            finish = slice['finish']
            duration = finish - start
            
            if pid == -1:
                # IDLE BLOCK (Grey with hashes)
                ax.broken_barh([(start, duration)], (y_pos, height), 
                               facecolors='#f0f0f0', hatch='///', edgecolor='gray', linewidth=0.5)
                # Only label if wide enough
                if duration > 1:
                    ax.text(start + duration/2, y_pos + height/2, "IDLE", 
                            ha='center', va='center', fontsize=8, color='gray', rotation=90)
            else:
                # PROCESS BLOCK
                color = colors[(pid - 1) % 10] 
                ax.broken_barh([(start, duration)], (y_pos, height), facecolors=color, edgecolor='black', linewidth=0.5)
                
                if duration > 0.5:
                    ax.text(start + duration/2, y_pos + height/2, f"P{pid}", 
                            ha='center', va='center', fontsize=9, color='white', fontweight='bold')

        ax.set_yticks([]) 
        ax.set_xlabel("Time Units")
        ax.grid(True, axis='x', linestyle='--', alpha=0.5)
        
        # Set dynamic x-limit
        max_time = max([t['finish'] for t in timeline]) if timeline else 10
        ax.set_xlim(0, max_time + 1)

    if not os.path.exists("results"): os.makedirs("results")
    output_path = os.path.join("results", filename)
    plt.savefig(output_path, dpi=150)
    print(f"📊 Gantt Chart saved to: {output_path}")
    plt.close()
