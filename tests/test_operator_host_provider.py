from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import time

import pytest

from scripts import operator_host_provider
from seed_runtime.supplied_invocation_material import (
    SuppliedWitnessMaterialOccurrence,
)


class _PopenReached(Exception):
    pass


def _invoke(command):
    supplied = []
    result = operator_host_provider.invoke_operator_host(
        command, supplied.append
    )
    assert result is None
    return tuple(supplied)


@pytest.mark.parametrize(
    ("command", "argv"),
    (
        (b"!ls\n", (b"/usr/bin/ls",)),
        (
            b"!calculator 2+2\n",
            (b"/usr/bin/gnome-calculator", b"--solve=2+2"),
        ),
        (
            b"!cat path with spaces\r\n",
            (b"/usr/bin/cat", b"--", b"path with spaces"),
        ),
        (b"!ls\t\xff\n", (b"/usr/bin/ls", b"--", b"\xff")),
        (
            b"!pytest tests/exact.py::test_one\n",
            (
                *operator_host_provider._PYTEST_INVOCATION,
                b"tests/exact.py::test_one",
            ),
        ),
    ),
)
def test_host_provider_uses_only_fixed_argv_without_a_shell(
    monkeypatch, command, argv
):
    calls = []

    def reached(supplied_argv, **kwargs):
        calls.append((supplied_argv, kwargs))
        raise _PopenReached

    monkeypatch.setattr(subprocess, "Popen", reached)
    with pytest.raises(_PopenReached):
        operator_host_provider.invoke_operator_host(command, lambda _item: None)

    assert calls[0][0] == argv
    assert calls[0][1]["shell"] is False
    assert calls[0][1]["stdin"] is subprocess.DEVNULL


def test_pytest_provider_has_one_exact_argument_and_a_clean_environment(
    monkeypatch,
):
    calls = []

    def reached(supplied_argv, **kwargs):
        calls.append((supplied_argv, kwargs))
        raise _PopenReached

    monkeypatch.setenv("PYTEST_ADDOPTS", "developer supplied")
    monkeypatch.setattr(subprocess, "Popen", reached)
    with pytest.raises(_PopenReached):
        operator_host_provider.invoke_operator_host(
            b"!pytest tests/path with spaces.py::test_one\n",
            lambda _item: None,
        )

    argv, coordinates = calls[0]
    assert argv == (
        *operator_host_provider._PYTEST_INVOCATION,
        b"tests/path with spaces.py::test_one",
    )
    assert coordinates["env"] == {
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "SEED_IMPLEMENTATION_FUNCTION_CATALOG": coordinates["env"][
            "SEED_IMPLEMENTATION_FUNCTION_CATALOG"
        ],
        "SEED_IMPLEMENTATION_FUNCTION_MEASUREMENT": coordinates["env"][
            "SEED_IMPLEMENTATION_FUNCTION_MEASUREMENT"
        ],
    }
    assert coordinates["cwd"] == operator_host_provider._ROOT
    assert "PYTEST_ADDOPTS" not in coordinates["env"]


@pytest.mark.parametrize(
    "command",
    (
        b"!sh\n",
        b"!cat a\x00b\n",
        b"!pytest a\x00b\n",
        b"!calculator\n",
        b"!calculator 2+\x002\n",
        b"ls\n",
    ),
)
def test_unknown_or_unrepresentable_host_invocation_is_refused_before_process(
    monkeypatch, command
):
    monkeypatch.setattr(
        subprocess,
        "Popen",
        lambda *args, **kwargs: pytest.fail((args, kwargs)),
    )
    with pytest.raises(operator_host_provider.OperatorHostProviderError):
        operator_host_provider.invoke_operator_host(command, lambda _item: None)


def test_calculator_provider_preserves_supplied_material_and_completion(
    monkeypatch,
):
    def bounded(
        argv,
        *,
        supply,
        time_limit_second_count,
        material_byte_count_limit,
    ):
        assert argv == (
            b"/usr/bin/gnome-calculator",
            b"--solve=2+2",
        )
        assert (
            time_limit_second_count
            == operator_host_provider.TIME_LIMIT_SECOND_COUNT
        )
        assert (
            material_byte_count_limit
            == operator_host_provider.MATERIAL_BYTE_COUNT_LIMIT
        )
        supply(
            SuppliedWitnessMaterialOccurrence(
                b"exact output material",
                "invocation output occurrence 0",
            )
        )
        supply(
            SuppliedWitnessMaterialOccurrence(
                b"exact error material",
                "invocation error occurrence 0",
            )
        )
        return False, False, False

    monkeypatch.setattr(operator_host_provider, "_bounded_invocation", bounded)

    supplied = _invoke(b"!calculator 2+2\n")

    assert supplied == (
        SuppliedWitnessMaterialOccurrence(
            b"exact output material",
            "invocation output occurrence 0",
        ),
        SuppliedWitnessMaterialOccurrence(
            b"exact error material",
            "invocation error occurrence 0",
        ),
        SuppliedWitnessMaterialOccurrence(
            b"",
            "invocation completion",
        ),
    )


