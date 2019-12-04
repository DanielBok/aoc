def solution_1(x):
    return x // 3 - 2


for v, exp in [(12, 2),
               (14, 2),
               (1969, 654),
               (100756, 33583)]:
    assert solution_1(v) == exp

with open('d1.txt') as f:
    print(sum([solution_1(int(line.strip())) for line in f.readlines()]))


def solution_2(x):
    fuel = x // 3 - 2
    if fuel <= 0:
        return 0
    return fuel + solution_2(fuel)


solution_2(100756)

for v, exp in [(12, 2),
               (14, 2),
               (1969, 966),
               (100756, 50346)]:
    assert solution_2(v) == exp


with open('d1.txt') as f:
    print(sum([solution_2(int(line.strip())) for line in f.readlines()]))
