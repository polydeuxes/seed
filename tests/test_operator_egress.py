from __future__ import annotations

from io import BytesIO
import os

try:
    import fcntl
except ImportError:  # pragma: no cover - Linux owns this kernel witness.
    fcntl = None

import pytest


from seed_runtime.operator_egress import (
    EXACT_MATERIAL_WRITE_BOUNDARY_RULE,
    ExactMaterialEgressFailure,
    emit_exact_material,
    operator_emission_boundary,
    read_operator_emission_boundary,
)


def test_operator_emission_boundary_binds_stream_boundary_and_locality():
    output = BytesIO()
    boundary = operator_emission_boundary(
        output,
        boundary_identity="exact-material-write",
        locality_identity="operator-locality",
        boundary_rule=EXACT_MATERIAL_WRITE_BOUNDARY_RULE,
    )

    assert read_operator_emission_boundary(boundary) == (
        output,
        "exact-material-write",
        "operator-locality",
        EXACT_MATERIAL_WRITE_BOUNDARY_RULE,
    )


@pytest.mark.parametrize(
    "boundary",
    (
        [BytesIO(), "exact-material-write", "operator-locality", EXACT_MATERIAL_WRITE_BOUNDARY_RULE],
        (BytesIO(), "", "operator-locality", EXACT_MATERIAL_WRITE_BOUNDARY_RULE),
        (BytesIO(), "exact-material-write", "", EXACT_MATERIAL_WRITE_BOUNDARY_RULE),
        (BytesIO(), "exact-material-write", "operator-locality", ""),
        (BytesIO(), "exact-material-write", "operator-locality", None),
    ),
)
def test_operator_emission_boundary_refuses_inferred_or_empty_coordinates(boundary):
    with pytest.raises(TypeError, match="exact operator boundary"):
        read_operator_emission_boundary(boundary)


def test_operator_emission_boundary_requires_one_exact_writable_boundary():
    with pytest.raises(TypeError, match="writable boundary"):
        operator_emission_boundary(
            object(),
            boundary_identity="exact-material-write",
            locality_identity="operator-locality",
            boundary_rule=EXACT_MATERIAL_WRITE_BOUNDARY_RULE,
        )


def test_operator_emission_boundary_refuses_a_later_lost_write_capability():
    class MutableBoundary:
        def write(self, material):
            return len(material)

    output = MutableBoundary()
    boundary = operator_emission_boundary(
        output,
        boundary_identity="exact-material-write",
        locality_identity="operator-locality",
        boundary_rule=EXACT_MATERIAL_WRITE_BOUNDARY_RULE,
    )
    output.write = None

    with pytest.raises(TypeError, match="writable boundary"):
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


@pytest.mark.skipif(
    fcntl is None or not hasattr(fcntl, "F_GETPIPE_SZ"),
    reason="Linux pipe coordinates are unavailable",
)
def test_egress_refuses_a_short_write_reported_by_a_linux_pipe():
    read_fd, write_fd = os.pipe()
    try:
        os.set_blocking(write_fd, False)
        capacity = fcntl.fcntl(write_fd, fcntl.F_GETPIPE_SZ)
        filled = 0
        while filled < capacity:
            filled += os.write(write_fd, b"x" * (capacity - filled))

        pipe_atomic_write_limit = os.fpathconf(write_fd, "PC_PIPE_BUF")
        assert len(os.read(read_fd, pipe_atomic_write_limit)) == (
            pipe_atomic_write_limit
        )
        material = b"y" * (pipe_atomic_write_limit * 2)
        with os.fdopen(write_fd, "wb", buffering=0, closefd=False) as output:
            with pytest.raises(
                ExactMaterialEgressFailure, match="did not preserve"
            ) as raised:
                emit_exact_material(output, material)

        assert raised.value.reported_count == pipe_atomic_write_limit
        assert raised.value.error is None
    finally:
        os.close(write_fd)
        os.close(read_fd)


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


def test_egress_refuses_a_socket_like_boundary_reporting_partial_completion():
    class PartialSocketBoundary:
        def __init__(self):
            self.material = None

        def sendall(self, material):
            self.material = material[:-1]
            return len(self.material)

    output = PartialSocketBoundary()
    with pytest.raises(
        ExactMaterialEgressFailure, match="did not preserve"
    ) as raised:
        emit_exact_material(output, b"hello")

    assert output.material == b"hell"
    assert raised.value.reported_count == 4
    assert raised.value.error is None
