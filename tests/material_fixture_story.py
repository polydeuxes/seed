from __future__ import annotations

from pathlib import Path


STORY_FIRST_LINE = 126
STORY_MATERIAL_COUNT = 300


def supplied_story_material(root: Path) -> tuple[bytes, ...]:
    material = (
        root / "corpus" / "english_grimm_fairy_tales.txt"
    ).read_bytes().splitlines(keepends=True)
    supplied = material[
        STORY_FIRST_LINE : STORY_FIRST_LINE + STORY_MATERIAL_COUNT
    ]
    if len(supplied) != STORY_MATERIAL_COUNT:
        raise ValueError("fixture material differs from its exact count")
    return tuple(supplied)
