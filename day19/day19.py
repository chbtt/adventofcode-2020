#!/usr/bin/env python3
import sys


def buildMatcher(rules: dict, ruleValue):
    if isinstance(ruleValue, str):
        return ruleValue

    matchOptions = []
    for ruleOption in ruleValue:
        matchingStrings = []

        for ruleIndex in ruleOption:
            matchingStrings.append(buildMatcher(rules, rules[ruleIndex]))

        matchOptions.append(matchingStrings)

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
