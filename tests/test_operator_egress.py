from __future__ import annotations

from io import BytesIO

import pytest

FIDELITY_SUBJECT = "exact_emission_boundary"

from seed_runtime.operator_egress import (
    ExactMaterialEgressFailure,
    emit_exact_material,
    operator_emission_boundary,
    read_operator_emission_boundary,
)


def test_operator_emission_boundary_binds_stream_boundary_and_locality():
    output = BytesIO()
    boundary = operator_emission_boundary(
        output,
        boundary_identity="terminal-write",
        locality_identity="operator-terminal",
    )

    assert read_operator_emission_boundary(boundary) == (
        output,
        "terminal-write",
        "operator-terminal",
    )


@pytest.mark.parametrize(
    "boundary",
    (
        [BytesIO(), "terminal-write", "operator-terminal"],
        (BytesIO(), "", "operator-terminal"),
        (BytesIO(), "terminal-write", ""),
    ),
)
def test_operator_emission_boundary_refuses_inferred_or_empty_coordinates(boundary):
    with pytest.raises(TypeError, match="exact operator boundary"):
        read_operator_emission_boundary(boundary)


def test_egress_writes_exact_bytes_without_decoding():
    output = BytesIO()
    material = b"\x00\xff\x80hello"

    assert emit_exact_material(output, material) == len(material)
    assert output.getvalue() == material


def test_egress_refuses_non_bytes():
    with pytest.raises(TypeError, match="exact material bytes"):
        emit_exact_material(BytesIO(), "hello")


def test_egress_refuses_a_short_write():
    class ShortBoundary:
        def write(self, material):
            return len(material) - 1

    with pytest.raises(
        ExactMaterialEgressFailure, match="did not preserve"
    ) as raised:
        emit_exact_material(ShortBoundary(), b"hello")

    assert raised.value.reported_count == 4
    assert raised.value.error is None


def test_egress_does_not_infer_a_count_from_a_write_returning_none():
    class UnreportedBoundary:
        def __init__(self):
            self.material = None

        def write(self, material):
            self.material = material
            return None

    output = UnreportedBoundary()

    with pytest.raises(
        ExactMaterialEgressFailure, match="did not preserve"
    ) as raised:
        emit_exact_material(output, b"hello")

    assert output.material == b"hello"
    assert raised.value.reported_count is None
    assert raised.value.error is None


def test_egress_preserves_a_write_exception_without_inventing_a_count():
    error = OSError("write failed")

    class FailedBoundary:
        def write(self, material):
            raise error

    with pytest.raises(
        ExactMaterialEgressFailure, match="before reporting"
    ) as raised:
        emit_exact_material(FailedBoundary(), b"hello")

    assert raised.value.reported_count is None
    assert raised.value.error is error
    assert raised.value.__cause__ is error


def test_exact_write_acceptance_does_not_claim_or_invoke_a_later_flush():
    class FlushBoundary:
        def __init__(self):
            self.material = None
            self.flush_count = 0

        def write(self, material):
            self.material = material
            return len(material)

        def flush(self):
            self.flush_count += 1

    output = FlushBoundary()

    assert emit_exact_material(output, b"hello") == 5
    assert output.material == b"hello"
    assert output.flush_count == 0


def test_egress_does_not_recast_process_death_as_a_boundary_result():
    class ProcessDeath(BaseException):
        pass

    class DyingBoundary:
        def write(self, material):
            raise ProcessDeath()

    with pytest.raises(ProcessDeath):
        emit_exact_material(DyingBoundary(), b"hello")


def test_egress_carries_exact_bytes_to_a_socket_like_boundary():
    class SocketBoundary:
        def __init__(self):
            self.material = None

        def sendall(self, material):
            self.material = material

    output = SocketBoundary()
    material = b"\x00video-like-bytes"

    assert emit_exact_material(output, material) == len(material)
    assert output.material == material
