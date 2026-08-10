# mg-f8e5 — PREDICTIONS, committed BEFORE any script of this directory exists

This file is written and committed before `lib_f8e5.py`, `d1_five.py`,
`d2_unmeasured.py`, `d3_adopt.py`, `d4_movingref.py` or `selftest_f8e5.py`
exists in any tree. Nothing below is revised after the fact. Where a prediction
misses, the miss is kept in the README with the number that refuted it.

The ticket is a **disposal**, not a census: mg-1abe measured 398/112/31 and
named five false records, and this item disposes of the five individually,
accounts for the 31, adopts mg-1abe's proposed convention with a control, and
sweeps for the moving-ref defect mg-1abe disclosed in its own suite.

---

## 0. DISCLOSURES — measurements ALREADY IN HAND, not predictions

The arc's rule is that a measurement already taken is disclosed as a
measurement rather than laundered into a prediction. **This item's exposure is
LARGE and most of it is my own hand-work, not the dispatch's.**

**H1 — MY TICKET BODY PRINTS THE ANSWER.** The dispatch states 398/112/31, "the
damage is FIVE FALSE RECORDS", 649 of 6516 SHA sites, 66 distinct commits, 65
twins, the third bucket being ZERO over 234 pairs, and the own-defect (t1 at
`eacc5e1` vs t2 at `81214a9`). Every reproduction of any of those numbers is a
**FORMALITY** and is tagged as one. I did not discover them.

**H2 — I READ `code/transcript_census_1abe/README.md` IN FULL** before writing
this file, including its nine kept defects and its four missed predictions. No
definition, bucket name or grain below is a discovery.

**D1 — FOUR OF THE FIVE FALSE RECORDS HAVE ALREADY BEEN RE-RUN BY HAND**, in
detached worktrees at their carrying commits, before this file was committed. I
have seen the diffs. Specifically:

- `code/hodge_leverage_audit_f922/out_audit.txt` @ `553033a` — the re-run emits
  **one extra decision row**, `[ENLARGEMENT STATED] docs/OneThird-Hodge-Side-
  Leverage-Mg3c24Repair-IndependentAudit.md`, under a sentence that says "every
  site in the repository that states A5". Nothing else moves.
- `code/hash_population_6e58/out_p2_population.txt` @ `fe6a495` and
  `out_p3_unrestricted.txt` @ `fe6a495` — both go **`SELF-ERRORS: 0` →
  `SELF-ERRORS: 1`**, each from the producer's own tripwire ("counted and never
  read"), and their populations move (88486 → 93352 `ast.Call` nodes;
  `NEW SINCE THIS ADJUDICATION WAS WRITTEN : 0` → `5`).
- `code/audit_c067/out_c1_rebase.txt` @ `47e56b3` — `[CONFIRMED] C1a … 5
  commit(s) were REPLAYED` becomes **`[REFUTED] C1a … 0 commit(s)`**, because
  the pre-rebase commits hang off no ref at that commit and the script walks
  refs.

**D2 — I ALSO ALREADY MEASURED that all ten commits `out_c1_rebase.txt` names
still RESOLVE in this object store** (five off-`main`, five on it), so the
objects are present and only the refs are gone.

**D3 — `run_all.sh` OF `code/transcript_census_1abe/` ALREADY RESOLVES THE
REVISION ONCE** and passes it to every script; the fix landed in `a7d7fb9` with
the incident in the file's own header. Step 4's *confirm* half is therefore a
FORMALITY and only the *sweep* half is live.

**D4 — I already listed the file sets of the ten `NO-RUNNER` directories AS
THEY STAND ON `main`** (not at their carrying commits) and saw that three of
them carry a runner named `run_audit.sh` rather than `run_all.sh`, and that two
carry a `run_all.sh` on `main` today. P1 and P2 below are stated at the
CARRYING COMMIT, which I have not looked at.

**D5 — MY OWN FIRST RE-RUN OF `code/hodge_leverage_repair_ff3e` WAS KILLED
MID-MUTATION** by a two-minute tool timeout, leaving that worktree dirty in
four files; the second run then correctly REFUSED, and I mistook the refusal
for a census result for about one minute before checking `git status`. It is
disclosed here because it is exactly the failure this arc keeps committing —
reading an instrument's output without checking what state it ran against — and
because it means `repair_9207.py` cannot be safely interrupted.

---

## 1. THE FIVE FALSE RECORDS — DISPOSAL

**P1.1 (0.75) — at least 3 of the 5 have `re-run and re-commit` as the WRONG
remedy**, because re-running would overwrite a measurement that cannot be
re-taken or would produce a third answer that goes stale again immediately.
Scored by naming the remedy for each of the five with its reason.

**P1.2 (0.60) — for at least 1 of the 5, no remedy restores the assertion,
because the evidence it rests on is no longer reachable.** Named in advance as
the likely one: `code/audit_c067/out_c1_rebase.txt`.

**P1.3 (0.55) — for at least 3 of the 5, the transcript's own bytes already
name the revision it is a fact about**, so `annotate with the revision it is
actually a fact about` is a no-op on the content and a claim about the reader's
route to it. Scored by grepping each transcript for a resolvable sha and
checking it against the tree the re-run agrees with.

**P1.4 (0.35) — for at least 1 of the 5, there is an ancestor commit at which
the producer reproduces the committed bytes EXACTLY.** Put low: three of the
five read repository-global state, so the reproducing tree may be a state that
was never committed at all. This is the ticket's originating question — *which
revision is each figure a fact about* — asked as a search rather than as a
reading.

