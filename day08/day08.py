#!/usr/bin/env python3
import copy
import sys


accumulator = 0
ip = 0


def acc(arg: int):
    global accumulator
    global ip
    accumulator += arg
    ip += 1


def jmp(arg: int):
    global ip
    ip += arg


def nop(arg: int):
    global ip
    ip += 1


instructions = {"acc": acc, "jmp": jmp, "nop": nop}


def tryToExecuteBootCode(bootCode: list) -> bool:
    global accumulator
    global ip
    accumulator = 0
    ip = 0

    alreadyExecuted = []
    while ip < len(bootCode):
        if ip in alreadyExecuted:
            return False
        alreadyExecuted.append(ip)

        instructions.get(bootCode[ip]["op"])(bootCode[ip]["arg"])

    return True


if len(sys.argv) != 2:
    print("Usage: python <path-to-input-data>")
    sys.exit(1)

bootCode = list()
with open(sys.argv[1], "r") as f:
    lines = [line.strip().split() for line in f.readlines()]
    bootCode = [{"op": currOp, "arg": int(currArg)} for (currOp, currArg) in lines]

# puzzle 1
tryToExecuteBootCode(bootCode)

print("Puzzle 1 accumulator value:", accumulator)

# puzzle 2
for fixIndex in range(0, len(bootCode)):
    fixIndexOp = bootCode[fixIndex]["op"]
    fixedOp = ""

    if fixIndexOp == "acc":
        continue
    if fixIndexOp == "jmp":
        fixedOp = "nop"
    if fixIndexOp == "nop":
        fixedOp = "jmp"

    fixedBootCode = copy.deepcopy(bootCode)
    fixedBootCode[fixIndex]["op"] = fixedOp

    if tryToExecuteBootCode(fixedBootCode):
        break

print("Puzzle 2 accumulator value:", accumulator)
