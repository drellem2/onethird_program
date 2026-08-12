# `compression_novelty_623a` — is `docs/imports/compression.tex` new?

Instrument for `mg-623a`. Verdict document:
[`docs/OneThird-Compression-Novelty-mg-623a.md`](../../docs/OneThird-Compression-Novelty-mg-623a.md).

`./run_all.sh` — **32.8 s measured** on the invocation that wrote the committed
transcripts. Pure Python 3, no third-party packages (this host has no `numpy`), and
**no import from any other library in this repository**: a shared poset or eigen library
would make "it agrees" a statement about one derivation read twice.

| file | what it decides | transcript |
|---|---|---|
| `lib623a.py` | posets, linear extensions, the BK chain, `C_o`/`C_e`, pair-orientation statistics — all conventions fixed in one place | — |
| `a1_identities.py` | are the note's four structural claims **true**? Exact `Fraction`, no float. Three inverted controls. | `out_a1_identities.txt` |
| `a2_tightness.py` | does `(**)` **reach** the BK gap, or only bound it from above? `[FLOAT]` | `out_a2_tightness.txt` |
| `a3_sites.py` | the three sites the ticket names, read for their claim; term census with positive controls | `out_a3_sites.txt` |

## Headline

* **A1–A4: 0 failures.** Every labelled poset `n = 2..5` (4 472 of them), 3 coefficient
  vectors each. The cube foliation, the covariance-free fiber variance, the energy
  identity `(*)` and the operator identity `(***)` all hold exactly.
* **A5a/A5b/A6 fire.** The identities fail off their hypothesis (9 420 / 13 416), and
  `P_BK f` is **not** again a pair-orientation statistic (8 796 / 13 416) — which is why
  `(**)` is an upper bound on the gap and not a restriction of the operator.
* **A7.** On `V_k`, the family `docs/OneThird-Hodge-Side-Leverage.md:132` records as having
  AT graph `= Q_k`, the odd compression collapses to **one** fiber and the even to
  singletons. The foliation is trivial exactly where this tree already knew the answer.
* **B2.** The BK bottom eigenfunction is **not** a pair-orientation statistic at
  61 of 195 posets at `n = 4` and **2 260 of 3 810 at `n = 5`** — 59 %, rising. `(**)`
  therefore does not reach the gap at a majority of posets by `n = 5`.
* **C2.** 0 hits for the note's vocabulary across all three repositories, with five
  positive controls nonzero in all three.

## Reads outside this tree: **yes**

`a3_sites.py` greps `/Users/daniel/research/one_third` and
`/Users/daniel/research/one_third_width_three` read-only. Its `C2` transcript therefore
does **not** reproduce from this repository alone, and will drift if either sibling
moves. Declared here rather than discovered later, per the convention every committed
census transcript on `main` already follows.

## Caps and blind spots

* `a1`, `a2`: `n ≤ 5`. `n ≥ 6` is **not** enumerated.
* `a2`: posets with `|L(P)| > 24` are **skipped** (301 of 4 231 at `n = 5`, including the
  large antichains); the count is printed in its own table.
* `a2` is the only float arm; worst Jacobi off-diagonal residual `9.8e-13`, and its
  energy matrix is cross-checked against `a1`'s identity to `7.8e-16`.
* `a3`'s census reads `.tex .md .py .txt .json .lean .html .sh` and skips `.git`/`.lake`;
  a term living only inside a compiled artifact would not be found. `one_third_width_three`
  is 8.1 GB, almost all of it a Lean build tree, which is why the filter exists.

## Three defects of my own, kept

* **D1** — the first `a3` grepped `one_third_width_three` unfiltered and **hung**, killed
  at 120 s with zero output. A timeout very nearly went into the record as a measurement.
* **D2** — `a3` resolved the three site paths against `cwd`, so it worked from the repo
  root and raised `FileNotFoundError` from its own directory. Found by `run_all.sh`, not
  by me. Now resolved against the repository root from `__file__`.
* **D3** — the 32.8 s above is one host, timed on the run that wrote these transcripts.
  It is not a claim about any other machine.
