# mg-d3f3 — independent audit of mg-8af0's F1/F2/F3 repair

**Pre-filed as a SAME ACTION alongside mg-8af0.** `PREDICTIONS.md` was committed at
`d698bfa`, before a line of this audit's code existed. Six instruments, 44 checks, exit 0.
Nothing outside `code/face_geometry_audit_d3f3/` is edited — no frozen transcript is
regenerated, no repair is applied.

---

## The verdict, in one paragraph

**F2 was fixed before F1 and the fix is real: the V6 rows are scored against the artifact,
the source and a fresh run, and none of them is a condition on a literal beside it.**
`a3.7/Z1` shows the inversion directly — moving the declared census with the repository
untouched turns V6b **red**, where mg-e35b's row went green on exactly that input.

**But the mechanism F2 named is not what hid F1, and the repair's own disclosure points at
the wrong remedy.** Put mg-fcb2's F1 back at the source and **nothing in the repair goes
red** — not V6a, V6b, V6c, V6d, V7, either demonstration, or any of the three probes; 0 of
35 artefacts (`a1`). Run mg-8af0's **complete** repaired verifier against the tree **as it
was before mg-8af0 touched it** and it reports **28 checks, 0 refuted** (`a5.3`). The
instrument does not separate the repaired tree from the unrepaired one, because every
difference the repair made lives in prose, in the operand of one `%` expression, and in the
verifier's own `TABLE` — and **no row of the verifier reads any of those three**.

---

## Correcting the ticket's framing, which is what it asked for

> "V6a is the row that must catch an F1-shaped defect. CONSTRUCT ONE and confirm V6a goes
> red."

**That instruction cannot be satisfied, and the reason is mg-8af0's own E1.** F1's repair
changed no digit — 86/86 before, 86/86 after — so F1's *return* changes no digit either.
V6a is `anchor in artifact` over twelve literal strings; V6c and V6d compare byte-for-byte
against the same artifact. **A substring test on unchanged bytes cannot move.** Measured
(`a1.1`): the revert regenerates `controls_output.txt` at **41081 bytes against the
committed 41081**, byte-identical.

So the construction runs the other way round: put F1 back, then build the whole candidate
space of things that could notice, and count. `a1` also carries the wrong-direction control
that makes the count mean something — **X2**, a tautology that prints *different* digits
(`% (N - 1, N, …)` → 85/86). X2 turns V6a and V7 red and exits 1. X1 and X2 are the same
defect class; **what separates them is not the defect, it is whether the digits happened to
move.**

---

## The findings

### F-1 — the declared limit is true, and the remedy it names is false

`a3.2`. The limit is declared at four sites. Two of them do not stop at the census; they go
on to name the fix:

- the demonstration: *"That is why F1 needed a row of its own (V7) and not just a census."*
- the README: *"That is why F1 needed V7 and not just a census."*

`a1.2` ran **V7 with F1 present** and V7 came out **green**. V7 checks
`site == 86 and "corrupted on 86/86 posets" in art`; both halves are true whichever
expression produced the digits. Naming a remedy that does not remedy is the half of a
declared limit that reads as candour.

**And the file is honest where the README is not** (`a3.3`): V7's own comment says *"What
this row CANNOT do is tell whether 86/86 is the right answer for the right reason — it is
one more route to one number,"* and that hedge is printed into the transcript. The two
disagree. The README is the site to fix.

**My own prediction P2a is refuted here, by the most careful of the four sites** (`a3.1a`).
I predicted all four name V6b alone. The demonstration's line reads *"…**the three rows**
catch every way a count could be added. V6b is a tripwire … moves none of **them**"* — and
on the reading where *them* is the three rows, mg-8af0 declared the limit for V6a, V6b
**and** V6c, which is more than I gave it credit for. The antecedent is genuinely ambiguous
(*"them"* could be the printed positions) and this audit does not resolve it in either
direction. **What neither reading covers is V7.**

### F-2 — no artefact in the repair ever reads the operand side of a `%`-expression

`a3.5`, and this is the sharpest form of F-1. A `%`-format `BinOp` has two children:
`left`, the format string, and `right`, the operand tuple. **F1 was a defect in `.right`**
— the same name twice. Measured across every source-reading artefact in the repair:

| | `.left` accesses | `.right` accesses |
|---|---|---|
| `verify_e35b.py` | 2 | **0** |
| `demo_f2_row_can_go_red.py` | 0 | **0** |
| `demo_v6d_row_can_go_red.py` | 0 | **0** |

