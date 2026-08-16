from __future__ import annotations

import sys


WIDTH = 7
HEIGHT = 6
DIRECTIONS = ((1, 0), (0, 1), (1, 1), (1, -1))


def same(positions, coordinate, row, mark, dx, dy):
    found = 0
    for distance in range(1, 4):
        other_coordinate = coordinate + dx * distance
        other_row = row + dy * distance
        if (
            not 0 <= other_coordinate < WIDTH
            or not 0 <= other_row < HEIGHT
            or positions[other_coordinate][other_row] != mark
        ):
            break
        found += 1
    return found


def main() -> int:
    material = sys.stdin.buffer.read()
    positions = [[0 for _ in range(HEIGHT)] for _ in range(WIDTH)]
    heights = [0 for _ in range(WIDTH)]
    stopped = False
    for occurrence_position, coordinate in enumerate(material):
        if stopped or coordinate >= WIDTH or heights[coordinate] >= HEIGHT:
            return 1
        row = heights[coordinate]
        mark = 1 + occurrence_position % 2
        positions[coordinate][row] = mark
        heights[coordinate] += 1
        stopped = any(
            1
            + same(positions, coordinate, row, mark, dx, dy)
            + same(positions, coordinate, row, mark, -dx, -dy)
            >= 4
            for dx, dy in DIRECTIONS
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
