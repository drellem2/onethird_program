# mg-cf83 — the summary block may not disagree with the rows

**The repair of mg-4d3b's finding, and the positive control that is its
acceptance.** The repaired file is `code/census_repair_f3ff/s1_rows.py`; this
directory is the control that drives it against a real broken remote.

```
python3 c1_summary_guard.py        # ~3 min; arm H's loose chain reader dominates
```

Pure Python 3 + git. Every arm runs against **throwaway clones** under a
scratch directory — no command here fetches, checks out, stashes or pulls in
either source repo.

---

## 1. What was wrong

mg-4d3b's independent audit confirmed mg-f3ff's four census rows from a
disjoint reader (7 / 5 / 0 / 0 — REFUTED, REFUTED, UPHELD, UPHELD, **2 of 4**)
and then found the defect one layer up, in the part mg-f3ff never tested: its
own summary output. Run `s1_rows.py` against a repo whose `git fetch` fails and
the **per-row sections are correct** — verdict UNKNOWN, count `?` never 0,
per-repo UNKNOWN, `CHAIN: UNKNOWN`, the reason named; five checks, five passes.
Then, in the same transcript:

| | what printed under a total fetch failure |
|---|---|
| F1 | the accuracy table rendered UNKNOWN's depth columns as `0 / 0` — `0 if not gens else len(gens)`, and `not None` is True |
| F2 | `n = 4, and all 4 are now checked against the tree`, when **zero** were |
| F3 | `The census was WRONG on 0 of its 4 rows and RIGHT on 0` |
| F4 | `4 of 4 checked, 0 refuted`, in the paragraph whose next sentence is `this does not round toward either` |
| F5 | then `TypeError: object of type 'NoneType' has no len()` — `len(L.successors(...))`, thirty lines from the docstring saying callers must not treat `None` as an empty list |

A total fetch failure produced a summary that reads as a clean, confident,
fully-measured result. **The per-row layer told the truth and the summary layer
contradicted it, and the summary is the part a human reads.**

## 2. What was changed

All in `code/census_repair_f3ff/s1_rows.py`; `lib_f3ff.py` is **untouched** —
the library was already right, which is exactly mg-4d3b's point about the
remedy being one layer too low. §10 of that directory's README states the three
rules. In short: `cell()` renders unmeasured as `?`; every count-bearing
sentence has an UNKNOWN branch; and every summary figure is a fold over
`lines`, the row sections' own output, so nothing after the row loop re-reads a
repo or touches a value that can be `None`. F5's crash is therefore
*unreachable*, not caught.

Two changes go beyond F1–F5 and are named as extensions rather than smuggled in:

* **Prediction scoring gained `UNMEASURED`.** Before, an UNKNOWN row scored
  `*** MISS ***` against its prediction and fed `Predictions scored: 0 of 4
  hit, MISSES on rows 1, 2, 3, 4` — a scoreline computed from no measurement.
  A prediction is not refuted by a run that did not happen.
* **`s1` exits 1 when a repo could not be read.** Findings about the census
  still exit 0, as `run_all.sh` documents at length. *This run did not happen*
  is a different fact and exits the way `s0_freshness.py` already does.

## 3. The control — three arms, and the healthy one is not optional

`c1_summary_guard.py` copies `code/census_repair_f3ff/` verbatim, patches the
single `REPOS` constant and nothing else, runs the **real** `s1_rows.py` as a
subprocess, and greps the **real** stdout.

| arm | setup | what it establishes |
|---|---|---|
| **H** | both clones healthy | **the mutation control.** A summary hard-wired to UNKNOWN would pass D and P. H requires real verdicts, `all 4 are now checked` still printed *because it is true*, no `?` in any depth cell, nothing marked UNMEASURED, exit 0 — and mg-4d3b's confirmed **`2 of 4` reproduced unchanged**, because a repair that moves a confirmed number is a regression |
| **D** | **clone first, then break the origin URL** in both | the acceptance. `git fetch` fails while `origin/main` still **resolves locally** — the incident's own shape: no network at boot, every checkout holding yesterday's refs. The ref is asserted to resolve, so a pass cannot be an artefact of an absent ref |
| **P** | one remote broken | UNKNOWN is sticky, so the rows are UNKNOWN while half the population is perfectly readable — the arm where a summary is most tempted to report the half it can see |

**And a structural check in every arm**, which is rule 3 stated as a property
rather than a promise: the verdict column of the summary table is compared row
by row against the verdict the *row section* printed for the same row, both
read out of the same transcript. Nothing in mg-f3ff's suite compared those two,
which is how a transcript came to hold UNKNOWN in the rows and `0`-shaped
figures in the summary with every check passing.

**Result: 55 checks, 0 failures, exit 0** — arm H 0 red, arm D 0 red, arm P 0
red. Transcript: `out_c1_summary_guard.txt`.

## 4. The independent acceptance: mg-4d3b's own detector

The strongest check here is not mine. `code/census_audit_4d3b/a3_fetchfail.py`
contains the auditor's own grep for F1–F5, written before this repair existed.
Re-run **unmodified** against the repaired script:

