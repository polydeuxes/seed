from __future__ import annotations

import sys


LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def main() -> int:
    material = sys.stdin.buffer.read()
    positions = bytearray(9)
    stopped = False
    for occurrence_position, coordinate in enumerate(material):
        if stopped or coordinate >= len(positions) or positions[coordinate] != 0:
            return 1
        mark = 1 + occurrence_position % 2
        positions[coordinate] = mark
        stopped = any(
            all(positions[position] == mark for position in line)
            for line in LINES
        )
    sys.stdout.buffer.write(positions)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
