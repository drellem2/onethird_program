# mg-d53d — OUTCOMES

`PREDICTIONS.md` scored against the committed transcripts. It was written and
committed at `79e23c8`, **before any script in this directory existed**, and
has not been edited since. Nothing below revises a prediction because the
measurement disagreed with it — a refuted prediction is a result, and five of
the twenty-five are the most useful lines in this document.

## How twenty-five ids are counted

`PREDICTIONS.md` says twenty-five and its ids run `Q1`–`Q10`, `Q12`–`Q25`.
**There is no `Q11`** — the id is skipped in the pre-registration and is
reported here rather than quietly renumbered. That leaves twenty-four ids;
`Q19` asks two separable questions (mg-4adb's three `*.md` files in the census,
and a self-exclusion in `t3_census.py`'s population) and is scored as `Q19a`
and `Q19b`. Twenty-four ids, twenty-five answers.

The one numbered disclosure that is scored (`disc.4`, the line counts counted
from the source before any probe existed) is scored **so that a reader can see
the disclosure was true**, not so that it counts as a hit. `G5a`, the
`__pycache__` transcript observation, is not scored at all, for the same reason
`PREDICTIONS.md` gives: it was seen before that file existed.

## The score

**20 held, 5 missed.** Four of the five missed in the direction of *more*.

| id | held? | predicted | measured |
|----|-------|-----------|----------|
| disc.4 | HELD | 83, 85, 87 (255); e2 299; kernd633 252 | identical, re-derived in the sandbox |
| Q1 | **HELD** | 1, 1, 1, each the cross-section call | 1, 1, 1, each the cross-section call |
| Q2 | **HELD** | 255 of 255 agree, row for row | 255 of 255, on exit code, disposition and finding-printed |
| Q3 | HELD | 255 rows, 0 outside the three runners | 255 rows, 0 outside |
| Q4 | *MISSED* | 2 e2 deletions leave exit 0, both printing the finding | **3**, and one of them silent |
| Q5 | *MISSED* | 6 of 6 exit 0, 6 of 6 print the finding | **9 of 9** exit 0, **6 of 9** print it |
| Q6 | *MISSED* | 0 kernd633 deletions lose the gate | **3**, all three silent |
| Q7 | *MISSED* | 2 outside the certified population | **6**, against 806 lines of which 255 are covered |
| Q8 | HELD | 15 of 15 steps leave the runner non-zero | 15 of 15 |
| Q9 | HELD | exit 1, 1, 1 on a natural input each | 1, 1, 1, caught by three distinct checkers — `E2`, `w3_scope.py`, `CHECK_DOC` — read out of the runs |
| Q10 | **HELD** | HEAD 1,1,1 agreeing; pin 0,0,0 disagreeing, finding printed 3 of 3 both | exactly that |
| Q12 | *MISSED* | the bucket line says UNREADABLE, names PermissionError, and `ENCODING` is not on it | first two yes; the word **is** on it, inside a denial |
| Q13 | HELD | `w3_scope.py` exit 1 | 1 |
| Q14 | HELD | the f8fa runner exit 1 | 1 |
| Q15 | HELD | undecodable file: exit 0, bucket says ENCODING | exactly that |
| Q16 | HELD | e2 on an unreadable `*.md`: exit 1 by traceback, no finding printed | exactly that |
| Q17 | HELD | unreadable directory: onerror fires, NOT STATED, e2 exit 1 | exactly that |
| Q18 | HELD¹ | diff empty; 0 self-excluding predicates anywhere | empty; 6 candidates, 0 self-exclusions |
| Q19a | HELD | mg-4adb's three `*.md` files, 3 of 3 in the census | 3 of 3 |
| Q19b | HELD | no self-exclusion in `t3_census.py`'s population | 0, and its own commits are in it |
| Q20 | HELD¹ | this instrument's own files join the census and are not excluded | they do; 0 self-exclusions in its source |
| Q21 | HELD | 6 of the 7 end in an unconditional `sys.exit(0)`; `selftest.py` does not | exactly that |
| Q22 | HELD | those six exit 0, 6 of 6 | 6 of 6 |
| Q23 | HELD | the last command is `grep -h "TOTAL BAD" out_t*.txt` | exactly that |
| Q24 | **HELD** | a step printing `TOTAL BAD: 7` leaves the runner exiting 0 | exit 0, with that line in its own output |
| Q25 | HELD | a step forced to exit 1 makes the runner exit 1 | 1 |

¹ Scored with the stage-2 rule. **With the rule as first written, Q18 and Q20
both scored MISSED, at 2 each.** That run's numbers and the reason are in
`README.md` under *Four defects of this instrument, kept*, and the four lines
it wrongly flagged are printed in `out_g4_self.txt` with their code-only
rendering beside them. The rule was repaired; the score it produced first is
recorded here rather than replaced.

## The four misses that matter, and what they say

**Q4, Q5, Q6 and Q7 all missed low.** The pre-registration predicted two
deletions outside the certified population would turn a red gate green, both
printing the finding. There are **six**, and **four of the six are silent** —
the checker reads nothing, reports nothing, and returns 0.

- `e2_crosssection.py:52`, `FILES += _f`. Predicted nowhere. Deleting it leaves
  `FILES` empty, so no document is read, no strike is measured, `bad` stays 0
  and e2 exits 0 **without printing the finding**. The two lines that *were*
  predicted, `bad += len(fires)` and `sys.exit(1 if bad else 0)`, both print it.
- `kernd633.py:127`, `196` and `205`. Predicted **0**, on the reasoning that
  Python's indentation turns most deletions in that file into a raise and that
  `E2b`'s five constructed controls catch the ones that quietly disable the
  detector. The reasoning is right about 249 of the 252 lines and wrong about
  three, and all three are silent.

The prediction that named the mechanism was correct about the mechanism and
wrong about its reach. That is the useful shape of a miss: `E2b` does catch a
detector that has been disarmed *in a way E2b's inputs exercise*, and three
deletions disarm it in a way they do not.

**Q12 missed on the word and not on the substance.** The prediction asked for
`ENCODING` to be absent from the line. The line reads:

> `declined, NOT STATED: probe_d53d_x4.py   REACHED AND NOT READ: open() raised
> PermissionError.  This is NOT an encoding problem -- the file's bytes were
> never seen`

The word is there because the repair put it there, inside an explicit denial of
the attribution mg-6ef4's reader was sent to. The prediction tested for a word;
the question was about an attribution. `G3a` now asks the substantive question
as its own row — *does the line attribute the decline to the file's encoding* —
and that row holds. **Q12 is left as written.**

## What was falsified

`PREDICTIONS.md` names four things that would falsify this audit. None of them
happened:

- *Q1 measuring anything other than 1, 1, 1* — it measured 1, 1, 1. mg-4adb's
  headline figure reproduces under an instrument that shares no code with it.
- *Q4 measuring 0* — it measured 3. The second layer is open, and wider than
  predicted.
- *Q10's pin column not reproducing 0, 0, 0* — it reproduced, with the finding
  printed 3 of 3. The before-state is what both tickets describe.
- *Q21 measuring 0* — it measured 6. The fourth runner does not report its own
  findings.

## What this audit did that no list in either ticket asked for

Named, as the floor item requires:

1. **`code/species_7d75/run_all.sh`** — the fourth species runner, in no
   deletion population in this arc (G5, five predictions, all held, one
   finding).
2. **`e2_crosssection.py` and `kernd633.py` as a deletion population** — 551
   lines nobody had deleted (G1f, G1h, four findings).
3. **An unreadable directory** under `code/` holding a `*.md` — a route into
   layer 1's residue that neither ticket lists (G3g).
4. **The counterfactual for the unreadable file** — the same bytes, readable,
   shown to be a live X4 finding, so that "not counted" is measured against
   what counting looks like (G3e).
5. **`e2_crosssection.py`'s own behaviour on an unreadable `*.md`** — the
   fourth checker mg-4adb measured and did not repair (G3f).