def test_cat_preserves_exact_posix_path_and_material(tmp_path):
    directory = os.fsencode(tmp_path)
    path = directory + b"/material-\xff"
    exact = b"\x00\xffexact material\n"
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(descriptor, exact)
    finally:
        os.close(descriptor)

    supplied = _invoke(b"!cat " + path + b"\n")

    assert tuple(occurrence.exact_bytes for occurrence in supplied) == (
        exact,
        b"",
        b"",
    )
    assert len({occurrence.source_boundary for occurrence in supplied}) == 3


def test_ls_preserves_a_non_utf8_posix_path(tmp_path):
    directory = os.fsencode(tmp_path)
    name = b"entry-\xff"
    path = directory + b"/" + name
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    os.close(descriptor)

    supplied = _invoke(b"!ls " + directory + b"\n")

    assert tuple(occurrence.exact_bytes for occurrence in supplied) == (
        name + b"\n",
        b"",
        b"",
    )


def test_host_material_boundary_is_one_mebibyte():
    assert operator_host_provider.MATERIAL_BYTE_COUNT_LIMIT == 1_048_576


def test_cat_preserves_finite_material_across_multiple_pipe_reads(tmp_path):
    exact = (bytes(range(256)) * 851) + bytes(range(256))[:202]
    assert len(exact) == 218_058
    path = tmp_path / "multiple-pipe-reads"
    path.write_bytes(exact)

    supplied = _invoke(b"!cat " + bytes(path) + b"\n")
    output = next(
        occurrence
        for occurrence in supplied
        if occurrence.source_boundary == "invocation output"
    )

    assert output.exact_bytes == exact
    assert tuple(
        len(occurrence.exact_bytes)
        for occurrence in output.read_occurrences
    ) == (
        65_536,
        65_536,
        65_536,
        21_450,
    )
    assert b"".join(
        occurrence.exact_bytes for occurrence in output.read_occurrences
    ) == exact
    assert tuple(
        occurrence.invocation_position
        for occurrence in output.read_occurrences
    ) == tuple(sorted(
        occurrence.invocation_position
        for occurrence in output.read_occurrences
    ))
    assert all(occurrence.known_loss == () for occurrence in supplied)


def test_host_output_is_bounded_without_returncode_material():
    supplied = _invoke(b"!cat /dev/zero\n")

    output = next(
        occurrence
        for occurrence in supplied
        if occurrence.source_boundary == "invocation output"
    )
    assert len(output.exact_bytes) == (
        operator_host_provider.MATERIAL_BYTE_COUNT_LIMIT
    )
    assert tuple(
        occurrence.source_boundary for occurrence in output.read_occurrences
    ) == tuple(
        f"invocation output read {position}"
        for position in range(len(output.read_occurrences))
    )
    assert output.known_loss
    assert supplied[-1].exact_bytes == b""
    assert supplied[-1].known_loss


def test_bounded_invocation_uses_its_exact_material_byte_count_limit():
    supplied = []

    timed_out, output_limited, error_limited = (
        operator_host_provider._bounded_invocation(
            (b"/usr/bin/printf", b"abcdef"),
            supply=supplied.append,
            time_limit_second_count=1.0,
            material_byte_count_limit=3,
        )
    )

    assert not timed_out
    assert output_limited
    assert not error_limited
    assert tuple(occurrence.exact_bytes for occurrence in supplied) == (
        b"abc",
        b"",
    )


@pytest.mark.parametrize(
    ("time_limit_second_count", "material_byte_count_limit"),
    (
        (0.0, 3),
        (1, 3),
        (1.0, 0),
        (1.0, 3.0),
    ),
)
def test_bounded_invocation_refuses_invalid_exact_limits_before_process(
    monkeypatch,
    time_limit_second_count,
    material_byte_count_limit,
):
    monkeypatch.setattr(
        subprocess,
        "Popen",
        lambda *args, **kwargs: pytest.fail((args, kwargs)),
    )

    with pytest.raises(TypeError):
        operator_host_provider._bounded_invocation(
            (b"/usr/bin/printf", b"exact"),
            supply=lambda _occurrence: None,
            time_limit_second_count=time_limit_second_count,
            material_byte_count_limit=material_byte_count_limit,
        )


