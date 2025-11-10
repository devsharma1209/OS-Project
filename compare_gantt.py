import matplotlib.pyplot as plt

def compare_gantt(all_results):
    """Display multiple Gantt charts side-by-side."""
    fig, axes = plt.subplots(len(all_results), 1, figsize=(12, 3 * len(all_results)))

    for ax, (name, results) in zip(axes, all_results.items()):
        for r in results:
            ax.barh(f"P{r['pid']}", r['finish'] - r['start'],
                    left=r['start'], edgecolor='black', height=0.4)
        ax.set_title(name, fontsize=12, fontweight='bold')
        ax.grid(True, axis='x', linestyle='--', alpha=0.6)
        ax.set_xlabel("Time")
        ax.set_ylabel("Process")

    plt.tight_layout()
    plt.show()
