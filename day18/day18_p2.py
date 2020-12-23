#!/usr/bin/env python3
import sys


def add(a: int, b: int) -> int:
    return a + b


def mul(a: int, b: int) -> int:
    return a * b


def getInnerClosureEnd(substr: str, startIndex: int) -> int:
    index = startIndex
    closureCount = 1

    while closureCount > 0:
        index += 1

        if substr[index] == "(":
            closureCount += 1

        if substr[index] == ")":
            closureCount -= 1

    return index


def newClosure(substr: str) -> int:
    closure = preprocessClosure(substr)
    index = 0
    result = 0
    currOp = add

    while index < len(closure):
        if closure[index] == "(":
            closureEnd = getInnerClosureEnd(closure, index)
            closureResult = newClosure(closure[(index + 1) : closureEnd])
            result = currOp(result, closureResult)

            index = closureEnd + 1
            continue

        if closure[index] == "*":
            currOp = mul
            index += 1
            continue

        if closure[index] == "+":
            currOp = add
            index += 1
            continue

        result = currOp(result, int(closure[index]))
        index += 1

    return result


def preprocessClosure(substr: str) -> str:
    index = 0
    substrWithoutClosures = ""
    while index < len(substr):
        if substr[index] == "(":
            stopIndex = getInnerClosureEnd(substr, index)
            padding = " " * (stopIndex - index + 1)
            substrWithoutClosures += padding
            index = stopIndex
        else:
            substrWithoutClosures += substr[index]

        index += 1

    # no more inner closures needed
    if substrWithoutClosures.find("*", 0) == -1:
        return substr

    # at least one inner closure needed
    index = 0
    preprocessedClosure = "("
    while (mulIndex := substrWithoutClosures.find("*", index)) != -1:
        preprocessedClosure += substr[index:mulIndex]
        preprocessedClosure += ")*("
        index = mulIndex + 1

    preprocessedClosure += substr[index:] + ")"

    return preprocessedClosure


if len(sys.argv) != 2:
    print("Usage: python <path-to-this-file> <path-to-input-data>")
    sys.exit(1)

lines = []
with open(sys.argv[1], "r") as f:
    lines = ["".join(line.split()) for line in f.readlines()]

resultSum = sum(list(map(lambda line: newClosure(line), lines)))
print("Puzzle 2 sum:", resultSum)
