# Recurrence Navigation Investigation

## Purpose and boundary

This investigation asks whether recurrence navigation is the next safe layer after recurrence visibility.

Repository authority wins.

This report is investigation only. It does not implement prose interpretation, claim extraction, authority inference, shape inference, ontology promotion, NLP, LLM analysis, recommendation systems, workflow systems, or new CLI behavior.

## Repository evidence reviewed

Implementation and test evidence show the current documentation structure surface can observe:

```text
section labels
front matter keys
heading depths
code fence languages
link target classes
recurrence distributions
rare structures
section skeleton signatures
missing common sections
structural outliers
```

The existing recurrence review also identified a remaining gap: recurrence rows can show raw counts but not example documents for every recurring entry.

Fresh local command evidence from this investigation:

```bash
python scripts/seed_local.py --documentation-structure --recurrence --skeletons --outliers --top 5
```

Observed current corpus output included:

```text
Documents: 442
Purpose: 277
Non-Goals: 106
Conclusion: 86
status: 135
domain: 93
doc_type: 90
text: 7890
python: 33
1 occurrence section-label bucket: 7976
no H2/H3 sections: 10 docs
Structural outliers: docs/audit_snapshot_and_comparison_design_audit.md ...
```

This confirms that recurrence visibility now answers `what recurs?` for multiple structural categories, and it already partly answers `where is structural outlier evidence?` through document paths in the outlier view.

## Recurrence visibility versus recurrence navigation

### Recurrence visibility

Recurrence visibility answers:

```text
What structural item recurs?
How often does it recur?
How is recurrence distributed across frequency buckets?
Which structural rows are rare or common?
Which skeleton signatures recur?
Which documents miss common structural labels?
Which documents have structural outlier signals?
```

Examples from repository-backed surfaces:

```text
Purpose: 277
status: 135
text: 7890
1 occurrence section-label bucket: 7976
section skeleton signature: 10 docs
```

This remains structural because the output is limited to observed forms and counts.

### Recurrence navigation

Recurrence navigation would answer:

```text
Where does this observed structural item occur?
Which bounded example documents contain it?
Which document paths are members of this exact structural recurrence row?
Where can an operator inspect the concrete source without inferring meaning?
```

The proposed distinction is therefore:

```text
visibility = item + count + bucket + structural signal
navigation = item + bounded document locations/examples for source inspection
```

Navigation does not need to say why a structure exists, what it means, whether it is important, or whether documents are related. It can simply attach document paths and possibly line positions to exact structural observations already produced by the observer.

## Can navigation answer `Where does this structure occur?` without interpreting meaning?

Yes, if the navigation key is an exact observed structural key and the answer is a bounded list of observed document locations.

Supported structural examples:

| Structural question | Safe navigation answer |
| --- | --- |
| Where does section label `Purpose` occur? | Document paths containing a heading whose normalized label is `Purpose`; optionally heading depth and line. |
| Where does front matter key `status` occur? | Document paths whose YAML front matter contains the key `status`. |
| Where does skeleton signature `S` occur? | Document paths whose ordered H2/H3 skeleton exactly equals signature `S`. |
| Where does code fence language `python` occur? | Document paths containing fenced code blocks whose observed language is `python`; optionally fence line. |
| Where does this structural outlier signal occur? | Document paths already carrying that signal, such as `high_code_fence_count` or `missing_front_matter`. |

The safe rule is exact structural matching. The unsafe rule is conceptual expansion.

For example:

```text
safe: documents with section label exactly `Purpose`
unsafe: documents about purpose
```

```text
safe: documents with front matter key exactly `status`
unsafe: documents that are status-like or active
```

```text
safe: documents with the same skeleton signature
unsafe: documents with similar intent or related meaning
```

## Navigation forms that remain structural

The following forms remain inside the existing boundary if they are bounded and explicitly structural:

1. **Example documents**
   - A small, deterministic sample of paths for a recurrence row.
   - Useful when high-frequency rows such as `Purpose` or `status` would otherwise be abstract counts.

2. **Document counts**
   - Already central to recurrence visibility.
   - Navigation can preserve counts while exposing examples or complete location lists only under an explicit drilldown.