def test_completed_invocation_is_not_recast_as_timed_out_by_a_slow_consumer(
    monkeypatch,
):
    supplied = []

    def slow_consumer(occurrence):
        supplied.append(occurrence)
        if len(supplied) == 1:
            time.sleep(0.03)

    timed_out, output_limited, error_limited = (
        operator_host_provider._bounded_invocation(
            (b"/usr/bin/printf", b"exact"),
            supply=slow_consumer,
            time_limit_second_count=0.01,
            material_byte_count_limit=64,
        )
    )

    assert not timed_out
    assert not output_limited
    assert not error_limited
    assert tuple(occurrence.exact_bytes for occurrence in supplied) == (
        b"exact",
        b"",
    )


def test_inherited_open_pipe_is_bounded_without_recasting_parent_as_timed_out(
    monkeypatch,
):
    supplied = []
    program = (
        b"import os,time\n"
        b"if os.fork() == 0:\n"
        b" time.sleep(0.5)\n"
        b" os._exit(0)\n"
        b"os.write(1,b'exact')\n"
        b"os._exit(0)\n"
    )

    timed_out, output_limited, error_limited = (
        operator_host_provider._bounded_invocation(
            (operator_host_provider._PYTEST_INVOCATION[0], b"-c", program),
            supply=supplied.append,
            time_limit_second_count=0.05,
            material_byte_count_limit=64,
        )
    )

    assert not timed_out
    assert output_limited
    assert error_limited
    assert tuple(occurrence.exact_bytes for occurrence in supplied) == (
        b"exact",
        b"",
    )


def test_pytest_provider_supplies_a_distinct_exact_measurement_artifact():
    nodeid = (
        b"tests/test_implementation_function_measurement.py::"
        b"test_compiled_code_supplies_exact_identities"
    )

    supplied = _invoke(b"!pytest " + nodeid + b"\n")

    by_boundary = {
        occurrence.source_boundary: occurrence
        for occurrence in supplied
    }
    invocation_output = tuple(
        occurrence
        for occurrence in supplied
        if occurrence.source_boundary in ("invocation output", "invocation error")
    )
    assert invocation_output
    assert all(
        occurrence.source_boundary in ("invocation output", "invocation error")
        for occurrence in invocation_output
    )
    assert {
        "implementation function catalog",
        "implementation function measurement",
        "invocation completion",
    } <= set(by_boundary)
    assert any(
        occurrence.exact_bytes
        for occurrence in invocation_output
        if occurrence.source_boundary == "invocation output"
    )
    catalog_occurrence = by_boundary["implementation function catalog"]
    artifact_occurrence = by_boundary["implementation function measurement"]
    catalog = json.loads(catalog_occurrence.exact_bytes)
    artifact = json.loads(artifact_occurrence.exact_bytes)
    assert [occurrence["pytest_identity"] for occurrence in artifact["pytest"]] == [
        nodeid.decode("ascii")
    ]
    assert artifact["pytest"][0]["fidelity_distinction_reference"] == [
        "book_coordinates",
        "01.Source.C",
    ]
    assert "test_subject" not in artifact["pytest"][0]
    assert "witness_for" not in artifact["pytest"][0]
    assert "distinct_from" not in artifact["pytest"][0]
    implementation_positions = {
        coordinate["implementation_function_position"]
        for coordinate in artifact["pytest"][0]["python"]
    }
    assert implementation_positions
    assert all(
        position < len(catalog["python"])
        for position in implementation_positions
    )
    assert catalog_occurrence.known_loss == ()
    assert artifact_occurrence.known_loss == ()
    assert len(artifact_occurrence.exact_bytes) < 5000
    assert by_boundary["invocation completion"].exact_bytes == b""


def test_repeated_pytest_reuses_one_exact_catalog_and_keeps_observation_sparse():
    command = (
        b"!pytest tests/test_implementation_function_measurement.py::"
        b"test_compiled_code_supplies_exact_identities\n"
    )

    first = _invoke(command)
    second = _invoke(command)

    first_by_boundary = {
        occurrence.source_boundary: occurrence for occurrence in first
    }
    second_by_boundary = {
        occurrence.source_boundary: occurrence for occurrence in second
    }
    first_catalog = first_by_boundary["implementation function catalog"]
    second_catalog = second_by_boundary["implementation function catalog"]
    assert first_catalog.exact_bytes == second_catalog.exact_bytes
    assert first_catalog is not second_catalog
    assert len(
        first_by_boundary["implementation function measurement"].exact_bytes
    ) < 5000
    assert len(
        second_by_boundary["implementation function measurement"].exact_bytes
    ) < 5000


