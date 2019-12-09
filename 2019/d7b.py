from itertools import permutations

from typing import List, Optional

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


class Amplifier:
    def __init__(self, instructions, phase):
        self.instructions = instructions
        self._p = 0
        self._queue = [phase]

    def __len__(self):
        return len(self.instructions)

    def __getitem__(self, item):
        return self.instructions[item]

    def __setitem__(self, key: int, value: int):
        self.instructions[key] = value

    def run(self, output: int) -> Optional[int]:
        self._queue.append(output)
        p = self._p
        while p < len(self):
            op = self[p]
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
                self.save_value(out, self._queue.pop(0))
                p += 2

            elif op % 100 == INSTRUCTION["OUTPUT"]:
                pos = self.get_parameter(p + 1, MODE["IMMEDIATE"])
                output = self.get_parameter(pos, MODE["IMMEDIATE"])
                p += 2

                self._p = p
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

        self._p = p
        return output

    def get_parameter(self, pos: int, mode: int):
        if mode == MODE["POSITION"]:
            return self[self[pos]]
        elif mode == MODE["IMMEDIATE"]:
            return self[pos]
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
        self[pos] = value


class Solution:
    def __init__(self, instructions: str, phase_options: List[int]):
        self._instructions = instructions
        self._results = {}
        for inputs in permutations(phase_options):
            self._results[self.solve(inputs)] = inputs

    @property
    def best_results(self):
        best_output = max(self._results.keys())
        return best_output, self._results[best_output]

    def solve(self, inputs: List[int]):
        count = 0
        output = 0
        amplifiers = [Amplifier(self.instructions, phase) for phase in inputs]
        thrust = None

        while True:
            for amp in amplifiers:
                output = amp.run(output)
                if output is None:
                    break
                count += 1

            if thrust is None and output is None:
                raise RuntimeError("Thrust and output are both none")
            elif thrust is None:
                thrust = output
            elif output is None:
                return thrust
            elif output > thrust:
                thrust = output

            if count > 5000:
                raise RuntimeError("Could not find solution")

    @property
    def instructions(self):
        return [int(i) for i in self._instructions.split(",")]


def test_solution_for_part_2():
    for test_input, thrust, phase in [
        ("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5", 139629729,
         (9, 8, 7, 6, 5)),
        ("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,"
         "53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10",
         18216, (9, 7, 8, 5, 6))
    ]:
        sol = Solution(test_input, [*range(5, 10)])
        assert thrust == sol.best_results[0]
        assert phase == sol.best_results[1]


test_solution_for_part_2()
print(Solution(q_input, [*range(5, 10)]).best_results)