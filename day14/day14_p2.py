#!/usr/bin/env python3
import sys

MASK_LEN = 36

if len(sys.argv) != 2:
    print("Usage: python <path-to-this-file> <path-to-input-data>")
    sys.exit(1)

lines = []
with open(sys.argv[1], "r") as f:
    lines = [
        line.strip()
        .replace("mem[", "")
        .replace("]", "")
        .replace("mask", "")
        .split(" = ")
        for line in f.readlines()
    ]

memory = dict()
mask = "0" * MASK_LEN
for [index, value] in lines:
    if index == "":
        mask = value
        continue

    index = "{0:0{1}b}".format(int(index), MASK_LEN)
    indexAppliedMask = [i if m == "0" else m for [m, i] in zip(mask, index)]

    indices = [""]
    for ix in indexAppliedMask:
        if ix == "X":
            indices = [i + "0" for i in indices] + [j + "1" for j in indices]
            continue

        indices = [k + ix for k in indices]

    memory.update([(int(i, 2), int(value)) for i in indices])

print("Puzzle 2 sum: ", sum(memory.values()))
