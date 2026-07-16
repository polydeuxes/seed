from seed_runtime.bounded_constitutional_question import BoundedConstitutionalQuestion


def bounded_question(**overrides):
    values = {
        "bounded_question_id": "bounded-question:pipeline-test",
        "operator_inquiry": "Operator says constitutional process should be inspected; this is testimony.",
        "inquiry_provenance": "frontier:test-support:established",
        "bounded_question": "Explain the explicitly requested constitutional process view.",
        "constitutional_intent": "established bounded compatibility inquiry",
        "scope_status": "bounded by established test frontier",
        "uncertainty": ("caller scope preserved",),
        "unknowns": ("operator assertion not verified",),
        "caller_supplied_fields": (("selection_key", "process"),),
    }
    values.update(overrides)
    return BoundedConstitutionalQuestion(**values)
