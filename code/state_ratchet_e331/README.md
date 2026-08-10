# mg-e331 — THE STATE.md SIZE RATCHET

**What this directory is:** a gated quantity on `STATE.md`'s word count, wired into the
command the refinery runs on every merge request, together with the measurement that chose
its threshold and the exhibit that demonstrates it firing.

**What it does on red:** `./build.sh` exits non-zero, the merge request FAILS, and the branch
does not land. It blocks; it does not notify.

---

## 0. THE TICKET, AND WHAT IT ASKED FOR IN ORDER

mg-ea0e cut `STATE.md` from 186,710 B / 29,094 w to 32,772 B / 4,658 w on 2026-08-06 against
its own stated target of under 6,000 words. Four days later it was back. The ticket named the
finding precisely — not "STATE.md is big", but **a restructure with no mechanism holding its
target is a one-off cleanup wearing the language of a fix** — and it forbade going straight to
the ratchet. Four things, in order:

1. Characterise the growth before ratcheting it. → §1, `out_p1_growth.txt`
2. Decide whether the target is right, with the evidence from (1). → §2
3. Then build the ratchet, failing loudly at the landing. → §3
4. Give it a positive control: demonstrate it FAILS. → §4, `out_x1_positive.txt`

---

## 1. WHAT GREW — AND THE TICKET'S OWN COUNT IS ONE SHORT

`out_p1_growth.txt` walks every first-parent landing that touched `STATE.md` — 60 of them —
and the first thing it finds is that **mg-ea0e was not the first cleanup with no mechanism.
It was the second.**

| cut | date | before → after | how much was undone | how fast |
|---|---|---|---|---|
| **mg-34bf** | 2026-07-30 | 192,898 → 164,577 B | **78% of the cut** | 8.5 hours, 7 landings |
| **mg-ea0e** | 2026-08-06 | 186,710 → 32,772 B | **59% of the cut** | 95.3 hours, 20 landings |

mg-34bf's regression was interrupted only because a *larger* cut arrived on top of it. So when
mg-ea0e was planned, the failure of a cleanup-without-a-mechanism was already on this
repository's record, seven days old. That is the strongest available argument that what was
missing is a **mechanism** and not more care — and it is why this ticket's deliverable is a
gate rather than another tidy-up.

**The growth is two different mechanisms, and one explanation covers neither.** Of the +90,840
bytes added since mg-ea0e:

- `## Attempt index` — **+47,536 B, 52% of all growth.** It went from 24 rows to 29. The
  **5 new rows carry +44,837 characters** (mean 8,967 each; the longest is 11,438 characters
  **in a single markdown table cell**) while the 24 rows that already existed grew by 1,648
  between them. **27.2× — this half grows by GAINING WHOLE DOCUMENTS.**
- `### Full ledger` — **+13,859 B, and ZERO new rows.** The fixed 13 rows absorbed +13,044
  characters of qualification in place; row 8 alone took +5,878.
- `## The one-paragraph state` — +11,189 B. The section named *one-paragraph* now contains a
  single blockquote of 9,601 characters.

At mg-ea0e's landing the longest line in the file was 1,772 characters and nothing exceeded
2,000. Today 14 lines exceed 2,000 and 6 exceed 5,000.

**Does the content BELONG here?** The ticket's stated hazard was that a ratchet on a file
absorbing work with no other home "will simply relocate the problem or start failing every
landing". Measured:

> `docs/state-history/` exists, was created by mg-ea0e for exactly this content, and holds 9
> `attempt-*.md` files. Of the **20 landings that changed STATE.md since mg-ea0e, 1 also wrote
> to it.** Nineteen did not.

So the destination is not missing, not unknown, and four days old. **What was missing was not
a home. It was anything that asked.**

---

## 2. IS 6,000 WORDS THE RIGHT TARGET? — DECIDED, NOT ASSERTED

The ticket is explicit that this must be decided with evidence, because "if four days of
honest work needs more than that, the target is wrong and ratcheting to it institutionalises a
lie."

```
HEAD                                        19,077 words
minus every attempt-index row added since   - 7,351 words   (44,837 chars, 5 rows)
= residue if ALL of it were relocated        11,726 words
mg-ea0e's stated target                       6,000 words
```

**Relocating every byte that has a home elsewhere still leaves nearly double the target.** So
the threshold is NOT set to 6,000, and the reason is not that 6,000 was wrong when mg-ea0e
chose it:

