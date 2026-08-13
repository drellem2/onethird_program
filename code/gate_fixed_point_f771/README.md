# mg-f771 — THE GATE'S OWN FIXED POINT

**A committed `out_*.txt` must never be able to disagree with the repo it describes.**

## 1. The defect this was filed about

`code/facts_registry_03cf/out_f0_registry_discipline.txt`, as committed at `1d89a29`, ended:

    STATE.md claims 20 entries; docs/FACTS.md has 20   [PASS]
    18 relative links checked, 0 broken
    VERDICT: GREEN — 20 entries

The registry has **23**. F21, F22 and F23 are on main and have been since `d3355f2`/`de8aa86`.
So a reader of the committed file was told `GREEN — 20 entries` about a registry that has 23,
and the file's own VERDICT line — the part written to be quotable — was the wrong half.

Nothing was lost: the file regenerates in about a second. But *regenerable* and *correct to
leave stale* are different claims, and a stale `out_*.txt` is a **report**, not a build
artifact. It is quoted.

## 2. The choice, made against measurement rather than taste

mg-f771 offered two mechanisms and required the choice be made against whether anything
actually consults these files. Both were measured, and **both were refuted**.

**Option 1 — untrack them.** *Refuted: there are live consumers, and one of them reads the
committed blob out of git on purpose.*

| consumer | what it does |
|---|---|
| `docs/FACTS.md:110` | links `code/facts_registry_03cf/out_f1_adjacency_corollary.txt` as the evidence for a registered fact |
| `code/sweep_evidence_control_d2c2/p1_names.py:60-73` | reads **`git HEAD:code/control_audit_9876/out_a4_sweep.txt`** as its declared baseline |
| `code/hodge_leverage_audit_835f/audit_a318_repair.py:608` | reads a committed `out_control.txt` through `V.tree()` |
| `docs/` at large | 1,024 tracked `out_*.txt` exist; roughly 280 distinct basenames are quoted across `docs/` and `STATE.md` |

`p1_names.py` is the decisive one. Its own D5 records that **the first gate run erased its
finding** — `build.sh` regenerated `out_a4_sweep.txt` in place, the diff came back empty, and
the finding was deleted by the act of checking the tree. Its repair was to recover the
declared reading from `git HEAD:`. Untracking that file removes the thing it reads.

**Option 2 as literally stated — fail when a regenerated output differs from its committed
copy.** *Refuted: it is unsatisfiable.* The ticket's premise that these files are "a pure
function of repo state" is **false, and measurably so**. On one gate run in this worktree,
four of the seven re-dirtied files differed only in:

* wall-clock timings — `36.4s` → `30.7s`, `0.17s` → `0.31s`, `13.5s` → `14.0s`;
* **absolute worktree paths** — `/Users/daniel/.pogo/polecats/p28b6/…` → `…/pf771/…`, one of
  them truncated mid-name at a column limit (`cannot read /Users/daniel/.pogo/polecats/p28`).

The path half is fatal on its own: the same repo state produces different bytes in *every*
polecat worktree, by construction. A byte-comparison gate would be red on every merge from
every worktree, forever, and a gate that can never be green is worse than no gate.

**What was built — option 2, repaired against that measurement.** The transcripts stay
tracked and quotable. The gate compares committed against freshly-generated **after erasing
exactly two declared families that are not a function of repo state**, and grades every other
difference red. The two families are in `lib_f771.py`:

    N1  absolute paths to a checkout of this repository  ->  <ROOT>   (the ROOT only; the tail is graded)
    N2  decimal seconds  (36.4s, 0.55 s)                 ->  <t>s     (integers are NOT eaten)
    N3  on a line containing <ROOT>, the shorter may be a prefix of the longer

**N3 was not in the first version, and the refinery refused this branch to put it there.**
The first version *enumerated* the checkout shapes it knew — `.pogo/polecats/<name>` and
`research/onethird_program` — and the refinery merges in neither: it clones to
`/Users/daniel/.pogo/refinery/worktrees/onethird_program`. **A list of known roots is a list
of the places somebody has already looked**, so N1 no longer enumerates: it matches "an
absolute path that runs into a repo-relative entry", which is what a checkout root *is*.