def test_admitted_implementation_test_has_no_fidelity_or_witness_uptake():
    supplied = _invoke(
        b"!pytest tests/test_events.py::test_append_records_reality_in_order\n"
    )
    measurement = next(
        occurrence
        for occurrence in supplied
        if occurrence.source_boundary == "implementation function measurement"
    )
    artifact = json.loads(measurement.exact_bytes)

    assert artifact["pytest"] == []
    assert artifact["witness_material"] == []


def test_missing_pytest_measurement_artifact_is_refused(monkeypatch):
    monkeypatch.setattr(
        operator_host_provider,
        "_bounded_invocation",
        lambda *args, **kwargs: (False, False, False),
    )

    with pytest.raises(
        operator_host_provider.OperatorHostProviderError,
        match="exact implementation measurement material required",
    ):
        _invoke(b"!pytest tests/exact.py\n")


@pytest.mark.parametrize(
    ("timed_out", "output_limited", "error_limited"),
    (
        (True, False, False),
        (False, True, False),
        (False, False, True),
    ),
)
def test_bounded_pytest_preserves_partial_results_and_known_artifact_loss(
    monkeypatch, timed_out, output_limited, error_limited
):
    def bounded(*args, supply, **kwargs):
        supply(
            SuppliedWitnessMaterialOccurrence(
                b"partial out",
                "invocation output occurrence 0",
            )
        )
        supply(
            SuppliedWitnessMaterialOccurrence(
                b"partial error",
                "invocation error occurrence 0",
            )
        )
        return timed_out, output_limited, error_limited

    monkeypatch.setattr(
        operator_host_provider,
        "_bounded_invocation",
        bounded,
    )

    supplied = _invoke(b"!pytest tests/exact.py\n")

    assert tuple(occurrence.exact_bytes for occurrence in supplied) == (
        b"partial out",
        b"partial error",
        b"",
        b"",
        b"",
    )
    assert supplied[0].known_loss == ()
    assert supplied[1].known_loss == ()
    assert all(supplied[position].known_loss for position in (2, 3, 4))


def test_pytest_measurement_artifact_is_bounded(tmp_path):
    path = tmp_path / "measurement"
    exact = b"x" * (operator_host_provider.IMPLEMENTATION_MEASUREMENT_BYTE_LIMIT + 1)
    path.write_bytes(exact)

    material, limited = operator_host_provider._bounded_artifact(path)

    assert material == exact[:-1]
    assert limited is True


def test_pytest_provider_death_is_not_replaced_by_supplied_results(monkeypatch):
    def die(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(operator_host_provider, "_bounded_invocation", die)

    with pytest.raises(KeyboardInterrupt):
        _invoke(b"!pytest tests/exact.py\n")


PYTEST_ADMISSION = (
    test_host_provider_uses_only_fixed_argv_without_a_shell,
    test_pytest_provider_has_one_exact_argument_and_a_clean_environment,
    test_unknown_or_unrepresentable_host_invocation_is_refused_before_process,
    test_calculator_provider_preserves_supplied_material_and_completion,
    test_cat_preserves_exact_posix_path_and_material,
    test_ls_preserves_a_non_utf8_posix_path,
    test_host_material_boundary_is_one_mebibyte,
    test_bounded_invocation_refuses_invalid_exact_limits_before_process,
    test_bounded_invocation_uses_its_exact_material_byte_count_limit,
    test_cat_preserves_finite_material_across_multiple_pipe_reads,
    test_host_output_is_bounded_without_returncode_material,
    test_completed_invocation_is_not_recast_as_timed_out_by_a_slow_consumer,
    test_inherited_open_pipe_is_bounded_without_recasting_parent_as_timed_out,
    test_pytest_provider_supplies_a_distinct_exact_measurement_artifact,
    test_repeated_pytest_reuses_one_exact_catalog_and_keeps_observation_sparse,
    test_admitted_implementation_test_has_no_fidelity_or_witness_uptake,
    test_missing_pytest_measurement_artifact_is_refused,
    test_bounded_pytest_preserves_partial_results_and_known_artifact_loss,
    test_pytest_measurement_artifact_is_bounded,
    test_pytest_provider_death_is_not_replaced_by_supplied_results,
)
