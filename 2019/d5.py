q_input = "3,225,1,225,6,6,1100,1,238,225,104,0,1101,90,60,224,1001,224,-150,224,4,224,1002,223,8,223,1001,224,7,224,1,224,223,223,1,57,83,224,1001,224,-99,224,4,224,1002,223,8,223,1001,224,5,224,1,223,224,223,1102,92,88,225,101,41,187,224,1001,224,-82,224,4,224,1002,223,8,223,101,7,224,224,1,224,223,223,1101,7,20,225,1101,82,64,225,1002,183,42,224,101,-1554,224,224,4,224,102,8,223,223,1001,224,1,224,1,224,223,223,1102,70,30,224,101,-2100,224,224,4,224,102,8,223,223,101,1,224,224,1,224,223,223,2,87,214,224,1001,224,-2460,224,4,224,1002,223,8,223,101,7,224,224,1,223,224,223,102,36,180,224,1001,224,-1368,224,4,224,1002,223,8,223,1001,224,5,224,1,223,224,223,1102,50,38,225,1102,37,14,225,1101,41,20,225,1001,217,7,224,101,-25,224,224,4,224,1002,223,8,223,101,2,224,224,1,224,223,223,1101,7,30,225,1102,18,16,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,7,226,226,224,102,2,223,223,1006,224,329,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,344,1001,223,1,223,8,677,226,224,1002,223,2,223,1005,224,359,101,1,223,223,107,677,677,224,1002,223,2,223,1006,224,374,101,1,223,223,7,677,226,224,1002,223,2,223,1006,224,389,101,1,223,223,108,677,226,224,1002,223,2,223,1005,224,404,101,1,223,223,1108,677,226,224,102,2,223,223,1005,224,419,101,1,223,223,8,226,677,224,102,2,223,223,1006,224,434,1001,223,1,223,1008,677,677,224,1002,223,2,223,1005,224,449,1001,223,1,223,1107,226,677,224,102,2,223,223,1006,224,464,101,1,223,223,107,226,677,224,1002,223,2,223,1006,224,479,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,494,1001,223,1,223,8,677,677,224,102,2,223,223,1006,224,509,1001,223,1,223,1108,677,677,224,102,2,223,223,1005,224,524,1001,223,1,223,1108,226,677,224,1002,223,2,223,1005,224,539,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,554,1001,223,1,223,1007,226,226,224,102,2,223,223,1005,224,569,1001,223,1,223,1008,226,226,224,102,2,223,223,1005,224,584,101,1,223,223,1007,677,677,224,1002,223,2,223,1005,224,599,1001,223,1,223,108,677,677,224,1002,223,2,223,1006,224,614,1001,223,1,223,1007,226,677,224,1002,223,2,223,1006,224,629,101,1,223,223,1008,677,226,224,102,2,223,223,1005,224,644,101,1,223,223,1107,226,226,224,1002,223,2,223,1005,224,659,1001,223,1,223,108,226,226,224,1002,223,2,223,1005,224,674,101,1,223,223,4,223,99,226"

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
    def __init__(self, instructions: str, input):
        self.instructions = [int(i) for i in instructions.split(",")]
        self.output = self.execute(input)

    def execute(self, input: int):
        p = 0
        output = None
        while p < len(self.instructions):
            op = self.instructions[p]
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
                self.save_value(out, input)
                p += 2

            elif op % 100 == INSTRUCTION["OUTPUT"]:
                out = self.get_parameter(p + 1, MODE["IMMEDIATE"])
                output = self.instructions[out]
                p += 2

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
                return output
            else:
                raise ValueError(f"Unknown op: {op}")

        return output

    def get_parameter(self, pos: int, mode: int):
        if mode == MODE["POSITION"]:
            return self.instructions[self.instructions[pos]]
        elif mode == MODE["IMMEDIATE"]:
            return self.instructions[pos]
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
        self.instructions[pos] = value


s = Solution(q_input, 1)
print(s.output)

s = Solution(q_input, 5)
print(s.output)
