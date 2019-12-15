from collections import defaultdict
from dataclasses import dataclass
from math import ceil
from typing import List, Tuple


def read_input():
    with open('d14.txt') as f:
        return f.read()


@dataclass
class Chemical:
    name: str
    quantity: int


@dataclass
class ReactionFormula:
    name: str
    quantity: int
    components: List[Chemical]

    def __init__(self, result: Tuple[str, int], *components: Tuple[str, int]):
        self.name = result[0]
        self.quantity = result[1]
        self.components = [Chemical(n, q) for n, q in components]

    def __getitem__(self, item):
        return self.components[item]


class FormulaBook:
    def __init__(self, formula: str):
        self.book = {}

        for line in formula.strip().split('\n'):
            components, result = line.strip().split('=>')
            reaction = ReactionFormula(self._process_line(result),
                                       *(self._process_line(c) for c in components.split(',')))
            self.book[reaction.name] = reaction

    @staticmethod
    def _process_line(line_item: str):
        quantity, chemical = line_item.strip().split(' ')
        return chemical, int(quantity)

    def __getitem__(self, item):
        return self.book[item]

    def __contains__(self, item):
        return item in self.book


class Refinery:
    def __init__(self, formula: str):
        self.formulas = FormulaBook(formula)
        self.ore = self.calculate_num_ores_for_fuel(1)
        self.fuel = self.calculate_fuel_from_ore(1_000_000_000_000)

    def calculate_num_ores_for_fuel(self, fuel):
        required = defaultdict(int, {'FUEL': fuel})

        stack: List[ReactionFormula] = [self.formulas["FUEL"]]
        while len(stack) > 0:
            formula = stack.pop()
            batch_size = ceil(required[formula.name] / formula.quantity)

            for c in formula.components:
                required[c.name] += batch_size * c.quantity

                if c.name in self.formulas:
                    stack.append(self.formulas[c.name])

            required[formula.name] -= batch_size * formula.quantity

        return required["ORE"]

    def calculate_fuel_from_ore(self, ore=0):
        low = ore // self.calculate_num_ores_for_fuel(1)
        high = low * 2

        while high > low:
            mid = (high + low) // 2
            if mid == low:
                break

            fuel_ore = self.calculate_num_ores_for_fuel(mid)

            if fuel_ore > ore:
                high = mid
            else:
                low = mid

        return low


r = Refinery(read_input())
print("Part 1: ", r.ore)
print("Part 2: ", r.fuel)
