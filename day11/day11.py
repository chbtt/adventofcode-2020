#!/usr/bin/env python3
import copy
import sys


OCCUPIED = "#"
EMPTY = "L"
FLOOR = "."
# clockwise starting top-left
adjacentIndexMods = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
]


def isValidSeat(waitingArea: list, xIndex: int, yIndex: int) -> bool:
    borderX = len(waitingArea[0])
    borderY = len(waitingArea)

    if (0 <= xIndex < borderX) and (0 <= yIndex < borderY):
        return True

    return False


def getNumOccupiedSeats(waitingArea: list) -> int:
    return sum([row.count(OCCUPIED) for row in waitingArea])


def getNumAdjacentOccupiedSeats(waitingArea: list, xIndex: int, yIndex: int) -> int:
    adjacentIndices = [
        (xIndex + xMod, yIndex + yMod) for (xMod, yMod) in adjacentIndexMods
    ]
    adjacentSeats = [
        waitingArea[y][x]
        for (x, y) in adjacentIndices
        if isValidSeat(waitingArea, x, y)
    ]

    return adjacentSeats.count(OCCUPIED)


def processSeatP1(waitingArea: list, xIndex: int, yIndex: int) -> str:
    if waitingArea[yIndex][xIndex] == EMPTY:
        if getNumAdjacentOccupiedSeats(waitingArea, xIndex, yIndex) == 0:
            return OCCUPIED

        return EMPTY

    if waitingArea[yIndex][xIndex] == OCCUPIED:
        if getNumAdjacentOccupiedSeats(waitingArea, xIndex, yIndex) >= 4:
            return EMPTY

        return OCCUPIED

    return FLOOR


def getNextVisibleSeat(
    waitingArea: list, xIndex: int, yIndex: int, xMod: int, yMod: int
) -> str:
    currX = xIndex + xMod
    currY = yIndex + yMod

    while isValidSeat(waitingArea, currX, currY):
        if waitingArea[currY][currX] in [OCCUPIED, EMPTY]:
            return waitingArea[currY][currX]

        currX += xMod
        currY += yMod

    return FLOOR


def getNumVisibleOccupiedSeats(waitingArea: list, xIndex: int, yIndex: int) -> int:
    visibleSeats = [
        getNextVisibleSeat(waitingArea, xIndex, yIndex, xMod, yMod)
        for (xMod, yMod) in adjacentIndexMods
    ]

    return visibleSeats.count(OCCUPIED)


def processSeatP2(waitingArea: list, xIndex: int, yIndex: int) -> str:
    if waitingArea[yIndex][xIndex] == EMPTY:
        if getNumVisibleOccupiedSeats(waitingArea, xIndex, yIndex) == 0:
            return OCCUPIED

        return EMPTY

    if waitingArea[yIndex][xIndex] == OCCUPIED:
        if getNumVisibleOccupiedSeats(waitingArea, xIndex, yIndex) >= 5:
            return EMPTY

        return OCCUPIED

    return FLOOR


if len(sys.argv) != 2:
    print("Usage: python <path-to-this-file> <path-to-input-data>")
    sys.exit(1)

waitingArea = []
with open(sys.argv[1], "r") as f:
    waitingArea = [list(line.strip()) for line in f.readlines()]

# puzzle 1
waitingAreaBeforeRound = []
waitingAreaAfterRound = copy.deepcopy(waitingArea)
while waitingAreaBeforeRound != waitingAreaAfterRound:
    waitingAreaBeforeRound = waitingAreaAfterRound

    waitingAreaAfterRound = [
        [
            processSeatP1(waitingAreaBeforeRound, x, y)
            for x in range(0, len(waitingAreaBeforeRound[y]))
        ]
        for y in range(0, len(waitingAreaBeforeRound))
    ]

print("Puzzle 1 occupied seats:", getNumOccupiedSeats(waitingAreaAfterRound))

# puzzle 2
waitingAreaBeforeRound = []
waitingAreaAfterRound = copy.deepcopy(waitingArea)
while waitingAreaBeforeRound != waitingAreaAfterRound:
    waitingAreaBeforeRound = waitingAreaAfterRound

    waitingAreaAfterRound = [
        [
            processSeatP2(waitingAreaBeforeRound, x, y)
            for x in range(0, len(waitingAreaBeforeRound[y]))
        ]
        for y in range(0, len(waitingAreaBeforeRound))
    ]

print("Puzzle 2 occupied seats:", getNumOccupiedSeats(waitingAreaAfterRound))
