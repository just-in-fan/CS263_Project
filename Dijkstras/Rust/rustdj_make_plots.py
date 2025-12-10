# rustdj_make_plots.py
import pandas as pd
import matplotlib.pyplot as plt

# 1) Load the CSV
df = pd.read_csv("rust_dijkstra_bench.csv")

# Clean up algorithm names (remove '_rs' suffix)
df["algorithm"] = df["algorithm"].str.replace('_rs', '', regex=False)

# 2) Choose one edge probability to plot
edge_probs = [0.05, 0.1, 0.2]

for prob in edge_probs:
    df_sub = df[df["edge_prob"] == prob]
    
    # 3) Make a line for each algorithm
    plt.figure(figsize=(10, 6))
    
    # Define colors for algorithms
    colors = ['blue', 'orange', 'green', 'red']
    markers = ['o', 's', '^', 'D']
    
    # Define the order we want to plot algorithms
    algorithm_order = ['chatgpt', 'claude', 'deepseek', 'gemini']
    
    for i, algo in enumerate(algorithm_order):
        if algo in df_sub["algorithm"].values:
            group = df_sub[df_sub["algorithm"] == algo]
            group_sorted = group.sort_values("num_nodes")
            color = colors[i % len(colors)]
            marker = markers[i % len(markers)]
            
            plt.plot(group_sorted["num_nodes"], group_sorted["median_sec"], 
                    marker=marker, label=algo, linewidth=2.5, markersize=8,
                    color=color)
    
    plt.xlabel("Number of Nodes", fontsize=12)
    plt.ylabel("Median Runtime (seconds)", fontsize=12)
    plt.title(f"Rust Dijkstra Median Runtime vs Number of Nodes (edge_prob={prob})", fontsize=14, pad=15)
    plt.legend(title="Algorithm", fontsize=10, title_fontsize=11)
    plt.grid(True, alpha=0.3)
    
    # Use logarithmic scale for y-axis since times vary
    # plt.yscale("log")
    
    # Format axes
    # from matplotlib.ticker import ScalarFormatter
    # plt.gca().yaxis.set_major_formatter(ScalarFormatter())
    # plt.gca().yaxis.set_minor_formatter(ScalarFormatter())
    
    plt.tight_layout()
    # Save with probability in filename
    prob_str = str(prob).replace('.', '')
    plt.savefig(f"rust_dijkstra_runtime_n_vs_p{prob_str}.png", dpi=300, bbox_inches="tight")
    plt.close()

print("Individual plots saved as 'rust_dijkstra_runtime_n_vs_p<prob>.png'")

# 4) Create a single comparison figure with subplots
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Define algorithm colors for consistency across plots
color_map = {
    'chatgpt': 'blue',    # Blue for Chatgpt
    'claude': 'orange',   # Orange for Claude
    'deepseek': 'green',  # Green for Deepseek
    'gemini': 'red'       # Red for Gemini
}

for idx, prob in enumerate(edge_probs):
    ax = axes[idx]
    df_sub = df[df["edge_prob"] == prob]
    
    # Plot in consistent order
    for algo in ['chatgpt', 'claude', 'deepseek', 'gemini']:
        if algo in df_sub["algorithm"].values:
            group = df_sub[df_sub["algorithm"] == algo]
            group_sorted = group.sort_values("num_nodes")
            ax.plot(group_sorted["num_nodes"], group_sorted["median_sec"], 
                    marker="o", label=algo, linewidth=2, markersize=6,
                    color=color_map.get(algo, 'black'))
    
    ax.set_xlabel("Number of Nodes", fontsize=10)
    ax.set_ylabel("Median Runtime (s)", fontsize=10)
    ax.set_title(f"Edge Probability: {prob}", fontsize=12, pad=10)
    ax.grid(True, alpha=0.3)
    # ax.set_yscale("log")
    
    # Add legend to first subplot only
    if idx == 0:
        ax.legend(title="Algorithm", fontsize=9, title_fontsize=10)

plt.suptitle("Rust Dijkstra Algorithm Performance Across Different Edge Probabilities", 
             fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig("rust_dijkstra_runtime_all_probs.png", dpi=300, bbox_inches="tight")
plt.close()

print("Comparison plot saved as 'rust_dijkstra_runtime_all_probs.png'")