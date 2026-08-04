# PREDICTIONS — mg-b2af, the repair of mg-330a's population and its two OPENs

Committed **BEFORE any script of this instrument exists**. Written at
`451a128` (HEAD of `polecat-b2af` at the time of writing), against `fba5f63`
— *"docs+audit: independent audit of the mg-8d5e anchor-and-term repair…"* —
and the brief in `mg-b2af`.

Every row below is what I expect **before** the run. **Misses are kept as
written**, with what was wrong recorded beside them in `README.md` and in the
transcripts. Nothing here is edited after a run; corrections go in an
**ADDENDUM** block at the bottom of the row's section.

---

## THE DISCLOSURE, MADE BEFORE ANYTHING ELSE — AND IT IS NOT A SMALL ONE

**I ran mg-330a's own sweep at HEAD before writing this file.** Not one of my
scripts — `code/audit_330a/lib330a.py`'s `sweep_anchor_calls()` and
`sweep_helper_uses()`, imported and called from a throwaway snippet, while
still reading the brief. So **P-1 below is not a prediction. It is a
measurement already taken, written down in the prediction file, and labelled
as such.**

I could have omitted the numbers and pretended. mg-330a booked the same shape
of thing about `k1_prerepair.py` and wrote *"pretending otherwise would be the
exact failure this arc exists to catch"*. It is booked here for the same
reason, and it is worse than mg-330a's: theirs was a foreign script whose
transcript they had not read, mine is the exact figure my first section is
about.

**Everything from P-2 down was written with no measurement behind it**, and
those are the rows this file should be scored on.

---

## P-1 (NOT A PREDICTION — A MEASUREMENT ALREADY TAKEN)

The brief opens with *"the anchor population is SIXTEEN history-derived across
13 directories (of 36 sites) … plus 16 call sites with no `--format=%H`"*.
mg-330a's committed transcript, `code/audit_330a/out_s1_anchors.txt`, says at
the same six places:

| figure | the brief / `docs/audit-mg-330a-*.md` | `out_s1_anchors.txt` | measured by me at `451a128` |
|---|---|---|---|
| all revision-producing call sites | **36** | **37** | **40** |
| history-derived | **16** | **16** | **19** |
| directories | **13** | **12** | **13** |
| `OLDEST` | **10** | **11** | **11** |
| `PICKAXE` | 6 | 6 | 6 |
| `RANGE` | 4 | 4 | 4 |
| helper call sites | **16** | **12** (+4 `DEF`) | **12** (+4 `DEF`) |

The doc and the transcript **landed in the same commit, `fba5f63`**, and
disagree in four of seven rows. So the disagreement is not "measured at
different commits" — that would be `mg-132a`'s `DISPLACED`, and it is the
first thing I will test rather than assume.

**What I have NOT measured and will not assume:** whether either published set
reproduces at the commit it was published at. That is P-2.

---

## P-2 — DO THE PUBLISHED FIGURES REPRODUCE AT THEIR OWN COMMITS?

Sweep re-run in clones at `ea97d0a` (where the transcript was written) and at
`fba5f63` (where both the transcript and the doc landed).

| row | prediction |
|---|---|
| **P-2a** | the transcript's `37 / 16 / 12 / 11 / 6 / 4` reproduces **exactly** at `ea97d0a` |
| **P-2b** | it reproduces at `fba5f63` **too** — I expect no revision-anchor call site to have been added between the two commits |
| **P-2c** | the doc's `36 / 16 / 13 / 10` reproduces at **neither**. I expect at least the `OLDEST 10` and the `16 helper call sites` to be **unreproducible at any commit**, because `16` is the transcript's count of `DEF` + `CALL` rows reported as a count of `CALL` sites — one number over two populations, which is F-2's shape one more time |
| **P-2d** | the `13 directories` in the doc **does** reproduce somewhere: it is the count over history-derived rows **alone**, where the transcript's `12` is the count over history-derived rows **union** helper call sites. Two populations again, and this one favours neither side |

