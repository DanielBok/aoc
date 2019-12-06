from typing import List


def read_question_input():
    with open('d6.txt') as f:
        return [s.strip().split(')') for s in f.readlines()]


def count_orbits(_input: List[List[str]]):
    orbits = {child: parent for parent, child in _input}

    def count_orbit_for(node: str, current=0):
        if node not in orbits:
            return current
        return count_orbit_for(orbits[node], current + 1)

    total = 0
    for child in orbits:
        total += count_orbit_for(child)

    return total


def test_count_orbits():
    test_input = [i.split(")") for i in """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
""".strip().split("\n")]

    count_orbits(test_input)


# Part 1
print(count_orbits(read_question_input()))


def steps_to_santa(_input: List[List[str]]):
    orbits = {child: parent for parent, child in _input}

    def get_parents(node: str, parents, current=0):
        if node not in orbits:
            return parents
        parents[orbits[node]] = current + 1
        return get_parents(orbits[node], parents, current + 1)

    my_parents = get_parents("YOU", {})
    santa_parents = get_parents("SAN", {})

    common_parents = set(my_parents.keys()) & set(santa_parents.keys())
    return min(my_parents[p] + santa_parents[p] for p in common_parents) - 2


# part 2
print(steps_to_santa(read_question_input()))
