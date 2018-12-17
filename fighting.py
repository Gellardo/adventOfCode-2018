#!/usr/bin/env python
from common import Input,iterable_add
import time
import sys
from collections import namedtuple,deque

debug=len(sys.argv)==1

Position = namedtuple('Position', ['y','x'])
def position_add(one, two):
    return Position(one.y+two.y, one.x+two.x)


class Cave():
    def __init__(self, cave_map, atk=3):
        self.map = []
        for y, l in enumerate(cave_map):
            self.map.append([])
            for x, c in enumerate(l):
                if c in "EG":
                    c = Unit(y, x, c, atk if c == "E" else 3)
                self.map[y].append(c)
        self.initial_elves = self.elves()

    def __str__(self):
        for y, l in enumerate(self.map):
            for x, c in enumerate(l):
                print(c, end='')
            print([c for c in l if type(c) is Unit])
        return ""

    def __getitem__(self, pos):
        return self.map[pos.y][pos.x]
    def __setitem__(self, pos, value):
        self.map[pos.y][pos.x] = value

    def elves(self):
        return len([1 for l in self.map for c in l if type(c) is Unit and c.faction == 'E'])


    def get_units(self):
        return [c for l in self.map for c in l if type(c) is Unit]

    def neighbors(self, pos, mode='any'):
        for d in [Position(-1,0), Position(0,-1), Position(0,1), Position(1,0)]:
            p = position_add(pos, d)
            if mode == 'any' and self[p] != '#':
                yield p
            elif mode == 'enemy' and type(self[p]) is Unit and self[p].faction != self[pos].faction:
                yield p


class Unit():
    def __init__(self,y,x,faction,atk):
        self.pos = Position(y,x)
        self.faction = faction
        if faction == 'E':
            self.pretty = f"\033[32;12m{faction}\033[92;40m"
        elif faction == 'G':
            self.pretty = f"\033[91;41m{faction}\033[92;40m"
        self.atk = atk
        self.hp = 200

    def __str__(self):
        return self.pretty
    def __repr__(self):
        return f"Unit({self.pretty},{self.hp})"

    def won(self, units):
        return all(map(lambda o: self.faction == o.faction, units))

    def plan(self, cave):
        # breadth first search using reading order, so that the first found
        # enemy (and the path to it) is the right one according to the rules
        # set by the puzzle
        visited = {} # contains (node, came_from)
        to_visit = deque([(self.pos,self.pos)])
        while len(to_visit) > 0:
            curr, parent = to_visit.popleft()
            if curr in visited:
                continue
            visited[curr] = parent
            for n in cave.neighbors(curr):
                if type(cave[n]) is Unit:
                    if cave[n].faction != self.faction:
                        # reconstruct the path leading to this cell
                        result = curr
                        while visited[result] != self.pos:
                            result = visited[result]
                        return result
                    else:
                        # we can't walk over friendly units
                        continue
                if n not in visited:
                    to_visit.append((n, curr))
        return self.pos

    def move(self, cave, pos):
        #print(f"move from {self.pos} to {pos}")
        cave[self.pos] = '.'
        self.pos = pos
        cave[self.pos] = self

    def plan_and_move(self, cave):
        if self.hp <= 0:
            return
        self.move(cave, self.plan(cave))

    def get_hit(self, dmg, cave):
        self.hp -= dmg
        if self.hp <= 0:
            cave[self.pos] = '.'

    def attack(self, cave):
        if self.hp <= 0:
            return
        targets = [cave[pos] for pos in cave.neighbors(self.pos, mode='enemy')]
        if len(targets) > 0:
            # reading order should be given by find_spaces
            min(targets,key=lambda u: u.hp).get_hit(self.atk,cave)


def print_cave_map(cave, rounds=-1):
    if not debug:
        return
    print(f'After round {rounds}\n\033[92;40m',end='')
    print(cave)


def simulate_fight(in_cave, sleep=0, intervention=False, round_limit=10**3):
    def fight(cave):
        full_rounds = 0
        while full_rounds <= round_limit:
            print_cave_map(cave, rounds=full_rounds)
            for unit in sorted(cave.get_units(), key=lambda u: u.pos):
                if unit.won(cave.get_units()):
                    return full_rounds * sum(map(lambda u: u.hp, cave.get_units()))
                unit.plan_and_move(cave)
                unit.attack(cave)
            full_rounds += 1
            time.sleep(sleep)
        return -1

    for elves_attack in range(3,200):
        cave = Cave(in_cave, atk=elves_attack)

        outcome = fight(cave)
        if elves_attack in [8,9,33,34]:
            print(f"atk={elves_attack:2d}: {cave.initial_elves} elves -> {cave.elves()} survivors")
        if not intervention or cave.initial_elves == cave.elves():
            return outcome
    return -1

assert simulate_fight("""\
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
""".split('\n')) == 47 * 590 == 27730
assert simulate_fight("""\
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######\
""".split('\n')) == 37 * 982 == 36334
assert simulate_fight("""\
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######\
""".split('\n')) == 46 * 859 == 39514
assert simulate_fight("""\
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######\
""".split('\n')) == 35 * 793 == 27755
assert simulate_fight("""\
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######\
""".split('\n')) == 54 * 536 == 28944
assert simulate_fight("""\
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########\
""".split('\n')) == 20 * 937 == 18740

print("Part 1:", simulate_fight(Input(15)))
print("Part 2 (minimise the necessary amount of damage for no elven casualties):", simulate_fight(Input(15), intervention=True))
