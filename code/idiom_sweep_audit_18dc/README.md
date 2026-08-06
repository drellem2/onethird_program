# mg-18dc — INDEPENDENT AUDIT of the arc-wide runner-idiom sweep

**Subject:** mg-ec63, the arc-wide truncate-before-probe sweep, which has merged;
and through it mg-03d1's three inherited figures **109 / 86 / 43**.

**The instruction was to re-derive them myself, so nothing here inherits a
number.** Where I quote one I say whose it is. Where I re-derive one I say with
what rule, over what population, at what revision.

Run `sh run_all.sh`. It clones this repository into `$TMPDIR` — **six clones,
one per worker** — and runs the arc's runners there. Nothing in the worktree is
executed, written or restored. The transcripts are built under `$V18_WORK`,
outside the repository, and land here only after the last probe exits.

**The headline correction is to my own hypothesis, not to the parent's number.**
I pre-registered that mg-ec63's `NEVER EXERCISED = 0` would prove non-empty. It
does not. The rule is still unsound and the answer is still right.

---

## PROVENANCE OF THESE TRANSCRIPTS — READ THIS FIRST

They are not all from one invocation, and the reason is a defect of mine.

| transcript | pass | why |
|---|---|---|
| `out_v3_bite.txt` | **pass 1** | pre-dates the `main` fix (SD14). See below. |
| everything else | **pass 2** | post-fix, one invocation of `run_all.sh` |

Midway through this audit I found that my disposable clone had **no local
`main`** — `git clone` creates only the source's current branch, which in a
polecat worktree is the polecat's own. The arc's probes resolve `main`
constantly, so many of them crashed for that reason alone. I fixed it and
re-ran the whole suite. The V3 re-run reached roughly 80% of its 109 trees and
was then **deliberately killed**: it had driven this shared host to a load
average of 65 and other agents work here. So V3 ships from pass 1.

**What that costs, stated rather than buried.** Pass-1 V3 ran probes that
sometimes died early on the missing `main`, so it saw fewer opens than it
should have. **Its 11 is biased DOWN**; the true figure is somewhere between 11
and 43, and mg-ec63's independent 19 sits in that interval. Every V3 conclusion
below is stated so that a downward bias cannot overturn it.

---

## The method, in one paragraph, because it is why the numbers differ

mg-03d1 matched a **regex** against runner source. mg-ec63 **parsed the shell**.
Both are statements about text, and a third rule of the same kind could only
join the argument. This **runs the shell** and watches the filesystem:
`python3` is replaced by a stub that writes a fixed marker and records, at the
instant it is invoked, **the size of every `out_*.txt` in its directory**. The
defect then has a direct observable — *is this transcript empty at the moment
its probe starts* — with no `>` in it and no regex. For the reading half an
`open`-audit hook records every open with its **mode, its pid and the size the
opener saw**; a read of a zero-byte transcript of one's own tree is the bite,
observed rather than inferred.

The stub writes a marker rather than nothing **on purpose**: a silent stub
leaves every transcript at zero bytes and makes `.new`+`mv` indistinguishable
from `>` — the exact collapse this ticket is about. The `.new`+`mv` trees are
the negative control and they come out clean, with their reads *seen and not
called empty*: 42 and 12 own-tree reads between them, none at size 0.

---

## THE ORDERING — the brief's first item, and it holds

From `git log --diff-filter=M`, not from the report's narrative. Over the window
from mg-03d1's carrier `eacc5e1` to mg-ec63's carrier `7fccb4e`:

| | |
|---|---|
| `code/*/run_all.sh` **added** | 4 |
| `code/*/run_all.sh` **modified** | 3 |
| …of those, in the sweep's own tree | 1 |
| …of those, in **any other tree that already existed at `eacc5e1`** | **0** |

**Zero.** The three modifications are mg-ec63 repairing its own runner and
mg-1abe repairing its own, twice — and mg-1abe's runner was itself *added*
inside the window, so it was never part of the swept population either. No
runner of the arc was edited between the count and the sweep. **The sweep ran
against an unrepaired arc.**

