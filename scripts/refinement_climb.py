#!/usr/bin/env python3
"""Refine one partition through complete ordered-pair witness coverage."""

from __future__ import annotations

from typing import Callable, Hashable, Iterable, Sequence

Subject = Hashable
Partition = list[tuple[Subject, ...]]
Witness = Callable[[Subject, Subject], Hashable]


def one_class(subjects: Iterable[Subject]) -> Partition:
    return [tuple(subjects)]


def by(key: Callable[[Subject], Hashable], subjects: Iterable[Subject]) -> Partition:
    grouped: dict[Hashable, list[Subject]] = {}
    for subject in subjects:
        grouped.setdefault(key(subject), []).append(subject)
    return [tuple(subjects) for subjects in grouped.values()]


def refine(partition: Partition, witness: Witness) -> Partition:
    subjects = tuple(other for subjects in partition for other in subjects)
    observed = {
        (first, second): witness(first, second)
        for first in subjects
        for second in subjects
    }
    refined: Partition = []
    for subjects_at_one_coordinate in partition:
        grouped: dict[Hashable, list[Subject]] = {}
        for subject in subjects_at_one_coordinate:
            complete = (
                tuple(observed[subject, other] for other in subjects),
                tuple(observed[other, subject] for other in subjects),
            )
            grouped.setdefault(complete, []).append(subject)
        refined.extend(tuple(split) for split in grouped.values())
    return refined


def climb(first: Partition, witness: Witness) -> list[Partition]:
    nxt = refine(first, witness)
    return [first] if len(nxt) == len(first) else [first, nxt]


def heights(rungs: Sequence[Partition]) -> list[int]:
    return [len(rung) for rung in rungs]


def unseparated(rungs: Sequence[Partition]) -> list[tuple[Subject, ...]]:
    return [subjects for subjects in rungs[-1] if len(subjects) > 1]
