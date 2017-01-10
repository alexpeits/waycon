# -*- coding: utf-8 -*-

import curses
import copy
import time
import sys

try:
    range = xrange
except NameError:
    pass

ON = '*'
OFF = ' '
DELAY = 1.0/10

directions = {
    (-1, 1), (0, -1),
    (0, 1), (-1, 0),
    (1, 0), (-1, -1),
    (1, -1), (1, 1)
}


def neighbor_count(cell, grid, W, H):
    x, y = cell
    count = 0
    for d in directions:
        if grid[(y + d[1]) % H][(x + d[0]) % W] == ON:
            count += 1
    return count


def next_grid(grid, W, H):
    new_grid = [[' ' for i in range(W)] for j in range(H)]
    for y, yd in enumerate(grid):
        for x, xd in enumerate(yd):
            count = neighbor_count((x, y), grid, W, H)
            st = True if xd == ON else False
            if not st:
                if count == 3:
                    new_grid[y][x] = ON
                else:
                    new_grid[y][x] = OFF
            else:
                if count < 2 or count > 3:
                    new_grid[y][x] = OFF
                else:
                    new_grid[y][x] = ON
    return new_grid


def draw(grid, screen):
    for y, yd in enumerate(grid):
        screen.addstr(y, 0, ''.join(yd), curses.color_pair(1))
    screen.refresh()


if __name__ == '__main__':
    temp = [list(line) for line in sys.stdin.read().splitlines()]
    H = len(temp)
    W = max(len(i) for i in temp)
    canvas = [[' ' for x in range(W)] for y in range(H)]
    for y, yd in enumerate(temp):
        for x, xd in enumerate(yd):
            if xd == ON:
                canvas[y][x] = xd

    try:
        screen = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, 3, -1)
        new = copy.deepcopy(canvas)
        while True:
            new = next_grid(new, W, H)
            draw(new, screen)
            time.sleep(DELAY)

        curses.endwin()
    except:
        curses.endwin()