## 2. THE 31 UNMEASURED

**P2.1 (0.85) — at least 10 of the 31 are unmeasurable ONLY because the runner
is named something other than `run_all.sh`**, and become measurable by widening
one rule. (Exposed by D4 at `main`; predicted here at the carrying commit.)

**P2.2 (0.70) — at least 25 of the 31 have a producing script whose name maps
to the transcript by the arc's `out_<stem>.txt` ↔ `<stem>.py` convention or by
an `audit_<stem>.py` / `<stem>.py` variant**, at their carrying commits.

**P2.3 (0.50) — at least 1 of the 31 has NO producer at any commit** — a
transcript kept by hand, or produced by a script that was never committed. That
one is genuinely unmeasurable and stays so.

**P2.4 (0.30) — running the recovered producers, at least 5 of the 31
REPRODUCE byte-for-byte.** Put low because the base rate in the arc is 78% for
suites *with* runners, and a directory that never had a runner is likely to be
older, smaller and more repository-coupled.

## 3. THE CONVENTION

**P3.1 (0.90) — adopting R1/R2/R3 in this directory will be green at its own
publishing step**, i.e. every transcript here declares a `code-digest:` equal
to the digest recomputed from the tree at the commit carrying it. mg-1abe
already showed this survives its own publishing step; the live risk is that
mine does not because I add a script after the transcripts are written.

**P3.2 (0.65) — the checkable control will be RED somewhere on `main` the first
time it is run over more than one directory**, because coverage is 0 of 541 and
any directory that has not adopted must be reported as UNDECLARED rather than
as passing. A control whose only possible answer is green is the failure
mg-1abe scored as its own P5.2 MISS, and I am predicting I avoid it by counting
UNDECLARED as a finding rather than as silence.

**P3.3 (0.55) — R2 (`reads-outside-tree:`) can be made CHECKABLE without a
`git`-intercepting harness**, by a static test over the producer's own source
that agrees with the author's declaration at 100% of adopters. mg-1abe declared
this "worth building and not built here". If the static test disagrees with any
declaration, the prediction is scored MISSED even if the disagreement is the
declaration's fault.

## 4. THE MOVING-REF SWEEP

**P4.1 (0.80) — at least 20 suites under `code/` have the moving-ref shape**:
two or more scripts driven by one runner, each independently resolving a moving
ref (`main`, `HEAD`, `origin/main`, or an unpinned `git log`), with no resolved
revision passed down from the runner.

**P4.2 (0.45) — at least 1 suite can be shown to have ALREADY been bitten**,
i.e. two of its committed transcripts print different `as-of`-style revisions or
different values for the same repository-wide count. This is the difference
between "the shape is present" and "the shape fired", and only the second is
damage.

**P4.3 (0.25) — the sweep finds the shape in a suite whose runner LOOKS like it
resolves once** — a single `git rev-parse` in the runner that is then not passed
to every script, or passed to some and not others. Put low; it is the
interesting case if it lands.

## 5. ERRORS OF MY OWN, FILED IN ADVANCE

**E1 — I re-run a suite that mutates the working tree and read the result
without checking the tree was clean first.** Already committed once (D5). The
guard: every re-run in `d1` must assert a clean worktree BEFORE and restore
AFTER, and record the assertion in the transcript.

**E2 — I report a FLIP as damage when the re-run is what is wrong.** `c067` is
the live case: its instrument sees fewer commits than it did, because refs were
deleted, not because history changed. If I print "5 false records" without
splitting THE RECORD IS FALSE from THE RE-RUN CANNOT SEE WHAT THE RECORD SAW, I
have committed the over-report this whole ticket exists to prevent.

**E3 — I answer "can it be made measurable?" by asserting a producer rather
than running it.** A filename that maps is not a producer that reproduces. The
guard: `d2` must EXECUTE every producer it recovers and report the bytes, and
must count a recovered-but-not-run producer in its own bucket.

**E4 — I adopt the convention in my own directory and call that adoption.**
Coverage of 1 directory out of 116 is coverage of 1 directory, and if my README
says "adopted" without the denominator it is the same sentence mg-1abe scored
as its own P5.2 miss.

**E5 — my moving-ref detector over-collects.** mg-1abe's `t6` over-collected by
32× on exactly this kind of textual shape. If every suite that calls `git`
anywhere counts as having the defect, the detector's population is not what its
name says. The guard: the finding requires ≥2 scripts AND a runner that passes
no revision, and the transcript must print the rejected near-misses.

**E6 — I strike or rewrite a committed transcript belonging to another
ticket.** mg-1abe's rule is that a transcript that does not reproduce is a
MEASUREMENT and overwriting it destroys it. My deliverable is a disposal
*record*, not an edit to those five files. If I edit one, I have destroyed the
only evidence of the damage I was sent to describe.

**E7 — I confirm the `run_all.sh` fix by reading the file I am standing in.**
`a7d7fb9` must be shown to be an ancestor of `main`, not merely present in my
worktree, or the confirmation is about my branch and not about the repository.

**E8 — the sweep's own suite has the shape it hunts.** `run_all.sh` here must
resolve the revision once and pass it down, and `d4` must include its own
directory in its population rather than exempting it.

**E9 — I publish a count over "the five" that is really a count over four.**
`ff3e`'s re-run had not completed when this file was committed. If it comes back
`REPRODUCES` — i.e. the census's FLIP does not replay for me — that is a
finding about the census and it must be printed as one, not quietly dropped to
keep the number at five.
