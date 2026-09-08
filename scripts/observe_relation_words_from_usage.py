"""Bring forth words preserved English uses to relate one thing to another.

Two relation physiologies on one road carry no name the grammar states.  Before
any word is considered, the population of candidate words has to come from
somewhere other than the person choosing.  So it is brought forth from
preserved language: words occurring in the position English puts a relating
word in, between something and something else.

The position is recognized by one stated heuristic, which is this file's and
not the corpus's: a lowercase word standing immediately before a determiner,
with a word before it.  That finds where English relates two things, and it
also finds other constructions.  It is a way to bring forth a population, never
a way to decide what a word means.

The runtime's own labels for the two physiologies are not read here, and no
word is proposed for either.  This produces the population only.

Usage:
    .venv/bin/python scripts/observe_relation_words_from_usage.py [--books N]
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

CORPUS = Path(__file__).resolve().parents[1] / "corpus"
DETERMINERS = {
    "the", "a", "an", "his", "her", "its", "their", "our", "your", "my",
    "this", "that", "these", "those", "one", "each", "every", "such",
}
BETWEEN = re.compile(r"([a-z]{3,})\s+([a-z]{2,})\s+([a-z]+)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--books", type=int, default=6)
    arguments = parser.parse_args()

    books = sorted(
        path
        for path in CORPUS.glob("*.txt")
        if path.name.startswith(
            ("prose_", "fiction_", "english_", "law_", "science_", "federalist")
        )
    )[: arguments.books]

    relating: Counter[str] = Counter()
    per_book: dict[str, set] = {}
    for path in books:
        text = path.read_text(encoding="utf-8", errors="replace").lower()
        found: Counter[str] = Counter()
        for before, word, after in BETWEEN.findall(text):
            if after in DETERMINERS and word not in DETERMINERS:
                found[word] += 1
        relating.update(found)
        per_book[path.name] = {word for word, count in found.items() if count > 4}

    print(f"  books read: {len(books)}")
    for path in books:
        print(f"    {path.name}")

    everywhere = set.intersection(*per_book.values()) if per_book else set()
    print(f"\n  words found in the relating position: {len(relating)}")
    print(f"  found in every book read, more than four times each: {len(everywhere)}")

    print("\n  the population, ordered by how much of the corpus carries it:")
    for word in sorted(everywhere, key=lambda w: -relating[w])[:40]:
        carrying = sum(1 for words in per_book.values() if word in words)
        print(f"    {relating[word]:7}  in {carrying}/{len(per_book)} books  {word}")

    print(
        "\n  Two rules narrowed this and both are mine: the position heuristic above,\n"
        "  and requiring a word in every book read more than four times each.  The\n"
        "  unnarrowed population is the larger number printed above.\n"
        "\n  This is a population, not a shortlist.  The heuristic that found it\n"
        "  is stated above and is this file's, so a word appearing here occurs\n"
        "  where English relates two things and may occur there for another\n"
        "  reason.  No word is compared to any physiology here, and frequency\n"
        "  orders the printing only."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
