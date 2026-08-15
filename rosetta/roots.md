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
    seed_runtime.byte_measurement::record_byte_count_layer
    seed_runtime.byte_measurement::record_adjacent_byte_pair_count_layer

Yield Evidence
    seed_runtime.yield_evidence::_record_yield_evidence

Assertion addressability and locality movement
    seed_runtime.byte_measurement::assertions_of_recorded_byte_measurement
    seed_runtime.byte_measurement::_move_byte_assertion_to_locality

Applicability
    seed_runtime.byte_measurement::get_recorded_pair_input_applicability

Emission Locality / Participation / Yield
    seed_runtime.operator_representation::emit_operator_representation

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
Lineage        ordered source and occurrence references beneath Provenance
Artifact       exact representation, record, Assertion, or result
Projection     exact Act occurrence + representation + its carried coordinates
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
Addressability of preserved coordinates
```

None of these shorthands adds a constitutional subject, relation, occurrence,
or Standing. If the expansion loses a distinction, read the missing exact
coordinate rather than restoring the compressed noun.

## Use

Rosetta is for translation. An argument that depends on a shorthand has not
yet reached Seed grammar.
