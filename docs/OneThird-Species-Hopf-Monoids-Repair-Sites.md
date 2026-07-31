# Repair of mg-6cb9's three OPEN items — a contingent extent made true by construction, a check that now runs, and an anchor checked where a reader meets it

**Work item:** mg-821e. **Date:** 2026-07-31.
**Repairs:** `docs/OneThird-Species-Hopf-Monoids-ExtentRepair-IndependentAudit.md` (mg-6cb9,
`26c8d5c`), which audited mg-d633 / `e8fbd4f`.
**Instrument:** `code/species_sites_821e/`, 5 Python files, 89-assertion self-test.
`sh run_all.sh`, ~4 minutes, **no network**.

---

## 0. VERDICT

**All three OPEN items are closed, by three separate changes to three separate files, each with
its own deletion test.** mg-6cb9's standing note asked for exactly that: *three findings, three
different grains, not variations of one bug and not to be closed with one fix.*

| open | what it was | what was done | the measurement |
|---|---|---|---|
| **1** | *"EVERY REGULAR FILE in each tree is read"* was true **only because no tree had a subdirectory** — a claim measured, true, and contingent on a condition nobody stated | **the walks recurse.** `s1_extent.py`, `w3_scope.py` and `e1_extents.py` all use `os.walk`. One directory rule is left, `__pycache__`, and it is **printed in the extent line** | 18 probes. **5 of 5** inside fire, **4 of 4** outside silent, **2 of 2** deletion tests go silent again, **4 of 4** guards |
| **2** | the check closing B1 was **called by 0 of 3** species runners — present in the tree, absent from every run | **the removal question was asked first** and answered with measurements (**outcome 2**), then the check was wired into all three and **verified by running them** | **3 of 3** runners print the check's own output. With B1 restored on disk, **3 of 3 catch it wired** and **3 of 3 are green unwired** |
| **3** | C4 was a **presence test** over a document that writes 3 of its 5 anchors more than once — deleting the copy a reader meets left the run green | **seven (site, anchor) pairs**, each checked in the heading region a reader meets it in; multiplicity elsewhere is printed and has no vote | **2 of 7** fire against the checker as it stood before this ticket; **7 of 7** fire now. **3 of 3** non-site mutations stay silent |

**And the strongest evidence is not mine.** mg-6cb9's own `a1_bothways.py`, **unmodified**, re-run
against the repaired tree: `A1 TOTAL BAD` **1 → 0**; **Q2** — the prediction that *was* finding F3
— goes from `*** MISSED ***` to `as predicted`; **Q10** and **Q17** go from exit 0 to exit 1,
`extent TRUE here`. Its `a2_crosssection.py`, unmodified, now reads **`the species trees'
run_all.sh reach it — 3 of 3 ok`** where it read `0 of 3`. Transcripts are committed as
`code/species_sites_821e/out_a1_6cb9_after.txt` and `out_a2_6cb9_after.txt`, produced with `git
diff` compared before and after so the tree they measure is the tree that ships.

**One row of mg-6cb9's table will still print red and it is not a surviving defect.** §4 below
says which, why, and what measurement separates the two readings.

**Nothing retreated. 0 mathematics disturbed. 3 of this instrument's own predictions were wrong
and are kept as written, and 7 defects in this instrument are recorded** (`OUTCOMES.md`) — **three
of them the very classes this ticket repairs**, committed by the instrument repairing them: a
comparison anchored to `HEAD` that stopped comparing the moment the repair landed (both such
comparisons are now pinned to `b6bc2ef`, with an assertion that the pin does not already carry
the repair); a self-test piped through `tee`, so a red self-test left the runner exiting 0; and a
`git status --porcelain` restore contract that could not see a probe fail to restore an
already-modified file.

---

## 1. OPEN 1 — the condition was removed rather than stated

