# mg-4700 — OUTCOMES

Scores `PREDICTIONS.md`, which was written before any probe ran and has not been
edited. Two predictions missed. Both are kept as written and both are below.

---

## The predictions that missed

### D2b — I predicted `s1_extent.py` would be SILENT on a symlinked directory; it exits 1

**Predicted:** exit 0.  **Got:** exit 1.

And the miss is the sharper result, which is why it is worth the space. The
checker's **scan** is exactly as blind as I predicted — its own S1b line reads
`0 statement-occurrence(s) still asserted at source` and its own extent line
reads `18 file(s) read, 0 of them below the tree root`, with a forbidden
statement sitting one symlink inside that tree. What exits 1 is control (c),
which `shutil.copytree`s the tree into a scratch directory to test that an
injected statement raises the count. `copytree` defaults to `symlinks=False`,
so it **follows** the link and materialises the planted file as a real one in
the copy — where the same scan, now walking a real directory, finds it. The
control expected `now + 1` and got `now + 2`.

So the exit code is right for a reason that has nothing to do with the extent,
and the **diagnosis a reader is handed is wrong**: the run says the injection
control failed. Nothing in it says a forbidden statement is live in
`code/species_7d75`. I had not thought of `copytree` following links, and a
prediction of "silent" that turns into "loud for the wrong reason" is a better
outcome for the reader than the one I expected — but only because the probe
printed all three numbers instead of the exit code alone.

### D5b — I predicted `A2 TOTAL BAD 1`; it is 2

**Predicted:** 1, the row being R29, per `41ac5d4`'s own commit message.
**Got:** 2. The second row is `the committed CENSUS is right for the shipped
tree *** WRONG ***`. Developed in F3 below. I took a commit message's figure as
my prediction and it was true where it was measured and false where it shipped,
which is the finding.

### D1i — the number was right and my reasoning was wrong, and that is not a hit

I predicted exit 1 for reverting `e1_extents.py`'s **own** walk, and wrote in
`PREDICTIONS.md` that I expected to be wrong: my reasoning was that E1's
expectation would shrink to match a subject that still recursed, `want <= got`
would still hold, and E1 would go quiet. E1 exits 1 — but through a different
row than the one I was reasoning about (`the printed file count agrees with what
was read`, not `reads every regular file`). The scoreboard counts this as a hit
because the exit code matched. It is recorded here because a prediction that
lands on the right number by the wrong route is worth less than the tally makes
it look, and Q1c scores only the two SUBJECT walks for that reason.

---

## Findings

### F1 — MAJOR. The F1 shape survives the repair, one directory rule to the side

`q1_depth.py` Q1d. The repaired extent reads *EVERY REGULAR FILE … AT ANY DEPTH*
and names exactly one directory rule, `__pycache__`. `os.walk` does not descend
into a **symlinked directory** unless `followlinks=True`, and none of the three
walks passes it; the link is classified into `dirnames`, so it is never a
candidate file either. Measured, with a statement planted behind a link:

| checker | exit | what it says |
|---------|------|--------------|
| `w3_scope.py` | 0 | silent |
| `s1_extent.py` | 1 | but its scan read 18 files, **0 below the root**, 0 asserted — see D2b above |
| `e1_extents.py` | 0 | **certifies the extent as TRUE** |

`e1_extents.py` is the file whose whole job is deciding whether a printed extent
is true, and it walks the same way, so it cannot disagree — which is word for
word the sentence mg-821e wrote about `os.listdir`, with `followlinks` in place
of recursion. The rule is precisely *symlinked **directory***: D2d shows a
symlink to a **file** is read, because `os.path.isfile` follows it. None of the
three printed extents contains the word `symlink` (D2e, 0 of 3).

This is not a claim that the repair failed. The condition mg-6cb9 named is
removed and removed properly — D1a–D1d catch a statement at depth 1, at depth 3,
and in a tree mg-6cb9 never planted in. What survives is the **class**: an extent
sentence complete about the rule somebody thought of, and silent about the state
of the world it still assumes.

### F2 — MAJOR. The deletion test was run at a unit two of whose parts have no return

