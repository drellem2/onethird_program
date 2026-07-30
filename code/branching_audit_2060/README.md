# `code/branching_audit_2060` — the instrument for the independent audit of mg-db09

Supports `docs/OneThird-Bratteli-Path-Algebras-IndependentAudit.md`.
Audits `code/branching_locate_db09/` and
`docs/OneThird-Bratteli-Path-Algebras-Where-This-Lives.md` (commit `03d7f91`).

```
./run_all.sh      # ~20 min, pure Python 3, no dependencies, NO NETWORK
./fetch2060.sh    # the ONE network script; run_all.sh does not call it
```

## What each file decides

| file | what it decides |
|---|---|
| `kern2060.py` | exact linear algebra over `Q`; Temperley–Lieb diagrams, link states, cell modules, the bilinear form; the radical by the trace form with an independent nilpotency check; posets, `F(P)`, `AC(P)`, the band algebra |
| `b0_repro.sh` | mg-db09's own instrument, re-run in a scratch copy, its five committed outputs diffed **byte for byte** |
| `selftest2060.py` | 56 940 assertions against facts independent of the target: Catalan numbers, the Catalan triangle, associativity, `e² = βe`, the three published TL semisimplicity controls, trace-form vs Gram-form agreement, Fubini and Bell numbers, the left-regular-band identity |
| `b1_branching.py` | **the finding.** The branching graph of the TL tower under Vershik–Okounkov's definition — vertices are irreducibles, edges are restriction multiplicities — at `β ∈ {3,2,1,0}`. Plus VO Prop. 1.4's centralizer test applied to the TL side, where mg-db09 did not run it |
| `b2_pathbasis.py` | the claim no pre-filed list names: *"a path-pair basis exists **iff** `dim A = Σ (#paths)²`"*, refuted in the "if" direction by construction |
| `b3_quotes.py` | quotations against PDFs **this audit fetched**: every content line of mg-db09's own `sources_db09.txt` (the fabrication check), 22 quotations taken out of the delivered prose including 9 that T4 does not cover, six negative controls, and D9 closed against a refereed source |
| `b4_ours.py` | `kF(P)` with **no size cap** — all 87 poset classes to `n ≤ 5` including `\|F\| = 541`; the Cartan matrix rebuilt from MSS's closed formula (4.9) with the Möbius function; the "symmetric ∧ unitriangular ⟹ identity" one-liner executed |
| `b5_successor.py` | the proposed successor: CMPX's axioms quoted from the paper, (A1) tested and exhibited, (A3) tested, (A2)(i) measured over **every** face idempotent realising (A1) |
| `b6_ledger.py` | the derivation census — located / commissioned / developed-here, and which mg-db09 flagged — and its claim ledger re-scored on the numbers this audit can check |
| `b7_gz.py` | mg-db09's T2 recomputed on a disjoint instrument: `dim GZ`, skipped chains, the six centralizers, `ℂS_4` |

## Independence

Written fresh. It imports nothing from `code/branching_locate_db09`,
`code/branching_af28`, `code/species_7d75` or any other directory here.
`b0_repro.sh` and `b3_quotes.py` are the only files that read the audited
directory at all, and they read it as **data to check**, not as code to reuse.

Where the same object is built twice, the routes are chosen to share nothing:

* **The radical** is the radical of the trace form, and is separately verified
  to be a two-sided nilpotent ideal without using Dickson's theorem.
* **The simple TL modules** are `V(n,p)/rad⟨,⟩` from the Gram form; the
  agreement `Σ_p (dim L(n,p))² = dim A − dim rad` is checked on all 20 `(n,β)`
  pairs and is what validates both routes at once.
* **Restriction multiplicities** come from characters, and the solve is checked
  for uniqueness, integrality, non-negativity **and** the dimension identity
  `Σ_q m_q · dim L(n−1,q) = dim L(n,p)`.
* **The Cartan matrix** is rebuilt from formula (4.9), not from the character
  argument mg-db09 used, and is checked by the **per-column** identity
  `Σ_X C_{X,Y} = |L_Y|` — strictly stronger than the total `Σ C = dim A`.

## Sources

`sources2060/` holds the **whole** `pdftotext` extraction of each paper,
gzipped, with `SHA256SUMS.txt` for the PDFs. A line-numbered window is a claim
about where a sentence is; the whole file is not, and it lets an auditor of this
audit grep for anything, including sentences this audit chose not to quote.

Two papers are new to this lineage: **Ehrig–Tubbenhauer, `arXiv:1710.02851`**
(which closes mg-db09's self-declared weakest citation) and
**Cox–Martin–Parker–Xi, `arXiv:math/0411395`** (which mg-db09 had as *"located,
NOT evaluated"*).

## Reading the `TOTAL BAD` lines

Not all of them mean the same thing, and saying so here is the point.

* `b0`, `b2`, `b4`, `b5`, `b6`, `b7` — `TOTAL BAD: 0`. These count **errors in
  this audit's own instrument**.
* `b1` — **`TOTAL BAD: 2`**, and both are **findings**: they count disagreements
  between what mg-db09 states and what the branching graph measures.
* `b3` — **`TOTAL BAD: 1`**, and it is a **finding**: 1 of 22 quotations taken
  out of the delivered prose is not verbatim. The deviation is a single inserted
  comma and the near-miss analysis prints it character by character.

## Conventions that have bitten this repo before

* `V(n,p)` is indexed by `p` = the number of **arcs**, which is mg-db09's
  indexing, kept so the tables compare row for row. The number of defects is
  `n − 2p`.
* A **link state** is a non-crossing partial matching in which no arc covers a
  defect. It is generated here as a bracket word with every defect at nesting
  depth 0, which is what makes the count `C(n,p) − C(n,p−1)`.
* `frozenset` is only **partially** ordered by `<`, so `sorted()` on tuples of
  frozensets is not canonical. Faces are compared as sets, never by sorting.
  This cost a false negative in `b5` before it was caught.
* The order convention on `Λ(B)` under which MSS formula (4.9) is correct is
  `X ≤ Y ⟺ X refines Y`. It is **determined by the checks**, not chosen: the
  other convention gives a matrix with the wrong diagonal.