**One qualification, because the clean answer is the one nobody double-checks.**
`runner_exit_repair_bf79` was already fixed before *either* measurement. It is
the only instance in the arc with a known positive on the record — nine hidden
labels — and neither mg-03d1 nor mg-ec63 could observe it defective. For the one
tree that matters most, sweep-then-fix was already inverted, by a different
ticket, before this arc began. mg-ec63 saw this and re-ran its control at
`675c2ba` rather than at HEAD.

---

## 109 — RE-DERIVED, AND TRUE AT ONE REVISION THAT IS NOT ON `main`

My rule is `git ls-tree -r <rev> -- code/`, a property of a **commit**. mg-03d1
and mg-ec63 both globbed a **working directory**, which counts whatever was on
disk at one moment that no longer exists.

| revision | what it is | mine | shipped |
|---|---|---|---|
| `9f1ecaa` | mg-03d1 predictions (pre-rebase) | **108** | 109 ✗ |
| `d33970b` | mg-03d1 audit (pre-rebase) | **109** | 109 ✓ |
| `eacc5e1` | mg-03d1 audit — **the commit that carries the 109 onto `main`** | **112** | 109 ✗ |
| `3fc870a` | mg-ec63 instrument (pre-rebase, declared by its own S1) | **110** | 110 ✓ |
| `41972fb` | mg-ec63 evidence (pre-rebase) | **110** | 110 ✓ |
| `7fccb4e` | mg-ec63 evidence — **the commit that carries the 110 onto `main`** | **116** | 110 ✗ |

Three things follow, and none of them is "109 is wrong".

**One. mg-03d1's transcript declares `HEAD: 9f1ecaa`, where the tracked count is
108.** The missing member is `code/grain_axis_audit_03d1` — its own tree, still
untracked when the count was taken. The 109 reproduces only at `d33970b`, one
commit later. mg-03d1 recorded that its own tree joined the population it
counts; what it did not record is that **at the revision its own transcript
names, that member does not exist**.

**Two. Both totals are false in the commit that publishes them.** All four
predictions/evidence pairs in this lineage are **patch-id IDENTICAL and tree
DIFFERENT** — pre- and post-rebase twins. A rebase preserves the diff and moves
the base, and every population figure is a fact about the base. `eacc5e1` ships
`109 RUNNERS IN THE ARC` into a tree holding 112; `7fccb4e` ships `110` into a
tree holding 116. Neither was wrong when measured. Nothing in either tree says
so. *Patch-id adjudicates the diff; it is not an oracle about the tree.*

