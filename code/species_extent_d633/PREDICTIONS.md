# PREDICTIONS — mg-d633

**Written before any probe was run, and not edited afterwards.** Wrong predictions are kept as
written and scored in `OUTCOMES.md`. mg-a4ef missed 4 of 60 and kept them; mg-7dd3 missed 6 of
72 and kept them. That is the bar.

The exit-code convention across this arc: **0 = the checker is silent, 1 = the checker fires.**
G4 in mg-7dd3's own record is the reminder that this is a convention and not a law — a checker
can report a finding and still exit 0, and three in this repository did until they were fixed.
So every prediction below is a prediction about the **exit code**, and `E3` also records
whether the finding text appeared, because those are two different claims.

---

## The rule being tested, per checker

For each checker: **a mutation planted INSIDE its printed extent must make it FIRE, and a
mutation planted OUTSIDE its printed extent must leave it SILENT.** An extent that names a
region the checker does not truly reach is the BROKEN finding of mg-7dd3, and only a mutation
inside the claimed region exposes it. An extent narrower than reality is a lesser fault and
still a false statement, and only a mutation outside it exposes that.

---

## `check_doc.py` — extent: this document, plus the repair document for C4's five assertions

| probe | mutation | in / out | predicted |
|---|---|---|---|
| **P1** | un-strike X7 in the document — remove the `~~` around §4's AM §17.5 sentence | IN | **1** |
| **P2** | delete *"WHAT THIS REPAIR DID NOT DO"* from the repair document | IN (2nd file) | **1** |
| **P3** | plant X7, live, in `docs/OneThird-Species-Hopf-Monoids-Repair-Remainder.md` | OUT | **0** |
| **P4** | plant X3, live, in `code/species_7d75/t6_fock_and_record.py` | OUT | **0** |

P2 is the probe that exists because the extent line used to say *"ONE FILE … it reads no
code"*. If P2 fired while the old line was in force, the old line was false — it was, and that
is C1.

## `w3_scope.py` — extent: X4, X5 and the character-ring rule over `code/species_7d75`, every regular file

| probe | mutation | in / out | predicted |
|---|---|---|---|
| **P5** | plant X4 in `code/species_7d75/run_all.sh` | IN | **1** |
| **P6** | plant X4 in `code/species_7d75/README.md` | IN | **1** |
| **P7** | plant X4 in `code/species_repair_6f61/README.md` | OUT | **0** |
| **P8** | plant X3 in `code/species_7d75/README.md` — a statement not on this list | OUT | **0** |

**P5 is the one that matters.** Before mg-d633 this file filtered on `.py/.txt/.md`, so
`run_all.sh` was in the tree, inside the extent's *"over ONE tree"*, and not read. I predict 1
**because the code was widened**; against the parent commit it would be 0.

## `s1_extent.py` — extent: 11 statements over the document + 4 trees, every regular file less 5 named

| probe | mutation | in / out | predicted |
|---|---|---|---|
| **P9** | plant X3 in `code/species_7d75/run_all.sh` | IN | **1** |
| **P10** | plant X3 in a new `.md` in `code/species_7d75` | IN | **1** |
| **P11** | plant X3 in `code/species_repair_a4ef/run_all.sh` | IN | **1** |
| **P12** | plant X3 in `code/species_audit_73df/README.md` — a tree the extent declares silent | OUT | **0** |
| **P13** | plant X3 in `code/species_repair_a4ef/OUTCOMES.md` — a NAMED exclusion | OUT | **0** |

**P9 is mg-7dd3's M12, which exited 0 and is the whole of finding A1.** P10 is its M13 control,
which exited 1 then and must still. P13 is the named exclusion doing its job: the extent says
those five files are skipped, so silence there is the extent being true, not a hole.

## `s2_seam.py` — extent: passages of the document over 60 normalised characters

| probe | mutation | in / out | predicted |
|---|---|---|---|
| **P14** | duplicate a **short** block quote (~139 chars) exactly, elsewhere in the document | IN | **1** |
| **P15** | duplicate a **long** block quote (>300 chars) exactly | IN | **1** |
| **P16** | duplicate a prose passage of 60 characters or fewer | OUT | **0** |
| **P17** | duplicate a Markdown **table row** | OUT | **0** |

**P14 is mg-7dd3's M16, which exited 0 while the run reported *"worst pair 5 %"*, and is the
whole of finding A2.** P16 and P17 are the extent's declared silences: both must stay 0, and
both are now printed by the run rather than left to a threshold nobody wrote down.

## `e2_crosssection.py` (new) — extent: every `*.md` under `docs/` and under `code/`

| probe | mutation | in / out | predicted |
|---|---|---|---|
| **P18** | restore §0's misquotation — the state of the file from `83ac472` to mg-d633 | IN | **1** |
| **P19** | restate a struck claim, un-struck, in a **different** `docs/*.md` that carries a strike | IN | **1** |
| **P20** | the same restatement, in a paragraph that says the claim is struck | OUT | **0** |
| **P21** | restate a struck claim in a `.py` in a code tree | OUT | **0** |

P18 is B1 itself and is also E2's own control (a); it is repeated here so that the same probe
harness measures all five checkers rather than each grading its own homework.

---

## Predictions I am least sure of, named in advance

1. **P5.** `w3_scope.py` exonerates a hit within 4 lines of `mg-f8fa`, *"used to"* or *"no
   longer"*. `code/species_7d75/run_all.sh` contains `mg-7d75` in its second line and none of
   those three, so I expect no accidental exoneration — but the whole class of defect in this
   arc is a marker disarming a checker by accident, twice recorded, so this is the probe I
   would bet against myself on.
2. **P16.** The duplicate must land in its **own** passage. If it lands adjacent to other prose
   the two merge into one block over 60 characters and the probe measures something else. The
   harness inserts it between blank lines for that reason, and if the prediction is wrong this
   is the first thing to check.
3. **P17.** I believe Markdown tables are in no passage at all — the prose predicate excludes
   lines starting with `|` and the block-quote predicate wants `>`. If a table row somehow
   joins a prose block, this returns 1 and the extent sentence *"tables and headings are swept
   by neither pass"* is wrong.
4. **P19.** Needs a second document carrying a strike whose claim can be restated with no
   negation word anywhere in the surrounding paragraph. If the harness's inserted paragraph
   trips `NEGATES` by accident, the probe returns 0 and it is the probe that is wrong, not the
   checker.

## Predicted totals

**21 probes: 11 predicted to fire, 10 predicted to stay silent.** I predict **0 misses**, which
is the prediction most likely to be wrong — the two previous workers predicted the same and
missed 4 and 6.
