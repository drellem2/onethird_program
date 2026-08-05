# mg-d075 — PREDICTIONS, committed BEFORE any script of this repair exists

**Written and committed before a single line of `code/branching_bound_d075/*.py` was
written.** The pre-filed independent audit is `mg-aaf4`; it is instructed not to take my
numbers on trust, and this file is the thing it measures me against. Nothing below is
revised after a run. A refuted prediction stays as written and is reported as refuted.

---

## 0. FULL DISCLOSURE — every command I ran before writing this file

I did not come to these predictions cold. I read the parent's committed transcript and I
ran hand greps. All of them, in order:

1. `mg show mg-d075`, `mg show mg-aaf4` — the brief and the pre-filed audit.
2. `ls`, `ls code`, `ls docs/`, `wc -l docs/OneThird-Branching-Graphs-Where-This-Lives.md`.
3. `git log --all --oneline | grep -i 19ec` — the parent's five commits.
4. `ls code/branching_audit_19ec/`.
5. `grep -rn "33" --include=*.md --include=*.py --include=*.txt . | grep -i interval | head -40`.
6. `cat code/branching_audit_19ec/out_e5_population.txt` — **the parent's POP-3 block,
   which states 8 sites / 4 bounded / 4 unbounded and prints all eight.** I have read it.
7. `cat code/branching_audit_19ec/e5_population.py` — **the parent's detector source.**
   I have read the POP-3 predicate: a live sentence containing `\b33\b` **and** matching
   `Young–Fibonacci|Young-Fibonacci|`\[0̂, w\]``, scored BOUNDED by
   `rank(w) ≤ 6 | to rank 6 | rank 6` **in the same sentence**.
8. `grep -n "33" docs/OneThird-Branching-Graphs-Where-This-Lives.md` — 10 hit lines:
   166, 177, 186, 187, 209, 220, 225, 307, 413, 414.
9. `grep -rln "33" docs/*.md` and a per-file `grep -c "33"` loop over `docs/*.md`.
10. `sed -n '160,230p' docs/OneThird-Branching-Graphs-Where-This-Lives.md`.

**So P1 below is not a blind guess.** It was derived by hand from (8) and (10) against the
predicate I read in (7). What has *not* happened is any execution: no script of this repair
exists, and the hand derivation has not been checked by a machine. That is the thing being
predicted — whether my hand count survives a parser.

---

## 1. THE COUNT — is EIGHT the population?

The brief tells me not to inherit 8. I do not.

**P1 — EIGHT IS NOT THE POPULATION EITHER. I predict 9, not 8, and 5 unbounded, not 4.**

- **Population:** live sentences in `docs/OneThird-Branching-Graphs-Where-This-Lives.md`
  — *live* exactly as the parent defined it (outside fenced code, outside block quotes,
  outside units carrying a `**STRUCK` / `**CORRECTED` / `**RE-SCOPED` marker or one of the
  three "the version/reading this replaces" / "the scope this adds" phrases).
- **Grain:** one sentence, split by the parent's own splitter.
- **Predicate:** the sentence states the 33-interval figure **about Young–Fibonacci
  intervals**, where the attribution may come from the sentence *or from the table cell /
  paragraph the sentence sits in*. This is the parent's predicate with exactly one clause
  relaxed: the demand that the naming string sit in the same sentence as the numeral.
- **Predicted value: 9 sites — 4 bounded, 5 unbounded.**

**P1a — I name the ninth site in advance.** It is the second 33-sentence of the row-10 cell
at **line 307**: *"Row 10 therefore has an index-set contact of the **same kind** as the one
this document headlines for Young's, on 28 of 33 intervals; …"*. It states the figure, it is
about Young–Fibonacci intervals, it carries **no** rank bound, and the parent's POP-3 misses
it because the sentence says *"for Young's"* and never spells "Young–Fibonacci".

**P1b — the parent's own POP-1 already printed this sentence** (POP-1 `[09]`, line 307) and
scored it unbounded. So the ninth site is not new evidence; it is the parent's own two
instruments disagreeing with each other, and only the smaller number reaching the verdict.

**P2 — the parent's 8/4/4 reproduces exactly under its own predicate.** Re-implemented
independently and run against the same file at this commit, the parent's POP-3 predicate
returns population 8, bounded 4, unbounded 4, and the same eight line numbers
(166, 166, 175, 181, 202, 307, 413, 414). *If this fails, the disagreement is mine to
explain, not the parent's.*

**P3 — the four the parent called unbounded are the four I will find unbounded**, i.e. my
five-element unbounded set is the parent's four plus the line-307 sentence, with no site
moving in the other direction.

**P4 — widened to the whole `docs/` corpus** (same liveness rule, same relaxed predicate,
population = live sentences in all `docs/*.md`), the count is **greater than 20** and the
unbounded fraction is **greater than half**. I have not counted this by hand and have no
site list for it; this is a genuine forecast.