If P-2c is wrong and every doc figure reproduces at some commit, then mg-330a's
prose is `DISPLACED` and not wrong, and I will say so in exactly those words.

## P-3 — THE CLASSIFIER DOES NOT DISTINGUISH FROZEN FROM MOVING

`classify_call` reads the flags. It does **not** look at whether the call
carries a **constant revision argument**: `log -1 --format=%H -- <path>` moves
on any later edit, and `log -1 --format=%H e5787e1 -- <path>` cannot, because
the revision is pinned. Both are classified `NEWEST`.

| row | prediction |
|---|---|
| **P-3a** | of the 19 history-derived sites, **2 to 4** carry a constant revision argument and are frozen |
| **P-3b** | of the 19, **8 to 12** take their path from a **parameter**, so the site is a facility and the anchor is at the *call site* — the same lesson as F-1, one level down |
| **P-3c** | **fewer than 6** are sites where a literal path and no pinned revision meet: an actual, moving, file-anchored derivation |
| **P-3d** | the refinement is **demonstrated by construction**, never asserted: a cosmetic commit in a clone, and each reconstructible site's answer re-resolved before and after. Every site I call frozen returns the **same** revision across that commit; every site I call moving returns a **different** one. I predict **0** sites contradict their label |

**The denominator does not shrink.** Whatever P-3 finds, the population stays
**19 by mg-330a's own classifier**, and the refinement is reported as a
sub-classification with both numbers printed. A repair that makes a defect
population smaller by re-reading it is the failure this arc exists to catch,
and it is the mirror image of the `OLDEST` inflation mg-330a warned about.

## P-4 — CONVERTED-COUNT, REPORTED AGAINST THE FULL POPULATION

The brief: *convert the history-derived 16 to property-derived, or
pin-and-compare each, and report converted-count against 16*.

| row | prediction |
|---|---|
| **P-4a** | **converted to property-derived: 0.** Every one of the 19 lives in another ticket's directory, and 13 of those directories carry committed transcripts that a signature change would invalidate. I expect to pin-and-compare instead, and to say `0 converted` in those words rather than let a treatment count stand in for it |
| **P-4b** | **pinned-and-compared: every site that resolves to a revision at all** — I predict **6 to 10** of the 19. A parameterised helper has no revision to pin; what gets pinned there is its call sites |
| **P-4c** | the pin-and-compare is **one file**, `ANCHORS.tsv`, re-resolved and compared by `t1`. Drift anywhere in those 13 directories becomes loud **in one place**, which is the only version of this that a 14th directory does not silently escape |
| **P-4d** | `OLDEST` is **not** absorbed. `t1` gates on the treatment population containing **0** `OLDEST` rows |

## P-5 — OPEN 1 (F-1): THE GATE AT THE POINT OF SPEND

| row | prediction |
|---|---|
| **P-5a** | before the edit, at HEAD: **2 of 4** consumers gate — `k1_prerepair.py` and `selftest_e34a.py` yes, `k2_five.py` and `k4_cancel.py` no. Scored by walking the source, not by reading mg-330a's table |
| **P-5b** | after: **4 of 4** |
| **P-5c** | drift constructed in a clone (the pin edited to a revision that exists), `k4_cancel.py` re-run there: **before** the edit it exits with its usual count and says nothing about the anchor; **after**, it books an additional finding naming the anchor it spends. The difference is the whole of F-1 and it is measured, not argued |
| **P-5d** | `k4_cancel.py` at HEAD, unperturbed: **exit 1**, `TOTAL BAD: 2`, both findings unchanged in text. `k2_five.py`: **exit 0**, `TOTAL BAD: 0`. The gate must be silent when there is no drift or it is not a gate, it is a banner |
| **P-5e** | the rule is made **structural**: an AST check that every script in `code/branching_audit_e34a/` naming an anchor either gates on the whole of `ANCHOR_DRIFT` or calls `gate_spent` for each anchor it names. I predict this check goes **green after the edit and red before it** — and I will run it both ways |
| **P-5f** | `k1_prerepair.py` and `selftest_e34a.py` are **not touched**. Their gate is a superset of the one I am adding, and rewriting them would move two transcripts for no property gained — one of which takes ten minutes to regenerate |

