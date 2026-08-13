# mg-585e — A TRANSCRIPT WHOSE TEXT IS A FUNCTION OF THE VERDICT OSCILLATES BY CONSTRUCTION

Successor carrier for `mg-5987`.  The ticket names two carry-forward candidates and says they
are pm-onethird's call.  **This directory answers the first one and does not touch the second**,
which belongs to `mg-05c6` (dispatched as p05c6) and is named in §5 only where the two meet.

    1.  Whether a self-exempting transcript can be made NON-OSCILLATING — e.g. by recording
        the verdict's *inputs* rather than its *outcome*, so its text is not a function of
        what it reports.

**The answer is yes, it is exhibited running, and it is not vacuous.**  What it costs is one
sentence, and the sentence is stated in §4 rather than buried.

---

## §1  THE FINDING, AND IT IS NOT ABOUT VERDICTS

`lib_f771.SELF_EXCLUDED` gives the reason for the exemption as: the transcript is written
after the measurement and **its text depends on the verdict**.  That is true and it is a
symptom.  The operative property does not mention verdicts at all:

> `g0` runs at tree `T` and its output is committed into tree `T'`.  The repair that produces
> `T'` is *commit the regenerated transcripts*.  `g0`'s §2 reports `D(T)`, the set of
> transcripts whose committed copy disagrees.  **`D(T') = {}` by definition of the repair.**
> So whenever `D(T)` is non-empty the committed text is false about the tree it lands in, and
> it is false *because* that commit repaired it.

A transcript cannot record a quantity that its own commit sets to zero.  Stating it that way
is what makes the rest decidable: content is safe iff it is **invariant under the repair**, and
the repair rewrites transcript bytes and nothing else.

**This is why `g0`'s own docstring rule is the mistake.**  It says *"Only the DISAGREES list,
which is repo state, is on stdout"*.  The DISAGREES list **is** repo state — of the tree at run
time, which is not the tree the file is committed into.  *Is it repo state* is the wrong test;
*does the repair move it* is the right one.  The two tests disagree on exactly one item, and
that item is the whole of §2.  (Predicted as P8, confirmed by `v2` §4.)

---

## §2  THE OSCILLATION, COUNTED OVER THE RECORD — `v1`

`lib_f771` justifies the exemption with *"measured over five runs … the oscillation does not
damp"*.  Five runs in one worktree was the evidence available then.  The evidence available now
is the file's own committed history, walked from a pinned `AS_OF` (`0cb0fa4`, checked to resolve
and to be an ancestor of `origin/main`, so this transcript cannot go stale when its subject
next moves):

| | |
|---|---|
| committed versions of `out_g0_fixed_point.txt` | **31** |
| RED-shaped (`THE DISAGREEMENTS, SHOWN`) | **16** |
| shape flips between consecutive versions | **24** |
| commits touching **that file and nothing else** | **7** |

Two of those rows are the finding.

**24 flips over 31 versions is what "does not damp" looks like counted rather than described** —
almost no commit inherits a transcript that is still true.

**7 commits exist on `main` for nothing but turning that file green.**  Each is a second
`./build.sh` run and a second trip through the merge queue, spent on a file that went red
*because the tree got fixed*.  Their subjects say so out loud: `refresh: THE FIXED-POINT
TRANSCRIPT SAYS GREEN AND IT IS THE ONLY FILE THIS RUN COMMITS`, five times.

**A LOWER BOUND, NOT A TOTAL.**  `v1` reads *committed* versions; a red run that its author
re-ran before committing leaves no trace.  So the oscillation happened at least this often and
reached `main` exactly this often.

The asymmetry in §4 of that transcript is the mechanism in one line: the 15 green versions
collapse onto **three** distinct byte sizes (essentially one text), the 16 RED ones onto
**fifteen** — green is a fixed point of the run, RED is never a fixed point of the commit that
carries it, because that commit is the repair.

---

## §3  WHERE IT LIVES — `v2`, LOCATED BY RUNNING