So the census could not have seen F1 *whatever its population had been*, and the row that
could have — a five-line `ast` check that the operand tuple at the site does not repeat a
name — is the one this repair did not write. **V4a shows the repair knows how to write
exactly that kind of row, for exactly that kind of claim** (it `ast`-parses
`face_complex.py` to establish that `at_laplacian` takes no incidence argument). The
technique was in the file; it was not pointed at the defect.

### F-3 — V6b's row name is not V6b's measurement, in two directions

`a2`. The name asserts *"NEGATIVE CONTROL 4 prints 210 formatted values and **no count has
been added or removed** since this table was written."* What is measured is a seven-field
dict of conversion-type **multiplicities**.

- **Y1b — add and remove.** One `%d`-bearing count removed from
  `negative_control_incidence` and a different one added. Census identical, **all rows
  green, exit 0.** A count was added and a count was removed.
- **Y2 — out of population.** `controls_output.txt` is the output of **eleven** calls in
  `main()`, of which `negative_control_incidence` is one. A printed count added to the
  sibling `negative_control_construction` **reaches the artifact** and moves none of
  V6a/V6b/V6c/V6d, **exit 0.** The docstring's claim for V6c — *"a count **cannot** be
  added to the artifact without moving V6b"* — is false as written.
- **Y3 — the wrong-direction control.** The same count added *inside* the section turns
  V6b **and** V6d red, exit 1. So Y1b and Y2 are not reporting a census that never fires.

**Is "TRIPWIRE" the honest word?** Honest about the **mechanism** — it fires on a change
rather than proving a correspondence, and the row says so. Not honest about the **scope**,
and the scope is the half a reader scores the repair by. `census()`'s docstring states the
population correctly, twice; the row name does not carry it. **The repair is one clause:
put the population in the name.** (Recommended, not applied — nothing here is edited.)

### F-4 — the repaired verifier was never watched failing on the real tree

`a4.4`, and **my prediction P7b is refuted**. I predicted the F2 commit would exit 1 with
one refuted row. The committed transcripts say:

| commit | | |
|---|---|---|
| `0c3a2ba` F2 | 26 checks | **0 refuted** |
| `534c06b` F1 | 27 checks | **0 refuted** |
| `66130f8` F3 | 28 checks | **0 refuted** |

So on the branch that landed, **F2-before-F1 is a commit ordering, not a demonstration.**
The ordering was mandated and correctly obeyed; what it is not is *evidence*, and `a1`
says why it could not have been. Worth recording: the **sibling** branch of the same ticket
(`0c39f34`, never merged — the double dispatch of `1d89a29`) *did* exit 1 at its F2 commit,
because it added V7 at F2 time rather than at F1 time.

### F-5 — E10's fourth row is scored HIT and was never run

`a5`. `PREDICTIONS.md` E10 is five exit codes; the README scores the table **"HIT, 5/5"**.
Four have a committed artefact behind them. The fourth —

> `verify_e35b.py` **repaired**, against the **pre-repair** artifact → **1**

— has none, and nothing in the repair builds that world. This audit built it, from git, in
all three readings the sentence admits:

| reading | measured | E10 said | |
|---|---|---|---|
| R-a the whole pre-repair tree (`5f542f0`), repaired verifier (`66130f8`) | **0** | 1 | MISS |
| R-b the repaired tree with a stale artifact from `5f542f0` | **1** | 1 | HIT |
| R-c the real tree at the F2 commit | **0** | 1 | MISS |

**HIT under one reading of three, and the one that comes out 1 is the stale-artifact
reading, where V6c fires — and V6c is a row about staleness, not about F1.** Under both
readings that are *about F1*, the answer is 0. mg-8af0 draws the run/reasoned distinction
elsewhere repeatedly and at its own expense; this is the one place it does not.

### F-6 — the E6a caveat does not check out against its own hypothesis

`a3.6`. The README says: *"What the miss changes: with 184 sites and 12 table entries there
is no per-count mapping available, so V6b **cannot** be a coverage check and is scored as a
tripwire."* But **E6a itself derived that conclusion before measuring anything**, from
`SITES > 11`:

> *"E6a — SITES … is **more than 11** … so no per-row mapping is available and the census
> must be reported at its own grain."*

