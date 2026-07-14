import hashlib
import json

from campaigns.project_gutenberg_external_orientation_campaign_001 import (
    FetchResult,
    FixtureHttpClient,
    MAX_REQUESTS,
    _Limiter,
    candidate_handoff_for_selection,
    run_campaign,
    select_introductory_material,
)


def _fixture_client(extra=None):
    home = b'<html>Project Gutenberg <a href="/policy/robot_access.html">robot</a><a href="/ebooks/123">ordinary</a></html>'
    robots = b"User-agent: *\nDisallow: /cache/\n"
    policy = b'<html>Robot access says use machine catalog. <a href="/catalog-fixture.json">RDF catalog</a> download with delay. ordinary page narrower text.</html>'
    catalog = json.dumps(
        {
            "records": [
                {
                    "ebook_number": "1",
                    "title": "Other",
                    "creator": "Nobody",
                    "rendition_url": "https://www.gutenberg.org/files/1/1.txt",
                },
                {
                    "ebook_number": "7010",
                    "title": "Graded Lessons in English",
                    "creator": "Alonzo Reed and Brainerd Kellogg",
                    "rendition_url": "https://www.gutenberg.org/files/7010/7010-0.txt",
                    "copyright_status": "Public domain in the USA.",
                },
            ]
        }
    ).encode()
    rendition = b"LESSON 1\nNouns name things.\nExamples: birds fly.\nExercise: change one word.\n"
    responses = {
        "https://www.gutenberg.org/": (200, "text/html", home, ()),
        "https://www.gutenberg.org/robots.txt": (200, "text/plain", robots, ()),
        "https://www.gutenberg.org/policy/robot_access.html": (
            200,
            "text/html",
            policy,
            (),
        ),
        "https://www.gutenberg.org/catalog-fixture.json": (
            200,
            "application/json",
            catalog,
            (),
        ),
        "https://www.gutenberg.org/files/7010/7010-0.txt": (
            200,
            "text/plain; charset=utf-8",
            rendition,
            ("https://www.gutenberg.org/cache/epub/7010/pg7010.txt",),
        ),
    }
    if extra:
        responses.update(extra)
    return FixtureHttpClient(responses)


def test_homepage_orientation_discovers_policy_link_and_robots_separate():
    result = run_campaign(_fixture_client(), sleep=lambda s: None)
    assert result.classification.startswith("A.")
    assert any(r.rule_kind == "robots" for r in result.rules)
    assert any(r.rule_kind == "automation_policy" for r in result.rules)
    assert result.rules[0].source_url.endswith("robots.txt")


def test_declared_machine_path_is_preferred_over_ordinary_page_and_not_seed_authorization():
    result = run_campaign(_fixture_client(), sleep=lambda s: None)
    assert result.selected_route == "https://www.gutenberg.org/catalog-fixture.json"
    assert "https://www.gutenberg.org/ebooks/123" not in _fixture_client().calls
    assert result.writes_event_ledger is False and result.mutates_cluster is False
    assert not hasattr(result, "site_policy")


def test_rules_remain_attributed_and_conflicts_unresolved():
    result = run_campaign(_fixture_client(), sleep=lambda s: None)
    statuses = {r.interpretation_status for r in result.rules}
    assert "scope_unknown" in statuses
    assert all(r.source_url and r.content_hash and r.acquired_at for r in result.rules)


def test_limits_redirects_blocks_and_no_recursive_crawl():
    client = _fixture_client()
    result = run_campaign(client, sleep=lambda s: None)
    assert result.request_count <= MAX_REQUESTS
    assert result.byte_count < 15 * 1024 * 1024
    assert result.rendition["redirect_chain"] == [
        "https://www.gutenberg.org/cache/epub/7010/pg7010.txt"
    ]
    assert client.calls == [
        "https://www.gutenberg.org/",
        "https://www.gutenberg.org/robots.txt",
        "https://www.gutenberg.org/policy/robot_access.html",
        "https://www.gutenberg.org/catalog-fixture.json",
        "https://www.gutenberg.org/files/7010/7010-0.txt",
    ]
    blocked = _fixture_client(
        {
            "https://www.gutenberg.org/policy/robot_access.html": (
                429,
                "text/html",
                b"rate",
                (),
            )
        }
    )
    assert run_campaign(blocked, sleep=lambda s: None).classification.startswith("E.")


def test_catalog_no_match_and_ambiguous_results_are_preserved():
    cat = json.dumps(
        {
            "records": [
                {
                    "ebook_number": "10",
                    "title": "Graded Lessons in English A",
                    "creator": "x",
                    "rendition_url": "u",
                },
                {
                    "ebook_number": "11",
                    "title": "Graded Lessons in English B",
                    "creator": "x",
                    "rendition_url": "u",
                },
            ]
        }
    ).encode()
    result = run_campaign(
        _fixture_client(
            {
                "https://www.gutenberg.org/catalog-fixture.json": (
                    200,
                    "application/json",
                    cat,
                    (),
                )
            }
        ),
        sleep=lambda s: None,
    )
    assert result.classification.startswith("B.")
    assert result.catalog_attempts[0].ambiguity == "ambiguous"
    assert result.catalog_attempts[1].absence == "absent"


def test_selected_record_distinct_from_work_rendition_hash_and_hash_changes():
    result = run_campaign(_fixture_client(), sleep=lambda s: None)
    assert result.selected_record["ebook_number"] == "7010"
    assert result.rendition["catalog_record_identity"] == "7010"
    h = result.rendition["SHA-256"]
    assert (
        h
        == hashlib.sha256(
            b"LESSON 1\nNouns name things.\nExamples: birds fly.\nExercise: change one word.\n"
        ).hexdigest()
    )
    assert h != hashlib.sha256(b"altered").hexdigest()
    assert "downloaded rendition is not historical work" in result.rendition["unknowns"]


def test_selected_material_bounds_parent_hash_and_no_semantics():
    result = run_campaign(_fixture_client(), sleep=lambda s: None)
    assert result.selection["parent_rendition_sha256"] == result.rendition["SHA-256"]
    assert result.selection["line_bounds"].startswith("1-250")
    assert "no grammar semantics inferred" in result.selection["unknowns"]


def test_candidate_handoff_is_caller_supplied_and_deterministic():
    sel = select_introductory_material(b"H\nExample.\n", "abc")
    first = candidate_handoff_for_selection(sel)
    second = candidate_handoff_for_selection(sel)
    assert first["source"] == "caller-supplied structural testimony"
    assert first["json"] == second["json"]
    assert first["human"] == second["human"]
    assert first["json"]["writes_event_ledger"] is False
    assert "campaign-author inspection" in first["human"]


def test_byte_limit_enforced():
    limiter = _Limiter(lambda s: None)
    huge = b"x" * (15 * 1024 * 1024 + 1)
    client = FixtureHttpClient({"u": (200, "text/plain", huge, ())})
    try:
        limiter.fetch(client, "u")
    except RuntimeError as exc:
        assert "maximum_total_download_bytes" in str(exc)
    else:
        raise AssertionError("byte limit not enforced")
