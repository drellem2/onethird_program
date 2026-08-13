# `code/asof_census_20ee/` — mg-20ee's census, and what the first tranche learned

`pc824` measured this population and mailed it. `mg-20ee` exists because *"the census has an
owner rather than living in one verdict mail"* — so the first thing in this directory is the
census **as an instrument**, pinned like any other, and the second is the ground truth that
corrects it.

| file | what it is |
|---|---|
| `census.py` / `out_census.txt` | the classifier. A **net**, pinned at `5a62e8c`, re-runnable |
| `ground_truth.sh` / `out_ground_truth.txt` | re-runs each candidate suite and asks whether its transcript still reproduces. **The number to quote** |
| this file | the tranche landed, the remainder, and the rules found by measurement |

## The numbers, and why three of them disagree

    pc824, mailed          105 transcripts   64 instruments   40 already moved
    census.py at 5a62e8c   125 transcripts   73 instruments   (2070 addresses)
    ground truth, re-run     —                —               32 actually stale

The classifier here is **looser** than `pc824`'s and says so: it resolves bare paths by suffix and
its *"the instrument actually reads that file"* test is weaker. It also **cannot see that an
instrument already reads at a declared commit** — `code/state_audit_6a2f` pins two literal revs
and is counted anyway. Both biases inflate it.

**32 is the honest already-stale count on this evidence**, and it comes from running the
instruments rather than from reasoning about `git log`. Of 44 candidates, 9 reproduce (the
classifier was wrong about them) and 3 have no runner.

Report the smaller number and declare the difference. Quoting 44, or 105, would be quoting a net
as if it were a catch.

## What landed in this branch

Five instruments, each verified in both directions, one commit each.

| instrument | `AS_OF` | transcript effect | direction 2 |
|---|---|---|---|
| `absent_step_7ae5` | `1024bc2` | 3 counts move, **no classification** | 46 lines: counts, addresses, tallies, stamp |
| `anchor_drift_96df` | `f59fe1f` | `+7/-1`, `+1/-1` | 6 lines, all addresses/counts |
| `n0_strike_audit_dd8b` | `dafe759` | `+28/-0` × 4 | counts move **by design**; every control identical |
| `face_geometry_audit_e720` | `8fab006` | `+18/-0`, `+25/-0` | every attack outcome identical; **2 verdicts move — reported** |
| `pairbias_indep_audit_6bd1` | `52d290a` | `+20/-0` × 2 | 8 lines, all addresses; every adjudication identical |

All five satisfy `git merge-base --is-ancestor <AS_OF> origin/main`.

## The criterion, as corrected by `pm-onethird` mid-branch

The ticket's stated acceptance — *"reproduces byte-identically against the declared commit"* —
is **not sufficient on its own**, and following it literally produced a bad pin in this branch's
own first commit. `absent_step_7ae5` reproduces byte-identically at exactly one commit,
`3fce8b9`, which is **not an ancestor of `origin/main`**: the refinery rebased the branch, and
that commit survives only because `origin/polecat-p7ae5` still points at it. That is `mg-daba`'s
defect, committed deliberately.

**Both conditions, in this order:**

1. `git merge-base --is-ancestor <declared-commit> origin/main` **must** be yes;
2. the transcript reproduces byte-identically at that commit.

**When they conflict, regenerate at the main-reachable commit.** Checking (2) first is what
produces a bad pin, because it makes the unreachable commit look like the only right answer.

Then apply the discrimination: if only addresses, corpus-size lines and the as-of block move, it
is a **pinning** — land it. **If a verdict moves, that is a finding** — report it; do not absorb
it into a pinning commit.

## Three `AS_OF` rules, all found by measurement, none by assumption

A successor should **search** for the pin, not guess it. All three of these appeared in five
instruments:

1. **The newest ancestor that reproduces** (`n0_strike_audit_dd8b`). Notably **not** the commit
   carrying the transcript: `STATE.md` gained a line before that commit landed, putting one
   address at `:210` against the committed `:209`.
2. **The parent of the carrying commit** (`face_geometry_audit_e720`). Its evidence is `git log`
   walks, and pinning at the carrying commit lets a `-60` walk reach *that commit itself*. **An
   instrument is run before it is committed**, so the history it measured excludes its own commit.
3. **`main`'s twin of a rebased commit** (`absent_step_7ae5`), when byte-identity and
   main-ancestry are incompatible — with the price measured and published.

The general form: **anything reasoning about identity by sha or ancestry breaks across a rebase,
and this repo rebases every merge.** Key on content, or on a main-reachable commit.

## The address defect is usually not alone

Every instrument in this tranche needed something else named before *any* transcript could
reproduce. None of these is an address, and none was folded in silently:

- **An absolute worktree path** printed into the transcript (`anchor_drift_96df`), so it
  reproduced for exactly one operator — `p96df` — and for nobody else, ever.
- **"HEAD vs the working tree"** standing in for *"before and after the repair"*, which is only
  the same thing while the repair sits uncommitted on the author's own desk.