mg-6cb9 named the flavour and it is worth keeping: **a claim that is measured, true, and
contingent on a condition nobody stated.** Not wrong, not asserted-without-measurement. The
sentence *"EVERY REGULAR FILE in each tree is read — there is no extension rule"* was true on
2026-07-30 for exactly one reason: no tree under `code/species_*` contained a directory. Both
scans were a single `os.listdir` and a `continue` past anything that is not `os.path.isfile`, so
a directory was dropped **by a rule no sentence carried** — word for word the defect mg-d633
removed one layer up.

**The brief offered two repairs and this took the first.** *Either make the walk actually recurse,
so the claim is true by construction, or state the condition in the extent.* Stating it would
have left the repository carrying a promise — *no subdirectories present* — that nothing in it
can keep, and the day somebody added a directory the failure would have been a person not
noticing a sentence. All three walks now recurse.

**One directory rule survives and it is carried by a sentence.** `__pycache__` is not descended
into: it holds bytecode the runs write themselves, it is not authored, and its contents vary with
the interpreter. That rule is printed in both extent lines and probe **P6** is what shows it is
real. mg-6cb9's finding was never that a rule existed — it was that the rule was in the code and
in no sentence.

**`e1_extents.py` had the same blind spot and that is the part that made it MAJOR.** The file
whose whole job is deciding whether a printed extent is true listed the tree the same way, so it
certified the sentence over a file it also could not see. An instrument that computes its
expectation the way the subject computes its answer cannot disagree with the subject. It walks
now, and the walk is written out in full rather than imported from either scan, so if one of them
widens or narrows the rule, E1's expectation does **not** move with it.

### 1.1 The probes, and what each is for

| id | dir | site | exit |
|---|---|---|---|
| P1 | IN | X4 one level down, `species_7d75/sub/leak.md` — **mg-6cb9's Q10, which exited 0** | **1** |
| P2 | IN | X3 in the same place — **mg-6cb9's Q17, which exited 0** | **1** |
| P3 | IN | X1 **two** levels down, in a different tree | **1** |
| P4 | IN | X1 in an **extensionless** file in a subdirectory — both removed rules at once | **1** |
| P5 | IN | X1 in `sub/PREDICTIONS.md` — the named exclusion is a **path**, not a basename | **1** |
| P6 | OUT | X1 under `__pycache__` — the one stated directory rule | **0** |
| P7 | OUT | a subdirectory of a tree `s1_extent.py` **disclaims** | **0** |
| P8 | OUT | a subdirectory of a tree `w3_scope.py` does not name | **0** |
| P9 | OUT | a **named exclusion at the root**, still excluded | **0** |
| P10, P11 | DEL | P1 and P2 again, with **one line** removed | **0, 0** |
| P12, P13 | GUARD | a subdirectory planted and one walk put back to non-recursive — E1 must **catch** it | **1, 1** |
| P14 | GUARD | a subdirectory planted, everything recursing — nothing is false | **0** |
| P15 | GUARD | **E1's own** descent line removed | **1** |

**The deletion test declares the unit it removes,** which is mg-9220's rule: one line per site,
the line telling `os.walk` which directories to descend into, set to `[]`. Nothing else changes.
P10 and P11 put the finding back exactly as mg-6cb9 measured it.

**P5 decided a reading rather than confirming one.** `EXCLUDE` names five files and the run
prints them root-relative. Matching on the basename would silently make a printed list mean more
than it says — `sub/PREDICTIONS.md` dropped by a name the reader only ever sees attached to the
root. It matches the path, and P5 is the probe that says so.

---

## 2. OPEN 2 — the removal question, asked before the wire

The amendment is explicit: **do not wire it as the first move.** A check called by zero callers is
the cheapest possible moment to ask whether it should exist at all, because nothing depends on it
yet, and wiring it creates dependents. So the question was asked first, and it is answered in the
run itself — `p3_wiring.py` section **P3a** — not only here.

> **Can whatever makes B1 breakable be removed, so that no check is needed?**

**The generator, stated so that it can be argued with:** a claim struck at one site of a document
can stand un-struck at another site of the same document, because striking is per **occurrence**
and a document may state one claim in more than one place.

