#!/usr/bin/env python3
import sys
import re


def parsePassport(passportString: str) -> dict:
    passport = dict()

    keyValuePairs = passportString.strip().split()
    for currEntry in keyValuePairs:
        currPair = currEntry.split(":")
        passport[currPair[0]] = currPair[1]

    return passport


def checkRequiredFields(passport: dict) -> bool:
    requiredFields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

    for key in requiredFields:
        if passport.get(key) == None:
            return False

    return True


def checkHeightField(heightField: str) -> bool:
    metric = heightField[-2:]

    if metric == "cm":
        value = heightField.rstrip(metric)
        return 150 <= int(value) <= 193

    if metric == "in":
        value = heightField.rstrip(metric)
        return 59 <= int(value) <= 76

    return False


def checkValidFields(passport: dict) -> bool:
    hairColorRegex = re.compile(r"^#[0-9a-f]{6}$")
    passportIdRegex = re.compile(r"^[0-9]{9}$")
    eyeColors = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
    validationFunctions = {
        "byr": lambda x: 1920 <= int(x) <= 2002,
        "iyr": lambda x: 2010 <= int(x) <= 2020,
        "eyr": lambda x: 2020 <= int(x) <= 2030,
        "hgt": lambda x: checkHeightField(x),
        "hcl": lambda x: hairColorRegex.match(x) != None,
        "ecl": lambda x: x in eyeColors,
        "pid": lambda x: passportIdRegex.match(x) != None,
    }

    for key in validationFunctions.keys():
        if passport.get(key) == None:
            return False

        if validationFunctions.get(key)(passport.get(key)) == False:
            return False

    return True


if len(sys.argv) != 2:
    print("Usage: python <path-to-this-file> <path-to-input-data>")
    sys.exit(1)

lines = []
with open(sys.argv[1], "r") as f:
    lines = f.readlines()

passports = []
currPassport = []
for currLine in lines:
    if currLine == "\n":
        passports.append(parsePassport("".join(currPassport)))
        currPassport = []
        continue

    currPassport.append(currLine)
# last passport is not caught by currLine == "\n"
passports.append(parsePassport("".join(currPassport)))

# puzzle 1
validPassports = 0
for currPassport in passports:
    validPassports += checkRequiredFields(currPassport)

print("Puzzle 1 valid passports:", validPassports)

# puzzle 2
validPassports = 0
for currPassport in passports:
    validPassports += checkValidFields(currPassport)

print("Puzzle 2 valid passports:", validPassports)
