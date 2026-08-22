"""Inventory the Book law the machine grammar does not carry.

Every clause carrying an identifier projects exactly, so the identifier
comparison reports a complete projection.  It is complete over what carries an
identifier.  A fifth of the Book states law in prose carrying none.

Each distinction stated in that prose is recovered here and set beside the
grammar, one row per distinction, classified as represented exactly,
represented but compressed, or absent.  A distinction is read as compressed
where the grammar carries the word and not the physiology the Book states for
it, because a bare coordinate name enforces nothing the word means.

The classification is a reading of two recovered texts.  The texts are quoted
so the reading can be disagreed with at the row that states it.

Usage:
    .venv/bin/python scripts/observe_unprojected_book_law.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

BOOK = Path(__file__).resolve().parents[1] / "book_of_seed"
GRAMMAR = BOOK / "witness_grammar.json"
CLAUSE = re.compile(r"^#{2,3}\s+([0-9]+)\.([A-Za-z][A-Za-z0-9.]*)\s+—", re.M)

# (chapter, distinction the Book states, class, what the grammar carries)
INVENTORY = (
    ("11 Representation", "material-acquisition Responsibility bounds one exact source boundary and one acquisition Act", "B", "01.Source.G bounds the operator boundary only"),
    ("11 Representation", "its Yield relation, Act occurrence to exact material result", "A", "01.Source.G relations: yield, locality"),
    ("11 Representation", "the result preserves source role, source boundary, provenance, Authority, Scope, Locality, known loss, limits, and Unknown", "B", "01.Source.G result is one name, exact_operator_material_result, carrying none of the nine"),
    ("11 Representation", "operator-supplied and Witness-supplied material have separate source branches and occurrences", "C", "one source branch is declared"),
    ("11 Representation", "shared material establishes no shared occurrence, result, Yield, source relation, or Standing", "C", "establishes_no exists on other coordinates, not this one"),
    ("11 Representation", "a Representation Act preserves exact material from one exact source result", "C", "Representation occurs nowhere in the grammar"),
    ("11 Representation", "its Yield relation, occurrence to exact Representation result", "C", "no Representation coordinate to carry it"),
    ("11 Representation", "the Representation result establishes no relation for the material content", "C", "absent"),
    ("11 Representation", "an emission Responsibility carrying Representation result, destination operator boundary, emission Act, Authority, Scope, Locality, limits, conflicts, known loss, and Unknown", "C", "emission occurs nowhere; conflicts and known loss occur nowhere"),
    ("11 Representation", "required Admission establishing the Representation-to-destination position", "C", "Admission is declared for the subject-to-Act position only"),
    ("11 Representation", "Admission establishes no Participation or emission", "C", "absent"),
    ("11 Representation", "the admitted Representation requires Participation to the emission Act occurrence", "C", "absent"),
    ("11 Representation", "that occurrence and the destination boundary result are the subjects of one Yield", "C", "absent"),
    ("11 Representation", "an exact-material boundary write preserves the material accepted and its reported count", "C", "absent"),
    ("11 Representation", "attempt, partial write, failure, accepted write, and emission are separate occurrences and results", "C", "five occurrence kinds, none declared"),
    ("11 Representation", "a later failure establishes no erasure of an accepted write", "C", "absent"),
    ("11 Representation", "effects beyond the addressed boundary require a separate responsible occurrence", "C", "absent"),
    ("12 Stopping", "one stopping Responsibility carrying its subject, stopping Act, Authority, Scope, Locality, limits, and required support relations", "C", "responsibility.coordinates carries support_relations; no stopping Responsibility is declared"),
    ("12 Stopping", "a support Assertion requires Participation to the stopping Act occurrence", "C", "the support relation runs to an input-to-Act position, not to a stopping Act"),
    ("12 Stopping", "that occurrence and one exact Stop result are the subjects of one Yield", "C", "Stop occurs nowhere in the grammar"),
    ("12 Stopping", "Completion is a separate Assertion with its own subject, Responsibility, Act occurrence, Yield, Authority, Scope, Locality, limits, and Standing", "C", "Completion occurs twice, both inside another clause's establishes_no"),
    ("12 Stopping", "no movement, no applicable input, failure, local exhaustive result, or Stop result establishes completion beyond its exact Scope", "C", "01.Standing.D denies completion for another Responsibility, a different subject"),
    ("05 Provenance", "provenance is the exact ordered source and occurrence reference path preserved with material", "B", "provenance is one bare name in responsibility.coordinates; the ordered path is not carried"),
    ("05 Provenance", "each reference carries one exact source or occurrence", "C", "absent"),
    ("05 Provenance", "the path establishes no addressed occurrence, source relation, Authority, Applicability, Participation, result, or Standing", "C", "absent"),
    ("05 Provenance", "use of each addressed subject requires the Responsibility, Authority, Scope, Locality, limits, and responsible occurrence that use requires", "C", "absent"),
    ("02 Authority", "Authority carries one exact source, Responsibility, subject, Act, occurrence, result, Scope, and limits", "B", "Authority is one required item in five relations; its eight coordinates are not carried"),
    ("02 Authority", "material carrying exact Authority coordinates establishes no other Authority", "C", "absent"),
    ("02 Authority", "Scope bounds the subjects, relations, Acts, occurrences, results, Localities, and limits addressed by one Responsibility", "B", "Scope is one required item; what it bounds is not carried"),
    ("02 Authority", "one Scope establishes no Scope for another Responsibility", "C", "absent"),
    ("02 Authority", "Authority movement and Scope movement require an exact responsible occurrence", "C", "03.Movement.A declares movement generically, not of Authority or Scope"),
    ("02 Authority", "carriage of Authority or Scope establishes no Authority or Scope at another boundary", "C", "absent"),
    ("09 Recording", "one Yield carries a recording Act occurrence to one exact retrievable record", "B", "05.Recording.A result is recorded_Assertion, and retrievability is not carried"),
    ("09 Recording", "the result preserves material, source coordinates, Authority, Scope, Locality, limits, and Unknown established at that recording boundary", "B", "the seven are not carried on the result"),
    ("09 Recording", "record existence establishes no recorded source occurrence, relation, Applicability, Participation, renewed occurrence, movement, or Standing", "C", "absent"),
    ("01 Standing", "this Seed first current Standing carries no coordinates", "A", "standing.current.coordinates is empty"),
    ("01 Standing", "each exact Responsibility carried by current Standing is one branch of that Standing", "C", "standing.path is one ordered list and states no branch"),
    ("01 Standing", "a Responsibility is no other Standing subject", "C", "absent"),
)


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    declared = grammar["book_coordinates"]

    print(f"  {len(declared)} coordinates, projecting 31 identified clauses exactly.")
    print(f"  {len(INVENTORY)} distinctions recovered from Book prose carrying no identifier.\n")

    for name, mark in (("A represented exactly", "A"),
                       ("B represented but compressed", "B"),
                       ("C absent", "C")):
        rows = [row for row in INVENTORY if row[2] == mark]
        print(f"  {name}: {len(rows)}\n")
        for chapter, distinction, _mark, carried in rows:
            print(f"    {chapter}")
            print(f"      Book:    {distinction}")
            print(f"      grammar: {carried}")
        print()

    print("  words the Book states law about, counted in the grammar:\n")
    text = GRAMMAR.read_text(encoding="utf-8").lower()
    for word in ("representation", "emission", "stop", "completion",
                 "known loss", "conflicts", "admission", "provenance"):
        print(f"    {text.count(word):3}  {word}")

    print("\n  clause identifiers, and the chapter carrying each:\n")
    mismatched = 0
    for path in sorted((BOOK / "chapters").glob("*.md")):
        chapter = int(path.name.split("_")[0])
        for match in CLAUSE.finditer(path.read_text()):
            if int(match.group(1)) != chapter:
                mismatched += 1
    print(f"    {mismatched} of 31 identifiers carry a number that is not their chapter's.")
    print("    An identifier is a citation address, and citing it locates no chapter.")

    print(
        "\n  Every distinction above is stated by the active Book and none of it\n"
        "  can be projected, cited by identifier, or enforced, because the prose\n"
        "  stating it carries no identifier.  The Representation Act, the emission\n"
        "  Responsibility, the Stop result, and Completion are four subjects the\n"
        "  Book states in full and the grammar never names.\n"
        "\n  The rows are a reading of two recovered texts and are recorded so a\n"
        "  disposition can be disagreed with at the row that states it.  Nothing\n"
        "  here says which side should change, or that unnumbered law should be\n"
        "  numbered."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
