# mg-d2c2 — THE NUMBER THAT WENT UP IS NOT MEASURING WHAT IT SAYS

`audit.sweep_dirs_without_evidence` went **25 → 27** on 2026-08-12 and the two new names are
this arc's. The ticket asked whether the two gaps are real or an artefact of the detector's
definition, and said that if they were artefacts the finding would be about the detector and
would be the more interesting one.

**They are artefacts. Both of them. And so are at least two of the original 25.**

## THE VERDICT IN FOUR LINES

1. The two names, read out of the sweep and not inferred from the count:
   **`code/audit_successor_consolidation_9134`** and **`code/compression_novelty_623a`**.
2. Both gaps are **DETECTOR ARTEFACTS**. 9134 ships four planted worlds and an arm
   reproducing its own control's blindness on purpose; 623a ships three arms declared
   `[MUST FAIL]` and a committed transcript recording them firing on 9420 of 13416 inputs.
   Eleven exhibits are located at run time by `p3_adjudicate.py` and printed with file and
   line.
3. **Nothing was added to move the number**, because the ticket's item 3 does not apply and
   because adding token-shaped evidence to a directory that already has real evidence is the
   exact conversion of a real metric into a decorative one that the ticket forbids.
4. **The number after: the field still reads 27, against a population of 202 directories.**
   Of those 27, 11 carry an inverted arm the sweep cannot see. The remainder — **16 of
   202** — is a LOWER BOUND on the real gaps, in mg-9876's own sense of CANDIDATES. It is
   below 25, and not one directory changed to get there.

## THE FINDING THAT IS BIGGER THAN THE TWO DIRECTORIES

`a4_sweep.py` §4 is titled "THE SWEEP'S OWN TWO-SIDED CONTROL" and runs seven checks with
known answers: three on the `tee` detector, three on `membership`, one on `pipe-status`.

**Zero on the §3 evidence probe.**

That probe is the one producing the field `BASELINE.json` describes as *"the number that
should go DOWN as the estate is widened past these two directories, and watching it is the
point of recording it."* The one number in the sweep declared to be watched comes from the
one detector in the sweep that was never required to answer a question whose answer was
known in advance.

`p2_two_sided_control.py` builds that control. Five constructed directories, each with a
known correct answer, run through the probe **imported from `a4_sweep.py`, never copied**:

| world | what it is | correct | probe says | |
|---|---|---|---|---|
| W0 | computes a sum; no arm, no control, nothing required to fail | BARE | BARE | PASS |
| W1 | ships `negative_control.py` and a transcript saying `CAUGHT` | EVIDENCE | EVIDENCE | PASS |
| W2 | an arm `[MUST FAIL]`, scored inverted, firing in its transcript | EVIDENCE | **BARE** | FALSE NEGATIVE |
| W3 | `controls.py` whose entire body is `print("hello")` | BARE | **EVIDENCE** | FALSE POSITIVE |
| W4 | a README saying no mutation was `CAUGHT` *because none was attempted* | BARE | **EVIDENCE** | FALSE POSITIVE |

The probe answers both ways — which is all §4 asks of the other three detectors — and is
still **wrong three times out of five**. Both of its halves test VOCABULARY: one matches six
substrings in filenames, the other matches six words anywhere in prose. Neither has read an
arm, run one, or asked whether anything in the directory is required to fail. W4 is the
sharpest of the three: a sentence stating the *absence* of a control is scored as its
presence.

So the metric does not go down when the estate gets better controlled. It goes down when
people use the six words. Today it went up because two directories did unusually thorough
control work in a vocabulary the probe was not built around.

## THE BASELINE 25 WAS NEVER A COUNT OF REAL GAPS EITHER

If it had been, today's move would be two new gaps against a clean baseline. It is not.
Two of the ORIGINAL 25, adjudicated by the same method in `p3_adjudicate.py`:

- **`counterexample_audit_a7b4`** ships a file called **`selfcheck.py`** and its output
  `selfcheck_output.txt`. Missed because the probe's regex spells it `selftest|self_test`.
  One character.
- **`sibling_sweep_7085`** ships **`out_r1_sweep_FIRSTRUN_2FAIL.txt`** — a transcript whose
  *filename* records two failures — containing a section headed `ANTI-VACUITY -- the broken
  arms must be broken FOR THE RIGHT REASON` and eleven lines reading `and it ACTUALLY FAILED
  at least once`. Missed because `RED_TOKENS` wants `FAILED TO`, not `FAILED`.

So the 25 → 27 move is not two misreadings on top of a clean baseline. It is two more on top
of an unknown number of them, and `p3` bounds that number from below at 11 of the 27.

## THIS DIRECTORY IS ITS OWN EXHIBIT, AND IT IS DISCLOSED RATHER THAN LAUNDERED

