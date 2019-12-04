from typing import List

question_input = "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,1,6,19,23,1,10," \
                 "23,27,2,27,13,31,1,31,6,35,2,6,35,39,1,39,5,43,1,6,43,47," \
                 "2,6,47,51,1,51,5,55,2,55,9,59,1,6,59,63,1,9,63,67,1,67,10," \
                 "71,2,9,71,75,1,6,75,79,1,5,79,83,2,83,10,87,1,87,5,91,1,91," \
                 "9,95,1,6,95,99,2,99,10,103,1,103,5,107,2,107,6,111,1,111,5," \
                 "115,1,9,115,119,2,119,10,123,1,6,123,127,2,13,127,131,1,131," \
                 "6,135,1,135,10,139,1,13,139,143,1,143,13,147,1,5,147,151,1," \
                 "151,2,155,1,155,5,0,99,2,0,14,0"


def solution_1(array: List[int], noun: int = None, verb: int = None):
    if noun is not None:
        array[1] = noun
    if verb is not None:
        array[2] = verb

    for i in range(0, len(array), 4):
        if array[i] == 99:
            break

        command, index1, index2, output = array[i:i + 4]

        if command == 1:
            array[output] = array[index1] + array[index2]
        elif command == 2:
            array[output] = array[index1] * array[index2]
        else:
            raise ValueError(f"index {i}. {array[i:i + 4]}")

    return array[0]


def run_1():
    def to_ints(inp: str):
        return list(map(int, inp.split(",")))

    for string, expected in [("1,1,1,4,99,5,6,0,99", 30),
                             ("1,9,10,3,2,3,11,0,99,30,40,50", 3500),
                             ("1,0,0,0,99", 2),
                             ("2,3,0,3,99", 2)]:
        assert solution_1(to_ints(string)) == expected

    return solution_1(to_ints(question_input), 12, 2)


def run_2():
    for i in range(99):
        for j in range(99):
            _input = list(map(int, question_input.split(",")))
            if solution_1(_input, i, j) == 19690720:
                return i * 100 + j
