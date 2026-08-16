# Responsibility spine

Translation testimony only. The [Book of Seed](../book_of_seed/README.md) is
the authority; this file has none.

Rosetta follows the same ordering as the Book and runtime:

```text
Responsibility
    ├── responsible boundary
    ├── subject or material
    ├── exact Act
    ├── Authority / Evidence
    ├── Scope / locality
    ├── Applicability / Admission where required
    ├── Act occurrence
    ├── result / Assertion
    └── Standing
```

Relations recur across live implementation roads:

```text
content ── Locality → occurrence
subject ── Participation(role) → Act occurrence
Act occurrence ── Yield → result
Evidence of Yield relation ── Carried_by(evidence_of_yield_relation_identity) → recording occurrence of result
first subject ── Locality → second subject
```

The endpoints do not supply a relation by co-presence. Each relation requires
its exact Evidence. These relations are not every relation
about which Seed may carry an Assertion or Standing.

## Live implementation references

These references are representative witnesses, not a runtime inventory. They
do not define grammar. An acquisition Act or result does not enter Rosetta
unless an ordinary word needs translation to an exact Seed
distinction.

```text
Measurement Responsibility / Act / occurrence / Assertions
    seed_runtime.byte_measurement::record_byte_measurement_responsible_act_evidence
    seed_runtime.byte_measurement::record_byte_measurement_result
    seed_runtime.byte_measurement::record_byte_position_pair_count_layer

Evidence of Yield relation
    seed_runtime.evidence_of_yield_relation::_record_evidence_of_yield_relation

Assertion addressability and locality movement
    seed_runtime.byte_measurement::assertions_of_recorded_byte_measurement
    seed_runtime.byte_measurement::_move_byte_assertion_to_locality

Applicability
    seed_runtime.byte_measurement::get_recorded_pair_input_applicability

Emission Locality / Participation / Yield
    seed_runtime.operator_representation::emit_operator_representation_material

Machine-grammar Fidelity
    tests/test_grammar_implementation.py
```

## Directional shorthand

`Examination` describes movement from presented material toward bounded Seed
Assertions. `Presentation` describes movement from bounded Seed Assertions
toward an emitted representation. Neither is a root, Act, or
occurrence. They are directions across the Responsibility spine.

## Translation shorthand

The following words are ordinary compression. Expand them before reasoning
about Seed:

```text
Producer       Act occurrence + Yield + result
Consumer       subject + role + Applicability + Participation
Consumption    Participation in an exact Act occurrence
Uptake         availability + Applicability + Participation
Handoff        movement, or an exact Responsibility/Authority change
Memory         addressed prior Locality Standing boundary + Book-bounded Responsibility assignment + direct Standing Locality continuation + new Locality; availability != Applicability; another exact Act remains required
Checkout       exact recorded Standing boundary reference + new Locality + direct Locality relation; no history copy; no persistent Memory
Pointers       one preserved thing + many exact references to it + no identity collapse; pointer equality establishes no occurrence, Standing, or Evidence equality
Lineage        ordered source and occurrence references beneath Provenance
Artifact       exact representation, record, Assertion, or result
Projection     exact Act occurrence + representation + its carried coordinates
Material-reference comparison exact selected material-result references + one implementation-function coordinate tuple + bounded Compare occurrences; no Applicability or Admission by identity
Comparison point carried recorded-reference occurrence + source Locality identity + exact Standing boundary occurrence + addressed Representation; transient read only; no Standing copy; availability != Applicability
View           exact Act occurrence + representation + its carried coordinates
Formation      exact Act occurrence + Yield + representation
Constructor    callable implementation mechanism; no Authority by identity
Owner          responsible boundary bearing an exact Responsibility
Ownership      Assertion concerning that Responsibility assignment
Claim          asserted content
Fact           Assertion described through its bounded Standing
Testimony      asserted content with carried source coordinates
Attribution    Assertion concerning a source relation
Purpose        the exact Act's other carried coordinates
Meaning        Assertion concerning an exact represented relation
Capability     exact Act / Authority / Constraints / Evidence
Gap            bounded Compare result
Goal           locality-bound material concerning a desired result
Demand         shorthand that a bounded result is absent
Reliance       Assertion that an exact input supports an exact result
Continuum      earlier Standing + later occurrence + Compare of preserved coordinates
Closure        bounded Fidelity claim across the exact admitted coordinates
Interrogator   exact material + implementation-function invocation occurrence + exact returned coordinates + Measurement / Compare
Exposure       availability at an exact Locality, or an emitted Representation; resolve the exact Act
Recover        acquisition Act/result + Measurement + Compare + Admission + bounded Standing
Replay         exact recorded Locality occurrences in recorded order + Standing read from no prior Standing; a recorded Act does not occur
Story          ordered exact occurrences through Localities + Acts / Participation + results + later Compare
Addressability of preserved coordinates
```

## Connective shorthand

A connective noun does not establish a Seed relation. Translation resolves the
exact coordinates doing the work:

```text
exact subject or material
    ↓
exact Act + Responsibility + Authority + Scope
    ↓
Act occurrence + Evidence + Participation
    ↓
Yield or exact Locality relation
    ↓
exact result + Standing
    ↓
Compare
```

Material acquisition currently gives a concrete example:

```text
measured source Assertion reference
    + measured material Assertion reference
    ↓
addition Act occurrence at an exact position
    ↓
exact material result identity

source implementation-function invocation occurrence
    + addition Act occurrence
    + result implementation-function invocation occurrence
    ↓
Compare occurrence
```

A composite preserves the same crossings:

```text
removal Act occurrence
    ↓
exact removal result reference
    ↓
addition Act occurrence
```

A connective composite receives no Act, relation, Evidence, Authority, or
Standing by identity.

`Grammar distinctions` are bounded discriminators:

```text
exact material result reference
    + implementation function invocation occurrence
    + complete result coordinates
    + Admission occurrence
```

Same result coordinates do not establish same material, occurrence, identity,
grammar, or Standing. Different result coordinates establish only the bounded
distinction. Neither result establishes what either material represents, and
Admission grouping does not establish language or a represented relation.

## This

`This` is not discarded as connective material and does not establish
currentness or identity by itself. Keep the coordinates that can discriminate
its represented relation:

```text
exact material occurrence
    + Representation occurrence
    + exact addressed subject
    + Locality
    + occurrence boundary
    + represented-relation Evidence or Unknown
```

The same material under another occurrence or Locality does not preserve the
addressed subject by identity. Different material at the same occurrence does
not establish a different addressed subject by identity. Acquisition compares
both directions before a bounded represented relation receives Standing.

None of these shorthands adds a constitutional subject, relation, occurrence,
or Standing. If the expansion loses a distinction, read the missing exact
coordinate rather than restoring the compressed noun.

## Use

Rosetta is for translation. An argument that depends on a shorthand has not
yet reached Seed grammar.
