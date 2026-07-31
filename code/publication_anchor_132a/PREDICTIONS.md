# mg-132a — predictions, written BEFORE the instrument exists

**Committed alone, before `anchor_132a.py` is written.** Everything below is a claim about a
repository I have read with `git log` / `git ls-tree` and about an instrument that does not yet
exist. Misses are kept as written.

## The finding I was pointed at, restated as a measurement

mg-97fb reports that both transcripts in `repair_7e39.py`'s `COMPUTED` publish **473** while the
tree at their publishing commit holds **481**, and that they were **right when written** — the
pre-merge commits hold exactly 473 and the merge rebased them.

**P0 — the baseline, before I change anything.** `sh code/hodge_leverage_repair_3f3b/run_all.sh` at
`94ecf9d` exits **1** with **S4a REFUTED**, naming both transcripts, `473` against `481` at
`3958b5a` and `75333b2`. The *committed* `out_repair_3f3b.txt` at `75333b2` says `0` disagree and
the suite exited 0. Both are true; they are measurements at different commits.

> *Measured before writing this file so that the rest of the document is built on a fact rather than
> on the ticket's word. Recorded here as a prediction anyway, because a prediction I have already
> confirmed is worth less than one I have not and should be labelled so: **P0 is CONFIRMED IN
> ADVANCE**, and P1–P12 are not.*

## The decision: (2), and why

The ticket names two coherent answers and asks for one.

**I take (2): stop keying on `git log -1`. A figure's anchor is the commit it was MEASURED at.**

Three reasons, in order of weight.

1. **The anchor is already published — the checker was reading the wrong field.** This is the
   decisive one and it is a fact about the tree, not a preference.
   `repair_ec07.py:population_line()` already writes *"473 .py files swept, walked from the WORKING
   TREE at HEAD 8a07ae01fc45"*, and `repair_7e39.py` already prints `HEAD : 3d7b32fdd240` at the
   head of its own transcript. **Both transcripts name the tree they measured.** Option (2) costs
   nothing to adopt because the publication step has been recording the anchor all along; only
   `publishing_commit()` ignored it and asked `git log -1` instead. Choosing (1) would throw away
   provenance that is already on disk in order to preserve a query that was never the right one.
2. **(1) makes every rebase a silent invalidation detectable only by a re-run** — and nothing
   re-runs after a merge, which is the gap that produced this defect. Under (1) the repository's
   correctness is a property of *how recently someone happened to run the suite*.
3. **A rebased figure is not false.** `473 at 8a07ae0` is a true statement about a named tree and
   stays true forever. What it loses is *currency*, not truth, and those deserve different words —
   the existing check has one word for both and calls it `STALE`.

**The cost I am accepting, stated up front:** under (2) a reader can meet `473` beside a tree of
`481` and the check stays green. That is only tolerable because the figure names its own tree, so
the reader can tell which. The moment the anchor stops resolving, `473` becomes exactly the
unfalsifiable assertion the ticket warns about — which is why P5/P6 below are gates and not notes.

**What (1) still is:** the remedy when (2) cannot be satisfied. An unanchored or unresolvable figure
has no way back except a re-run. So (1) is not rejected; it is demoted from *rule* to *repair*.

## The verdicts the instrument will distinguish

`STALE` is one word doing four jobs. The instrument will separate them, per transcript:

| verdict | anchor resolves? | anchor tree yields the figure? | publishing tree yields it? | gate |
|---|---|---|---|---|
| `AGREES` | yes | yes | yes | green |
| `DISPLACED` | yes | yes | **no** | **green, and named** — right when written, moved by a rebase |
| `WRONG WHEN WRITTEN` | yes | **no** | — | **RED** — this is F2 proper |
| `UNANCHORED` | **no commit named at all** | — | — | **RED** — unfalsifiable |
| `UNRESOLVABLE` | named but gone | — | — | **RED** unless recovered by digest |

## Predictions

**P1 — the two live transcripts are DISPLACED, not stale.** `out_repair_6df0.txt` anchors at
`8a07ae0` and `out_repair_3f3b.txt` at `3d7b32f`; each anchor tree holds **473**, each publishing
tree holds **481**. Verdict `DISPLACED` for both, **0 WRONG WHEN WRITTEN**.

