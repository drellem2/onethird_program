# `code/branching_audit_a218/` — the instrument for mg-a218

The independent audit of **mg-e8b8 / `2e66d03`**, the repair of mg-db09 that
mg-2060 called for. Target: `docs/OneThird-Bratteli-Path-Algebras-Where-This-Lives.md`
and `code/branching_locate_db09/`.

```
./run_all.sh        # ~1.5 min, pure Python 3, NO NETWORK
```

## This audit shares no code with either instrument it audits

`kern_a218.py` rebuilds Temperley–Lieb from the definitions in the papers the
target quotes: planar diagrams as perfect matchings of `2n` points, link
states as non-crossing partial matchings with no defect nested inside an arc,
the cell modules `V(n,p)` with the diagram action truncated to zero when the
defect count drops, the cellular bilinear form, `L(n,p) = V(n,p)/rad⟨,⟩`, and
the trace form of the regular representation. All arithmetic is exact
(`Fraction`); `β` is an integer at every parameter measured.

It is the **third** instrument to measure this object. mg-db09's `t1_tl.py`
(`T1b2`) is the first, mg-2060's `b1_branching.py` (`B1a`/`B1b`) the second.

## Exit-code convention

Every `c*.py` exits `0` **iff `SELF-ERRORS == 0` and `FINDINGS == 0`**. A
non-zero exit means *"this script has something to report"*, never *"this
script is broken"* — the two numbers are printed separately so the code is
unambiguous. `selftest_a218.py` exits `0` iff every assertion passes.
`PREDICTIONS.md` holds the exit code predicted for each script **before any of
them was run**, and the two wrong predictions are kept as written.

**Every count in every output names its population.** A bare total is not a
measurement.

## The scripts

| script | what it does |
|---|---|
| `selftest_a218.py` | 80 001 assertions on this audit's own kernel: ballot numbers, Catalan counts, the TL relations, associativity, the module axiom, symmetry of the Gram form, the five published Ridout–Saint-Aubin semisimplicity controls, and `Σ_p (dim L)² = dim A/rad` by **two disjoint routes** on all 24 `(n, β)` pairs |
| `c0_repro.sh` | copies `code/branching_locate_db09/` to a scratch directory, runs its `run_all.sh` **against the repaired code**, and diffs all five committed outputs byte for byte; also checks the document's stated `699 520` assertions and the four `TOTAL BAD: 0` lines |
| `c1_branching.py` | **the primary target.** The branching graph as Vershik–Okounkov define it, measured in **every cell** — the labelled vertex set at every level of every parameter, and every ordered pair `(p,q)` of restriction multiplicities including the zeros — then compared cell by cell against mg-e8b8's committed `out_t1_tl.txt` |
| `c2_vertexsets.py` | the vertex **set** against the vertex **count**, for every ordered pair of parameters at every level; and the repair's own new claim that `T1b2` *"agrees ROW FOR ROW with mg-2060's B1a/B1b"*, measured across all three instruments |
| `c3_withdrawal.py` | 38 named text checks: is the withdrawal stated as a withdrawal, is the verdict attributed to the theorem, is the withdrawn claim still asserted anywhere in prose **or instrument**, does D10 read as a conjecture, is the retraction in the document, are the other unverified items marked — and a **deletion test** that every sentence of the pre-repair §4 item 3 survives verbatim |
| `c4_seam.py` | the seam sweep. Similarity **threshold 0.80** (`difflib.SequenceMatcher` on normalised, case-folded text) of every quotation unit in six files against every line the two correcting commits **deleted** |
| `c5_record.py` | the retraction as a *record* — the item no list names — plus whether *"deliberately NOT repaired"* is accurate about mg-2060's X2 |

## Two marker lists were widened after their first run

Both widenings are recorded in the source with the reason, and neither is
silent: `c3`'s withdrawal-marker list gained `"failing phrase"` and
`"asserted"` after the first run flagged the one sentence that *performs* the
withdrawal, and `c4`'s gained `"not read"` and `"NOT evaluated"` after the
first run flagged two bibliography lines whose **added** text already carries
that status. `c0`'s `TOTAL BAD` population was corrected from five files to
four: the self-test is not one of the four test scripts and prints no
`TOTAL BAD` line. Each was this instrument's error, not the target's.
