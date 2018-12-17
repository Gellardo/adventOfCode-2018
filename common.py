#!/usr/bin/env python

import requests
import os
import itertools

def Input(day):
    if not os.path.exists(f'day{day}.input'):
        print(f'downloading input file for day {day}')
        with open('cookie') as f:
            cookie = f.read().strip()
        resp = requests.get(f'https://adventofcode.com/2018/day/{day}/input',
                            cookies={'session': cookie})
        if resp.status_code == 200:
            with open(f'day{day}.input', 'w') as f:
                f.write(resp.text)
        else:
            print(f'Coockie might be expired: {res.status_code} {res.reason}')
    with open(f'day{day}.input') as f:
        # discard the last line, since it is empty
        return f.read().split('\n')[:-1]
iterable_add = lambda xs,ys: tuple(x + y for x, y in itertools.zip_longest(xs, ys))
