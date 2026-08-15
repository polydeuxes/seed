from __future__ import annotations

from pathlib import Path
import shutil
import sys

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import ingest_material


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_material_invocation import (  # noqa: E402
    IngestResultReference,
    MaterialImplementationFunction,
    MaterialAdmissionOccurrence,
    MaterialInvocationOccurrence,
    admit_invocation_occurrences,
    ingest_result_reference,
    reference_occurrences_across,
)
from compiled_format_invocation import (  # noqa: E402
    COMPILED_IMPLEMENTATION_FUNCTIONS as FORMAT_IMPLEMENTATION_FUNCTIONS,
    admit_compiled_invocation_occurrences,
    compiled_reference_invocations,
)
from material_admission import compare_admission_results  # noqa: E402
from material_fixture_media import supplied_media_material  # noqa: E402


IMPLEMENTATION_FUNCTIONS = (
    MaterialImplementationFunction(
        "compiled-0",
        (
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=format_name",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            "pipe:0",
        ),
    ),
    MaterialImplementationFunction(
        "compiled-1",
        ("ffmpeg", "-nostdin", "-v", "error", "-i", "pipe:0", "-f", "null", "-"),
    ),
    MaterialImplementationFunction("compiled-2", ("identify", "-")),
    MaterialImplementationFunction("compiled-3", ("file", "-b", "-")),
    MaterialImplementationFunction(
        "compiled-4",
        (
            "ffmpeg",
            "-nostdin",
            "-v",
            "error",
            "-f",
            "s16le",
            "-ar",
            "48000",
            "-ac",
            "1",
            "-i",
            "pipe:0",
            "-f",
            "null",
            "-",
        ),
    ),
    MaterialImplementationFunction(
        "compiled-5",
        (
            "ffmpeg",
            "-nostdin",
            "-v",
            "error",
            "-f",
            "rawvideo",
            "-pixel_format",
            "rgb24",
            "-video_size",
            "2x2",
            "-i",
            "pipe:0",
            "-frames:v",
            "1",
            "-f",
            "null",
            "-",
        ),
    ),
)


REQUIRED_PROGRAMS = frozenset(
    function.invocation[0] for function in IMPLEMENTATION_FUNCTIONS
) | {"ffmpeg"}
IMPLEMENTATION_FUNCTIONS_AVAILABLE = all(
    shutil.which(program) is not None for program in REQUIRED_PROGRAMS
)


@pytest.fixture(scope="module")
def media_ingests():
    if not IMPLEMENTATION_FUNCTIONS_AVAILABLE:
        pytest.skip("compiled implementation functions are unavailable")
    supplied = supplied_media_material()
    ledger = EventLedger()
    events = tuple(
        ingest_material(
            ledger,
            locality_identity=f"media-material-{position}",
            exact_bytes=material.exact_material,
            source_role="fixture material",
            source_boundary=f"fixture-{position}",
        )
        for position, material in enumerate(supplied)
    )
    references = tuple(
        ingest_result_reference(ledger, event.identity) for event in events
    )
    return supplied, ledger, events, references


@pytest.fixture(scope="module")
def media_invocations(media_ingests):
    references = media_ingests[3]
    return reference_occurrences_across(
        references,
        boundary_identity="media-material-invocation",
        implementation_functions=IMPLEMENTATION_FUNCTIONS,
    )


@pytest.fixture(scope="module")
def media_format_invocations(media_ingests):
    return compiled_reference_invocations(
        media_ingests[3],
        boundary_identity="media-format-invocation",
        implementation_functions=FORMAT_IMPLEMENTATION_FUNCTIONS,
    )


@pytest.fixture(scope="module")
def media_admissions(media_ingests, media_invocations):
    return tuple(
        admit_invocation_occurrences(
            row,
            boundary_identity="media-material-admission",
            occurrence_position=position,
        )
        for position, row in enumerate(media_invocations)
    )


@pytest.fixture(scope="module")
def media_format_admissions(media_format_invocations):
    return tuple(
        admit_compiled_invocation_occurrences(
            row,
            boundary_identity="media-format-admission",
            occurrence_position=position,
        )
        for position, row in enumerate(media_format_invocations)
    )


@pytest.fixture(scope="module")
def all_media_admissions(media_admissions, media_format_admissions):
    return media_admissions + media_format_admissions


