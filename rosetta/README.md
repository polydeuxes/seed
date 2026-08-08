# Rosetta of Seed

**Nothing in this directory carries constitutional Authority.** It is
translation testimony: ordinary English about Seed's grammar, and mappings from
words people have used to whatever current grammar corresponds to them. A
mapping recorded here establishes no standing, no kind, and no equivalence. It
records what a term was reaching for, and nothing more.

This is not part of the Book of Seed and is deliberately not stored inside it.
English placed inside `book_of_seed/` acquires ambiguous authority — a reader
cannot tell whether a sentence is grammar or explanation. Keeping the
explanation outside removes the ambiguity in both directions: the Book can
become grammar-only, and this can be plainly readable.

## Why this exists

The Book has been shedding vocabulary. Terms are retired when they turn out to
name nothing, to compress several distinctions into one friendly word, or to
be ordinary English that acquired constitutional-looking capitalisation.

Retiring a word from the Book should not delete the knowledge of what it meant
and why it went. But that knowledge cannot live in the Book, because
maintaining a list of dead vocabulary keeps dead vocabulary present in the
grammar.

## What belongs here

```text
retired vocabulary          words the Book no longer uses, and what
                            current grammar covers what they covered

external / ordinary words   English that was never constitutional but
                            reads as though it might be

implementation vocabulary   runtime and repository names that are not
                            constitutional grammar

worked explanation          ordinary-language answers to "what does
                            Standing actually mean"
```

## What does not belong here

A word is not preserved merely because it was deleted. The disposal rule:

```text
useful for translating history or explaining the grammar?
    yes  →  record it here
    no   →  it is simply gone
```

This directory is not a landfill for everything ever removed, and it is not a
banned-word registry. "Banned" is a curation decision; translation is this
directory's job.

## The governing constitutional clause

`01.External` in the Book governs the boundary this directory sits on: external
vocabulary may be translated, attributed, and compared **without thereby
becoming constitutional grammar**. That chapter is the authority *for* a
Rosetta. It is not itself a Rosetta, and this is not a chapter.

The recursion worth noting: a Rosetta representation produced under bounded
translation does not become constitutional merely because Seed produced it.

## Relationship to the other artifacts

```text
book_of_seed/       constitutional grammar only
concordance.md      navigation across live grammar, with aliases
rosetta/            external and retired vocabulary, translation
reports + git       historical testimony, preserved as written
```

The concordance maps *live* terms and warns that aliases "do not grant
constitutional equivalence or standing." This directory maps *retired* ones,
where the honest entry is often not an alias at all — `State` corresponds to
four current terms and no single one of them.

## Files

- [Retired vocabulary](retired-vocabulary.md)
