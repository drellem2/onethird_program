# `mg-54b1` — the four transcripts in this directory, re-run on 2026-08-13, and what moved

The README beside this file is **mg-6cb9's own audit report and is not edited**: its "What it
found" table is that author's finding list, written against the tree of `e8fbd4f`, and rewriting
it would erase the thing this file exists to record. What follows is the correction, placed here
so that a reader who meets the false belief in `README.md` reaches it — which is the standard
`a3_differ_and_placement.py`'s own **A3c** applies to every other correction in this arc.

    sh run_all.sh                     # aborts at the self-test; see §4
    python3 -B a1_bothways.py         # ~83 s
    python3 -B a2_crosssection.py
    python3 -B a3_differ_and_placement.py

`out_a1_bothways.txt`, `out_a2_crosssection.txt`, `out_a3_differ.txt` and `out_selftest.txt` in
this commit are the output of those four commands, run in that order, from this directory, on
`main` + this branch. The pre-refresh copies are the parent commit's.

## The summary

| arm | committed before this refresh | today | class |
|---|---|---|---|
| `a1_bothways.py` | `A1 TOTAL BAD: 1` | `A1 TOTAL BAD: 0` | **verdicts moved** |
| `a2_crosssection.py` | `A2 TOTAL BAD: 2` | `A2 TOTAL BAD: 6` | **verdicts moved, and its baseline control is red** |
| `a3_differ_and_placement.py` | 8 flip tests, 5 placements, 7 thresholds | `AssertionError: mutation target absent` | **the instrument no longer runs at all** |
| `selftest6cb9.py` | `33 assertion(s), 0 failed` | `33 assertion(s), 2 failed` | **precondition failed** |

Four arms, four different outcomes, and only the first is the one `mg-54b1` was filed about.

## 1 — `a1`: three verdicts moved, and two of them are repairs

Exactly the table `p6e4f` filed, reproduced here:

| row | before | today |
|---|---|---|
| `Q2  check_doc.py IN delete C4's '2 of 45' anchor` | `1 0 *** MISSED ***` | `1 1 as predicted` |
| `Q10 w3_scope.py WIDE X4 in species_7d75/sub/leak.md` | `0 0 *** EXTENT WIDER ***` | `0 1 extent TRUE here` |
| `Q17 s1_extent.py WIDE X3 in species_7d75/sub/leak.md` | `0 0 *** EXTENT WIDER ***` | `0 1 extent TRUE here` |
| `check_doc.py` summary | `INSIDE 1/2 fired` | `INSIDE 2/2 fired` |
| WIDE sites silent | `3` | `1` |
| `A1 TOTAL BAD` | `1` | `0` |

**Q10 and Q17 are `README.md`'s finding #1** — *"EVERY REGULAR FILE in each tree is read is true
only because no species tree has a subdirectory"*. Both scans now read the subdirectory, so the
finding is **repaired in the subject**, not withdrawn by the instrument. **Q2 is finding #5's own
missed prediction**, and it now fires.

**Deterministic, measured rather than assumed:** three runs of `a1_bothways.py` — two consecutive
on a clean tree, one after the self-test and from the sequence above — are byte-identical. So the
committed/today difference is staleness and not flake.

## 2 — `a2`: the baseline control is red, so the exit code no longer discriminates

`R0` is `a2`'s unmutated baseline: the cross-section checker run with nothing planted, predicted
`0`. It now exits `1` with **5 standing strikes already present**, and every `OUT` probe therefore
also exits `1`. Four rows print `*** MISSED ***` for that single reason.

**A probe that plants a claim into a checker that is already red measures nothing by its exit
code**, so `a2`'s `IN`/`OUT` discrimination *as scored* is void on this tree, and its
`A2 TOTAL BAD: 6` should be read as four instances of one cause, not six findings.

**The instrument's other column survives, and this is worth keeping.** `a2` prints the checker's
own `standing` count beside the exit code, and that column still separates the two populations
exactly as the exit code did before:

    R0   baseline   5 standing
    R25  IN         6        R28   OUT   5
    R26  IN         6        R29   OUT   6   <-- the pre-existing miss, unchanged
    R27  IN         6        R29b  OUT   5
                             R30   OUT   5

3 of 3 `IN` raise it, 3 of 4 `OUT` leave it, and the one `OUT` that does not is `R29`, which was
**already** a `*** MISSED ***` in the committed transcript. The finding `a2` was built to
demonstrate is intact; what has gone is the ability of the number it *scores* to show it.