That was only half of it. The refinery's path is **54 characters against a polecat
worktree's 34**, and several transcripts cut their lines at a fixed column — so a line that
embeds a path loses *fifteen more characters of its tail* in the refinery than in the
worktree the bytes were committed from:

    committed (34-char root)   …/BASELINE.json.no-such-file is missing.  A gate
    refinery  (54-char root)   …/BASELINE.json.no-such-file is missin

No root-substitution repairs that: what differs is *how much of the line survived*, which is
a function of where the checkout lives. Hence N3, which is the weakest of the three rules
and is priced as such — a change that only **shortens** a line after the path now reads as
noise (`W12`, green on purpose), while a tail that **diverges before the cut** is still
caught (`W13`), which is what keeps `W6` alive.

A wider normaliser is an unfalsifiable escape hatch — anyone facing a real disagreement can
silence it by widening the rule, and nothing in the machinery tells that edit from a correct
one. The only defence offered is `g1_controls.py`: **six worlds the normaliser must catch,
three it must not, two refusals**, with the three "must not" marked GREEN ON PURPOSE.

## 3. The arms

| arm | asks | cost |
|---|---|---|
| `g0_fixed_point.py` | after a gate run, does any committed `code/**/out_*.txt` disagree with this tree? | 0.19 s |
| `g1_controls.py` | can this control fire, and is its blindness the declared one? | 0.04 s |

**The freshness handshake.** `g0`'s subject is the *side effect of a gate run*. Run on its
own it would compare each committed transcript against a worktree copy nothing had refreshed,
find them equal, and print a green meaning only "nobody hand-edited these" under a heading
claiming more — a laundered green in the file written to find them. So `build.sh` sets
`BUILD_SH_RAN_THE_SUITES=1` on the one line that invokes this suite, and `g0` **refuses**
(exit 2) without it. `R2` in `g1` demonstrates the refusal rather than asserting it.

**The watched class** is every tracked file under `code/` whose basename is `out_*.txt`. Not
a hardcoded list, so a new gate suite is covered the day it lands. Four consequences worth
stating:

* `code/libweak_audit_c4f5/out_a4_census.txt` (mg-c824) — which must **not** be regenerated,
  because it prints line numbers into a document it does not own — is outside this control
  **by construction, not by exemption**. This instrument regenerates nothing; it only reads.
  A file no suite rewrites is never modified, so it never appears.
* `STATE.md` and `docs/` are outside the watched class, so editing them locally with the gate
  running does not trip a control about transcripts.
* A gate suite that wrote a tracked file *not* named `out_*.txt` would be invisible here.
  Named rather than discovered: no such suite exists today, and that is a fact about today.
* **Nothing is exempt.** `g0`'s own transcript was the single exclusion until mg-c15e and is
  now in the class on the same terms as everything else; `lib_f771.SELF_EXCLUDED` is deleted
  rather than narrowed. Every row `g1` grades as *out* is out because it is **not a
  transcript**. §9.

## 4. This remedy is an artifact of the same kind as the defect

A tracked transcript that goes stale is the defect; this directory ships two tracked
transcripts. Enumerated before committing, and both hazards are real:

* **D1 — the plain `>` redirect would have made this suite fail on itself, every run,
  forever.** Every other suite in the gate writes `python3 arm.py > out_arm.txt`, and the
  shell truncates the target *before* python starts. `g0`'s own transcript is inside `g0`'s
  own watched class, so `g0` would open it, find it **empty**, and grade the committed copy as
  disagreeing with the tree — in the file written to detect exactly that. `run_all.sh`
  therefore writes to `.out_<arm>.txt.partial` and `mv`s it into place, with the temp files
  removed from a `trap` armed before the loop. Measured, not anticipated: it is why that line
  is a `mv`.
