"""Measure the recorded measurement occurrences, not the material.

Everything so far measures preserved ingress. This measures what Seed did to
it: the recorded measurement occurrences themselves are preserved events, and
counting over them is the same kind of act performed on a different subject.

**Why it is needed.** `#2396` found that ordered material separates from
shuffled material on one source and not another. Reading the five measurement
forms, a reader can see that all five measure exactly one position away, and so
can suspect that what separates is dense immediate arrangement. Seed could not
see that, because the distance was never written down — it lived in the
indexing, and a coordinate that is never recorded cannot be observed to have
never varied.

Each measurement now records where it measured, as coordinates. This surveys
those records and reports, for each coordinate, how many distinct values the
ledger holds.

**It reports variation. It proposes nothing.** A coordinate observed with one
value is reported as a coordinate observed with one value. Nothing here
suggests another value, ranks coordinates, or treats invariance as a defect —
a coordinate may be constant because the forms happen to agree, because the
material permits nothing else, or because a degree of freedom exists and has
never been used, and this survey cannot tell those apart.

Nothing here establishes meaning, relation, or standing. It is a count over
preserved occurrences whose subject happens to be Seed's own acts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from seed_runtime.events import EventLedger
from seed_runtime.preserved_material_measurement import (
    MEASUREMENT_RECORDED_KIND,
    DeclaredMeasurement,
    MeasurementFinding,
    Occupancy,
    PreservedMaterialMeasurementError,
    record_measurement_finding,
)

SELF_SURVEY_SCOPE = (
    "the measurement occurrences recorded by this session; occurrences "
    "elsewhere are not counted and not claimed absent"
)


@dataclass(frozen=True)
class CoordinateVariation:
    """One coordinate of the measured position, and the values observed."""

    coordinate: str
    values: tuple[str, ...]
    occurrence_count: int

    @property
    def varied(self) -> bool:
        """Whether more than one value was observed. Not whether it could vary."""

        return len(self.values) > 1


def surveyed_occurrences(
    ledger: EventLedger, *, workspace_id: str, session_id: str
) -> list:
    """Every recorded measurement occurrence that stated where it measured."""

    return [
        event
        for event in ledger.list(workspace_id)
        if event.session_id == session_id
        and event.kind == MEASUREMENT_RECORDED_KIND
        and event.payload.get("measured_position")
    ]


def survey_measured_positions(
    ledger: EventLedger, *, workspace_id: str, session_id: str
) -> list[CoordinateVariation]:
    """How many distinct values each position coordinate was recorded with."""

    occurrences = surveyed_occurrences(
        ledger, workspace_id=workspace_id, session_id=session_id
    )
    if not occurrences:
        raise PreservedMaterialMeasurementError(
            "no recorded measurement occurrence states where it measured"
        )
    observed: dict[str, dict[str, int]] = {}
    for event in occurrences:
        for coordinate, value in event.payload["measured_position"].items():
            counts = observed.setdefault(coordinate, {})
            key = str(value)
            counts[key] = counts.get(key, 0) + 1
    return [
        CoordinateVariation(
            coordinate=coordinate,
            values=tuple(sorted(counts)),
            occurrence_count=sum(counts.values()),
        )
        for coordinate, counts in sorted(observed.items())
    ]


def record_self_survey(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    variations: list[CoordinateVariation],
) -> Any:
    """Preserve the survey, so what Seed did is consumable like what it measured.

    Recorded through the same boundary as any other finding. Its subject is
    Seed's own occurrences rather than preserved ingress, and its authority is
    the same: measurement evidence only.
    """

    finding = MeasurementFinding(
        declared=DeclaredMeasurement(
            representation_measured=(
                "the position coordinates recorded by this session's "
                "measurement occurrences"
            ),
            equivalence_rule=(
                "byte-for-byte equality of each coordinate's recorded value; "
                "no normalization"
            ),
            counting_scope=SELF_SURVEY_SCOPE,
            form="self_survey",
            relative_to=(),
        ),
        positions_measured=sum(v.occurrence_count for v in variations),
        occupancies=tuple(
            Occupancy(
                representation=f"{v.coordinate}={'|'.join(v.values)}",
                occurrence_count=v.occurrence_count,
            )
            for v in variations
        ),
        consumed_event_ids=tuple(
            event.id
            for event in surveyed_occurrences(
                ledger, workspace_id=workspace_id, session_id=session_id
            )
        ),
    )
    return record_measurement_finding(
        ledger,
        workspace_id=workspace_id,
        session_id=session_id,
        finding=finding,
        extra={
            "coordinates_observed_with_one_value": sorted(
                v.coordinate for v in variations if not v.varied
            ),
            "coordinates_observed_with_several": sorted(
                v.coordinate for v in variations if v.varied
            ),
            # Stated so the record cannot be read as a recommendation.
            "forbidden_inference": (
                "a coordinate observed with one value is not thereby a defect, "
                "a degree of freedom, or an instruction to vary it"
            ),
        },
    )


def render_survey(variations: list[CoordinateVariation]) -> str:
    """Show the survey without commenting on it."""

    rows = ["coordinate        distinct values observed   occurrences"]
    for variation in variations:
        rows.append(
            f"  {variation.coordinate:<16} "
            f"{len(variation.values)}  {{{', '.join(variation.values)}}}"
            f"{'':>6}{variation.occurrence_count}"
        )
    return "\n".join(rows) + "\n"
