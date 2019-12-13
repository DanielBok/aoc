from enum import Enum, auto
from typing import Dict, Tuple, Union


def read_input():
    with open('d11.txt') as f:
        return {i: int(j) for i, j in enumerate(f.read().strip().split(","))}


class Operation(Enum):
    ADD = auto()
    MULTIPLY = auto()
    INPUT = auto()
    OUTPUT = auto()
    JUMP_IF_TRUE = auto()
    JUMP_IF_FALSE = auto()
    LESS_THAN = auto()
    EQUAL_TO = auto()
    INCREASE_RELATIVE_BASE = auto()
    HALT = auto()

    @staticmethod
    def get_operation(inst):
        return {
            1: Operation.ADD,
            2: Operation.MULTIPLY,
            3: Operation.INPUT,
            4: Operation.OUTPUT,
            5: Operation.JUMP_IF_TRUE,
            6: Operation.JUMP_IF_FALSE,
            7: Operation.LESS_THAN,
            8: Operation.EQUAL_TO,
            9: Operation.INCREASE_RELATIVE_BASE,
            99: Operation.HALT,
        }[inst % 100]


class Mode(Enum):
    POSITION = auto()
    IMMEDIATE = auto()
    RELATIVE = auto()

    @staticmethod
    def get_modes(inst: int):
        return [{
                    0: Mode.POSITION,
                    1: Mode.IMMEDIATE,
                    2: Mode.RELATIVE,
                }[inst // (10 ** (i + 2)) % 10] for i in range(3)]


class Color(Enum):
    BLACK = 0
    WHITE = 1


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Grid:
    def __init__(self, initial_panel: Color):
        self.grid = {(0, 0): initial_panel}

    def __getitem__(self, item: Tuple[int, int]) -> Color:
        if item not in self.grid:
            self.grid[item] = Color.BLACK
        return self.grid[item]

    def __setitem__(self, key: Tuple[int, int], value: Color):
        self.grid[key] = value

    def __len__(self):
        return len(self.grid)


class Robot:
    def __init__(self):
        self._x, self._y = 0, 0
        self.face = Direction.UP

    @property
    def coordinate(self):
        return self._x, self._y

    def turn(self, direction: Direction):
        of, oc = self.face, self.coordinate
        if self.face == Direction.UP:
            self._y += (-1 if direction == Direction.LEFT else 1)
            self.face = Direction.LEFT if direction == Direction.LEFT else Direction.RIGHT
        elif self.face == Direction.DOWN:
            self._y += (1 if direction == Direction.LEFT else -1)
            self.face = Direction.RIGHT if direction == Direction.LEFT else Direction.LEFT
        elif self.face == Direction.LEFT:
            self._x += (1 if direction == Direction.LEFT else -1)
            self.face = Direction.DOWN if direction == Direction.LEFT else Direction.UP
        elif self.face == Direction.RIGHT:
            self._x += (-1 if direction == Direction.LEFT else 1)
            self.face = Direction.UP if direction == Direction.LEFT else Direction.DOWN
        else:
            raise RuntimeError


class Action(Enum):
    MOVE = auto()
    PAINT = auto()


class Painter:
    def __init__(self, instruction: Union[Dict[int, int], str], initial_panel=Color.BLACK):
        if isinstance(instruction, str):
            self.instruction = {i: int(j) for i, j in enumerate(instruction.strip().split(","))}
        else:
            assert isinstance(instruction, dict)
            self.instruction = instruction

        self.grid = Grid(initial_panel)
        self.robot = Robot()
        self._relative_base = 0
        self.execute()

    def execute(self):
        p = 0
        num_instructions = 0

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
                self.instruction[p1] = self.grid[self.robot.coordinate].value
                p += 2

            elif op == Operation.OUTPUT:
                p1 = self.get_index(p, 1)[0]
                output = self.instruction[p1]
                if num_instructions % 2 == 0:
                    self.grid[self.robot.coordinate] = Color.BLACK if output == 0 else Color.WHITE
                else:
                    self.robot.turn(Direction.LEFT if output == 0 else Direction.RIGHT)

                num_instructions += 1
                p += 2

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
        inst = self.instruction[pos]
        modes = Mode.get_modes(inst)
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

    def draw(self):
        letter_map = {
            Color.WHITE: '█',
            Color.BLACK: ' '
        }
        grid = self.grid.grid
        max_x = max([x[0] for x in grid.keys()]) + 1
        max_y = max([x[1] for x in grid.keys()]) + 1

        for x in range(max_x):
            print(''.join(letter_map[grid.get((x, y), Color.BLACK)] for y in range(max_y)))


painter = Painter(read_input())
print(len(painter.grid))

painter = Painter(read_input(), Color.WHITE)
painter.draw()
