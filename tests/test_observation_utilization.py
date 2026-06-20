import json
from pathlib import Path

from scripts import seed_local
from seed_runtime.observation_utilization import (
    build_observation_utilization_audit,
    format_observation_utilization,
    observation_utilization_json,
)


def test_cli_observation_utilization_renders(capsys):
    assert seed_local.main(["--observation-utilization"]) == 0
    out = capsys.readouterr().out
    assert "Observation Utilization Audit" in out
    assert "Predicate | Providers | Collected | Projected | Read Model | Diagnostic | First Loss" in out
    assert "Dead-zone visibility" in out


def test_cli_observation_utilization_json_is_valid(capsys):
    assert seed_local.main(["--observation-utilization", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert set(payload) == {"summary", "predicates", "metadata"}
    assert payload["predicates"]
    assert set(payload["predicates"][0]) >= {
        "predicate",
        "provider_count",
        "collected",
        "projected",
        "read_model",
        "diagnostic_consumed",
        "first_loss",
    }


def test_predicates_are_discovered_from_observation_inventory_implementation():
    audit = build_observation_utilization_audit()
    predicates = {row.predicate for row in audit.predicates}
    assert {"os", "hostname", "up"} <= predicates
    source = Path("seed_runtime/observation_utilization.py").read_text()
    assert "OBSERVATION_UTILIZATION" not in source
    assert "local_host" not in source


def test_projected_read_model_and_diagnostic_participation_are_detected(tmp_path):
    runtime = tmp_path / "seed_runtime"
    runtime.mkdir()
    (runtime / "observation_sources.py").write_text(
        '''
class UsedObservationSource:
    name = "used"
    source_type = "fixture"
    def collect(self):
        return [Observation(subject="s", predicate="used_predicate", value="v")]
''',
        encoding="utf-8",
    )
    (runtime / "state.py").write_text('"used_predicate"', encoding="utf-8")
    (runtime / "state_views.py").write_text('"used_predicate"', encoding="utf-8")
    (runtime / "ownership_discrepancies.py").write_text('"used_predicate"', encoding="utf-8")
    row = build_observation_utilization_audit(tmp_path).predicates[0]
    assert row.projected
    assert row.read_model
    assert row.diagnostic_consumed
    assert row.first_loss == "none"


def test_unused_predicates_and_first_loss_are_identified(tmp_path):
    runtime = tmp_path / "seed_runtime"
    runtime.mkdir()
    (runtime / "observation_sources.py").write_text(
        '''
class DeadObservationSource:
    name = "dead"
    source_type = "fixture"
    def collect(self):
        return [Observation(subject="s", predicate="dead_predicate", value="v")]
''',
        encoding="utf-8",
    )
    audit = build_observation_utilization_audit(tmp_path)
    row = audit.predicates[0]
    assert row.predicate == "dead_predicate"
    assert row.collected
    assert not row.projected
    assert not row.read_model
    assert not row.diagnostic_consumed
    assert row.first_loss == "unused"
    assert audit.summary["unused_predicates"] == 1
    assert "dead_predicate: unused" in format_observation_utilization(audit)


def test_first_loss_classification_for_each_stage(tmp_path):
    runtime = tmp_path / "seed_runtime"
    runtime.mkdir()
    (runtime / "observation_sources.py").write_text(
        '''
class FixtureObservationSource:
    name = "fixture"
    source_type = "fixture"
    def collect(self):
        return [
            Observation(subject="s", predicate="projected_only", value="v"),
            Observation(subject="s", predicate="read_only", value="v"),
            Observation(subject="s", predicate="fully_used", value="v"),
        ]
''',
        encoding="utf-8",
    )
    (runtime / "state.py").write_text('"projected_only" "read_only" "fully_used"', encoding="utf-8")
    (runtime / "state_views.py").write_text('"read_only" "fully_used"', encoding="utf-8")
    (runtime / "ownership_discrepancies.py").write_text('"fully_used"', encoding="utf-8")
    audit = build_observation_utilization_audit(tmp_path)
    losses = {row.predicate: row.first_loss for row in audit.predicates}
    assert losses == {
        "fully_used": "none",
        "projected_only": "read_model_loss",
        "read_only": "diagnostic_loss",
    }


def test_filtering_works_for_predicate_and_provider():
    provider_audit = build_observation_utilization_audit(provider_filter="systemd")
    assert provider_audit.predicates
    assert all("systemd" in row.providers for row in provider_audit.predicates)
    predicate_audit = build_observation_utilization_audit(predicate_filter="up")
    assert [row.predicate for row in predicate_audit.predicates] == ["up"]


def test_summary_counts_are_correct():
    payload = observation_utilization_json(build_observation_utilization_audit())
    rows = payload["predicates"]
    assert payload["summary"]["predicates_discovered"] == len(rows)
    assert payload["summary"]["projected_predicates"] == sum(row["projected"] for row in rows)
    assert payload["summary"]["read_model_predicates"] == sum(row["read_model"] for row in rows)
    assert payload["summary"]["diagnostic_consumed_predicates"] == sum(row["diagnostic_consumed"] for row in rows)
    assert payload["summary"]["unused_predicates"] == sum(row["first_loss"] == "unused" for row in rows)


def test_empty_behavior_is_sane(tmp_path):
    (tmp_path / "seed_runtime").mkdir()
    audit = build_observation_utilization_audit(tmp_path)
    assert audit.predicates == ()
    assert audit.summary["predicates_discovered"] == 0
    assert "Predicates discovered: 0" in format_observation_utilization(audit)
