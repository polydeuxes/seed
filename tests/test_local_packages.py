import os
import subprocess
from datetime import datetime, timezone

from seed_runtime.events import EventLedger
from seed_runtime.local_packages import (
    PackageRecord,
    package_records_to_observations,
    parse_dpkg_status,
)
from seed_runtime.observation_sources import (
    FakeObservationSource,
    LocalHostObservationSource,
    ObservationCollectionService,
)
from seed_runtime.observations import ObservationIngestor
from seed_runtime.state import StateProjector

BASE_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)

INSTALLED_RECORD = """Package: curl
Status: install ok installed
Architecture: amd64
Version: 8.5.0-2ubuntu10.6
Description: command line tool for transferring data with URL syntax
"""

SKIPPED_RECORD = """Package: oldpkg
Status: deinstall ok config-files
Architecture: amd64
Version: 1.0
"""


def test_parse_dpkg_status_installed_records_parse_deterministically():
    assert parse_dpkg_status(INSTALLED_RECORD) == [
        PackageRecord(
            name="curl",
            manager="dpkg",
            installed=True,
            version="8.5.0-2ubuntu10.6",
            architecture="amd64",
        )
    ]


def test_parse_dpkg_status_skips_non_installed_config_files_records():
    assert parse_dpkg_status(SKIPPED_RECORD) == []


def test_parse_dpkg_status_skips_malformed_missing_package_and_missing_status_safely():
    fixture = """Package curl
Status: install ok installed
Architecture: amd64
Version: 1

Status: install ok installed
Architecture: amd64
Version: 1

Package: missing-status
Architecture: amd64
Version: 1

Package: unpacked
Status: install ok unpacked
Architecture: amd64
Version: 1
"""

    assert parse_dpkg_status(fixture) == []


def test_parse_dpkg_status_multi_record_fixtures_are_deterministic():
    fixture = f"""{SKIPPED_RECORD}
{INSTALLED_RECORD}
Package: zlib1g
Status: install ok installed
Architecture: amd64
Version: 1:1.3.dfsg-3.1ubuntu2
"""

    records = parse_dpkg_status(fixture)

    assert records == [
        PackageRecord(
            name="curl",
            manager="dpkg",
            installed=True,
            version="8.5.0-2ubuntu10.6",
            architecture="amd64",
        ),
        PackageRecord(
            name="zlib1g",
            manager="dpkg",
            installed=True,
            version="1:1.3.dfsg-3.1ubuntu2",
            architecture="amd64",
        ),
    ]


def test_package_records_emit_generic_host_subject_package_predicates_only():
    observations = package_records_to_observations(
        "node115",
        [
            PackageRecord(
                name="curl",
                manager="dpkg",
                version="8.5.0-2ubuntu10.6",
                architecture="amd64",
            )
        ],
        BASE_TIME,
        "discovery",
    )

    triples = {(obs.subject, obs.predicate, obs.value) for obs in observations}
    assert triples == {
        ("node115", "package_installed", "curl"),
        ("node115", "package_version", "8.5.0-2ubuntu10.6"),
        ("node115", "package_architecture", "amd64"),
        ("node115", "package_manager", "dpkg"),
    }
    assert all(obs.subject == "node115" for obs in observations)
    assert all(
        obs.dimensions == {"package_name": "curl", "package_manager": "dpkg"}
        for obs in observations
    )
    assert all(not obs.predicate.startswith("dpkg_") for obs in observations)


def test_package_observations_do_not_introduce_entities_relationships_or_inferences():
    observations = package_records_to_observations(
        "node115",
        [PackageRecord(name="curl", manager="dpkg", version="8.5.0", architecture="amd64")],
        BASE_TIME,
        "discovery",
    )
    ledger = EventLedger()

    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        FakeObservationSource(observations, source_type="discovery"), "ws_packages"
    )
    state = StateProjector(ledger).project("ws_packages")

    assert state.entities == {}
    assert state.relationships == []
    forbidden_predicates = {
        "service_running",
        "service_status",
        "capability_available",
        "capability_verified",
        "process_running",
        "listening_endpoint",
        "listening_protocol",
        "listening_address",
        "listening_port",
        "vulnerability_present",
        "patch_status",
        "availability_status",
    }
    emitted_predicates = {obs.predicate for obs in observations}
    assert emitted_predicates.isdisjoint(forbidden_predicates)
    assert all(obs.metadata["service_inferred"] is False for obs in observations)
    assert all(obs.metadata["capability_inferred"] is False for obs in observations)
    assert all(obs.metadata["process_inferred"] is False for obs in observations)
    assert all(obs.metadata["port_inferred"] is False for obs in observations)
    assert all(obs.metadata["vulnerability_inferred"] is False for obs in observations)


def test_local_package_collection_reads_only_dpkg_status_without_cli_network_or_repos(
    monkeypatch, tmp_path
):
    from seed_runtime import observation_sources as sources

    def fail_forbidden(*args, **kwargs):  # pragma: no cover - guard callback
        raise AssertionError("package observation must not execute or use network")

    status = tmp_path / "status"
    status.write_text(f"{INSTALLED_RECORD}\n{SKIPPED_RECORD}", encoding="utf-8")

    monkeypatch.setattr(os, "system", fail_forbidden)
    monkeypatch.setattr(subprocess, "run", fail_forbidden)
    monkeypatch.setattr(subprocess, "Popen", fail_forbidden)
    monkeypatch.setattr(sources.socket, "create_connection", fail_forbidden)
    monkeypatch.setattr(sources.socket, "getaddrinfo", fail_forbidden)
    monkeypatch.setattr(sources, "urlopen", fail_forbidden)

    source = LocalHostObservationSource(dpkg_status=status)
    observations = source._collect_local_package_observations(BASE_TIME, "node115")

    assert {(obs.predicate, obs.value) for obs in observations} == {
        ("package_installed", "curl"),
        ("package_version", "8.5.0-2ubuntu10.6"),
        ("package_architecture", "amd64"),
        ("package_manager", "dpkg"),
    }
    assert all(obs.metadata["package_manager_cli_called"] is False for obs in observations)
    assert all(obs.metadata["repository_inspected"] is False for obs in observations)
    assert all(obs.metadata["lock_inspected"] is False for obs in observations)


def test_package_current_facts_and_fact_support_expose_dimensioned_package_facts():
    observations = package_records_to_observations(
        "node115",
        [
            PackageRecord(
                name="curl",
                manager="dpkg",
                version="8.5.0-2ubuntu10.6",
                architecture="amd64",
            )
        ],
        BASE_TIME,
        "discovery",
    )
    ledger = EventLedger()

    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        FakeObservationSource(observations, source_type="discovery"), "ws_package_facts"
    )
    state = StateProjector(ledger).project("ws_package_facts")

    dimensions = {"package_name": "curl", "package_manager": "dpkg"}
    assert state.get_current_facts("node115", "package_installed")
    assert state.get_current_facts("node115", "package_version")
    assert state.get_current_facts("node115", "package_architecture")
    assert state.get_current_facts("node115", "package_manager")
    support = state.get_fact_support(
        "node115", "package_version", dimensions=dimensions
    )
    assert support is not None
    assert support.value == "8.5.0-2ubuntu10.6"
    assert support.dimensions == dimensions
    assert support.source_types == ["discovery"]
