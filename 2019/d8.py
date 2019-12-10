from collections import Counter


def read_content():
    with open('d8.txt') as f:
        return f.read().strip()


def solve_part_1(width=25, height=6, content=read_content()):
    span = width * height

    counters = {}
    for i in range(0, len(content), span):
        c = Counter(content[i:i + span])
        counters[c['0']] = c

    max_counter = counters[min(counters)]
    return max_counter['1'] * max_counter['2']


print(solve_part_1())


def solve_part_2(width=25, height=6, content=read_content()):
    span = width * height

    layer = ["2"] * span
    for i in range(0, len(content), span):
        for j in range(span):
            if layer[j] == "2":
                layer[j] = content[i + j]

    layer = ''.join(layer).replace('0', ' ').replace('1', '#')

    for i in range(0, len(layer), width):
        print(layer[i: i + width])


solve_part_2()
