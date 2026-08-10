# `mg-d19f` — the `mg-51f4` / `mg-28ff` contradiction: adjudicated, then repaired

Two landed canonical documents contradicted each other at `HEAD`.

* `docs/OneThird-SweepLoss-mg-51f4.md:148` — *"`mg-28ff`'s `n = 7` figures are deterministic
  samples of 40–200 posets, **correctly labelled as such at every appearance** in its
  document"*
* `docs/OneThird-L2-Conditionality-mg-28ff.md:21` — *"§4.3 summary … read a **sample** as an
  enumeration, and is **FALSE OF THE TRUTH**"*

They cannot both be true. `mg-64cb`'s concurrency sweep found it (`REPORT.md` §3.2) and
deliberately did not edit another ticket's landed document. This ticket edits it.

## What is here

| arm | what it does |
|---|---|
| `r0_selftest.py` | six forced arms (plus one informational), three of which must REFUSE |
| `r1_adjudicate.py` | **which claim is true**, decided against `mg-28ff`'s text as `mg-51f4` read it and against the underlying measurement — never against a timestamp |
| `r2_literals.py` | **the other eleven** shared literals `mg-64cb`'s screen flagged and nobody had read |
| `r3_selfcheck.py` | the repair checked against the defect class it repairs |

`run_all.sh`, exit 0 across four arms. Every number below is readable in the committed
`out_r*.txt`.

## The three answers

**1. `mg-28ff:21` is TRUE. `mg-51f4` is FALSE, at THREE sites, not the one filed.**

The adjudication is over `mg-28ff` at `cb496e9` — its only revision before `mg-51f4` landed,
so not a choice — and over `code/sweep_loss_51f4/out_s3_n7.txt`, read from the transcript
rather than from either document's prose. All three of `mg-29fe`'s joints CONFIRM against
that text by machine. And the sharpest fact in the exchange: **`mg-51f4` supplied the very
measurement (168 of 86278) that makes `mg-28ff:21` true**, while certifying as correct the
sentence that measurement refutes.

`r0`'s **A2** is why this is not decided by recency: that rule returns `mg-51f4` at the
landing instant and `mg-28ff` at `HEAD`, because `mg-28ff` was amended twice afterwards. One
rule, two answers. It is run so its refusal is demonstrated rather than asserted.

**The two extra sites.** §11's *"None of these is a labelling failure"* sits **three lines
above its own site 1**, whose "why" column describes exactly a labelling failure — the same
joint `mg-29fe` found, discovered independently by `mg-51f4` and then denied by the blanket
sentence above the table. §12's *"not quoted anywhere … the one place I mention one"* was
false the day the document landed: §11's table quotes all three `n = 7` sample values.
**All three sites are one defect** — a blanket about labelling asserted over a population
the author had not enumerated — and only the first needed a concurrent audit to expose it.

**2. The residue of `mg-64cb`'s literal screen is FIVE, not eleven, and it carries nothing.**

`lib64cb` indexes a commit under every work-item id it *mentions*, which is right for "which
items does this commit concern" and wrong for "which item wrote it". `mg-51f4`'s `canonical`
list is therefore three commits and only one is `mg-51f4`'s landing:

```
a65860e  mg-c50b   2026-08-10T01:39:01+01:00   a LATER ticket that cites mg-51f4
2f76a01  mg-51f4   2026-08-09T22:46:06+01:00   the landing
18a1347  mg-29fe   2026-08-09T22:40:32+01:00   THE AUDIT'S OWN COMMIT
```

So for three of the twelve literals the screen intersected the audit **with itself**. Of the
twelve: **5** are `mg-51f4`'s (`0.250000, 0.306250, 0.308339, 0.327508, 0.550747` — all
`n ≤ 6` cells of its own exhaustive table, recomputed on an instrument sharing no source line
with `lib28ff`, and `mg-29fe` withdrew no figure for them to supersede), **4** are
`mg-c50b`'s, **3** are `mg-29fe`'s own. Residue after this arm: **0**.

This is a property of the SCREEN and not a defect of `mg-64cb`'s report, which says in its own
§3.3 that a shared literal is a necessary condition and not a finding.

