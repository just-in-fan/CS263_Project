// src/bin/quicksort_performance.rs
//
// Performance benchmark harness for Rust sorting algorithms.
//
// Run with:
//    cargo run --bin quicksort_performance --release
//
// and writes results to "rust_bench_results.csv" in the project root.

use std::fs::File;
use rand::rngs::StdRng;
use rand::{Rng, SeedableRng};
use std::io::{BufWriter, Write};
use std::time::Instant;

type SortFn = fn(&mut [i32]);

// Import Algorithms

mod quicksort_chatgpt;
mod quicksort_claude;
mod quicksort_deepseek;
mod quicksort_gemini;

use quicksort_chatgpt::quicksort as quicksort_chatgpt_fn;
use quicksort_claude::quicksort as quicksort_claude_fn;
use quicksort_deepseek::quicksort as quicksort_deepseek_fn;
use quicksort_gemini::quicksort as quicksort_gemini_fn;

// Test Case Generators

fn gen_random(n: usize, rng: &mut StdRng) -> Vec<i32> {
    (0..n)
        .map(|_| rng.gen_range(-1_000_000..=1_000_000))
        .collect()
}

fn gen_sorted(n: usize, rng: &mut StdRng) -> Vec<i32> {
    let mut v = gen_random(n, rng);
    v.sort();
    v
}

fn gen_reversed(n: usize, rng: &mut StdRng) -> Vec<i32> {
    let mut v = gen_random(n, rng);
    v.sort_by(|a, b| b.cmp(a));
    v
}

fn gen_nearly_sorted(n: usize, rng: &mut StdRng) -> Vec<i32> {
    let mut v = gen_sorted(n, rng);
    if n <= 1 {
        return v;
    }
    let num_swaps = (n / 100).max(1); // ~1%
    for _ in 0..num_swaps {
        let i = rng.gen_range(0..n);
        let j = rng.gen_range(0..n);
        v.swap(i, j);
    }
    v
}

fn gen_few_values(n: usize, rng: &mut StdRng) -> Vec<i32> {
    (0..n).map(|_| rng.gen_range(0..=9)).collect()
}

const DIST_NAMES: &[&str] = &["random", "sorted", "reversed", "nearly_sorted", "few_values"];
const SIZES: &[usize] = &[500, 1_000, 5_000, 10_000];
const RUNS_PER_COMBO: usize = 10;

// Precomputed inputs so each algorithm sees identical data.
struct InputSet {
    dist_name: &'static str,
    n: usize,
    runs: Vec<Vec<i32>>,
}

fn precompute_inputs() -> Vec<InputSet> {
    println!("Precomputing input arrays...");
    let mut rng = StdRng::seed_from_u64(1);
    let mut sets = Vec::new();

    for &dist in DIST_NAMES {
        for &n in SIZES {
            let mut runs = Vec::with_capacity(RUNS_PER_COMBO);
            for _ in 0..RUNS_PER_COMBO {
                let arr = match dist {
                    "random" => gen_random(n, &mut rng),
                    "sorted" => gen_sorted(n, &mut rng),
                    "reversed" => gen_reversed(n, &mut rng),
                    "nearly_sorted" => gen_nearly_sorted(n, &mut rng),
                    "few_values" => gen_few_values(n, &mut rng),
                    _ => panic!("unknown distribution {dist}"),
                };
                runs.push(arr);
            }
            sets.push(InputSet { dist_name: dist, n, runs });
        }
    }

    println!("Done.\n");
    sets
}

// Benchmark logic

#[derive(Debug)]
struct BenchRow {
    algorithm: String,
    distribution: String,
    n: usize,
    runs: usize,
    median_sec: f64,
    mean_sec: f64,
    min_sec: f64,
    max_sec: f64,
}

fn time_one_run(sort_fn: SortFn, arr: &[i32]) -> f64 {
    let mut v = arr.to_vec();
    let start = Instant::now();
    sort_fn(&mut v);
    let dt = start.elapsed();
    dt.as_secs_f64()
}

fn benchmark() -> Vec<BenchRow> {
    let algos = vec![
        ("Chatgpt", quicksort_chatgpt_fn as SortFn),
        ("Claude", quicksort_claude_fn as SortFn),
        ("Deepseek", quicksort_deepseek_fn as SortFn),
        ("Gemini", quicksort_gemini_fn as SortFn),
    ];

    if algos.is_empty() {
        eprintln!("No algorithms registered.");
        return Vec::new();
    }

    let inputs = precompute_inputs();
    let mut rows = Vec::new();

    for (name, sort_fn) in algos {
        println!("Benchmarking algorithm: {name}");

        for set in &inputs {
            let mut durations = Vec::with_capacity(set.runs.len());

            for arr in &set.runs {
                let dt = time_one_run(sort_fn, arr);
                durations.push(dt);
            }

            durations.sort_by(|a, b| a.partial_cmp(b).unwrap());
            let min = durations[0];
            let max = *durations.last().unwrap();
            let median = if durations.len() % 2 == 0 {
                let mid = durations.len() / 2;
                (durations[mid - 1] + durations[mid]) / 2.0
            } else {
                durations[durations.len() / 2]
            };
            let sum: f64 = durations.iter().copied().sum();
            let mean = sum / durations.len() as f64;

            println!(
                "{:<12} | {:<13} | n={:<7} | median={:.6}s | mean={:.6}s | min={:.6}s | max={:.6}s",
                name, set.dist_name, set.n, median, mean, min, max
            );

            rows.push(BenchRow {
                algorithm: name.to_string(),
                distribution: set.dist_name.to_string(),
                n: set.n,
                runs: durations.len(),
                median_sec: median,
                mean_sec: mean,
                min_sec: min,
                max_sec: max,
            });
        }

        println!();
    }

    println!("All benchmarks completed.");
    rows
}

fn write_csv(rows: &[BenchRow], filename: &str) {
    if rows.is_empty() {
        eprintln!("No rows to write.");
        return;
    }

    let file = File::create(filename).expect("failed to create CSV file");
    let mut w = BufWriter::new(file);

    writeln!(
        w,
        "algorithm,distribution,n,runs,median_sec,mean_sec,min_sec,max_sec"
    )
    .unwrap();

    for r in rows {
        writeln!(
            w,
            "{},{},{},{},{:.9},{:.9},{:.9},{:.9}",
            r.algorithm,
            r.distribution,
            r.n,
            r.runs,
            r.median_sec,
            r.mean_sec,
            r.min_sec,
            r.max_sec
        )
        .unwrap();
    }

    println!("Results written to {filename}");
}

fn main() {
    let rows = benchmark();
    write_csv(&rows, "rust_bench_results.csv");
}
