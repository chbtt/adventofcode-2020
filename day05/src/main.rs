use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

const ROW_BIT_BASE: u32 = 64;
const ROW_UPPER_CHAR: char = 'B';
const ROW_LOWER_CHAR: char = 'F';
const COL_BIT_BASE: u32 = 4;
const COL_UPPER_CHAR: char = 'R';
const COL_LOWER_CHAR: char = 'L';
const SEAT_ID_MULTIPLIER: u32 = 8;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        println!("Usage: cargo run -- <path-to-input-data>");
        std::process::exit(1);
    }

    let mut seat_id_list: Vec<u32> = Vec::new();
    if let Ok(lines) = read_lines(&args[1]) {
        for line in lines {
            if let Ok(mut curr_boarding_pass_string) = line {
                if curr_boarding_pass_string.ends_with('\n') {
                    curr_boarding_pass_string.pop();
                }
                if let Some(seat_id) = parse_boarding_pass(curr_boarding_pass_string) {
                    seat_id_list.push(seat_id);
                }
            }
        }
    }

    // puzzle 1
    seat_id_list.sort();
    println!(
        "Puzzle 1 highest seat id: {}",
        *seat_id_list.last().unwrap()
    );

    // puzzle 2
    // set_id_list already sorted
    let mut my_seat_id: u32 = 0;
    let mut last_seat_id: u32 = 0;
    for seat_id in seat_id_list {
        if seat_id == (last_seat_id + 2) {
            my_seat_id = seat_id - 1;
            break;
        }
        last_seat_id = seat_id;
    }
    println!("Puzzle 2 seat id: {}", my_seat_id);
}

fn parse_boarding_pass(boarding_pass_string: String) -> Option<u32> {
    let mut row: u32 = 0;
    let mut col: u32 = 0;
    let mut row_bit: u32 = ROW_BIT_BASE;
    let mut col_bit: u32 = COL_BIT_BASE;

    for curr_char in boarding_pass_string.chars() {
        match curr_char {
            ROW_UPPER_CHAR => {
                row ^= row_bit;
                row_bit >>= 1;
            }
            ROW_LOWER_CHAR => {
                row_bit >>= 1;
            }
            COL_UPPER_CHAR => {
                col ^= col_bit;
                col_bit >>= 1;
            }
            COL_LOWER_CHAR => {
                col_bit >>= 1;
            }
            _ => {
                return None;
            }
        }
    }

    return Some(row * SEAT_ID_MULTIPLIER + col);
}

// https://doc.rust-lang.org/rust-by-example/std_misc/file/read_lines.html
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
