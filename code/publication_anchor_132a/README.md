# mg-132a — a figure's provenance is where it was **computed**, not where it came to rest

    sh run_all.sh                  # ~10 s, exit 0
    sh run_all.sh --at <rev>       # the same audit as of any commit — RUN THIS AFTER A MERGE

Committed transcript: `out_anchor_132a.txt`. The decision and the predictions, **written and
committed before this instrument existed**: `PREDICTIONS.md`.

## The defect

`repair_7e39.py` repaired mg-7e39's **F2** — *"a population figure that was already wrong at the
commit which published it"* — with a check keyed on `publishing_commit(rel)`, which is
`git log -1 -- rel`.

At `94ecf9d` **that check is red on the two transcripts it was built to protect.** Both publish
`473`; the tree at each one's publishing commit holds `481`.

**And they were right when written.** The pre-merge commits `8a07ae0` and `3d7b32f` hold exactly
`473`. **The merge rebased them** onto a tree that had grown, and `git log -1` follows a file to
wherever a rebase puts it — so **the commit that publishes each figure is no longer the commit it
was measured at**.

> F2 was *wrong when written*. This is the complementary failure, and the repair's vocabulary had no
> word for it: the "publication step" it separates from prose is **the run**, and the step that broke
> this is **the merge**.

## The decision: answer (2)

The ticket named two coherent answers. **This deliverable takes (2) — stop keying on `git log -1`;
a figure's anchor is the commit it was *measured* at** — and the reason is a fact about the tree
rather than a preference:

> **The anchor was already published. The checker was reading the wrong field.**
> `repair_ec07.py`'s `population_line()` has been writing *"… walked from the WORKING TREE at HEAD
> 8a07ae01fc45"* all along, and `repair_7e39.py` prints `HEAD : 3d7b32fdd240` at the top of its own
> transcript. **Both transcripts name the tree they measured.** Adopting (2) costs nothing because
> the publication step has been recording the anchor from the start; choosing (1) would discard
> provenance that is already on disk in order to preserve a query that was never the right one.

Two further reasons: **(1) makes every rebase a silent invalidation that only a re-run can detect**,
and nothing re-runs after a merge — under (1) the repository's correctness becomes a property of how
recently someone happened to run the suite. And **a rebased figure is not false**: `473 at 8a07ae0`
is a true statement about a named tree and stays true. What it loses is **currency**, not **truth**.

**(1) is not rejected — it is demoted from rule to repair.** It is what you do when (2) cannot be
satisfied, because an unanchored figure has no way back except a re-run. That is exactly the
prescription this instrument issues for the two legacy transcripts (see *the exposure*, below).

### The price, stated rather than hidden

Under (2) a reader can meet `473` beside a tree of `481` and the check stays green. **That is only
tolerable while the anchor resolves.** The instant it does not, `473` is the unfalsifiable assertion
in a file that (2) is accused of being. So:

* every anchor is **verified by re-deriving the count at the named rev** — never believed (`A2c`);
* an anchor that resolves to nothing is **red** (`A1b`);
* the declared anchor line carries a **digest of the population**, so a figure whose anchor commit
  has been pruned can still be located (`A2d`).

## Six verdicts where `STALE` was one word

| verdict | meaning | gate |
|---|---|---|
| `AGREES` | anchor verified, and the publishing tree holds it too | green |
| `DISPLACED` | anchor verified; the publishing tree holds something else — **right when written, moved by a rebase** | **green, and named** |
| `WRONG WHEN WRITTEN` | the anchor resolves and its tree does **not** hold the figure — mg-7e39's F2 proper | **red** |
| `UNANCHORED` | the transcript names no commit that resolves | **red** |
| `UNRESOLVABLE` | an anchor was declared and is gone, and no tree holds its digest | **red** |
| `INCONSISTENT` | the declared `count=` disagrees with the figure the file publishes | **red** |

`DISPLACED` being green **is** the decision. A displaced figure is a correct statement about a named
tree; `A1c` is where a reader learns that a re-run is owed.

## The declared anchor line

The publication step now writes its provenance as a field rather than leaving it in a sentence:

    POPULATION ANCHOR: commit=<40 hex> count=<n> digest=<16 hex> scope=code/**/*.py

