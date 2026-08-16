from __future__ import annotations

import os
import subprocess

import pytest

from scripts import operator_host_provider


class _PopenReached(Exception):
    pass


@pytest.mark.parametrize(
    ("command", "argv"),
    (
        (b"!ls\n", (b"/usr/bin/ls",)),
        (
            b"!cat path with spaces\r\n",
            (b"/usr/bin/cat", b"--", b"path with spaces"),
        ),
        (b"!ls\t\xff\n", (b"/usr/bin/ls", b"--", b"\xff")),
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
        operator_host_provider.invoke_operator_host(command)

    assert calls[0][0] == argv
    assert calls[0][1]["shell"] is False
    assert calls[0][1]["stdin"] is subprocess.DEVNULL


@pytest.mark.parametrize("command", (b"!sh\n", b"!cat a\x00b\n", b"ls\n"))
def test_unknown_or_unrepresentable_host_invocation_is_refused_before_process(
    monkeypatch, command
):
    monkeypatch.setattr(
        subprocess,
        "Popen",
        lambda *args, **kwargs: pytest.fail((args, kwargs)),
    )
    with pytest.raises(operator_host_provider.OperatorHostProviderError):
        operator_host_provider.invoke_operator_host(command)


def test_cat_preserves_exact_posix_path_and_material(tmp_path):
    directory = os.fsencode(tmp_path)
    path = directory + b"/material-\xff"
    exact = b"\x00\xffexact material\n"
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(descriptor, exact)
    finally:
        os.close(descriptor)

    supplied = operator_host_provider.invoke_operator_host(
        b"!cat " + path + b"\n"
    )

    assert supplied.output_material.exact_bytes == exact
    assert supplied.error_material.exact_bytes == b""
    assert supplied.end_material.exact_bytes == b""
    assert len(
        {
            supplied.output_material.source_boundary,
            supplied.error_material.source_boundary,
            supplied.end_material.source_boundary,
        }
    ) == 3


def test_ls_preserves_a_non_utf8_posix_path(tmp_path):
    directory = os.fsencode(tmp_path)
    name = b"entry-\xff"
    path = directory + b"/" + name
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    os.close(descriptor)

    supplied = operator_host_provider.invoke_operator_host(
        b"!ls " + directory + b"\n"
    )

    assert supplied.output_material.exact_bytes == name + b"\n"
    assert supplied.error_material.exact_bytes == b""
    assert supplied.end_material.exact_bytes == b""


def test_host_output_is_bounded_without_returncode_material():
    supplied = operator_host_provider.invoke_operator_host(b"!cat /dev/zero\n")

    assert len(supplied.output_material.exact_bytes) == (
        operator_host_provider.MATERIAL_BYTE_LIMIT
    )
    assert supplied.output_material.known_loss
    assert supplied.end_material.exact_bytes == b""
