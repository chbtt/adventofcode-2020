#!/usr/bin/env python3
import sys


def add(a: int, b: int) -> int:
    return a + b


def mul(a: int, b: int) -> int:
    return a * b


def newClosure(substr: str) -> (int, int):
    index = 0
    result = 0
    currOp = add

    while index < len(substr):
        if substr[index] == "(":
            index += 1
            closureIndex, closureResult = newClosure(substr[index:])
            index += closureIndex
            result = currOp(result, closureResult)
            continue

        if substr[index] == ")":
            index += 1
            return (index, result)

        if substr[index] == "*":
            currOp = mul
            index += 1
            continue

        if substr[index] == "+":
            currOp = add
            index += 1
            continue

        result = currOp(result, int(substr[index]))
        index += 1

    return (index, result)


if len(sys.argv) != 2:
    print("Usage: python <path-to-this-file> <path-to-input-data>")
    sys.exit(1)

lines = []
with open(sys.argv[1], "r") as f:
    lines = ["".join(line.split()) for line in f.readlines()]

resultSum = sum(list(map(lambda line: newClosure(line)[1], lines)))
print("Puzzle 1 sum:", resultSum)