3. **Document locations**
   - Paths, heading depths, and line numbers derived from Markdown structure.
   - No interpretation is required to report where a heading, key, or code fence appears.

4. **Bounded drilldown**
   - A limit-controlled path list for one recurrence category and one recurrence key.
   - Safer than emitting all locations for every row because it prevents a broad structural view from becoming noisy or workflow-like.

5. **Exact skeleton membership**
   - Documents grouped by identical structural skeleton signature.
   - Safe only if described as exact ordered structural membership, not a document family or semantic template.

6. **Structural outlier path drilldown**
   - Documents carrying already-defined structural signals.
   - Safe when the signal remains mechanical, such as missing front matter, high section count, high code fence count, deep heading depth, empty sections, or rare section labels.

## Navigation forms that pressure interpretation

The following forms begin to cross the boundary:

1. **Related documents**
   - `Related` can imply an artifact relationship, semantic connection, or authority linkage.
   - It is not equivalent to sharing a section label or skeleton.

2. **Similar documents**
   - Similarity requires a distance function and invites interpretation of why documents are similar.
   - Exact structural equality is safer than similarity scoring.

3. **Recommended documents**
   - Recommendation introduces selection pressure and workflow guidance.
   - It asks the system to decide what an operator should inspect next.

4. **Important documents**
   - Importance is not structurally observable from recurrence alone.
   - High frequency, rarity, or outlier status can be visible, but none proves importance.

5. **Meaningful cluster names**
   - Names such as `architecture docs`, `status reports`, or `decision records` would promote interpretation unless already backed by repository metadata or another authoritative surface.

6. **Shape or ontology promotion**
   - A repeated section label does not prove a required document shape.
   - A repeated skeleton does not prove a schema.

## Navigation opportunities

### Section label to matching documents

Opportunity:

```text
section label -> bounded matching document paths
```

Usefulness:

- Answers where a common label such as `Purpose` occurs.
- Helps inspect long-tail labels that currently appear only as rare rows.
- Supports cleanup by locating exact headings without interpreting their prose.

Boundary:

- Match observed heading labels only.
- Do not expand to synonyms or documents about the label.

### Front matter key to matching documents

Opportunity:

```text
front matter key -> bounded matching document paths
```

Usefulness:

- Shows where metadata coverage exists.
- Helps review adoption of keys such as `status`, `domain`, and `doc_type`.

Boundary:

- Report key presence only.
- Do not infer lifecycle, ownership, authority, or completeness from the key.

### Skeleton signature to matching documents

Opportunity:

```text
skeleton signature -> matching document paths
```

Usefulness:

- Turns `10 docs` or `1 docs` skeleton rows into inspectable source locations.
- Supports coverage review of exact structural repetition.

Boundary:

- Use exact signature membership.
- Avoid labels such as template, type, family, or recommended shape unless separately established.

### Rare structure to matching documents

Opportunity:

```text
rare structure -> document paths containing the rare observation
```

Usefulness:

- Rare labels are otherwise hard to inspect in a corpus where singleton section-label buckets are large.
- Helps distinguish intentional one-off documents from cleanup candidates by allowing human source inspection.

Boundary:

- Do not say rare means wrong.
- Do not recommend remediation automatically.

### Outlier signal to matching documents

Opportunity:

```text
outlier signal -> document paths carrying the signal
```

Usefulness:

- The current output already lists outlier document paths with mechanical signals.
- A focused drilldown by signal would help inspect all documents with `high_code_fence_count`, `missing_front_matter`, or `deep_heading_depth`.

Boundary:

- Do not claim outlier means problematic, important, or conceptually central.

## Counterexamples

### Navigation adds little value

1. **Very common generic labels**
   - A full path list for `Purpose` across 277 documents would be noisy.
   - Bounded examples help; exhaustive default output would not.

2. **Universally common heading depths**
   - `depth 2: 6252` is useful as a distribution signal, but a document list for every depth-2 heading may add little value.

3. **Dominant code fence language `text`**
   - `text: 7890` is too broad for default navigation.
   - A drilldown may still help only when scoped by document, limit, or outlier context.