**Three. Six runners at `7fccb4e` were never in the sweep's population**, and
the first is `code/grain_axis_audit_03d1` — the tree whose three numbers the
sweep exists to re-derive. mg-ec63's S1a prints `code/grain_axis_audit_03d1
present here:  NO` and reasons from its absence. **It is present in the commit
that ships that sentence.**

---

## 86 — RE-DERIVED BY EXECUTION: I get **88**

Over the 109 runners at `d33970b` — mg-03d1's own tree state, which is the only
way a disagreement means anything.

| rule | number | over |
|---|---|---|
| mg-03d1, regex over source, **re-run by me** | **86** | 109 at `d33970b` |
| mg-ec63, shell parser over source | 96 | *110 at `3fc870a` — a different population, named and not subtracted* |
| **mg-18dc, execution of the shell** | **88** | 109 at `d33970b` |

I reproduce mg-03d1's 86 **exactly** by running its rule as written, so the
disagreement is entirely about the rule and not about the population.

- **1 false positive.** `state_landing_control_2da3` — the source says `>`, and
  no probe of that run ever starts on an empty transcript.
- **3 false negatives.** `branching_bound_audit_aaf4`, `branching_bound_d075`,
  `face_geometry_audit_fcb2` — the source does not match and step 0 demonstrably
  starts with its transcript at zero bytes.

**The negative control:** the two `.new`+`mv` runners come out with no probe
starting on an empty transcript. If my instrument called them truncating too it
would be measuring *does a runner write files*, not *does the fix work*.

**Both figures are lower bounds** and V2a says so where they are printed: 0
runners timed out and 0 invoked no `python3`, but a runner whose truncation sits
behind a failure branch is never reached by a stub that always exits 0.

---

## 43 — RE-DERIVED: **11 trees / 16 transcripts**, with 27 unmeasured

The bite is measured as **one** observation rather than two rules conjoined: a
process opens an `out_*.txt` **of its own tree**, for **reading**, and the file
**has zero bytes at that moment**.

| rule | number | over |
|---|---|---|
| mg-03d1, two regexes conjoined, **re-run by me** | **43** | 109 at `d33970b` |
| mg-ec63, audit hook on the probe's own transcript | 19 trees / 32 steps | *110 at `3fc870a`* |
| **mg-18dc, size==0 at the `open` call** | **11 trees / 16 transcripts** | 109 at `d33970b` |

Again I reproduce mg-03d1's 43 exactly from its own rule, so the gap is the
rule. **36 of its 43 are false positives** and **4 trees it misses do bite**.
The false positives split two ways and the split matters:

- trees whose probes read their own transcripts **and never an empty one**;
- trees where **no own-tree transcript is read at all**, so the second half of
  the conjunction is simply false.

**27 of the 109 were killed at the 420 s timeout and are UNMEASURED, not
clean.** They are named in the transcript and they sit inside the denominator.
The killed set was **not stable between passes** — 22 at a 240 s timeout, 27 at
420 s, because the machine was busier — so "unmeasured" is not even a fixed list
of trees.

**The direction of mg-ec63's correction is independently confirmed.** My 11 is
biased down (see PROVENANCE) and mg-ec63's 19 is over a slightly larger
population; 43 is roughly three to four times either. mg-ec63 was right that 43
is inflated, and right about roughly how much, by a method sharing nothing with
mine.

**The instrument is shown firing in both directions**, which is the only reason
the negative half means anything: across the pass it recorded **788 reads of a
populated transcript and 107 of an empty one**. A broken hook gives 0 and 0; a
size read after the fact rather than at the call gives 0 for the second.

---

## THE THIRD OUTCOME — the rule is unsound and the answer is right

mg-ec63's `classify()` (`s3_sweep.py:89-106`) reaches `NEVER EXERCISED` only
through

```
b_broke = B timed out or B raised a Traceback
a_ok    = A did not time out and did not raise
if b_broke and a_ok:  return "NEVER EXERCISED"
```

**B is the healthy arm. A is the defect arm — the one the arc has been
shipping.** So the verdict fires only when the *populated* run breaks and the
*emptied* run works. The outcome the ticket names — *the probe cannot run at all
against real input* — fails **both** arms, is therefore `A == B`, and falls
through to **`SAME`: "the ordering bug cost the arc nothing."** Fed a
constructed row that raises the same traceback in both arms, mg-ec63's rule
returns `SAME` and mine returns `CANNOT RUN AT ALL`. **The reported 0 is a
property of the rule before it is a fact about the arc.**

**And then the class turns out to be empty anyway.** Re-running mg-ec63's own 25
`SAME` and `NONDETERMINISTIC` steps at its own tree state `3fc870a`:

| | |
|---|---|
| CANNOT RUN AT ALL — traceback in both arms | **0** |
| BREAKS ONLY UNDER THE DEFECT — the shipped arm crashes | **0** |
| NEVER EXERCISED, mg-ec63's sense | **0** |
| DIFFERENT | **9** |
| INERT READ — reads the emptied file, same answer either way | **13** |
| SAME, no read observed | **1** |
| one arm timed out — **unmeasured** | **2** |

**So P5a is a MISS and it is kept as written.** mg-ec63's 0 is unsupported by
its own reasoning and correct in fact. Those are different criticisms and only
the first survives.

**The finding that does survive is next to it.** Split by what mg-ec63 recorded:

- of its **11 `SAME`** steps: **10 INERT READ + 1 SAME**. Every one is genuinely
  same. mg-ec63 was right about all eleven.
- of its **14 `NONDETERMINISTIC`** steps: **9 come out DIFFERENT** on my re-run,
  3 INERT READ, 2 unmeasured.

mg-ec63's own WHAT I DID NOT DO says *"I did not investigate the 14
NONDETERMINISTIC steps. They are excluded from DIFFERENT by a control, not
explained."* Nine of them show a delta between the emptied and the populated
arm. That does not make them DIFFERENT — a probe that is genuinely
nondeterministic will show a delta for reasons unrelated to the shape, which is
exactly why the control exists. It does mean **the headline `4 DIFFERENT` is a
floor over a population with 14 unexplained rows beneath it**, and that nine of
those rows are where a reader would want to look first.

---

## THE FIX'S CONVERGENCE, AND THE RESTORE

mg-03d1's A4d verified **6 of 6** transcripts byte-identical over two runs of
`runner_exit_repair_bf79`. Re-verified on a tree it did **not** use —
`code/grain_axis_audit_03d1`, its own, which A4d excluded from `subjects` by
name:

| | |
|---|---|
| transcripts written by each run | **7** |
| byte-identical across two consecutive runs | **6** |
| **still differing on the second run** | **1** — `out_a1_axes.txt` |

**6 of 6 does not generalise to 7 of 7.** The `.new`+`mv` fix removes the
self-emptying transcript; it does not make a suite converge, and mg-03d1's own
tree is the counter-example.

**The restore, checked by hash rather than by status** as the brief asks: **6**
transcripts differ from committed before the restore, **0** after. The BEFORE
row is printed precisely so the check cannot pass vacuously — a run that dirtied
nothing would make the restore untestable.

**P7 is a MISS.** I predicted A4d's one-directory `git status` assertion would
be narrower than the run it guards. Measured over the whole clone: **6 paths
dirty inside the subject directory, 0 outside**. The scope is narrower in
principle and adequate in fact for the tree it was written for.

---

## THE SHAPE ELSEWHERE — the sibling the brief names is already gone

Re-derived at HEAD over 117 runners. **My first attempt was wrong and the way it
was wrong is the finding underneath it.**

| | first draft | corrected |
|---|---|---|
| runners using `\| tee` | 23 | **1** |
| runners setting `pipefail` | 31 | **2** |
| runners using `tee` **without** `pipefail` | 20 | **0** |

29 of the 31 "setting `pipefail`" are **comments** — *"`set -o pipefail` is not
used: /bin/sh is dash on Linux, which rejects the option"* — the single most
repeated line in this arc's runners; 22 of the 23 `tee` matches are the same
kind. **A rule that reads a comment as code turned a 2 into a 31.** All of my
rules over runner source now go through `lib18dc.code_of`; the rules I
*reproduce* from mg-03d1 deliberately do not, because re-deriving its 86 means
running its rule as written.

Corrected, the answer to the brief's question is: **the two populations do not
overlap, because one of them is empty.** The `tee`-without-`pipefail` shape that
mg-c2b3 found at 23 of 63 is **0** at HEAD, while `>`-before-probe stands at
**92 of 117**. The brief's own figure for it — "only 1 setting pipefail" — is
already contradicted inside the tree it cites: mg-c2b3's `out_k1_census.txt`
prints `ticket 1  re-derived 0  DIFFERS`.

### Does the repair address the SHAPE, or only the 43?

**Only the 43, and mg-ec63 says so itself.** At `7fccb4e`:

| | |
|---|---|
| runners carrying the `.new`+`mv` structural fix | **2** |
| runners writing transcripts outside the repository | **4** |
| **runners still starting a probe on an empty transcript** | **92 of 117** |

That is the correct outcome of a ticket ordered *sweep first, fix second*, and
it is also the state of the repair: **the shape is measured and unrepaired.**
The four trees mg-ec63 named as changing their answer are named in its own
README, and its WHAT-I-DID-NOT-DO records that no ticket was opened for any.

---

## MATERIAL BEYOND THE BRIEF

**A commit whose subject announces a repair its own diff does not contain.**
`2bf262f`'s subject reads *"S1a PRINTS THREE NUMBERS INSTEAD OF ASSERTING TWO
AGREE … and the sentence that said 'THE TOTALS AGREE' is gone because it stopped
being true when my own runner landed"*. That commit touches `README.md` and
`out_s2_bite.txt.new`. **It does not touch `s1_population.py`**, which has been
modified by exactly one commit in its life, `8313882`. Checkable in three lines:

- `s1_population.py:40` still prints `mg-03d1's sweep also says 109.  THE TOTALS
  AGREE AND THE POPULATIONS DO NOT`.
- `out_s1_population.txt` still contains it — **six lines under its own printed
  total of 110**, which the sentence contradicts.
- mg-ec63's README says of that sentence *"it is gone rather than patched"*. It
  is in the source and in the shipped transcript.

The repair was made **in the README's prose** — the three-number table there is
real and correct — and announced in a commit subject as though it had been made
in the code. Source and transcript agree with each other and disagree with both
the commit message and the README. Not a wrong number: a repair that exists only
in prose while its commit message says otherwise, in a lineage whose whole
subject is claims that outrun their evidence.

**A committed `.new` leftover.** `2bf262f` also added
`code/truncate_sweep_ec63/out_s2_bite.txt.new` to the tree — mg-03d1's A4c names
exactly this as the limit of the `.new`+`mv` fix. It was committed and removed
two commits later. The predicted artifact of the fix reached `main`.

---

## PREDICTIONS, SCORED

Nine hit, three missed, one unscored. See `OUTCOMES.md`. Two of the misses are
misses because of defects in my own instrument, and that is said where it
happened rather than repaired backwards into a hit.

---

## DEFECTS OF THIS INSTRUMENT

**Thirteen**, in `out_v7_self.txt`. Four are worth naming here because they are
the audited defect class committed by the auditor:

- **SD12 — this suite's own V4 transcript was destroyed by this suite**, leaving
  a 19-byte file holding the stub's marker: a vacuous pass of exactly this
  ticket's shape. `run_all.sh` exports `$V18_WORK`, the arc's runners inherit
  the environment, and this directory became a `code/*/run_all.sh` the moment it
  had a runner — so V6's sweep of HEAD ran **my own runner** over the file V4 was
  writing. **The re-entrancy guard did not fire**: `V18_RUNNING` is set by the
  *runner*, and the collision came from a *probe* invoked directly. A guard on
  the runner does not protect a probe. Repaired structurally, not with a second
  guard.
- **SD14 — the disposable clone had no `main`, and it manufactured this audit's
  headline.** Six steps read as CANNOT RUN AT ALL — precisely the finding I was
  sent to look for — and all six were my harness. Caught by reading a traceback
  instead of counting it.
- **SD13 — a clean bill of health over an empty population, in the section about
  my own defects.** V7c printed `0 invocations / 0 emptied` and concluded my
  runner was clean; the runner had refused to start on an inherited
  `V18_RUNNING`. It now reports 8 invocations and 0 emptied, which is a result.
- **SD9/SD8/SD10/SD1/SD2** — a comment read as code (twice), an `all` over an
  empty set, a row name that was not its measurement, and a selftest assertion
  that could not fail on the property it named.

**And my own runner, measured the way everything else here is measured** — by
running it under the stub, not by reading it: **8 invocations, 0 starting on an
empty transcript of this tree.** mg-ec63's S6a got the analogous question wrong
in the other direction and corrected it in prose; an execution measurement
cannot make that mistake because it looks at the file.

**The population contains the counter**, for the third audit running: 117
runners at HEAD including this one, 116 excluding it. Both are printed.

---

## WHAT I DID NOT DO

- **I did not complete a post-`main`-fix V3 pass.** It reached ~80% and was
  killed for degrading a shared host. V3's 11 is biased down and the bias is
  named where the number is printed.
- **I did not resolve the 27 trees killed at the timeout.** Unmeasured, not
  clean, and the set is not stable between passes.
- **I did not re-run mg-ec63's 32-step EMPTIED population from scratch.** V4
  re-runs the 25 steps where a collapse would hide and takes its `DIFFERENT` and
  `TIMED OUT` rows on trust.
- **I did not run any probe at its own publishing revision**, so mg-ec63's three
  *suspect* trees are still suspect. It remains the largest open piece of work in
  this arc and this audit does not close it.
- **I did not investigate the 9 NONDETERMINISTIC steps that come out DIFFERENT.**
  I established that they are worth investigating; I did not investigate them.
- **I did not measure the STALE class at all.** mg-ec63 counts 12 steps in 11
  further trees; I measure only EMPTIED.
- **I did not open a ticket for the `2bf262f` finding.** It is recorded here.
- **I did not repair any runner**, for the reason mg-ec63 gave: the ticket orders
  sweep-then-fix, and this is an audit of the sweep.
