#!/usr/bin/env python3
import functools
import sys


def parseLines(lines: list) -> (list, list):
    ingredientLists, allergenLists = [], []

    for line in lines:
        i, a = line.replace(")", "").split("(contains")
        ingredientLists.append([item.strip() for item in i.split()])
        allergenLists.append([item.strip() for item in a.split(",")])

    return (ingredientLists, allergenLists)


def identifyIngredient(
    ingredientLists: list, allergenLists: list, allergen: str
) -> str:
    containingIngredientLists = [
        set(ingredients)
        for ingredients, allergenes in zip(ingredientLists, allergenLists)
        if allergen in allergenes
    ]

    ingredientsLeft = functools.reduce(
        lambda a, b: a.intersection(b), containingIngredientLists
    )

    if len(ingredientsLeft) != 1:
        return ""

    return ingredientsLeft.pop()


if len(sys.argv) != 2:
    print("Usage: python <path-to-this-file> <path-to-input-data>")
    sys.exit(1)

lines = []
with open(sys.argv[1], "r") as f:
    lines = [line.strip() for line in f.readlines()]

ingredientLists, allergenLists = parseLines(lines)
ingredients = list(set([b for a in ingredientLists for b in a]))
allergenes = list(set([b for a in allergenLists for b in a]))
identifiedIngredients = dict()

while len(allergenes) > 0:
    for currAllergen in allergenes:
        currIngredient = identifyIngredient(
            ingredientLists, allergenLists, currAllergen
        )
        if currIngredient != "":
            identifiedIngredients[currIngredient] = currAllergen
            allergenes.remove(currAllergen)

            ingredientLists = [
                [
                    ingredient
                    for ingredient in ingredients
                    if ingredient != currIngredient
                ]
                for ingredients in ingredientLists
            ]
            allergenLists = [
                [allergene for allergene in allergenes if allergene != currAllergen]
                for allergenes in allergenLists
            ]

print("Puzzle 1 appearances:", len([b for a in ingredientLists for b in a]))

print(
    "Puzzle 2 dangerous ingredients:",
    ",".join(
        sorted(identifiedIngredients.keys(), key=lambda i: identifiedIngredients[i])
    ),
)
