# mg-330a — independent audit of the mg-8d5e anchor-and-term repair (`dfa263c`)

Pre-filed in the same action as its parent. Six scripts, 36 self-test
assertions, worst exit 1. `PREDICTIONS.md` committed in `71a1f55` **before any
script of this instrument existed**, with the misses kept as written and what
was wrong beside each.

The brief said: **do not check its logic; resolve every derived anchor and
look.** So nothing here reads a derivation and reasons about it. Every anchor
is run and its answer printed; every column of the kernel-half confirmation is
re-derived by installing the pinned predicate and running it; the cosmetic-edit
failure is **built**, at HEAD and again at a commit where the defect is still
present.

---

## THE VERDICT

**The two sites mg-2c77 left open are closed, and the closures hold under
construction rather than under argument.**

| what | measured | verdict |
|---|---|---|
| A cosmetic edit to `g1_provenance.py` at HEAD moves the anchor | **no** — `REPAIR_REV`, `PRE_REV`, `REV_7E58`, `PRE_7E58_REV` all unmoved | **holds** |
| the same edit at `e2577e5`, before the repair | **all three history anchors move, silently, selftest still exit 0** | the defect **reproduces** |
| the kernel-half confirmation is a DIFFERENCE | `3bc2cf76` → **0/0/0**, HEAD → **1/1/3**, re-derived from scratch | **holds** |
| the two columns are two predicates | `kernel_source=` **absent** at the old side, **present** at the new | **holds** |
| the drifted pair was one predicate twice | both columns **1/1/3** on the same bend | **vacuity measured** |
| the term: denoted / covered / neither | **39 / 17 / 22**, counted by an independent AST walk | **holds** |
| the qualifier at all 15 sites | **15 QUALIFIED, 0 unqualified** | **holds** |
| the ruler was not moved | a constructed `deciding-condition` site still scores **UNQUALIFIED** | **holds** |
| the four preserved items | all present, all at their published values | **holds** |

**Two findings**, neither of them a failure of the two repaired sites:

**F-1 — THE DRIFT GATE IS NOT WHERE THE ANCHOR IS USED.** `ANCHOR_DRIFT` is
built once at import of `libe34a` and gated in exactly **two** of the four
scripts that read an anchor. `k4_cancel.py` — **the script the repair itself
identifies as the one "where the count actually moved"** — reads `REPAIR_REV`
and does **not** carry the gate; neither does `k2_five.py`, which reads
`PRE_7E58_REV`. Run alone, either would print a number derived from a drifted
anchor with nothing to say so. The repair makes drift loud in `selftest_e34a.py`
and `k1 (i)`; it is silent in the two scripts whose numbers move.

**F-2 — `every one a record` IS TWO POPULATIONS UNDER ONE WORD.** `dfa263c`'s
summary says *"20 sites remain unqualified in the tree, every one a record"*.
Re-derived at HEAD the residue is **exactly 20** — this audit found no site the
repair did not name, and the sites are correctly declined. But `r3 (iii)`
derives a site's **kind** from its **path** (`out_*.txt` transcript,
`PREDICTIONS.md` record, **anything else a live claim**) and that rule is what
decides whether a site gets edited; `r3 (iv)` then labels the same residue by
**scope** — whose ticket owns the file — and the summary reports the scope label
as the kind label. Under the repair's own path rule, **15 of the 20 are live
claims**, not records. A reader who applies `r3 (iii)`'s rule to `r3 (iv)`'s
list gets 15 where the sentence says 0.

That is **A-2's own shape — one word over two populations — in the sentence
summarising the repair of a word over two populations.**

---

## THE SWEEP FOR A FOURTH — AND THE POPULATION, FINALLY ENUMERATED

The brief: *the population of history-derived anchors has still never been
enumerated.* It is now, **repo-wide**, by `ast` over every `.py` under `code/`
— 36 revision-producing `git log` call sites, classified by **how** the
revision is obtained, because that is what decides whether an unrelated edit
moves it:

| kind | sites | what it is |
|---|---|---|
| `NEWEST` — `log -1 --format=%H -- <path>` | **7** | HISTORY-DERIVED — the A-1 defect class |
| `INDEXED` — `log --format=%H -- <path>` then `[n]` | **8** | HISTORY-DERIVED — A-1's second half |
| `UNRESTRICTED` — no pathspec | **1** | HISTORY-DERIVED, on the branch |
| `OLDEST` — `log --reverse … -- <path>` then `[0]` | 10 | **stable** against later edits |
| `PICKAXE` — `log -S` / `log -G` | 6 | **PROPERTY-DERIVED** |
| `RANGE` — `log <a>..<b>` | 4 | a set, not an anchor |

Plus **16 call sites of the two named helpers** (`last_touching`,
`nth_touching`) which contain no `--format=%H` at all and which a flag-grep
would miss entirely.

**So: 16 history-derived call sites across 13 directories.** `OLDEST` is named
separately on purpose — a file's *creation* does not move when the file is
edited, and lumping it in would count a safe construct as the defect. That
inflation would be A-2's mistake committed inside an audit of A-2.

The two the repair named are two of the sixteen. **The repair's own
enumeration ("11 anchors") is scoped to `code/repair_8d5e/`** — which its
transcript states and which is not a defect — but it is not this population,
and the difference is printed rather than left to be inferred.

The repair's commit message also points at `code/repair_69d1/p3_reason.py (i-b)`
— an anchor on `HEAD`, vacuous since mg-69d1's own repair landed — and declines
to fix it. Confirmed: its committed transcript ends `TOTAL BAD: 1`.

---

## `LAST_TOUCHING_G1` — DEMONSTRATED, NOT READ

*"The quantity that moved is the evidence."* The claim is that removing it
would lose a **detector**, not a **dependency**. Checked by **deleting both
names in a clone and re-running**, rather than by reading the source:

- **2 scripts** read them (`k1_prerepair.py` prints, `selftest_e34a.py`
  asserts). **No anchor is derived from either.**
- Deleting them makes the consumers **raise** — exit 1, `AttributeError`.
- **2 selftest assertions** are stated in terms of them: that the property
  anchor and the history anchor still return *different* commits, and that the
  second history anchor had moved too.

So `used by no anchor` is **true**; `used by nothing` is **false**. What would
be lost is the `apart` column and both non-vacuity assertions — a detector —
and the failure mode of removing it is loud, which is the right failure mode
for evidence.

---

## THE CONFIRMATION IS A DIFFERENCE — AND THE VACUITY IS SHARPER THAN STATED

Re-derived in `s3`, with each pinned `g1` travelling with **its own
`lib58da`** (mg-76cc changed `run_c1`'s signature in the same commit, so a
pre-repair `g1` against the repaired library is a third thing that never
existed):

| column | revision | exit | self | find |
|---|---|---|---|---|
| **BEFORE THE REPAIR** (property) | `3bc2cf76` | **0** | **0** | **0** |
| **THIS REPAIR** | HEAD | **1** | **1** | **3** |
| before the repair (DRIFTED) | `e5787e11` | 1 | 1 | 3 |
| the repair (DRIFTED) | `d01ff32d` | 1 | 1 | 3 |

`k1_prerepair.py`, re-run unmodified, prints the same two triples in its own
kernel-bend row. Two independent derivations, one answer.

**And one step further than the parent states it.** The drifted `this repair`
column resolves to `d01ff32d`, and `g1_provenance.py` there is **byte-identical
to `g1_provenance.py` at HEAD**. So under the drifted anchor the column
labelled *"the repair"* was not merely the same *predicate* as the current one
— it was **the same file**. The parent's report says both sides became
"mg-76cc's ALREADY-REPAIRED predicate"; the byte identity is the sharper form
of that statement, and it is measured here rather than inferred.

This is also *why nothing complained*: the two drifted sources **differ** by
sha, so a file-identity check would have passed. It was not a comparison of a
file with itself; it was a comparison of a **predicate** with itself, and only
the first of those is visible to a sha.

---

## THE FAILURE, CONSTRUCTED

