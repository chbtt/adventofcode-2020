#!/usr/bin/env python3
import sys


PUZZLE_INPUT = [int(x) for x in "467528193"]


def prepareDestinationCupLabelList(cups: list) -> list:
    maxCupLabel = max(cups)
    destinationCups = [0] * (maxCupLabel + 1)

    for currCupLabel in cups:
        destinationCupLabel = currCupLabel - 1
        if destinationCupLabel <= 0:
            destinationCupLabel += maxCupLabel

        destinationCups[currCupLabel] = destinationCupLabel

    return destinationCups


def simulateMove(cups: list, destinationCups: list, currCupIndex: int) -> int:
    currCup = cups[currCupIndex]

    pickupStart = currCupIndex + 1
    pickupCups = [
        cups.pop(pickupStart if pickupStart < len(cups) else 0) for _ in range(0, 3)
    ]

    destinationCup = currCup
    while (destinationCup := destinationCups[destinationCup]) in pickupCups:
        pass
    newPickupIndex = (cups.index(destinationCup) + 1) % len(cups)

    cups[newPickupIndex:newPickupIndex] = pickupCups
    nextCupIndex = (cups.index(currCup) + 1) % len(cups)

    return nextCupIndex


cups = PUZZLE_INPUT[:]
destinationCups = prepareDestinationCupLabelList(cups)
currCupIndex = 0
for _ in range(0, 100):
    currCupIndex = simulateMove(cups, destinationCups, currCupIndex)
label1Index = cups.index(1)

print(
    "Puzzle 1 order:",
    "".join([str(x) for x in cups[label1Index + 1 :] + cups[:label1Index]]),
)