**P5 — the corpus number will NOT be repaired, and that is a scope decision, not an
oversight.** Historical audit and repair documents are dated records of what was measured
then; rewriting them would destroy the evidence trail this arc runs on. My repair population
is exactly one file: `docs/OneThird-Branching-Graphs-Where-This-Lives.md`, the living
document. I predict I will report a corpus count I do not repair, and name it as such.

## 2. THE REPAIR

**P6 — after the repair, unbounded = 0** on my repair population under my own relaxed
predicate, **and** 0 under the parent's stricter one. Population 9 unchanged: I bound
sentences, I do not delete them.

**P7 — no hedge is introduced.** Every bound I add is an ENUMERATION or a stated numeric
scope (`rank(w) ≤ 6`, `to rank 6`, an explicit list), never a softening word. Scanned
against a hedge-token list of **at least 26 tokens** in the *same sentence* as the new
phrasing, the count of new phrasings carrying a hedge token is **0**.

**P8 — the sharpest site is line 186** — the clause faulting Young–Fibonacci for *"naming
no class of `P`"* whose own statement of the **Young** classification (*"the intervals of
Young's lattice are `J(P)` for `P` **exactly** the skew cell posets"*) carries no bound,
while the measurement under it covers only `|λ| ≤ 6`, 30 intervals. I predict the repair of
this site must bound **both halves** — the criticism and the thing it is made from — and
that bounding only the Young–Fibonacci half would leave the defect exactly where it was.

## 3. THE THING THE BRIEF SAYS TO EXPECT OF MYSELF

The brief: *"Whoever repairs this should expect to do the same thing somewhere in the
repair, and should look for it deliberately."*

**P9 — I WILL DO IT. I predict that the first run of my own criticism-sentence check
(`s5`) over my own README finds AT LEAST ONE unbounded sentence of mine in which I fault
someone else's scope.** I predict `s5` **exits 1 on its first run**, and I will commit that
first transcript rather than only the fixed one. If `s5` exits 0 first time I will say so,
and P9 is refuted.

**P10 — the class, not the instance.** I predict my honest answer to *"did you address the
instance or the class?"* is **the instance, plus one class-level artefact and no more** —
because a document-wide bound is enforceable by a checked-in instrument but the *arc*-wide
class (a term denoting 39 vs a table classifying 17; a hand-list of 5 vs a gate printing 6;
a figure at 8-or-9 sites bounded at 4) is not fixable by any edit to this document. I
predict I will say that plainly rather than claim the class.

## 4. EXIT CODES — every script, predicted before it exists

| script | what it exits on | predicted |
|---|---|---|
| `s1_census.py` | 1 if my count on the parent's population ≠ 8 | **1** |
| `s2_reproduce.py` | 0 if the parent's own 8/4/4 reproduces exactly | **0** |
| `s3_bound.py` | 0 if unbounded = 0 on the repaired doc, both predicates | **0** |
| `s4_hedge.py` | 0 if 0 new phrasings carry a hedge token in their own sentence | **0** |
| `s5_own_criticism.py` | 1 if any of MY OWN criticism sentences is itself unbounded | **1 first run, 0 final** |
| `s6_class.py` | 0 always — it reports, it does not gate | **0** |
| `selftest_d075.py` | 0 if every mutation of the doc is caught by the detector | **0** |
| `run_all.sh` | 0 iff every script matches the row above | **0** |

**Nine predicted exit values across 7 scripts + the runner.**

## 5. THE FLOOR — one thing no list names

The audit's standing asks for at least one thing no brief names. Mine:

**P11 — THE PARENT'S LIVENESS RULE ADMITS A CELL OF A ROW THAT RECORDS A WITHDRAWN CLAIM.**
Site `<08>`, line 414, is the fourth cell of ledger row **B4′**, whose *second* cell opens
*"(the reading this replaces, mg-6ad0's X4)"* — the exact phrase the parent's own STRUCK
regex matches. The regex is applied per **cell**, so the marker excludes the cell that
carries it and admits the three beside it. I predict this is real: **the same row yields
both struck and live cells**, and I predict **at least 2 cells of row B4′ are excluded as
struck while at least 1 is admitted live.** Whether that is a defect is an adjudication I
will make in prose; the structural fact is what I am predicting.

**P12 — and it is not confined to B4′.** I predict **at least one other ledger row** in the
document splits the same way — some cells struck, some live, from one row. Count predicted:
**≥ 1 row besides B4′.** I have not looked.

---

*Committed before `s1`…`s6`, `selftest_d075.py`, `lib_d075.py` and `run_all.sh` existed.
Twelve predictions, nine exit values. Whatever these turn out to be, they stay as written.*
