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
**and `docs/`** at the end and goes red if anything was left behind. On the run
that ships these transcripts it is **0 lines of change outside this tree**.

---

## The answer, in one table

| | |
|---|---|
| runners under `code/`, **including this suite's own** | **110** |
| …the arc this sweep is *about* | **109** |
| …that truncate a transcript with a plain `>` | **96** — see the correction below; the arc-only figure is **95** |
| …with mg-bf79's `.new`+`mv` structural fix | **1** |
| …that write no transcript at all | **13** |
| …the resolver refuses to fully parse | **3**, printed as UNRESOLVED |
| TRUNC steps whose transcript is committed | **422** (of 431) |
| …**observed to read their own emptied transcript** | **32** in **19 runners** |
| …that read *another* transcript (STALE, not empty) | **12** in **11 further runners** |
| …where a *child process* read it, not the probe | **5** |
| …killed at the 120 s timeout before they could answer | **40** |
| of the 32: **SAME** — the ordering bug cost nothing | **11** |
| of the 32: **DIFFERENT** — the answer changes | **4** |
| of the 32: **NEVER EXERCISED** — B cannot run at all | **0** |
| of the 32: NONDETERMINISTIC (excluded by the control) | **14** |
| of the 32: both runs hit the timeout | **3** |
| of the 4 DIFFERENT: committed transcript **provably is** a defect run | **1** |
| of the 4 DIFFERENT: tree has drifted, attribution not provable | **3** |
| of the 4 DIFFERENT: a changed figure that reached prose | **0** |

---

## I do not get 86, and I do not get 43. State your own numbers.

**Three numbers, and none of them is "109 and so is theirs."** mg-03d1 counted
109. I count **110** including this suite's own runner and **109** excluding it —
`code/*/run_all.sh` is a property, so the population acquired a member that is
the counter the moment this directory had a runner. mg-03d1 recorded exactly
that, and its own A4b prediction went from right to wrong when it happened. Both
of my numbers are printed; neither is the one I would pick to protect a sentence.

**And 109 vs 109 would not be agreement anyway.** mg-03d1's 109 **includes its
own tree**, `code/grain_axis_audit_03d1`, which is not on this branch — its MR
was still `queued` in the refinery. Two totals that match over different sets are
a coincidence of composition. An earlier draft of S1a said *"THE TOTALS AGREE AND
THE POPULATIONS DO NOT"*; that sentence stopped being true the instant my own
runner landed, and it is gone rather than patched.

**86 → 96 (95 excluding me), and the gap is the rule, not the arc.** mg-03d1's
truncation test is a regex over the runner text. The arc has **six** runner
idioms and two of them disagree about argument order:

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
parameters, `shift`, `${x%.py}`, `$(basename "$1" .py)`, `$HERE/` prefixes, line
continuations, loop unrolling — and reports **3 runners it refuses to guess at**
rather than binning them. Every parsed path is validated against the disk; that
validation is what caught this instrument inventing probes called `can`, `the`
and `ridge` out of a quoted `step "F2: can the V6 row go red?"`.

**43 → 32 steps in 19 trees, and the ticket's own sentence is narrower than the
rule that produced 43.** Under `>`, at the instant probe *X* starts, `out_X.txt`
is empty. Every *other* `out_*.txt` still holds **the previous run's bytes**.

```
EMPTIED   probe X reads out_X.txt        it reads nothing, guaranteed
STALE     probe X reads out_W.txt        it reads last run's bytes
```

mg-03d1's rule is at the grain of the *tree* and matches both. Mine is at the
grain of the *step* and separates them: **19 trees EMPTIED, 11 further trees
STALE-only, 30 under mg-03d1's rule as I measure it.** Both are defects. Only the
first is the one this ticket names, and merging them inflates the count of the
thing being repaired.

**And the measurement is of what the process opens, not of what its source
spells.** A `sys.addaudithook` on the `open` audit event records every path each
probe really opens, **with the mode and the pid**. Scored against mg-03d1's
`READS_OWN` regex over the same 422 probes: **336 agree, 58 false positives**
(the source mentions a transcript the process never opens) and **28 false
negatives** (a path built from a variable or an `os.path.join` that never spells
`out_` literally). The text rule is wrong in both directions.

**Every count above is a LOWER BOUND.** 40 of the 422 steps were killed at the
120 s timeout, and a probe killed before it reaches the line that opens its own
transcript is recorded as not-reading when the truth is not-known. S2a says so
where the number is printed, not in a footnote.