@pytest.fixture(scope="module")
def media_admission_compares(media_admissions):
    references = tuple(
        occurrence.result_reference for occurrence in media_admissions
    )
    return tuple(
        compare_admission_results(
            first,
            second,
            boundary_identity="media-material-admission-compare",
            occurrence_position=position,
        )
        for position, (first, second) in enumerate(
            (first, second)
            for first in references
            for second in references
            if first is not second
        )
    )


@pytest.fixture(scope="module")
def all_media_admission_compares(all_media_admissions):
    references = tuple(
        occurrence.result_reference for occurrence in all_media_admissions
    )
    return tuple(
        compare_admission_results(
            first,
            second,
            boundary_identity="all-media-admission-compare",
            occurrence_position=position,
        )
        for position, (first, second) in enumerate(
            (first, second)
            for first in references
            for second in references
            if first is not second
        )
    )


def test_pcm_lossy_audio_and_photo_material_are_exact_fixture_testimony():
    if not IMPLEMENTATION_FUNCTIONS_AVAILABLE:
        pytest.skip("compiled implementation functions are unavailable")
    supplied = supplied_media_material()

    assert tuple(material.testimony for material in supplied) == (
        "pcm-a",
        "pcm-a-again",
        "pcm-b",
        "mp3",
        "ogg-opus",
        "raw-rgb-a",
        "raw-rgb-b",
        "png",
        "jpeg",
    )
    assert supplied[0].exact_material == supplied[1].exact_material
    assert all(type(material.exact_material) is bytes for material in supplied)


def test_each_supplied_material_has_a_fresh_locality_and_exact_ingest_result(
    media_ingests,
):
    supplied, _, events, references = media_ingests

    assert len(events) == len(references) == len(supplied)
    assert len({event.locality_identity for event in events}) == len(events)
    assert len({event.identity for event in events}) == len(events)
    assert len({reference.act_occurrence_identity for reference in references}) == len(
        references
    )
    assert len({reference.result_identity for reference in references}) == len(
        references
    )
    assert len({reference.yield_evidence_identity for reference in references}) == len(
        references
    )
    assert tuple(reference.exact_material for reference in references) == tuple(
        material.exact_material for material in supplied
    )
    assert references[0].exact_material == references[1].exact_material
    assert references[0] != references[1]


def test_every_exact_ingest_result_reaches_every_implementation_function(
    media_ingests, media_invocations
):
    references = media_ingests[3]

    assert len(media_invocations) == len(IMPLEMENTATION_FUNCTIONS)
    assert all(len(row) == len(references) for row in media_invocations)
    assert len(
        {
            occurrence.occurrence_identity
            for row in media_invocations
            for occurrence in row
        }
    ) == len(IMPLEMENTATION_FUNCTIONS) * len(references)
    for row in media_invocations:
        assert tuple(occurrence.source_reference for occurrence in row) == references
        assert tuple(occurrence.exact_material for occurrence in row) == tuple(
            reference.exact_material for reference in references
        )
        assert all(type(occurrence.returncode) is int for occurrence in row)
        assert all(type(occurrence.stdout_bytes) is bytes for occurrence in row)
        assert all(type(occurrence.stderr_bytes) is bytes for occurrence in row)


def test_one_material_ladder_reaches_every_registered_compiled_function(
    media_ingests, media_invocations, media_format_invocations
):
    references = media_ingests[3]
    rows = media_invocations + media_format_invocations
    expected_functions = IMPLEMENTATION_FUNCTIONS + FORMAT_IMPLEMENTATION_FUNCTIONS

    assert len(rows) == len(expected_functions)
    assert tuple(row[0].implementation_function for row in rows) == expected_functions
    assert all(
        tuple(occurrence.source_reference for occurrence in row) == references
        if isinstance(row[0], MaterialInvocationOccurrence)
        else tuple(occurrence.source_coordinate for occurrence in row) == references
        for row in rows
    )
    assert len(
        {
            occurrence.occurrence_identity
            for row in rows
            for occurrence in row
        }
    ) == len(expected_functions) * len(references)


def test_equal_material_keeps_distinct_ingest_and_invocation_occurrences(
    media_ingests, media_invocations
):
    references = media_ingests[3]

    assert references[0].exact_material == references[1].exact_material
    assert references[0].recorded_occurrence_identity != (
        references[1].recorded_occurrence_identity
    )
    for row in media_invocations:
        assert row[0].coordinates == row[1].coordinates
        assert row[0].occurrence_identity != row[1].occurrence_identity
        assert row[0].result_identity != row[1].result_identity
        assert row[0].result_reference.coordinates == (
            row[1].result_reference.coordinates
        )
        assert row[0].result_reference.result_identity != (
            row[1].result_reference.result_identity
        )
        assert row[0].source_reference != row[1].source_reference


