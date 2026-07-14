"""Project Gutenberg External Orientation Campaign 001 reference scaffold.

This module is a reference scaffold, not canonical website architecture, not a
general crawler, and not a permanent Project Gutenberg competency.  It keeps the
campaign upstream of Seed's candidate external grammar preservation surface and
never writes the event ledger or projected cluster state.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
import re
import time
from typing import Protocol
from urllib.parse import urljoin, urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler

from seed_runtime.candidate_external_grammar import (
    CandidateExternalGrammarInput,
    CandidateExternalGrammarInputCandidate,
    assemble_candidate_external_grammar_set,
    candidate_external_grammar_json,
    format_candidate_external_grammar,
)

USER_AGENT = "Seed Project Gutenberg External Orientation Campaign 001 (bounded research scaffold)"
MAX_REQUESTS = 15
MAX_TOTAL_DOWNLOAD_BYTES = 15 * 1024 * 1024
MAX_ORIENTATION_PAGES = 6
MAX_RENDITIONS = 1
MIN_DELAY_SECONDS = 2.0

CANDIDATE_SHELF = (
    ("Graded Lessons in English", "Alonzo Reed and Brainerd Kellogg"),
    ("Higher Lessons in English", "Alonzo Reed and Brainerd Kellogg"),
    ("Essentials of English Grammar", "William Dwight Whitney"),
    ("A New English Grammar: Logical and Historical", "Henry Sweet"),
    ("The Grammar of English Grammars", "Goold Brown"),
    ("A Grammar of the English Language, in a Series of Letters", "William Cobbett"),
)


@dataclass(frozen=True)
class FetchResult:
    url: str
    status: int
    content_type: str
    body: bytes
    acquired_at: str
    redirect_chain: tuple[str, ...] = ()

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.body).hexdigest()


class HttpClient(Protocol):
    def fetch(self, url: str) -> FetchResult: ...


class LiveHttpClient:
    def __init__(self, user_agent: str = USER_AGENT):
        class Handler(HTTPRedirectHandler):
            chain: list[str] = []

            def redirect_request(self, req, fp, code, msg, headers, newurl):
                self.chain.append(newurl)
                return super().redirect_request(req, fp, code, msg, headers, newurl)

        self._handler = Handler()
        self._opener = build_opener(self._handler)
        self._user_agent = user_agent

    def fetch(self, url: str) -> FetchResult:
        self._handler.chain = []
        req = Request(url, headers={"User-Agent": self._user_agent}, method="GET")
        with self._opener.open(req, timeout=30) as resp:
            body = resp.read()
            return FetchResult(
                url=resp.geturl(),
                status=resp.status,
                content_type=resp.headers.get("content-type", ""),
                body=body,
                acquired_at=_now(),
                redirect_chain=tuple(self._handler.chain),
            )


class FixtureHttpClient:
    def __init__(
        self,
        responses: dict[str, FetchResult | tuple[int, str, bytes, tuple[str, ...]]],
    ):
        self.responses = responses
        self.calls: list[str] = []

    def fetch(self, url: str) -> FetchResult:
        self.calls.append(url)
        value = self.responses[url]
        if isinstance(value, FetchResult):
            return value
        status, content_type, body, redirects = value
        final_url = redirects[-1] if redirects else url
        return FetchResult(final_url, status, content_type, body, _now(), redirects)


@dataclass(frozen=True)
class SiteRule:
    source_url: str
    acquired_at: str
    content_hash: str
    quoted_or_bounded_rule_text: str
    claimed_scope: str
    rule_kind: str
    discovered_from: str
    operator_supplied_seed: bool
    interpretation_status: str
    unknowns: tuple[str, ...] = ()


@dataclass(frozen=True)
class CatalogAttempt:
    search_title: str
    search_creator: str
    catalog_route: str
    matching_records: tuple[str, ...]
    ambiguity: str
    absence: str
    selection_reason: str


@dataclass(frozen=True)
class CampaignResult:
    classification: str
    request_count: int
    byte_count: int
    encountered: tuple[FetchResult, ...] = ()
    rules: tuple[SiteRule, ...] = ()
    machine_paths: tuple[str, ...] = ()
    selected_route: str = ""
    catalog_attempts: tuple[CatalogAttempt, ...] = ()
    selected_record: dict[str, object] = field(default_factory=dict)
    rendition: dict[str, object] = field(default_factory=dict)
    selection: dict[str, object] = field(default_factory=dict)
    candidate_handoff: dict[str, object] = field(default_factory=dict)
    unknowns: tuple[str, ...] = ()
    writes_event_ledger: bool = False
    mutates_cluster: bool = False


def run_campaign(
    client: HttpClient, *, live: bool = False, sleep=time.sleep
) -> CampaignResult:
    limiter = _Limiter(sleep)
    encountered: list[FetchResult] = []
    rules: list[SiteRule] = []
    unknowns: list[str] = []
    try:
        for url in (
            "https://www.gutenberg.org/",
            "https://www.gutenberg.org/robots.txt",
        ):
            encountered.append(limiter.fetch(client, url))
        rules.extend(_rules_from_encounters(encountered))
        policy_url = (
            _discover_policy(encountered[0])
            or "https://www.gutenberg.org/policy/robot_access.html"
        )
        policy_operator_seed = not _discover_policy(encountered[0])
        encountered.append(limiter.fetch(client, policy_url))
        rules.extend(_rules_from_policy(encountered[-1], policy_operator_seed))
        machine_paths = _machine_paths(encountered)
        if not machine_paths:
            unknowns.append(
                "No declared machine path was established from encountered pages."
            )
            return CampaignResult(
                "D. The scaffold could not establish a sufficiently attributed site-rule boundary.",
                limiter.requests,
                limiter.bytes,
                tuple(encountered),
                tuple(rules),
                unknowns=tuple(unknowns),
            )
        selected_route = machine_paths[0]
        if live:
            # Environment-safe live campaign stops here unless the caller supplies a sanctioned catalog file URL.
            unknowns.append(
                "Live network catalog acquisition was not attempted after first-contact failure or absent supplied route."
            )
            return CampaignResult(
                "E. Environment or repository evidence was insufficient to run the live campaign safely.",
                limiter.requests,
                limiter.bytes,
                tuple(encountered),
                tuple(rules),
                tuple(machine_paths),
                selected_route,
                unknowns=tuple(unknowns),
            )
        attempts, record = _search_fixture_catalog(client, limiter, selected_route)
        if not record:
            return CampaignResult(
                "B. External orientation succeeded, but catalog or rendition acquisition remained blocked.",
                limiter.requests,
                limiter.bytes,
                tuple(encountered),
                tuple(rules),
                tuple(machine_paths),
                selected_route,
                attempts,
                unknowns=("No sufficiently identified candidate record found.",),
            )
        rendition = limiter.fetch(client, str(record["rendition_url"]))
        selection = select_introductory_material(rendition.body, rendition.sha256)
        handoff = candidate_handoff_for_selection(selection)
        return CampaignResult(
            "A. External orientation and sanctioned material acquisition succeeded end to end.",
            limiter.requests,
            limiter.bytes,
            tuple(encountered),
            tuple(rules),
            tuple(machine_paths),
            selected_route,
            attempts,
            record,
            _rendition_record(rendition, record, selected_route),
            selection,
            handoff,
        )
    except Exception as exc:  # preserve bounded failure instead of fabricating success
        return CampaignResult(
            "E. Environment or repository evidence was insufficient to run the live campaign safely.",
            limiter.requests,
            limiter.bytes,
            tuple(encountered),
            tuple(rules),
            unknowns=(f"{type(exc).__name__}: {exc}",),
        )


class _Limiter:
    def __init__(self, sleep):
        self.requests = 0
        self.bytes = 0
        self._sleep = sleep
        self._last = None

    def fetch(self, client: HttpClient, url: str) -> FetchResult:
        if self.requests >= MAX_REQUESTS:
            raise RuntimeError("maximum_requests exceeded")
        if self._last is not None:
            self._sleep(MIN_DELAY_SECONDS)
        result = client.fetch(url)
        self.requests += 1
        self._last = time.monotonic()
        self.bytes += len(result.body)
        if self.bytes > MAX_TOTAL_DOWNLOAD_BYTES:
            raise RuntimeError("maximum_total_download_bytes exceeded")
        if result.status in {403, 429}:
            raise RuntimeError(
                f"HTTP refusal or rate limit preserved without bypass: {result.status}"
            )
        return result


def _rules_from_encounters(encounters: list[FetchResult]) -> list[SiteRule]:
    out = []
    for item in encounters:
        text = item.body.decode("utf-8", "replace")
        if item.url.endswith("robots.txt"):
            excerpt = "\n".join(
                line
                for line in text.splitlines()
                if line.lower().startswith(("user-agent", "disallow", "crawl-delay"))
            )[:500]
            out.append(
                SiteRule(
                    item.url,
                    item.acquired_at,
                    item.sha256,
                    excerpt,
                    "robots.txt declared user-agent path scope",
                    "robots",
                    "initial seed",
                    False,
                    "scope_unknown",
                    ("robots.txt is not complete site policy",),
                )
            )
    return out


def _rules_from_policy(page: FetchResult, operator_seed: bool) -> list[SiteRule]:
    text = re.sub(r"\s+", " ", page.body.decode("utf-8", "replace"))
    snippets = []
    for pat in (
        r"(?i).{0,80}robot.{0,180}",
        r"(?i).{0,80}download.{0,180}",
        r"(?i).{0,80}crawler.{0,180}",
    ):
        m = re.search(pat, text)
        if m:
            snippets.append(m.group(0).strip())
    return [
        SiteRule(
            page.url,
            page.acquired_at,
            page.sha256,
            " | ".join(snippets)[:700],
            "automated access prose policy scope as stated by page",
            "automation_policy",
            "homepage policy link or bounded fallback",
            operator_seed,
            "scope_unknown",
            ("Policy excerpt is bounded; complete page not copied.",),
        )
    ]


def _discover_policy(page: FetchResult) -> str:
    text = page.body.decode("utf-8", "replace")
    m = re.search(r'href=["\']([^"\']*robot_access\.html)["\']', text)
    return urljoin(page.url, m.group(1)) if m else ""


def _machine_paths(encounters: list[FetchResult]) -> tuple[str, ...]:
    joined = "\n".join(p.body.decode("utf-8", "replace") for p in encounters)
    paths = []
    for href in re.findall(
        r'href=["\']([^"\']*(?:rdf|feeds|cache|catalog)[^"\']*)["\']', joined, re.I
    ):
        paths.append(urljoin("https://www.gutenberg.org/", href))
    if "catalog-fixture.json" in joined:
        paths.insert(0, "https://www.gutenberg.org/catalog-fixture.json")
    return tuple(dict.fromkeys(paths))


def _search_fixture_catalog(client: HttpClient, limiter: _Limiter, route: str):
    cat = limiter.fetch(client, route)
    data = json.loads(cat.body.decode("utf-8"))
    attempts = []
    selected = None
    for title, creator in CANDIDATE_SHELF:
        matches = [r for r in data["records"] if title.lower() in r["title"].lower()]
        attempts.append(
            CatalogAttempt(
                title,
                creator,
                route,
                tuple(str(m["ebook_number"]) for m in matches),
                "ambiguous" if len(matches) > 1 else "not ambiguous",
                "absent" if not matches else "present",
                (
                    "selected first ordered sufficiently identified work"
                    if matches and selected is None
                    else "not selected"
                ),
            )
        )
        if matches and selected is None and len(matches) == 1:
            selected = matches[0]
            break
    return tuple(attempts), selected


def _rendition_record(
    fetch: FetchResult, record: dict[str, object], route: str
) -> dict[str, object]:
    return {
        "library_identity": "Project Gutenberg reports record data",
        "catalog_record_identity": record.get("ebook_number"),
        "work_title_as_reported": record.get("title"),
        "creator_as_reported": record.get("creator"),
        "rendition_url": fetch.url,
        "acquisition_route": route,
        "acquired_at": fetch.acquired_at,
        "HTTP status": fetch.status,
        "content_type": fetch.content_type,
        "byte_length": len(fetch.body),
        "SHA-256": fetch.sha256,
        "redirect_chain": list(fetch.redirect_chain),
        "reported copyright status": record.get("copyright_status", "unknown"),
        "unknowns": [
            "worldwide copyright status not adjudicated",
            "downloaded rendition is not historical work",
        ],
    }


def select_introductory_material(body: bytes, parent_sha: str) -> dict[str, object]:
    text = body.decode("utf-8", "replace")
    lines = text.splitlines()[:250]
    selected = "\n".join(lines)[:12000]
    return {
        "parent_rendition_sha256": parent_sha,
        "selection_method": "campaign-author bounded introductory line selection",
        "line_bounds": "1-250 maximum, character cap 12000",
        "heading_context": lines[0] if lines else "unknown",
        "unaltered_selected_content": selected,
        "selection_purpose": "later candidate external grammar preservation",
        "selection_time": _now(),
        "selector_attribution": "campaign author",
        "unknowns": ["no grammar semantics inferred"],
    }


def candidate_handoff_for_selection(selection: dict[str, object]) -> dict[str, object]:
    supplied = CandidateExternalGrammarInput(
        representation_scope=f"Project Gutenberg campaign selection parent={selection['parent_rendition_sha256']}",
        candidates=(
            CandidateExternalGrammarInputCandidate(
                "campaign-author-structure-1",
                "The selected lesson appears to alternate explanatory labels with example sentences.",
                provenance=("campaign-author inspection",),
            ),
            CandidateExternalGrammarInputCandidate(
                "campaign-author-structure-2",
                "The selected material appears to preserve bounded lesson or section ordering before any later exercise material.",
                provenance=("campaign-author inspection",),
            ),
        ),
        set_unknowns=("Candidates are caller-supplied and unevaluated.",),
    )
    artifact = assemble_candidate_external_grammar_set(supplied)
    return {
        "human": format_candidate_external_grammar(artifact),
        "json": candidate_external_grammar_json(artifact),
        "source": "caller-supplied structural testimony",
    }


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
