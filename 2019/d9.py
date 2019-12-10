from enum import Enum, auto
from typing import Dict, Union


def read_input():
    with open('d9.txt') as f:
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


class CodeRunner:
    def __init__(self, instruction: Union[Dict[int, int], str], input_: int = 0):
        if isinstance(instruction, str):
            self.instruction = {i: int(j) for i, j in enumerate(instruction.strip().split(","))}
        else:
            assert isinstance(instruction, dict)
            self.instruction = instruction

        self._relative_base = 0
        self.output = []
        self.execute(input_)

    def execute(self, input_: int):
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
                self.instruction[p1] = input_
                p += 2

            elif op == Operation.OUTPUT:
                p1 = self.get_index(p, 1)[0]
                self.output.append(self.instruction.get(p1, 0))
                print(self.instruction.get(p1, 0))
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


part1 = CodeRunner(read_input(), 1)
part2 = CodeRunner(read_input(), 2)
