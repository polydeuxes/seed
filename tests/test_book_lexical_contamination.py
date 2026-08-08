"""Lexical contamination gate for Book proper.

Scope is active constitutional law only:

    book_of_seed/[0-9][0-9]-*/**/*.md
    book_of_seed/README.md
    book_of_seed/concordance.md

Historical reports under ``book_of_seed/`` are testimony and are left to rot
unchanged.  ``rosetta/`` is specifically permitted to carry retired and
external vocabulary; that is its purpose.

Each banned pattern names vocabulary that a recovery removed from
constitutional grammar, or that a recovery found smuggles a claim.  A word
being banned here does not make it forbidden English -- it makes it
non-constitutional, and its explanation belongs in ``rosetta/``.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book_of_seed"

# (pattern, label).  Patterns are matched case-insensitively.
BANNED: tuple[tuple[str, str], ...] = (
    (r"\bexamin\w*\b", "examin*"),
    (r"\bexecut\w*\b", "execut*"),
    (r"\bsuffi\w*\b", "suffi*"),
    (r"\bpermission\w*\b", "permission*"),
    (r"\btool\w*\b", "tool*"),
    # standalone work only; workspace/workflow are not matched
    (r"\bwork(?:s|ed|ing)?\b", "work"),
    (r"\bperformance\w*\b", "performance*"),
    (r"\bmethod\w*\b", "method*"),
    (r"\btrigger\w*\b", "trigger*"),
    (r"\bcontrol\w*\b", "control*"),
    (r"\btarget\w*\b", "target*"),
    (r"\benough\b", "enough"),
    (r"\bdeliver\w*\b", "deliver*"),
    (r"\breceipt\w*\b", "receipt*"),
    (r"\backnowledg\w*\b", "acknowledg*"),
    # standalone operation forms only; operator is not matched
    (r"\boperations?\b", "operation"),
    (r"\boperational\w*\b", "operational*"),
    (r"\breadiness\w*\b", "readiness*"),
    (r"\bactivation\w*\b", "activation*"),
    (r"\benablement\w*\b", "enablement*"),
    (r"\blenses?\b", "lens"),
    (r"\broads?\b", "road"),
    (r"\bconstitutive warrant\b", "constitutive warrant"),
    (r"\bstanding effect\b", "standing effect"),
    (r"\b(?:almost|near|nearly)\s+certain\w*\b", "almost/near/nearly certain*"),
    # The retired State abstraction.  The ordinary verb forms `states` and
    # `stated` are not matched: banning the noun does not ban English.
    (r"\bstate\b", "state"),
    (r"\bStateProjector\b", "StateProjector"),
)

COMPILED = tuple((re.compile(p, re.IGNORECASE), label) for p, label in BANNED)


def book_proper_files() -> list[Path]:
    """Active law only.  Reports and rosetta/ are out of scope by design."""
    files = sorted(BOOK.glob("[0-9][0-9]-*/**/*.md"))
    for extra in ("README.md", "concordance.md"):
        candidate = BOOK / extra
        if candidate.exists():
            files.append(candidate)
    return files


def find_violations() -> list[tuple[str, int, str, str]]:
    """Every violation, not merely the first: (path, line, label, text)."""
    found: list[tuple[str, int, str, str]] = []
    for path in book_proper_files():
        rel = path.relative_to(ROOT).as_posix()
        for number, line in enumerate(path.read_text().split("\n"), start=1):
            for pattern, label in COMPILED:
                if pattern.search(line):
                    found.append((rel, number, label, line.strip()))
    return found


def render_violations(found: list[tuple[str, int, str, str]]) -> str:
    by_label: dict[str, int] = {}
    for _, _, label, _ in found:
        by_label[label] = by_label.get(label, 0) + 1
    lines = [f"{len(found)} lexical violations in Book proper", ""]
    for label, count in sorted(by_label.items(), key=lambda kv: -kv[1]):
        lines.append(f"  {count:4}  {label}")
    lines.append("")
    for rel, number, label, text in found:
        lines.append(f"{rel}:{number}  [{label}]")
        lines.append(f"    {text[:150]}")
    return "\n".join(lines)


def test_book_proper_scope_excludes_reports_and_rosetta():
    files = {p.relative_to(ROOT).as_posix() for p in book_proper_files()}
    assert any(f.startswith("book_of_seed/0") for f in files)
    assert not any("/rosetta/" in f or f.startswith("rosetta/") for f in files)
    # A historical report sitting directly under book_of_seed/ is out of scope.
    assert not any(
        f.startswith("book_of_seed/") and f.count("/") == 1 and f.endswith("_001.md")
        for f in files
    )


def test_book_proper_carries_no_banned_vocabulary():
    found = find_violations()
    assert not found, "\n" + render_violations(found)


if __name__ == "__main__":  # pragma: no cover - inventory entry point
    print(render_violations(find_violations()))
