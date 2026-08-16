from __future__ import annotations

from pathlib import Path


MATERIAL_WINDOWS = (
    ("grammar_goold_brown.txt", 6000),
    ("webster_dictionary.txt", 6000),
    ("roget_thesaurus.txt", 6000),
    ("grammar_kittredge.txt", 6000),
    ("algebra_rivenburg.txt", 1800),
    ("boole_laws_of_thought.tex", 6000),
    ("euclid_elements.txt", 6000),
    ("bash_abs_guide.txt", 6000),
    ("cookbook_farmer.txt", 6000),
    ("french_les_miserables.txt", 6000),
    ("latin_vulgate.txt", 6000),
    ("prose_austen_pride.txt", 6000),
    ("prose_dickens_copperfield.txt", 6000),
    ("prose_franklin_autobiog.txt", 6000),
    ("prose_emerson_essays.txt", 6000),
    ("prose_hume_enquiry.txt", 6000),
)


def supplied_material(root: Path, name: str, first_line: int) -> bytes:
    lines = (root / "corpus" / name).read_bytes().splitlines(keepends=True)
    material = lines[first_line : first_line + 300]
    if len(material) != 300:
        raise ValueError("fixture material does not carry 300 lines")
    return b"".join(material)


def supplied_book_material(root: Path) -> tuple[bytes, ...]:
    return tuple(
        supplied_material(root, name, first_line)
        for name, first_line in MATERIAL_WINDOWS
    )