`q2_wiring.py` Q2c. mg-821e deletion-tests the wiring as **one 20-line unit**. It
has three separable parts and each was deleted alone here:

* **the `|| { … exit 1; }` guard, removed alone**, with B1 restored on disk:
  all three runners still exit 1 (D3e, 3 of 3). Under `set -e` a failed command
  substitution in an assignment already aborts the script. The guard moves the
  **message**, not the **verdict**; five of the block's twenty lines are inert
  under the test that was applied to the block as a whole.
* **the two `echo`s that print the check's output, removed alone**: all three
  runners exit 0 with **no trace that the check ran** (D3f, 3 of 3). The
  sentence that distinguishes this repair from the state mg-6cb9 found — *a call
  present in a script is not evidence of execution, so the OUTPUT is printed* —
  is itself guarded by nothing. No self-test and no checker asserts those two
  lines exist.

The call itself is load-bearing and was correctly identified. The claim that is
not supported is that the unit deletion-tested is the unit that has a return.

### F3 — MAJOR. The committed census is 8 short, and `A2 TOTAL BAD` is 2, not 1

`q4_standing.py` Q4b2 and Q4d. Counting `*.md` under `docs/` and `code/` from
`git` alone:

| commit | what it is | transcript claims | tree holds | short |
|--------|-----------|-------------------|-----------|-------|
| `e8fbd4f` | mg-d633 wrote it | 100 | 105 | 5 |
| `af432ee` | **mg-821e regenerated it** | 123 | 131 | 8 |
| `HEAD` | the tree it ships in | 123 | 131 | 8 |

mg-6cb9 raised this against mg-d633's transcript. `af432ee` regenerated the file
and **the gap widened**. mg-821e's own published transcript records the run that
produced 123 as having seen `git ls-tree HEAD -- 123`, a tree no commit in this
history has, and 34 of its 129 lines no longer reproduce.

**Why, and it matters that the repair did the right thing by the rule it was
given.** `b534db7` exists solely to obey this arc's Appendix A — *A COMMIT THAT
MEASURES SOMETHING IT ALSO MODIFIES MUST PUBLISH THE POST-COMMIT MEASUREMENT* —
and it did: it re-ran a2 with the repair landed and both F4 rows turned `ok`.
Then the work was **rebased** onto a main that had grown by eight markdown files
while the ticket was open, and the artifact regenerated against the pre-rebase
HEAD shipped inside a different tree. **Post-commit is not post-merge.** The rule
as written names a condition — *the commit* — that a merge queue is free to
change underneath it, and nothing re-checks it afterwards.

That is this repair's own OPEN 1 one level out and in its evidence rather than
its code: a measurement true because of a state of the world nobody stated.
There it was *no tree has a subdirectory*; here it is *main has not moved since I
ran this*. mg-821e removed the first by construction. The second is stated
nowhere and has now gone false twice in the same file.

**Not affected:** e2's verdict. A live run at HEAD reports 0 standing, Q2a
printed exactly that from inside all three runners, and none of the 8 unread
files carries a strike. What is false is an **extent line on a committed
transcript**, which is the kind of claim this arc exists to take seriously.

### F4 — MINOR. `| tee` still swallows a red self-test in two of the three repaired runners

`q2_wiring.py` Q2e. `41ac5d4` fixed this in mg-821e's own runner and its message
says *"Every other run_all.sh in this arc still uses `| tee`; noted, not
touched."* Measured rather than taken on the message's word, with each
self-test forced red:

| runner | exit | printed `*** FAILED ***` | |
|--------|------|--------------------------|-|
| `species_repair_a4ef` | 0 | yes | **swallowed** |
| `species_remainder_f8fa` | 0 | yes | **swallowed** |
| `species_repair_6f61` | 1 | no | stopped the run |

Two of the three files this repair opened — it added twenty lines to each — still
carry it. The class is repo-wide: 10 `run_all.sh` pipe a self-test through `tee`.
It is MINOR because it is disclosed, and it is a finding because disclosure in a
commit message is not a guard.

### F5 — MINOR, reported and not scored. A crash is reported as a specific finding