- **A gate set to 6,000 today is RED ON ARRIVAL by 13,077 words** and blocks every merge in
  this repository from the moment it lands, for a reason no author of an unrelated branch can
  act on. `code/control_gate_724a/gate.py` refuses exactly that construction in its own
  docstring, about a different suite. mg-d91f is the record of what happens next: a control
  that lints its own remedy gets suppressed, and a suppressed control is worse than none.
- `out_x1_positive.txt` §4.2 measures it rather than asserting it: a ratchet set to mg-ea0e's
  achieved 4,658 words would have **BLOCKED 20 of the 20 landings since**. That cuts both
  ways, and both ways matter — it is the evidence that the mechanism bites, *and* the evidence
  that a threshold stopping twenty consecutive landings does not hold a line, it gets removed.

**A ratchet is not a target. It is a monotone floor under a regression**, and it binds from
wherever it is set. **6,000 words is not withdrawn and it is not mine to withdraw** — it
remains what mg-ea0e aimed at and what `docs/state-history/` was built to make reachable. The
gap is a **debt of 13,077 words with a named remedy** (5 attempt-index rows → per-attempt
files), not a number to assert into a config file and call enforced.

---

## 3. THE RATCHET

**One gated quantity**, `len(STATE.md.split())`, against **one declared number** in
`CEILING.json`, which carries the reason it is what it is. **RED IS EITHER DIRECTION** —
mg-724a's rule, not a new one:

| verdict | when | what it means | exit |
|---|---|---|---|
| `GREEN` | within the band | nothing to say | 0 |
| `ABOVE-CEILING` | words > `words_ceiling` | **the regression** | 1 |
| `SLACK-UNRATCHETED` | words < `tighten_below` | you shrank the file and left the ceiling where it was — **the cut was not banked** | 1 |
| `REFUSED` | STATE.md or CEILING.json unreadable | did not reach a decision; never mapped onto a verdict | 2 |

**`SLACK-UNRATCHETED` is the half that makes this a ratchet and not a cap.** mg-34bf and
mg-ea0e both did real work and neither banked it, so neither held. A cut that does not lower
the number it is measured against buys hours.

**The remedy is always a one-line diff in the same commit**, and the failure output prints the
exact three numbers to write. Growth is not forbidden — it is **declared**. There is no
`--refresh` mode and there will not be one: a ratchet that rewrites its own threshold on
demand is laundering with extra steps.

### Where it is wired, and why there

`build.sh` at the repository root — **not** `.pogo/refinery.toml` alone. That file's own header
explains why: the refinery reaches the gate by two routes (the config file, and default
discovery of `./build.sh`), and there must be exactly one definition of what the gate IS or the
two routes drift into two gate lists that disagree. Adding a suite to the config alone would
leave the surviving route one suite short. Every suite runs and the **worst exit wins** — not
`&&`, because a gate that reveals its findings one per merge attempt is a gate people learn to
stop reading.

**Cost on the merge critical path: 0.02 s**, against the existing gate's ~6 s.

### It is itself a control

`ratchet.py` §3 runs 14 probes on **every merge**, derived from that run's observed values and
never typed, and the run is BROKEN — not green — if any is a hole. The guard that matters:
**an explained-unfalsifiable probe is a fact about the subject; on a GREEN tree nothing can
explain one, and the ratchet is BROKEN.** Explaining-away that only ever fires in one direction
is laundering; this one cannot fire on a green tree.

---

## 4. THE POSITIVE CONTROL — 8 OF 8, ON REAL COMMITS

The ticket: *"Demonstrate it FAILS on a commit that exceeds the threshold before trusting that
it passes. An unfalsified ratchet is a decorative check."* Nothing here is synthetic; every arm
plants a `STATE.md` this repository really contained and runs the **real** `ratchet.py` as a
**subprocess** — never imported, because importing a rule is one refactor away from
re-specifying it.

