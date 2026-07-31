# mg-8d5e — predictions, committed BEFORE any script of this instrument exists

Written at `3fbf6f68`. Nothing in `code/repair_8d5e/` exists yet except this
file. Every row below is a claim made before the thing that measures it was
written, and every miss stays here with what was wrong beside it.

Two sites, from one audit (mg-2c77 on the mg-69d1 repair `d01ff32`). Neither
deferred.

| | site | what is wrong |
|---|---|---|
| **A-1** | mg-2c77 **OPEN 1** | `libe34a` derives `REPAIR_REV` as *the last commit that touched `g1_provenance.py`*; mg-69d1 edited a sentence in that file, so the anchor re-pointed and both sides of the pre-repair comparison are now mg-76cc's already-repaired predicate |
| **A-2** | mg-2c77 **OPEN 2** | `explicit boolean operand` denotes 39 operands in the census's two files; the table classifies the 17 that lie inside a deciding condition; the term is written without that qualifier at 15 sites in files `d01ff32` touched |

*(That row's wording was clarified after this file was committed — the phrase now carries the
unhyphenated words the scoring rule looks for. No predicted value was touched; `r4 (ii)` books the
edit as this deliverable's own instance of the defect it repairs.)*

---

## WHAT I HAD ALREADY OBSERVED BEFORE PREDICTING

Kept separate from the predictions, because a figure I have already read is
not a figure I predicted, and folding the two together is how a prediction
file comes to look better than it was.

| observed | value |
|---|---|
| `libe34a.REPAIR_REV` at `3fbf6f6`, by the file-history derivation | `d01ff32d` |
| `libe34a.PRE_REV` at `3fbf6f6` | `e5787e11` |
| `k1_prerepair.py` at `3fbf6f6` | exit 1, 3 findings, backwards 0 / 0 / 0 |
| `k4_cancel.py` at `3fbf6f6` | `in the COMMIT MESSAGE of d01ff32d : no`, `15 place(s) … 15 in all` |
| `code/branching_audit_e34a/out_k4_cancel.txt`, as committed | `in the COMMIT MESSAGE of 4755d029 : yes`, `4 place(s) … 5 in all` |
| the 15 unqualified in-`d01ff32` census sites reproduce at `adcfb1f` | yes, 15 of 15 |

The last two are the reason A-1 is predicted below to have a **second**
consequence mg-2c77 did not name.

---

## THE EXIT CODES

| script | predicted | measured |
|---|---|---|
| `selftest_8d5e.py` | 0 | **0** — HIT (35 assertions) |
| `r1_anchor.py` | 0 | **0** — HIT |
| `r2_kernel_half.py` | 0 | **0** — HIT |
| `r3_term.py` | 0 | **0** — HIT, *at the third attempt*: it went red twice on sites in this deliverable's **own** new prose (`README.md:8`, `docs/repair-mg-8d5e-…md:128`) that I had just written. Recorded because the instrument found them and I did not |
| `r4_self.py` | 0 | **0** — HIT, same history as `r3` |
| `run_all.sh` worst | 0 | **0** — HIT |

## THE RE-RUNS OF OTHER PEOPLE'S RUNNERS, AFTER THE REPAIR

| runner | predicted | measured |
|---|---|---|
| `code/branching_audit_e34a/selftest_e34a.py` | 0 | **0** — HIT (54 → 66 assertions) |
| `code/branching_audit_e34a/k1_prerepair.py` | exit **1**, findings **1** | exit 1, findings 1 — HIT |
| `code/branching_audit_e34a/k4_cancel.py` | exit **1** (mg-e34a predicted 1) | exit 1 — HIT |
| `code/branching_audit_e34a/run_all.sh` worst | 1 | **1** — HIT |
| `code/repair_69d1/selftest_69d1.py` | 0 | **0** — HIT (40 assertions, unchanged) |
| `code/repair_69d1/p1_bound.py` | 0 | **0** — HIT |
| `code/repair_69d1/run_all.sh` worst | 0 | **1** — ***MISS***. `p3_reason.py` self-errors: its control runs the discriminator **against `HEAD`** and requires ≥1 live assertion of the inverted sentence there, and mg-69d1's own repair landing removed the last one. `r1 (vi)` runs `p3` at `3fbf6f6` and it is **already red there**, so this repair did not cause it. It is the same shape as A-1 in a script mg-2c77 did not name, and it is **not repaired here** — §6 of the document |

## A-1 — THE ANCHOR

| # | claim | predicted | measured |
|---|---|---|---|
| A1.1 | the anchor re-derived from the **property** — the first commit at which `g1_provenance.py` carries `kernel_source=`, the two-source signature that IS the restored kernel half — returns mg-76cc's repair | `4755d029` | `4755d029` — HIT |
| A1.2 | its first parent, the pre-repair predicate | `3bc2cf76` | `3bc2cf76` — HIT |
| A1.3 | that parent's `g1_provenance.py` and `lib58da.py` are byte-identical to `lib76cc.REV_957F` = `e006581c`, so k1's own e006581c gate goes green again | yes | yes — HIT; the 2 findings k1 booked about it are gone |
| A1.4 | the same defect is present in a **second** anchor nobody named: `PRE_7E58_REV`, derived as the parent of the *second*-newest commit touching the file, has also re-pointed one repair forward | yes — it reads `3bc2cf76`, which is mg-**76cc**'s parent, under the label *before mg-7e58* | yes — HIT, exactly as written |
| A1.5 | property-anchored `PRE_7E58_REV`, from the first commit carrying `def measurement(` | `52aeaf43` | `52aeaf43` — HIT |
| A1.6 | the drift has a **second consequence in a second script**: `k4_cancel.py` scans `REPAIR_REV`'s commit message for the inverted sentence, and at `3fbf6f6` it scans mg-69d1's message instead of mg-76cc's — so a copy of the sentence under test silently left the count | yes; after the repair k4 prints `4755d029 : yes` again | yes — HIT. `k4` printed `d01ff32d : no`, `15 place(s) … 15 in all`; it now prints `4755d029 : yes`, `15 … 16 in all`, and its committed transcript recorded `4755d029 : yes` |
| A1.7 | after the repair, k1's three coverage numbers | 0 / 0 / 0 | 0 / 0 / 0 — HIT, and now about `3bc2cf76`↔`d01ff32` |
| A1.8 | after the repair, the two findings k1 books at `3fbf6f6` that are **not** in its committed transcript are gone, and the one that **is** in it remains | 2 gone, 1 remains | 2 gone, 1 remains — HIT |
| A1.9 | a **synthetic drift** — a commit that touches `g1_provenance.py` and does not move the property — moves the file-history anchor and does **not** move the property anchor | yes | yes — HIT. `r1 (ii)`: the file-history derivation moves from `d01ff32d` onto the constructed commit (whose sha differs every run, so it is not quoted here), and the property anchor reads `4755d029` on both sides. Both outcomes are gated |
| A1.10 | a **synthetic break** — the pinned pair made to disagree with the derived pair — fails **loudly**: the assertion books an error rather than the run quietly adopting a different pair | yes | yes — HIT, three ways: a wrong pin, an unfindable marker and a non-monotone marker, each red in mg-e34a's **own** selftest |
| A1.11 | the property marker is monotone over the file's history: once present, present in every later commit touching it (a marker that came and went would make *first introducing* the wrong anchor) | yes, for both markers | yes — HIT for both markers |

## A-2 — THE TERM

| # | claim | predicted | measured |
|---|---|---|---|
| A2.1 | the two populations, re-walked here: every operand of every `and`/`or` anywhere in `face_complex.py` + `posets.py`, and those inside a deciding condition | 39 and 17 | 39 and 17 — HIT (35+4 and 15+2) |
| A2.2 | the repair **fixes the term, not the walk** — so both numbers are unchanged after it | still 39 and 17 | still 39 and 17 — HIT |
| A2.3 | my scoring rule, run at `adcfb1f` where mg-2c77's transcript was committed, reproduces its 15 in-`d01ff32` unqualified sites | 15 of 15, same paths and lines | 15 of 15, same paths and lines — HIT (0 only mine, 0 only its) |
| A2.4 | the same rule at `adcfb1f` returns a *total* that differs from the transcript's 54/34, because `adcfb1f` also committed the audit's own write-up | 57 sites, 35 unqualified | 57 sites, 35 unqualified — HIT |
| A2.5 | after the repair, unqualified sites **in files `d01ff32` touched** | 0 | **0** — HIT |
| A2.6 | unqualified sites remaining anywhere in the tree | 19 | **20** — ***MISS by one***. I counted mg-2c77's own record at 8 from its `out_q3_operands.txt` table; it is 9, because that transcript's **own finding text** is a site the table does not list itself as. 9 + mg-eaef's 11 = 20 |
| A2.7 | every one of those 19 is a **record** — a transcript, a prediction file committed before its run, or an audit's statement of what it found — and none is a live claim about what the instrument covers | yes | yes — HIT; `r3 (iv)` gates that 0 unqualified sites fall outside a named record scope |
| A2.8 | unqualified sites **inside `code/repair_8d5e/`**, this deliverable's own files | 0 | **0** — HIT at the end, and see `r3_term.py` above: it was 3, then 1, then 0 |
| A2.9 | two of the 15 are transcripts. They are repaired by editing the **source that prints them** and re-running, never by hand | yes, and the re-run transcripts differ from the committed ones only in lines containing the term | ***MISS***, and for a wider reason than the one written below. `out_selftest_69d1.txt` differs in exactly one added line; `out_p1_bound.txt` differs in **26 lines**, because `p1 (ii)` now prints the wider population as a table *and* because `p1 (i)`'s own site census moved — my new files quote the narrow bound sentence, so its `7 copy/copies` became `9`, and every line number below an edit moved |
| A2.10 | two of the 15 are in `code/repair_69d1/PREDICTIONS.md`, a record committed before its own run. It gets an **addendum** with the original text left standing, not an edit | yes | yes — HIT, and the placement mattered: the addendum sits **in the table, between the two rows**, so the qualifier falls inside the 3-line window the scoring rule uses. At the foot of the file it would have left both rows scoring UNQUALIFIED |
| A2.11 | the `kern5f9a.py` edit is a comment and changes no behaviour: `d2_deletion.py`'s sweep numbers are unchanged | yes | yes — HIT; the parsed modules are identical |

## THE THING NO LIST NAMES

The prediction I most expect to miss, written out so the miss is legible:

> **A2.9's "differ only in lines containing the term" is the risky one.**
> `out_p1_bound.txt` also carries a findings-population sentence that is
> rebuilt from the source string, and `out_selftest_69d1.txt` carries a
> section heading. If either script prints anything derived from a line I
> edit — a length, an offset, a wrapped column — the diff will be wider than
> the term and this row misses.

And the structural one:

> **A-1 is fixed by pinning as well as deriving, and a pin is what mg-e34a
> deliberately refused.** Its rationale — *a literal cannot notice that the
> file moved* — is correct and is not withdrawn here. What is added is that a
> derivation cannot notice that it has started measuring something else. The
> repair keeps both and **compares them**, so neither failure is silent; the
> derivation that re-pointed stays in the output as a printed row, because the
> quantity that moved is evidence and deleting it would be the third version
> of the same mistake.

---

## THE SCORE

**35 rows.** 31 HIT, **4 MISSES**, kept above with what was wrong beside each:

| miss | what was wrong |
|---|---|
| `code/repair_69d1/run_all.sh` worst = 0 | it is 1, and has been since mg-69d1's own repair landed. `p3_reason.py`'s control is anchored on `HEAD` — the same shape as A-1, in a script mg-2c77 did not name. Measured at the base revision by `r1 (vi)`; **not repaired**, and §5 of the document says so |
| A2.6, 19 sites remaining | 20. I read mg-2c77's residue off its own table and the table does not list its own finding text as a site |
| A2.9, transcripts differ only in the term's lines | `out_p1_bound.txt` moved 26 lines. The reason I wrote down was right and incomplete: I predicted the *printed* figures might move and did not predict that **my own new files would join `p1`'s site census**, taking its narrow-sentence count from 7 to 9 |
| — the fourth is not a numbered row — | `r3` and `r4` were **red twice on this deliverable's own prose** before they were green. Both times the site was in something I had written *after* declaring the term repaired. The prediction that this deliverable would carry 0 unqualified sites (A2.8) is a HIT only because the instrument disagreed with me twice first |

The last one is the one worth carrying. **A repair for a term that means two things is written in prose,
and prose is where the term goes wrong.** The check that caught it is the same check applied to the
subject — which is the only reason it caught anything.

---

## ONE THING NO ROW ABOVE PREDICTED

**mg-2c77's own `q4_prerepair.py` still fires against the repaired tree, and it is wrong now.**

Its gate is `PRE_REV == lib76cc.REV_957F` — **revision** identity — where the property is **file**
identity. `e006581c` and `3bc2cf76` are different commits at which `g1_provenance.py` and
`lib58da.py` are byte-identical, which is what mg-e34a's design says and what `k1 (i)` checks and
passes. `q4`'s own message now reads *moved from `4755d029` (mg-76cc's repair) to `4755d029`
(mg-69d1's own)* — **a gate whose message says a value moved from a revision to itself.**

`r2 (v)` runs it, prints both comparisons, and gates the file one. mg-2c77's record is not edited.

I did not predict this because I predicted the repair and not the auditor's reaction to it. That is
the lesson the same shape keeps teaching: **the artifact you did not think to re-run is the one
still measuring the old thing.**
