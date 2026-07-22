# 01 Architecture

## System summary

Seed's current active witness is bounded rather than a universal request pipeline.
The implementation records append-only events, projects current state, ingests
observations, derives evidence-backed facts and relationships, exposes read-only
views and diagnostics, and supports bounded inquiry, selection, capability
testimony, and provider recommendation metadata where those surfaces are backed
by code.

Seed does **not** own shell execution, arbitrary provider-output execution,
secrets, host mutation, retries, scheduling, or long-running job lifecycle.

## Knowledge and projection responsibilities

Core projection responsibilities include:

- facts derived from Evidence with confidence and provenance;
- FactSupport aggregates grouped by subject, predicate, and value;
- predicate cardinality for single-valued conflict handling and multi-valued
  current sets;
- measurements retained as current projected samples with bounded recent history;
- identity and alias resolution without hiding provenance;
- relationships and topology projection from facts;
- entity type projection and validation;
- graph validation for impossible edges, unknown types, ambiguous identity, and
  type/predicate mismatches;
- explanation/why queries that traverse fact support, conflicts, inference links,
  and provenance without adding a new reasoning mechanism.

## Boundary clarity

- `EventLedger` is the historical event source.
- `ProjectionStore` caches current world-model snapshots; it never becomes the
  source of truth.
- `State` is the current projected world model derived from the ledger.
- State views are read-only representations of projected State for facts,
  observations, requirements, capabilities, issues, and summary counts. They are
  projection views, not a second state store.
- `CapabilityCatalog` is read-only capability/provider metadata; catalog presence
  does not prove availability or verification.
- `ToolRegistry` is registered operation inventory. Registered operation handling
  remains separate from arbitrary provider text, shell commands, and host
  mutation.

## Ownership boundary

Seed owns:

- event ledger;
- state projection;
- observation ingestion;
- fact/evidence model;
- relationships and topology projection;
- capability gaps and capability testimony where currently implemented;
- recommendation metadata and ranking where currently implemented;
- audit trail;
- state views that answer what Seed currently knows without reading raw events or
  invoking operation behavior.

Seed delegates or excludes:

- unregistered or arbitrary execution;
- shell commands and host mutation;
- secrets;
- retries;
- scheduling;
- long-running jobs;
- credential prompts.

## Read-only views and diagnostics

State views, evidence graph views, contradiction detection, confidence
aggregation, selection views, and diagnostics are projections or bounded read
models. They do not append events, mutate State, run shell commands, perform
network calls, or create separate persistence layers unless an individual
implemented surface explicitly documents a narrower record-only diagnostic
boundary.

## Current stopping point

This document intentionally does not define a new canonical runtime flow or a
replacement decision, policy, or execution architecture. Deleted planning,
handoff, proposal, authorization, and pending-action artifacts are absent from
active architecture ownership.