`q2_wiring.py` Q2d. The guard prints `E2 CROSS-SECTION FAILED -- a struck claim
stands un-struck elsewhere`, which is the one thing `e2` exits 1 for; the `||`
reaches it for any non-zero exit. With `e2` made to raise, all three runners exit
1, all three print that sentence, and none prints a `STANDING UN-STRUCK` line —
stderr is not captured into `$E2OUT`, so the traceback goes to the terminal while
the summary asserts a finding that was never made. Not scored: the run does go
red, so it is a wrong message and not a missing verdict.

---

## What is confirmed, and was not disturbed

* **OPEN 3 is closed cleanly.** 7 of 7 one-site deletions fire with every other
  copy left standing — including `mg-a61f` with 17 copies still in the file —
  against **2 of 7** for the checker at the pinned pre-repair ref. The other
  direction holds: a copy deleted at a non-site is silent, an emptied section 10
  fires, and a renamed heading fires loudly with `NO SUCH SECTION`.
* **OPEN 1's walks recurse.** Depth 1, depth 3, and a tree mg-6cb9 never planted
  in all catch the statement; `__pycache__` is still skipped and still named.
* **OPEN 2's check executes.** 3 of 3 runners print `E2 TOTAL BAD: 0` from the
  check's own stdout; with B1 restored, 3 of 3 go red **and** 3 of 3 are green
  with the wiring removed, so the red is attributable. `unwire()` of each runner
  is byte-identical to the pinned pre-repair file, so "a pure addition" is
  measured.
* **The four extents are still measured both ways.** mg-6cb9's `a1_bothways.py`,
  run unmodified: `A1 TOTAL BAD: 0`, and mg-821e's published transcript of it is
  **byte-identical, 178 of 178 lines**, to the live run.
* **The cross-section check still fires three ways in two documents.**
  `a2_crosssection.py`, run unmodified, still reports `the species trees'
  run_all.sh reach it 3 of 3 ok`.

Nothing above was weakened. The mathematics was not touched.

---

## Five defects in this instrument, kept

1. **The working directory.** An early `cd` into this directory persisted across
   later shell commands, and `ls code/species_repair_6f61/` came back *No such
   file or directory* — which read for a moment as a probe having deleted a tree.
   It had not; `git status` was clean. Every path in the instrument is absolute
   or `REPO`-relative for this reason.
2. **The pin assertion was too coarse and failed against a correct pin.**
   `selftest4700.py` asserted `"os.walk" not in` the pre-repair
   `e1_extents.py` — but that file already walked `docs/` and `code/` for its
   markdown sweep before the repair. The assertion was wrong, not the pin, and
   the tempting fix was to weaken it. It is now the **one call** each repair
   changed, per file, plus the matching `os.listdir` in the same direction.
3. **This instrument perturbs the measurement it takes.** Its own markdown files
   are under `code/`, and `e2_crosssection.py` reads every `*.md` under `code/`,
   so the live file count in Q4c is higher than the shipped tree's by exactly
   the number of markdown files here. Declared in the run. Q4d counts from `git`
   at four named commits and is immune.
4. **The first D2 probe would have measured nothing.** Planting the hidden
   directory *inside* the tree and symlinking to it from the same tree makes the
   file reachable by the ordinary walk, and the probe would have reported the
   checker seeing it. The target directory is created outside the repository.
5. **A prediction was right for the wrong reason and the tally cannot see it.**
   D1i, above. Q1c scores only the two subject walks as a result.

## Extent of this audit

Four sections over one repair. It covers the three OPEN items mg-6cb9 left and
the two findings it confirmed, by planting files, executing runners, and running
mg-6cb9's own battery unmodified. It says **nothing** about the mathematics of
the species tree, nothing about mg-6cb9's `a3_differ_and_placement.py`, nothing
about `e2_crosssection.py`'s own correctness (mg-d633 and mg-6cb9 measured that),
and nothing about any tree outside `code/species_7d75`,
`code/species_repair_a4ef`, `code/species_remainder_f8fa`,
`code/species_repair_6f61` and `code/species_extent_d633`. `Q1..Q4 TOTAL BAD`
counts probes whose **outcome** was wrong; `PREDICTIONS MISSED` counts
**predictions** that were wrong, and the two are separate on purpose.
