# PREDICTIONS — mg-0ba7, the INDEPENDENT AUDIT of the mg-b2af repair of mg-330a's anchor population

Committed **BEFORE any script of this instrument exists**. Written on
`polecat-y0ba7` at `b1c3467` — *"evidence: the committed transcripts of the
mg-b2af suite…"* — against the three commits mg-b2af landed (`06c9271`,
`14c6c3b`, `b1c3467`) and the brief in `mg-0ba7`.

**This audit was PRE-FILED IN THE SAME ACTION AS ITS PARENT.** `mg-0ba7` and
`mg-b2af` were created together by `pm-onethird`; the audit of the repair
existed as a ticket before the repair had a line of code. That is the standard
for this lineage and it is why this file can be scored at all: the questions
were fixed before the answers were available to anybody, including the parent.

Every row is what I expect **before** the run. **Misses are kept as written**,
with what was wrong recorded beside them in `README.md`. Nothing here is
edited after a run.

---

## THE DISCLOSURE, FIRST AND UNABRIDGED

Before writing this file I ran **mg-330a's own sweep** (`lib330a.py`'s
`sweep_anchor_calls`, `sweep_helper_uses`, `classify_call`) from a throwaway
snippet in a scratch directory, at this worktree's HEAD, and I ran two
throwaway AST snippets of my own. **The rows labelled M-n below are therefore
NOT predictions. They are measurements already taken, written down in the
prediction file and labelled as such.**

The parent booked the same disclosure for its P-1 and called it *"worse than
mg-330a's"*. Mine is worse again: I took **six** such readings, not one, and
two of them are the openings of my first two sections. I am not going to
launder them into predictions by omitting the numbers.

**P-n rows carry no measurement behind them.** Those are the rows this file
should be scored on.

---

## THE MEASUREMENTS ALREADY TAKEN (M-1 … M-6)

### M-1 — mg-330a's classifier, re-run by me at this worktree's HEAD

| figure | mg-330a doc | mg-330a transcript | mg-b2af at its tree | **me at `b1c3467`** |
|---|---|---|---|---|
| all revision-producing call sites | 36 | 37 | 40 | **44** |
| `NEWEST` | 7 | 7 | 8 | **9** |
| `INDEXED` | 8 | 8 | 10 | **12** |
| `UNRESTRICTED` | 1 | 1 | 1 | **1** |
| `OLDEST` | 10 | 11 | 11 | **12** |
| `PICKAXE` | 6 | 6 | 6 | **6** |
| `RANGE` | 4 | 4 | 4 | **4** |
| history-derived | 16 | 16 | 19 | **22** |
| directories (history-derived) | 13 | 12 | 13 | **14** |

**Population:** every `ast.Call` in every `.py` under `<repo>/code` at the
worktree. **Grain:** one row per *call site*, not per file and not per anchor.

### M-2 — the parent's helper sweep at the same tree

`sweep_helper_uses` returns **16 rows = 4 `DEF` + 12 `CALL`**. The parent's own
headline is that mg-330a's document reported *16 call sites* when 16 was the
**row** count over **two** populations. **At my tree the split is identical**,
which means the parent's finding survives a tree it was not measured at.

### M-3 — the seed set is not two names

Parsing every `.py` under `code/` and asking *which function definitions
directly contain a call that mg-330a's own classifier calls history-derived*
returns **11 distinct function names**:

`a3`, `base_before_dir`, `commits_touching`, `last_lacking`, `last_touching`,
`log_paths`, `main`, `my_last_touching`, `my_nth_touching`, `nth_touching`,
`publishing_commit`

**The parent's helper sweep knows two of these eleven** — `last_touching` and
`nth_touching`, hard-coded in `sweep_helper_uses`'s body.

### M-4 — `last_touching` is defined three times

`code/branching_audit_e34a/libe34a.py:130`,
`code/branching_repair_76cc/lib76cc.py:176`,
`code/repair_8d5e/lib8d5e.py:138`. A sweep that matches a **bare name** across
the repo cannot say which of the three a given call site reaches.

### M-5 — six directories outside `code/branching_audit_e34a/` import `libe34a`

