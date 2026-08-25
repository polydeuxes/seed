# Rosetta of Seed

This directory holds translation testimony: ordinary English about Seed's grammar, and mappings from
words people have used to whatever current grammar corresponds to them. A
mapping recorded here establishes no standing, no kind, and no equivalence.

This is not part of the Book of Seed and is not stored inside it. English
placed inside `book_of_seed/` acquires ambiguous status, since a reader
cannot tell whether a sentence is grammar or explanation. Keeping explanation
outside removes the ambiguity in both directions: the Book can be grammar-only,
and this can be plainly readable.

## Purpose

The Book sheds words. Terms leave when they name nothing, when they
compress several distinctions into one word, or when they are ordinary English
that acquired constitutional-looking capitalisation.

Retiring a word from the Book does not delete what it meant or why it went.
That knowledge cannot live in the Book: a maintained list of dead words
keeps dead words present in the grammar. It lives here.

## Scope

```text
Responsibility spine        ordinary-English traversal of the same spine used
                            by the Book and instantiated by runtime occurrences;
                            Examination and Presentation are directional views

translation words           words the Book does not use, and what
                            current grammar covers what they covered

external / ordinary words   English that was never constitutional but
                            reads as though it might be

implementation words        runtime and repository names that are not
                            constitutional grammar


implementation              names for how something is done on this machine
                            in this language, whose exact behavior supports
                            no constitutional clause, recorded so they stop
                            being audited as though it might

worked explanation          ordinary prose returned for material like
                            "what does Standing mean"
```

## Disposal rule

A word is not preserved merely because it was deleted.

```text
useful for translating history or explaining the grammar?
    yes  →  record it here
    no   →  gone
```

This directory is not a landfill for everything ever removed, and not a
banned-word registry. Banning is a curation decision; translation is the work
done here.

External acquisition is not Rosetta. Observed external material, occurrences,
Assertions, and relations remain on their own bounded road; they do not enter
this directory merely because Seed observed them. Implementation references in
Rosetta are representative translation witnesses, not an implementation index.

## Constitutional boundary

`01.Source` governs the boundary this directory sits on: ordinary words
may retain source coordinates and be compared **without thereby becoming
constitutional grammar**. That chapter carries the applicable source rule. It is
not itself a Rosetta, and this directory is not a chapter.

A Rosetta representation produced under bounded translation does not become
constitutional because Seed produced it.

## Neighbouring artifacts

```text
book_of_seed/       constitutional grammar only
rosetta/concordance.md navigation across live grammar, with aliases
rosetta/            translation words and exact mappings
reports + git       historical testimony, preserved as written
```

The concordance maps live terms and states that aliases "do not grant
constitutional equivalence or standing." This directory maps those words,
where the mapping is frequently not an alias relationship: `State` corresponds
to four current terms and to no single one of them.

## Files

- [Responsibility spine](roots.md)
- [Concordance](concordance.md)
- [Rosetta admission](rosetta_admission.txt)
- [Book admission](../book_of_seed/book_admission.txt)

Rosetta keeps the translation lexicon. The Book keeps its own narrower admission
and points here without importing Rosetta admission into active law. In
particular, Rosetta admits the `warrant` word family while Book proper names
the exact source and occurrence coordinates, Scope, preserved limits, and
support relation.

The Book's Responsibility spine supplies the ordering. Rosetta words hang
from the exact coordinates they translate, or record a word that named nothing
so its removal stays legible.