**P2 — the original F2 is caught by the new rule, by a different route.** The transcript committed at
`77306a7` publishes **429** against a tree of **448**. I predict it is caught not as a
tree-mismatch but as **`UNANCHORED`**: I have grepped it and it contains **no hex token of 12+
characters at all**. It names no tree. That is a stronger statement about why it was wrong than
"the number disagrees with the tree", and it means the repaired rule still fires on the commit
where the defect is present.

**P3 — the same bytes, two commits, two verdicts.** `c1a57fd` (pre-rebase) and `3958b5a`
(post-rebase) publish an **identical** `out_repair_6df0.txt`. Audited as of `c1a57fd` the verdict is
`AGREES`; as of `3958b5a` it is `DISPLACED`. **Nothing about the file changed.** This is the rebase
made visible in a single row, and it is the control that shows the old rule could not have seen it.

**P4 — the anchor must be verified, never asserted.** Every anchor row is `git ls-tree` at the named
rev, recomputed. A recorded commit that is merely *stated* is worth nothing.

**P5 — an unresolvable anchor is RED, and a digest is what buys it back.** Going forward the
publication step emits a declared line carrying the commit, the count **and a digest of the sorted
population**, so that a figure whose anchor commit has been pruned can still be located by
searching history for a tree with that digest. I predict recovery **succeeds** for this
deliverable's own transcript when I delete the anchor sha from a copy and force the search path.

**P6 — an INFERRED anchor is weaker than a DECLARED one, and will be labelled so.** The two live
transcripts predate the declared line, so their anchor must be *inferred* by resolving hex tokens
in their text and keeping those whose tree yields the figure. **That inference selects for
agreement and therefore cannot witness `WRONG WHEN WRITTEN`.** I predict I will have to report this
as a limitation of the compatibility path rather than hide it, and that A-rows on inferred anchors
will carry the word `INFERRED`.

**P7 — the anchors are alive only on a side ref.** `8a07ae0`, `c1a57fd` and `3d7b32f` are **not
reachable from HEAD** — they survive because `origin/polecat-3f3b` still exists. I predict the
instrument reports `reachable-from-audited-rev: NO` for both live anchors, and that this is the
honest price of (2): a provenance anchor one `git gc` away from disappearing. Predicted count of
verified-but-unreachable anchors: **2**.

**P8 — the gap: nothing re-runs after a merge.** I predict I cannot close this from inside the
repository, because the rebase is performed by the refinery and no hook in this tree runs after it.
What I *can* do, and predict I will: make the audit take `--at <rev>` so it is one command against
any commit including a post-merge one, and **state in the README that a committed `0 REFUTED` is a
measurement at the run's commit and not a live property**. Predicted: the README says this in those
terms.

**P9 — the existing S4a's own sentence is false and will be corrected.** It reads *"keyed on each
transcript's OWN publishing commit rather than on HEAD — so a merge that lands elsewhere cannot
make it red"*. A merge that rebases **this file's own commit** did make it red. Predicted: that
clause is rewritten, and `repair_7e39.py`'s S4 keys on the anchor with the publishing commit
reported beside it.

**P10 — one source of truth, not two copies.** `repair_7e39.py` will *load* the anchor rule rather
than re-implement it. The repo has already been bitten by two copies of `figures()` disagreeing on
3 (`8c55168`). Predicted: exactly one definition of the verdict lattice in the tree.

**P11 — my own transcript AGREES at the commit that publishes it, and is DISPLACED after the
merge.** My commits land in this order: predictions (no `.py`), instrument (`+1 .py`), transcript
(no `.py`). So the anchor commit and the publishing commit hold the **same** population and the
verdict is `AGREES` — until the refinery rebases the branch onto a grown `main`, at which point my
own transcript becomes `DISPLACED` exactly like the two it audits. **I predict this, I will check it
after the merge rather than before, and I predict the post-merge verdict is `DISPLACED` with the
anchor verified — not `WRONG WHEN WRITTEN`.**

**P12 — exit codes.** `sh code/publication_anchor_132a/run_all.sh` exits **0**.
`sh code/hodge_leverage_repair_3f3b/run_all.sh` exits **0** after the repair, having exited **1**
before it (P0), and its S4a reports **2 DISPLACED, 0 wrong when written** rather than **2 stale**.

## What I am NOT predicting (written before the instrument)

I do not predict that adopting (2) makes the two live figures *current*. It does not, and it is not
supposed to. `473` beside a tree of `481` is still `473` beside a tree of `481`; what changes is
that the repository can now say **which of the two questions it is answering** and stops reporting
`0 STALE` for a state that has one answer of each.

---

