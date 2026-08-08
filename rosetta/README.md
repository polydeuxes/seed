# Rosetta of Seed

**Nothing in this directory carries constitutional Authority.** It holds
translation testimony: ordinary English about Seed's grammar, and mappings from
words people have used to whatever current grammar corresponds to them. A
mapping recorded here establishes no standing, no kind, and no equivalence.

This is not part of the Book of Seed and is not stored inside it. English
placed inside `book_of_seed/` acquires ambiguous authority, since a reader
cannot tell whether a sentence is grammar or explanation. Keeping explanation
outside removes the ambiguity in both directions: the Book can be grammar-only,
and this can be plainly readable.

## Purpose

The Book sheds vocabulary. Terms are retired when they name nothing, when they
compress several distinctions into one word, or when they are ordinary English
that acquired constitutional-looking capitalisation.

Retiring a word from the Book does not delete what it meant or why it went.
That knowledge cannot live in the Book: a maintained list of dead vocabulary
keeps dead vocabulary present in the grammar. It lives here.

## Scope

```text
retired vocabulary          words the Book no longer uses, and what
                            current grammar covers what they covered

external / ordinary words   English that was never constitutional but
                            reads as though it might be

implementation vocabulary   runtime and repository names that are not
                            constitutional grammar

worked explanation          ordinary-language answers to questions like
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

## Constitutional authority

`01.External` governs the boundary this directory sits on: external vocabulary
may be translated, attributed, and compared **without thereby becoming
constitutional grammar**. That chapter is the authority *for* a Rosetta. It is
not itself a Rosetta, and this directory is not a chapter.

A Rosetta representation produced under bounded translation does not become
constitutional because Seed produced it.

## Neighbouring artifacts

```text
book_of_seed/       constitutional grammar only
concordance.md      navigation across live grammar, with aliases
rosetta/            external and retired vocabulary, translation
reports + git       historical testimony, preserved as written
```

The concordance maps live terms and states that aliases "do not grant
constitutional equivalence or standing." This directory maps retired ones,
where the mapping is frequently not an alias relationship: `State` corresponds
to four current terms and to no single one of them.

## Files

- [Retired vocabulary](retired-vocabulary.md)
