#!/usr/bin/env python3
import sys
import re


def parseLine(currLine: str) -> (str, dict):
    (bagType, bagRulesString) = [x.strip() for x in currLine.split("bags contain")]
    bagRules = dict()

    if "no other bags" in bagRulesString:
        return (bagType, bagRules)

    bagRulesRegex = r"(\d+)\s+([a-zA-Z\s]+)bags?"
    for currRule in re.finditer(bagRulesRegex, bagRulesString):
        (currAmount, currBagType) = [x.strip() for x in currRule.groups()]
        bagRules[currBagType] = int(currAmount)

    return (bagType, bagRules)


def canContainBag(bags: dict, targetBagType: str, baseBagType: str) -> bool:
    if len(bags[baseBagType]) == 0:
        return False

    if bags[baseBagType].get(targetBagType) != None:
        return True

    for nextBaseBagType in bags[baseBagType].keys():
        if canContainBag(bags, targetBagType, nextBaseBagType):
            return True

    return False


def getBagCount(bags: dict, targetBagType: str) -> int:
    bagCount = 0
    for currBagType in bags[targetBagType].keys():
        # the bags of currBagType themselves
        bagCount += bags[targetBagType][currBagType]
        # the bags inside of currBagType
        bagCount += bags[targetBagType][currBagType] * getBagCount(bags, currBagType)

    return bagCount


if len(sys.argv) != 2:
    print("Usage: python <path-to-input-data>")
    sys.exit(1)

bags = dict()
with open(sys.argv[1], "r") as f:
    bags.update([parseLine(line) for line in f.readlines()])

# puzzle 1
bagCount = 0
for currBagType in bags.keys():
    bagCount += canContainBag(bags, "shiny gold", currBagType)

print("Puzzle 1 count:", bagCount)

# puzzle 2
bagCount = getBagCount(bags, "shiny gold")

print("Puzzle 2 count:", bagCount)
