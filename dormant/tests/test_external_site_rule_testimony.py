import json
from pathlib import Path

import pytest
from scripts import seed_local
from seed_runtime.external_site_rule_testimony import (
    BOUNDARY_NOTES,
    ExternalSiteRuleTestimonyInput,
    ExternalSiteRuleTestimonyValidationError,
    assemble_external_site_rule_testimony_set,
    external_site_rule_testimony_json,
    format_external_site_rule_testimony,
)
from seed_runtime.state import StateProjector


def make_testimony(tid="t1", **overrides):
    data = {
        "testimony_id": tid,
        "source_url": "https://example.test/robots.txt",
        "acquired_at": "2026-07-14T00:00:00Z",
        "content_hash": "sha256:1111111111111111111111111111111111111111111111111111111111111111",
        "bounded_rule_text": "User-agent: *\nDisallow: /tmp/",
        "claimed_scope": "specific path",
        "rule_kind": "robots_directive",
        "discovery_route": "operator_seed",
        "operator_supplied_seed": True,
        "interpretation_status": "uninterpreted",
        "unknowns": ["site authorship time unknown"],
    }
    data.update(overrides)
    return data


def supplied(*items, site_scope="example.test bounded site", set_unknowns=None):
    return ExternalSiteRuleTestimonyInput.from_json_dict(
        {"site_scope": site_scope, "testimonies": list(items), "set_unknowns": set_unknowns or []}
    )


def test_one_independently_attributed_testimony_preserves_fields_without_verification():
    artifact = assemble_external_site_rule_testimony_set(
        supplied(make_testimony(), set_unknowns=["authority relationship unknown"])
    )
    assert artifact.site_scope == "example.test bounded site"
    item = artifact.testimonies[0]
    assert item.testimony_id == "t1"
    assert item.source_url == "https://example.test/robots.txt"
    assert item.acquired_at == "2026-07-14T00:00:00Z"
    assert item.content_hash.startswith("sha256:")
    assert item.bounded_rule_text == "User-agent: *\nDisallow: /tmp/"
    assert item.claimed_scope == "specific path"
    assert item.rule_kind == "robots_directive"
    assert item.discovery_route == "operator_seed"
    assert item.operator_supplied_seed is True
    assert item.interpretation_status == "uninterpreted"
    assert item.unknowns == ("site authorship time unknown",)
    assert artifact.set_unknowns == ("authority relationship unknown",)
    assert artifact.read_only is True
    assert artifact.writes_event_ledger is False
    assert artifact.mutates_cluster is False


def test_multiple_testimonies_remain_distinct_including_robots_and_prose_consistency_and_conflict():
    artifact = assemble_external_site_rule_testimony_set(
        supplied(
            make_testimony("robots", rule_kind="robots_directive", bounded_rule_text="Disallow: /tmp/"),
            make_testimony(
                "policy",
                source_url="https://example.test/policy",
                rule_kind="automation_policy",
                discovery_route="homepage_link",
                operator_supplied_seed=False,
                bounded_rule_text="Automated downloads may be available through the catalog.",
                claimed_scope="automated access",
                interpretation_status="candidate_machine_guidance",
            ),
            make_testimony(
                "terms",
                source_url="https://example.test/policy",
                rule_kind="terms_statement",
                bounded_rule_text="Some automated access may be restricted.",
                interpretation_status="possibly_conflicting",
            ),
        )
    )
    assert [t.testimony_id for t in artifact.testimonies] == ["robots", "policy", "terms"]
    assert [t.source_url for t in artifact.testimonies] == [
        "https://example.test/robots.txt",
        "https://example.test/policy",
        "https://example.test/policy",
    ]
    assert [t.rule_kind for t in artifact.testimonies] == [
        "robots_directive",
        "automation_policy",
        "terms_statement",
    ]


def test_zero_testimonies_is_a_valid_set_not_failure():
    artifact = assemble_external_site_rule_testimony_set(supplied())
    assert artifact.testimonies == ()
    assert "zero-testimony set, not failure" in format_external_site_rule_testimony(artifact)


def test_duplicate_testimony_ids_fail_structural_validation():
    with pytest.raises(ExternalSiteRuleTestimonyValidationError, match="duplicate testimony_id"):
        assemble_external_site_rule_testimony_set(supplied(make_testimony("dup"), make_testimony("dup")))


@pytest.mark.parametrize("status", ["authorized", "permitted", "prohibited", "applicable", "binding"])
def test_interpretation_status_cannot_be_seed_policy_verdict(status):
    with pytest.raises(ExternalSiteRuleTestimonyValidationError):
        assemble_external_site_rule_testimony_set(supplied(make_testimony(interpretation_status=status)))


def test_human_and_json_rendering_preserve_boundaries_without_route_or_movement():
    artifact = assemble_external_site_rule_testimony_set(
        supplied(make_testimony(bounded_rule_text="No prohibition stated here."))
    )
    human = format_external_site_rule_testimony(artifact)
    payload = external_site_rule_testimony_json(artifact)
    for note in BOUNDARY_NOTES:
        assert note in human
        assert note in payload["boundary_notes"]
    assert "Site-reported permission does not grant Seed authorization." in human
    assert "Absence of prohibition is not permission." in human
    assert "robots.txt is not treated as complete site policy." in human
    assert "select or authorize external movement" in human
    assert payload["artifact_type"] == "ExternalSiteRuleTestimonySet"
    assert payload["read_only"] is True
    rendered = json.dumps(payload, sort_keys=True)
    assert "access_route" not in rendered
    assert "authorized_movement" not in rendered


def test_cli_human_and_json_are_read_only_and_do_not_append_events_or_mutate_state(tmp_path, capsys):
    path = tmp_path / "testimony.json"
    path.write_text(json.dumps({"site_scope": "example.test", "testimonies": [make_testimony()]}))
    db = tmp_path / "events.sqlite"
    ledger = seed_local.SQLiteEventLedger(str(db))
    before = ledger.list_events(seed_local.DEFAULT_WORKSPACE)
    before_state = StateProjector(ledger).project(seed_local.DEFAULT_WORKSPACE)

    assert seed_local.main(["--db", str(db), "--external-site-rule-testimony", str(path)]) == 0
    human = capsys.readouterr().out
    assert "External Site Rule Testimony Set" in human
    assert "source_url: https://example.test/robots.txt" in human

    assert seed_local.main(["--db", str(db), "--external-site-rule-testimony", str(path), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["testimonies"][0]["content_hash"] == make_testimony()["content_hash"]
    after = ledger.list_events(seed_local.DEFAULT_WORKSPACE)
    after_state = StateProjector(ledger).project(seed_local.DEFAULT_WORKSPACE)
    assert after == before
    assert after_state == before_state


def test_diagnostic_inventory_and_shape_audit_register_surface():
    from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
    from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit

    inventory = {entry.name: entry for entry in DIAGNOSTIC_INVENTORY}
    assert inventory["external_site_rule_testimony"].writes_event_ledger is False
    assert inventory["external_site_rule_testimony"].mutates_cluster is False
    rows = {row.diagnostic: row for row in build_diagnostic_shape_audit()}
    assert rows["external_site_rule_testimony"].status == "consistent"
