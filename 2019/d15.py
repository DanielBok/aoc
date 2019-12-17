from typing import Dict, List, Union

WALL = 0
ROAD = 1
GOAL = 2

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4


def read_input():
    with open('d15.txt') as f:
        return {i: int(j) for i, j in enumerate(f.read().strip().split(","))}


class IntCodeRunner:
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUAL_TO = 8
    INCREASE_RELATIVE_BASE = 9
    HALT = 99

    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

    def __init__(self, instruction: Union[Dict[int, int], str], inputs: List[int] = None, relative_base=0):
        if isinstance(instruction, str):
            self.instruction = {i: int(j) for i, j in enumerate(instruction.strip().split(","))}
        else:
            assert isinstance(instruction, dict)
            self.instruction = instruction

        self._inputs = [] if inputs is None else inputs
        self.relative_base = relative_base
        self._output = []
        self._terminated = False

    def execute(self, new_inputs: List[int] = None):
        p = 0
        if isinstance(new_inputs, list):
            self._inputs.extend(new_inputs)

        while not self._terminated and p in self.instruction:
            op = self.instruction[p] % 100

            if op == self.ADD:
                p1, p2, p3 = self.get_index(p, 3)
                self.instruction[p3] = self.instruction[p1] + self.instruction[p2]
                p += 4

            elif op == self.MULTIPLY:
                p1, p2, p3 = self.get_index(p, 3)
                self.instruction[p3] = self.instruction[p1] * self.instruction[p2]
                p += 4

            elif op == self.INPUT:
                p1 = self.get_index(p, 1)[0]
                self.instruction[p1] = self._inputs.pop(0)
                p += 2

            elif op == self.OUTPUT:
                p1 = self.get_index(p, 1)[0]
                self._output.append(self.instruction[p1])
                p += 2

            elif op == self.JUMP_IF_TRUE:
                p1, p2 = self.get_index(p, 2)
                p = self.instruction[p2] if self.instruction[p1] > 0 else p + 3

            elif op == self.JUMP_IF_FALSE:
                p1, p2 = self.get_index(p, 2)
                p = self.instruction[p2] if self.instruction[p1] == 0 else p + 3

            elif op == self.LESS_THAN:
                p1, p2, p3 = self.get_index(p, 3)
                self.instruction[p3] = 1 if self.instruction[p1] < self.instruction[p2] else 0
                p += 4

            elif op == self.EQUAL_TO:
                p1, p2, p3 = self.get_index(p, 3)
                self.instruction[p3] = 1 if self.instruction[p1] == self.instruction[p2] else 0
                p += 4

            elif op == self.INCREASE_RELATIVE_BASE:
                p1 = self.get_index(p, 1)[0]
                self.relative_base += self.instruction[p1]
                p += 2

            elif op == self.HALT:
                break

            if len(self._output) > 0:
                break

        return self._output

    def get_index(self, pos: int, num_index: int):
        modes = self._get_mode(self.instruction[pos])
        index = []
        for i in range(num_index):
            p = pos + i + 1
            if modes[i] == self.POSITION:
                index.append(self.instruction.get(p, 0))
            elif modes[i] == self.IMMEDIATE:
                index.append(p)
            elif modes[i] == self.RELATIVE:
                index.append(self.instruction.get(p, 0) + self.relative_base)

        return index

    @classmethod
    def _get_mode(cls, inst: int):
        return [inst // (10 ** (i + 2)) % 10 for i in range(3)]


def part1():
    directions = [NORTH, SOUTH, WEST, EAST]
    finish = False
    paths = {'': []}
    current_path = ''
    shortest_path = ''
    state = {'': (read_input(), 0)}
    reached_goal = False

    while not finish:
        used_directions = paths[current_path]
        next_input = [i for i in directions if i not in used_directions][0]
        used_directions.append(next_input)

        instructions, base = state[current_path]
        runner = IntCodeRunner({**instructions}, relative_base=base)

        out = runner.execute([next_input]).pop()
        if out == WALL:
            if len(used_directions) == len(directions):
                # checked all possible paths from current position and met deadend
                # time to return to free area
                for past_path, past_directions in paths.items():
                    if len(past_directions) != len(directions):
                        current_path = past_path
                        break
                else:
                    finish = True

        elif out in (GOAL, ROAD):
            current_path += str(next_input)
            state[current_path] = ({**runner.instruction}, runner.relative_base)

            reverse_direction = {
                NORTH: SOUTH,
                SOUTH: NORTH,
                WEST: EAST,
                EAST: WEST
            }[next_input]
            paths[current_path] = [reverse_direction]  # prevent backtracking

        else:
            raise ValueError(f"unknown output: {out}")

        if out == GOAL:
            shortest_path = current_path
            reached_goal = True

    if reached_goal:
        return len(shortest_path)
    else:
        raise RuntimeError("Never found goal (oxygen leak)")


print(part1())


def part2():
    directions = [NORTH, SOUTH, WEST, EAST]
    finish = False

    curr_pos = (0, 0)
    state = {curr_pos: (read_input(), 0)}
    paths = {curr_pos: []}
    grid = {curr_pos}
    start = None

    while not finish:
        used_directions = paths[curr_pos]
        next_input = [i for i in directions if i not in used_directions][0]
        used_directions.append(next_input)

        instructions, base = state[curr_pos]
        runner = IntCodeRunner({**instructions}, relative_base=base)

        out = runner.execute([next_input]).pop()
        if out == WALL:
            if len(used_directions) == len(directions):
                # checked all possible paths from current position and met deadend
                # time to return to free area
                for past_position, past_directions in paths.items():
                    if len(past_directions) != len(directions):
                        curr_pos = past_position
                        break
                else:
                    finish = True

        elif out in (GOAL, ROAD):
            if next_input == NORTH: curr_pos = (curr_pos[0], curr_pos[1] + 1)
            if next_input == SOUTH: curr_pos = (curr_pos[0], curr_pos[1] - 1)
            if next_input == EAST: curr_pos = (curr_pos[0] + 1, curr_pos[1])
            if next_input == WEST: curr_pos = (curr_pos[0] - 1, curr_pos[1])

            state[curr_pos] = ({**runner.instruction}, runner.relative_base)

            reverse_direction = {
                NORTH: SOUTH,
                SOUTH: NORTH,
                WEST: EAST,
                EAST: WEST
            }[next_input]
            paths[curr_pos] = [reverse_direction]  # prevent backtracking
            grid.add(curr_pos)

        else:
            raise ValueError(f"unknown output: {out}")

        if out == GOAL:
            start = curr_pos

    count = 0
    boundary = [start]
    while len(grid) > 0:
        new_boundaries = []
        for x, y in boundary:
            for new_pos in [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]:
                if new_pos in grid:
                    grid.remove(new_pos)
                    new_boundaries.append(new_pos)

        boundary = new_boundaries
        count += 1

    return count


print(part2())