85 > 11 and 184 > 11 give the same verdict. **The 2.2× miss is not what made V6b a
tripwire; the reason was already in the prediction that missed.** The addendum asked
whether the miss and the limitation "agree". They do not disagree about a *number* — both
say 184 — they disagree about a *cause*. What the miss is really evidence about is reading
a thousand-line function by eye, and that sentence is not in the scoring table.

---

## What is NOT a finding, said explicitly

The brief asks for status language both ways, so these are recorded as **clean**:

- **The three rows really are scored against things outside the file** (P5a, `a3.7/Z1`).
  V6a's measured side is the artifact, V6b's is `controls.py`'s source text, V6c's is a
  subprocess run, V6d's is an instrumented run. In every case the in-file literal is the
  *declared* side. Moving the literal alone produces a **red**, which is the exact
  inversion of F2. **F2 has not been reintroduced in a new dress.**
- **"C4 is red for V6a alone" reproduces** (`a3.9`), and `demo_f2_row_can_go_red.py`
  reproduces its committed transcript **byte for byte**, 1849 bytes, exit 0. No replacement
  row is redundant. *But C4 is not F1-shaped* — it changes a printed string, so the
  artifact moves; the count of the five constructions that leave the artifact
  byte-identical is **0**.
- **Deleting an entry from `TABLE` moves nothing** (`a3.7/Z2`) — V6a's population *is*
  `TABLE`. This is the design's **stated** boundary: `forced` and `len(TABLE)` are printed
  and explicitly *not scored*, because scoring them is what F2 was. Correctly declared, not
  a defect.
- **The eight declared omissions are genuinely out of scope** (`a4.6`–`a4.10`): mg-fcb2's
  **F4** is not in mg-8af0's brief, which names F1/F2/F3 and nothing else, stated in its own
  PREDICTIONS before any code existed; **STATE.md** is untouched across all nine commits;
  **n > 6** really is unswept (`NMAX = 6`); and **A1.4a** scores `worst >= 3`, a claim about
  the *mathematics*, so it correctly stays `[REFUTED]` after a repair that changed wording.
- **E9's half-miss is recorded honestly** (`a4.5`): the F1 commit does touch
  `verify_e35b.py`, and the README scores it HALF-MISS rather than rounding it to a hit.
- **The addendum's four commit hashes are pre-rebase** (`a4.1`, `a4.2`). None is an ancestor
  of main; the landed commits are `c420303`/`0c3a2ba`/`534c06b`/`66130f8`/`2657490`. Every
  file each repair commit touches has the **same blob** pre- and post-rebase. Not work loss.
- **mg-8af0's E11 called the material-beyond-the-brief finding in advance.** The three
  scripts it adds print **54** formatted values, none classified by any census or table.
  E11 predicted exactly that, so it is scored **CALLED, not DISCOVERED**, and it is not this
  audit's headline. The worst material beyond the brief is the **prose**, not the code: F-1,
  F-5 and F-6 all live in the README's "Predictions, scored" section (P9b, bet at 0.50).

---

## Predictions, scored

