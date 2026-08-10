"""Seed runtime package with lazy compatibility exports.

Importing a live submodule must not initialize the historical runtime barrel.
The names below remain available to compatibility callers and load their
owning modules only when requested.
"""

from __future__ import annotations

from importlib import import_module

_EXPORTS: dict[str, tuple[str, str]] = {
    "AnsibleInventoryObservationSource": ("ansible_inventory_source", "AnsibleInventoryObservationSource"),
    "CapabilityCatalog": ("capability_catalog", "CapabilityCatalog"),
    "CapabilityCandidate": ("capability_candidates", "CapabilityCandidate"),
    "CapabilityCandidateEvidence": ("capability_candidates", "CapabilityCandidateEvidence"),
    "CapabilityCandidateInspection": ("capability_candidates", "CapabilityCandidateInspection"),
    "build_capability_candidates": ("capability_candidates", "build_capability_candidates"),
    "EntityTypeCatalog": ("entity_type_catalog", "EntityTypeCatalog"),
    "EntityTypeDefinition": ("entity_type_catalog", "EntityTypeDefinition"),
    "InferenceCatalog": ("inference_catalog", "InferenceCatalog"),
    "InferenceRule": ("inference_catalog", "InferenceRule"),
    "ProjectionIntegritySummary": ("integrity_summary", "ProjectionIntegritySummary"),
    "build_projection_integrity_summary": ("integrity_summary", "build_projection_integrity_summary"),
    "PredicateCatalog": ("predicate_catalog", "PredicateCatalog"),
    "RelationshipCatalog": ("relationship_catalog", "RelationshipCatalog"),
    "RelationshipDefinition": ("relationship_catalog", "RelationshipDefinition"),
    "RelationshipKind": ("relationship_catalog", "RelationshipKind"),
    "PredicateNormalizer": ("predicate_normalizers", "PredicateNormalizer"),
    "Evidence": ("evidence", "Evidence"),
    "BeliefExplanation": ("explanations", "BeliefExplanation"),
    "Explanation": ("explanations", "Explanation"),
    "ExplanationBuilder": ("explanations", "ExplanationBuilder"),
    "FactExplanation": ("explanations", "FactExplanation"),
    "Fact": ("facts", "Fact"),
    "FactConflict": ("facts", "FactConflict"),
    "FactSupport": ("facts", "FactSupport"),
    "FakeObservationSource": ("observation_sources", "FakeObservationSource"),
    "JsonObservationSource": ("observation_sources", "JsonObservationSource"),
    "ObservationCollectionService": ("observation_sources", "ObservationCollectionService"),
    "ObservationSource": ("observation_sources", "ObservationSource"),
    "export_observations_json": ("observation_sources", "export_observations_json"),
    "EndpointAliasNormalizer": ("observation_normalizers", "EndpointAliasNormalizer"),
    "EndpointIdentityNormalizer": ("observation_normalizers", "EndpointIdentityNormalizer"),
    "ObservationNormalizationPipeline": ("observation_normalizers", "ObservationNormalizationPipeline"),
    "ObservationNormalizer": ("observation_normalizers", "ObservationNormalizer"),
    "Observation": ("observations", "Observation"),
    "ObservationIngestor": ("observations", "ObservationIngestor"),
    "InputArtifact": ("input_inspector", "InputArtifact"),
    "InputInspector": ("input_inspector", "InputInspector"),
    "Event": ("event", "Event"),
    "EntityRelationship": ("state", "EntityRelationship"),
    "EntityTypeAssertion": ("state", "EntityTypeAssertion"),
    "VerificationEvidence": ("verification_evidence", "VerificationEvidence"),
    "VerificationEvidenceInspection": ("verification_evidence", "VerificationEvidenceInspection"),
    "build_verification_evidence": ("verification_evidence", "build_verification_evidence"),
}

__all__ = list(_EXPORTS)


def __getattr__(name: str):
    try:
        module_name, attribute = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc
    value = getattr(import_module(f"{__name__}.{module_name}"), attribute)
    globals()[name] = value
    return value