def test_each_compiled_function_establishes_one_exact_admission(
    media_ingests, media_invocations, media_admissions
):
    references = media_ingests[3]

    assert len(media_admissions) == len(IMPLEMENTATION_FUNCTIONS)
    for invocation_row, admission in zip(media_invocations, media_admissions):
        assert admission.source_material == references
        assert frozenset(
            material
            for coordinate in admission.admitted_material
            for material in coordinate
        ) == frozenset(references)
        coordinates = {
            reference: occurrence.coordinates
            for reference, occurrence in zip(references, invocation_row)
        }
        for material_at_coordinate in admission.admitted_material:
            assert len(
                {coordinates[material] for material in material_at_coordinate}
            ) == 1


def test_media_implementation_functions_do_not_all_make_one_admission(
    media_admissions,
):
    admitted = {
        admission.admitted_material for admission in media_admissions
    }

    assert len(admitted) > 1
    assert any(len(admission.admitted_material) > 1 for admission in media_admissions)
    assert any(
        len(material) > 1
        for admission in media_admissions
        for material in admission.admitted_material
    )


def test_every_ordered_media_admission_pair_has_an_exact_compare_occurrence(
    media_admissions, media_admission_compares
):
    count = len(media_admissions)

    assert len(media_admission_compares) == count * (count - 1)
    assert len(
        {comparison.act_occurrence_identity for comparison in media_admission_compares}
    ) == len(media_admission_compares)
    assert all(
        comparison.first_reference.source_material
        == comparison.second_reference.source_material
        for comparison in media_admission_compares
    )
    assert all(
        comparison.result_reference.act_occurrence_identity
        == comparison.act_occurrence_identity
        for comparison in media_admission_compares
    )
    for comparison in media_admission_compares:
        assert comparison.first_reference.admission_occurrence in media_admissions
        assert comparison.second_reference.admission_occurrence in media_admissions
        assert (
            comparison.first_reference.admission_occurrence.invocation_result_references
        )
        assert (
            comparison.second_reference.admission_occurrence.invocation_result_references
        )


def test_every_compiled_function_admission_is_compared_in_both_directions(
    all_media_admissions, all_media_admission_compares
):
    count = len(all_media_admissions)

    assert count == len(IMPLEMENTATION_FUNCTIONS) + len(
        FORMAT_IMPLEMENTATION_FUNCTIONS
    )
    assert len(all_media_admission_compares) == count * (count - 1)
    assert {
        (
            comparison.first_reference.result_identity,
            comparison.second_reference.result_identity,
        )
        for comparison in all_media_admission_compares
    } == {
        (first.result_identity, second.result_identity)
        for first in all_media_admissions
        for second in all_media_admissions
        if first is not second
    }
    assert len(
        {
            admission.admitted_material
            for admission in all_media_admissions
        }
    ) > 1


def test_invocation_occurrence_refuses_material_different_from_its_ingest_result():
    reference = IngestResultReference(
        recorded_occurrence_identity="recorded",
        locality_identity="locality",
        act_occurrence_identity="act-occurrence",
        result_identity="result",
        yield_evidence_identity="yield-evidence",
        exact_material=b"a",
    )

    with pytest.raises(ValueError, match="differs from its exact source"):
        MaterialInvocationOccurrence(
            boundary_identity="boundary",
            invocation_position=0,
            exact_material=b"b",
            implementation_function=MaterialImplementationFunction(
                "compiled-0", ("file", "-b", "-")
            ),
            returncode=0,
            stdout_bytes=b"",
            stderr_bytes=b"",
            source_reference=reference,
        )


def test_invocations_refuse_repeated_implementation_function_identity(media_ingests):
    implementation = MaterialImplementationFunction(
        "compiled-0", ("file", "-b", "-")
    )

    with pytest.raises(ValueError, match="identities must be distinct"):
        reference_occurrences_across(
            media_ingests[3],
            boundary_identity="repeated-implementation-function",
            implementation_functions=(implementation, implementation),
        )


def test_material_admission_refuses_a_result_from_another_function(
    media_admissions, media_invocations
):
    admission = media_admissions[0]
    crossed = (
        *admission.invocation_result_references[:-1],
        media_invocations[1][-1].result_reference,
    )

    with pytest.raises(ValueError, match="cannot cross implementation functions"):
        MaterialAdmissionOccurrence(
            admission_occurrence=admission.admission_occurrence,
            invocation_result_references=crossed,
        )