**3. What neither the screen nor this arm could ever have found: the labelling claim itself.**
It carries no numeric literal. Stated because it is the honest limit of both instruments.

## Defects of my own, kept

**D1 — a committed-state probe answering a working-tree question.** `r3`'s C4 first read
`git diff --name-only main...HEAD` and reported NOTHING CHANGED with an edited working tree
underneath it. It would have been green at every moment before the commit — which is exactly
when the arm is worth running.

**D1b — and the fix reached for a ref by its NAME.** `main` in a polecat worktree is a local
ref nobody updates; it sat one commit *ahead* of this branch's base, so C4 then reported
twelve files of `mg-724a`'s as changed by this ticket. That is `mg-f8e5`'s `c1_rebase.py:48`
and `mg-223d`'s pinned refs in a third costume. The baseline is now the computed branch point
and the arm REFUSES if it does not resolve.

**D2 — MY REPAIR CREATED A FALSE SENTENCE, AND MY OWN ARM CAUGHT IT.** Quoting `0.832530`
(`mg-28ff`'s `f*(7)` sample) as joint 1's evidence falsified §12's *"`mg-28ff`'s `n = 7`
sample figures are not quoted anywhere"*. C5's `added` list is what surfaced it. Reading that
bullet out then showed it was **already false at `2f76a01`** — §11's table quotes all three —
so the repair did not create the defect, it made a standing one one appearance worse and
forced it to be read. §12 is struck and corrected with all five appearances named. **This is
the repair exhibiting the defect class it repairs, inside the same edit.**

**D2b — and the correction of D2 contradicted the repair three sentences up.** §4's sentence
continues *"and I do not quote any of them"* — the same blanket as §12's, in the same
paragraph the repair had just corrected. So the first draft of this repair left the document
saying, four lines apart, that the figures are not quoted and that all three are. It is
struck too, and corrected to *"I do not USE any of them"*, which is the true form and the one
`mg-29fe` certifies.

**D3 — the joint-3 probe first printed per FILE.** `b1_footrule.py` draws
`sample_posets(7, 90)` at `:34` and `sample_posets(7, 200)` at `:73`, so a per-file summary
read as one script contradicting itself rather than as two arms of one document. Reported
per call site, with the three rows `mg-3bb9`'s repair-E table cites marked.

**D4 — an exact-count probe over a document that gained a section quoting itself.** `r0`'s A5
asserted each false sentence appears exactly once, and went RED the moment the repair landed:
§0.0's table quotes both, so each is findable twice. Not a site vanishing — a probe unable to
tell the defect from the record of its repair. That is `mg-64cb`'s D1 in a smaller costume,
where a survival classifier scored six superseded figures LIVE and every one was a quotation
inside the document correcting it. A5 now asks whether each site is findable, which is the
question it meant.

## What this ticket did NOT do

* **It did not touch `mg-28ff`.** `r3`'s C4 measures it: exactly one document outside this
  directory changed.
* **It did not harmonise.** The true claim is left alone; the false ones are struck.
* **It did not re-open either document's mathematics.** `mg-29fe`'s verdict already records
  that `mg-51f4`'s handling of `mg-28ff`'s `n = 7` figures is *"carried and not used, which
  is the correct handling"*, and this ticket's own read agrees.
* **It moved NO figure.** `r3`'s C5: 0 measured literals dropped, as a multiset against the
  branch point. Added literals are quoted evidence.
* **It did not audit `mg-51f4`'s seven proposed repair sites.** Two are checked and dated —
  site 1 landed, site 6 has not — and the other five are explicitly left unadjudicated,
  because dating them all is an audit of `mg-28ff` that nobody asked for.

## Provenance

Population: `docs/OneThird-SweepLoss-mg-51f4.md` and
`docs/OneThird-L2-Conditionality-mg-28ff.md` at `HEAD`, plus `mg-28ff` at `cb496e9`
(pinned in `libd19f.py`, and it is not a choice — it is the only revision that existed when
`mg-51f4` wrote its sentence). Evidence read and not recomputed:
`code/sweep_loss_51f4/out_s3_n7.txt`, `code/landing_audit_sweep_64cb/{REPORT.md,survival.json}`,
`code/l2_conditionality_28ff/{b1_footrule,b2_census,b5_trend}.py`.
