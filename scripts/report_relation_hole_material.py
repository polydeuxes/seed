"""Read coordinate material around already-frozen relation holes.

This runs strictly after the combined structural report is written.  It takes
the frozen artifact, records the digest it was frozen at, and only then reads
the coordinate paths as material.  The structural report knows nothing about
these words, so no word can have selected a hole.

Material recorded here is not a relation and is not a candidate relation.  An
unadmitted word is unadmitted implementation coordinate material, nothing more.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
from typing import Any


def coordinate_material(path: list[object]) -> list[str]:
    material = []
    for part in path:
        if not isinstance(part, str) or part == "#":
            continue
        material.extend(re.findall(r"[A-Za-z]+", part.replace("_", " ").lower()))
    return material


def material_counts(report: dict[str, Any]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for family in report["repeated_bare_handoff_families"]:
        counts.update(coordinate_material(family["reference_path"]))
    for key in (
        "relation_coordinate_missing_content_families",
        "unrendered_relation_occurrence_families",
    ):
        for family in report[key]:
            counts.update(coordinate_material(family["coordinate_path"]))
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()

    report = json.loads(arguments.report.read_text(encoding="utf-8"))
    frozen_digest = report.get("structural_digest")
    if not frozen_digest:
        raise SystemExit(
            f"{arguments.report} carries no structural digest; it is not frozen"
        )

    counts = material_counts(report)
    result = {
        "reading": (
            "coordinate material read after the structural report was frozen; "
            "material is not a relation and not a candidate relation"
        ),
        "frozen_report": arguments.report.name,
        "frozen_structural_digest": frozen_digest,
        "distinct_material_count": len(counts),
        "opaque_coordinate_material": [
            {"material": word, "occurrence_count": count}
            for word, count in sorted(
                counts.items(), key=lambda item: (-item[1], item[0])
            )
        ],
    }
    arguments.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(
        f"{arguments.output} distinct={result['distinct_material_count']} "
        f"frozen_at={frozen_digest}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