| arm | subject | required | got |
|---|---|---|---|
| X1 | `b80dea0e` pre-restructure, 29,094 w | exit 1, ABOVE-CEILING | ✅ `+10,017 past the ceiling` |
| X2 | `cc4c663e` mg-ea0e's own landing, 4,658 w | exit 1, SLACK-UNRATCHETED | ✅ `14,419 below the ceiling` |
| X3 | the tree as it stands | exit 0, GREEN | ✅ **not red on arrival** |
| X4 | a `CEILING.json` that does not parse | exit 2, REFUSED | ✅ |
| X5 | counterfactual: ceiling at mg-ea0e's 4,658, every landing since | ≥1 blocked | ✅ **20 of 20 blocked** |
| X0 | **the PRE-EXISTING gate**, planted 24,678-word tree | exit 0 — blind | ✅ `GATE VERDICT: GREEN` |
| X6 | **`./build.sh`**, *the same tree, same bytes* | exit ≠ 0, naming the ratchet | ✅ `exit 1 · RATCHET VERDICT: RED` |
| X7 | P7's own file against the pre-existing gate | scored, not required | recorded — **P7 MISS** |

**X0 and X6 are one planted tree, two commands, one difference.** The plant is derived from
real bytes rather than typed: this repository's own `docs/state-history/attempt-mg-a3d4.md`,
appended to `STATE.md` — precisely the content whose five successors were written into the
attempt index instead. The gate this repository had twenty minutes ago exits 0 GREEN on it.
With this suite added, the same command exits 1 and names the cause.

The real tree is touched only by X0/X6/X7, the original bytes are held in memory, the digest is
taken before, the restore is in a `finally`, and the digest is re-checked after — so a crash
leaves a **detectable** state rather than a silently edited `STATE.md`.

---

## 5. DEFECTS OF MY OWN — ALL KEPT

**D4 is the worst thing in this ticket and the positive control is the only thing that could
have found it.**

- **D1.** `p1_growth.py` printed a literal `%d` in its headline — the format argument was on
  the next `print`. A number that never got substituted, in the summary line.
- **D2.** My first regrowth rule asked *did it return to its PRE-CUT size* and answered "NOT
  yet back" for mg-34bf. Literally true, thoroughly misleading: mg-34bf's cut **was** 78%
  undone in 8.5 hours and escaped the threshold only because a larger cut arrived first. **An
  absolute threshold that a later, bigger cut makes unreachable forever reports every
  interrupted regression as no regression** — mg-f8e5's `c1_rebase.py:48` in a third costume.
  Repaired to measure the peak before the next cut.
- **D3.** My probes credited **14 of 14 CAUGHT**, and two of them (`N5`, `N6`) expected GREEN
  against an input that was already GREEN — **predicates already satisfied by the good input,
  credited as falsifications, inside the module whose docstring adopts the rule forbidding
  exactly that.** They are not deleted (an off-by-one at the edge is the likeliest defect this
  rule will ever have) but are scored `BOUNDARY` as a *transition*, and counted as neither
  caught nor a hole.
- **D4. THE RATCHET WAS STRUCTURALLY INCAPABLE OF REPORTING ITS OWN FINDING.** Two correct
  rules composed into a broken one: a probe satisfied by the good input is UNFALSIFIABLE, and
  any UNFALSIFIABLE made the verdict BROKEN. So **the moment `STATE.md` went over the ceiling,
  `N1`/`N2` were satisfied by the real input and the verdict became `BROKEN` (exit 2) instead
  of `RED` (exit 1)** — all 20 counterfactual landings came back REFUSED, X1 came back BROKEN,
  and the entire `WHAT TO DO` remedy text could never print. **It was not fail-open**, which is
  exactly why it would have survived: the gate still went red, the branch still did not land,
  and the message told the author the ratchet was broken rather than that their file grew. A
  control that blocks correctly while diagnosing wrongly is how an author learns to route
  around it. Fixed by distinguishing *explained* from *unexplained* unfalsifiability, guarded
  so the explanation is unavailable on a green tree.
- **D5.** `N2` was `observed * 2` and `N4` was mg-ea0e's 4,658 typed as a literal. Both are
  fine against *this* tree and both break against trees the positive control actually plants:
  doubling 4,658 is 9,316, still under the ceiling, so N2 expected ABOVE and got SLACK; and
  N4's literal **equals** the observed count on the mg-ea0e landing itself, so its mutation was
  the identity. mg-2f44 lost two fixtures to that second one. Both now derived from the ceiling.
- **D6.** **This branch does not edit `STATE.md`'s content, so the ratchet is green on its own
  branch by construction** — a check only ever observed green on the branch that introduced it.
  That is what §4 exists to answer for, and it is why §4 uses real commits rather than this one.
