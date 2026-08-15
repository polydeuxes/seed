"""Lexical contamination gate for Book proper.

Scope is active constitutional law only:

    book_of_seed/chapters/*.md
    book_of_seed/README.md
    book_of_seed/concordance.md

Historical reports under ``book_of_seed/`` are records and are left to rot
unchanged.  ``rosetta/`` is specifically permitted to carry retired and
retired vocabulary; that is why it exists.

Each banned pattern names vocabulary that a reconstruction removed from
constitutional grammar, or that a reconstruction found smuggles a Assertion.  A word
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
    # The retired composite noun only.  `examines` and `examinable` are
    # ordinary prose in active law -- `03.Prerequisite:36,104,122` have
    # applicability as the subject doing the examining -- and banning the whole
    # family would refuse them.  `examination` is already at zero occurrences,
    # so this is a regression guard against the noun returning.
    (r"\bexaminations?\b", "examination"),
    (r"\bexecut\w*\b", "execut*"),
    (r"\bsuffi\w*\b", "suffi*"),
    (r"\bpermission\w*\b", "permission*"),
    (r"\btool\w*\b", "tool*"),
    # Standalone work only; workflow is not matched. Workspace was a runtime
    # partition that the Book collapsed into exact Locality relations, so it
    # has no surviving constitutional coordinate.
    (r"\bwork(?:s|ed|ing)?\b", "work"),
    (r"\bworkspaces?\b", "workspace"),
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
    (r"\bconstitutive support\b", "constitutive support"),
    (r"\bstanding effect\b", "standing effect"),
    (r"\b(?:almost|near|nearly)\s+certain\w*\b", "almost/near/nearly certain*"),
    # The retired State abstraction.  The ordinary verb forms `states` and
    # `stated` are not matched: banning the noun does not ban English.
    (r"\bstate\b", "state"),
    (r"\bStateProjector\b", "StateProjector"),
    # Words active law contains but never defines, which arrive carrying an
    # ordinary-language bundle no clause supplies.  `translation` drags source
    # language, target language, semantic equivalence, represented relation preservation,
    # and a translator; no clause states what a translation is, names a
    # translation occurrence, or names a translation boundary.  See
    # `relation_proposal_join_investigation_001.md` section 9.
    (r"\btranslat\w*\b", "translat*"),
    # 18 sentences in active law, 11 of them pure denial -- "retained history
    # is not learning, changed stored data is not learning, a new current value
    # is not learning".  The rest are topic lists ("Learning may concern
    # condition, trajectory, ..."), one passive definition, and one that says
    # Learning establishment "may be understood as" constrained movement, which
    # is a reading aid rather than an establishment.  No clause names a
    # Learning responsible boundary, boundary, occurrence, responsibility, or act.
    # Active law previously denied one Learning object spanning exact bounds
    # and denied authorizing general language learning.
    (r"\blearn\w*\b", "learn*"),
    # `actor` entered with the retired generalized runtime as a closed list of
    # user/model/system/tool/builder/approver labels.  It names no Responsibility
    # that established occurrence or source-relation distinctions do not
    # already carry.  The durable occurrence column is retained as
    # unconstrained compatibility shape; storage survival does not establish
    # Book grammar.
    (r"\bactors?\b", "actor"),
    (r"\bproducers?\b|producer[-_]", "producer"),
    (r"\bconsumers?\b|consumer[-_]", "consumer"),
    (r"\bowners?\b|owner[-_]", "owner"),
    (r"\bownership\w*\b|ownership[-_]", "ownership*"),
    (r"\bowns\b|\bowned\b|\bowning\b", "owns/owned/owning"),
    (r"\bautomatic\w*\b", "automatic*"),
    (r"\bformations?\b|formation[-_]", "formation"),
    (r"\bestablishments?\b|establishment[-_]", "establishment"),
    (r"\buptake\b|uptake[-_]", "uptake"),
    (r"\bhandoffs?\b|handoff[-_]", "handoff"),
    (r"\blineage\b|lineage[-_]", "lineage"),
    (r"\bpurposes?\b|purpose[-_]", "purpose"),
    (r"\bmeanings?\b|meaning[-_]", "meaning"),
    (r"\bcapabilit(?:y|ies)\b|capability[-_]", "capability"),
    (r"\bgaps?\b|gap[-_]", "gap"),
    (r"\bgoals?\b", "goal"),
    (r"\bdemands?\b", "demand"),
    (r"\btestimon(?:y|ies)\b|testimony[-_]", "testimony"),
    (r"\battribut\w*\b|attribut[-_]", "attribut*"),
    (r"\bconstructors?\b|constructor[-_]", "constructor"),
    (r"\bproduction authority\b", "production authority"),
    (r"\bproduc\w*\b|produc[-_]", "produc*"),
    (r"\breyield\w*\b|reyield[-_]", "reyield*"),
    # `warrant` survives only in Seed's single Standing declaration. Elsewhere
    # the exact Evidence, Authority, Scope, support relation, occurrence, or
    # Standing must be named instead.
    (r"\bwarrant\w*\b|warrant[-_]", "warrant*"),
    (r"\bvalidatey\b|reconstruction[-_]", "reconstruction"),
    (r"\bconsum\w*\b|consum[-_]", "consum*"),
    (r"\breli\w*\b|reli[-_]", "reli*"),
    (r"\bclaims?\b|claim[-_]", "claim"),
    (r"\bfacts?\b|fact[-_]", "fact"),
    (r"\bartifacts?\b|artifact[-_]", "artifact"),
    (r"\bprojections?\b|projection[-_]", "projection"),
    (r"\bviews?\b|view[-_]", "view"),
    (r"\bdistricts?\b", "district"),
    (r"\bknowledge\w*\b|knowledge[-_]", "knowledge*"),
    (r"\borientat\w*\b|orientat[-_]", "orientat*"),
    (r"\buniversal\w*\b|universal[-_]", "universal*"),
    (r"\bexternal\w*\b|external[-_]", "external*"),
    (r"\bexecutions?\b|execution[-_]", "execution"),
    (
        r"\binvent(?:s|ed|ing|ion|ions)?\b|invent(?:s|ed|ing|ion|ions)?[-_]",
        "invent*",
    ),
    (r"\binventor(?:y|ies)\b|inventory[-_]", "inventory"),
    (r"(?<![A-Za-z])presentation\w*\b|(?<![A-Za-z])presentation[-_]", "presentation*"),
)

# The discriminator, corrected.
#
# An earlier version of this list asked whether active law *defines* the term.
# That test is too weak and it cleared `learn*`, which active law defines and
# never owns.  A definition describes; it does not supply a responsibility.
#
# The test is:
#
#     name the Responsibility no other established coordinate already carries,
#     then reconstruct its responsible boundary, the act that establishes it, and the standing that
#     yield establishes
#
#     unique Responsibility can be named  ->  admitted vocabulary, however
#                                             ordinary it sounds
#     no unique Responsibility             ->  wording, alias, or duplicate;
#                                             it must not enter as the doer
#
# `05.Recording.A` passes: a recording boundary may create retrievable
# assertion-bearing material, and the yielded standing is that a record exists
# and preserves an Assertion carrying source coordinates. Responsible boundary, act, standing.
#
# `learning` and `translation` fail it.  Neither has a clause naming who does
# it.  Sentence-initial capitals are not evidence either way; `Remembering`
# was the same shape.
#
# Considered, recorded so the test is not re-litigated from the word alone:
#
#   examines      NOT banned.  `03.Prerequisite:36,104,122` have applicability
#                 as the subject doing the examining.  Ordinary prose whose
#                 subject is an established coordinate is not the retired noun.
#   Assertion     The constitutional subject and ceiling for asserted content.
#                 Claim and Fact are Rosetta shorthand only; both are guarded
#                 above from returning to active law.
#   artifact      Rosetta shorthand only. The active grammar names the exact
#                 representation, record, Assertion, result, or occurrence.
#   assertion     UNRESOLVED, deliberately not banned here.  It fails the test
#                 above -- `#2382` established that no clause names what
#                 yields `the relation assertion` -- but `01.Kinds:28`
#                 *requires* it as a coordinate, so banning it would flag
#                 active law's own required text.  A required coordinate with
#                 no responsible boundary is a different defect from a word with no responsible boundary, and
#                 this gate is not the place to decide which repair applies.
#   actor         BANNED.  Historical reconciliation called it coarse event
#                 authorship vocabulary, but it carries no Responsibility not
#                 already carried by established occurrence or source-relation
#                 distinctions.  `#2450` removed its closed runtime grammar
#                 while retaining the durable column as an unconstrained
#                 compatibility label.  That physical field does not earn
#                 admission to active law.

COMPILED = tuple((re.compile(pattern, re.IGNORECASE), label) for pattern, label in BANNED)


def scan_active_line(line: str) -> str:
    """Expose active language while ignoring only Markdown destinations."""

    scanned = re.sub(r"\]\([^)]*\)", "]()", line)
    # Identifiers are language too. Snake-case and kebab-case may not hide
    # vocabulary that active prose is forbidden to carry.
    return re.sub(r"[_-]+", " ", scanned)


def book_proper_files() -> list[Path]:
    """Active law only.  Reports and rosetta/ are out of scope by design."""
    files = sorted((BOOK / "chapters").glob("*.md"))
    for extra in ("README.md", "concordance.md", "grammar.json"):
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
            # Stable historical file addresses may retain retired words.  The
            # visible label is active law; a Markdown destination is not.
            scanned = scan_active_line(line)
            scanned = scanned.replace(
                "This Seed carries only Standing it can warrant through its "
                "Evidence, Authority, Scope, and preserved limits.",
                "",
            )
            for pattern, label in COMPILED:
                if pattern.search(scanned):
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
    assert any(f.startswith("book_of_seed/chapters/") for f in files)
    assert not any("/rosetta/" in f or f.startswith("rosetta/") for f in files)
    # A historical report sitting directly under book_of_seed/ is out of scope.
    assert not any(
        f.startswith("book_of_seed/") and f.count("/") == 1 and f.endswith("_001.md")
        for f in files
    )


def test_book_proper_carries_no_banned_vocabulary():
    found = find_violations()
    assert not found, "\n" + render_violations(found)


def test_identifier_separators_cannot_hide_retired_vocabulary():
    examples = {
        "requires_later_consumption": "consum*",
        "exact-reyield-edge": "reyield*",
        "production_evidence_id": "produc*",
        "invented_relation": "invent*",
        "coordinate_inventory": "inventory",
        "workspace_id": "workspace",
    }

    for identifier, expected_label in examples.items():
        scanned = scan_active_line(identifier)
        labels = {label for pattern, label in COMPILED if pattern.search(scanned)}
        assert expected_label in labels


def test_active_test_witnesses_carry_no_retired_narrative():
    retired = re.compile(
        r"\b(?:consum\w*|reli(?:ance|ances|ant|ed|es|ing|y)|automatic\w*|"
        r"owners?|ownership\w*|claims?|meanings?|districts?|"
        r"invent(?:s|ed|ing|ion|ions)?)\b",
        re.IGNORECASE,
    )
    contaminated = {
        path.relative_to(ROOT).as_posix(): [
            (line_number, line.rstrip())
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            )
            if retired.search(scan_active_line(line))
        ]
        for path in sorted((ROOT / "tests").glob("test_*.py"))
        if path.name != Path(__file__).name
    }

    assert {path: hits for path, hits in contaminated.items() if hits} == {}


if __name__ == "__main__":  # pragma: no cover - command-line entry point
    print(render_violations(find_violations()))


LEXICON = BOOK / "admitted-lexicon.txt"
ROSETTA_LEXICON = ROOT / "rosetta" / "admitted-lexicon.txt"


def admitted_lexicon() -> set[str]:
    """Every word active law may carry.  One word per line, sorted."""
    return set(_lexicon_entries())


def test_book_has_its_own_lexicon_and_points_to_rosetta():
    assert LEXICON == ROOT / "book_of_seed" / "admitted-lexicon.txt"
    assert ROSETTA_LEXICON != LEXICON
    assert not LEXICON.is_symlink()
    assert not ROSETTA_LEXICON.is_symlink()
    assert (
        "# Rosetta lexicon: ../rosetta/admitted-lexicon.txt"
        in LEXICON.read_text(encoding="utf-8").splitlines()
    )
    book_entries = set(_lexicon_entries(LEXICON))
    rosetta_entries = set(_lexicon_entries(ROSETTA_LEXICON))
    assert book_entries < rosetta_entries


def test_warrant_admission_is_broad_in_rosetta_and_singular_in_book():
    book_warrant = {
        word for word in _lexicon_entries(LEXICON) if word.startswith("warrant")
    }
    rosetta_warrant = {
        word
        for word in _lexicon_entries(ROSETTA_LEXICON)
        if word.startswith("warrant")
    }

    assert book_warrant == {"warrant"}
    assert rosetta_warrant == {"warrant", "warranted", "warranting", "warrants"}


def _lexicon_entries(path: Path = LEXICON) -> dict[str, str]:
    """Each admitted word mapped to its reason, empty when none is given."""
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        word, _, reason = line.partition("#")
        entries[word.strip()] = reason.strip()
    return entries


def book_proper_words() -> dict[str, list[tuple[str, int]]]:
    """Each word in active law, with every place it occurs."""
    found: dict[str, list[tuple[str, int]]] = {}
    for path in book_proper_files():
        rel = path.relative_to(ROOT).as_posix()
        for number, line in enumerate(path.read_text().split("\n"), start=1):
            for word in re.findall(r"[A-Za-z]+", scan_active_line(line).lower()):
                found.setdefault(word, []).append((rel, number))
    return found


def test_book_proper_admits_only_lexicon_words():
    """The gate a banned list cannot be: a word not admitted is refused.

    A blocklist must anticipate the word that contaminates.  This one need
    not.  Vocabulary entering active law now costs a deliberate lexicon
    entry, which is where the argument for admitting it belongs.
    """

    unadmitted = {
        word: places
        for word, places in book_proper_words().items()
        if word not in admitted_lexicon()
    }
    report = "\n".join(
        f"  {word} -- {places[0][0]}:{places[0][1]}"
        + (f" and {len(places) - 1} more" if len(places) > 1 else "")
        for word, places in sorted(unadmitted.items())
    )
    assert not unadmitted, (
        "\nActive law carries vocabulary the lexicon does not admit.\n"
        "Book vocabulary is not admitted by book_of_seed/admitted-lexicon.txt. "
        "Remove it or request curation; automated agents must not amend the lexicon:\n"
        + report
    )


def test_lexicon_cannot_readmit_banned_vocabulary():
    """A refused word is admitted only with a reason on its line."""

    entries = _lexicon_entries()
    readmitted = sorted(
        word
        for word, reason in entries.items()
        if not reason
        for pattern, _ in COMPILED
        if pattern.search(word)
    )
    assert not readmitted, (
        "\nThe lexicon admits refused vocabulary with no reason given: "
        + ", ".join(readmitted)
    )


def test_lexicon_carries_no_unused_admissions():
    """Admission is evidence of use, so a word no longer in law is retired."""

    unused = sorted(admitted_lexicon() - set(book_proper_words()))
    assert not unused, (
        "\nThe lexicon admits words active law no longer carries: "
        + ", ".join(unused)
    )
