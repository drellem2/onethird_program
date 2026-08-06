# mg-ec63 — the ARC-WIDE truncate-before-probe sweep

**The ask was the sweep, not the fix.** For each tree where a probe reads a
transcript its own run has already emptied: *what did the probe fail to see, and
what was published on the strength of it?* Changing the ordering is the easy part
and is explicitly not the deliverable. **I applied the fix to no other tree** —
see WHAT I DID NOT DO.

Run `sh run_all.sh`. It takes about **two hours**: it runs 422 of the arc's own
probes once each, and the confirmed-biting subset two or three times more. Every
probe's output is captured to memory, never redirected onto a transcript, and
every tree is `git checkout`-restored afterwards. S6e checks the whole of `code/`
**and `docs/`** at the end and goes red if anything was left behind.

---

## The answer, in one table

| | |
|---|---|
| runners in the arc | **109** |
| …that truncate a transcript with a plain `>` | **95** |
| …with mg-bf79's `.new`+`mv` structural fix | **1** |
| …that write no transcript at all | **12** |
| TRUNC steps whose transcript is committed | **422** |
| …whose probe was **observed to read its own emptied transcript** | **37** (21 runners) |
| …whose probe reads *another* transcript (STALE, not empty) | **13** (11 further runners) |
| of the 37: **SAME** — the ordering bug cost nothing | **12** |
| of the 37: **DIFFERENT** — the answer changes | **6** |
| of the 37: **NEVER EXERCISED** — B cannot run at all | **0** |
| of the 37: NONDETERMINISTIC (excluded by the control) | **14** |
| of the 37: both runs hit the 120 s timeout | **5** |
| of the 6 DIFFERENT: committed transcript **provably is** a defect run | **1** |
| of the 6 DIFFERENT: tree has drifted, attribution not provable | **5** |
| of the 6 DIFFERENT: an integer of the delta also appears in prose | **3** *(candidate, not proof)* |

Exact figures are regenerated on every run; the transcripts in this directory are
from the run that ships them.

---

## I do not get 86, and I do not get 43. State your own numbers.

The ticket said to re-derive rather than inherit, and the numbers move.

**109 vs 109 is not agreement.** mg-03d1 counted 109 runners; so do I. Its 109
**includes its own tree**, `code/grain_axis_audit_03d1`, which is not on this
branch — its MR was still `queued` in the refinery. Two totals that match over
different sets are a coincidence of composition, and this arc has already lost a
night to an orphaned number that travelled into four artifacts.

**86 → 95, and the gap is the rule, not the arc.** mg-03d1's truncation test is
a regex over the runner text. The arc has **six** runner idioms and two of them
disagree about argument order:

```
python3 X.py > out_X.txt                       direct
run <probe> <out>                              helper, probe first
run <out> <probe>                              helper, OUT first
expect <code> <probe>   (out from the stem)    helper, derived name
run <name> ; python3 "$HERE/$name.py"          helper, no extension
for s in a b c ; python3 "$s.py" > out_$s      a LOOP — N steps, not one
```

A regex keyed on `python3 … > out_` reads the third as *running the transcript
and writing the probe*, cannot see the fourth or fifth at all, and counts the
sixth once. `lib_ec63.parse_runner` walks the shell instead — positional
parameters, `shift`, `${x%.py}`, `$(basename "$1" .py)`, `$HERE/` prefixes,
line continuations, loop unrolling — and reports **3 runners it refuses to
guess at** rather than binning them. Every parsed path is validated against the
disk; that validation is what caught this instrument inventing probes called
`can`, `the` and `ridge` out of a quoted `step "F2: can the V6 row go red?"`.

**43 → 37 steps in 21 trees, and the ticket's own sentence is narrower than the
rule that produced 43.** Under `>`, at the instant probe *X* starts, `out_X.txt`
is empty. Every *other* `out_*.txt` still holds **the previous run's bytes**.

```
EMPTIED   probe X reads out_X.txt        it reads nothing, guaranteed
STALE     probe X reads out_W.txt        it reads last run's bytes
```

mg-03d1's rule is at the grain of the *tree* and matches both. Mine is at the
grain of the *step* and separates them: **21 trees EMPTIED, 11 further trees
STALE-only, 32 under mg-03d1's rule as I measure it.** Both are defects. Only
the first is the one this ticket names, and merging them inflates the count of
the thing being repaired.

**And the measurement is of what the process opens, not of what its source
spells.** A `sys.addaudithook` on the `open` audit event records every path
each probe really opens, with the mode. Scored against mg-03d1's `READS_OWN`
regex over the same 422 probes: **56 false positives** (a docstring, a dead
branch — the source mentions a transcript the process never opens) and **32
false negatives** (a path built from a variable or an `os.path.join` that never
spells `out_` literally). The text rule is wrong in both directions.

---

## The three outcomes, not collapsed

For every EMPTIED step the probe runs twice at the same tree state: **A** with
its transcript emptied first (the defect, reproduced) and **B** with the
committed bytes in place. `diff(A, B)` is attributable to the shape and nothing
else. Two controls guard the split:

- **determinism** — every candidate DIFFERENT is re-run under B conditions; if
  `B != B'` it is NONDETERMINISTIC and not counted. **14 of 37** fall here, which
  is why the headline is 6 and not 20.
