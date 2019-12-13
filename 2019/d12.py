import re
from math import gcd
from typing import List

q_input = """
<x=-7, y=-1, z=6>
<x=6, y=-9, z=-9>
<x=-12, y=2, z=-7>
<x=4, y=-17, z=-12>
""".strip()


class Velocity:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: "Velocity"):
        return Velocity(self.x + other.x,
                        self.y + other.y,
                        self.z + other.z)

    @property
    def energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


class Position:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def gravity_influence(self, others_moon: List["Moon"]):
        def _get_gravity_change(value: int, other: int):
            if value == other:
                return 0
            elif value > other:
                return -1
            else:
                return 1

        x, y, z = 0, 0, 0
        for moon in others_moon:
            x += _get_gravity_change(self.x, moon.position.x)
            y += _get_gravity_change(self.y, moon.position.y)
            z += _get_gravity_change(self.z, moon.position.z)

        return Velocity(x, y, z)

    def __add__(self, other: Velocity):
        return Position(self.x + other.x,
                        self.y + other.y,
                        self.z + other.z)

    @property
    def energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


class Moon:
    def __init__(self, x: int, y: int, z: int):
        self.velocity = Velocity()
        self.position = Position(x, y, z)

    def set_new_velocity(self, other_moons: List["Moon"]):
        velocity_change = self.position.gravity_influence(other_moons)
        self.velocity += velocity_change

    def set_new_position(self):
        self.position += self.velocity

    @property
    def energy(self):
        return self.position.energy * self.velocity.energy

    def __getitem__(self, item: str):
        if item.startswith('p'):
            return getattr(self.position, item[-1])
        else:
            return getattr(self.velocity, item[-1])


class System:
    def __init__(self, input_: str):
        self.moons = []
        for pos in re.findall(r"x=(-?\d+), y=(-?\d+), z=(-?\d+)", input_):
            self.moons.append(Moon(*[int(i) for i in pos]))

    def update_velocities(self):
        for moon in self.moons:
            moon.set_new_velocity(self.moons)
        return self

    def update_positions(self):
        for moon in self.moons:
            moon.set_new_position()
        return self

    @property
    def energy(self):
        return sum(moon.energy for moon in self.moons)

    def __iter__(self):
        for moon in self.moons:
            yield moon


def part_1(input_: str, steps: int):
    system = System(input_)
    for _ in range(steps):
        system.update_velocities() \
            .update_positions()

    return system.energy


def test_part_1():
    for input_, steps, expected in [
        ("""
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>""", 10, 179),
        ("""<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
        """, 100, 1940)
    ]:
        assert part_1(input_.strip(), steps) == expected


test_part_1()
print(part_1(q_input, 1000))


def part_2(input_: str):
    system = System(input_)

    x, y, z = 0, 0, 0
    steps = 0
    while True:
        system.update_velocities().update_positions()
        steps += 1

        if x == 0 and all(moon.velocity.x == 0 for moon in system):
            x = steps

        if y == 0 and all(moon.velocity.y == 0 for moon in system):
            y = steps

        if z == 0 and all(moon.velocity.z == 0 for moon in system):
            z = steps

        if x > 0 and y > 0 and z > 0:
            break

    lcm = x
    for i in (y, z):
        lcm *= (i // gcd(lcm, i))

    return lcm * 2


def test_part_2():
    for input_, expected in [
        ("""
    <x=-1, y=0, z=2>
    <x=2, y=-10, z=-7>
    <x=4, y=-8, z=8>
    <x=3, y=5, z=-1>""", 2772),
        ("""<x=-8, y=-10, z=0>
    <x=5, y=5, z=10>
    <x=2, y=-7, z=3>
    <x=9, y=-8, z=-3>
            """, 4686774924)
    ]:
        assert part_2(input_.strip()) == expected


test_part_2()
print(part_2(q_input))
