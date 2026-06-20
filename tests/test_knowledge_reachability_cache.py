from datetime import datetime, timezone

from seed_runtime.facts import Fact, FactSupport
from seed_runtime.knowledge_reachability import (
    _TokenizationCache,
    _build_indexes,
    _candidate_flags_from_indexes,
    _discover_candidates,
    _new_counters,
    _surface_terms,
)
from seed_runtime.models import Event
from seed_runtime.state import State


def _now() -> datetime:
    return datetime(2026, 1, 1, tzinfo=timezone.utc)


def _repeated_state(count: int) -> State:
    facts = {}
    supports = []
    for index in range(count):
        fact = Fact(
            id=f"fact-{index}",
            subject_id="repeat-host",
            predicate="repeat_predicate",
            value="repeat value",
            dimensions={"zone": "repeat-zone"},
            source_type="discovery",
            observed_at=_now(),
        )
        facts[fact.id] = fact
        supports.append(
            FactSupport(
                subject="repeat-host",
                predicate="repeat_predicate",
                value="repeat value",
                dimensions={"zone": "repeat-zone"},
                supporting_fact_ids=[fact.id],
                source_types=["discovery"],
                confidence=0.9,
                observed_at=_now(),
                latest_observed_at=_now(),
            )
        )
    return State(workspace_id="default", facts=facts, fact_supports=supports)


def test_surface_terms_tokenizes_repeated_identical_strings_once():
    counters = _new_counters()
    cache = _TokenizationCache(counters)

    terms = _surface_terms(
        ["Repeated Shared String", "Repeated Shared String", "repeated shared string"],
        counters,
        cache,
    )

    assert "repeated shared string" in terms
    assert counters["tokenization_requests"] == 3
    # The cache is keyed by the unique input string for the run. The differently
    # cased string is a separate input, while the exact repeat is reused.
    assert counters["tokenizations"] == 2
    assert counters["tokenization_unique"] == 2
    assert counters["tokenization_cache_hits"] == 1


def test_reachability_cache_is_shared_across_discovery_indexes_and_evaluation(tmp_path):
    counters = _new_counters()
    cache = _TokenizationCache(counters)
    state = _repeated_state(25)
    events = [
        Event(
            id=f"event-{index}", kind="fact.observed", payload={"value": "repeat value"}
        )
        for index in range(10)
    ]

    _discover_candidates(
        events,
        state,
        tmp_path,
        counters,
        token_cache=cache,
        limit=None,
        all_candidates=True,
    )
    after_discovery_unique = counters["tokenization_unique"]

    indexes = _build_indexes(events, state, counters=counters, token_cache=cache)
    _candidate_flags_from_indexes("repeat-host", indexes, counters, cache)

    assert counters["tokenization_requests"] > counters["tokenization_unique"]
    assert counters["tokenization_cache_hits"] > 0
    assert counters["tokenization_unique"] == counters["tokenizations"]
    assert counters["tokenization_unique"] >= after_discovery_unique


def test_reachability_tokenization_scales_with_unique_strings_not_rows(tmp_path):
    counters = _new_counters()
    cache = _TokenizationCache(counters)
    row_count = 200
    state = _repeated_state(row_count)
    events = [
        Event(
            id=f"event-{index}", kind="fact.observed", payload={"value": "repeat value"}
        )
        for index in range(row_count)
    ]

    _discover_candidates(
        events,
        state,
        tmp_path,
        counters,
        token_cache=cache,
        limit=None,
        all_candidates=True,
    )
    indexes = _build_indexes(events, state, counters=counters, token_cache=cache)
    _candidate_flags_from_indexes("repeat-host", indexes, counters, cache)

    assert counters["tokenization_requests"] > row_count
    assert counters["tokenization_cache_hits"] > row_count
    assert counters["tokenization_unique"] < 25