Three miniature repositories differing in one line of one watched transcript — untouched
(`green`), a moved wall-clock (`noise`), a moved **count** (`red`) — with **the real
`g0_fixed_point.py` copied in and run as a subprocess** against each.  Not re-implemented:
a re-spelling would make every line below a statement about the re-spelling (mg-d2c2, and
mg-f771's own `g1` obeys the same rule).

| measured | |
|---|---|
| everything up to the `§2` heading, red vs green | **byte-identical** (24 lines) |
| `§2` onward | 7 lines green, 18 lines red |
| green tree vs noise tree | **identical** |
| two independent green sandboxes (seconds scrubbed) | **identical** |

The last row is the control that makes the third attributable: what moves between red and green
moves *because of the verdict*, not because two runs of anything differ.

So **the transcript already splits cleanly at `g0`'s own §-boundary**, and §1 — the watched
class, the exemption, the two declared noise families — is *already* invariant.  The whole
oscillating surface is §2 plus the `VERDICT` line.

---

## §4  THE CANDIDATE ANSWER — `v3`, BUILT AND PRICED

`lib585e.invariant_report` is a transcript of the verdict's **inputs**: the watched-class rule,
the exemption list, the normaliser's rule inventory in readable form, and a `sha256` of the four
functions that actually decide.  Every field is invariant under the repair.

**It does not oscillate.**  Byte-identical on the red, green and noise trees — 1745 bytes, with
**no scrubbing applied to either side, because there is no clock in it at all**.

**And the test can fail.**  The same writer with the outcome appended — today's arrangement —
goes through the identical comparison and comes back **CAUGHT**.

**It is not vacuous, which is the half that matters.**  A constant file also never oscillates
and buys nothing: admitting it to the watched class would add a file that *cannot* disagree.
So the wrong-direction test widens `N2` in a sandbox to eat integer seconds — the exact escape
hatch `lib_f771`'s own docstring names as unfalsifiable — and requires the report to move.  It
moves, legibly, one line:

```
-  SECONDS      re.compile(r"\b\d+\.\d+\s*s\b")
+  SECONDS      re.compile(r"\b\d+(?:\.\d+)?\s*s\b")
```

**So the exemption becomes removable, and the removal buys something specific.**  `lib_f771`
names its own main risk: *"A WIDER NORMALISER IS AN UNFALSIFIABLE ESCAPE HATCH — an operator
facing a real disagreement can silence it by widening the rule, and nothing in the machinery
tells that edit from a correct one."*  With the report inside the watched class, an operator who
widens the rule and does not re-run the gate is caught **by the control they widened**.

**Nothing is lost that was not already elsewhere.**  On the red tree, today, with no change to
`g0`: exit status `1`, and stderr already names the disagreeing file.  The exit status is what
`run_all.sh` reads and what `build.sh` folds into the gate verdict — **the outcome has never
travelled to the merge gate through the transcript** — and the per-file grading is already on
stderr by `g0`'s own design (README D4).  The proposal moves one more line to a channel already
carrying its neighbours.

**WHAT IS GENUINELY LOST, AND IT IS ONE SENTENCE:** the committed file stops being quotable for
*was the gate green*.  mg-f771's own diagnosis is the reply — the file that opened that ticket
was stale precisely **because** the quotable part was the verdict, and `lib_f771`'s first
paragraph says so: *"the part written to be quotable was the wrong half."*

---

## §5  THE OTHER INVARIANT CONTENT IS THE WORSE TRADE, AND IT IS PRICED RATHER THAN ARGUED

A **census** of the watched class is also invariant under the repair, so it would also stop the
oscillation.  Over the window from the transcript's introducing commit to the pin
(`137bc4ce..0cb0fa4`, 129 commits touching `code/`):

| | |
|---|---|
| commits that ADD or DELETE a tracked `code/**/out_*.txt` | **31** |
| commits that touched `out_g0_fixed_point.txt` | **30** |
| in **both** sets | **4** |

⚠ **The 31 and the 30 are different quantities over the same window and their near-equality is
arithmetic, not identity** — the overlap row is what says so.  Read together they say the trade
buys nothing: a census moves about as often as the verdict does, on a nearly disjoint set of
commits, and it moves into **`mg-05c6`'s conflict class** — the file every concurrent branch
must regenerate — instead of into an extra commit in one worktree.  Swapping an oscillation in a
worktree for a conflict in the merge queue is a worse trade at the same frequency.

**The rule inventory moves on neither.**  It is a function of `lib_f771.py`, which neither the
repair nor a new directory under `code/` touches.  Of the three candidates it is the only one
invariant under **both**.

This is where this directory and `mg-05c6` touch and it is the only place: `mg-05c6` owns the
conflict class, and this measurement says *do not enlarge it*.  The ticket's second carry-forward
candidate — a pre-submit rebase check — is not addressed here.

---

## §6  WHAT THIS DIRECTORY DELIBERATELY DOES NOT DO

**It does not edit `code/gate_fixed_point_f771`.**  The proposal is exhibited in this directory,
run against sandboxes, and priced.  Landing it means rewriting another ticket's arm, its `g1`
membership row `E1`, its README and its `SELF_EXCLUDED` tuple — a change to an instrument this
branch does not own, on a question the ticket puts to pm-onethird.  A demonstration that is
binding by the back door is not a demonstration.

**It is not in `build.sh`.**  There is nothing here for the merge gate to enforce, and adding an
arm that grades a proposal would make the proposal binding the same way.

`STATE.md` is untouched, `docs/FACTS.md` gets no entry (every measurement here is consumed by
this landing — mg-3da1's homelessness test), and `docs/CONCEPTS.md` gets no row.

---

## §7  CONTROLS — `v0`, AND IT RUNS LAST

Five scrubber worlds (two must fire, **three must not** — an integer is not a second, or every
count in every compared transcript would be invisible), four plants, three refusals, and an
own-output scan.  `v0` runs **last** because its §4 scans the transcripts the other three arms
have just written; a scan of the previous run's transcripts grades a tree nobody is committing.

**D1 FIRED ON THIS DIRECTORY'S OWN CONSTRUCTION AND THE MATCHER WAS TIGHTENED RATHER THAN THE
PLANT RELAXED.**  The digest identified its four deciding functions by the prefix
`"def verdict_for"`, and the plant renames one to `def verdict_for_RENAMED(` — which *starts
with* that prefix.  The first run came back **INERT**: a digest was returned, covering a
function that no longer exists under the name it was asked about.  The names now carry their
opening parenthesis.

**AND THIS DIRECTORY REPRODUCED mg-f771's README D4 IN ITSELF, ON ITS SECOND RUN.**  `v2` §1
printed `g0`'s verdict line verbatim, wall clock and all, so `out_v2_partition.txt` failed to
reproduce (`0.03s` → `0.04s`) and the raw-bytes-identical row flipped `YES`/`no` with the
rounding.  Caught by running the suite twice and comparing, not by reading it.  The remedy is
D4's own: the seconds are scrubbed before printing and **the raw-identity result went to
stderr**, where the build log keeps it and no tracked file does.  A directory whose whole
subject is a transcript that cannot be a fixed point had, on its second run, a transcript that
was not a fixed point.

**mg-9876's SMELL INDEX COUNTS THIS DIRECTORY TWICE, THE DECISION IT COUNTED WAS REPAIRED, AND
THE COUNT DID NOT MOVE — WHICH IS THE INTERESTING PART.**  The index goes
`220 → 222 in 76 of 232 → 77 of 233`, and both sites are this directory's.  One was real:
`v1` classified a committed version by `RED_MARK in text`, a membership test against a whole
captured output — mg-9876 §1's smell exactly, in the arm that reads 31 transcripts.  That arm's
own instruction is that a candidate is not a defect until it is **run both ways**, so it was:
across all 31 versions the string occurs **0 times outside the `§2` heading**, so the loose form
is not wrong today.  It is unguarded for tomorrow — one line of prose quoting the heading and
every version reads RED forever — so the decision is now line-anchored.

**And the index still reads 2, because running a predicate both ways means KEEPING the loose
form in the file as the control.**  `loose_red` exists only to let `v1` §1 print
`anchored and loose disagree: 0 of 31`.  mg-9876 §1 counts the site whether it is the decision
or the control, and it cannot tell them apart — the same shape as `mg-9876`'s other rows that
cannot read English.  **Reported and not repaired**, because that row belongs to mg-9876 and a
branch that re-scoped another instrument's detector to make its own number look better would be
doing the worse thing.  The second site, `lib585e.py`'s `if old not in text:`, is the guarded
shape: it refuses when a sandbox patch anchor is absent, and its two-way run is `v0`'s `D1` and
`D2`, which are exactly the worlds in which that anchor is gone.

**Declared blind spots.** The sandboxes hold one watched transcript; nothing measured here says
what `g0` does when several disagree at once, and `v3`'s claim is that the proposed report does
not mention them at all — an argument, named as one.  Nothing runs the proposed report inside
`code/gate_fixed_point_f771`, per §6.

**Reproducibility:** two consecutive `sh run_all.sh` runs are **byte-identical on all four
transcripts**, ~6 s.  Every figure in `v1` and `v3` §4 is a function of two commits; the sandbox
arms have no clock left in their output and no randomness or sampling anywhere.

---

## §8  RECOMMENDATION TO pm-onethird

1. **Candidate 1 is available and cheap.**  Replace `g0`'s §2 with the rule inventory, keep the
   outcome in the exit status and on stderr, and **delete `SELF_EXCLUDED`** — the watched class
   becomes total and the normaliser's escape hatch acquires the only guard it has ever had.
   Price: one sentence of quotability, and mg-f771's own first paragraph already argues that
   sentence was the wrong half.
2. **Do not reach for a census to do it.**  §5 prices that route; it relocates the churn into
   `mg-05c6`'s conflict class at the same frequency.
3. **Candidate 2 is not answered here** and should stay with `mg-05c6`.
