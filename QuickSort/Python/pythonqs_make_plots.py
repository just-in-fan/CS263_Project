# pythonqs_make_plots.py
import pandas as pd
import matplotlib.pyplot as plt

# 1) Load the CSV
df = pd.read_csv("python_bench_results.csv")

# 2) Choose one distribution to plot
distributions = ["random", "sorted", "reversed", "nearly_sorted", "few_values"]

for distribution in distributions:
    df_sub = df[df["distribution"] == distribution]
    
    # 3) Make a line for each algorithm
    plt.figure(figsize=(10, 6))
    
    # Define colors for algorithms
    colors = ['blue', 'orange', 'green', 'red']
    markers = ['o', 's', '^', 'D']
    
    for i, (algo, group) in enumerate(df_sub.groupby("algorithm")):
        group_sorted = group.sort_values("n")
        color = colors[i % len(colors)]
        marker = markers[i % len(markers)]
        
        plt.plot(group_sorted["n"], group_sorted["median_sec"], 
                marker=marker, label=algo, linewidth=2.5, markersize=8,
                color=color)
    
    plt.xlabel("Array Size (n)", fontsize=12)
    plt.ylabel("Median Runtime (seconds)", fontsize=12)
    plt.title(f"Sorting Algorithm Runtime vs Array Size (distribution={distribution})", fontsize=14, pad=15)
    plt.legend(title="Algorithm", fontsize=10, title_fontsize=11)
    plt.grid(True, alpha=0.3)
    
    # Use logarithmic scale for y-axis since times vary greatly
    plt.yscale("log")
    
    # Format y-axis to show scientific notation clearly
    from matplotlib.ticker import ScalarFormatter
    plt.gca().yaxis.set_major_formatter(ScalarFormatter())
    plt.gca().yaxis.set_minor_formatter(ScalarFormatter())
    
    plt.tight_layout()
    # Save with distribution name in filename
    plt.savefig(f"sorting_runtime_{distribution}.png", dpi=300, bbox_inches="tight")
    plt.close()

print("Plots saved as 'sorting_runtime_<distribution>.png'")

# 4) Bonus: Create a single comparison figure with subplots
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

# Remove the last subplot if we have 5 distributions (2x3 grid)
if len(distributions) < 6:
    fig.delaxes(axes[5])

# Define algorithm colors for consistency across plots
algorithms = df["algorithm"].unique()
color_map = {
    'chatgpt': 'blue',
    'claude': 'orange', 
    'deepseek': 'green',
    'gemini': 'red'
}

for idx, distribution in enumerate(distributions):
    ax = axes[idx]
    df_sub = df[df["distribution"] == distribution]
    
    for algo, group in df_sub.groupby("algorithm"):
        group_sorted = group.sort_values("n")
        ax.plot(group_sorted["n"], group_sorted["median_sec"], 
                marker="o", label=algo, linewidth=2, markersize=6,
                color=color_map.get(algo, 'black'))
    
    ax.set_xlabel("Array Size (n)", fontsize=10)
    ax.set_ylabel("Median Runtime (s)", fontsize=10)
    ax.set_title(f"Distribution: {distribution}", fontsize=12, pad=10)
    ax.grid(True, alpha=0.3)
    ax.set_yscale("log")
    
    # Add legend to first subplot only
    if idx == 0:
        ax.legend(title="Algorithm", fontsize=9, title_fontsize=10)

plt.suptitle("Sorting Algorithm Performance Across Different Data Distributions", 
             fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig("sorting_runtime_all_distributions.png", dpi=300, bbox_inches="tight")
plt.close()

print("Comparison plot saved as 'sorting_runtime_all_distributions.png'")