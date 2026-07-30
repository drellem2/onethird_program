# mg-821e — what happened, including this instrument's own defects

**3 of the predictions in `PREDICTIONS.md` were wrong and are kept as written.** Seven defects in
this instrument are recorded below; **three of them made a measurement read as its own
opposite**, and **three are the same classes of defect this ticket exists to repair** — a check
resting on an unstated condition, a control that exists and does nothing, and a comparison that
silently stops comparing.

---

## The result

| open item | closed by | measured |
|---|---|---|
| **OPEN 1** — extent true only because no tree had a subdirectory | all three walks recurse; one directory rule (`__pycache__`) left and **printed** | P1: 18 probes, 5 of 5 IN fire, 4 of 4 OUT silent, 2 of 2 deletion tests go silent again, 4 of 4 guards |
| **OPEN 2** — the check closing B1 called by 0 of 3 runners | **removal question asked first** (outcome 2, measured), then wired into all three | P3: 3 of 3 runners print the check's output; with B1 restored on disk, 3 of 3 catch it **wired** and 3 of 3 are green **unwired** |
| **OPEN 3** — C4 a presence test | seven (site, anchor) pairs, each checked in its own heading region | P2: **2 of 7** fire at HEAD, **7 of 7** fire now; 3 of 3 non-site mutations silent |

**Nothing retreated. 0 mathematics disturbed.**

---

## 1. A prediction that missed, and the reason is better than the prediction

**P3a (2)** applies candidate removal (a) — delete every strike marker in the target document, keep the
text, and put B1 back — and asks what `e2_crosssection.py` says. I predicted **exit 0**: the
sweep would find nothing standing, because there are no strikes left to compare against, and
that is the whole point.

The sweep did report **0 standing**, and the exit was **1**. The failure is e2's own **control
(a)**, which restores B1 by *reversing* §0's repair. With the strikes deleted, the paragraph it
reverses into is gone, so the control prints *the control cannot run* and books itself as failed.

**The detector reports ITSELF broken instead of reporting the false belief.** That sharpens the
conclusion rather than softening it: removal (a) takes out the detector and the evidence in one
move. The prediction is kept and the measurement in P3a was re-pointed at the sweep's own rows —
`0 standing` — rather than at the exit code, with the miss printed in the run.

## 2. A deletion test that broke the thing it was deleting from

`unwire()` removes the wiring block from a runner. Its first version cut from the marker comment
to the **first** line mentioning `$E2OUT` — but the block contains two, and the first is inside
the failure branch. The cut left a dangling `}` behind.

Every unwired runner then exited **1 for a shell syntax error**, and P3b's `unwired` column read
*the check's output is gone* — which was true, and true because **the script was gone**, not
because the wiring was. P3c's `unwired (before)` column read exit 1 on all three, which would
have said mg-6cb9's F2 was not reproducible.

**A deletion test that breaks the thing it deletes from measures nothing.** Fixed to cut to the
**last** such line, and the self-test now asserts the strong form: `unwire(runner)` is
**byte-identical to `git show HEAD:`** for all three, so *the wiring is a pure addition* is a
measurement and not a claim.

## 3. `git sees it` — a check that could not fail, twice, for two different reasons

The self-test asserts that a `Probe` mutation is visible to git before asserting that the restore
puts it back. It could not fail:

1. **First version** probed `kern821e.py` — this instrument's own source, in an **untracked
   directory**. `git status --porcelain` reports an untracked directory as one `??` line whatever
   is inside it, so the status before and after were equal. A check that cannot fail, inside the
   self-test of an instrument auditing checks that cannot fail.
2. **Second version** probed a tracked file — `s1_extent.py`, which **this ticket has already
   modified**. Porcelain reads ` M code/…` before the probe and ` M code/…` after it, so it was
   *still* equal.

The second one is the serious half, because it is not only the self-test: **every probe in this
instrument used `git status --porcelain` as its restore contract**, and every probe runs against
a worktree where four files are modified. A probe that mutated one of those and failed to restore
it would have compared **equal** and the run would have continued. `git_status()` now returns
porcelain **and the full `git diff`**, which is byte-level for tracked files, with porcelain still
covering the untracked ones the probes create.

## 4. Killing the harness leaves the mutation on disk