- **drift** — does A reproduce the committed transcript? Only where it does can
  "the published figure was computed under the defect" be said at all.

**NEVER EXERCISED came out 0.** No probe in the emptied population fails against
a populated transcript. That is the class the ticket calls the worst and easiest
to miss, and the answer is that this sweep found none — stated plainly rather
than left to silence.

**The six DIFFERENT rows all have the same mechanism**: the probe is a census
over the tree's own artifacts, and the artifact it cannot see is its own
transcript. So both numerator and denominator are understated —
`84 site(s) in all; 20 …` becomes `87; 21`; `ALL 86 / 21 / 36` becomes
`87 / 21 / 37`; `72 occurrences` becomes `73`.

---

## The damage, and the line I will not cross

**Proven: one.** `runner_exit_repair_70c7 :: r6_self.py` — run A comes out
byte-identical to the committed `out_r6_self.txt`, so the shipped bytes *are* a
run that could not see that file. Its delta is confined to the transcript: **no
prose claim rests on it.** A real result, recorded as one.

**Suspect: five.** The other five trees have drifted since publication —
neither A nor B reproduces the committed bytes — so `diff(A, B)` proves the
*shape changes this probe's answer* and does not prove any *published* figure is
wrong. Three of the five have an integer from the delta appearing somewhere in
their prose, and S4a labels that a **candidate, not a proof**: a README saying
`20` and a transcript saying `20` may be the same 20 or two different ones, and
only reading the sentence settles it. Turning suspect into wrong needs each
probe run at its own publishing revision. **I did not do that.**

---

## The positive control, and what it found instead

An instrument reporting "no damage" is indistinguishable from one that cannot
see damage. The one instance with an answer already on the record is mg-bf79's
`p5_self.py`, which hid **NINE** of its own labels.

**At HEAD the control cannot fire, and the reason is a finding.**
`p5_self.py:81` carries a provenance label `HEAD (truncated on disk by
run_all.sh)`: the probe **detects its own transcript being empty and falls back
to the committed bytes**. mg-bf79 closed that hole *twice* — structurally in the
runner and defensively in the probe — and the record names only the first. A
reader of mg-bf79's README would conclude the runner fix is what protects that
probe. It is not the only thing protecting it.

**At `675c2ba`, the last revision without that fallback, it fires**: the probe
sees **+27** of its own rows once the transcript is real (102 → 129), 4 counts
rise, and 10 more offending rows appear.

**It does not recover exactly 9, and PREDICTIONS.md/P5a is a MISS kept as
written.** P5a said any other number means the instrument is wrong. What P5a
actually got wrong was assuming a figure measured against the 2026-08-05 tree is
reproducible against the 2026-08-06 one — mg-bf79's tree has been republished
twice since. That is this arc's own recurring error, made inside the prediction
written to guard against it.

---

## Defects of this instrument

Seven, measured in S6 rather than asserted, three of them the audited defect
committed by the auditor:

- **SD1** — this tree is a member of the population it counts. Both numbers are
  printed. Its runner uses the structural fix, which is the only reason S3's
  numbers are not partly about itself.
- **SD2** — the audit hook sees only the probe's own process. A probe reading a
  transcript through `cat` is invisible to it. Reported as a **bound**.
- **SD3** — the resolver invented probes called `can`, `the` and `ridge` by
  splitting a quoted argument on whitespace.
- **SD3a** — the trace counted a **write** as a **read**, *and then I
  misattributed the evidence for it*. The mode fix is right and its measured
  effect is **0**; the two modified transcripts that sent me looking were
  written by probes of *other* trees, killed by this suite's timeout. A rigorous
  fix with a confidently wrong mechanism.
- **SD3b** — the restore rested on the files happening to be **tracked**. Caught
  by the assertion that checks the restore, on an untracked fixture.
- **SD4** — a `shift` on the same line as an assignment was invisible, so every
  positional parameter after it was off by one.
- **SD6b** — steps killed at the timeout are recorded as not-reading when the
  truth is not-known. **Every count in S2b is a lower bound.**
- **SD6c** — a killed probe leaves **another ticket's fixture** on disk. The
  first full pass left an unreadable file, an injected directory, two strike
  files, and **two appended sections in `docs/`** — a measurement that edited the
  arc's prose. `restore_arc()` now walks every tree and `docs/`.

---

## WHAT I DID NOT DO

- **I did not apply the fix to the other 94 runners.** The ticket orders
  sweep-then-fix and says inverting it destroys the evidence. Step 2 of the
  ticket is a second action and this is not it.
- **I did not run any probe at its own publishing revision.** That is what would
  turn the five *suspect* rows into *wrong* or *fine*, and it is the single
  largest piece of work this ticket leaves open.
- **I did not resolve the 5 steps where both runs hit the 120 s timeout**, nor
  the 46 steps in S2 that timed out before they could answer. Those are not
  clean; they are unmeasured, and S2a says so where the number is printed.
- **I did not open a ticket per finding.** The ticket says a silently-green
  control belongs in its own ticket; the proven row (70c7) and the five suspect
  rows are named here and nowhere else.
- **I did not read the 3 candidate prose sentences closely enough to adjudicate
  them.** S4a prints them so a human can.
- **I did not measure the STALE class beyond counting it.** 13 steps in 11
  further trees read a transcript holding the *previous* run's bytes. That is a
  real defect of a different shape and nothing here says what it cost.
