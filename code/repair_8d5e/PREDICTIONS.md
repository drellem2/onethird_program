# mg-8d5e — predictions, committed BEFORE any script of this instrument exists

Written at `3fbf6f68`. Nothing in `code/repair_8d5e/` exists yet except this
file. Every row below is a claim made before the thing that measures it was
written, and every miss stays here with what was wrong beside it.

Two sites, from one audit (mg-2c77 on the mg-69d1 repair `d01ff32`). Neither
deferred.

| | site | what is wrong |
|---|---|---|
| **A-1** | mg-2c77 **OPEN 1** | `libe34a` derives `REPAIR_REV` as *the last commit that touched `g1_provenance.py`*; mg-69d1 edited a sentence in that file, so the anchor re-pointed and both sides of the pre-repair comparison are now mg-76cc's already-repaired predicate |
| **A-2** | mg-2c77 **OPEN 2** | `explicit boolean operand` denotes 39 operands in the census's two files; the table classifies 17; the term is written without the deciding-condition qualifier at 15 sites in files `d01ff32` touched |

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
| `selftest_8d5e.py` | 0 | |
| `r1_anchor.py` | 0 | |
| `r2_kernel_half.py` | 0 | |
| `r3_term.py` | 0 | |
| `r4_self.py` | 0 | |
| `run_all.sh` worst | 0 | |

## THE RE-RUNS OF OTHER PEOPLE'S RUNNERS, AFTER THE REPAIR

| runner | predicted | measured |
|---|---|---|
| `code/branching_audit_e34a/selftest_e34a.py` | 0 | |
| `code/branching_audit_e34a/k1_prerepair.py` | exit **1**, findings **1** | |
| `code/branching_audit_e34a/k4_cancel.py` | exit **1** (mg-e34a predicted 1) | |
| `code/branching_audit_e34a/run_all.sh` worst | 1 | |
| `code/repair_69d1/selftest_69d1.py` | 0 | |
| `code/repair_69d1/p1_bound.py` | 0 | |
| `code/repair_69d1/run_all.sh` worst | 0 | |

## A-1 — THE ANCHOR

| # | claim | predicted | measured |
|---|---|---|---|
| A1.1 | the anchor re-derived from the **property** — the first commit at which `g1_provenance.py` carries `kernel_source=`, the two-source signature that IS the restored kernel half — returns mg-76cc's repair | `4755d029` | |
| A1.2 | its first parent, the pre-repair predicate | `3bc2cf76` | |
| A1.3 | that parent's `g1_provenance.py` and `lib58da.py` are byte-identical to `lib76cc.REV_957F` = `e006581c`, so k1's own e006581c gate goes green again | yes | |
| A1.4 | the same defect is present in a **second** anchor nobody named: `PRE_7E58_REV`, derived as the parent of the *second*-newest commit touching the file, has also re-pointed one repair forward | yes — it reads `3bc2cf76`, which is mg-**76cc**'s parent, under the label *before mg-7e58* | |
| A1.5 | property-anchored `PRE_7E58_REV`, from the first commit carrying `def measurement(` | `52aeaf43` | |
| A1.6 | the drift has a **second consequence in a second script**: `k4_cancel.py` scans `REPAIR_REV`'s commit message for the inverted sentence, and at `3fbf6f6` it scans mg-69d1's message instead of mg-76cc's — so a copy of the sentence under test silently left the count | yes; after the repair k4 prints `4755d029 : yes` again | |
| A1.7 | after the repair, k1's three coverage numbers | 0 / 0 / 0 | |
| A1.8 | after the repair, the two findings k1 books at `3fbf6f6` that are **not** in its committed transcript are gone, and the one that **is** in it remains | 2 gone, 1 remains | |
| A1.9 | a **synthetic drift** — a commit that touches `g1_provenance.py` and does not move the property — moves the file-history anchor and does **not** move the property anchor | yes | |
| A1.10 | a **synthetic break** — the pinned pair made to disagree with the derived pair — fails **loudly**: the assertion books an error rather than the run quietly adopting a different pair | yes | |
| A1.11 | the property marker is monotone over the file's history: once present, present in every later commit touching it (a marker that came and went would make *first introducing* the wrong anchor) | yes, for both markers | |

## A-2 — THE TERM

| # | claim | predicted | measured |
|---|---|---|---|
| A2.1 | the two populations, re-walked here: every operand of every `and`/`or` anywhere in `face_complex.py` + `posets.py`, and those inside a deciding condition | 39 and 17 | |
| A2.2 | the repair **fixes the term, not the walk** — so both numbers are unchanged after it | still 39 and 17 | |
| A2.3 | my scoring rule, run at `adcfb1f` where mg-2c77's transcript was committed, reproduces its 15 in-`d01ff32` unqualified sites | 15 of 15, same paths and lines | |
| A2.4 | the same rule at `adcfb1f` returns a *total* that differs from the transcript's 54/34, because `adcfb1f` also committed the audit's own write-up | 57 sites, 35 unqualified | |
| A2.5 | after the repair, unqualified sites **in files `d01ff32` touched** | 0 | |
| A2.6 | unqualified sites remaining anywhere in the tree | 19 | |
| A2.7 | every one of those 19 is a **record** — a transcript, a prediction file committed before its run, or an audit's statement of what it found — and none is a live claim about what the instrument covers | yes | |
| A2.8 | unqualified sites **inside `code/repair_8d5e/`**, this deliverable's own files | 0 | |
| A2.9 | two of the 15 are transcripts. They are repaired by editing the **source that prints them** and re-running, never by hand | yes, and the re-run transcripts differ from the committed ones only in lines containing the term | |
| A2.10 | two of the 15 are in `code/repair_69d1/PREDICTIONS.md`, a record committed before its own run. It gets an **addendum** with the original text left standing, not an edit | yes |
| A2.11 | the `kern5f9a.py` edit is a comment and changes no behaviour: `d2_deletion.py`'s sweep numbers are unchanged | yes | |

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