`A2f` asserts that this line is **not itself readable as a population figure** — adding provenance
must not change which number a reader, or the checker, takes as the figure. Transcripts written
before the line existed fall back to an **inferred** anchor (resolving hex tokens in their own
text); `A1e` labels those, and says plainly that **inference selects for agreement and therefore
cannot witness `WRONG WHEN WRITTEN`** on a legacy transcript.

## Every rung is shown firing, on this repository

| | |
|---|---|
| `A2a` | **the original F2, on the commit where it is still present.** The transcript at `77306a7` is caught — not as a tree mismatch but as **`UNANCHORED`**: it contains no hex token at all. *It names no tree.* A figure that names none cannot be right or wrong, only unchecked, which is why it survived a publication step |
| `A2b` | **the same bytes, two commits, two verdicts.** `out_repair_6df0.txt` is byte-identical at `c1a57fd` and `3958b5a` and reads `AGREES` at the first, `DISPLACED` at the second. **Nothing about the file changed — the merge moved it**, and no run happened in between |
| `A2c` | `WRONG WHEN WRITTEN` on a **self-consistent** declared anchor, so nothing cheaper could have caught it: the file agrees with itself and only the tree can refute it |
| `A2d` | the **digest buys back a pruned anchor** — an anchor sha naming no object recovers, and the figure survives its own anchor |
| `A2e` | and recovery **fails closed** when no tree holds the digest. A recovery that could only succeed would be a blessing, not a check |
| `A2g` | a declared anchor **true about its tree and wrong about its file**. ⚠️ No tree lookup could see this: whichever tree is named, one of the two numbers matches |
| `A2h` | **a digest witnesses a population, not a commit** — many commits share one, because a commit adding no `.py` file leaves the population untouched. Enough to verify a *count*, not enough to identify provenance uniquely |

## Two defects of this instrument, kept rather than smoothed away

1. **The first version of `A2d` built a self-contradictory forgery** — an anchor stating one tree's
   count inside a transcript publishing a different figure — and the run **refuted it**. The forgery
   was wrong, not the lattice; but it exposed a rung that did not exist. **`INCONSISTENT` and `A2g`
   exist because of that refutation.**
2. **Digest recovery is many-to-one** and the first version did not say so. `A2h` now measures it.

## The exposure, measured (`A1d`, `A2i`)

Both legacy anchors are **verified and not reachable** from the mainline: they survive only because
`origin/polecat-3f3b` still exists, and **no reachable commit holds the population they were
measured against**. Delete that branch, run `git gc`, and those two figures become permanently
uncheckable — no digest to search by and no tree left to find.

**For those two files specifically the remedy is answer (1): re-run them.** That is not a
contradiction of the decision; it is the decision applied to figures that predate it.

## The gap this deliverable does **not** close (`A3c`)

**Nothing re-runs the staleness check after a merge**, and the rebase that produced this defect is
performed by the refinery, *outside* the repository. No artifact committed inside it can run after
one — `A3c` reports the post-merge hook count rather than asserting the point.

What is delivered instead is **`--at <rev>`**, so a post-merge audit is one command (`A3d` exercises
it at a commit that is not HEAD), and a banner at the top of every transcript saying:

> **a committed `0 REFUTED` is a measurement at the run's commit, not a live property of the
> repository.**

Claiming the gap closed would be this deliverable committing the defect it repairs.

## What changed in `repair_7e39.py`

| | |
|---|---|
| `S4a` | keyed on **the anchor**, with the publishing commit reported *beside* it rather than standing in for it. It was red at `94ecf9d`; it is green now, reporting **2 `DISPLACED`** |
| that row's own sentence | the clause *"a merge that lands elsewhere cannot make it red"* **was false** — a merge that rebased this file's own evidence made it red within four commits. Corrected in place |
| `S4a'` | a new row saying the section's result is a measurement at the run's commit |
| `POP_FIGURE`, `py_files_at`, `publishing_commit` | **bound to `anchor_132a.py`'s, not copied.** One definition of the rule in the tree — this repository has already been bitten by two copies of `figures()` disagreeing on 3 (`8c55168`) |
| `S0` | emits the **declared anchor line**, so this transcript's own provenance stops being something a reader has to infer |

## Reproduction

Read-only apart from its own transcript — unlike the mg-3f3b suite it mutates nothing, so it has no
restore path to get wrong. Every figure it prints is re-derived from `git ls-tree` at a named rev on
each run; nothing in this README carries a population figure, because prose has no publication step
that recomputes it.