- **A self-referential count**: `a2` was counting its own **not-yet-written** transcript, so its
  `483/22` could never have been reproduced by anyone. Pinning is what gave that suite a fixed
  point at all. `22 + 6 = 28` is the self-consistent value; the verdict does not move.
- **A synthetic fixture routed through the pin** (`pairbias_indep_audit_6bd1`), which looked for
  a selftest's temp file in a commit that never contained it and took the transcript from 226
  lines to 2. Explicit paths are read off disk; only the corpus default is pinned.
- **Unbounded history walks** scored as verdicts (`face_geometry_audit_e720`).

## What remains

27 of the 32 measured-stale instruments are unrepaired, plus the ~24 not-yet-stale ones the
ticket defers and the 3 with no runner. `out_ground_truth.txt` lists every candidate with the
size of its drift, which is the best available ordering for the next tranche — the small ones
(`species_remainder_f8fa` at `2+/2-`, `species_repair_a4ef` at `2+/4-`) are cheap; the large ones
(`runner_exit_audit_dee4` at `774+/91-`, `landing_audit_sweep_64cb` at `363+/111-`) are likely
carrying more than an address defect.

**Cost, measured rather than estimated: about 30 minutes per instrument** done to the acceptance,
across five. The ticket's *"do not do all 64 in one branch"* is right for a second reason it does
not give — not only reviewability, but that a rushed pin is indistinguishable from a correct one
in the diff and is caught only by the two-direction test.

---

# Tranche 3 (`mg-4020`) — a condition **before** the three, and the instrument that could not run

Tranche 2 pinned one instrument and built condition 3. Tranche 3 pinned **none**, and that is the
result rather than a shortfall: the two cheapest instruments left on the work-list were worked in
drift order and **neither is repairable by a pin**, for two different reasons. Reporting that at a
low water mark is what tranche 2's own README asks for.

## 1. Condition 3's instrument died on 23 of the 27 instruments condition 3 is for

`consumers.py` was built against one subject and ran correctly on it. Used on a second —
`code/landscape_repair_audit_3b51` — it **crashed**, after printing a correct-looking header.

`git grep` exits **1 for no match** and 2+ for a real error; the `git()` wrapper read every
non-zero as fatal. So any subject script that nothing outside its own directory names took the
whole census down. Blast radius, **measured across the remaining work-list rather than guessed:
23 of 27 crash, 4 run** — and one of the 4 is the single subject it was built against.

**The repair that made it correct is what made it fatal.** *A basename is not a name* searches a
**shared** basename by full repository path, and `code/audit_2c77/run_all.sh` appears in no other
tracked file. The rule that stopped the census reporting every README in the estate is the rule
that guaranteed it would find nothing — and finding nothing was fatal. Four of the 23 are that
rule alone. This is tranche 2's *"a repair can introduce the defect it repairs"* by a second route.

The previously-fatal case is now a **printed figure**, not a tolerated silence: the count of
subject scripts named in no tracked `*.py`/`*.sh` outside their own directory, with their names,
and the sentence that the census has **no evidence either way** about them. A repair that turned a
crash into a silence would be worse than the crash. The default subject reports **`0 of 6`** —
which is precisely why this was never seen.

## 1b. And a **94% over-count** in the same instrument, found by pointing it at itself

Condition 3 applied to *this* change — `consumers.py code/asof_census_20ee` — reported fifteen
instruments as no-arg consumers of `census.py`. They are not. `census.py` is a **unique** basename,
so it was searched for by basename, and the test was a plain substring: it matched `s1_census.py`,
`d5_census.py`, `a4_census.py` and every other numbered step in the estate whose name **ends** in
it. Measured: **76 of 81 occurrences outside its own directory were substrings of a longer
filename**, 5 were real.

**This is the exact inverse of the repair it sits beside.** *A basename is not a name* fixes a
basename **shared** by many files, by searching the full path. This is a basename that is a
**suffix** of other filenames — which that rule cannot see, because `census.py` really is unique
among tracked paths. Two opposite failure modes, one substring test, and only the first had ever
been met.

The boundary is on the neighbouring **character**, deliberately not a word regex: `/` must stay
allowed before the needle, or every full-path (shared-basename) needle would stop matching and the
loud over-count would become the silent **under-count** section D warns about. `C8` is that
negative half. After the fix, section A for this directory is **empty**, and
`out_consumers.txt` for the default subject is **byte-identical** — the fix removes 76 false
positives elsewhere and moves no verdict where the instrument was validated.

**Both defects in condition 3's instrument were found by *using* it on a subject it had not seen** —
never by reading it. It had one subject and passed.

## 2. Condition 0: **is a pin the remedy at all?**

`pinnable.py`. Conditions 1–3 all assume the question is settled; this asks it, by classifying a
drift the caller has already produced. Two rules, each built from a real instance:

| rule | fires when | real instance |
|---|---|---|
| **R1 ignored address** | a changed line names a path `git check-ignore` matches — in **no commit**, so no `AS_OF` reaches it | `species_repair_a4ef` |
| **R2 declared revision** | a subject script carries a hex token `git cat-file -e` **resolves** | `state_relocation_audit_b0ae` |

