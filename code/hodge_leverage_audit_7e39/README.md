# mg-7e39 — the independent audit of the mg-6df0 repair

Target: the repair of the **mg-ec07 verdict** — `77306a7`, on
`code/hodge_leverage_landing_e1d0/verify_landing.py`. The repair is derived from git by the
instrument, never named as a sha in its source.

    sh run_all.sh          # ~2 min, exit 0

Report: `docs/OneThird-Hodge-Side-Leverage-Mg6df0RepairAudit.md`.
Predictions, written before the first run and **committed before any transcript existed**:
`PREDICTIONS.md`. Committed transcript: `out_audit_7e39.txt`.

## What is mine and what is the artifact's

The brief's standing direction is *replication is not corroboration when the copies share a
source — build your own instrument*. So:

| | |
|---|---|
| **mine** | the two site cutters, written from the repair's own **disclosure sentences** rather than from its code; the twelve kind derivations; the file write-back; the AST sweep; every population; and the scoring, which runs `verify_landing.py` **as a subprocess** and reads gate rows out of its stdout. No cell of the matrix is decided by anything imported from the artifact |
| **the artifact's** | the figure-token grammar and the figure/segment seam (`partition`) in B6, because that seam is the definition under audit — declared, with the token counts cross-checked against a naive regex of mine, which misses the `+755` form and says so; and the gate itself everywhere, because the gate is the **subject** |

`B0d` is the check that the two readings meet: cutters written from the sentences reproduce the
artifact's three sites **byte for byte at 3 of 3**. That is what makes those sentences a
specification rather than a label.

## The four things the brief asked for

| | |
|---|---|
| **the matrix, not a total** | `B1` — 12 kinds × 3 sites, built again, **29 of 29 applicable cells fire, 0 silent, 7 n/a**. `B1e` puts it against the artifact's own cell by cell: **35 of 36 agree**, and the one disagreement is applicability |
| **the refusal over all 34 rows** | `B3` — the three rows the substring test excluded are the `RECORD PARTITION` rows, one per site. `partition` bent lossy **at one site at a time**: **3 of 3 REFUSE at HEAD**, and the same probe at the pre-repair commit **BLESSES 3 of 3 with the record rewritten**. The parent demonstrated this once, with all three bent together |
| **exist vs touched** | `B4` — **6 instances existed at the repair's parent, the repair touched 1, 5 are live in the commit it landed in.** Every one carries a declared disposition; four of the five select 6 rows where 3 were meant |
| **do not disturb** | `B6` — **37 909 of 37 909** lossless at the site (the population mg-ec07 measured at 37 866, grown by the repair's own 43), control **462 of 37 909 (1.2%)** at `eb600f7`, and **847 of 847** figure exchanges undisturbed with `FIGURE ORDER` refuted and `SITE RECORD` green on every one. **No regression.** |

## The floor — the thing no list in the brief names

`B2`. **`n/a` is where a matrix hides.** The repair's own predictions record that its first
matrix reported 19 applicable cells because a write-back was failing silently, and state the
lesson in as many words: *a derivation that fails silently reads exactly like a site that has no
such text.* So every one of the eight `n/a` reasons is read here as a **claim about the site**
and measured against the site independently — pipe rows, whitespace-column rows, figure-carrying
rows, header lines, marked quotations, quotations carrying figures, paragraphs. Seven survive.
One does not.

## Findings

| | |
|---|---|
| **F1** | `K11 @ the STATE.md row` is `n/a` with the reason *"no line here has two runs of two or more spaces to shift"* — a fact about the **derivation**, which shifts whitespace columns, not about the site, which is a **markdown pipe table** whose alignment is its cell padding. An independent alignment shift **FIRES**, caught by `SITE RECORD`. The matrix is 8 `n/a` where it should be 7 |
| **F2** | the sweep publishes **429 `.py` files swept**; the tree at the commit that ships that transcript holds **448**, and so did its parent — **19 files in the population and not in the number a reader is given**, inside the sweep whose whole argument is *the reported line is never the population* |
| **F3** | **1 of 6** — the exist/touched pair the brief asked for |
| **F4** | *"the negative control now mutates the file and re-cuts the sites from it"* is true of the 36-cell matrix and not of the **19 further probes in `negative_control`'s own body**, which still mutate site text in memory — the construction the repair itself names as unable to exhibit a site-boundary defect |
| **F5** | the sweep's **vocabulary** is a hand list of five row names where the gate prints six. Same rule, vocabulary derived from the code that prints the rows: **5 occurrences where the hand list finds 4** |

## What is confirmed and must not be disturbed by whatever comes next

- `B1` — **29 of 29** applicable cells of the product fire, at exit 1, every one.
- `B3` — the refusal covers the three `RECORD PARTITION` rows **individually**, against a control
  that blesses at the commit where the defect is present.
- `B6` — **37 909 of 37 909**, **462 of 37 909**, **847 of 847**. Any movement in these outranks
  every finding above.
