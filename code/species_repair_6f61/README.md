# `code/species_repair_6f61` — the repair of mg-7d75 under mg-a61f's audit

Instruments for **mg-6f61**, landing the findings of
`docs/OneThird-Audit-mg-7d75-Species-Hopf-Monoids.md` into
`docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md` and into
`code/species_7d75/`. The reasoning is in
`docs/OneThird-Species-Hopf-Monoids-Repair.md`.

Run: `./run_all.sh` — pure Python 3, no dependencies, **no network**, about
30 seconds, of which `r2_columns.py` is 27.

Shares no code with `code/species_7d75/` (`kern7d75.py`, `hopf7d75.py`) or
`code/species_audit_a61f/` (`kerna61f.py`). Where an object is also built
there it is built here by a **third** route, so agreement is evidence:

| object | 7d75 | a61f | here |
|---|---|---|---|
| poset | frozenset of ordered pairs | frozenset of ordered pairs | **tuple of int up-masks** |
| poset enumeration | subsets of the pairs, incremental closure | three-way choice per unordered pair, then a transitivity test | **fixed points of the Warshall closure** |
| face | tuple of frozensets, recursive block choice | tuple of frozensets, recursive insertion | **tuple of int masks, from block-index functions** |
| quotient acyclicity | DFS colouring | DFS | **Kahn's algorithm** |

Certified in `selftest6f61.py` (3 188 assertions) against **A001035**
(labelled posets), **A000112** (poset classes), **A000670** (faces),
**A000110** (flats) and **A000142** (`|Aut|` of the antichain), plus the
closed forms `2^{n-1}` for the chain's faces and hand-checkable small cases —
external anchors only, nothing either predecessor computes.

| file | what it does |
|---|---|
| `kern6f61.py` | posets, faces, flats, `AC(P)` by two routes, automorphisms, canonical form, and a bimonoid battery **generic in the collection AND in the operations** |
| `r1_smallest.py` | **X1.** The smallest poset with `AC(P) ≠ Π[n]`, computed exhaustively to `n ≤ 4`: it is the **3-chain**, 6 labelled witnesses in one isomorphism class, not `{a<c, b<d}`. 11 predictions written before the run; a control shows the search can return `n = 2` |
| `r2_columns.py` | **X3.** Per column, whether it can fail — **six collections** with the operations fixed, **three operation mutations** with the collection fixed. 45 cells, every one predicted before the run |
| `r3_quotes.py` | **X6/X7/X8.** The two corrected quotations and the restored truncation, re-derived from the audit's committed `pdftotext` extraction, offline; and the **anticipated-vs-unanticipated** ledger |
| `check_doc.py` | reads the repaired documents off disk: every false sentence must survive **only** inside the strike that replaces it, every correction must be present, and mg-a61f's own anchors must survive |
| `selftest6f61.py` | 3 188 assertions |

**Three design points worth knowing before reading the outputs.**

*`R2 PREDICTIONS MISSED: 2 of 45` is not a defect and is not zero.* Every cell
of the mutation battery carries the outcome predicted **before** the run. Two
missed — the even-block-count predicate turned out to be closed under
concatenation (block counts add, so parity survives), and swapping the two
tensor factors of the coproduct turned out to be a **symmetry** of the
compatibility axiom. Both are explained in `out_r2_columns.txt` R2e and kept
exactly as written. `R2 TOTAL BAD` counts something else: **columns left with
no demonstrated failure on either axis**, which is 0. A miss folded into a
fault count is a miss that gets edited away.

*The negative half of `check_doc.py` is the load-bearing half.* Ten false or
superseded sentences are required to occur in the document **and to occur
nowhere outside a `~~struck~~` span**. A repair that adds a correction beside
a false sentence and leaves the false sentence in force has repaired nothing.

*Nothing here re-fetches a PDF, and nothing here re-runs the audit.*
`r3_quotes.py` compares the repaired document against
`code/species_audit_a61f/quotes_a61f.txt`, the extraction the audit committed,
and re-derives each verdict from the passage rather than trusting the audit's
prose. mg-a61f's battery was separately re-run **unmodified** against the
repaired document and reports exactly what it reported before —
`A4 TOTAL BAD: 1`, which is X1, and 0 everywhere else. `check_doc.py` asserts
the sixteen strings that battery depends on, so a future edit that would make
the document unauditable fails here first.
