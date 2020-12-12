#!/usr/bin/env python3
import sys
import functools


def getTreeCountOnMapTraversal(baseMap: list, stepX: int, stepY: int) -> int:
    mapBorderX = len(baseMap[0])
    mapBorderY = len(baseMap)
    indexX = stepX
    indexY = stepY
    trees = 0

    while indexY < mapBorderY:
        trees += baseMap[indexY][indexX] == "#"

        indexX = (indexX + stepX) % mapBorderX
        indexY += stepY

    return trees


if len(sys.argv) != 2:
    print("Usage: python <path-to-this-file> <path-to-input-data>")
    sys.exit(1)

baseMap = []
with open(sys.argv[1], "r") as f:
    baseMap = [entry.strip() for entry in f.readlines()]

trees = []
trees.append(getTreeCountOnMapTraversal(baseMap, 3, 1))

print("Puzzle 1 trees en route:", trees[0])

trees.append(getTreeCountOnMapTraversal(baseMap, 1, 1))
trees.append(getTreeCountOnMapTraversal(baseMap, 5, 1))
trees.append(getTreeCountOnMapTraversal(baseMap, 7, 1))
trees.append(getTreeCountOnMapTraversal(baseMap, 1, 2))

print("Puzzle 2 multiply result:", functools.reduce(lambda x, y: x * y, trees))
