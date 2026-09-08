"""Ask which admitted words the Book keeps only inside a denial.

The admission list holds every word the Book uses.  It cannot say which words
the Book needs.  A word occurring only inside `X establishes no Y` is in the
lexicon because something was forbidden, and once that denial goes the word has
nowhere left to occur.

Those words are the vocabulary a blocklist keeps alive.  They are read here
before any further denial is deleted, so the lexicon consequence of the
whitelist campaign is known in advance rather than discovered by a failing test.

Words are separated by whitespace and stripped of punctuation.  Sentences are
separated by a full stop and a space.  Nothing here matches a pattern.

Usage:
    .venv/bin/python scripts/observe_admitted_words_kept_by_denials.py
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from book_admission import BOOK, book_admission  # noqa: E402

EDGES = ".,;:`()[]—-_\"'"
DENIES = ("establishes no", "establish no", "requires no", "require no")


def _words(text: str) -> set[str]:
    return {
        word.strip(EDGES).lower()
        for word in text.split()
        if word.strip(EDGES).isalpha()
    }


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    prose = " ".join(
        " ".join(path.read_text(encoding="utf-8").split())
        for path in sorted((BOOK / "chapters").glob("*.md"))
    )
    sentences = [s for s in prose.split(". ") if s.strip()]

    denying: set[str] = set()
    stating: set[str] = set()
    for sentence in sentences:
        lowered = sentence.lower()
        target = denying if any(d in lowered for d in DENIES) else stating
        target |= _words(sentence)

    admitted = book_admission()
    kept = sorted((admitted & denying) - stating)

    print(f"  admitted words:                       {len(admitted)}")
    print(f"  sentences read:                       {len(sentences)}")
    print(f"  words the Book states outside denial: {len(stating & admitted)}")
    print(f"  admitted words occurring only inside a denial: {len(kept)}\n")

    for word in kept:
        carrying = [s for s in sentences if word in _words(s)]
        print(f"    {word:14} {len(carrying)} sentence(s)")
        print(f"      {carrying[0][:100]}")

    print(
        f"\n  These {len(kept)} words are in the lexicon because something was\n"
        "  forbidden.  Each denial deleted takes its words with it, and a word\n"
        "  here has no other sentence to fall back to.\n"
        "\n  This says nothing about whether any denial should go.  It reports what\n"
        "  the lexicon loses when one does, so the loss is chosen rather than met\n"
        "  as a failing admission test.\n"
        "\n  A word occurring outside a denial is not thereby earning its place;\n"
        "  this measures where words occur and never what they do."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
