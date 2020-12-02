#!/usr/bin/env python3
import sys
import re

if len(sys.argv) != 2:
    print("Usage: python <path-to-input-data>")
    sys.exit(1)

entries = []
with open(sys.argv[1], "r") as f:
    entries = f.readlines()

lineRegex = re.compile(r"(\d*)-(\d*)\s*([a-zA-Z]):\s*(\w*)")

# puzzle 1
validPasswords = 0
for currEntry in entries:
    (policyMin, policyMax, policyChar, password) = lineRegex.match(currEntry).groups()

    if int(policyMin) <= password.count(policyChar) <= int(policyMax):
        validPasswords += 1

print("Puzzle 1 valid passwords:", validPasswords)

# puzzle 2
validPasswords = 0
for currEntry in entries:
    (indexOne, indexTwo, policyChar, password) = lineRegex.match(currEntry).groups()

    indexOne = int(indexOne) - 1
    indexTwo = int(indexTwo) - 1

    validPasswords += (password[indexOne] == policyChar) \
                    ^ (password[indexTwo] == policyChar)

print("Puzzle 2 valid passwords:", validPasswords)
