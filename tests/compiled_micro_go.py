from __future__ import annotations

import sys


WIDTH = 3
DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def connected(positions, coordinate):
    mark = positions[coordinate]
    found = {coordinate}
    pending = [coordinate]
    while pending:
        current = pending.pop()
        column, row = divmod(current, WIDTH)
        for dx, dy in DIRECTIONS:
            other_column = column + dx
            other_row = row + dy
            other = other_column * WIDTH + other_row
            if (
                0 <= other_column < WIDTH
                and 0 <= other_row < WIDTH
                and other not in found
                and positions[other] == mark
            ):
                found.add(other)
                pending.append(other)
    return found


def has_zero(positions, material):
    for coordinate in material:
        column, row = divmod(coordinate, WIDTH)
        for dx, dy in DIRECTIONS:
            other_column = column + dx
            other_row = row + dy
            if (
                0 <= other_column < WIDTH
                and 0 <= other_row < WIDTH
                and positions[other_column * WIDTH + other_row] == 0
            ):
                return True
    return False


def main() -> int:
    material = sys.stdin.buffer.read()
    positions = [0 for _ in range(WIDTH * WIDTH)]
    earlier = [tuple(positions)]
    consecutive_nines = 0
    stopped = False
    for occurrence_position, coordinate in enumerate(material):
        if stopped or coordinate > len(positions):
            return 1
        if coordinate == len(positions):
            consecutive_nines += 1
            stopped = consecutive_nines == 2
            continue
        consecutive_nines = 0
        if positions[coordinate] != 0:
            return 1
        mark = 1 + occurrence_position % 2
        positions[coordinate] = mark
        other_mark = 1 + mark % 2
        for other in range(len(positions)):
            if positions[other] == other_mark:
                material_at_mark = connected(positions, other)
                if not has_zero(positions, material_at_mark):
                    for removed in material_at_mark:
                        positions[removed] = 0
        if not has_zero(positions, connected(positions, coordinate)):
            return 1
        if tuple(positions) in earlier:
            return 1
        earlier.append(tuple(positions))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