**(1) Is it live?** 14 documents carry a strike, 33 strikes are measured, and e2's own control
(a) restores B1 and fires. **Live.**

**(2) Removal (a) — stop marking.** Delete every strike marker in the target document, keep the
text, and put B1 back. The document's 11 strikes go to 0, the repo-wide count goes 33 → 22, and
**the sweep reports 0 standing while the false belief is still sitting in §0**. Removal (a) does
not make the class impossible; it makes it **invisible**. *(This is where a prediction missed: I
wrote exit 0 and the exit is 1 — not the sweep, but e2's control (a), which restores B1 by
reversing §0's repair and can no longer find the paragraph to reverse. The detector reports
**itself** broken instead of reporting the false belief, which sharpens the conclusion: removal
(a) takes out the detector and the evidence in one move. The prediction is kept.)* **REJECTED,
measured.**

**(3) Removal (b) — forbid restatement.** One copy per claim, so a strike has nothing to compare
against. **3 of the 33 strikes are exonerated**: the claim *is* restated, and legitimately —
quoted back in order to correct it. **A rule that forbids restating a struck claim forbids
correcting one.** And there is no generator to delete: these are markdown files written by hand.
**REJECTED, measured.**

**(4) Has B1 been closed for another reason?** No. §3 below restores it on disk and the three
runners are green without the wiring.

### **OUTCOME 2. The generator is not removable, so the check is wired — and here is why removal was rejected, so that nobody re-asks.**

Removal (a) converts a detectable defect into an undetectable one; removal (b) forbids the
correction of a struck claim. If either measurement stops holding, the question is open again,
and P3a re-measures both on every run rather than quoting this paragraph.

### 2.1 Wired, and verified by running

The block added to each of the three runners calls `e2_crosssection.py`, **fails the run on a
non-zero exit**, and **prints the check's own output**. Presence in a script is not evidence of
execution — a guarded branch, an early exit or a swallowed error all leave the line in place — so
the measurement is the runner's stdout:

```
cross-section check (mg-821e), its own output:
  14 file(s) carry a strike, 33 strike(s) measured, 0 standing.
E2 TOTAL BAD: 0
```

**3 of 3.** And the deletion test: remove the block — one unit, 20 lines, counted from the patch —
and the output disappears from all three runs, with each runner still exiting 0. The self-test
asserts the strong form: `unwire(runner)` is **byte-identical to `git show b6bc2ef:`** for all three,
so *the wiring is a pure addition* is a measurement rather than a claim.

`code/species_extent_d633/run_all.sh` already called the check and was **not** given a second
copy.

---

## 3. B1 itself, restored on disk, against all three runners

§0's paragraph is reversed back to the misquotation it carried from `83ac472` until mg-d633 —
reversed, not spliced next to, because an occurrence sitting in the paragraph that corrects it is
exonerated and correctly so. Each runner is then run twice:

| runner | wired (now) | unwired (the state mg-6cb9 measured) |
|---|---|---|
| `code/species_repair_6f61` | exit 1, **CAUGHT** | exit 0, green |
| `code/species_remainder_f8fa` | exit 1, **CAUGHT** | exit 0, green |
| `code/species_repair_a4ef` | exit 1, **CAUGHT** | exit 0, green |

**That is the whole of OPEN 2 in one table.** The right-hand column is the historical failure
reproduced — three runners green while B1 stands, every per-section checker true — and the
left-hand column is it closed. The artifact was present and the behaviour was absent; the
behaviour is now in the run, and §2.1's deletion test shows the wiring is what put it there.

---

## 4. OPEN 3 — the anchor is checked where a reader meets it

C4 was `flat(s) in flat(rep)`: a presence test over the whole repair document. Three of its five
anchors occur more than once in that file — `mg-a61f` **19** times, `code/species_repair_6f61`
**twice**, `2 of 45` **three** times — so for three of five it was a check on **no site**.

**Which of the three remedies, and why.** The brief ranks them: one copy; failing that, derive the
others from it; failing that, check at the reader-facing site.

