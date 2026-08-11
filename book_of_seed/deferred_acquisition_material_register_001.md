# Deferred acquisition material: register 001

Not a plan. A record of material the operator named for a later Acquisition
Seed, so it is not re-derived from conversation. Nothing here is admitted to
`corpus/`, and admission rules follow.

## Admission rule, from this session

```text
  while building Seed      public domain, CC0, or Unlicense only,
                           established at the exact work and release
  once Seed acquires       the operator's personal collection becomes
    through its own egress available, and licence terms stop governing what
                           may be held locally
```

**[inference]** Egress does not change what material is. It changes who
performed the acquisition. The reason the second store can relax is that the
operator is acquiring on their own machine for their own use — not that the
mechanism launders terms.

**The boundary must be a recorded coordinate, not a filename.** Once two stores
exist, a comparison across them consumes inputs carrying different terms and
nothing in the record says so. `#2410` established that provenance lives outside
Seed by default, which is fine while `corpus/SOURCES.md` is the only consumer
and stops being fine the moment a derived Seed is produced. The terms belong in
the bounded exchange's own record from the first ingest of the second store, as
Scope — so a later act can decline to cross it.

## District A — operator's list, restricted for now

```text
  Knowledge and Decisions        knowledge, decision, incentives
  Basic Economics                broad economic grammar
  Capitalism and Freedom         Authority, institutions, choice
  Buffett Essays                 business, value, capital, accounting
  Lombard Street                 money, banks, credit, liquidity
  Wealth of Nations              production, labour, price, trade
```

**[measured]** `Wealth of Nations` and `Lombard Street` are already public
domain; `smith_wealth_of_nations.txt` is in `corpus/` now. The rest are the
restricted district.

## District B — public-domain software

Curator's list. The admission rule is **explicit PD/CC0 at the exact work and
release**, never "open source", and never a whole organisation.

```text
  SQLite            PD dedication, signed affidavits, ~14 MB, tests included
                    parser, planner, VM, B-tree, transactions, journal, locking
  D. J. Bernstein   qmail, djbdns, daemontools, cdb, checkpassword, clockspeed
                    explicit PD dedications, one author, six different problems
  NIST              per-repository only; some carry Apache or external material
  USGS              CC0 by policy; per-release only, non-federal contributions exist
  18F               worldwide CC0 dedication on many repositories
  stb               single-file C libraries, explicit PD option beside MIT
  LibTom            LibTomCrypt PD; family is Unlicense/WTFPL-grade
```

**[inference]** Preserve source URI, project and release as **Seed provenance**
even where attribution is not legally required. That is Evidence, not licence
compliance, and it keeps a derived Seed free of NOTICE obligations while Seed
still knows where its material came from.

## What measurement would find there, measured before it is built

**[measured]** Current forms are byte-for-byte adjacency at declared
displacements. Token populations differ sharply:

```text
  prose (Austen)    'the':4509  'to':4275  'of':3899  'and':3444
  seed_runtime/*.py '=':1254    ')':800    'not':606  'if':592
  bash guide        '#':11354 outranks 'the':6041
```

**[measured]** Code's top-10 tokens carry **16.5%** of all tokens against
prose's **20.7%**, on roughly half the distinct vocabulary.

**[inference]** Under the current forms a software district would recur on `=`,
`if`, `(` and `return` across every C body, and report that they are all C.
That is not a reason to withhold the district; it is a reason not to read
`('if','(')` in nine bodies as a discovery. Adding it tests nothing new until a
form exists whose subject is not token adjacency.

## The scaling wall, computed not run

Scaled from the Test Seed's measured 720,881 comparisons over 120 body-pairs at
540/s and 5,096 B each:

```text
  bodies   body-pairs        comparisons       storage      elapsed
      16          120            720,881        3.7 GB        0.4 h
     100        4,950         29,736,341      151.5 GB       15.3 h
     500      124,750        749,415,873    3,819.0 GB      385.5 h
    1000      499,500      3,000,667,162   15,291.4 GB    1,543.6 h
```

**[measured]** Ingest is linear — ~2,000 events/s across sources from 3,956 to
974,256 lines. Nothing above ingest is.

**[inference]** So a large corpus is affordable to **acquire** and unaffordable
to **sweep**. The all-pairs comparison is a Test Seed act. At district scale the
open question is *what selects the pairs*, and `#2431` already holds that a
declared Scope must be declared rather than discovered — which at 16 exchanges
is a list one can type and at 1000 is a selection nobody has warranted.

## Distinctions this material will force, already owed

**[measured]** `corpus/` currently holds two Douay-Rheims editions, one of them
named `latin_vulgate.txt` for four reports before `#2435` withdrew the finding
that rested on it.

The list the departing worker recorded, which is not future work:

```text
  repeat presentation        edition          quotation
  same representation        revision         independent source
  republication              translation
```

**[inference]** Two of those are already unlabelled in the corpus today. Byte
deduplication would erase the distinction rather than establish it.

## What this register does not establish

**That any of it should be acquired.** It records what was named and why, so the
reasoning is not reconstructed from memory later.

**That the districts are separable by subject.** Literature, law, economics and
software are a reader's grouping. `#2408` established that a reader's categories
predicted nothing about the sixteen sources already held.

**That egress is close.** The operator's position stands: it is not near. This
register assumes the restricted district waits, and says so rather than planning
around it.
