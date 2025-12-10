// src/bin/quicksort_correctness.rs
//
// Correctness test harness for Rust sorting algorithms.
//
// Run with:
//    cargo run --bin quicksort_correctness
//
// This assumes each assistant implementation is in the format
//    pub fn quicksort(a: &mut [i32]) { ... }

use std::collections::HashMap;
use std::panic::{catch_unwind, AssertUnwindSafe};
use rand::rngs::StdRng;
use rand::{Rng, SeedableRng};

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

fn algorithms() -> HashMap<&'static str, SortFn> {
    HashMap::from([
        ("Chatgpt", quicksort_chatgpt_fn as SortFn),
        ("Claude", quicksort_claude_fn as SortFn),
        ("Deepseek", quicksort_deepseek_fn as SortFn),
        ("Gemini", quicksort_gemini_fn as SortFn),
    ])
}

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

fn make_array(dist: &str, n: usize, rng: &mut StdRng) -> Vec<i32> {
    match dist {
        "random" => gen_random(n, rng),
        "sorted" => gen_sorted(n, rng),
        "reversed" => gen_reversed(n, rng),
        "nearly_sorted" => gen_nearly_sorted(n, rng),
        "few_values" => gen_few_values(n, rng),
        _ => panic!("unknown distribution {dist}"),
    }
}

fn edge_cases() -> Vec<Vec<i32>> {
    vec![
        vec![],
        vec![1],
        vec![1, 1, 1],
        vec![0, -1, 5, -1],
        vec![2, 1],
        vec![2, 2, 1, 1],
        vec![5, 4, 3, 2, 1],
    ]
}

const SIZES: &[usize] = &[0, 1, 2, 5, 10, 100, 1000, 5000];
const CASES_PER_COMBO: usize = 20;

// Run Tests

fn run_correctness_tests() {
    let algos = algorithms();
    if algos.is_empty() {
        eprintln!("No algorithms registered.");
        return;
    }

    let mut rng = StdRng::seed_from_u64(1);

    for (name, sort_fn) in algos {
        println!("{}", "=".repeat(70));
        println!("Testing algorithm: {name}");
        let mut total_tests = 0usize;
        let mut total_failures = 0usize;
        let mut total_exceptions = 0usize;

        println!("  Edge cases:");
        for (idx, case) in edge_cases().into_iter().enumerate() {
            total_tests += 1;
            let mut arr = case.clone();
            let mut expected = case.clone();
            expected.sort();

            let res = catch_unwind(AssertUnwindSafe(|| {
                sort_fn(&mut arr);
            }));

            match res {
                Ok(_) => {
                    if arr != expected {
                        total_failures += 1;
                        println!(
                            "    FAIL edge_case[{idx}]: input={:?}, got={:?}, expected={:?}",
                            case, arr, expected
                        );
                    }
                }
                Err(_) => {
                    total_exceptions += 1;
                    println!("    PANIC edge_case[{idx}]");
                }
            }
        }

        println!("  Randomized distributions:");
        for &dist in DIST_NAMES {
            let mut dist_tests = 0usize;
            let mut dist_failures = 0usize;
            let mut dist_exceptions = 0usize;

            for &n in SIZES {
                for _ in 0..CASES_PER_COMBO {
                    total_tests += 1;
                    dist_tests += 1;

                    let input = make_array(dist, n, &mut rng);
                    let mut arr = input.clone();
                    let mut expected = input.clone();
                    expected.sort();

                    let res = catch_unwind(AssertUnwindSafe(|| {
                        sort_fn(&mut arr);
                    }));

                    match res {
                        Ok(_) => {
                            if arr != expected {
                                total_failures += 1;
                                dist_failures += 1;
                                println!(
                                    "    FAIL {dist}, n={n}: input(sample)={:?}, got(sample)={:?}, expected(sample)={:?}",
                                    &input.get(0..10).unwrap_or(&input[..]),
                                    &arr.get(0..10).unwrap_or(&arr[..]),
                                    &expected.get(0..10).unwrap_or(&expected[..]),
                                );
                            }
                        }
                        Err(_) => {
                            total_exceptions += 1;
                            dist_exceptions += 1;
                            println!("    PANIC {dist}, n={n}");
                        }
                    }
                }
            }

            println!(
                "    {dist}: tests={dist_tests}, failures={dist_failures}, panics={dist_exceptions}"
            );
        }

        println!("{}", "-".repeat(70));
        println!(
            "Summary for {name}: tests={total_tests}, failures={total_failures}, panics={total_exceptions}\n"
        );
    }

    println!("All correctness tests completed.");
}

fn main() {
    run_correctness_tests();
}