**Neither is a verdict.** R1 says a pin cannot remove *that line*; R2 says a pin already *exists*.
Both are reasons to stop and read before paying the ~45 minutes conditions 1–3 cost.

## 3. The three instruments, measured

| instrument | drift | class | why a pin is or is not the remedy |
|---|---|---|---|
| `species_repair_a4ef` | `2+/5-` | **not pinnable** | its whole drift names `__pycache__` in sibling trees — `.gitignore`'d, so in no commit |
| `state_relocation_audit_b0ae` | `7+/7-` | **already pinned** | `OLD_REV`/`NEW_REV` declared; drift is entirely B8.2, which its own runner header calls *"about the repo as it stands"* |
| `landscape_repair_1953` | `27+/8-` | **pinnable** | a walk of `docs/`, `23` → `44` occurrences as the corpus went 267 → 530 files |

`a4ef` is **measured in both directions at HEAD with no pin whatever**: create the three empty
directories and the committed transcript reproduces **byte-identically**; remove them and the
`2+/5-` returns. **The transcript is a function of which suites the operator has run**, not of repo
state. Pinning `b0ae`'s B8.2 would not repair the section — it would delete the question it asks.

**So the work-list is not 26 pinnings.** Whether it is *mostly* pinnings is **not known and is not
claimed** — three instruments is three instruments. What is established is that *"drifts"* and
*"wants an `AS_OF`"* are different properties, and the second must be measured per instrument
rather than inherited from membership of a list nominated by a classifier **for foreign
addresses**. `mg-54b1`'s sweep reached the same conclusion from the other direction on an
**unselected** sample, which is why this is a rule and not an anecdote.

## 4. A control that planted its own probe into the corpus it searched

`C5` requires that a needle nothing names returns empty. Spelled as one literal it **found itself
the moment it was committed** — this file is a tracked `*.py` and the rule greps tracked `*.py`.
The needle is now assembled from pieces at runtime.

That is the **measurement environment leaking into the measurement** for the third time in this
arc, by a third route — after tranche 2's dirty-worktree baseline and `mg-54b1`'s *"the sweep runs
in a clone of the branch that carries it"*. It is no longer a hazard to remember; it is a thing to
**check for by construction** whenever a control plants a string.

## 5. What tranche 3 leaves

**26 instruments remain**, unchanged in count, and that is honest: this tranche bought triage and a
working condition-3 instrument, not pins. `out_pinnable_a4ef.txt` and `out_pinnable_b0ae.txt` are
**one dated hand-run each and no suite re-takes them** — the same declaration `out_ground_truth.txt`
makes about itself, and the same blind spot.

`pinnable.py` is **not in `run_all.sh`**, because it requires a suite to have been run and *not*
restored — a state no build path should be in.

**The next tranche should triage before it pins**: run the suite, run `pinnable.py`, and only then
start conditions 1–3.

### The next candidate, diagnosed but **not** pinned — `landscape_repair_audit_3b51`

Triaged here, and left for tranche 4 rather than rushed, because *"a rushed pin is
indistinguishable from a correct one in the diff"*. What is measured:

* **Condition 0 fires R2 — a partial pin.** `audit_scope_text.py` declares `OLD_REV = 714aceb` and
  reads **the audited document** through `git show OLD_REV:…`, but D1's *corpus* comes from
  `grep -rn` over the **live worktree**. The script pins its subject and not its corpus, in the
  same forty lines. That is the drift, and it **is** pin-reachable — this is mg-20ee's remedy
  applying as designed, unlike `a4ef` and `b0ae`.
* **But a verdict moves, so it is not a pinning commit alone.** The R4-slip finding has
  **relocated**: `docs/roadmap.md:41` → `docs/OneThird-Landscape-Repair-IndependentAudit.md:190`
  and `:290`, and a `False` → `True` alongside it. Per mg-20ee's own discrimination, **report it;
  do not absorb it into the pin.** The relocation is live information about the corpus that no
  transcript currently records.
* **Condition 3 applies for real, and the repaired `consumers.py` confirms it.**
  `audit_scope_text.py` is executed by `code/landscape_repair_1953/run_all.sh` — a **C1 confirmed**
  no-arg consumer, which is also why `1953` appears on the work-list in its own right at `27+/8-`
  carrying *the same drift*. **One pin, two transcripts**, and the consumer must be re-measured.
  This is the first C1 hit the consumer census has produced for a subject other than the one it
  was built for — and it only produced it **after** the crash above was repaired.

So the ready pin is a **three-part** item: pin the corpus read, re-measure `1953`, and file the
moved verdict separately. Estimating it as one pinning is how it would go wrong.

---

**Two entries in `out_ground_truth.txt` are not independent**, and are marked there:
`n0_strike_audit_dd8b` reports `REPRODUCES` only because this branch had already pinned it when
the sweep reached it, and `census_remainder_f8e5` reports `rc=143` because its worker was killed
after 37 minutes to unblock the sweep — that line is unreliable and must be re-measured.
