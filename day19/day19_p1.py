#!/usr/bin/env python3
import sys


def buildMatchingStrings(rules: dict, ruleValue) -> list:
    if isinstance(ruleValue, str):
        return [[ruleValue]]

    matchOptions = []
    for ruleOption in ruleValue:
        currMatchOptions = [[]]

        for ruleIndex in ruleOption:
            nextLevelMatches = buildMatchingStrings(rules, rules[ruleIndex])
            currMatchOptions = [
                base + nextLevel
                for base in currMatchOptions
                for nextLevel in nextLevelMatches
            ]

        matchOptions.extend(currMatchOptions)

    return matchOptions


def parseRule(rule: str) -> (int, list):
    ruleIndex, ruleValue = [element.strip() for element in rule.split(":")]

    # actual character rule
    if ruleValue.startswith('"'):
        return (int(ruleIndex), ruleValue.replace('"', ""))

    # recursive rule
    ruleValue = [
        [int(item) for item in element.strip().split()]
        for element in ruleValue.split("|")
    ]
    return (int(ruleIndex), ruleValue)


if len(sys.argv) != 2:
    print("Usage: python <path-to-this-file> <path-to-input-data>")
    sys.exit(1)

sections = []
with open(sys.argv[1], "r") as f:
    sections = [
        [line.strip() for line in section.split("\n") if line.strip() != ""]
        for section in f.read().split("\n\n")
    ]

rules = {
    ruleIndex: ruleValue
    for ruleIndex, ruleValue in [parseRule(rule) for rule in sections[0]]
}
messages = sections[1]

rule0MatchingStrings = [
    "".join(matchingString) for matchingString in buildMatchingStrings(rules, rules[0])
]
numValidMessages = len(list(filter(lambda msg: msg in rule0MatchingStrings, messages)))
print("Puzzle 1 valid messages:", numValidMessages)
