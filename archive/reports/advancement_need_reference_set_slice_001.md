# Advancement need reference set slice 001

This slice adds one read-only `AdvancementNeedReferenceSet` projection over one exact immutable `GoalAdvancementNeedSet` snapshot.

The projection emits one visible reference for every native item in each supplied clarification, inquiry, authority, and operational-realization need projection. Reference identity binds the need set, selected goal, bounded horizon, family, native projection, and family-local native lineage. Native standing, bucket placement, evidence quality, and selectability remain metadata rather than identity.

Only native `established` records are selectable. Unsupported, unknown, conflicting, excluded, outside-current-scope, unclassified-here, and unclassified native records remain visible but non-selectable.

Duplicate family-local native lineage is preserved as a visible `duplicate_native_lineage` conflict. The conflict uses the native lineage itself and does not depend on presentation order, list indexes, bucket names, standing values, serialized payload hashes, priority, routing, or reclassification.

The projection is read-only and does not reclassify needs, select or prioritize a need, route work, request clarification, open inquiry, request authority, select realization, authorize work, execute, record, write the event ledger, or mutate cluster state.