4. **Singleton labels with no cleanup question**
   - A rare label path is useful for inspection, but if the label is clearly document-specific, navigation may not change operator understanding.

### Navigation becomes interpretation

1. **From exact match to semantic match**
   - `section label: Purpose` becomes interpretive if it expands to `Objective`, `Intent`, or prose that explains purpose.

2. **From same skeleton to same document type**
   - Exact skeleton equality is structural.
   - Calling the group a type, family, or template asserts more than the structure proves.

3. **From outlier to problem**
   - `high_code_fence_count` is a structural signal.
   - `needs cleanup` is workflow guidance unless explicitly requested by a cleanup task.

4. **From frequency to importance**
   - `status: 135` is recurrence evidence.
   - `status is important repository knowledge` is unsupported by recurrence alone.

## Can navigation improve exploration, coverage review, cleanup, inventory, and structural auditing?

Yes, but only as source location support, not workflow guidance.

| Activity | Structural improvement | Boundary |
| --- | --- | --- |
| Exploration | Let operators open examples for a recurrence row. | Do not rank what they should read. |
| Coverage review | Show which docs contain or miss a structural key. | Do not infer policy compliance unless a policy exists. |
| Cleanup | Locate exact documents with missing front matter, empty sections, rare labels, or unclosed fences. | Do not decide cleanup priority. |
| Inventory | Attach path examples to counts and buckets. | Do not promote inventory terms into ontology. |
| Structural auditing | Prove that surfaced structural signals have source locations. | Do not extract claims from prose. |

## Supported conclusions

1. Recurrence navigation is a bounded source-location layer over already observed structural recurrence.
2. It differs from recurrence visibility by adding `where` answers to existing `what/how many` answers.
3. Navigation remains structural when it uses exact observed keys, document paths, line locations, counts, and bounded drilldown.
4. Navigation becomes interpretive when it introduces relatedness, similarity, recommendation, importance, semantic expansion, document families, templates, or shape authority.
5. The safest next layer after recurrence visibility appears to be bounded recurrence navigation, not semantic similarity or workflow recommendation.

## Unsupported conclusions

- Recurrence navigation proves meaning.
- Recurrence navigation proves document relationship.
- Recurrence navigation proves importance.
- Recurrence navigation should recommend documents.
- Repeated section labels define required document shapes.
- Exact skeleton membership defines a document type.
- Rare structures are automatically defects.
- Outlier structures are automatically cleanup priorities.

## Recommended next step

Investigate or prototype only the smallest structural navigation slice:

```text
one recurrence category
one exact structural key
bounded matching document paths
optional line/depth evidence
explicit boundary statement
JSON and text parity
```

Best first candidate:

```text
section label -> bounded matching documents
```

Reason:

- Section labels are already visible, numerous, and recurrence-heavy.
- The current corpus shows both highly common labels and a large singleton bucket.
- A bounded path drilldown would directly answer `Where does this structure occur?` without requiring meaning extraction.

The next candidate after that would be:

```text
front matter key -> bounded matching documents
```

because key presence is also an exact structural observation and supports coverage review without semantic inference.

## Acceptance answers

### What is recurrence navigation?

Recurrence navigation is a read-only, non-interpretive source-location layer that maps an already observed recurring structural item to bounded document examples or locations.

### How is it different from recurrence visibility?

Recurrence visibility says what recurs and how often. Recurrence navigation says where the already observed recurrence occurs.

### What navigation remains structural?

Exact section-label matches, front-matter-key matches, code-fence-language matches, exact skeleton-signature membership, rare-structure locations, outlier-signal locations, counts, paths, line numbers, and bounded drilldowns remain structural.

### Where does navigation become interpretation?

It becomes interpretation when it claims semantic relatedness, similarity, recommendations, importance, document type, template authority, required shape, or conceptual meaning from recurrence alone.

### Is recurrence navigation the safest next layer after recurrence visibility?

Yes, with a narrow condition: it is safe as bounded exact structural drilldown. It is not safe if it becomes related-document search, semantic similarity, recommendation, importance ranking, or shape promotion.
