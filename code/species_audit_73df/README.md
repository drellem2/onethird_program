# `code/species_audit_73df` — the independent audit instrument for mg-73df

Audits the **final state** of `docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md`
— that is `83ac472` (mg-6f61) **plus** `a13b4a9` (mg-f8fa), the two commits that
repaired mg-7d75 after the audit mg-a61f — together with the instrument trees
`code/species_7d75`, `code/species_repair_6f61` and `code/species_remainder_f8fa`.

```
./run_all.sh          # ~100 s, pure Python 3, NO NETWORK
```

`c4_scope.py` shells out to `git archive 83ac472` (local) for the pre-repair tree and
to `code/species_remainder_f8fa/w3_scope.py` for one of its controls. If `git` is
missing the control is recorded as **SKIPPED and counted as a fault**, never silently
passed.

## What it shares with what it audits

Nothing. `kern73df.py` imports from none of the four trees and no routine was copied
from any of them. Posets are enumerated by extending a strict order and rejecting
non-transitive candidates (not as Warshall fixed points, not from a cover generator);
faces come from a block-by-block ordered-partition recursion and a cone filter (not
from block-index functions); quotient acyclicity is a depth-first cycle search (not
Kahn's algorithm). The self-test anchors every count to **A001035, A000670, A000110,
A000112, A000041 and A000142** — 5 384 assertions — and independently rebuilds
`|F| = 4399`, `|AC| = 2685` and `|P × Σ| = 16425` on the ground set `[4]`.

## The files

| file | what it decides |
|---|---|
| `selftest73df.py` | the kernel against six OEIS sequences, plus positive controls on the measuring routine itself |
| `c1_columns.py` | the five bimonoid columns, per column, on **seven collections and five operation mutations chosen here** — 60 cells, every one predicted before the run |
| `c2_pinned.py` | "no sub-collection can move three of the columns" swept over 24 arbitrary sub-collections, with a non-vacuity check and a positive control |
| `c3_bidigare.py` | T3d and T3e rebuilt from both definitions; and whether §0's *"the left side **is** Solomon's descent algebra"* is loose wording or false |
| `c4_scope.py` | **all eight** of mg-6f61's corrections scanned across three trees, with four controls |
| `c5_doc.py` | the seam between the two repairs: duplicate passages, stale cross-references, survivals in **both** directions, and 24 cited figures against the outputs they are cited to |

## `TOTAL BAD` here counts FINDINGS, not faults

Following `code/species_audit_a61f`: a non-zero `TOTAL BAD` is this instrument
reporting something about the audited work, not something wrong with itself.
`C1 PREDICTIONS MISSED` is on its own line and is **not** folded into it — a miss is a
finding, and a finding counted as a fault gets edited away.

```
C1 PREDICTIONS MISSED: 4 of 60      four of my own predictions missed, kept as written
C1 TOTAL BAD: 0                     every column demonstrated able to fail
C2 TOTAL BAD: 0                     72 of 72 pinned cells zero, non-vacuously
C3 TOTAL BAD: 0                     T3d and T3e reproduce entry for entry
C4 STILL ASSERTED AT SOURCE: 4      two corrections still in force in code/species_7d75
C4 TOTAL BAD: 1                     w3_scope.py's docstring vs its own evidence file
C5 TOTAL BAD: 5                     one duplicated passage, four stale cross-references
```

## Two defects this instrument found in itself, kept on the record

1. **`c2_pinned.py`'s first sweep was vacuous.** Applying the arithmetic rule to every
   ground set emptied the one-element components, and then *every* associativity
   triple needs an empty component — so the sweep reported `0` by testing nothing.
   That is the exact failure the file exists to exclude, and it turned up inside the
   file rather than in the thing audited. The triple count is now printed for every
   rule.
2. **`c4_scope.py`'s first exoneration rule was disarmed by an adjacent unrelated
   phrase.** It accepted the generic English *"is not the …"*, and
   `t6_fock_and_record.py`'s *"is not the framework this ticket is about"* — four
   lines below the X3 sentence and about something else entirely — cleared it. That is
   `w3_scope.py`'s own recorded false negative, reproduced against this file by the
   same mechanism, and it is why the rule is now the narrow one.