| | prediction | result |
|---|---|---|
| P1a | reverting F1 leaves the artifact byte-identical | **HIT** — 41081 = 41081 |
| P1b | all four V6 rows, V7 green; verifier exit 0, 29 checks | **HIT** |
| P1c | `probe_f1_count_moves.py` also exits 0, never reading `controls.py` | **HIT** |
| P1d | 0 artefacts go red when F1 returns | **HIT** — 0 of 35 |
| P2a | all four disclosure sites name V6b alone | **MISS** — the demonstration names three (`a3.1a`) |
| P2b | the README offers V7 as the remedy; V7's own text hedges correctly | **HIT**, both halves |
| P2c | no source-level check on the F1 site's expression | **HIT**, and sharper than predicted: 0 `.right` accesses anywhere |
| P3a | add-and-remove leaves V6a/b/c/d green | **HIT on the V6 half, MISS on the exit code** — Y1's deleted print carried a V5 anchor; Y1b removes the collateral and exits 0 |
| P3b | a count added outside the population moves nothing | **HIT** |
| P3c | the instrument reproduces its own defect class | **HIT** — F-3 |
| P3d | "TRIPWIRE" honest about mechanism, not about scope | **HIT** |
| P4a | the demonstration reproduces its transcript byte for byte | **HIT** |
| P4b | "C4 red for V6a alone" reproduces | **HIT** |
| P4c | C4 is not F1-shaped; 0 F1-shaped constructions in the demo | **HIT** |
| P4d | the demo was not extended to a V6d column | **HIT** — 5 × 4 counting the old row |
| P5a | all four rows scored against something external | **HIT** |
| P5b | the V6 heading quotes the declaration, and says so | **HIT** |
| P5c | `forced` is printed and not scored | **HIT** |
| P6a | E6a's conclusion came from "> 11", so the README's causal claim is false | **HIT** |
| P7a | F2 strictly before F1; F2 touches nothing under `face_geometry/` | **HIT** |
| P7b | the F2 commit exits 1 with one refuted row | **MISS** — 0 refuted at all three repair commits (F-4) |
| P7c | E9's second clause false, scored HALF-MISS | **HIT** |
| P8a–d | F4, STATE.md, n > 6, A1.4a all genuinely out of scope | **HIT, 4/4** |
| P9a | E11 is a hit for the parent | **HIT** — 54 unclassified counts |
| P9b | the worst material beyond the brief is the prose, not the probes | **HIT** — F-1, F-5, F-6 |
| P10a | ≥ 2 of my own printed counts are FORCED, one named in advance | **HIT** — 5 FORCED across six transcripts, including the one named |
| P10c | at least one of my own bets is wrong | **HIT** — three are (P2a, P3a's exit half, P7b) |

**Two of my instrument's own rows were defective and both were caught by their own runs,
not by re-reading.** `a3.1`'s first version scored "does this site name V6b alone" over a
window whose width I chose — a row name that was not its measurement, in an audit whose
subject is row names that are not their measurements; it is now printed as REPORTED, NOT
SCORED and the claim moved to `a3.1a`/`a3.2`. `a4.2`'s first version compared whole *trees*
across the rebase, called the difference a failure, and was measuring the rest of the
repository; it compares blobs of the touched files now. Both are recorded in the source at
the site, not just here.

---

## What this audit did NOT do

- **It did not repair anything.** No file under `code/face_geometry/`,
  `code/face_geometry_repair_e35b/` or `code/face_geometry_repair_8af0/` is edited, and
  the four instruments that mutate the tree hash all 21 of those files before and after
  every construction (`a0.4`, `a1.6`, `a2.5`, `a3.11`). `a5` carries no such row and needs
  none — it builds its worlds from `git show` into a temporary directory and never opens a
  file under `code/` for writing. The repairs F-1/F-2/F-3 recommend are named and left.
- **It did not re-audit mg-e35b's mathematics** — the dichotomy, the gauge/non-similar
  splits, the vacuity separation, the absorbability routing. mg-fcb2 and mg-8af0 both did.
- **It did not re-run or extend the n ≤ 6 multiplicity sweep**, and takes no view on F3's
  forcing argument beyond confirming that `NMAX = 6` is where the sweep stops.
- **It did not check mg-36f5's `probe_f3_tightness.py` or mg-843d's V6d demonstration on
  their own terms.** Both are exercised as part of the candidate space in `a1.3` and appear
  in `a0`/`a2` verdicts, but neither is audited; they are not mg-8af0's.
- **It did not resolve the antecedent of "them"** in the demonstration's NOT-SHOWN line.
  Both readings are stated and the finding is written so that it holds under either.
- **It did not regenerate `out_demo_f2.txt`, `out_verify_e35b.txt`, or any transcript of
  mg-fcb2, mg-e35b or mg-8af0.** They are read and compared, never rewritten.
- **It did not touch STATE.md, docs/FACTS.md, build.sh, or any other ledger.** The
  recommendations above are routed to pm-onethird in the verdict mail, which is the choice
  mg-2789, mg-e35b and mg-8af0 all made at this site.
- **It ran only on this machine, at one commit.** Every runtime and byte count in this
  README is measured 2026-08-13 on the tree that ships it.

## Running it

```sh
sh code/face_geometry_audit_d3f3/run_all.sh    # 192 s, 6 steps, 44 checks, exit 0
```

Measured 2026-08-13: a0 13.9 s, a1 86.5 s, a2 39.6 s, a3 46.3 s, a4 1.0 s, a5 4.3 s. The
cost is `a1` and `a2` running `verify_e35b.py` and `controls.py` over a dozen mutated copies
of the tree, which is the method: **no verdict in this audit is re-implemented — every one
is read out of the repository's own scorer.** Deliberately **not** added to `build.sh`: an
audit's transcripts are a record of what was true at the commit that took them, and a gate
that regenerated them would make them a status board instead.
