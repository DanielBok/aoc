import numpy as np


def read_input():
    with open('d16.txt') as f:
        return f.read()


def array_row(n: int, i: int):
    pattern = [0, 1, 0, -1]
    row = np.repeat(pattern, i + 1)
    if len(row) < n + 1:
        row = np.tile(row, n // 4 + 2)
    return row[1:n + 1].astype(int)


def pattern_array(n: int):
    result = np.zeros((n, n), np.int8)
    for i in range(n):
        result[:, i] = array_row(n, i)

    return result.astype(int)


def part1(input_value: str):
    vector = np.array([int(i) for i in input_value])
    arr = pattern_array(len(vector))

    for _ in range(100):
        vector = np.abs(vector @ arr) % 10

    return ''.join(str(i) for i in vector[:8])


def test_1():
    for input_value, expected in [
        ("80871224585914546619083218645595", "24176176"),
        ("19617804207202209144916044189917", "73745418"),
        ("69317163492948606335995924319873", "52432133"),
    ]:
        assert part1(input_value) == expected


test_1()
print(part1(read_input()))


def part2(input_value: str):
    skip = int(input_value[:7])
    vector = np.tile([int(i) for i in input_value], 10000)[skip:]
    vector = vector[::-1]

    for _ in range(100):
        for i in range(1, len(vector)):
            # this only works when skip > len(vector) / 2
            vector[i] = (vector[i] + vector[i - 1]) % 10

    return ''.join(str(i) for i in vector[::-1][:8])


def test_2():
    for input_value, expected in [
        ("03036732577212944063491565474664", "84462026"),
        ("02935109699940807407585447034323", "78725270"),
        ("03081770884921959731165446850517", "53553731"),
    ]:
        assert part2(input_value) == expected


test_2()
print(part2(read_input()))
