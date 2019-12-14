from enum import Enum
from typing import Dict, Union


def read_input():
    with open('d13.txt') as f:
        return {i: int(j) for i, j in enumerate(f.read().strip().split(","))}


class Operation(Enum):
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

    @classmethod
    def get_operation(cls, inst: int):
        return cls._value2member_map_[inst % 100]


class Mode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

    @classmethod
    def get_modes(cls, inst: int):
        return [cls._value2member_map_[inst // (10 ** (i + 2)) % 10] for i in range(3)]


class Tile(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

    @classmethod
    def get_tile(cls, value: int):
        return cls._value2member_map_[value]


class GameStatus:
    def __init__(self):
        self.paddle_position = 0
        self.ball_position = 0
        self.score = 0

    @property
    def joystick_direction(self):
        if self.paddle_position == self.ball_position:
            return 0  # don't move
        elif self.paddle_position > self.ball_position:
            return -1  # paddle is to the right of the ball, should move left towards the ball
        else:
            return 1  # paddle is to the left of the ball, should move right towards the ball


class GameRunner:
    def __init__(self, instruction: Union[Dict[int, int], str]):
        if isinstance(instruction, str):
            self.instruction = {i: int(j) for i, j in enumerate(instruction.strip().split(","))}
        else:
            assert isinstance(instruction, dict)
            self.instruction = instruction

        self._relative_base = 0

        self._output = []
        self._status = GameStatus()

        self.execute()

    @property
    def score(self):
        return self._status.score

    def execute(self):
        p = 0

        while p in self.instruction:
            op = Operation.get_operation(self.instruction[p])

            if op == Operation.ADD:
                p1, p2, p3 = self.get_index(p, 3)
                self.instruction[p3] = self.instruction.get(p1, 0) + self.instruction.get(p2, 0)
                p += 4

            elif op == Operation.MULTIPLY:
                p1, p2, p3 = self.get_index(p, 3)
                self.instruction[p3] = self.instruction.get(p1, 0) * self.instruction.get(p2, 0)
                p += 4

            elif op == Operation.INPUT:
                p1 = self.get_index(p, 1)[0]
                self.instruction[p1] = self._status.joystick_direction
                p += 2

            elif op == Operation.OUTPUT:
                p1 = self.get_index(p, 1)[0]
                self._output.append(self.instruction.get(p1, 0))
                p += 2
                if len(self._output) == 3:
                    self._process_output()

            elif op == Operation.JUMP_IF_TRUE:
                p1, p2 = self.get_index(p, 2)
                if self.instruction.get(p1) > 0:
                    p = self.instruction.get(p2, 0)
                else:
                    p += 3

            elif op == Operation.JUMP_IF_FALSE:
                p1, p2 = self.get_index(p, 2)
                if self.instruction.get(p1) == 0:
                    p = self.instruction.get(p2, 0)
                else:
                    p += 3

            elif op == Operation.LESS_THAN:
                p1, p2, p3 = self.get_index(p, 3)
                self.instruction[p3] = 1 if self.instruction.get(p1, 0) < self.instruction.get(p2, 0) else 0
                p += 4

            elif op == Operation.EQUAL_TO:
                p1, p2, p3 = self.get_index(p, 3)
                self.instruction[p3] = 1 if self.instruction.get(p1, 0) == self.instruction.get(p2, 0) else 0
                p += 4

            elif op == Operation.INCREASE_RELATIVE_BASE:
                p1 = self.get_index(p, 1)[0]
                self._relative_base += self.instruction.get(p1, 0)
                p += 2

            elif op == Operation.HALT:
                return

    def get_index(self, pos: int, num_index: int):
        modes = Mode.get_modes(self.instruction[pos])
        index = []
        for i in range(num_index):
            p = pos + i + 1
            if modes[i] == Mode.POSITION:
                index.append(self.instruction.get(p, 0))
            elif modes[i] == Mode.IMMEDIATE:
                index.append(p)
            elif modes[i] == Mode.RELATIVE:
                index.append(self.instruction.get(p, 0) + self._relative_base)

        return index

    def _process_output(self):
        x, y, value = self._output
        if x == -1 and y == 0:
            self._status.score = value
        else:
            tile = Tile.get_tile(value)
            if tile == Tile.PADDLE:
                self._status.paddle_position = x
            elif tile == Tile.BALL:
                self._status.ball_position = x

        self._output.clear()


def part_2():
    input_ = read_input()
    input_[0] = 2

    runner = GameRunner(input_)
    return runner.score


print(part_2())