## P-6 — OPEN 2 (F-2): KIND AND SCOPE ARE TWO LABELS

| row | prediction |
|---|---|
| **P-6a** | the residue re-derived at HEAD, excluding this ticket's own files: **exactly 20**, same as mg-330a found |
| **P-6b** | by `r3 (iii)`'s **path** rule: **5** transcripts-and-records, **15** live claims |
| **P-6c** | including this ticket's own files the count is **higher** — this file contains the word under test in prose about the word under test. I predict **20 + between 2 and 8**, and I will print both numbers rather than pick the flattering one |
| **P-6d** | the corrected sentence is printed with **both** labels, and `t3` gates on the two labels being reported as two |

## P-7 — DO NOT DISTURB

| row | prediction |
|---|---|
| **P-7a** | all four anchors resolve to the pairs their prose names, **with each commit's subject printed beside its sha** |
| **P-7b** | `g1_provenance.py` at `d01ff32d` is **byte-identical** to `g1_provenance.py` at HEAD — re-derived here by blob sha, not read out of mg-330a's prose |
| **P-7c** | a distinctness check on **shas** passes on that pair and a distinctness check on **what they resolve to** fails. That is the sharpened lesson and I expect to be able to print both outcomes on the same pair |
| **P-7d** | `0/0/0` vs `1/1/3` is **READ** from mg-330a's committed transcript and labelled `READ`. It costs ten minutes of `k1_prerepair.py` to re-derive and mg-330a already re-derived it from scratch; a second re-derivation buys nothing this ticket needs. **Saying `READ` is the point** |
| **P-7e** | the refuse/report division survives: a cosmetic edit **reports**, a property-moving edit **refuses**. Constructed in a clone |

## P-8 — THE SCRIPTS AND THEIR EXIT CODES

Convention, taken from `code/branching_audit_e34a/run_all.sh` so the ruler is
theirs: every `t*.py` exits `0` iff `SELF-ERRORS == 0` **and**
`FINDINGS == 0`. Non-zero means *this script has something to report*.

| script | predicted exit | why |
|---|---|---|
| `selftest_b2af.py` | **0** | if it is not 0 nothing below can be read |
| `t1_population.py` | **1** | P-2c — I expect at least one published figure not to reproduce anywhere |
| `t2_gate.py` | **0** | it tests my own repair; if it is not 0 the repair is not done |
| `t3_term.py` | **1** | the corrected sentence is not in `dfa263c`'s commit message and I cannot edit a commit message. The finding stands and is named |
| `t4_preserve.py` | **0** | I expect to disturb nothing |

**Worst exit predicted: 1.**

## P-9 — FOREIGN SCRIPTS I INTEND TO RE-RUN

| script | predicted exit | why |
|---|---|---|
| `code/branching_audit_e34a/k4_cancel.py` | **1** | committed transcript ends `TOTAL BAD: 2`; my edit adds a gate that is silent when green |
| `code/branching_audit_e34a/k2_five.py` | **0** | committed transcript ends `TOTAL BAD: 0` |
| `code/branching_audit_e34a/selftest_e34a.py` | **0** | committed transcript ends `66 assertions, 0 failed` |
| `code/branching_audit_e34a/k1_prerepair.py` | **not run** | ten minutes, and nothing in this ticket rests on re-deriving what P-7d marks `READ` |

## THE ONE I AM LEAST SURE OF

**P-6a.** mg-330a measured 20 at `fba5f63` and I am predicting the same number
at `451a128`, four commits later, in a repo where the last three commits are
prose about censuses. If it comes back 21 or 24 the prediction is a miss and
the miss is the same defect one more time — a count carried forward as a
property. I am writing `20` because that is what I actually expect, not
because it is safe.
