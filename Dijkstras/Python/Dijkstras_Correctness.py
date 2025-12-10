# Dijkstras_Correctness.py
"""
Correctness test harness for Python Dijkstra algorithms.

Assumes each algorithm is a function:
    def dijkstra(graph: Graph, source: Node) -> Dict[Node, float]:
"""
import math
import random
import networkx as nx
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

def nx_dijkstra_reference(graph: Graph, source: int) -> Dict[int, float]:
    G = nx.DiGraph()
    for u, edges in graph.items():
        for v, w in edges:
            G.add_edge(u, v, weight=w)

    # Returns a dict node -> distance
    dist = nx.single_source_dijkstra_path_length(G, source, weight="weight")
    return dist  # unreachable nodes just won't appear

def normalize(dist: Dict[int, float], nodes) -> Dict[int, float]:
    return {u: dist.get(u, math.inf) for u in nodes}

def test_one_algorithm(name: str, algo):
    random.seed(1) # for reproducibility
    
    # test 100 times with graphs of 20 nodes with each edge having a 20% chance of existing
    NUM_TESTS = 100
    N = 20
    EDGE_PROB = 0.2

    failures = 0
    exceptions = 0

    for _ in range(NUM_TESTS):
        g = gen_random_graph(N, EDGE_PROB)
        nodes = list(g.keys())
        source = random.randrange(N)

        try:
            ref = nx_dijkstra_reference(g, source)
            got = algo(g, source)

            ref_norm = normalize(ref, nodes)
            got_norm = normalize(got, nodes)

            for u in nodes:
                if not math.isclose(ref_norm[u], got_norm[u],
                                    rel_tol=1e-9, abs_tol=1e-9):
                    failures += 1
                    break
        except Exception:
            exceptions += 1

    print(f"{name}: failures={failures}, exceptions={exceptions}")

if __name__ == "__main__":
    for name, algo in ALGORITHMS.items():
        test_one_algorithm(name, algo)