`code/repair_69d1`, `code/repair_b2af`, `code/audit_2c77`, `code/repair_8d5e`,
`code/audit_330a`, and `libe34a`'s own directory. **`t2_gate.py`'s structural
rule walks `code/branching_audit_e34a/` and nothing else.**

### M-6 — `ANCHOR_OF` has four keys and `libe34a` derives more than four anchors

`LAST_TOUCHING_G1` (`libe34a.py:411`) and `NTH_TOUCHING_1` (`:428`) are
module-level revision anchors derived by `last_touching` / `nth_touching`, and
neither is a key of `ANCHOR_OF`.

---

## P-1 — MY OWN CLASSIFIER, WRITTEN FRESH, AGAINST mg-330a's

I will write a classifier from the taxonomy in mg-330a's docstring **without
importing `classify_call`**, and run both over the same 44 call sites.

**I predict agreement on 40 or more of the 44 rows, and at most 4
disagreements.** I expect the disagreements, if any, to be in `RANGE` (the
`".." in s` test in `classify_call` is written twice and the outer condition is
dead) and in the abbreviated-hash formats.

*If my classifier agrees on all 44, that is a weaker result than a
disagreement, and I will say so rather than present unanimity as
confirmation.*

## P-2 — THE POPULATION WITH NO `--format=%H`, RESOLVED BY IMPORT

The brief: *include the call sites carrying no `--format=%H`; the parent found
16 such, invisible to a flag-grep; **a search by flag has a population defined
by a flag***.

**A search by NAME has a population defined by a name-list**, and the parent's
list has two entries (M-3). I will derive the population instead: seed =
functions containing a history-derived call, closure = call sites of those
functions **resolved through the importing file's own bindings**, not by bare
name.

**I predict the import-resolved population of anchor-obtaining call sites that
carry no `--format=%H` is strictly greater than 12, and I predict it lands
between 25 and 45, over 8 or more directories.** (The naive bare-name closure
is 269 sites, which I have measured and which is an artefact of `main`; that
number is not the prediction.)

## P-3 — THE NAME-MATCH IS WRONG IN BOTH DIRECTIONS

**I predict the parent's 12 `CALL` rows contain at least one site whose bare
name resolves to a *different* definition than the row implies** (M-4 makes
three candidates available), **and that at least three whole helper names with
real call sites are missing from the population.**

## P-4 — `OLDEST` WAS NOT ABSORBED, AND THE GATE THAT SAYS SO CANNOT SAY IT

`t1_population.py:430` gates on `not [r for r in pinned if r["kind"] ==
"OLDEST"]`, where `pinned` is `ANCHORS.tsv` — a four-row file **this ticket
wrote**, drawn from a population `HISTORY_KINDS` excludes `OLDEST` from by
construction.

- **P-4a — the substantive answer: `OLDEST` was NOT absorbed.** I predict the
  history-derived population at every tree measured contains **zero** rows my
  classifier calls `OLDEST`, and that the `OLDEST` count moves only with the
  tree (10 → 11 → 12), never by reclassification. **The parent did not make
  A-2's mistake.**
- **P-4b — and its own gate could not have caught it if it had.** I predict I
  can construct a tree in which a site currently classified `OLDEST` is
  absorbed into the history-derived population — by deleting `--reverse` from
  its call — and that **`t1`'s `OLDEST` check stays green** through it, because
  the check reads `ANCHORS.tsv` rather than the classifier's rows.
- **P-4c — the boundary itself.** I predict the `OLDEST` *membership set* (not
  merely its count) at the parent's tree is a **subset** of the membership set
  at mine: 11 of the 12 are the same sites, one is new. **A count that grows
  is not evidence a boundary held; the set is.**

## P-5 — THE GATE AT THE POINT OF SPEND HAS A POPULATION DEFINED BY A DIRECTORY

**I predict at least one script outside `code/branching_audit_e34a/` spends a
`libe34a` anchor and does not call `gate_spent`**, and that `t2`'s rule is
silent about it because the rule walks one directory (M-5). I predict the
count of such external spending scripts is between 1 and 6.

## P-6 — TWO OF `libe34a`'s DERIVED ANCHORS CANNOT BE GATED BY NAME