**Why `R0` is red is not this instrument's fault and not this branch's.** `e2_crosssection.py`
walks every `*.md` under `docs/` and `code/`, and that corpus has gone **267 → 530 files** since
its own transcript was committed. Five strikes now stand un-struck in documents that did not
exist then. `code/species_extent_d633/out_e2_crosssection.txt` says `E2 TOTAL BAD: 1` over 267
files; a re-run says `5` over 530. That directory is `mg-20ee`'s to repair — it is one of the 32
its ground truth already records as `DIFFERS` — and nothing here touches it.

**One of `a2`'s findings is repaired in the subject.** `README.md`'s finding #3 — *"reachable by
reading and not by running: called by 0 of 3 species-tree `run_all.sh`"* — now reads **3 of 3
ok**. All three of `species_repair_a4ef`, `species_repair_6f61` and `species_remainder_f8fa` call
`../species_extent_d633/e2_crosssection.py` from their runners.

**And `A2c`'s finding got larger rather than going away.** The committed extent line was
`*** FALSE, off by 5 ***`; it is now `*** FALSE, off by 263 ***`, and the committed census that
survived last time — *"the census is right, so the verdict survives"* — is now `*** WRONG ***`
too (18 files / 37 strikes committed, against 43 / 154 in the shipped tree).

## 3 — `a3`: DEAD, and it is a different failure from the other three

`a3_differ_and_placement.py` does not produce a verdict today. It raises:

    AssertionError: mutation target absent:
      '        if not os.path.isfile(p) or f in EXCLUDE:\n            continue'

`D1` and `D1e` plant an extension rule back into `code/species_repair_a4ef/s1_extent.py` by
matching **two lines of its source verbatim**. `mg-821e` / `mg-5040` rewrote that scan into a
recursive walk, so the two lines are gone and `kern6cb9.py`'s mutation helper refuses to do
nothing — correctly, and loudly. The tree is left clean: `git status --porcelain` is unchanged
after the raise, which is `selftest6cb9.py`'s assertion 3 doing its job.

**This is `mg-686c`'s lesson in a third instrument — key the probe on the property, not on the
bytes** — and it is not repaired here, deliberately. Choosing where an extension rule *would now*
go in a rewritten walk is choosing what `D1` measures, and `mg-20ee` is explicit that a moving
verdict is a finding and must not be absorbed into a refresh. Inventing `D1`'s new answer is
strictly worse than publishing that it has none.

**What the last transcript that ran said is not lost**, and is one command away:

    git show 60f68c7:code/species_extent_audit_6cb9/out_a3_differ.txt

That copy carries findings #5, #6, #7 and #8 of `README.md`. **They are unverified as of today**
and should be treated as claims about the tree of `e8fbd4f` until `a3` runs again.

## 4 — `selftest6cb9.py`: 2 of 33, and `run_all.sh` correctly refuses

    disarming RUN_FRAC makes e2 red (its own controls catch it)        ok
    and e2 is green again immediately after the restore                *** FAILED ***
    ...
    e2_crosssection.py exits 0 unmutated                               *** FAILED ***

Both are the same fact as §2: `e2_crosssection.py` is red on the tree as found. The second
failure is **not** a restore failure — `e2` is red before the probe and after it, and the
assertion beside it (`no __pycache__ survives the probe`) passes.

`run_all.sh` aborts here, by design, and the abort is right: assertion group 5 is titled *"the
checkers are green on the tree as found"* and it is the precondition every probe in this
directory depends on. **The four transcripts in this commit were therefore produced by running
the four scripts individually**, which is what `run_all.sh` would have done had it not stopped.
`run_all.sh` is not edited: a runner that refuses when its precondition fails is the behaviour,
not the bug.

## What this refresh does not do

* **`a3` is not repaired**, and `out_a3_differ.txt` is a traceback. See §3.
* **`e2_crosssection.py` and `code/species_extent_d633` are not touched.** That instrument's own
  staleness is `mg-20ee`'s, already recorded as `DIFFERS` in `code/asof_census_20ee/out_ground_truth.txt`.
* **Nothing here is pinned to an as-of commit.** `mg-6cb9`'s arms measure the *live* tree on
  purpose — that is what makes them able to see a repair — so pinning them would trade this
  finding away for a fixed point. What they lack is a *runner that re-takes them*, which is the
  census question, answered in `code/verdict_staleness_census_54b1/`.
