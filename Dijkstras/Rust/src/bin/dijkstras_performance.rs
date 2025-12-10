// src/bin/dijkstras_performance.rs
//
// Performance benchmark harness for Rust dijkstra algorithms.
//
// Run with:
//    cargo run --bin dijkstras_performance --release
//
// and writes results to "rust_bench_results.csv" in the project root.

use std::collections::HashMap;
use std::time::Instant;
use rand::rngs::StdRng;
use rand::{Rng, SeedableRng};
use std::fs::File;
use std::io::{BufWriter, Write};

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

#[derive(Debug)]
struct BenchRow {
    algorithm: String,
    num_nodes: usize,
    edge_prob: f64,
    runs: usize,
    median_sec: f64,
    mean_sec: f64,
}

fn gen_random_graph(rng: &mut StdRng, num_nodes: usize, edge_prob: f64) -> Graph {
    let mut g: Graph = HashMap::new();
    for u in 0..num_nodes {
        let mut edges = Vec::new();
        for v in 0..num_nodes {
            if u == v {
                continue;
            }
            if rng.gen_range(0.0..10.0) < edge_prob {
                let w = rng.gen_range(0.0..10.0);
                edges.push((v, w));
            }
        }
        g.insert(u, edges);
    }
    g
}

fn bench_one<F>(name: &str, algo: F) -> Vec<BenchRow>
where
    F: Fn(&Graph, Node) -> HashMap<Node, Weight>,
{
    let mut rng = StdRng::seed_from_u64(1);

    let sizes: [usize; 4] = [100, 500, 1000, 5000];
    let edge_probs: [f64; 3] = [0.05, 0.10, 0.20];
    let runs_per_combo: usize = 5;

    let mut rows = Vec::new();

    for &n in &sizes {
        for &p in &edge_probs {
            let mut times = Vec::<f64>::new();

            // Pre-generate graphs + sources so every algorithm sees the same cases
            let mut graphs = Vec::new();
            let mut sources = Vec::new();
            for _ in 0..runs_per_combo {
                graphs.push(gen_random_graph(&mut rng, n, p));
                sources.push(rng.gen_range(0..n));
            }

            for (g, &s) in graphs.iter().zip(sources.iter()) {
                let start = Instant::now();
                let _ = algo(g, s);
                let elapsed = start.elapsed().as_secs_f64();
                times.push(elapsed);
            }

            times.sort_by(|a, b| a.partial_cmp(b).unwrap());
            let median = times[times.len() / 2];
            let mean: f64 = times.iter().sum::<f64>() / times.len() as f64;

            // Keep your original print:
            println!(
                "{},{},{},{},{:.6},{:.6}",
                name, n, p, runs_per_combo, median, mean
            );

            // Also store for CSV:
            rows.push(BenchRow {
                algorithm: name.to_string(),
                num_nodes: n,
                edge_prob: p,
                runs: runs_per_combo,
                median_sec: median,
                mean_sec: mean,
            });
        }
    }
    rows
}

fn write_csv(rows: &[BenchRow], filename: &str) {
    if rows.is_empty() {
        eprintln!("No rows to write.");
        return;
    }

    let file = File::create(filename).expect("failed to create CSV file");
    let mut w = BufWriter::new(file);

    // header
    writeln!(
        w,
        "algorithm,num_nodes,edge_prob,runs,median_sec,mean_sec"
    )
    .unwrap();

    // rows
    for r in rows {
        writeln!(
            w,
            "{},{},{},{},{:.9},{:.9}",
            r.algorithm, r.num_nodes, r.edge_prob, r.runs, r.median_sec, r.mean_sec
        )
        .unwrap();
    }

    println!("Results written to {filename}");
}

fn main() {
    println!("algorithm,num_nodes,edge_prob,runs,median_sec,mean_sec");

    let mut all_rows = Vec::new();

    all_rows.extend(bench_one("chatgpt_rs", dijkstra_chatgpt));
    all_rows.extend(bench_one("claude_rs", dijkstra_claude));
    all_rows.extend(bench_one("deepseek_rs", dijkstra_deepseek));
    all_rows.extend(bench_one("gemini_rs", dijkstra_gemini));

    write_csv(&all_rows, "rust_dijkstra_bench.csv");
}
