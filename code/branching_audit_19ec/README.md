# `code/branching_audit_19ec/` — the evidence for mg-19ec

**Work item:** mg-19ec, an independent audit pre-filed in the same action as its parent.
**Target:** `645b5a4` (mg-dffa), which landed mg-5800's four MINOR WARRANT findings on
`docs/OneThird-Branching-Graphs-Where-This-Lives.md` and
`code/branching_repair_41aa/check_doc.py`. **Deliverable:**
`docs/OneThird-Warrant-Repair-mg-dffa-IndependentAudit.md`.

**The four replacement sentences are read here as NEW CLAIMS, with the originals ignored.** A
narrowing can overshoot into a claim false in the other direction, and it can stay too wide
while looking smaller; and a repair whose entire content is rewriting claim statements is
where a wrong new statement is likeliest. So every sentence mg-dffa wrote is measured or
located here against the evidence cited *for it*, not against the sentence it replaced.

## Independence

Imports nothing from `branching_af28/`, `branching_audit_6ad0/`, `branching_audit_5800/`,
`branching_repair_41aa/` or `branching_warrant_dffa/` — checked mechanically by E1c, in both
directions, over all five directories' module names. Where a probe cites one of those it reads
the committed **output** and says so.

## Files

| file | what it settles |
|---|---|
| `PREDICTIONS.md` | every exit code and every substantive prediction, **committed at `170094f` before any probe ran** |
| `kern19ec.py` | posets, `canon`, ideals, lattice operations from the order, Young's lattice, Young–Fibonacci, skew shapes, order isomorphism |
| `selftest19ec.py` | 42 assertions, every one that matters in **both** directions |
| `e1_f1_cells.py` | **F1** — the two WIDENED ledger cells (B1, B5) as new claims |
| `e2_f2_clauses.py` | **F2** — the two NARROWED clauses; every figure re-derived; two unbounded populations |
| `e3_f4_brown.py` | **F4** — Brown `§4.3` re-read on a sixth extractor and **pinned by digest** |
| `e4_f3_control.py` | **F3** — the new control fired in **seven** configurations, four of them new |
| `e5_population.py` | **is four the population?** — three named sub-populations, every site printed |
| `e6_standing.py` | **do not disturb** — the Birkhoff-free converse of X1 **re-measured**, 107 of 405 |
| `e7_instrument.py` | **the thing no list named** — the audited runner's exit contract, and its self-test mutation-tested |
| `run_all.sh` | all of the above, ~35 s |

## The exit contract, and why it is this one

**`run_all.sh` is not green when every probe exits 0. It is green when every probe's exit code
equals the code predicted for it in `PREDICTIONS.md` before the run.** Three of the eight are
predicted to exit 1 because they carry findings; a runner that went red on those would be
reporting findings as breakage, and a runner that went green on a probe predicted to fire and
then silent would be hiding a miss. It exits with the number of misses.

**And `e3_f4_brown.py` returns 2 — not 0 — when it cannot reach arXiv.** That is deliberate and
it is the point of E7a: the instrument this audit examines has a network probe carrying the
whole of F4 which returns 0 when the download fails, so with no network its runner exits 0,
prints `done.`, and shows five green status lines while the premise the document's strongest
sentence stands on is unverified. Here, a probe that verified nothing cannot report green.

## The three controls that decide whether anything here is worth reading

**1. `canon` is the definition, not a shortcut.** The plain minimum over all `n!` relabellings.
mg-5800 recorded a control firing on a cheaper canonical form that reproduced A000112 exactly
to 16 999 while the bug was live, so a counting sequence is not accepted here as a control on a
canonical form. Checked against brute-force isomorphism on **all 3 969 ordered pairs of the 63
poset classes at `n = 5`**. The price is that `n = 7, 8` are out of reach and are **stated as
not established** rather than bought with a refinement.

**2. The Fibonacci rank sizes are not a control on the cover rule.** A deliberately WRONG
`yf_up_covers` is built in the self-test and is **required** to reproduce 1, 1, 2, 3, 5, 8, 13
**and** to fail `DU − UD = I`. Both mg-5800 and mg-dffa recorded the identical failure on their
own instruments.

**3. Nothing on the comparison path knows what a join-irreducible is.** Two lattices are
compared by an isomorphism search on the strict order relation. That is what makes the converse
of X1 measurable **without Birkhoff**, and losing it is the single thing mg-19ec was told to
protect. Checked mechanically against this directory's own source with docstrings and comments
stripped — the first version of that check searched the raw text and fired on its own
docstring.

## Reproduce

```
./run_all.sh                                    # ~35 s, pure Python 3; e3 needs network
```

Committed outputs: `out_selftest19ec.txt`, `out_e1_f1_cells.txt`, `out_e2_f2_clauses.txt`,
`out_e3_f4_brown.txt`, `out_e4_f3_control.txt`, `out_e5_population.txt`, `out_e6_standing.txt`,
`out_e7_instrument.txt`, and `out_upstream.txt` (the re-run of the five earlier suites).

**This directory changes no file it audits.**
