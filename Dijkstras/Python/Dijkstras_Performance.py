# Dijkstras_Performance.py
"""
Performance benchmark harness for Python Dijkstra algorithms.

Assumes each algorithm is a function:
    def dijkstra(graph: Graph, source: Node) -> Dict[Node, float]:
"""

import time
import random
import csv
from typing import Dict, List, Tuple

from Dijkstras_ChatGPT import dijkstra as dijkstra_chatgpt
from Dijkstras_DeepSeek import dijkstra as dijkstra_deepseek
from Dijkstras_Claude import dijkstra as dijkstra_claude
from Dijkstras_Gemini import dijkstra as dijkstra_gemini

Node = int
Weight = float
Graph = Dict[Node, List[Tuple[Node, Weight]]]

ALGORITHMS = {
    "chatgpt_py": dijkstra_chatgpt,
    "deepseek_py": dijkstra_deepseek,
    "claude_py": dijkstra_claude,
    "gemini_py": dijkstra_gemini,
}

def gen_random_graph(num_nodes: int, edge_prob: float) -> Graph:
    g: Graph = {u: [] for u in range(num_nodes)}
    for u in range(num_nodes):
        for v in range(num_nodes):
            if u == v:
                continue
            if random.random() < edge_prob:
                w = random.uniform(0.0, 10.0)
                g[u].append((v, w))
    return g

def bench():
    random.seed(1)

    # choose sizes and densities
    SIZES = [50, 100, 200, 500]      # number of nodes
    EDGE_PROBS = [0.05, 0.1, 0.2]    # edge probability
    RUNS_PER_COMBO = 5               # how many graphs per (n, p)

    with open("python_dijkstra_bench.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "algorithm",
            "num_nodes",
            "edge_prob",
            "runs",
            "median_sec",
            "mean_sec",
        ])

        for name, algo in ALGORITHMS.items():
            print("=" * 60)
            print(f"Benchmarking {name}")
            for n in SIZES:
                for p in EDGE_PROBS:
                    # pre-generate graphs + sources so all algos see same workload
                    graphs = [gen_random_graph(n, p) for _ in range(RUNS_PER_COMBO)]
                    sources = [random.randrange(n) for _ in range(RUNS_PER_COMBO)]
                    times: List[float] = []

                    for g, s in zip(graphs, sources):
                        start = time.perf_counter()
                        algo(g, s)
                        dt = time.perf_counter() - start
                        times.append(dt)

                    times.sort()
                    median = times[len(times) // 2]
                    mean = sum(times) / len(times)

                    print(
                        f"{name}: n={n:4d}, p={p:.2f}, "
                        f"median={median:.6f}s, mean={mean:.6f}s"
                    )
                    writer.writerow([name, n, p, len(times), median, mean])

if __name__ == "__main__":
    bench()
