# `code/branching_repair_7e58` — the instrument for mg-7e58

`mg-321d` confirmed that `mg-58da` restored the set-level corroboration — **10
of 10** pairs of sources agreeing at **24 of 24** cells, all five members
re-run — and then found that the apparatus which established that provenance
was **wrong about its own**.

> **G-1** `g1_provenance.py` asked *"did the measuring half change?"* and
> answered with a **file sha**, so `mg-58da`'s own commit made it **exit 1 on a
> finding its own section (iv) refutes**.
> **G-2** `g4_fleet.py` attributed by *"committed sha vs working-tree sha"*, so
> once `673b4c0` landed it said `ed9cde4` had touched `c1_branching.py`. It
> never did.

Both are repaired in `code/branching_audit_58da/`. This directory checks the
repair.

```
./run_all.sh          # ~8-12 min, pure Python 3, no dependencies, NO NETWORK
```

Committed outputs: `out_selftest_7e58.txt`, `out_k1_grain.txt`,
`out_k2_selfprov.txt`, `out_k3_setlevel.txt`, `out_k4_doccheck.txt`.

**Exit codes are the finding channel.** Every `k*.py` exits `0` iff
`SELF-ERRORS == 0` **and** `FINDINGS == 0`, and both numbers are printed
separately, so a non-zero exit never means the instrument is broken. **All four
are predicted to exit `0`** — a stronger claim than usual, and deliberate: this
ticket's job is to make an apparatus right about itself, and one that still has
something to report about itself has not finished. `PREDICTIONS.md` holds every
exit code and answer predicted **before** the run, **with three misses kept as
written**.

## The three things this directory is for

**1. `g1` was repaired, not silenced.** The disposition `mg-321d` demanded is
stated: *the section is right and `g1` should not fire*. So the file-sha
predicate is replaced by one that runs **both script revisions against the same
target**, on **both target forms**, and diffs `c1`'s own measurement — and then
`g1` itself, unmodified and in place, is run in four clones whose
`c1_branching.py` is mutated (never `g1`): **4 of 4** directions predicted, and
the clone carrying a real regression in the measuring half makes `g1` **exit
1**. Rows two and four of that table are the point — the file sha moves in both
and only one is a defect.

**2. `g4`'s attribution comes out of the history.** `k1 (iv)` re-derives it by
**two** routes that share no code with `g4` (`git log -- <path>` per member,
`git show --name-only` per commit), requires them to agree with each other
before either is used, and then compares both against what `g4` prints. `g4`
also gates its own summary against its own rows now, once per member plus the
union. The deletion test is **a commit landing** — the path `G-2` itself took.

**3. The set-level property is re-derived, not quoted.** This repair touched
**none** of `mg-a218`'s five, which is exactly why *"the member I changed still
works"* would say nothing. `k3` reads all five sources with readers written
here, compares **10 of 10** pairs at **24 of 24** cells over **240** cell
comparisons, re-runs **5 of 5** members in place, and probes each reader at a
cell it must move at and nowhere else — **5 of 5**.

## And the question the mayor added

*Enumerate the ways your own fix could exhibit the defect it remedies, and check
each.* That is `k2`: nine branches, each measured or given a **stated reason**
it cannot bite. The sharpest is **B1** — this repair's evidence is recorded
before the commit that commits it, which is `G-3`'s exact shape — so `k2` clones
the worktree, **commits the repair there**, and re-runs `g1` and `g4`:
self-errors, findings, exit codes and finding **texts** all identical.

## What each file decides

| file | what it decides |
|---|---|
| `lib7e58.py` | the readers and the clone helper. Five readers for the five sources, written from the file formats and sharing no line with `lib58da.py` or `lib321d.py` — two readers that share a line share a blind spot. `scratch_clone()` makes a real git clone **with the working tree committed**, which is the only honest way to ask whether a repair survives being committed |
| `selftest_7e58.py` | **65 assertions** on the apparatus before it is believed: the readers on known, **absent** and **hostile** input; cell locality; `replace_once` refusing to corrupt zero sites or two; the output parsers; the git helpers against the four named revisions; and `scratch_clone` in all three of its modes |
| `k1_grain.py` | the two sites, **before** and **after**. The before state is reproduced at `ef38841` in a clone, not quoted. **4 of 4** deletion probes on `g1` itself; the attribution derived twice and compared against `g4` at all five members |
| `k2_selfprov.py` | the nine branches on which this repair could carry the defect it removes |
| `k3_setlevel.py` | the property that was not to be lost, re-derived from the files |
| `k4_doccheck.py` | every figure in this repair's document, read **at its own site** against a committed `out_k*.txt`, each gate deletion-tested with a null probe beside it |

## Three things corrected during construction, not silently

All three are in `PREDICTIONS.md` as misses, and all three have the same shape:
**the repair was right and my instrument for checking it was wrong.**

* `k1`'s *"comparing half"* probe inserted its line **before** `c1`'s section
  (iii) header, which put it inside the **measuring** half. The probe was
  testing the opposite of what it claimed to test, and `g1` was right to fire.
* `k2`'s `B2` counted `mine_c`, `mine_v`, `mine_named` — names `c1`'s comparing
  half **binds for itself** — as quantities inherited from the measurement, and
  booked a finding against `c1`. `B3` looked for `c1`'s `Form read:` line in
  `g1`'s output; `g1` does not echo `c1`'s stdout.
* `k3`'s `b1_cells()` returned **0** cells — written with `mg-321d`'s own
  header miss on the page, and then matching a **row** shape `mg-2060` does not
  use. It went to the **SELF-ERROR** channel and the source was **withdrawn**,
  never scored as a disagreement, which is what that channel is for. And the
  locality probes first aimed at `beta=3, n=6`, whose row `beta=2` carries
  identically, so **none** of the five could be aimed at all.

One more was found in this repair's own code rather than in the checking of it:
`g1`'s internal probe builds a mutated `c1` from a source string, and in a tree
where `c1` had **already** been mutated the string was absent and `g1` raised
`ValueError` instead of reporting. It now books a **SELF-ERROR** and names the
probe as dropped — *"I could not build the probe"* is a fact about `g1`, never a
finding against anyone, and a shrinking population must stay visible.

## What is NOT closed here

* `c3_withdrawal.py` is red. That is `mg-d330`'s second finding, booked OPEN by
  `mg-58da`, and `k3` reports it by name rather than counting it as its own.
* `mg-d330`'s `e4` gate on `mg-a218`'s exit-code sentence is a **presence
  test**. `mg-58da` booked it and refused to work around it; so does this.
* `mg-321d`'s `M-1` (`g1`'s record check reads two git blobs and never the file
  in the tree) and `M-2` (the narrowing covers absence but not misread). Both
  are real, neither is in this ticket's scope, and neither is touched — `g1`
  still does not call `read_worktree` on `mg-a218`'s directory, so `M-1` stands
  exactly where `mg-321d` left it.
