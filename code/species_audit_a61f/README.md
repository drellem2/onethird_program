# `code/species_audit_a61f` — the audit instrument for mg-a61f

Supports `docs/OneThird-Audit-mg-7d75-Species-Hopf-Monoids.md`.
Target: `docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md` and
`code/species_7d75/` (mg-7d75, `6a22fbc`).

```
./run_all.sh          # ~2 min, pure Python 3, no dependencies, NO NETWORK
./fetch_sources.sh    # the ONE network script; regenerates quotes_a61f.txt
```

`run_all.sh` does **not** call `fetch_sources.sh`. `a5_quotes.py` reads the
committed `quotes_a61f.txt`, so the whole audit reproduces offline.

## Independence

Nothing is imported from `code/species_7d75/` (`kern7d75.py`, `hopf7d75.py`) or
from `core_af28.py` / `kern6ad0.py` / `core1953.py`. Where an object is also
built there, it is built here by a different route:

| object | mg-7d75's route | this directory's route |
|---|---|---|
| labelled posets | subsets of the ordered pairs, then transitivity | three-way choice per **unordered** pair, then transitivity |
| poset classes at `n = 6` | not built | adjoin a **maximal element** to each `n = 5` class (complete, and never enumerates 130 023 labelled posets) |
| `A/rad A` | `Φ` surjective + kernel nilpotent, explicitly **"no trace form"** | rank of the **trace form** `B(x,y) = tr(L_xy)` (Dickson), modulo two primes that must agree |
| set compositions | recursion over subsets of the remainder | recursion by inserting the least element |
| descent algebra | mg-7d75's own | rebuilt here, both composition conventions |

## What each file decides

| file | what it decides |
|---|---|
| `kerna61f.py` | posets, partitions, compositions, the Tits product, `F(P)`, `AC(P)` by two routes, `Aut(P)`, orbits, rank mod `p`, exact null spaces over `Q`, the trace form |
| `a1_headline.py` | the headline identity `(kF(P))^{Aut(P)}/rad = k^{AC(P)/Aut(P)}` — re-measured with **no size cap** on all 87 classes to `n ≤ 5`, exhibited on the rows **between** the two mg-7d75 prints, run **out of sample at `n = 6`**, and then **proved in three lines**, with both steps of the proof checked exactly over `Q`. Two wrong index sets as controls |
| `a2_bidigare.py` | Bidigare rebuilt from both definitions; mg-7d75's T3d table reproduced exactly; then: how many of its four candidate identifications are independent hypotheses |
| `a3_hopf.py` | the Hopf-monoid battery reproduced, then run on the **full ambient**, on a **wrong pairing**, and on a **deliberately broken subset**, to find out which of its five columns can fail at all |
| `a4_counts.py` | 21 numeric claims from the document, recomputed. 20 agree; 1 is **BROKEN** |
| `a5_quotes.py` | every quotation, checked against **poppler-rendered** extractions of the three PDFs — the attack mg-7d75 filed as #1 against itself |
| `a6_boundary.py` | **the primary target**: every derivation classified LOCATED / COROLLARY / MEASURED / DEVELOPED, and the verdict on mg-7d75's prediction about its own locating-exercise boundary |
| `selftesta61f.py` | 456 328 assertions against OEIS A000110 / A000041 / A000670 / A001035 / A000112, the left-regular-band identities, the group axioms, and matrices whose rank is known by inspection |

`quotes_a61f.txt` holds the passages as extracted by `pdftotext`, with the
source URL and the line range in each extraction.

## Caps, each stated where it is used

* `a1` A1c runs `n = 6` for the 179 of 318 classes with `|F(P)| ≤ 300`. The
  other 139 are skipped and counted. **A1d's proof covers every `n`,** so this
  cap bounds the measurement and not the claim.
* `a1` A1a and A1e run to `n ≤ 5` with **no cap** — this closes the 4 classes
  mg-7d75 exempted.
* `a1` A1d's exact-over-`Q` check of the proof's two steps runs to `n ≤ 4`
  (`dim ≤ 75`).
* `a2` runs to `n ≤ 5`, the same reach as the target.
* `a3` is exhaustive on the ground set `[4]`, the same reach as the target.
* `a5` reads the PDFs **as served on 2026-07-30**. A source revised after that
  date could move a line range; the passages themselves are committed.

## What this instrument does NOT establish

* Nothing about Solomon's theorem or Garsia–Reutenauer/Atkinson. Those sources
  were not fetched and the identification of the semisimple quotient with the
  character ring of `S_n` is **unchecked here**, exactly as mg-7d75 says.
* Nothing about Aguiar–Mahajan 2020, Aguiar–Mahajan 2017, Saliola or Commins.
  Not fetched, not read — so mg-7d75's `S12` non-location is not re-searched
  here; it is instead **dissolved by proof** in A1d, which is a stronger
  answer than a better search would have been.
* Nothing about whether our `F` is one of the published Hopf monoids under a
  different name. mg-7d75 §7 item 2 leaves that open and so does this.
