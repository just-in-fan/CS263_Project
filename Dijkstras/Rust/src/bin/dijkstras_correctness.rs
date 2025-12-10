// src/bin/dijkstras_correctness.rs
//
// Correctness test harness for Rust dijkstra algorithms.
//
// Run with:
//    cargo run --bin dijkstras_correctness
//
// This assumes each assistant implementation is in the format
//    pub fn dijkstra(graph: &Graph, source: Node) -> HashMap<Node, Weight> { ... }

use std::collections::HashMap;
use std::f64;

use rand::rngs::StdRng;
use rand::{Rng, SeedableRng};

use petgraph::graph::NodeIndex;
use petgraph::prelude::DiGraph;
use petgraph::algo::dijkstra as pg_dijkstra;

pub type Node = usize;
pub type Weight = f64;
pub type Graph = HashMap<Node, Vec<(Node, Weight)>>;

// Import Algorithms

mod dijkstras_chatgpt;
mod dijkstras_claude;
mod dijkstras_deepseek;
mod dijkstras_gemini;

use dijkstras_chatgpt::dijkstra as dijkstra_chatgpt;
use dijkstras_claude::dijkstra as dijkstra_claude;
use dijkstras_deepseek::dijkstra as dijkstra_deepseek;
use dijkstras_gemini::dijkstra as dijkstra_gemini;

/// Use petgraph's Dijkstra as the reference / oracle.
fn dijkstra_reference_lib(graph: &Graph, source: Node) -> HashMap<Node, Weight> {
    // Build a directed graph in petgraph
    let mut g: DiGraph<(), Weight> = DiGraph::new();

    // Map from your Node (usize) to petgraph's NodeIndex
    let mut index_map: HashMap<Node, NodeIndex> = HashMap::new();

    // First make sure every node that appears as a key gets a NodeIndex
    for &u in graph.keys() {
        let idx = g.add_node(());
        index_map.insert(u, idx);
    }

    // Also ensure nodes that only appear as targets exist as well
    {
        let mut extra_nodes: Vec<Node> = Vec::new();
        for (&u, edges) in graph.iter() {
            for &(v, _w) in edges {
                if !index_map.contains_key(&v) {
                    extra_nodes.push(v);
                }
            }
        }
        for v in extra_nodes {
            let idx = g.add_node(());
            index_map.insert(v, idx);
        }
    }

    // Add edges with weights
    for (&u, edges) in graph.iter() {
        let u_idx = index_map[&u];
        for &(v, w) in edges {
            let v_idx = index_map[&v];
            g.add_edge(u_idx, v_idx, w);
        }
    }

    // Run petgraph's Dijkstra
    let source_idx = match index_map.get(&source) {
        Some(idx) => *idx,
        None => {
            // source not even in graph: return empty
            return HashMap::new();
        }
    };

    let dist_map = pg_dijkstra(&g, source_idx, None, |e| *e.weight());

    // Convert back to HashMap<Node, Weight>
    let mut result: HashMap<Node, Weight> = HashMap::new();
    for (&node, &idx) in index_map.iter() {
        if let Some(&d) = dist_map.get(&idx) {
            result.insert(node, d);
        }
    }
    result
}

fn gen_random_graph(rng: &mut StdRng, num_nodes: usize, edge_prob: f64) -> Graph {
    let mut g: Graph = HashMap::new();
    for u in 0..num_nodes {
        let mut edges = Vec::new();
        for v in 0..num_nodes {
            if u == v {
                continue;
            }
            if rng.gen_range(0.0..1.0) < edge_prob {
                let w = rng.gen_range(0.0..10.0);
                edges.push((v, w));
            }
        }
        g.insert(u, edges);
    }
    g
}

fn normalize(dist: &HashMap<Node, Weight>, nodes: &[Node]) -> HashMap<Node, Weight> {
    let mut out = HashMap::new();
    for &u in nodes {
        let d = dist.get(&u).copied().unwrap_or(f64::INFINITY);
        out.insert(u, d);
    }
    out
}

fn approx_equal(a: f64, b: f64) -> bool {
    if a.is_infinite() && b.is_infinite() {
        return true;
    }
    let diff = (a - b).abs();
    let scale = a.abs().max(b.abs()).max(1.0);
    diff <= 1e-9 * scale
}

fn test_one_algorithm<F>(name: &str, algo: F)
where
    F: Fn(&Graph, Node) -> HashMap<Node, Weight> + std::panic::RefUnwindSafe,
{
    let mut rng = StdRng::seed_from_u64(1);

    const NUM_TESTS: usize = 100;
    const N: usize = 20;
    const EDGE_PROB: f64 = 0.2;

    let mut failures = 0usize;
    let mut exceptions = 0usize;

    for _ in 0..NUM_TESTS {
        let g = gen_random_graph(&mut rng, N, EDGE_PROB);
        let nodes: Vec<_> = g.keys().copied().collect();
        let source = rng.gen_range(0..N);

        let result = std::panic::catch_unwind(|| {
            let ref_dist = dijkstra_reference_lib(&g, source);
            let got_dist = algo(&g, source);

            let ref_norm = normalize(&ref_dist, &nodes);
            let got_norm = normalize(&got_dist, &nodes);

            for u in &nodes {
                if !approx_equal(ref_norm[u], got_norm[u]) {
                    return Err(());
                }
            }
            Ok(())
        });

        match result {
            Ok(Ok(())) => {}
            Ok(Err(())) => failures += 1,
            Err(_) => exceptions += 1,
        }
    }

    println!(
        "{}: tests={}, failures={}, exceptions={}",
        name, NUM_TESTS, failures, exceptions
    );
}

fn main() {
    test_one_algorithm("chatgpt_rs", dijkstra_chatgpt);
    test_one_algorithm("claude_rs", dijkstra_claude);
    test_one_algorithm("deepseek_rs", dijkstra_deepseek);
    test_one_algorithm("gemini_rs", dijkstra_gemini);
}