* **D2 — `out_g0_fixed_point.txt` WAS exempt from its own watched class, and the exemption is
  gone as of mg-c15e. There is no exemption now.** What it said: `g0` writes its transcript
  *after* taking its measurement and the text named the disagreement set, so a red run's
  transcript is committed alongside the very refresh that makes the tree green, and the next
  run reads that committed copy against a green one and grades it DISAGREES — **an innocent
  branch red for a non-reason, which is this ticket's own thesis shipped inside its remedy**
  (mg-479c's E9). Measured over five runs here and re-measured over the record by mg-585e:
  **31 committed versions, 16 of them RED, 24 shape flips, and 7 commits of `main` whose
  entire diff is that one file.** See §9 for how it was closed, what that buys and the one
  sentence it costs.
* **D4 — THE REMEDY FAILED ITS OWN INVARIANT ON RUN 2, AND IT IS KEPT HERE RATHER THAN
  QUIETLY FIXED.** After the refresh commit the gate was green, so the fixed point looked
  reached. It was not: run 2 came back **RED, 1 disagreement, and the disagreeing file was
  `out_g0_fixed_point.txt` itself**. The first draft printed the whole changed set — how many
  transcripts moved and which were graded NOISE — and *that set is not a function of repo
  state*. Whether `out_g1_values.txt` appears depends on whether its wall-clock timing rounded
  to the same tenth as the previous run. So this arm's tracked transcript changed between two
  runs of an unchanged tree, and the arm correctly graded its own committed copy as
  disagreeing. **The instrument caught its author**, which is the only reason it is written
  down; the failure would have been invisible had the convergence been asserted from one green
  run instead of measured over three. The repair: operational detail goes to **stderr**, which
  the build log keeps and no tracked file does. `run_all.sh` therefore drops the `2>&1` every
  other suite writes.

  **D4's own rule was half right, and mg-c15e supplied the other half.** The repair stopped at
  "only the DISAGREES list, *which is repo state*, reaches stdout" — and that test is the
  wrong one. The DISAGREES list *is* a function of repo state; it is a function of the tree at
  **run** time, and the file is committed into the tree **after** the repair. The right test
  is **does the repair move it**, the two tests disagree on exactly one item, and that item was
  the whole of §2. So §2 is now the rule inventory and the outcome is on stderr beside the
  changed set — D4's own remedy, applied to the half D4 exempted instead. `g0`'s crash and
  refusal paths went to stderr with it: a traceback on stdout was justified by the transcript
  being outside the watched class, and it is not outside it any more.
* **D3 — `g0` cannot check that a transcript is TRUE**, only that the committed bytes and the
  fresh bytes make the same assertions. An instrument that is wrong is wrong identically in
  both and this arm is silent. The gate is on AGREEMENT, not on truth — the same split
  `f0_registry_discipline.py` and `c0_concept_discipline.py` declare, for the same reason.

## 5. The cost, stated rather than discovered

`bytes 138335` in `code/state_ratchet_e331/out_ratchet.txt` is STATE.md's size, which **is** a
function of repo state. So **a branch that moves STATE.md must now also carry the refreshed
transcripts**. That is the current dirty-tree behaviour made mandatory instead of accidental,
and it is precisely the trade mg-f771 named in advance when it offered option 2. It is not a
side effect to be tuned out: it is the invariant applied to the case that made the invariant
worth having. Planted as `W8`, so it cannot be quietly removed later without a red control.

Two operational consequences:

* **Transcripts will conflict between branches.** Two branches that both move STATE.md both
  refresh `out_ratchet.txt`. The resolution is to re-run `./build.sh` after the rebase and
  commit what it writes — **never** to hand-merge a transcript, which would produce bytes no
  run ever generated.
* **The gate is 0.18 s more expensive.** Whole gate measured at **44.7 s** on this host with
  this suite in, against the 45.6 s mg-28b6 recorded for the six-suite gate — *below* it, so
  the seventh suite is not what moved the number and the two are two load conditions, not a
  speed-up. Both are runs. This README and `build.sh` were both drafted saying **46.9 s**,
  which was the addition arithmetic and not a run — mg-17aa's D4, drafted inside the very
  suite whose subject is a committed number that disagrees with what it describes. Corrected
  by running it, before the first commit rather than after.

## 6. What was refreshed, and the convergence measurement

The committed transcripts were refreshed on this branch — see the commit that carries them.
Five disagreed with the tree at `1d89a29`:

| transcript | committed said | tree says |
|---|---|---|
| `facts_registry_03cf/out_f0_registry_discipline.txt` | `GREEN — 20 entries` | `GREEN — 23 entries` |
| `control_audit_9876/out_a4_sweep.txt` | `212 directories under code/` | `214` |
| `control_gate_724a/out_gate.txt` | twin output `7696 bytes` | `8056 bytes` |
| `rendered_twin_pin_9bc2/out_control.txt` | `PASS  STATE.md is byte-identical to … the pin` | `DIFFERS` |
| `state_ratchet_e331/out_ratchet.txt` | `bytes 138325` | `138335` |

Two more moved with no change of meaning (`alias_agreement_06d1/out_g1_values.txt`,
`out_g2_predicate.txt` — timings only) and are graded NOISE.

**mg-69b4's D5 said four files in two directories. It is seven files in six directories**, and
the count was never the point — the stale VERDICT line was.

**The fixed point is measured over eight gate runs, not asserted from one green.** The
distinction earned its keep: the first green was reached at run 2 and was wrong.

| run | exit | g0 | |
|---|---|---|---|
| 1 | 1 | RED, 5 disagreements | the ticket's defect and four more |
| 2 | 0 | GREEN, 0 disagreements | *after the refresh commit — and this green was premature* |
| 3 | 1 | **RED, and the disagreeing file was `out_g0_fixed_point.txt` itself** | D4 |
| 4–5 | 1/0 | oscillating | each run's fix is the next run's disagreement; it does not damp |
| 6–8 | 0 | GREEN, 0 disagreements, three consecutive | after the D4 stderr split and the D2 exemption |
| 9 | **1** | **the refinery refused the branch** | third checkout shape, and the tail-length half — see §2 N3 |
| 10 | 0 | GREEN, 0 disagreements | in a clone at a **133-character root**, 4× a polecat worktree and 2.5× the refinery's |
| 11 | 1 | RED, 1 disagreement | the original defect re-planted **in that same 133-char clone**; it names `out_f0_registry_discipline.txt` and grades the other three NOISE |

Runs 10 and 11 are the pair that matters: **the same instrument, from a checkout nothing was
committed from, is green when the corpus agrees and red when it does not.** Run 9 is why they
were run at all — convergence in one worktree had looked like convergence.

At the steady state the gate leaves three transcripts modified
(`alias_agreement_06d1/out_g1_values.txt`, `out_g2_predicate.txt`,
`control_gate_724a/out_gate.txt`, plus this suite's own two), every one of them graded NOISE.
**The tree still goes dirty on every gate run — that was never the defect and is not fixed
here.** What is fixed is that a dirty transcript can no longer be a *stale claim*: the gate
now tells the two apart and refuses the merge for the second.

## 7. A finding outside this ticket's scope, filed rather than fixed

`code/sweep_evidence_control_d2c2`'s **D5 guard is defeated**, and this ticket's own remedy
will keep defeating it. `p1_names.py` recovers its declared baseline from
`git HEAD:code/control_audit_9876/out_a4_sweep.txt` on the reasoning that the *worktree* copy
is the one `build.sh` overwrites. But every merge that carries a refreshed transcript advances
**HEAD's** copy too: d2c2's transcript records a baseline of `25 bare of 188 directories`, and
`HEAD` at `1d89a29` already read `212`. The reference point it was written to protect has been
eroded by exactly the mechanism it warned about, one merge at a time. Making the refresh
*mandatory* — which is what this ticket does — makes that erosion regular instead of
occasional. Not repaired here: it is another directory's instrument, and the repair is a
choice between pinning a sha and pinning the numbers, which belongs with whoever owns it.

## 8. mg-05c6 — the transcript whose subject is the whole corpus has no per-branch fixed point

Section 5 predicted the cost in one bullet — *"Transcripts will conflict between branches"* —
and named the resolution: re-run `./build.sh` after the rebase, never hand-merge. That is still
the right resolution and it is not what this section changes. What section 5 did not price is
**how many branches pay it and for whose change**, and by 2026-08-13 the record had an answer.

### The measurement

Over the last 200 commits on `main`, grading each transcript's move with `verdict_for` — so
these are moves that survive N1–N3, not churn:

| transcript | real moves |
|---|---|
| `code/control_audit_9876/out_a4_sweep.txt` | **34** |
| `code/gate_fixed_point_f771/out_g0_fixed_point.txt` | 28 |
| `code/control_gate_724a/out_gate.txt` | 20 |
| `code/rendered_twin_pin_9bc2/out_control.txt` | 18 |

`out_a4_sweep.txt` is mg-9876's smell index, **a reading over every directory under `code/`**.
25 of its 34 moves changed `population:` itself; **2 moved only because a line number shifted
in a `.py` file elsewhere in the corpus**, which is the same defect arriving without a new
directory. Two merge requests conflicted on it in one morning (`mr-d9up972tjv1j0e4ismsg` at
09:56Z, and `mr-d9urij2tjv1j0e4isn40` at 12:32Z on `out_g0_fixed_point.txt`, which flips red
whenever the census does). The census's population walked `178 → 231` over 35 committed
versions.

### The rule this broke was already written, one directory over

`code/control_gate_724a/BASELINE.json` classes `audit.sweep_membership_candidates` as
**`recorded`, not `gated`**, and its `why` is this section's whole argument in mg-724a's own
words:

> a4 sweeps EVERY directory under code/, so this count moves when any ticket adds code — and
> the gate runs on the REBASED tree, so it moves when SOMEBODY ELSE's branch lands. … Had this
> field been gated, mg-724a's own branch would have been blocked by an unrelated merge — the
> exact *a gate that fails for reasons the author cannot act on* failure mode.

Its neighbour `audit.arms` is gated for the stated converse reason: *"a1's scope is
`code/rendered_twin_pin_9bc2` ONLY, so this number does not move when other tickets add
directories — which is what makes it gateable where the sweep counts below are not."*

**Byte-comparing the whole transcript gated the recorded fields through the back door.** This
section is mg-724a's recorded/gated split applied to the transcript class, not a new doctrine.

### The mechanism

A corpus-scoped producer prints a **corpus pin**: a digest of the corpus's *structure*
(directory names, and every `.py`/`.sh`/`.txt`/`.md` path) and the *content of its source*
(`.py` and `.sh`), less its own directory, with the population beside it. `verdict_for` gains
two verdicts:

* **`CORPUS`** — declared path, pin moved. The corpus moved; the difference is not the reading
  branch's. Not red. The branch **restores** the file rather than committing it (mg-4020).
* **`STALE`** — declared path, pin moved, population drift past `CORPUS_DRIFT_LIMIT` (10
  directories). **Red.** A pinned report nobody refreshes is the defect this whole control
  exists to find.

A **second pin** carries the corpus pin's missing half: the producer's own `.py`/`.sh`. A
moved producer pin is `DISAGREES` however far the corpus moved — an instrument's owner
refreshes the instrument's own transcript. Source only, because the transcripts in that
directory are rewritten by every run of that suite and pinning them would put the fixed-point
defect back one file over.

and **`DISAGREES` is unchanged in the two cases that matter**: same pin beside a moved text
(the instrument changed its answer on an unchanged corpus), and a declared transcript that
stopped printing a pin. The pin **excludes the producer's own directory** — §3 of the sweep
reads every `.txt`/`.md` including its own transcript, so a pin over the file containing it has
no fixed point, and the exclusion is also what stops a change made *there* buying the grade.

**Transcript and prose *content* are deliberately outside the pin, and the first draft got
that wrong.** It hashed the content of every file the sweep reads — the obvious spelling —
and `./build.sh` **rewrites transcripts**, `out_g0_fixed_point.txt` among them and *after* a4
has run. So the pin moved on every gate run of an unchanged corpus, and a pin that always
moves makes the same-pin clause — the entire fence — unreachable. Measured: a directory added
and then removed again, leaving the tree byte-identical to `HEAD`, still moved it. **The
remedy exhibiting the defect it remedies, caught by running it end to end rather than by
reading it**, and now planted as `P1` in `a4_sweep.py` §5 so it cannot come back quietly.

One dependency is left outside the pin and is named rather than discovered: §3's `has_red`
reads `.txt`/`.md` **content**, so a transcript whose red-token status flips, or a README that
gains the word `REFUTED`, moves the census with the pin standing still and is graded
`DISAGREES`. That is the loud direction rather than the silent one, and it is attributable —
a suite's output changes because of the branch running it.

### Section 4 applied to this remedy

The remedy is an exemption, and an exemption is the artifact most likely to exhibit the defect
it repairs — a silent hole. Ten planted worlds `C1`–`C10` in `g1_controls.py`, three green on
purpose, fed the same `verdict_for` `g0` calls:

* `C2` — **same pin, moved text, still RED.** The fence. If this goes quiet the exemption has
  become an escape hatch.
* `C3` — `C1`'s exact pair at an **undeclared path**, red. The exemption is a list, not a shape
  a transcript can grow into by printing a pin line.
* `C5` — the declared transcript **stopped printing its pin**, red. Losing the pin is how this
  would go silent.
* `C8` — the same pair with **no path given**, red. `relpath` defaults to `None` so a caller
  that does not name the file cannot be handed the exemption by accident.
* `C9` — **the corpus pin moved *and* the producer pin moved with it**, red. This one was
  found by this branch failing it: the corpus pin excludes the producer's directory, so a
  branch that edits the instrument **and** something else under `code/` moves the corpus pin
  for the unrelated half and the instrument change rides along forgiven. mg-05c6's own branch
  is exactly that shape and was graded `CORPUS` when it should have been asked to refresh. So
  the producer's own **source** is pinned separately and a moved producer pin is `DISAGREES`:
  an instrument's owner refreshes the instrument's own transcript.
* `C10` — the **producer pin went missing**, red, for the same reason `C5` forbids losing the
  corpus pin.
* Five registry rows carry the exclusions, each with the measurement that decided it — most
  usefully `out_gate.txt`, the near miss (20 real moves, but only **4** of them the §1 byte
  counts that follow the census, and 16 its own gated fields moving), and
  `code/grain_axis_audit_03d1/out_a4_sweep.txt`, the sharp case: **the same basename with a
  different instrument behind it**, so the obvious basename spelling would have exempted a
  file nobody looked at.
* And the pin is not taken on trust either: `a4_sweep.py` §5 plants **six sandboxed worlds**
  over the pin itself, three it must be blind to and three it must see, folded into the same
  `ok` flag that drives `SWEEP OK` / `SWEEP BROKEN` — so `audit.sweep_grade`, **gated** in
  `BASELINE.json`, gates the pin control too.

`g0`'s own transcript stays stable: the registry is printed (static, from code) and **the drift
figures go to stderr**, for the same reason `README` D4 put the changed set there.

### The cost, stated rather than glossed

* **A branch that trips the `STALE` bound pays a refresh it did not cause, and which branch
  pays is arbitrary.** The per-branch tax is amortised, not abolished. On the census's own
  history — population `178 → 231` over 34 refreshes — a bound of 10 would have required **6**
  refreshes and a bound of 5 would have required 11. 10 is an **82% reduction**, and it is a
  number rather than a hope.
* **One drift is not bounded at all.** A corpus change that adds no directory — the shifted
  line number above — never trips the bound, so the census can stay stale in that respect
  indefinitely. That is the price of measuring staleness in the census's own headline unit, and
  it is 2 of 34 on the record rather than an unknown.
* **A strict `AGREES` becomes a forgiven `CORPUS`.** The pin moves on any change under `code/`,
  so a substantive regression in the census could now ride along with an unrelated landing.
  What still catches that is not this control: a4's own two-sided detector control (exit 2 on
  FAIL) and `audit.sweep_grade`, **gated** in `BASELINE.json` precisely so that *the sweep's
  detector stopped discriminating* is red even where its counts are not.

### The branch paid the tax it removes, on its way in, and that is the last measurement

`mr-d9v4sgqtjv1j0e4iso80`, 2026-08-13 23:07Z: **`CONFLICT (content): Merge conflict in
code/control_audit_9876/out_a4_sweep.txt`**. While this branch sat in the merge queue, `main`
gained a landing that moved the census, and the branch that removes the conflict class was
refused by it — a third instance, one morning after the two the ticket was filed for, on the
same object.

Resolved the way the record already says these must be: **by re-running the producer at each
rebase step, never by hand** — a hand-merge is the one resolution that can invent a transcript
neither side produced (`mg-54b1`, applied at `mg-3da1`). After the rebase `./build.sh` is green
and the regenerated census is **byte-identical to the committed one**, so it does not appear in
`g0`'s moved list at all.

It is worth being exact about what this instance does and does not show. It is **not** a
failure of the mechanism: the mechanism removes the need for a *future* branch to carry the
census, and this branch necessarily carries it, because it is the branch that changes the
producer — which is `C9`'s rule applied to its own author. What it shows is the frequency. The
window between submit and rebase was **under a minute**, and it was enough.

### What this does not do (mg-05c6)

It does not touch `out_gate.txt`, `out_ratchet.txt` or `out_control.txt`, whose moves are
measured above as mostly their own — section 5's STATE.md cost is untouched and `W8` still
holds it. It does not make the tree stop going dirty. And it does not repair section 7's `d2c2`
finding, though it changes its arithmetic: the erosion of `HEAD:out_a4_sweep.txt` becomes *less*
regular, not more, which is the opposite of what section 7 predicted this ticket's remedy would
do to it.

## 9. mg-c15e — the exemption is deleted, and the watched class is total

`lib_f771.SELF_EXCLUDED` is gone. `out_g0_fixed_point.txt` is watched like every other
transcript in the corpus, and `is_watched` now agrees with `is_transcript` on every path.

### What D2 was measuring, and why it was the symptom

D2's reason — *the text depends on the verdict* — is true and is not the operative property.
mg-585e stated the sharper one and it does not mention verdicts:

> `g0` runs at tree `T` and its output is committed into `T'`. The repair that produces `T'`
> is **commit the regenerated transcripts**. So `D(T') = {}` **by definition of the repair**.

A transcript cannot record a quantity its own commit sets to zero. That makes it decidable
which *other* content is safe: content survives if it is **invariant under the repair**, and
the repair rewrites transcript bytes and nothing else. The membership of the watched class
survives. The normaliser's rules survive. The disagreement set is exactly what does not — and
D4's rule, *is it repo state*, is the wrong test, because the repo state the DISAGREES list is
a function of is the tree **before** the repair. The two tests disagree on one item and that
item was the whole of §2.

### The oscillation is measured, not described

Over the record, pinned at `AS_OF 0cb0fa4` by mg-585e's `v1_oscillation.py`: **31 committed
versions of `out_g0_fixed_point.txt`, 16 of them RED, 24 shape flips, and 7 commits of `main`
whose entire diff is that one file** — five of them titled *refresh: THE FIXED-POINT
TRANSCRIPT SAYS GREEN AND IT IS THE ONLY FILE THIS RUN COMMITS*. A lower bound rather than a
total: a red run repaired before its author committed leaves no trace, so this is how often it
reached `main`. The mechanism is visible in the byte sizes — 15 green versions collapse onto
**three** distinct sizes and the 16 red ones onto **fifteen**, because green is a fixed point
of the run and red is never a fixed point of the commit that carries it, that commit *being*
the repair.

### What replaced §2

The **rule inventory**: the constants the verdict is a function of, printed in full, and a
`sha256` over the six functions that decide (`normalise`, `lines_equivalent`,
`texts_equivalent`, `verdict_for`, `is_transcript`, `is_watched`). `g0`'s stdout is now a pure
function of `lib_f771.py`'s source — no tree, no clock, no outcome. The outcome is in the
**exit status**, which is the only channel it has ever reached the merge gate through, and on
**stderr**, beside the moved/NOISE/CORPUS census D4 already put there.

It is **two instruments and not one**, and the pair is load-bearing: the inventory shows the
rules spelled as *constants*, so a widening lands in a diff a reader can read; the digest
covers the rules spelled as *control flow*, because N3 is a prefix comparison and no constant
can show it.

### What the deletion buys, and it is this instrument's own stated main risk

`lib_f771`'s docstring: *a wider normaliser is an unfalsifiable escape hatch — an operator
facing a real disagreement can silence it by widening the rule, and nothing in the machinery
tells that edit from a correct one.* With `g0`'s transcript inside the watched class, an
operator who widens the rule and does not re-run the gate is caught **by the control they
widened**: the inventory moves, the committed copy does not, and `g0` grades it `DISAGREES`.

### What it costs, one sentence

**The committed transcript stops being quotable for *was the gate green*.** That is the whole
cost and it is not hidden. mg-f771's own first paragraph is the reply: the file that opened
this ticket was stale precisely *because* the quotable part was the verdict — *the part
written to be quotable was the wrong half*. One reader is affected and was repaired in the
same commit: `code/verdict_staleness_30bd/owners_937c.py` quoted the `VERDICT:` line, and now
reads the watched-class rule instead, which is the half of that transcript its own sentence
was actually about.

### Section 4 applied to this remedy

The remedy is a **replacement transcript**, and a replacement's characteristic failure is
being *constant* — a file that never moves also never oscillates, and buys nothing. So both
directions are planted in `g1_controls.py` §2b, fed the real `lib_f771.rule_inventory`:

* `I1` — **N2 widened to eat integer seconds**, the exact escape hatch named above. Must move.
* `I2` — **`ABS_TO_REPO` widened**, and this world found a defect *in the candidate this
  ticket landed*. mg-585e's draft read constants by **line prefix**, which reads only the
  first physical line of a bracketed assignment and reported this one as `re.compile(` — so a
  widening of the regex moved neither the printed rule nor the digest (`ABS_TO_REPO` is inside
  no deciding function). Measured against mg-585e's own reader rather than asserted: it comes
  back **unmoved**. The inventory is therefore parsed with `ast` and printed **in full and
  never truncated**, because a constant cut at a column is a constant whose tail can be
  widened invisibly, and the tail is where a regex keeps its alternatives.
* `I3` — **N3 relaxed to forgive any two lines.** Control flow; only the digest catches it.
* `I4` — **the exemption reintroduced inside `is_watched`.** The specific regression this
  ticket exists to make loud, and it is why both membership functions are in the digest.
* `I5` — **prose moved and nothing else.** The wrong-direction world: a transcript that moved
  whenever `lib_f771.py` moved would put this file back in every branch's diff, which is the
  tax being removed. Must **not** move.
* `I6`, `I7` — a deciding function **renamed** and a named constant **deleted**: both must
  `REFUSE`, not answer. `I6` is mg-585e's `D1`, which fired on that directory's own first
  draft, where the matcher was a `def <name>` prefix and `def verdict_for_RENAMED(` starts
  with it. Matching the parsed name closes it by construction; the world stays because a
  construction that is not run is a claim.
* `I8` — the inventory is a **fixed point of the normaliser itself**: no checkout path and no
  decimal second in it, so it has nothing for N1/N2 to forgive.

### And the claim itself is measured on the real arm

`g1` §2c builds **three miniature repositories** — two differing in one line of one watched
transcript, one with a defect planted in it — copies the real `g0` and `lib_f771` into each,
and runs them as subprocesses
(ported from mg-585e; copied rather than imported, because `lib_f771.ROOT` is derived from the
module's own location, and re-implementing the decision would make every finding a statement
about the re-implementation — mg-d2c2):

* `F1` — the two trees really do reach **different verdicts**, exit `0` and exit `1`. Without
  this, `F2` is two identically empty answers.
* `F2` — **and the two transcripts are byte-identical**, with no scrubbing on either side,
  because there is no clock in either.
* `F3` — the red run's disagreement is **on stderr**, naming the file. Nothing was lost by
  taking it off stdout.
* `F4` — the green run's stderr says `VERDICT: GREEN`. The wrong direction.
* `F5` — **a crash leaves the transcript at its fixed point too.** A planted `ValueError`
  inside `changed_transcripts`: exit 2, traceback on stderr, and stdout **byte-identical to
  the two runs that reached a verdict**. This is the hazard mg-c15e introduced and it is
  planted rather than promised — the traceback used to go to *stdout* on purpose, so it would
  land in the tracked file, and that was correct only while the file was outside the class.
* `F6` — **no sandbox path reached any of the three transcripts**, or this directory would be
  committing mg-f771's own defect while describing it.

### What was considered and rejected

A **census** of the watched class — how many transcripts exist, in how many directories — is
also invariant under the repair, and it is the worse trade. Priced by mg-585e over
`137bc4ce..0cb0fa4` (129 commits touching `code/`): a census would have moved on **31** of
them against the **30** that touched this transcript, with an **overlap of 4**. Two different
quantities whose near-equality is arithmetic and not identity — it moves about as often, on a
nearly disjoint set, and relocates the churn into mg-05c6's conflict class instead of leaving
it as one extra commit in one worktree. The rule inventory moves on **neither**.

### The convergence this branch owes

`out_g0_fixed_point.txt` is now watched, so the branch that changes `lib_f771.py` must carry
its refreshed transcript — `C9`'s rule (*an instrument's owner refreshes the instrument's own
transcript*) arriving for this file for the first time. That is a **once per instrument
change** cost and not a per-branch one: a branch that does not touch `lib_f771.py` leaves this
file byte-identical, which is exactly what the 7 commits counted above were paying for and no
longer have to.