| probe | `REPAIR_REV` follows? |
|---|---|
| cosmetic edit at `e2577e5` (pre-repair) | **YES — silently**, selftest still exit 0 |
| cosmetic edit at HEAD (repaired) | **NO** |

The control matters: at `e2577e5` the cosmetic commit **becomes** *"mg-76cc's
repair"* and its parent becomes *"the pre-repair predicate"*, with no drift row
anywhere, because there is nothing for the derivation to disagree with — and
`selftest_e34a.py` **passes**. That is what "silently" means, measured.

**Refuses, or reports?** Both, correctly divided. A **cosmetic** edit at HEAD
does not make the instrument red — it **reports**: `LAST_TOUCHING_G1` moves,
is printed, and the `apart` distance grows. A **property-moving** edit
**refuses**. An instrument that refused to run on every comment could not be
run on a live tree at all; what the repair must not do is *follow*, and it does
not.

**And the three pieces fail in three different ways** — built here, not read
out of `r1 (iii)`:

| constructed failure | selftest exit | drift rows | which assertions go red |
|---|---|---|---|
| a wrong pin | 1 | 1 | 3 assertions, incl. the pin comparison |
| an unfindable marker | 1 | 1 | 1 assertion, the fallback message |
| a non-monotone marker | 1 | **0** | 1 assertion, the monotonicity check |

No two make the same assertions go red. In particular the non-monotone case
produces **zero** drift rows and is caught by a different mechanism entirely —
so no single commit silences more than one of the three.

---

## THE TERM

Counted here, not read: **39** operands denoted, **17** inside a deciding
condition, **22** in no column — `35/15/20` for `face_complex.py` and `4/2/2`
for `posets.py`. All 22 are **named** in `out_s4_term.txt (ii)`; a count of
what is uncovered that cannot be pointed at is the same silence as no count at
all.

The 15 sites: re-derived at mg-2c77's own revision `adcfb1f1` by mg-2c77's own
rule (**57** sites stating the term there, **15** unqualified and in files
`d01ff32` touched), then re-scored at HEAD — **15 QUALIFIED, 0 unqualified**,
one file gone. Scored **per file**, because a line number is an anchor into a
file's *text* and editing the file moves every site below it — scoring the old
line number in the new file would be A-1 in miniature.

**The ruler was not moved.** A constructed site carrying only
`deciding-condition` still scores **UNQUALIFIED**; the unhyphenated form scores
QUALIFIED. The rule returned **3 distinct labels** over the tree it scores, so
it is distinguishing and not vacuous.

---

## MY OWN CHOICE — THE FLOOR, NOT THE SCOPE

Named in `PREDICTIONS.md` before it was run: **the same rule, re-scoped to
HEAD.** The repair scores the term over *the files `d01ff32` touched*. That is
the right population for a finding stated at `d01ff32` — re-deriving it as *the
files the newest repair touched* would be A-1 — but it is a population that
stops growing while the tree does not. Six commits landed after `dfa263c`.

The re-scoped run is what produced **F-2**. It also puts **this audit's own
files in the population**: two of my own lines scored UNQUALIFIED on the first
run and were repaired, because a rule that exempts its author is not a rule.

---

## FIVE DEFECTS OF THIS INSTRUMENT, RECORDED RATHER THAN SMOOTHED AWAY

1. **`selftest (d)` expected 6 operands and the walk returned 8.** I listed
   four BoolOp *pairs* and wrote down the count of pairs. The selftest went red
   on my own arithmetic before any number rested on it. Expectation wrong, walk
   right.
2. **The anchor classifier tested for `-S` and not `-G`,** and filed a real
   `git log -G` site (`repair_8aae.py:499`) under `INDEXED` — the defect class.
   `-G` is the regex pickaxe and selects by a property of the content exactly
   as `-S` does. Calling it history-derived would have **inflated the defect
   population by one**, which is A-2's mistake made inside an audit of A-2.
   Found by reading the sweep's own named rows — which is why the rows are
   named.