**I predict `gate_spent(R, "LAST_TOUCHING_G1")` produces a SELF-ERROR** — the
"unknown name" path the parent designed as a safety feature — **even though
`LAST_TOUCHING_G1` is a genuine derived anchor of that module, spent in
`k1_prerepair.py:107`** (M-6). The self-error is right about the name-list and
wrong about the anchor. I predict the same for `NTH_TOUCHING_1`.

## P-7 — THE CONSTRUCTED DRIFT REPRODUCES AT MY TREE

The parent's table: `k4_cancel.py` exit 1 `TOTAL BAD: 2` clean → `TOTAL BAD:
3` drifted; `k2_five.py` exit 0 `TOTAL BAD: 0` clean → exit 1 `TOTAL BAD: 1`
drifted. **I predict both rows reproduce exactly at my tree, under a drift I
construct independently** (I will edit a pin to a different *real* revision, as
the parent did, but choose a different revision).

## P-8 — THE TWO LABELS, RECOUNTED

The parent: 20 sites, by SCOPE all another ticket's, by KIND **5 records and
15 live claims**. **I predict the residue at my tree is NOT 20** — commits
landed after the parent's measurement — **and I predict it is between 21 and
30, with the records share growing faster than the live-claims share** (each
new ticket ships transcripts and a `PREDICTIONS.md`). I predict both labels
print, separately, in my instrument and in `t3`'s.

## P-9 — DISTINCTNESS BY RESOLUTION

**I predict that on a constructed pair of two distinct commit shas whose blob
for a given path is byte-identical, a distinctness test on shas passes and a
distinctness test on the resolved blob fails**, and that `t4`'s pair
(`d01ff32d`, HEAD) still exhibits this at my tree.

## P-10 — THE FLOOR: ONE THING NO LIST IN THE BRIEF NAMES

`classify_call` returns `None` unless the call carries **both** a `log`
argument **and** a hash format. So the population — every population in this
arc, mg-330a's and mg-b2af's alike — is *revision-producing calls that use
`git log` with an explicit hash format*. **`git rev-list`, `git rev-parse`,
`git merge-base` and `git describe` all produce revisions and carry neither.**

**I predict there are revision-producing call sites in `code/` that use one of
those four porcelain/plumbing commands and are in NO published population of
this arc, and I predict there are between 5 and 40 of them.** This is the
flag-defined-population defect one level up from where the brief points, and
neither mg-330a nor mg-b2af looked for it.

## P-11 — MY OWN INSTRUMENT WILL CARRY THE DEFECT UNDER AUDIT

**I predict that at least one population in my own instrument turns out to be
defined by my own convenience rather than by the property**, that I find it
before shipping, and that it is kept in `README.md` rather than quietly fixed.
I predict **two or more** such defects.

---

## THE EXIT CODES, PREDICTED

| script | predicted exit | why |
|---|---|---|
| `selftest_0ba7.py` | **0** | assertions on constructed inputs; if it exits 1 the instrument is broken, not the subject |
| `a1_population.py` | **1** | P-2 and P-3 both predict the published population is short; a finding is a red |
| `a2_oldest.py` | **0** | P-4a says the substantive answer is clean; P-4b is a *demonstration about a gate*, recorded as a note, not a finding against the repair |
| `a3_gate.py` | **1** | P-5 and P-6 both predict ungated spend |
| `a4_labels.py` | **0** | P-8 predicts a moved count, which is the tree moving, not a defect |
| `a5_resolution.py` | **0** | P-9 predicts the repair's own lesson holds |
| `a6_floor.py` | **1** | P-10 predicts a population nobody enumerated |
| `run_all.sh` aggregate | **1** | worst of the above |

**I predict at least 4 of these 8 exit codes are wrong.** The parent predicted
its twelve would not all land and then all twelve landed; predicting mass
failure is the same over-correction in the other direction, so 4 is a real
number and not a hedge.

---

## WHAT I WILL NOT DO

- I will not re-run the parent's suite and report its exit codes as my
  measurement. Its transcripts are committed; where I read them I will say
  **READ**.
- I will not rewrite `ANCHORS.tsv`, `libe34a.py`, or anything in
  `code/audit_330a/`, `code/repair_b2af/` or `code/branching_audit_e34a/`.
  Every mutation happens in a clone under the system temp directory.
- I will not shrink a disagreement by adopting the parent's classifier. The
  point of an independent audit is a second implementation.