* **One copy is not available**, and not for want of effort. `mg-a61f` is a ticket id in running
  prose, and a repair document that names the audit it answers exactly once is a worse document.
* **Deriving is not available.** These are markdown files, there is no generator, and inventing
  one to hold a ticket id would be a new machine to keep alive.
* **So it is the third remedy, done properly.** Seven `(site, anchor)` pairs, each checked in the
  heading region a reader meets it in. Two anchors are checked at **two** sites, because both are
  reader-facing and neither is the other's copy: the front matter tells a reader what the
  instrument is; §11 is the command a reader runs.

| anchor | copies | declared site(s) | delete that copy — before | now |
|---|---|---|---|---|
| names its target | 1 | front matter | 1 | **1** |
| names the audit | **19** | front matter | **0** | **1** |
| names the instrument | **2** | front matter; §11 REPRODUCE | **0**, **0** | **1**, **1** |
| records `2 of 45` | **3** | §2.1; §11 REPRODUCE | **0**, **0** | **1**, **1** |
| records what it did NOT repair | 1 | §10's heading | 1 | **1** |

**2 of 7 before the repair; 7 of 7 now.** The copy counts are printed in the run because they are the
reason: **an anchor with 19 copies was the least covered of the five.**

**And it is wrong in the other direction too, or it would just be a stricter presence test.**
Deleting an `mg-a61f` in §5, a `2 of 45` in §8, or rewriting an unrelated paragraph: **silent, 3
of 3.** Those copies are prose; they are not the anchor, and the extent line says so. The one
mutation the old check could see — every copy deleted — still fires, on both checkers.

mg-8a5c wrote this finding in the Hodge tree, mg-a318 repaired it there by writing each figure
once per site, mg-835f measured that repair at 12 of 12. The species tree has now had the pass.

---

## 5. THE ROW THAT WILL STILL PRINT RED, AND WHY IT IS NOT A DEFECT

mg-6cb9's `a1_bothways.py` row **Q17e** plants the same subdirectory and runs `e1_extents.py`, and
that instrument scores a `WIDE` row as good **only at exit 1**.

**`e1_extents.py` exits 1 when an extent line is FALSE.** Its polarity is the opposite of a
checker's. With the walks repaired, no extent line is false, so Q17e exits **0** and mg-6cb9's
table prints `*** EXTENT WIDER ***` against a tree where the extent is true. That is that
instrument's scoring, not a surviving defect, and this document is not asking to be believed on
it — the measurement that separates *the guard works* from *the guard is absent* is **P12, P13
and P15**: put any one of the three walks back to non-recursive with a subdirectory planted, and
`e1_extents.py` exits **1**. Before this ticket it could not, which is exactly what Q17e found.

`p1_depth.py` section **P1c** prints all of this in the run rather than leaving it to be
discovered by whoever next runs mg-6cb9's instrument.

---

## 6. WHAT THIS REPAIR DID NOT DO

1. **It did not close mg-6cb9's F4, F5, F6 or F7.** F4 (the shipped `out_e2_crosssection.txt`
   predating its own commit) is **incidentally corrected for this commit**: the d633 outputs were
   regenerated against the tree that ships, and `out_a2_6cb9_after.txt` was then **re-run after
   the commit landed** — per Appendix A's rule that *a commit which measures something it also
   modifies must publish the post-commit measurement* — so mg-6cb9's own two F4 rows now read
   `the COMMITTED run's extent line is true at HEAD — ok` and `the committed CENSUS is right for
   the shipped tree — ok`. That is a correct artifact, **not a repaired mechanism**: the next
   commit that adds a markdown file without re-running will make it false again, and nothing
   here stops it. F6 — `e2`'s `RUN_MIN` seam being two tokens
   wide — is untouched and remains as mg-6cb9 measured it.

   > **CORRECTED, mg-5040.** This paragraph said `A2 TOTAL BAD` **remains 1**, the one row being
   > R29. It does not. **Measured at `4372fae`** — the tree this work shipped in, which git cannot
   > move — mg-6cb9's `a2_crosssection.py` reports
   > `A2 TOTAL BAD` **2**; the second row is `the committed CENSUS is right for the shipped tree`
   > (mg-4700 F3). The figure `1` was true in the worktree where `b534db7` measured it and false
   > by the time the work merged: **post-commit is not post-merge**, and the rebase that landed it
   > put the artifact inside a tree eight markdown files larger. The rows win, so this sentence
   > moves to the rows and not the reverse. Two commit messages (`41ac5d4`, `b534db7`) carry the
   > same wrong figure and cannot be edited; they are dispositioned in §5 of
   > `docs/OneThird-Species-Hopf-Monoids-Bound-Repair.md`, together with the published transcript
   > `code/species_sites_821e/out_a2_6cb9_after.txt`, which is the **one run all three were copies
   > of**. mg-5040 regenerates the census, so a run in *its* tree reports `1` again — for a
   > different reason, and that is exactly why the figure above names the revision it was measured
   > at. A number with no tree attached cannot be corrected, only replaced.
