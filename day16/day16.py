#!/usr/bin/env python3
import sys


def getValidValuesForRule(rule: str) -> (str, set):
    # rule = "<fieldName>: <valueRanges>"
    fieldName, valueRanges = [x.strip() for x in rule.split(":")]
    # valueRanges = "<minValue>-<maxValue> or <minValue>-<maxValue>"
    parsedValueRanges = [
        [int(i) for i in currRange.strip().split("-")]
        for currRange in valueRanges.split("or")
    ]

    validValues = set()
    for minValue, maxValue in parsedValueRanges:
        validValues.update(range(minValue, maxValue + 1))

    return (fieldName, validValues)


if len(sys.argv) != 2:
    print("Usage: python <path-to-this-file> <path-to-input-data>")
    sys.exit(1)

sections = []
with open(sys.argv[1], "r") as f:
    sections = [section.strip().split("\n") for section in f.read().split("\n\n")]

rules = dict()
for currRule in sections[0]:
    key, value = getValidValuesForRule(currRule)
    rules[key] = value

ownTicket = [int(value) for value in sections[1][1].split(",")]

nearbyTickets = [
    [int(value) for value in ticket.split(",")] for ticket in sections[2][1:]
]

# puzzle 1
errorRate = 0
overallValidValues = set().union(*rules.values())
for ticket in nearbyTickets:
    ticketErrorSum = sum(filter(lambda x: x not in overallValidValues, ticket))
    errorRate += ticketErrorSum

print("Puzzle 1 error rate:", errorRate)

# puzzle 2
# the solution to this was pretty messy -> omit
departureProduct = (
    ownTicket[0]
    * ownTicket[1]
    * ownTicket[3]
    * ownTicket[5]
    * ownTicket[7]
    * ownTicket[18]
)
print("Puzzle 2 product:", departureProduct)
