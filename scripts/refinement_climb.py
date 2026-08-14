#!/usr/bin/env python3
"""Refine a classification until a rung establishes nothing the one below did.

The mechanism is not about bytes or codecs. Given subjects, a witness that
answers about pairs of them, and a first classification, each rung asks its
witness how the members of a class behaved and splits the class where they
behaved apart. A class whose members behaved alike survives untouched.

```text
  classesₙ
    ↓ read by the next measurement
  members disagree?   no  -> the classification survives
                      yes -> it decomposes
    ↓
  classesₙ₊₁
```

**A classification is lawful for the act that established it, and no longer.**
`0x80` and `0xff` are one class under a measurement of first bytes and two
under a measurement of pairs. Neither measurement is wrong; the second found
the first insufficient for its own purpose.

**Whether the first classification must carry something is the witness's
affair.** A witness that answers differently for a subject depending on which
side of a representative it falls will separate from one class containing
everything. A witness that answers `False` for almost every pair will not: from
one class every signature matches and nothing splits. The first rung is
supplied by a caller because it is a measurement in its own right, not a
detail of this one.

**Termination is not a limit chosen here.** The climb ends where a rung
separates nothing further, which is the witness having nothing left to say.
"""

from __future__ import annotations

from typing import Callable, Hashable, Iterable, Sequence

Subject = Hashable
Partition = list[tuple[Subject, ...]]
Witness = Callable[[Subject, Subject], Hashable]


def one_class(subjects: Iterable[Subject]) -> Partition:
    """Every subject together: the classification that establishes nothing."""

    return [tuple(subjects)]


def by(key: Callable[[Subject], Hashable], subjects: Iterable[Subject]) -> Partition:
    """A first classification carrying whatever the key measured."""

    grouped: dict[Hashable, list[Subject]] = {}
    for subject in subjects:
        grouped.setdefault(key(subject), []).append(subject)
    return [tuple(members) for members in grouped.values()]


def signature(
    subject: Subject, partition: Partition, witness: Witness
) -> tuple[tuple[Hashable, ...], tuple[Hashable, ...]]:
    """How this subject behaved against one representative of each class.

    Both directions are asked. A witness that answers differently depending on
    which side a subject is on would otherwise have half its testimony
    discarded.
    """

    representatives = [members[0] for members in partition]
    return (
        tuple(witness(subject, other) for other in representatives),
        tuple(witness(other, subject) for other in representatives),
    )


def refine(partition: Partition, witness: Witness) -> Partition:
    """Split each class where its members' signatures differ."""

    refined: Partition = []
    for members in partition:
        grouped: dict[Hashable, list[Subject]] = {}
        for subject in members:
            grouped.setdefault(signature(subject, partition, witness), []).append(
                subject
            )
        refined.extend(tuple(split) for split in grouped.values())
    return refined


def climb(first: Partition, witness: Witness, limit: int = 32) -> list[Partition]:
    """Every rung, from the classification supplied to the one that stops moving."""

    rungs = [first]
    for _ in range(limit):
        nxt = refine(rungs[-1], witness)
        if len(nxt) == len(rungs[-1]):
            break
        rungs.append(nxt)
    return rungs


def heights(rungs: Sequence[Partition]) -> list[int]:
    """How many classes each rung held."""

    return [len(rung) for rung in rungs]


def unseparated(rungs: Sequence[Partition]) -> list[tuple[Subject, ...]]:
    """Classes the climb never split, which is what the witness could not say."""

    return [members for members in rungs[-1] if len(members) > 1]
