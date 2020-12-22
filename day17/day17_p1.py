#!/usr/bin/env python3
import sys


ACTIVE = "#"
INACTIVE = "."


def getCoordinateNeighbours(x: int, y: int, z: int) -> list:
    return [
        (ix, iy, iz)
        for ix in [x - 1, x, x + 1]
        for iy in [y - 1, y, y + 1]
        for iz in [z - 1, z, z + 1]
        if not ((ix == x) and (iy == y) and (iz == z))
    ]


def getCoordinatesToCheck(activeCubes: list) -> set:
    coordinatesToCheck = set()
    for currActiveCube in activeCubes:
        coordinatesToCheck.update(getCoordinateNeighbours(*currActiveCube))

    return coordinatesToCheck


def simulateCycle(activeCubes: list) -> list:
    newActiveCubes = []

    for x, y, z in getCoordinatesToCheck(activeCubes):
        activeNeighbourCubes = len(
            list(
                filter(
                    lambda neighbourCube: neighbourCube in activeCubes,
                    getCoordinateNeighbours(x, y, z),
                )
            )
        )

        # cube is active
        if (x, y, z) in activeCubes:
            if 2 <= activeNeighbourCubes <= 3:
                newActiveCubes.append((x, y, z))
        # cube is inactive
        else:
            if activeNeighbourCubes == 3:
                newActiveCubes.append((x, y, z))

    return newActiveCubes


if len(sys.argv) != 2:
    print("Usage: python <path-to-this-file> <path-to-input-data>")
    sys.exit(1)

lines = []
with open(sys.argv[1], "r") as f:
    lines = [line.strip() for line in f.readlines()]

activeCubes = []
for y, line in enumerate(lines):
    for x, value in enumerate(line):
        if value == ACTIVE:
            activeCubes.append((x, y, 0))

for i in range(0, 6):
    activeCubes = simulateCycle(activeCubes)

print("Puzzle 1 active cubes:", len(activeCubes))