---

## The three outcomes, not collapsed

For every EMPTIED step the probe runs twice at the same tree state: **A** with
its transcript emptied first (the defect, reproduced) and **B** with the
committed bytes in place. `diff(A, B)` is attributable to the shape and nothing
else. Two controls guard the split:

- **determinism** — every candidate DIFFERENT is re-run under B conditions; if
  `B != B'` it is NONDETERMINISTIC and not counted. **14 of 32** fall here, which
  is why the headline is 4 and not 18.
- **drift** — does A reproduce the committed transcript? **11 do, 21 do not.**
  Only where it does can "the published figure was computed under the defect" be
  said at all.

**NEVER EXERCISED came out 0.** No probe in the emptied population fails against
a populated transcript. That is the class the ticket calls the worst and easiest
to miss, and the answer is that this sweep found none — stated plainly rather
than left to silence.

**The four DIFFERENT rows share one mechanism**: the probe is a census over the
tree's own artifacts, and the artifact it cannot see is its own transcript. Both
numerator and denominator are understated — `72 occurrences of an X2-shaped
claim` becomes `73`, and so on.

---

## The damage, and the line I will not cross

**Proven: one.** `runner_exit_repair_70c7 :: r6_self.py` — run A comes out
byte-identical to the committed `out_r6_self.txt`, so the shipped bytes *are* a
run that could not see that file. Its delta is confined to the transcript.

**Suspect: three.** `branching_audit_d330 :: e3_dispositions.py`,
`face_geometry_audit_6653 :: verify_claims.py`,
`runner_exit_audit_56dc :: t5_fixture.py` have drifted since publication —
neither A nor B reproduces the committed bytes — so `diff(A, B)` proves the
*shape changes this probe's answer* and does not prove any *published* figure is
wrong. Turning suspect into wrong needs each probe run at its own publishing
revision. **I did not do that.**

**Prose claims resting on an empty-file reading: zero found.** No integer that
moves between A and B appears in any of those trees' `.md` files or commit
subjects. S4a labels integer matching a **candidate, not a proof** in either
direction: a README saying `20` and a transcript saying `20` may be the same 20
or two different ones. Zero candidates is a weaker statement than "no damage",
and it is the one the evidence supports.

**So the honest headline is: the arc-wide idiom is real, it bites in 19 trees,
it changes an answer in 4, and on this branch it cost the published record
nothing that this instrument can find.** The four trees still need repairing —
they are publishing figures computed against a file they cannot see — but no
sentence a human read is currently false because of it.

---

## The positive control, and what it found instead

An instrument reporting "no damage" is indistinguishable from one that cannot see
damage. The one instance with an answer already on the record is mg-bf79's
`p5_self.py`, which hid **NINE** of its own labels.

**At HEAD the control cannot fire, and the reason is a finding.**
`p5_self.py:81` carries a provenance label `HEAD (truncated on disk by
run_all.sh)`: the probe **detects its own transcript being empty and falls back
to the committed bytes**. mg-bf79 closed that hole *twice* — structurally in the
runner and defensively in the probe — and the record names only the first. A
reader of mg-bf79's README would conclude the runner fix is what protects that
probe. It is not the only thing protecting it.

**At `675c2ba`, the last revision without that fallback, it fires**: the probe
sees **+27** of its own rows once the transcript is real (102 → 129), four counts
rise, and ten more offending rows appear.

**It does not recover exactly 9, and PREDICTIONS.md/P5a is a MISS kept as
written.** P5a said any other number means the instrument is wrong. What P5a
actually got wrong was assuming a figure measured against the 2026-08-05 tree is
reproducible against the 2026-08-06 one — mg-bf79's tree has been republished
twice since. That is this arc's own recurring error, made inside the prediction
written to guard against it.

---

## S6a/SD1b IS A FALSE POSITIVE OF MY OWN RESOLVER, AND IT IS CORRECTED HERE RATHER THAN RE-RUN AWAY

`out_s6_self.txt` prints, of this suite's own runner:

```
      my own runner's operators: TRUNC

  SD1b  AND MY OWN RUNNER CARRIES THE DEFECT I AM SWEEPING FOR
```

**That sentence is false, and the operator behind it is real.** `run_all.sh` does
write with a plain `>`, but the target is `"$WORK/$_o"` — a `mktemp -d` directory
**outside the repository entirely**. Nothing in this tree is ever truncated: the
transcripts are `cp`'d in once, after the last probe has exited. That is
*stronger* than `.new`+`mv`, not weaker.