```
  --- the SAME transcript, further down: findings about mg-f3ff ---
    (none -- the summary block handled UNKNOWN correctly)
```

and its five per-row checks still pass — the repair did not buy the summary's
honesty by breaking the row layer. `a3 exit: 0`. Its committed
`out_a3_fetchfail.txt` still records the five findings, correctly: they were
true of the code it ran against.

## 5. Defects of this instrument, kept

1. **The acceptance grep read my own prose as the defect.** The first version of
   c1's blunt check swept the summary block for `\b0 (of its|refuted|missed)\b`
   and **failed twice against a correctly repaired script**. One hit was
   `s1_rows.py`'s own new sentence *quoting* the string it no longer prints —
   a rule that reads a sentence about the defect as the defect, which is
   [mg-4d3b's a5 defect](../census_audit_4d3b/a5_selfdefect.py) committed by the
   polecat sent to repair mg-4d3b's finding, one ticket later. Fixed **at the
   cause**: `s1_rows.py` no longer reproduces any of the five literal strings
   anywhere in its output, not even as a quotation, so a whole-transcript grep
   is legitimate and needs no prose/code classifier.
2. **The other hit was the pattern being wrong, not unlucky.** `0 missed` is
   *true* and is not a claim from zero measurement. The blunt rule "no zero in
   the summary" is **false as a principle** — `0 of 4 are checked` is F2's own
   replacement and `REFUTED 0 of 4` is a count of verdict values. What is
   forbidden is a zero standing where a *measurement of the census* would go,
   and the check now names that class as eight literal patterns instead of
   guessing at it. The tally line is disambiguated in the output rather than
   deleted: `^ these are counts of VERDICT VALUES`.
3. **Arm H is slow (~3 min of the run) and it is the arm that can rot.** It
   pins `WRONG on 2 ... RIGHT on 2` against a clone of the live tree. That is
   deliberate — it is the regression check — but a future back-dated commit
   before 2026-07-31 would turn it red for a reason that has nothing to do with
   this repair. mg-4d3b measured exactly that: a constructed back-dated commit
   raises every row by 1 and flips rows 3 and 4.
4. **The row/table agreement check is regex over stdout**, so a change to the
   table's column layout breaks the check rather than the property. A shared
   data structure would be stronger; a grep over the printed thing is what the
   ticket is about, so this one reads what a human reads.

## 6. WHAT I DID NOT DO

* **I did not re-derive the census figures.** They are mg-4d3b's, confirmed from
  a disjoint reader, and the ticket says not to re-open them. Arm H *requires*
  them unmoved; it does not re-establish them, and if it ever disagreed the
  right reading is that this repair broke something, not that `2 of 4` moved.
* **I did not touch `lib_f3ff.py`.** The library already distinguished the two
  cases in both directions and NC3 already proved the propagation. Nothing
  there needed repair and changing it would have put the fix at the wrong layer
  for a second time.
* **I did not repair s2, s3 or s4.** mg-4d3b censused 8 `None`-as-list sites
  across the deliverable; this ticket is about s1's summary. After this change
  s1 has **0** such sites in code (one mention survives in a comment describing
  the old crash). **Four remain and are unrepaired**: `s2_controls.py:130-131`
  (LATENT — inside NC1, which runs with a healthy fetch by construction) and
  `s3_graph.py:85-86` (reachable). Their summary blocks were not examined at
  all; I have no evidence either way about what they print under a fetch
  failure.
* **I did not regenerate `out_s1_rows.txt`.** It is the pre-repair transcript at
  its own commit and re-running it would re-derive the census. This is stated in
  §9 of that directory's README so the next reader is not left comparing a
  transcript against a script that no longer produces it.
* **I did not run `run_all.sh` end to end.** It fetches
  `/Users/daniel/research/onethird_program` and
  `/Users/daniel/research/one_third_width_three` directly. Every arm here uses
  throwaway clones instead, so the healthy path is exercised — but against a
  clone, not against the source repos, and `selftest_f3ff.py`, `s0`, `s2`, `s3`
  and `s4` were not run at all. I changed no file any of them import.
* **I did not repair a stale sentence I found in mg-4d3b's `a3_fetchfail.py`.**
  Its narrative prose still reads `AND THE SCRIPT LEVEL IS WHERE IT BREAKS …
  which states four false things before the crash`, while the count it prints
  on the same page is now `0 finding(s)`. That is the same defect class as this
  ticket — a fixed string beside a measurement that disagrees with it — in the
  audit that found it. It is noted here and left alone: it is another agent's
  deliverable and out of this ticket's scope.
* **I did not check the ticket bodies or any document.** No prose outside
  `code/` was read or corrected, and nothing in `STATE.md` was touched.

## 7. Files

| file | what |
|---|---|
| `c1_summary_guard.py` | the positive control: arms H / D / P, 55 checks |
| `out_c1_summary_guard.txt` | committed transcript of a full run — the healthy summary and the failure summary, side by side |
| `run_all.sh` | the runner; reports the instrument's status, not `tee`'s |