The first run of `p1_names.py`, before `p2_two_sided_control.py` existed, put
**`code/sweep_evidence_control_d2c2` in the bare list as the 28th name** — an instrument
whose entire subject is falsification evidence, scored as shipping none. What removed it was
not a control. It was writing a file whose name contains the substring `control`. The probe
has not run that file, read it, or asked whether it answers both ways.

It goes further, and this is the sharpest instance in the document. The token probe now
credits this directory **three** times, on prose that is *about* the probe's false positives:
`CAUGHT` in this README's W4 row, `CAUGHT` in `out_p2_control.txt` where the W4 world is
printed, and `HOLE` in `out_p3_adjudicate.txt` — on the line

```
token probe matched : (nothing — no transcript contains HOLE/CAUGHT/MISMATCH/REFUTED/...)
```

**The sentence reporting that a directory's transcripts contain no red token is itself a
transcript containing red tokens, and credits this directory with evidence of a falsification
attempt on that basis.** A detector that scores its own negative report as a positive finding
is not measuring the estate.

`p1` prints all of this on every run, live, so it cannot go stale into a claim.

## DEFECTS OF MY OWN, KEPT

- **D1 — the wider screen in Part B commits the same defect it measures.** It scores 4 of 5
  on p2's worlds and the one it gets wrong is W4, whose README says *"Wiring up a negative
  control is left for a successor ticket"* — the marker `negative control` matching the
  sentence that denies one exists. It is left in rather than tuned out: deleting the marker
  would score 5 of 5 and would delete the demonstration that **a wider vocabulary is still a
  vocabulary**. This is why Part B's screen is presented as a BOUND and not as a repair, and
  why every row it counts prints its exhibit line.
- **D2 — the screen was written after p2's five worlds existed.** Its score on them is a
  floor, not a validation. Stated in the transcript as well as here.
- **D3 — Part A's adjudication is hand-authored.** Eleven literals, chosen by reading four
  files. It is pinned rather than asserted: each literal is located at run time and `p3`
  REFUSES if one has moved, but nothing makes the *choice* of literals complete.
- **D5 — the finding erased itself the first time I ran the gate, and that is now guarded.**
  `p1` diffs today's sweep against the committed `out_a4_sweep.txt`. That file is
  **regenerated in place by `./build.sh`**, which runs `control_audit_9876/run_all.sh`. So
  the first gate run advanced the "committed" reading from 25-of-188 to 27-of-202 and the
  diff came back **empty** — the finding deleted by the act of checking the tree. Measured,
  not anticipated: it happened here. `p1` now recovers the declared reading from
  `git HEAD:` and prints a loud line when the worktree copy disagrees. Demonstrated rather
  than asserted: regenerating the file and re-running `p1` produces the warning and still
  names both directories.
- **D4 — the population moved under the ticket.** The ticket says `code/` went 188 → 200;
  it reads 202 here, because `code/facts_registry_03cf` (mg-03cf) and this directory landed
  after the ticket was filed. Every number in these transcripts is stated against the
  population it was measured on.

## WHAT WAS DELIBERATELY NOT DONE

- **`a4_sweep.py` is not edited, and neither is `BASELINE.json`.** The field is `recorded,
  not gated`; every gate in `out_gate.txt` reads MATCH; nothing is broken. Widening the
  probe's vocabulary would move the number without changing what it measures — D1 is the
  demonstration that the obvious widening reproduces the defect — and a repair belongs with
  whoever owns mg-9876's detector, with the control in `p2` as its acceptance test. A
  successor that repairs the probe should expect `p2` to go RED, and that red means the
  defect is fixed.
- **No evidence was added to either directory.** Both already have it. Adding a
  vocabulary-shaped token to move the count is the decorative-metric conversion the ticket
  names, and it would have been the third false positive in this document.
- **This suite is not in `./build.sh`.** `p2` is scored inverted: its green records that the
  probe is wrong. A gate carrying it turns red on the day someone repairs the probe — a gate
  that punishes the repair it exists to motivate. `run_all.sh` states this at the top.

## RUNNING IT

```sh
./code/sweep_evidence_control_d2c2/run_all.sh      # ~1.5 s, pure Python 3, no dependencies
```

| producer | decision line | what it does |
|---|---|---|
| `p1_names.py` | `P1 NAMES —` | runs `a4_sweep.py` live, parses its §3 name list, diffs against the declared reading recovered from `git HEAD:` (see D5), and REFUSES if the parsed list and the SWEEP count disagree |
| `p2_two_sided_control.py` | `P2 CONTROL —` | the five worlds above, through the imported probe |
| `p3_adjudicate.py` | `P3 ADJUDICATION —` | per-directory adjudication with pinned exhibits, then the population bound |

Each producer must leave its decision line or the runner reports BROKEN, not green: python3
exits non-zero both when a check fires and when it dies before deciding anything. Nothing is
piped into `tee`.
