# mg-9876 — the audit of how `code/rendered_twin_pin_9bc2` gets VALIDATED

Filed from mg-2f44's verdict, which found the third laundered green in one directory and
correctly declined to treat it as its own defect. This is the pattern, not the instance.

**Run it:** `sh code/control_audit_9876/run_all.sh`

---

## THE COUNT, BOTH WAYS

| | |
|---|---|
| arms examined | **50** (38 before this ticket's repairs; the 12 new ones are repairs) |
| sites those arms occupy | **59**, none unclaimed by the census |
| **laundered** — reported the same thing when their subject stopped | **1** (`H4`) |
| **holes** — arms that discriminate and are still blind to a named bad input | **6** |
| **repaired** | **7** (the 1 laundered + all 6 holes) |
| **removed** | **0** — see *Nothing was deleted* below |
| arms now shown RED against a known-bad input | **50 of 50** |
| defects **in this auditor**, caught by its own rule | **8**, all kept and named |

Before: 38 arms, 31 shown to discriminate, 7 red — of which **6 were defects in my probes
and 1 in the target**. After: 50 arms, 50 shown to discriminate, 6 of 6 holes closed.
Both transcripts are committed (`out_a2_discriminate_PREREPAIR.txt` and `out_a2_discriminate.txt`).

**Nothing was deleted.** The ticket says a control that cannot be made to discriminate should
be DELETED rather than left passing. Exactly one arm could not discriminate — `H4`,
`run_all.sh`'s CLEAN fallthrough — and it is not a check that cannot work, it is a branch
that was classifying by the wrong quantity. It was repaired into three arms that do
discriminate (`H5`, `H6`, `H7`), which is strictly better than deleting the branch that
prints the green. No arm was found to be irreparable, so the delete column is honestly zero
rather than zero because nobody looked.

---

## THE ONE LAUNDERED ARM

**`H4` — `run_all.sh`'s CLEAN fallthrough.** Subject: *a green from this runner means the
control ran and found nothing.* Known-bad input: the control never ran (exit 127). Report:
`CLEAN — the twin's pinned ledger rows all still match STATE.md`, exit 0. Identical to a
healthy run.

This is the **fourth** instance of the directory's own defect, in the file that was rewritten
to remove the first. Removing the `tee` fixed *whose* exit code was read. It left standing
the deeper error: the exit code was being asked a question it cannot answer. A Python process
exits 1 when `twin_pin.py` finds drift **and** when it dies in a traceback, and anything
outside `{0,1,2}` fell through to the green.

Repaired by classifying on whether the control **reached its own verdict** — `grep -m1
'^VERDICT: '` — before any branch is taken, plus a refusal for an unknown exit code and a
refusal for a DRIFT report whose worklist is empty. mg-f8e5 reached the same rule from the
other direction after running five producers without their interpreter and reading the empty
files the redirections left: *classify by whether the run reached its first decision, never
by the exit code alone.*

---

## THE SIX HOLES, EACH DEMONSTRATED BEFORE IT WAS REPAIRED

Each was confirmed by running it, with the transcript frozen at
`out_a2_discriminate_PREREPAIR.txt`, and each now reports `CLOSED`.

1. **Section 5 exempted every line containing `<!--`.** The skip read
   `if L.PIN_START.split()[0] in line` — that token is `<!--`, so an ordinary HTML comment
   anywhere on a line hid the whole line from the guard. A live
   `<!----><span><b>Generated</b> 2026-08-10</span>` walked straight past the guard written
   for exactly that string. It was also **too narrow** for its stated purpose: only the pin
   block's first line carries `<!--`, so the rest of the block was scanned anyway. An
   exemption wider than the thing it names and narrower, at once. `COVERAGE.md` declares an
   `<i>`/`<s>` bypass; this one was undeclared. → repaired to a line range.

2. **Section 6 was a substring test.** `pinned_commit in shown` against the whole visible
   provenance line — ticket smell #1, live, inside the arm added to check a *duplicated*
   provenance string. Truncating the pin's commit to `4fcb` **passed**, and so did a visible
   line naming the pinned commit alongside a second revision. → repaired to parse the commits
   out of the line and compare the list exactly.

3. **Section 3 could not tell a moved `STATE.md` from a pin with no digest.** Deleting
   `state-sha256` outright made section 3 compare the real digest against the empty string
   and print `DIFFERS` — the same word it prints on ordinary runs, under a heading that says
   in terms that `DIFFERS` *"is NOT a defect and must not be read as one"*. A broken pin was
   indistinguishable from the normal condition. This is the *same shape* as the defect
   `COVERAGE.md` already records as fixed: the field-name pattern was `[a-z-]+`,
   `state-sha256` has digits, and section 3 printed the right answer for the wrong reason.
   **The pattern was repaired; the absence never was.** → absence is now its own arm, `C3a`,
   at structural grade.

4. **A crash was reported as DRIFT, at exit 0.** See `H4` above; this is its other face.

5. **The ledger could gain a column with every arm green.** `row_digests` joins four cells
   **by name**, and `parse_state_ledger` refuses *fewer* than five cells and has no opinion
   about more. A sixth column added to the header and all twelve rows left section 2
   byte-identical. Anything the ledger grows is outside the pin from the day it is added.
   → the pin now records the column list its digests were taken over, and section 1 compares
   it. Digesting the whole raw row instead would have moved every pinned digest and forced a
   re-pin nobody reconciled, which is the one move the instrument forbids.

6. **`run_all.sh` named rows 8 and 9 as literals in its own prose.** `negative_control.py`'s
   rule — *nothing in this file may name a pinned commit or a drifted row as a literal* — was
   adopted one file away and not applied here, and the sentence was already half wrong.
   → the worklist is read out of section 2.

---

## THE PRACTICE FIX, WHICH IS WORTH MORE THAN THE SIX

`negative_control.py` now runs **the baseline-absence guard**: before any mutation, the
unmutated report is taken, and every mutation's `expect` string must be **absent from it**. A
string present in the baseline scores `UNFALSIFIABLE` and takes the harness non-zero.

This is mg-2f44's repair generalised from one arm to all of them. That repair fixed the
positive control by parsing section 2's worklist line; it did not ask whether the *other ten*
rows had the same defect. They did not — measured, not assumed — but nothing would have said
so, and nothing would say so about the eleventh. The guard is demonstrated by `N19`, whose
bad world re-points a mutation's `expect` at `all three row sets agree`: precisely the line
`"8 9" in out` was matching for its whole life.

---

## EIGHT DEFECTS OF MY OWN, ALL CAUGHT BY THE RULES I WROTE, ALL KEPT

The ticket warns that the instrument built to audit the controls is itself a control. On its
first run this auditor scored **7 arms red, and 6 of those were defects in my probes.**

1. **`sect()` returned the empty string for a section that ends the report.** Section 1's
   structural FAIL returns immediately, so the extractor's lookahead never matched, every
   predicate over it was False, and `C1a` scored **LAUNDERED over a report naming the defect
   in full**. A laundered green produced by the auditor, on its first run, in the file written
   to find laundered greens.
2. **`C2`'s good side was already bad.** Row 8 has been drifted since the pin was seeded, so
   `^ row \S+ MOVED` was true on the unmutated input — the `"8 9" in out` shape with my name
   on it. Scored `UNFALSIFIABLE`, which is what that score is for.
3. **`C2`'s bad side was inert.** The mutation appended past the ledger row's final pipe,
   which `split_md_cells` turns into a sixth cell `row_digests` never reads. The digest did
   not move. That inert mutation is how hole 5 above was found.
4. **`R4`'s good side mutated the tree its bad side was about to test.** `--reconcile` writes,
   so `good()` re-pinned the drifted row and `bad()` was refused for the wrong reason. `R4`
   scored LAUNDERED while its refusal was firing perfectly, one message away.
5. **`S1`/`S2`/`S3` imported `seed_pin` from the sandbox**, so its `from twin_pin import ROOT`
   bound `ROOT` to a directory that is not a git repository and both sides failed identically.
   Three arms condemned by one line in the probe.
6. **The sweep's membership detector counted iteration as membership.** `in out\b` matched
   `for line in out.splitlines()` and returned **597 candidates over 119 directories** — a
   number large enough to read as a finding about the tree, which was a finding about the
   regex. Tightened to 202 over 66, with the two constructions named in its own control.

7. **Two of the selftest's planted worlds were borrowed from the subject under audit, and my
   own repairs destroyed them.** `P2` planted its LAUNDERED world by running the *audited*
   `run_all.sh` at exit 127 — so when that runner was repaired, both sides went red and P2
   scored `UNFALSIFIABLE`. `P6` patched a source string that the repair had removed and scored
   `SETUP FAILED`. A selftest whose planted worlds are borrowed from the thing it audits stops
   working the moment the audit succeeds — the same shape as a fixture hardcoding the one thing
   the instrument exists to let change, which is both of mg-2f44's defects. Both worlds are now
   constructed in the selftest itself.
8. **`P6` was one-sided.** It checked only that a repaired probe reports `CLOSED`. A register
   that can only print `CLOSED` is a list of assertions exactly as one that can only print
   `CONFIRMED` is a list of accusations. It now re-introduces the section-5 bypass into a copy,
   requires `CONFIRMED`, repairs it, and requires `CLOSED` — `CONFIRMED->CLOSED` or the
   selftest fails.

None of the eight was found by reading. All eight were found because the rules are two-sided,
and the last two only because the repairs landed — which is the third distinct event in this
lineage that has surfaced a defect, after *running* the instrument (mg-9bc2's three) and
*using it for its purpose* (mg-2f44's two).

---

## HOW IT WAS ESTABLISHED THAT THIS AUDITOR CAN FAIL

`a3_auditor_selftest.py`, six planted worlds whose correct verdict is fixed in advance:
a predicate satisfied by the good input must score `UNFALSIFIABLE`; a runner whose report does
not move must score `LAUNDERED`; a working arm must score `DISCRIMINATES`; a rotted fixture
must score `SETUP FAILED`; an unregistered arm-shaped site must make the **census refuse**;
and a repaired hole must flip from `CONFIRMED` to `CLOSED`. **6 of 6.** Two of the six require
the answer *this check is worthless*, which is the half that a self-congratulating selftest
never contains.

**What remains unfalsified, stated rather than implied:** the registry's **subject sentences**.
The census proves no arm-shaped *site* is unregistered. Nothing proves that an arm's subject —
*"the twin does not claim canonicity about itself"* — is the property the arm's code actually
tests. A probe is written **from** the subject, so a subject that misdescribes its arm yields
a probe that agrees with it. That is a human reading, and no machinery in this directory would
catch it.

**A second exposure, named because it is mine:** this auditor carries ticket smell #1 at ten
sites of its own — `has(needle)` tests membership against a whole captured report, and
`a4_sweep.py` lists `control_audit_9876` among the 66 directories that do. The defence is not
that my membership tests are better; it is that the two-sided rule makes an unconditional one
score `UNFALSIFIABLE` rather than `CAUGHT`, and P1 demonstrates that. Where the haystack is a
`twin_pin` report the predicate is scoped to a parsed section instead.

**A third, smaller:** the message strings live in three places — `twin_pin.py` emits them,
`lib9876.ARMS` registers them as sites, `negative_control.py` expects them. That duplication
is a maintenance cost and is deliberate: three independent copies is what makes the census and
the harness checks rather than restatements. It bit immediately — repairing section 6's
message broke the site string and the mutation's `expect`, and **both refused loudly**, which
is the arrangement working.

---

## THE POPULATION QUESTION

`a4_sweep.py` counts the same smells across all **178** directories under `code/`. These are
**candidates, not adjudications**: deciding whether a given membership test can actually fail
requires running it two ways, which was done for exactly one directory.

- **202** whole-output membership tests in **66** directories.
- **18** `| tee` sites in **4** directories (`eps_spec_sweep_372e`, `l2_conditionality_28ff`,
  `lstar_789d`, `state_restructure_ea0e`) — instance 1's exact construction, still live
  elsewhere in the arc. `0` sites read `$?` immediately after a pipeline, and that zero is a
  measurement: the detector is demonstrated firing on a constructed one.
- **24** directories ship code with **no evidence of any falsification attempt** — no file
  named for a negative/self/positive control, and no committed transcript containing a
  demonstrated failure.

Nothing outside `code/rendered_twin_pin_9bc2`, `code/control_audit_9876`, and the `columns:`
field added to the twin's pin was edited. Naming a site is in scope; repairing another
ticket's directory is not.

---

## WHAT THIS AUDIT DOES NOT COVER

- **Everything in `COVERAGE.md`'s *What it does NOT cover* still stands unedited.** In
  particular, whether an *unmoved* row is faithfully summarised — no digest can answer that,
  and this audit is about whether the checks can fail, not about what they check.
- **The 177 other directories** are indexed, not audited. The two-sided method was applied to
  one directory and the sweep says so on its own face.
- **`COVERAGE.md` §5 is unchanged and is still the highest-value follow-up**: nothing in this
  repository runs either suite on commit, on merge, or on any schedule. An instrument nobody
  runs is the same artifact as a date nobody re-reads. This ticket made the instruments
  falsifiable; it did not make them **fire**.
