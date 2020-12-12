#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: python <path-to-this-file> <path-to-input-data>")
    sys.exit(1)

entries = []
with open(sys.argv[1], "r") as f:
    entries = f.readlines()
    entries = [int(entry.strip()) for entry in entries]

# puzzle 1
for (i, x) in enumerate(entries):
    tempEntries = entries[:i] + entries[(i + 1) :]
    result = list(filter(lambda y: (x + y) == 2020, tempEntries))
    if len(result) > 0:
        y = result.pop()
        print("{:d} + {:d} = 2020".format(x, y))
        z = x * y
        print("{:d} * {:d} = {:d}".format(x, y, z))
        break

# puzzle 2
for (i, x) in enumerate(entries):
    tempEntriesX = entries[:i] + entries[(i + 1) :]
    for (j, y) in enumerate(tempEntriesX):
        tempEntriesY = tempEntriesX[:j] + tempEntriesX[(j + 1) :]
        result = list(filter(lambda z: (x + y + z) == 2020, tempEntriesY))
        if len(result) > 0:
            z = result.pop()
            print("{:d} + {:d} + {:d} = 2020".format(x, y, z))
            a = x * y * z
            print("{:d} * {:d} * {:d} = {:d}".format(x, y, z, a))
            sys.exit(1)
