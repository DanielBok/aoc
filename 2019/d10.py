import numpy as np
from collections import defaultdict

q_input = """
#..#....#...#.#..#.......##.#.####
#......#..#.#..####.....#..#...##.
.##.......#..#.#....#.#..#.#....#.
###..#.....###.#....##.....#...#..
...#.##..#.###.......#....#....###
.####...##...........##..#..#.##..
..#...#.#.#.###....#.#...##.....#.
......#.....#..#...##.#..##.#..###
...###.#....#..##.#.#.#....#...###
..#.###.####..###.#.##..#.##.###..
...##...#.#..##.#............##.##
....#.##.##.##..#......##.........
.#..#.#..#.##......##...#.#.#...##
.##.....#.#.##...#.#.#...#..###...
#.#.#..##......#...#...#.......#..
#.......#..#####.###.#..#..#.#.#..
.#......##......##...#..#..#..###.
#.#...#..#....##.#....#.##.#....#.
....#..#....##..#...##..#..#.#.##.
#.#.#.#.##.#.#..###.......#....###
...#.#..##....###.####.#..#.#..#..
#....##..#...##.#.#.........##.#..
.#....#.#...#.#.........#..#......
...#..###...#...#.#.#...#.#..##.##
.####.##.#..#.#.#.#...#.##......#.
.##....##..#.#.#.......#.....####.
#.##.##....#...#..#.#..###..#.###.
...###.#..#.....#.#.#.#....#....#.
......#...#.........##....#....##.
.....#.....#..#.##.#.###.#..##....
.#.....#.#.....#####.....##..#....
.####.##...#.......####..#....##..
.#.#.......#......#.##..##.#.#..##
......##.....##...##.##...##......
"""


def part1(input_: str):
    arr = np.array([[0 if i == "." else 1 for i in row] for row in input_.strip().split('\n')])
    row, col = np.indices(arr.shape)
    mask = arr == 1

    asteroids = np.dstack((col[mask], row[mask])).squeeze().astype(float).view(np.complex)

    highest, location = 0, asteroids[0]
    for i, coord in enumerate(asteroids):
        other_asteroids = np.concatenate([asteroids[:i], asteroids[i + 1:]])
        radians = np.angle(other_asteroids - coord)

        num_asteroids_spotted = len(np.unique(radians))
        if num_asteroids_spotted > highest:
            highest = num_asteroids_spotted
            location = coord

    return highest, location.view(float).astype(int)


def test_part_1():
    for _map, exp in [
        ("""
.#..#
.....
#####
....#
...##
""", 8),
        ("""
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
""", 33),
        ("""
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
""", 35),
        ("""
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..""", 41),
        ("""
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""", 210)
    ]:
        num_asteroids, _ = part1(_map)
        assert num_asteroids == exp


test_part_1()
print(part1(q_input)[0])


def part2(input_, pos):
    arr = np.array([[0 if i == "." else 1 for i in row] for row in input_.strip().split('\n')])
    row, col = np.indices(arr.shape)
    mask = arr == 1

    asteroids = np.dstack((col[mask] - pos[0], row[mask] - pos[1])).squeeze().astype(float).view(np.complex)

    angle = np.angle(asteroids, deg=True).squeeze()
    angle = (angle + 450) % 360
    radius = np.linalg.norm(asteroids, axis=1)
    coords = np.stack((angle, radius, np.arange(len(angle))), axis=1)

    sorted_coords = coords[np.lexsort((angle, radius))]
    unique_angles = np.sort(np.unique(angle))

    grouped_coords = defaultdict(list)
    for c in sorted_coords:
        grouped_coords[c[0]].append(c)

    count = 0
    while True:
        for a in unique_angles:
            if len(grouped_coords[a]) > 0:
                *_, index = grouped_coords[a].pop(0)
                count += 1

                if count == 200:
                    location = asteroids[int(index)].view(float) + pos
                    return int(location[0] * 100 + location[1])


def test_part_2():
    test_input = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
    assert part2(test_input, (11, 13)) == 802


test_part_2()
part2(q_input, part1(q_input)[1])
