use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

const NORTH_ACTION: char = 'N';
const SOUTH_ACTION: char = 'S';
const EAST_ACTION: char = 'E';
const WEST_ACTION: char = 'W';
const LEFT_ACTION: char = 'L';
const RIGHT_ACTION: char = 'R';
const FORWARD_ACTION: char = 'F';

enum Direction {
    NORTH,
    EAST,
    SOUTH,
    WEST,
}

impl Direction {
    fn degree_value(&self) -> i32 {
        match *self {
            Direction::NORTH => 0,
            Direction::EAST => 90,
            Direction::SOUTH => 180,
            Direction::WEST => 270,
        }
    }

    fn from_degrees(degrees: i32) -> Option<Direction> {
        match degrees {
            0 => Some(Direction::NORTH),
            90 => Some(Direction::EAST),
            180 => Some(Direction::SOUTH),
            270 => Some(Direction::WEST),
            _ => None,
        }
    }
}

#[derive(Clone)]
struct Instruction {
    action: char,
    value: i32,
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        println!("Usage: cargo run -- <path-to-input-data>");
        std::process::exit(1);
    }

    let mut instructions: Vec<Instruction> = Vec::new();
    if let Ok(lines) = read_lines(&args[1]) {
        for line in lines {
            if let Ok(curr_line) = line {
                let mut trimmed_line: String = String::from(curr_line.trim());
                let curr_value: i32 = trimmed_line.split_off(1).parse().unwrap();
                let curr_action: char = trimmed_line.chars().next().unwrap();

                instructions.push(Instruction {
                    action: curr_action,
                    value: curr_value,
                });
            }
        }
    }

    let puzzle_one_result: i32 = puzzle_one(instructions.clone());
    println!("Puzzle 1 distance: {}", puzzle_one_result);
    let puzzle_two_result: i32 = puzzle_two(instructions.clone());
    println!("Puzzle 2 distance: {}", puzzle_two_result);
}

fn calculate_position_modifier(curr_direction: &Direction, units: i32) -> (i32, i32) {
    match *curr_direction {
        Direction::NORTH => (0, units),
        Direction::EAST => (units, 0),
        Direction::SOUTH => (0, -1 * units),
        Direction::WEST => (-1 * units, 0),
    }
}

fn puzzle_one(instructions: Vec<Instruction>) -> i32 {
    let mut direction: Direction = Direction::EAST;
    let mut east_pos: i32 = 0;
    let mut north_pos: i32 = 0;

    for curr_instruction in instructions {
        match curr_instruction.action {
            NORTH_ACTION => {
                north_pos += curr_instruction.value;
            }
            SOUTH_ACTION => {
                north_pos -= curr_instruction.value;
            }
            EAST_ACTION => {
                east_pos += curr_instruction.value;
            }
            WEST_ACTION => {
                east_pos -= curr_instruction.value;
            }
            LEFT_ACTION => {
                let new_direction: i32 =
                    (360 + direction.degree_value() + (-1 * curr_instruction.value)) % 360;
                direction = Direction::from_degrees(new_direction).unwrap();
            }
            RIGHT_ACTION => {
                let new_direction: i32 = (direction.degree_value() + curr_instruction.value) % 360;
                direction = Direction::from_degrees(new_direction).unwrap();
            }
            FORWARD_ACTION => {
                let (east_modifier, north_modifier): (i32, i32) =
                    calculate_position_modifier(&direction, curr_instruction.value);
                east_pos += east_modifier;
                north_pos += north_modifier;
            }
            _ => {
                println!("Something went wrong during parsing!");
                std::process::exit(1);
            }
        }
    }

    return east_pos.abs() + north_pos.abs();
}

fn puzzle_two(instructions: Vec<Instruction>) -> i32 {
    let mut east_pos: i32 = 0;
    let mut north_pos: i32 = 0;
    let mut waypoint_east_pos: i32 = 10;
    let mut waypoint_north_pos: i32 = 1;

    for curr_instruction in instructions {
        match curr_instruction.action {
            NORTH_ACTION => {
                waypoint_north_pos += curr_instruction.value;
            }
            SOUTH_ACTION => {
                waypoint_north_pos -= curr_instruction.value;
            }
            EAST_ACTION => {
                waypoint_east_pos += curr_instruction.value;
            }
            WEST_ACTION => {
                waypoint_east_pos -= curr_instruction.value;
            }
            LEFT_ACTION => {
                for _ in 0..(curr_instruction.value / 90) {
                    let temp: i32 = waypoint_east_pos;
                    waypoint_east_pos = waypoint_north_pos * -1;
                    waypoint_north_pos = temp;
                }
            }
            RIGHT_ACTION => {
                for _ in 0..(curr_instruction.value / 90) {
                    let temp: i32 = waypoint_east_pos;
                    waypoint_east_pos = waypoint_north_pos;
                    waypoint_north_pos = temp * -1;
                }
            }
            FORWARD_ACTION => {
                east_pos += curr_instruction.value * waypoint_east_pos;
                north_pos += curr_instruction.value * waypoint_north_pos;
            }
            _ => {
                println!("Something went wrong during parsing!");
                std::process::exit(1);
            }
        }
    }

    return east_pos.abs() + north_pos.abs();
}

// https://doc.rust-lang.org/rust-by-example/std_misc/file/read_lines.html
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