2. **It did not wire `e2` anywhere but the three species runners.** Every other tree in this
   repository carrying a document with a strike still does not run it. That is a much larger
   wiring question than F2 asked, and it is named here rather than closed.
3. **It did not revisit which five anchors C4 checks.** §4 measures that each is checked where a
   reader meets it; whether they are the right five is `check_doc.py`'s business and was not
   re-opened.
4. **It did not test depth beyond two levels, or against symlinks, device nodes, or directories
   the walk cannot read.** None of those is claimed by any extent line.

   > **CORRECTED, mg-5040.** The second sentence is false, and it is the load-bearing one. The
   > extent lines said *EVERY REGULAR FILE … AT ANY DEPTH*, which **does** claim a file behind a
   > symlinked directory — and `os.walk` does not follow one without `followlinks=True`. mg-4700
   > measured it: with a statement planted behind a link, `w3_scope.py` was silent and
   > `e1_extents.py` **certified the extent as true**. "None of those is claimed" was the same
   > mistake as the one this section is disclaiming, made in the disclaimer. mg-5040 does not widen
   > the walk a third time; it makes each walk **return what it declined**, so a rule nobody
   > thought of arrives as a printed line and a red run. See
   > `docs/OneThird-Species-Hopf-Monoids-Bound-Repair.md` §2.
5. **Reachable is still not read.** §2.1 measures that the check executes. Whether anyone reads
   its output is not measurable here, and F2 was about the runner, which is.

---

## 7. THE ONE SENTENCE

mg-6cb9 closed with *"the extent line was the remedy for a total that named no population; the
next one is a remedy for a check that names no site."* Both remedies here name something the
check could not name before — the **depth** of a tree, the **section** of a document, the
**runner** that executes a script — and in each case the fix was to remove the unstated condition
rather than to write it down. **A condition you state is a promise; a condition you remove is a
property.** The one directory rule that survives is stated, because it could not be removed, and
it is printed where the total is printed so that it can be argued with.

---

## 8. REPRODUCE

```
cd code/species_sites_821e && sh run_all.sh          # ~4 min, pure Python 3, NO NETWORK
cd code/species_repair_6f61 && sh run_all.sh         # ~30 s, now runs the cross-section check
cd code/species_remainder_f8fa && sh run_all.sh      # ~15 s, likewise
cd code/species_repair_a4ef && sh run_all.sh         # ~5 s, likewise
cd code/species_extent_d633 && sh run_all.sh         # ~2 min, E1/E2/E3
```

`P1`, `P2` and `P3 TOTAL BAD` are all **0**, and each is followed in the output by its own extent.
**This instrument mutates the worktree it runs in**, one edit at a time, with `git status
--porcelain` *and the full `git diff`* compared before and after every probe; a difference stops
the run with exit 2. Do not kill it mid-probe — the restore lives in the process, and if it dies
you should read `git diff` before believing the tree. That happened during development and is
recorded in `OUTCOMES.md`.