While debugging, I killed a run that was inside a `Probe`. The restore is in the process, so the
target document was left carrying **B1** and one runner was left **unwired** — the exact two
mutations the instrument plants. `git status` showed the document as modified and the runner's
diff was one blank line, which is easy to read past.

Not a defect in the probes and not fixable inside them; it is a property of mutating the real
worktree, which mg-6cb9 chose deliberately and for a good reason. It is now stated in
`run_all.sh` and in the README: **do not kill this instrument mid-probe, and if you do, check
`git diff` before believing the tree.**

## 5. Re-wrapping a sentence silenced a check in mg-6cb9's instrument

`w3_scope.py`'s extent line gained *AT ANY DEPTH*, and the sentence was re-wrapped to fit. That
split the contiguous phrase **`every regular file in it`** across two `print` calls — and
mg-6cb9's `A1g`, which asks whether the committed output *says* the repair widened the code, looks
for exactly that phrase. It went `*** SILENT ***` against a file that now says so more loudly
than before, and `A1 TOTAL BAD` went 0 → 1.

Nothing here is a false statement; the label check is right to be string-anchored, because that
is what makes it an observation instead of a promise. **The artifact is what moves.** The line is
now one line on purpose, with a comment saying why, and `A1 TOTAL BAD` is back to 0.

**This is the argument for re-running the auditor's instrument rather than quoting it.** No probe
of mine would have caught it: my probes ask whether the checkers fire in the right places, and
this was a check in somebody else's tree reading a string in a committed transcript.

## 6. Two comparisons anchored to `HEAD` — and `HEAD` became the repair

`p2_sites.py` ran `check_doc.py` "as committed at `HEAD`" and the self-test asserted
`unwire(runner) == git show HEAD:`. Both were correct, and both were correct **only while HEAD
did not contain this work**. The moment the repair was committed, `p2_sites.py` reported the old
checker firing **7 of 7** — which reads as *the finding never existed* — and the self-test
reported the wiring **absent** from three runners that carry it.

Neither failed loudly at the right time. **A comparison against `HEAD` does not break when the
repair lands; it silently changes what it is comparing, and starts measuring the repair against
itself.** That is this ticket's own OPEN 1 one level out: a check whose meaning rests on a
condition nobody stated — *HEAD does not contain this work* — and the condition went false in the
ordinary course of doing the work.

Both are now pinned to `PRE_REPAIR = b6bc2ef`, the commit this branch left from, the way
`s1_extent.py` pins `ebecd89` and `83ac472`. Both call sites also assert that the pinned ref does
**not** already carry the repair, so a pin later moved onto a repaired commit is a loud failure
rather than a quiet 7 of 7.

**It was caught by running the whole tree again after committing**, which is the only reason it
is in this file rather than in the next audit.

## 7. A failing self-test that did not stop the run

`run_all.sh` had `python3 -B selftest821e.py | tee out_selftest.txt`. Under `set -e` a pipeline's
status is the **last** command's, and `tee` always exits 0 — so when defect 6 turned the
self-test red, the runner printed six `*** FAILED ***` lines and **exited 0**.

**A control that exists, is correct, and does nothing** — which is the exact shape of OPEN 2,
committed by the runner of the instrument repairing it. Fixed to redirect and guard on the exit
code. Every other `run_all.sh` in this arc still uses `| tee`; that is noted and not touched.

---

## What this instrument does not cover

* **Depth is tested to two levels** and to an extensionless file. Symlinks, unreadable
  directories and device nodes are not tested and are not claimed.
* **P2 says nothing about whether the five anchors are the RIGHT five.** It measures that each is
  checked where a reader meets it. Choosing the anchors is `check_doc.py`'s business and this
  ticket did not revisit it.
* **P3's removal question is answered for ONE generator** — a claim struck at one site of a
  document standing un-struck at another site of the same document. e2's own extent line names
  two holes it does not close (another document; a restatement in different words) and this
  ticket does not close them either.
* **`e2` is wired into the three species runners and no others.** Every other tree in this
  repository that carries a document with a strike is still not running it, and that is a much
  larger wiring question than mg-6cb9's F2 asked.
* **Reachable is still not read.** P3 measures that the check executes. Whether anyone reads its
  output is not measurable here.
