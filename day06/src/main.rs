use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        println!("Usage: cargo run -- <path-to-input-data>");
        std::process::exit(1);
    }

    let mut trimmed_lines: Vec<String> = Vec::new();
    if let Ok(lines) = read_lines(&args[1]) {
        for line in lines {
            if let Ok(curr_line) = line {
                trimmed_lines.push(String::from(curr_line.trim()));
            }
        }
    }

    let mut sum1: u32 = 0;
    let mut sum2: u32 = 0;
    let mut curr_group: Vec<String> = Vec::new();
    for curr_line in trimmed_lines.clone() {
        if curr_line == "" {
            sum1 += count_any_yes_answers(&curr_group);
            sum2 += count_intersecting_yes_answers(&curr_group);
            curr_group = Vec::new();
            continue;
        }

        curr_group.push(curr_line);
    }
    // last group is not caught by currLine == ""
    sum1 += count_any_yes_answers(&curr_group);
    sum2 += count_intersecting_yes_answers(&curr_group);

    println!("Puzzle 1 sum: {}", sum1);
    println!("Puzzle 2 sum: {}", sum2);
}

fn count_any_yes_answers(group: &Vec<String>) -> u32 {
    let mut yes_answers: HashSet<char> = HashSet::new();

    for entry in group.iter() {
        for curr_char in entry.chars() {
            yes_answers.insert(curr_char);
        }
    }

    return yes_answers.len() as u32;
}

fn count_intersecting_yes_answers(group: &Vec<String>) -> u32 {
    let mut intersecting_answers: HashSet<char> = group[0].chars().collect();

    for i in 1..group.len() {
        intersecting_answers = intersecting_answers
            .intersection(&group[i].chars().collect())
            .cloned()
            .collect();
    }

    return intersecting_answers.len() as u32;
}

// https://doc.rust-lang.org/rust-by-example/std_misc/file/read_lines.html
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
