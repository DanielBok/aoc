from itertools import permutations

from typing import List

q_input = "3,8,1001,8,10,8,105,1,0,0,21,42,67,84,109,122,203,284,365,446,99999,3,9,1002,9,3,9,1001,9,5,9,102,4,9,9,1001,9,3,9,4,9,99,3,9,1001,9,5,9,1002,9,3,9,1001,9,4,9,102,3,9,9,101,3,9,9,4,9,99,3,9,101,5,9,9,1002,9,3,9,101,5,9,9,4,9,99,3,9,102,5,9,9,101,5,9,9,102,3,9,9,101,3,9,9,102,2,9,9,4,9,99,3,9,101,2,9,9,1002,9,3,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,99"

INSTRUCTION = {
    "ADD": 1,
    "MULTIPLY": 2,
    "INPUT": 3,
    "OUTPUT": 4,
    "JUMP_IF_TRUE": 5,
    "JUMP_IF_FALSE": 6,
    "LESS_THAN": 7,
    "EQUAL_TO": 8,
    "HALT": 99
}

MODE = {
    "POSITION": 0,
    "IMMEDIATE": 1,
}


class Solution:
    def __init__(self, instructions: str, phase_options: List[int]):
        self._instructions = instructions
        self._temp_instructions: List[int] = []

        self._results = {}
        for inputs in permutations(phase_options):
            self._results[self.solve(inputs)] = inputs

    @property
    def best_results(self):
        best_output = max(self._results.keys())
        return best_output, self._results[best_output]

    def solve(self, inputs: List[int]):
        output = 0
        for i in inputs:
            output = self.execute(i, output)

        return output

    @property
    def instructions(self):
        return [int(i) for i in self._instructions.split(",")]

    def execute(self, phase: int, output: int):
        p = 0
        self._temp_instructions = self.instructions

        while p < len(self.instructions):
            assert output is not None
            op = self._temp_instructions[p]
            if op % 100 == INSTRUCTION["ADD"]:
                p1 = self.get_parameter(p + 1, self.get_mode(op, 0))
                p2 = self.get_parameter(p + 2, self.get_mode(op, 1))
                out = self.get_parameter(p + 3, MODE["IMMEDIATE"])
                self.save_value(out, p1 + p2)
                p += 4

            elif op % 100 == INSTRUCTION["MULTIPLY"]:
                p1 = self.get_parameter(p + 1, self.get_mode(op, 0))
                p2 = self.get_parameter(p + 2, self.get_mode(op, 1))
                out = self.get_parameter(p + 3, MODE["IMMEDIATE"])
                self.save_value(out, p1 * p2)
                p += 4

            elif op % 100 == INSTRUCTION["INPUT"]:
                out = self.get_parameter(p + 1, MODE["IMMEDIATE"])
                self.save_value(out, phase if phase is not None else output)
                phase = None
                p += 2

            elif op % 100 == INSTRUCTION["OUTPUT"]:
                pos = self.get_parameter(p + 1, MODE["IMMEDIATE"])
                output = self.get_parameter(pos, MODE["IMMEDIATE"])
                p += 2

                return output

            elif op % 100 == INSTRUCTION["JUMP_IF_TRUE"]:
                p1 = self.get_parameter(p + 1, self.get_mode(op, 0))
                out = self.get_parameter(p + 2, self.get_mode(op, 1))

                if p1 != 0:
                    p = out
                else:
                    p += 3

            elif op % 100 == INSTRUCTION["JUMP_IF_FALSE"]:
                p1 = self.get_parameter(p + 1, self.get_mode(op, 0))
                out = self.get_parameter(p + 2, self.get_mode(op, 1))

                if p1 == 0:
                    p = out
                else:
                    p += 3

            elif op % 100 == INSTRUCTION["LESS_THAN"]:
                p1 = self.get_parameter(p + 1, self.get_mode(op, 0))
                p2 = self.get_parameter(p + 2, self.get_mode(op, 1))
                out = self.get_parameter(p + 3, MODE["IMMEDIATE"])
                self.save_value(out, 1 if p1 < p2 else 0)
                p += 4

            elif op % 100 == INSTRUCTION["EQUAL_TO"]:
                p1 = self.get_parameter(p + 1, self.get_mode(op, 0))
                p2 = self.get_parameter(p + 2, self.get_mode(op, 1))
                out = self.get_parameter(p + 3, MODE["IMMEDIATE"])
                self.save_value(out, 1 if p1 == p2 else 0)
                p += 4

            elif op % 100 == INSTRUCTION["HALT"]:
                return None
            else:
                raise ValueError(f"Unknown op: {op}")

        return None

    def get_parameter(self, pos: int, mode: int):
        if mode == MODE["POSITION"]:
            return self._temp_instructions[self._temp_instructions[pos]]
        elif mode == MODE["IMMEDIATE"]:
            return self._temp_instructions[pos]
        else:
            raise ValueError(f"Unknown mode: {mode}")

    @staticmethod
    def get_mode(op: int, index: int):
        op = str(op)[:-2][::-1]
        while len(op) < 2:
            op += "0"

        if op[index] == "0":
            return MODE["POSITION"]
        else:
            return MODE["IMMEDIATE"]

    def save_value(self, pos: int, value: int):
        self._temp_instructions[pos] = value


def test_solution_for_part_1():
    for test_input, thrust, phase in [
        ("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", 43210, (4, 3, 2, 1, 0)),
        ("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0", 54321, (0, 1, 2, 3, 4)),
        ("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0", 65210,
         (1, 0, 4, 3, 2))
    ]:
        sol = Solution(test_input, [*range(5)])
        assert thrust == sol.best_results[0]
        assert phase == sol.best_results[1]


test_solution_for_part_1()
print(Solution(q_input, [*range(5)]).best_results)
