from typing import List, Tuple

import numpy as np


def read_input():
    with open('d3.txt') as f:
        eins, zwei = [i.strip() for i in f.readlines()]

    return eins, zwei


class Solution:
    def __init__(self, first: str, second: str, size=20000):
        self.first_path = self.form_path(first)
        self.second_path = self.form_path(second)
        self.start = size // 2, size // 2

        self.first_grid = self.form_grid(self.first_path, size)
        self.second_grid = self.form_grid(self.second_path, size)

    def solve(self):
        indices = np.indices(self.first_grid.shape)
        total = self.first_grid * self.second_grid
        return np.abs(indices[..., total == 1].T - self.start).sum(1).min()

    @staticmethod
    def form_path(path: str):
        return [(p[0], int(p[1:])) for p in path.split(",")]

    def form_grid(self, path: List[Tuple[str, int]], size: int):
        x, y = self.start
        grid = np.zeros([size, size])
        for direction, steps in path:
            if direction == "L":
                grid[x, y - steps:y + 1] = 1
                y -= steps
            elif direction == "R":
                grid[x, y: y + steps + 1] = 1
                y += steps
            elif direction == "U":
                grid[x - steps: x + 1, y] = 1
                x -= steps
            elif direction == "D":
                grid[x: x + steps + 1, y] = 1
                x += steps
            else:
                raise ValueError(f"Dir: {direction}")

        grid[self.start] = 0
        return grid


def test1():
    for left, right, grid_size, exp in [
        ("R8,U5,L5,D3", "U7,R6,D4,L4", 20, 6),
        ("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 500, 159),
        ("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 500, 135)
    ]:
        assert Solution(left, right, grid_size).solve() == exp


def solve1():
    return Solution(*read_input(), size=20000).solve()


class Solution2:
    def __init__(self, first: str, second: str, size=20000):
        self.first_path = self.form_path(first)
        self.second_path = self.form_path(second)
        self.start = size // 2, size // 2

        self.first_time_grid = self.form_grid(self.first_path, size)
        self.second_time_grid = self.form_grid(self.second_path, size)

    def solve(self):
        mask = (self.first_time_grid > 0) & (self.second_time_grid > 0)
        return min((self.first_time_grid + self.second_time_grid)[mask])

    @staticmethod
    def form_path(path: str):
        return [(p[0], int(p[1:])) for p in path.split(",")]

    def form_grid(self, path: List[Tuple[str, int]], size: int):
        x, y = self.start
        time_grid = np.zeros([size, size], int)

        time = 0
        for direction, steps in path:
            for _ in range(steps):
                time += 1
                if direction == "L":
                    y -= 1
                elif direction == "R":
                    y += 1
                elif direction == "U":
                    x -= 1
                elif direction == "D":
                    x += 1

                if time_grid[x, y] == 0:
                    time_grid[x, y] = time

        return time_grid


def test2():
    for left, right, grid_size, exp in [
        ("R8,U5,L5,D3", "U7,R6,D4,L4", 20, 30),
        ("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 500, 610),
        ("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 500, 410)
    ]:
        assert Solution2(left, right, grid_size).solve() == exp


def solve2():
    return Solution2(*read_input(), size=20000).solve()