The resolver reports TRUNC because of a simplification it makes deliberately and
states in its own source: **an untraceable `$VAR/` prefix is assumed to be a
directory whose basename is inside the tree.** That is sound for `"$HERE/out_…"`,
which is how the arc's runners use it, and unsound for a prefix that leaves the
repository. `locate()` then resolves `@OPAQUE/out_s2_bite.txt` to
`code/truncate_sweep_ec63/out_s2_bite.txt`, which exists, and the step is
classified as truncating a transcript it never touches.

Consequences, stated rather than buried:

- **S1b's 96 truncating runners is 95 over the arc**, plus this suite counted
  wrongly. The table above carries both.
- **SD1b's headline is wrong; SD1's is right.** This tree *is* a member of the
  population it counts. It is *not* an instance of the defect it sweeps for.
- **This is a twelfth defect of this instrument** — call it **SD5b**, the
  opaque-prefix assumption — and it was found by reading my own transcript after
  the run that ships it.

**Why it is corrected in prose and not in the code.** Editing `s6_self.py` to say
something the shipped transcript does not say would make the two disagree, and
re-running to make them agree costs another two-hour pass over the arc *and*
erases the record of my instrument getting this wrong. mg-b2af's still-open list
was corrected the same way — in place, beneath the bullet it leaves as written.
The transcript is what the instrument said; this is what is true.

---

## Defects of this instrument

**Twelve, measured in S6** (plus SD5b above, corrected in prose), four of them
found by something other than reading the output:

| | caught by | |
|---|---|---|
| **SD3** — invented probes called `can`, `the`, `ridge` | validating each parsed path against the disk | a quoted `step "F2: can the V6 row go red?"` split on whitespace |
| **SD3a** — a **write** counted as a **read**, then the evidence **misattributed** | `git status` after the pass | the mode fix is right; its measured effect is **0**; the two modified transcripts were written by probes of *other* trees, killed before cleanup. A rigorous fix with a confidently wrong mechanism |
| **SD3b** — the restore rested on files happening to be **tracked** | the selftest assertion that checks the restore | git cannot restore what it does not track |
| **SD4** — a `shift` sharing a line with an assignment was invisible | the `expect` trees resolving to a probe named `0` | every positional parameter after it off by one |
| **SD6d** — a **child's** read attributed to its **parent**, and unstable | arithmetic: S2 printed 37 EMPTIED steps and S3, reading the same ledger, swept 36 | `EC63_TRACE` is inherited; the trace now carries the pid, and 5 steps are now the child's |
| **SD6f** — **the sweep's own transcript was destroyed by the arc it was sweeping, twice** | a zero-byte `out_s2_bite.txt` beside `exit 32`, and a SUMMARY with the S2 row simply missing | a vacuous pass of exactly this ticket's shape, produced by the sweep for it. Repaired structurally: the transcripts, ledger, shim and traces now live outside the repository |
| **SD1, SD2, SD5, SD6b, SD6c, SD7** | S6, by construction | the population contains the counter; a non-Python child is invisible; a `#` in an unbalanced quote; **40 killed steps make every count a lower bound**; a killed probe leaves another ticket's fixture on disk, `docs/` included |

---

## WHAT I DID NOT DO

- **I did not apply the fix to the other 95 runners.** The ticket orders
  sweep-then-fix and says inverting it destroys the evidence. Step 2 of the
  ticket is a second action and this is not it.
- **I did not run any probe at its own publishing revision.** That is what would
  turn the three *suspect* rows into *wrong* or *fine*, and it is the single
  largest piece of work this ticket leaves open.
- **I did not resolve the 40 steps killed at the timeout**, nor the 3 where both
  runs timed out. Those are not clean; they are unmeasured.
- **I did not identify which of the arc's probes destroyed my S2 transcript.**
  A 40-step subset writes it perfectly, so it is one of the later probes; I
  repaired the exposure rather than naming the cause.
- **I did not investigate the 14 NONDETERMINISTIC steps.** They are excluded from
  DIFFERENT by a control, not explained. A probe that gives two answers to the
  same question in one minute is its own finding and nothing here pursues it.
- **I did not open a ticket per finding.** The four DIFFERENT trees are named
  here and nowhere else.
- **I did not measure the STALE class beyond counting it.** 12 steps in 11
  further trees read a transcript holding the *previous* run's bytes.
