#!/usr/bin/env python3
import sys


def simulateGame1(deck1: list, deck2: list) -> int:
    player1 = deck1[:]
    player2 = deck2[:]

    while len(player1) > 0 and len(player2) > 0:
        player1Card = player1.pop(0)
        player2Card = player2.pop(0)
        if player1Card > player2Card:
            player1 += [player1Card, player2Card]
        else:
            player2 += [player2Card, player1Card]

    winningDeck = player1 if len(player2) == 0 else player2

    return sum(map(lambda i: (i[0] + 1) * i[1], list(enumerate(reversed(winningDeck)))))


def simulateGame2(deck1: list, deck2: list) -> (int, int):
    players = [deck1[:], deck2[:]]
    previousRoundDecks = []

    while len(players[0]) > 0 and len(players[1]) > 0:
        roundDecks = (
            "1:"
            + ",".join([str(i) for i in players[0]])
            + "\n2:"
            + ",".join([str(j) for j in players[1]])
        )
        if roundDecks in previousRoundDecks:
            return (0, 0)
        previousRoundDecks.append(roundDecks)

        cards = [players[0].pop(0), players[1].pop(0)]

        if len(players[0]) >= cards[0] and len(players[1]) >= cards[1]:
            winnerIndex, _ = simulateGame2(
                players[0][: cards[0]], players[1][: cards[1]]
            )
            players[winnerIndex] += [cards[winnerIndex], cards[winnerIndex ^ 1]]
            continue

        if cards[0] > cards[1]:
            players[0] += [cards[0], cards[1]]
        else:
            players[1] += [cards[1], cards[0]]

    winnerIndex = 1 if len(players[0]) == 0 else 0

    return (
        winnerIndex,
        sum(
            map(
                lambda i: (i[0] + 1) * i[1],
                list(enumerate(reversed(players[winnerIndex]))),
            )
        ),
    )


if len(sys.argv) != 2:
    print("Usage: python <path-to-this-file> <path-to-input-data>")
    sys.exit(1)

player1, player2 = [], []
with open(sys.argv[1], "r") as f:
    player1, player2 = [
        [
            int(line.strip())
            for line in section.strip().split("\n")
            if "Player" not in line
        ]
        for section in f.read().split("\n\n")
    ]

winningScore = simulateGame1(player1, player2)
print("Puzzle 1 winning score:", winningScore)

_, winningScore = simulateGame2(player1, player2)
print("Puzzle 2 winning score:", winningScore)