# OBSERVATIONS — appended after the runs, with the predictions above untouched

Nothing above this line has been edited. Two predictions missed and both misses are kept, because
each one bought a control that would not otherwise exist.

| | outcome |
|---|---|
| **P0** | **HELD.** exit **1**, `S4a` REFUTED, both transcripts named. Measured before the predictions were written and labelled as such |
| **P1** | **HELD.** `DISPLACED` / `DISPLACED`, **0 `WRONG WHEN WRITTEN`** — anchors `8a07ae0` and `3d7b32f`, each holding the figure, each publishing tree holding more |
| **P2** | **HELD, and more sharply than predicted.** `77306a7` is `UNANCHORED` — **0** hex tokens in it resolve to commits. It names no tree at all |
| **P3** | **HELD.** `A2b`: byte-identical file, `AGREES` at `c1a57fd`, `DISPLACED` at `3958b5a` |
| **P4** | **HELD.** Every anchor count is re-derived by `git ls-tree`; `A2c` is the control that shows a *self-consistent* declared anchor still refuted by its tree |
| **P5** | **HELD — after the first attempt was refuted.** See *miss 1* |
| **P6** | **HELD.** `A1e` labels inferred anchors and states the structural weakness |
| **P7** | **HELD WHEN WRITTEN, AND THE NUMBER MOVED FOR A REASON I DID NOT ANTICIPATE.** See *miss 2* |
| **P8** | **HELD.** `A3c` reports **0** post-merge hooks and declines to claim the gap closed; `--at` delivered and exercised by `A3d` |
| **P9** | **HELD.** The false clause is corrected in place and the correction names what refuted it |
| **P10** | **HELD.** `POP_FIGURE`, `py_files_at` and `publishing_commit` are **bound** to `anchor_132a.py`'s. One definition in the tree |
| **P11** | **HELD at the publishing commit** (`A3a`: `AGREES`). The post-merge half is checked *after* the merge, not here |
| **P12** | **HELD.** New suite exit **0**; the mg-3f3b suite **1 → 0**, reporting `2 DISPLACED` where it had reported `2 STALE` |

## Miss 1 — the first `A2d` control was self-contradictory, and the run caught it

I predicted digest recovery would succeed. **It did — but my first control planted `3958b5a`'s
count beside a transcript publishing a different figure, and the run REFUTED the row.** The forgery
was wrong, not the lattice.

**What I had not predicted is what that exposed:** a declared anchor can be *true about its tree and
wrong about its file*, and **no amount of `git ls-tree` can see it** — whichever tree is named, one
of the two numbers matches it. That is F2's shape inside a single file. **`INCONSISTENT` and `A2g`
exist because a control of mine failed**, and `A2c` had to be rebuilt so that its forgery agrees
with itself, leaving the tree as the only thing that can refute it.

I also did not predict that **digest recovery is many-to-one**: many commits share one `code/`
population, because a commit that adds no `.py` file leaves it untouched. That is enough to verify a
*count* and not enough to identify provenance uniquely. `A2h` measures it; without it, `RECOVERED`
would have read as equal in strength to `DECLARED`, which it is not.

## Miss 2 — P7 predicted 2 unreachable anchors; the transcript reports 1

Both were unreachable when P7 was written and the first run confirmed **2**. The committed
transcript reports **1** — and the reason is the decision itself. Regenerating
`out_repair_3f3b.txt` through its own publication step, which the repair required anyway,
**re-anchored it at a reachable commit and upgraded it from `INFERRED` to `DECLARED`.** That is
answer **(1)** applied to a figure that predates the rule, exactly as the decision says (1) should
be used.

**So the deliverable demonstrates both answers on real files**: (2) as the rule that keeps
`out_repair_6df0.txt` honest without touching it, and (1) as the remedy that was available for the
transcript this arc owns. `A2i` records why (1) is the *only* remedy left for the other one — **no
reachable commit holds the population `473` was measured against**, so if `origin/polecat-3f3b` is
deleted that figure becomes permanently uncheckable.

## The prediction that cannot be settled here

**P11's second half.** This deliverable's own figures are `AGREES` at the commits that publish them
*in this branch*. The refinery rebases before it merges, which is the exact operation that displaced
the two transcripts this repair is about. **So the post-merge verdict is checked after the merge,
with `run_all.sh --at <merged-rev>`, and reported — not predicted green and left there.** A
deliverable about figures displaced by a merge that checked its own figures only before its merge
would be the defect one level up.