3. **`s3`'s "each pinned source must differ from HEAD" guard was applied to
   every column,** and booked a SELF-ERROR against the drifted `the repair`
   column, whose whole point is that it *is* the current predicate. The
   instrument scored a fact as a fault. The fact turned out to be worth more
   than the guard: it is the byte-identity result above, now printed as
   evidence.
4. **`s5`'s conspiring-shape check printed `not found by this reader`** where a
   gate wanted a yes/no. A reader that answers "I don't know" and a reader that
   answers "no" are different things, and printing the first where a gate wants
   the second is how a check becomes decoration. Replaced with an `ast` read of
   the two constructions' actual bodies.
5. **`s5`'s edge probe asked only whether the substrings `11` and `12` occurred
   anywhere in q2's output.** q2 prints dozens of numbers and two of them are
   two digits — a gate whose red is unreachable. That is the same defect as a
   comparison of a predicate with itself, committed in the audit whose whole
   subject is that defect. Replaced with a per-row read matched by q2's own
   labels and scored against the column each row must fall in.

---

## PREDICTIONS — 20 rows, 16 HIT, 4 MISSES, kept as written

The full table is in `PREDICTIONS.md`, unedited. The misses:

| row | predicted | actual | what was wrong |
|---|---|---|---|
| **P-1d** | 2–4 history-derived sites outside `libe34a` | **15**, across 13 directories | I reasoned from the two the repair named and assumed the class was rare. It is not rare; it is the default way this repo asks "when did this file change". The prediction was an anchor on a sample of two. |
| **P-4c** | 0 unqualified live claims at HEAD | **15** | I predicted from the repair's summary sentence — *"every one a record"* — instead of from its kind rule. Predicting from the sentence rather than the rule is exactly the reading error F-2 is about. I made it before I found it. |
| **q3** | exit 0 | **exit 1**, 2 findings | The repair only ever claimed to close q3's **census** finding, and that one *is* gone. I assumed the other two went with it. A miss on my side, not a defect in the repair. |
| **s4** | exit 0 | **exit 1** | Follows from P-4c. |

### The foreign scripts, re-run unmodified

| script | predicted | actual | |
|---|---|---|---|
| `k1_prerepair.py` | 1 | **1** | HIT. Reproduces its committed transcript byte-for-byte except one per-run temp-clone hash. |
| `selftest_e34a.py` | 0 | **0** | HIT. |
| `q1_reason.py` | 0 | **0** | HIT. All four inputs present, all at their published verdicts. |
| `q2_bound_edge.py` | 0 | **0** | HIT. |
| `q3_operands.py` | 0 | **1** | **MISS** — see above. The census finding *is* gone; the two survivors are q3's other findings. |
| `q4_prerepair.py` | 1 | **1** | HIT — and it went from **2** findings to **1**. |

**q4 confirms the repair's own account of it.** The repair says q4 still fires
and that this is a defect in the *auditor*: q4's gate compares **revision**
identity where the property is **file** identity. The tell the repair predicted
is now literally printed in q4's own finding text —

> `REPAIR_REV moved from 4755d029 (mg-76cc's repair) to 4755d029 (mg-69d1's own)`

— a value reported as having moved from itself to itself. Measured and pointed
at; mg-2c77's record is not edited here, exactly as the repair declined to edit
it.

One disclosure, made in `PREDICTIONS.md` **before** any measurement:
`k1_prerepair.py` was **launched before the predictions file was written**,
because it takes ~10 minutes and I did not want it on the critical path. Its
transcript was not read at the time of writing, so the prediction (P-K1, exit
1 — **HIT**) is honest, but the ordering is not clean. Booked rather than
smoothed, because pretending otherwise would be the exact failure this arc
exists to catch.

---

## RUNNING IT

    sh code/audit_330a/run_all.sh

Roughly ten minutes; `s3` runs `k1_prerepair.py` and four `g1` runs of its own,
`s5` runs mg-2c77's `q1` and `q2`. Every mutation is a **commit in a clone**
under the system temp directory — `g1` reads `c1` and the kernel with
`git show`, and a working-tree edit reaches nothing at all. Nothing writes into
another ticket's directory. No `| tee` anywhere (mg-c2b3, mg-f922).
