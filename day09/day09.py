#!/usr/bin/env python3
import sys


LEN_PREAMBLE = 25


def numberIsValid(sequence: list, index: int) -> bool:
    combinations = [
        sequence[i] + sequence[j]
        for i in range(index - LEN_PREAMBLE, index)
        for j in range(i, index)
    ]

    return sequence[index] in combinations


def checkForContiguousSet(
    sequence: list, targetNumber: int, startIndex: int
) -> (bool, int):
    endIndex = startIndex
    setSum = 0

    while setSum < targetNumber:
        setSum += sequence[endIndex]

        endIndex += 1

    return (setSum == targetNumber, endIndex)


if len(sys.argv) != 2:
    print("Usage: python <path-to-input-data>")
    sys.exit(1)

sequence = []
with open(sys.argv[1], "r") as f:
    sequence = [int(line.strip()) for line in f.readlines()]

# puzzle 1
index = LEN_PREAMBLE
while index < len(sequence):
    if not numberIsValid(sequence, index):
        break

    index += 1

invalidNumber = sequence[index]
print("Puzzle 1 number:", invalidNumber)

# puzzle 2
contiguousSet = []
startIndex = LEN_PREAMBLE
while startIndex < len(sequence):
    (contiguousSetFound, endIndex) = checkForContiguousSet(
        sequence, invalidNumber, startIndex
    )

    if contiguousSetFound:
        contiguousSet = sequence[startIndex:endIndex]
        break

    startIndex += 1

print("Puzzle 2 number:", min(contiguousSet) + max(contiguousSet))
