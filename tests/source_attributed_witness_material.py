from __future__ import annotations

from pathlib import Path


SOURCE_ATTRIBUTED_WITNESS_FIRST_LINE = 126
SOURCE_ATTRIBUTED_WITNESS_MATERIAL_COUNT = 300


def supplied_source_attributed_witness_material(root: Path) -> tuple[bytes, ...]:
    material = (
        root / "corpus" / "english_grimm_fairy_tales.txt"
    ).read_bytes().splitlines(keepends=True)
    supplied = material[
        SOURCE_ATTRIBUTED_WITNESS_FIRST_LINE : (
            SOURCE_ATTRIBUTED_WITNESS_FIRST_LINE
            + SOURCE_ATTRIBUTED_WITNESS_MATERIAL_COUNT
        )
    ]
    if len(supplied) != SOURCE_ATTRIBUTED_WITNESS_MATERIAL_COUNT:
        raise ValueError(
            "source-attributed Witness Material differs from its exact count"
        )
    return tuple(supplied)
