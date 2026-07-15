# Closed Choice Selection Binding Slice 001

This slice implements one read-only closed-choice selection-binding boundary.

It preserves:

- the exact presented choice set and its fingerprint;
- the captured operator token;
- a binding only when that token belongs to the exact referenced choice set;
- unsupported, unknown, and conflicting selection evidence; and
- the boundary that selection binding is not goal transition, authority, inquiry selection, or execution.

The implementation intentionally stops at binding. It does not apply the selected option to any operator goal or inquiry frontier.