- **D7.** The ceiling is a number read today. If another branch lands a legitimate `STATE.md`
  change between this measurement and this merge, **the ceiling is stale at its own landing**
  and the gate goes red for a reason its author cannot act on. That is mg-724a's recorded/gated
  hazard arriving from the other side; the remedy available is the one-line raise, which is D8.
- **D8. A RATCHET WHOSE CEILING CAN BE RAISED IS A SPEED BUMP.** Mine can be — one line, same
  commit, with a reason. **I do not have an argument that this stops growth. I have an argument
  that it stops SILENT growth**, which is the defect actually named. If the ceiling is raised at
  every landing, this will have produced a changelog of the regression and nothing else. Filed
  as E1 in `PREDICTIONS.md` before any of it was built, and it remains the honest limit.
- **D9.** `docs/state-history/` is now the named destination and **nothing measures it.**
  Relocation with no ratchet on the destination moves growth rather than stopping it. A scope
  decision, not an oversight.

---

## 6. PREDICTIONS: 6 HIT, 1 MISSED

Scored by machine in the transcripts, including the loss.

| | bet | | |
|---|---|---|---|
| P1 | growth is new rows, ≥5× in-place | **HIT** | 44,837 vs 1,648 = **27.2×** |
| P2 | the ledger gained ZERO rows | **HIT** | 0 new, +13,044 in place |
| P3 | 6,000 unreachable at HEAD; decide against it | **HIT** | residue 11,726 > 6,000 |
| P4 | ≥3 growth landings wrote nothing to the destination | **HIT** | **19 of 20** |
| P5 | red on REAL committed bytes, both directions | **HIT** | X1 exit 1 ABOVE, X2 exit 1 SLACK |
| P6 | a probe comes back unfalsifiable on run one | **HIT** | D4 **and** D5 |
| P7 | the existing gate exits 0 on the pre-restructure file | **MISS** | it exits **2** |

**P7 loses and the reason is worth more than the bet.** The pre-existing gate does not exit 0
on that file — it **REFUSES**, because the twin-pin suite cannot parse that file's ledger
(`twin.verdict_grade matched its pattern 0 time(s)`). It goes red on that tree **for a reason
that is not size at all**: a control broke, not a file grew. Had I scored blindness on P7's own
file I would have recorded a green I never saw. X0 is the honest form of the claim — a file
that grows while staying structurally intact, which is what the last twenty landings actually
did, sails straight through.

---

## 7. THE CEILING'S FIRST RAISE IS THIS COMMIT'S OWN

`STATE.md` gains one paragraph here: a pointer telling whoever edits it that the file is
ratcheted, where the number lives, and that per-attempt write-ups belong in
`docs/state-history/`. That is 108 words, so **the ceiling was raised from 18,969 to 19,077 in
the same commit, with the reason written into `why`** — the documented procedure, exercised by
its own author on the first landing that needed it. The pointer deliberately does **not** quote
the current word count: a size quoted inside the file it measures is stale at the next landing,
in a corpus whose entire culture is about figures that rot.

---

## 8. WHAT IS NOT HERE

- **`STATE.md` is not restructured.** Not one word of its existing content is moved, and the
  13,077-word debt is named, not paid. Paying it is a separate ticket with a separate audit.
- **Row 8 of the rendered twin's drift control is still unticketed.** c9bc2 reported it and
  this ticket's body explicitly says not to bundle it. It is not bundled and it is not fixed.
- **No published figure moved.** The only files this branch changes outside its own directory
  are `build.sh` (one suite added to the gate list) and `STATE.md` (one paragraph added).

## FILES

| | |
|---|---|
| `CEILING.json` | **the declared number.** One line to change, with a required `why`. |
| `lib_e331.py` | the single definition of size, the ceiling parser, and the rule. |
| `ratchet.py` | the gate. Reads the **working tree** — the refinery runs on a rebased tree that exists at no commit. |
| `negative_control_e331.py` | 14 probes, run on every merge. |
| `run_all.sh` | the runner. Requires the decision line before reading the exit code. |
| `p1_growth.py` → `out_p1_growth.txt` | §1–2. The characterisation the threshold rests on. |
| `x1_positive_control.py` → `out_x1_positive.txt` | §4. The demonstration that it fires. |
| `PREDICTIONS.md` | committed before one line of the instrument existed. |
