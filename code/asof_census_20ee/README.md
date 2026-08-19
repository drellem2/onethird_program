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

> **`anchor_drift_96df` is pinned and drifts again (`mg-e8b0`, tranche 9)** — `5+/5-` re-run by hand
> at `07a2fd0`. Its `AS_OF` is sound and the new drift is **not an address**: the instrument reads
> *another repository*, whose remote `main` has moved, and the moved lines are the **verdict** it
> exists to print. See tranche 9 §5 — **do not "fix" it**.

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

> **Stale, not wrong, and annotated rather than struck (`mg-e8b0`, tranche 9).** Both cheap ones
> have since been answered and *this sentence went on offering them for four tranches*.
> `species_remainder_f8fa` was **pinned at `e29ba2a`** — this arc's own tranche 2, `mg-6e4f` — and
> reproduces byte-identically at `07a2fd0`; `species_repair_a4ef` is `mg-4020`'s R1 instance and is
> **not pinnable at all**. The count knew about the first (tranche 3's `26 remain` already subtracts
> it) and **the name did not**, which is the whole of tranche 9: a count is not a record of *which*,
> and the reader picking the next instrument reads the name. `worklist.py` now prints this sentence
> beside the row it is wrong about, so the next one cannot be found by reading.

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

### Noted, not fixed — the **gate's own** transcripts carry an absolute worktree path

The backstop for this branch was a full `./build.sh` (green, `worst suite exit: 0`). It reported
`VERDICT: GREEN — 0 disagreements` and left **seven** tracked transcripts modified. Six lines are
timing, which `mg-f771`'s `W3` declares as noise; the byte counts beside them — `9455`, `45349` —
are **unchanged**, so this branch adds nothing those censuses count.

The remaining difference is **not** noise:

```
-  S1  ... /Users/daniel/.pogo/polecats/p54b1/code/control_gate_724a/BASELINE.json.no-such-file
+  S1  ... /Users/daniel/.pogo/polecats/p4020/code/control_gate_724a/BASELINE.json.no-such-file
```

`code/control_gate_724a/out_gate.txt` and `code/gate_fixed_point_f771/out_g1_controls.txt` carry
the **absolute worktree path of the polecat that last committed them**. They reproduce for exactly
one operator and for nobody else, ever — which is precisely the defect tranche 1 named in
`anchor_drift_96df`, now sitting in **two suites inside `build.sh`'s own loop**.

Two things follow, and neither is repaired here:

1. **`g0` is GREEN across it.** The gate's own fixed-point check does not catch a transcript that
   can only reproduce for one operator — `mg-f771` §4's *"they say nothing about whether the
   watched class is the right class"*, met in the field rather than in the abstract.
2. **Every branch inherits it.** This is a standing reason gate transcripts get recommitted, and
   each recommit re-points them at a new polecat.

**These seven were restored, not committed.** Committing them would have replaced `p54b1` with
`p4020` — planting the exact defect this directory exists to remove, on behalf of every later
operator. Out of scope for `mg-4020`; it belongs to `mg-724a` / `mg-f771`.

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

# Tranche 4 (`mg-0e77`) — the ready pin, landed; and **one pin does not serve two transcripts**

Tranche 3 diagnosed `landscape_repair_audit_3b51` and left it, calling it *"a three-part item:
pin the corpus read, re-measure `1953`, and file the moved verdict separately"*. All three are done.
Two of the three came out differently from the estimate, and both differences are the tranche.

## 1. The pin, and what it cost

`audit_scope_text.py` pinned its **subject** at `OLD_REV = 714aceb` from the first line it was
written, and never pinned its **corpus**: `read_new()` opened the live worktree and `rg()` shelled
out to `grep -rn` over it. Both now read at `AS_OF`, through `git show` and `git grep <rev>`.

| transcript | `AS_OF` | rule it came from | effect |
|---|---|---|---|
| `3b51/out_scope_text.txt` | `e924590` | **parent of the carrying commit** (rule 2) | 18 of 129 lines permuted, **set-identical** |
| `1953/out_scope_text_3b51_rerun.txt` | `1db0be9` | **newest ancestor that reproduces** (rule 1) | 30 of 149 permuted, **+1 address, `23` → `24`** |

Both satisfy `git merge-base --is-ancestor <AS_OF> origin/main`. Not one verdict, count or address
moved in the first; exactly one address and the count it belongs to moved in the second, and both
are corpus-valued.

**Direction 2, measured rather than asserted.** Running `code/landscape_repair_audit_3b51/run_all.sh`
end to end leaves **only** `out_scope_text.txt` modified — the suite's other five transcripts
reproduce byte-identically. The same holds for `landscape_repair_1953`: its own four transcripts
reproduce, and only the re-run moves. That is condition 3's section-D backstop run for real, and it
says the pin reaches its one consumer and nothing else.

## 2. **`23` → `24`: the second transcript was taken against a tree that is in no commit**

`1db0be9` is the carrying commit and not its parent, which by rule 2 should be wrong. It is not:
`358beff`, the parent, is 29 lines away, and `1db0be9` is 3. The residue is
`docs/OneThird-Branching-Graphs-Where-This-Lives.md:185` — one occurrence of `sharper`, in a document
belonging to a different arc, **added by `358beff` itself**.

So the tree that transcript was produced against had `mg-aec7`'s document and *not* `mg-af28`'s
paragraph: it is `mg-aec7`'s branch **before the refinery rebased it**, and no commit contains it.
That is tranche 1's rule 3 (`absent_step_7ae5`) and `mg-daba`'s defect, arriving on a second
instrument by the same route. Regenerated at the main-reachable commit with the price published,
which is what the criterion section says to do when the two conditions conflict.

## 3. **"One pin, two transcripts" was wrong, and the correction is the headline**

Tranche 3 recorded `1953` as *carrying the same drift* — one pin, two transcripts. Measured, the two
committed transcripts of this one script **disagree with each other by design**:

```
3b51/out_scope_text.txt            states a CONTACT CRITERION : False
1953/out_scope_text_3b51_rerun.txt states a CONTACT CRITERION : True
```

`1953`'s runner header says so in its own voice — the re-run exists as *"evidence that the A1/A3/A4
landing did not re-open the locating, from the auditor's code rather than this author's"*, and
`False` → `True` **is its content**. Pinning both at one commit would not repair the second
transcript; it would delete the comparison, which is `state_relocation_audit_b0ae`'s failure mode
arriving at the instrument tranche 3 called the clean pinnable case.

So `AS_OF` is a **parameter** (`argv[2]`) with a default, and `1953`'s runner passes its own.
**The ticket's rule goes one level down**: *"drifts"* and *"wants an `AS_OF`"* are different
properties per **transcript**, not merely per instrument. The same script, in one repository, has one
transcript that wants a pin and one that must not have the same one.

## 4. Condition 0 gains **R3**, and it is a rule about **condition 2**

`pinnable.py` was run on the pre-pin drift before any of this was paid for, and
`out_pinnable_3b51.txt` is that run. It fires R2 (the partial pin tranche 3 diagnosed) **and R3**,
which is new here and which predicted the shape of the result:

> **R3 UNORDERED WALK** — the subject enumerates the filesystem, so its transcript's **line order**
> is in no commit.

`grep -rn` emits directory-enumeration order. **Measured on this repository's own tree**: that order
is a deterministic function of the *set of names* — two trees built from the same 191 paths in
opposite creation order enumerate identically, and four consecutive runs agree — and it is not
sorted, not `git ls-files` order, and not derivable from the commit by any portable rule. It is the
filesystem's, and the filesystem is in no commit.

The consequence is **not** *don't pin*. The only form that reads a corpus at a commit is
`git grep <rev>`, and git sorts — so a **correct** pin necessarily permutes the transcript, and
condition 2's *"reproduces byte-identically"* cannot be met by it. **Read condition 2 as set-identity
plus a declared permutation wherever R3 fires**, or a clean pin scores as a failed one. Both pins
above are exactly that case.

**Blast radius, measured across the work-list rather than guessed: R3 fires on 17 of the 43
candidate directories.** Whoever works the remainder will meet it on roughly two in five.

### R3's own over-count, found the way this arc keeps finding them

The first version tested each line on its own, and **fired on both instruments tranche 1 pinned to
byte-identity** — `absent_step_7ae5` and `anchor_drift_96df` each `os.walk` into a list and
`return sorted(out)` seven or eight lines below. A per-line rule calls two clean pins defective:
tranche 3's 94% over-count, inside the rule written from it. It now scans to the end of the
enclosing block, which is a **syntactic** boundary and deliberately not a line count — a window
tuned to fit 7 and 8 would be a threshold guessed from the two cases it was built from. That took
the count from 26 of 43 to 17, and both tranche-1 pins go silent, which is the right answer for them.

**Found by pointing the new rule at subjects it had not seen, not by reading it** — tranche 3's
sentence, now twice.

### And R3 finds itself, which section 4 said to check for

R3 fires **six times on this directory and every one is false**: once on its own regex source and
five times on its controls' planted needles. That is section 4's *"a control that planted its own
probe into the corpus it searched"* for the **fourth** time in this arc — and section 4's remedy
does not apply, because a detector for a token cannot avoid containing that token. It is printed in
`pinnable.py`'s own output beside R1's and R2's self-hits, with the distinction that matters:
**R1's and R2's self-hits are true and R3's are false.** All three read text, not behaviour, which
is the sharper statement of why none of them is a verdict.

## 5. The moved verdict, reported and not absorbed

`argv[2]` is also what makes the finding reportable: `audit_scope_text.py ../.. HEAD` asks the pinned
instrument what the corpus says **today**. D7's R4-slip detector:

```
at e924590 (pinned)   docs/roadmap.md:41                              *** the R4 slip ***
at HEAD               docs/OneThird-Landscape-Repair-IndependentAudit.md:190   *** the R4 slip ***
                      docs/OneThird-Landscape-Repair-IndependentAudit.md:290   *** the R4 slip ***
```

**The slip was not repaired — it migrated, and it doubled.** `docs/roadmap.md` carries no mention of
`2,353` at all now; the sentence it carried is gone. One of the two new sites is a **verbatim
quotation of the deleted roadmap line** (`> *"The audit refuted it: 0 disagreements at every one of
2,353 levels to n≤5"*`). Deleting the sentence from the roadmap looks like a repair, and the sentence
had already been copied into the audit document, where the same detector still flags it.

This is a finding about `docs/`, not about this instrument, and per the criterion section it is
**reported rather than folded into a pinning commit**. Nothing in the corpus records it; it is
recorded here. *(D5's `False` → `True` is not a second finding — it is the known, intended
difference between `6b1eacf` and `mg-aec7`'s document, and section 3 above is why it survives.)*

## 6. What tranche 4 leaves

**25 instruments remain.** One landed, and the two counted by tranche 3 as separate items were one
pin with two revisions.

- **R3 will fire on about 17 of them**, so agree what condition 2 means before paying for a pin.
- `out_pinnable_3b51.txt` is **one dated hand-run and no suite re-takes it** — the same declaration
  `out_ground_truth.txt` and tranche 3's two make about themselves, and the same blind spot.
- The `2 353` slip in `docs/OneThird-Landscape-Repair-IndependentAudit.md:190` and `:290` is
  **unowned** and belongs to whoever owns that document.
### The backstop ran, and the operator-valued transcripts are now **counted**

`./build.sh` is green — `worst suite exit: 0`, `VERDICT: GREEN — 0 disagreements`, gate
`GATE VERDICT: GREEN` — and left **five** tracked transcripts modified. Four are `mg-f771`'s
declared `W3` timing noise, and the byte counts beside them — `9455` and `45349` — are **unchanged**,
which is the repo-state half: this branch adds nothing those censuses count. All five were
**restored, not committed**, for the reason tranche 3 gives.

The fifth is not noise, and it is a **third** instance of the defect tranche 3 named in two:

```
- N14  STATE.md absent from the tree   CAUGHT   cannot read /Users/daniel/.pogo/polecats/p14ad/…
+ N14  STATE.md absent from the tree   CAUGHT   cannot read /Users/daniel/.pogo/polecats/p0e77/…
```

`code/state_ratchet_e331/out_ratchet.txt` carries the absolute worktree path of the polecat that
last committed it. So counted rather than described, over every tracked transcript in the estate:

    9 tracked out_*.txt carry a polecat worktree path, naming 7 distinct polecats

    census_audit_4d3b/out_a5_selfdefect.txt          p4d3b
    control_gate_724a/out_gate.txt                   p14ad
    mirror_staleness_cdd5/out_s0_state.txt           pcdd5
    mirror_staleness_cdd5/prerepair/out_s0_state.txt pcdd5
    sibling_sweep_7085/out_r1_sweep.txt              p7085
    sibling_sweep_7085/out_r1_sweep_FIRSTRUN_2FAIL   p7085
    species_extent_audit_6cb9/out_a3_differ.txt      p54b1
    state_ratchet_e331/out_ratchet.txt               p14ad
    verdict_audit_f911/out_a4_recover.txt            pf911

**Tranche 3's prediction is confirmed in the field.** It wrote that every branch inherits these and
that *"each recommit re-points them at a new polecat"*; `control_gate_724a/out_gate.txt` said `p54b1`
then and says **`p14ad`** now, and `gate_fixed_point_f771/out_g1_controls.txt` no longer carries a
path at all. The class is not two files inside `build.sh`'s loop — it is nine files across seven
directories, six of them **outside** the loop, where `g0` cannot see them at all.

Not repaired here: five of the nine belong to directories with their own owners, and a fix is one
normalisation rule plus nine regenerations, which is its own item. Named, counted, and left —
`mg-724a` / `mg-f771` and the owning directories.

---

# Tranche 5 (`mg-885d`) — condition 2 gets an instrument, and the instrument amends the amendment

Tranche 4 established that a **correct** pin cannot satisfy condition 2 as written, and re-read it as
*"set-identity plus a declared permutation"*. That reading was then applied to two pins **by hand**
and written into three files — this README, `pinnable.py`'s docstring, and `pinnable.py`'s printed
output. Nothing in this estate could re-take it.

Condition 0 has an instrument. Condition 3 has an instrument. **Condition 2 — the one that decides
whether a pin landed — had a paragraph.** `permuted.py` is that instrument, and pointing it at the
two pins the paragraph was written from produced both of this tranche's findings.

## 1. `SET-IDENTITY` IS THE WRONG WORDING FOR THE RIGHT IDEA — the test is a **bag**

A set forgets **how many times** a line occurs. Transcripts in this estate repeat lines constantly,
and not only rules and blanks: `mg-3b51`'s own pinned transcript prints one address **twice**, and
`mg-1953`'s re-run prints one **three times**. Under a set comparison, a pin that dropped one of
those occurrences scores **IDENTICAL** — an address and the count it belongs to would have moved,
invisibly, in the one test condition 2 exists to be trusted about.

**Demonstrated on real data rather than planted** (`out_permuted.txt` §4): take mg-3b51's committed
transcript at `12aa5f8`, delete one occurrence of the line it prints twice, and the two wordings
disagree —

    set-identical : True     <- the wording as amended says NOTHING HAPPENED
    bag-identical : False    <- what this instrument decides on

**Blast radius, counted at a pinned commit rather than guessed:**

    1061  tracked out_*.txt at 12aa5f8
    1010  carry a repeated line — SET is strictly weaker there
     123  carry a repeated line THAT NAMES A REPOSITORY PATH

The 123 is the number that matters: that is where the two wordings can disagree **about an address**,
which is the dimension condition 2 exists for. This directory is at the top of that list
(`out_census.txt`, 84 such lines) — section 4's *"a control finding itself in the corpus it
searches"* for the **fifth** time in this arc, and unlike R3's six self-hits **this one is true**.

This is not a defect in tranche 4's finding, which is correct and is why the instrument exists. It is
the same shape that finding had: a rule stated in the words nearest to hand, met by an instrument,
and found to be measuring something slightly wider than it says.

## 2. Both tranche-4 pins survive — and the check could have failed

| transcript | byte | bag | permutation | declaration | verdict |
|---|---|---|---|---|---|
| `3b51/out_scope_text.txt` | no | no | 21 of 129 positions, 9 must move | 7 lines: AS_OF header + one blank | **holds** |
| `1953/out_scope_text_3b51_rerun.txt` | no | no | 26 of 148 positions, 11 must move | 10 lines, **3 of them content** | **holds** |

The second pin's residue is not pure header, and **its own commit message says so**: `23` → `24` plus
one new address is what mg-0e77 published as *"its whole price"*. This is the first time anything
could check that the published price was **the whole of it** — a fourth moved line would have printed
as `UNDECLARED`. It did not.

## 3. Neither hand figure reproduces, and `18 of 129` is not wrong so much as **undefined**

Three defensible readings of *"permuted"*, over the same two diffs:

    core positions holding a different line      21 and 26
    lines that MUST move (core less its LCS)      9 and 11
    lines a unified diff marks changed           25 and 32

`18` is none of them, and `30` is none of the second column either. **The verdict does not move** —
both pins still hold — so this is not a defect in tranche 4's conclusion. It is the reason condition 2
needed an instrument: a number quoted in three files with nothing behind it cannot be re-taken, and
nobody could tell **which quantity it was**. `permuted.py` prints two of the three and names which it
decides on.

## 4. `A DECLARED PERMUTATION` is made mechanical, and this file's own defect is enumerated

`--declare <file>` is where the operator writes the expected residue down, one literal line per line.
Matching is literal and **by occurrence** — declaring a line once does not excuse it twice, or §1's
defect returns one level up, inside the mechanism built to catch it (`P14`).

**The remedy is an artifact of the same kind as the defect.** A declaration written by *reading the
diff* excuses that diff entirely and turns `CONTENT MOVED` into a silent pass. So every declared line
is traced to a source **that is not the diff**, and the count that traces to nothing is printed:

| provenance | meaning |
|---|---|
| `script` | a literal prefix of a `print(...)` in the pinned instrument's **source** at the pinning commit — the strong half: written in code, before any transcript existed |
| `record` | a distinctive token appears in the pin's **published record** — commit message plus the README it landed with. **Declared weak**: one token is a low bar, and it is here because the 1953 pin's price was published in prose and nowhere else |
| `blank` | an empty line. Carries no address, count or verdict, so excusing one excuses nothing |
| `UNSOURCED` | traces to neither. **This is the circular-declaration detector** (`P15`) |

Both shipped declarations come out `script` + `record` + `blank`, zero `UNSOURCED`.

## 5. Reported, not repaired — **an over-count in R3, and it lands on the instrument tranche 4 pinned**

R3 matches the invocation plus a following short-flag cluster. mg-0e77 controlled *"the word in
prose"* with `N11` — but **N11 plants the bare word**, so a **sentence of commentary naming the
invocation** fires the rule, and in an estate where every docstring names its own method that is not
a rare shape.

**Counted at `12aa5f8` rather than supposed:**

    1384  .py/.sh tracked
      92  R3 hits across them
       3  sit on a COMMENT line, in 2 files

And the file it lands hardest on is `audit_scope_text.py` — **the instrument tranche 4 pinned**.
Its *only* two R3 hits are comments **explaining the defect it already repaired**: its corpus read is
`git grep <rev>` now, and R3 is reading the sentences describing what it used to be. Condition 0 run
on it today still prints `+R3: expect a permuted transcript`. That is precisely the failure `N9`'s
rationale exists to prevent — *"every repaired instrument in the estate is told it is still
defective"* — arriving **by prose** instead of by the git form.

Found while writing `permuted.py`: an early draft carried the same shape, R3 fired, and **rewording
the sentence made the hit go away**. That repairs nothing — it removes one file from a rule still
wrong for the others — and it is recorded because a clean self-score would otherwise read as
evidence. The shape is asserted as `N18`, a known-defect control in the form `N4`, `N5` and `C3`
already take: teach R3 to see prose and N18 goes RED, which is the signal to update its declared
self-hit count. **R3 is mg-0e77's rule and this is not its repair.**

## 6. What tranche 5 leaves

**No pin landed, and 25 instruments remain — unchanged.** This tranche bought condition 2 an
instrument and re-checked everything measured against the old reading, which is what the ticket asked
for; reporting that at the low water mark is what tranche 2's own README asks for.

The ticket's *"three properties, measured per instrument"* now has its third measured rather than
predicted. **R3 predicts a permutation from the subject's text; `permuted.py` measures whether one
actually happened, in the transcript.** Those are different questions and the second is the one
condition 2 asks — R3 fires on 17 of 43 candidate directories, and for every one of them condition 2
must now be **scored** rather than eyeballed.

**Blind spots, and they are load-bearing:**

- **It is not a verdict on the pin.** Bag-identity plus a declared residue says the transcript's
  *content* did not move. It says nothing about condition 1 (is the AS_OF an ancestor of
  `origin/main`?), nothing about condition 3, and nothing about whether the permutation is the one
  `git grep`'s sort predicts. **A pin at a commit in no branch passes here** — which is `mg-daba`'s
  defect exactly, and it is condition 1's job and not this one's.
- **It is not a reason to stop comparing bytes.** R3's permutation appears at the **pin transition**,
  not run to run: mg-0e77 measured enumeration order to be a deterministic function of the set of
  names. `./build.sh` and `mg-f771`'s fixed point are right to compare bytes and nothing here asks
  them to loosen.
- **`record` provenance is weak by construction and says so.** One distinctive token shared with a
  commit message passes it. A declaration is only worth what its provenance is, and the strong half
  is `script`.
- `out_permuted.txt` **is** re-taken by a suite — `run_all.sh` runs it, unlike `pinnable.py` and
  `ground_truth.sh` — because it needs no dirty tree. That is the one blind spot in this directory
  this file does **not** inherit.

### The backstop ran, and mg-9876's arm census does **not** move

`./build.sh` is green — `worst suite exit: 0`, `VERDICT: GREEN — 0 disagreements` — and left **five**
tracked transcripts modified. Four are `mg-f771`'s declared `W3` timing noise, and the byte counts
beside them — `9455` and `45349` — are **unchanged**, which is the repo-state half.

**And the census that moved for tranche 4 is unchanged here**: `144 of 223` shipping a control and
`145 of 223` recording a demonstrated failure, both still. This branch adds **files to a directory
already counted in both arms** — not a directory, and not a first control — so neither numerator nor
denominator moves. Checked rather than assumed, because tranche 4's `+1` came from exactly this arm
and looked like noise until it was attributed.

The fifth is the operator-valued path again, and it now reads a **third** value:

    S1  ... /Users/daniel/.pogo/polecats/p927a/code/control_gate_724a/BASELINE.json.no-such-file

`p54b1` at tranche 3, `p14ad` at tranche 4, **`p927a` now** — in a transcript neither of those
branches committed. Tranche 3's prediction that *"each recommit re-points them at a new polecat"* is
now confirmed three times over on one file. **All five restored, not committed**, for the reason
tranche 3 gives: committing them would replace `p927a` with `p885d` and plant the defect on behalf of
every later operator.

---

**Two entries in `out_ground_truth.txt` are not independent**, and are marked there:
`n0_strike_audit_dd8b` reports `REPRODUCES` only because this branch had already pinned it when
the sweep reached it, and `census_remainder_f8e5` reports `rc=143` because its worker was killed
after 37 minutes to unblock the sweep — that line is unreliable and must be re-measured.

---

# Tranche 6 (`mg-e5f3`) — R3 reads **code**, not prose; and the half-repair adds a hit

Tranche 5 reported an over-count in R3 and did not repair it, in as many words: *"R3 is mg-0e77's
rule and this is not its repair."* It left the signal for whoever did — `N18`, a known-defect
control whose own text says *"teach R3 to see prose and this control goes RED, which is the signal
to update its declared self-hit count."* This tranche is that update.

## 1. The reported figure was itself short — `3 on a comment line` was **9**

Tranche 5 counted the over-count with `h.startswith("#")`. That test sees a whole-line comment and
nothing else: not a **trailing** comment on a line of code, and not a **docstring** — which is where
6 of the 9 real hits are, in an estate whose every instrument explains its own method at the top of
its own file. **A rule measured by a one-line test, inside the transcript reporting it, is §3's own
`18 of 129` shape one section along.**

Counted at `12aa5f8`, all three rules side by side (`out_permuted.txt` §4):

    mg-0e77's rule — prose read as code          92 hits, 71 files, 47 dirs
    comments blanked ONLY — the half-repair      90 hits, 69 files, 46 dirs
    comments AND docstrings — the rule           83 hits, 63 files, 45 dirs

## 2. **The half-repair adds a hit, and it adds it to `pinnable.py` itself**

This is the measurement that decided the design, and it was taken rather than reasoned about.
Blanking **comments alone** removes 3 hits and **adds one** — to R3's own file. Its docstring line
*"So pinning a grep -r corpus necessarily permutes the transcript"* was being suppressed by a
`sorted(` that lives in the **block comment twenty lines below**. Remove the comments and you remove
the *suppressor*: a repair introducing the defect it repairs, in the half nobody would have looked
at, because the half everybody looks at demonstrably worked.

R3's negative half reads the whole enclosing block, so **prose could silence a real walk**. The two
surfaces are therefore blanked together. Planted as `P21`; at `12aa5f8` the full repair adds **zero**
hits, so no instrument in the estate was ordered only in prose — the control says what *would*
happen, and the estate scan says it does not.

## 3. The headline — condition 0 stops telling a repaired instrument it is defective

**Two directories go silent, and one of them is `landscape_repair_audit_3b51` — the instrument
tranche 4 repaired and pinned.** Its *only* two R3 hits were comments explaining the defect it no
longer has; its corpus read has been `git grep <rev>` since `de4ec4b`. Condition 0 run on it printed
`+R3: expect a permuted transcript` for sentences describing what it *used to be*. That is precisely
the failure `N9`'s rationale exists to prevent — *"every repaired instrument in the estate is told it
is still defective"* — arriving **by prose** instead of by the git form. It does not print it now:
run today, R3 on `audit_scope_text.py` is **0 code hits and 2 prose-only**, and the verdict carries no
`+R3`.

**`out_pinnable_3b51.txt` still carries that line and CANNOT be re-taken, which is a fact about the
pin rather than a stale transcript to refresh.** Condition 0 reads `git diff -- <subject>` and refuses
an empty one. Re-run end to end today (3m 44s), `code/landscape_repair_audit_3b51` **reproduces
byte-identically** — tranche 4's pin still holds, confirmed rather than assumed — so there is no
drift to classify and the instrument correctly refuses. That transcript is a dated record of a
pre-pin tree, its `+R3` line is a statement about a rule as it stood at tranche 3, and hand-editing it
would be fabricating a run. **The mechanical evidence for this section is `out_permuted.txt` §4**,
which takes the measurement at a commit and needs no dirty tree at all.

## 4. The other direction, checked rather than assumed

An under-count is the worse failure — nothing in the output says so — and this repair only ever
*removes* hits, so it is the failure this branch had to rule out.

- **All 9 removed hits are printed** in `out_permuted.txt` §4. Every one is a sentence.
- **No code line changed status**: the removed set is exactly those 9 prose lines.
- **Every newly-silent file was read.** `corpus_universe_1d6c/p1_glob.py` globs and `sorted()`s the
  result; the same for the other seven. Only their prose was ever firing.
- **`P19` plants the shape that would go silent if the boundary were wrong**: the only subject R3 has
  ever had spells its corpus read as *string literals in a list*, `["grep", "-rn", ...]`. So the rule
  blanks **docstrings** — a string standing alone as a statement — and no other string.
- **The boundary is "text the interpreter never executes"**, which is a fact about the language and
  not a judgement about intent. `tokenize` is asked rather than a regex written, which is `R2`'s own
  shape: `git cat-file -e` is git's answer to *"is this a revision"*. A scanner cutting at the first
  `#` would blank a real walk sitting after one inside a string — **and this file's own `WALK`
  pattern contains a `#`** (`P20`).

## 5. What this tranche leaves — reported at the low water mark

**No pin landed, and 25 instruments remain — unchanged.** R3 fires on 45 directories rather than 47.

- **2 of the 83 surviving hits are still prose**, both sentences inside a `print(...)`, both printed
  by name in §4. They stay because nothing here can tell `print("grep -rn …")` from
  `run(["grep","-rn",…])` without knowing which callee executes, and a rule special-casing `print`
  would go silently incomplete the moment a subject narrates through `banner()`.
- **A second over-count in R3, reported and not repaired**: the short-flag cluster fires on a
  **hyphenated word** — `grep 'STANDING UN-STRUCK'` matches on `-STR`. One rule change measured in
  both directions is this tranche's whole claim.
- **A fragment is not a file** (`N21`, a declared-limit control in the form `N18` used to take).
  Separating code from prose needs syntax; `tokenize` refuses a fragment and the fallback removes
  comments only. `main()` passes whole files, and **the count of files that fail to tokenize is
  printed** rather than swallowed — 0 at `12aa5f8` — because a repair that quietly stops applying is
  worse than one that never did.

### Three figures that were stale in this directory, and are not now

- **`pinnable.py` was still printing tranche 4's superseded wording.** Its R3 section said *"read
  condition 2 as SET-IDENTITY plus a declared permutation"* — the wording tranche 5's own instrument
  amended to **bag**, one file away, because a set forgets multiplicity. It also still quoted
  `18 of 129` and `30 of 149`, the hand counts §3 established reproduce as nothing. Both corrected,
  and the file now points at `permuted.py` rather than restating a number.
- **`permuted.py` §4 read the live worktree for one of its own figures** — R3 run over `permuted.py`
  as it sits on disk, the only read in that file that was not of a commit, in the file arguing that a
  transcript must be a function of repo state. It printed `0` and would have gone on printing `0`
  until somebody edited the prose above it. That is `mg-30bd`'s defect exactly; the line is gone and
  every number in §4 now comes from `AS_OF`.
- **`pinnable.py`'s `R3 FIRES ON THIS DIRECTORY SIX TIMES` is now counted, not asserted** — and it
  was already wrong by the time the sentence was written down here: run against a real subject on
  this branch it prints **7**, because the controls added above each plant a needle in the corpus R3
  searches. A self-hit count written as prose goes stale the next time somebody adds a control, which
  is the class `mg-30bd`'s census exists to count.
- **`selftest_20ee.py`'s closing tally is counted too**, for the same reason and in the same commit:
  it spelled out *"4 positive, 6 negative and 1 known-defect control on the pinnable pre-condition"*,
  and this branch adds seven to that one section. The controls that confirm a **known defect or a
  declared limit** are now **named** rather than counted — which they are is the load-bearing fact,
  and a number cannot carry it. `N18` leaves that list for the first time: it asked to be told when
  the thing it asserted got repaired, and this is that.

### The backstop ran, and mg-9876's arm census does **not** move

`./build.sh` exits 0 — `worst suite exit: 0`, `VERDICT: GREEN — 0 disagreements` — and
`out_a4_sweep.txt` reproduces **byte-identically**: `145 of 224` shipping a control and `146 of 224`
recording a demonstrated failure, the denominator still 224, all three unchanged. Checked rather than
assumed, because tranche 4's `+1` came from exactly this arm and looked like noise until somebody
attributed it. **This branch adds no directory and no file** — it modifies six that were already
there, in a directory already counted in both arms — so neither numerator nor denominator can move,
and naming *why* it does not move is the half that distinguishes this from tranche 4.

Six tracked transcripts were left modified and **all six were restored, not committed**. Five are
`mg-f771`'s declared `W3` timing noise (`109.9s → 88.0s`, `114.3s → 96.5s`) and the byte counts
beside them — `11674` and `52441` — are **unchanged**, which is the repo-state half: this branch adds
nothing those censuses count. The sixth is `state_ratchet_e331/out_ratchet.txt`'s `N14` row, which
carries the **absolute worktree root of the polecat that last committed it**; committing it would
swap one polecat for another and buy nothing, which is `mg-4020`'s finding and `mg-1344`'s explicit
decision, and it remains `mg-724a` / `mg-f771`'s to fix.

**`out_consumers.txt` is committed here and its movement is NOT this branch's fact.** It was last
regenerated at `820ade4`; the tree has gained `code/verdict_staleness_30bd` since (`mg-30bd`,
`c4190b5`), so the corpus figures go `193 → 194` files and `145 → 146`, and the new rows name that
directory. **This branch adds zero files** (`git diff --name-only --diff-filter=A main..HEAD` is
empty), which is what makes the attribution a measurement rather than an inference. Regenerating it
is the gate's own instruction; leaving it stale would be the drift this directory exists to count.

---

# Tranche 7 (`mg-44da`) — a flag's dash **starts a word**

Tranche 6 printed the line `grep 'STANDING UN-STRUCK'` in its own residue list, named the second
over-count that line shows, and declined it: *"R3's flag half is mg-0e77's rule and one rule change
measured in both directions is this tranche's whole claim."* This tranche is that change.

**The subject came out of the predecessor's own residue.** Tranche 6 was told what to do by `N18`, a
control that said what would make it wrong. Tranche 7 was told by a *printed remainder* — a list of
what the previous tranche would not fix, published at its low water mark. Neither was told by a
person, and that is the same mechanism twice in a row.

## 1. The defect — tolerance bought with a window, spent on a hyphen

R3 matches `grep` plus a following short-flag cluster containing `r` or `R`. The tolerance is a
24-character window, and it is there for a reason `P5` states: the only subject R3 has ever had
spells its corpus read as a **Python list** — `["grep", "-rn", "-E", pat]` — with a quote, a comma
and a space between the two tokens, so a pattern requiring `grep -r` adjacently sees nothing.

Every dash inside that window opened a cluster. So a **hyphenated word in the argument** was one:

| line | matched on |
|---|---|
| `grep 'STANDING UN-STRUCK'` | `-STR` |
| `bare grep over run_all.sh @%s re-derives %d` | `-der` |

**The guard is a fact about the shell's own tokenising, not a judgement about the word.** A flag's
dash *starts* a word; `UN-STRUCK` is one word. The repair is a lookbehind for a word character, and
the two spellings are kept side by side — `flags="loose"` is mg-0e77's rule character for character,
`flags="boundary"` is the rule — which is the arrangement `prose` already has, for the same reason: a
repair whose *before* is not printed beside its *after* is an assertion.

## 2. Both directions, and the second is the one that had to be ruled out

`83 → 80` hits, `63 → 60` files, `45 → 43` directories. **3 removed, ZERO added**, every removed hit
printed in `out_permuted.txt` §4 — because a repair that removes hits without showing which ones is
indistinguishable from one that broke the rule. All three are sentences; **no code line changed
status**.

**Two directories go silent, and they do not go silent for one reason.** Every enumeration site in
them is re-scanned and printed with the reason it is not a hit — **computed, not asserted**:

| sites | reason it is not a hit |
|---|---|
| 5 | `sorted(...)` on the line itself |
| 2 | prose, blanked by tranche 6 |
| 2 | **hyphenated word — this repair** |
| 1 | sorted in the **enclosing block** |

**The first draft of that paragraph asserted all of them were this repair's doing, and computing it
is what said otherwise.** Only 2 of the 10 are; the rest were already silent, and the directories
stayed lit because of the ones that were not. That distinction is invisible in the counts — a
directory going silent at this tranche can be silent for something the previous tranche did.

**No site is left unexplained, and one of them is a real `os.walk`** — `runner_exit_c2b3`'s
`libc2b3.py`, which collects into a list and `return sorted(found)` sits five lines below it. That is
the window rule doing its job, not this repair hiding a true positive. **A repair that did hide one
would look identical from the counts alone**, which is why the reason column exists rather than a
sentence claiming the files were read.

## 3. `--recursive` still fires, and that is why the guard is a *word* boundary

A guard written as "preceded by whitespace" would have silenced `grep --recursive` — its second dash
is preceded by a **dash**, which is not a word character. No such line exists in the estate at
`12aa5f8`, so the counts would not have said so. `P22` plants it. `P23` plants the other half: a line
carrying **both** a hyphenated word and a real `-r` still fires, because the engine backtracks over
the lazy window and tries each dash — asserting that from the pattern would be reading a regex rather
than running it.

## 4. Three figures that would have moved silently, and did not

- **Tranche 6's published `92 / 90 / 83` measure mg-0e77's *flag* half by definition.** The prose
  change is the only thing they are allowed to vary, so `permuted.py` §4 now pins `flags="loose"` on
  all three. Reading them at the repaired flag half would have moved three published figures while
  claiming to measure something else — this file's own subject arriving in the edit that measures it.
- **The prose delta is still measured against the prose rule alone.** Folding `mg-44da`'s 3 into
  `mg-e5f3`'s 9 would publish `12` as the prose over-count: a figure no tranche ever measured.
- **The residue count moved `2 → 1`, and it is attributed rather than left as drift.** The hit that
  left the list is *this tranche's own subject*. A residue shrinking because the rule got better looks
  identical, from the count alone, to a residue shrinking because the report got quieter.

## 5. What this tranche leaves — reported at the low water mark

- **`find(1)`'s half takes the same guard and it moves NOTHING** — 0 hits at `12aa5f8`, measured
  separately and **declared** rather than left to look like it contributed to the 3. It is applied
  anyway because it is the same defect in the same rule, and a guard that waits for its first false
  positive is one somebody has to find twice. `N24` is that measurement.
- **`find(1)` in the LIST spelling is invisible to R3** — `N25`, a known-defect control, **found by
  writing `N24` and getting the wrong answer**. R3's `find` half requires a following *space*, so
  `["find", root, "-type", "f"]` is not seen at all: the exact blind spot `P5` exists for, one
  alternative along, and an **under-count** rather than an over-count. Not repaired here, for the
  reason tranche 6 gave for declining *this* tranche's subject — `find` is an ordinary English verb
  where `grep` is not, so widening it is a second change whose false-positive direction nobody has
  measured. The control fires the day somebody does it.
- **1 of the 80 surviving hits is still prose** inside a `print(...)`, unchanged in kind from
  tranche 6: nothing here can tell `print("os.listdir(root)")` from the call itself without knowing
  which callee executes.
- **`out_pinnable_3b51.txt` still says `R3 FIRES ON THIS DIRECTORY SIX TIMES`** — a literal tranche 6
  replaced with a computed count in `pinnable.py`. It is a dated hand-run that **no suite re-takes**,
  which `run_all.sh` already declares; it was stale before this branch and this branch does not
  re-take it, because doing so needs a dirty tree and a subject suite run.

### The backstop ran, and mg-9876's arm census does **not** move

Checked rather than assumed, because tranche 4's `+1` came from exactly that arm and looked like
noise until somebody attributed it. **This branch adds no directory and no file** — it modifies four
that were already there, in a directory already counted in both arms — so neither numerator nor
denominator *can* move, and naming *why* is the half that distinguishes this from tranche 4.

**`out_gate.txt` and `alias_agreement_06d1`'s two moved on wall-clock alone and were restored, not
committed** (`mg-4020`) — the byte counts beside them, `11818` and `52431`, are **unchanged**, which
is the repo-state half. `out_a4_sweep.txt` is not modified at all: mg-9876's arm census reproduces
**byte-identically**, `145 of 224` and `146 of 224`, denominator still `224`.

### `out_consumers.txt` moves `194 → 196`, and only **one** of those is main's

The other one is **tranche 6's own transcript having shipped stale at its own commit**, which is the
class this directory exists to count, found in it:

- `+1` is main's — `code/image_geometry_c776/run_all.sh` arrived at `aaf78e8` (`mg-c776`) after
  tranche 6 landed.
- `+1` is tranche 6's — at `93ead80`, the commit that regenerated `out_consumers.txt`, **the tree
  held 195 files named `run_all.sh` and the transcript said 194**. It was measured on the pre-rebase
  tree and committed against the post-rebase one.

That is exactly the failure `aaf78e8`'s own message warns about one directory over — *"a census
regenerated on the pre-rebase tree would have attributed main's own movement to this branch"* — and
tranche 6 applied that discipline to `out_a4_sweep.txt` while missing it on `out_consumers.txt`, which
`consumers.py` computes from the **live index** rather than from a commit. **This branch adds zero
files** (`git diff --name-only --diff-filter=A origin/main...HEAD` is empty), which is what makes the
split a measurement rather than an inference. Regenerating it here is the repair.

---

# Tranche 8 (`mg-23af`) — a command name is a **whole token**, and two pointers that said *"this is controlled"* named controls that do not exist

Tranche 7 printed `N25` at its low water mark — R3's `find` half requires a following *space*, so
`["find", root, "-type", "f"]` is invisible to it — and **declined** the repair, in as many words:
*"`find` is an ordinary English verb where `grep` is not, so widening it is a second change whose
false-positive direction nobody has measured."* This tranche measured it. That makes **three
consecutive tranches whose subject came out of the predecessor's printed remainder** rather than out
of a person, and the practice is now worth naming as one: decline the repair, but leave the evidence
in the instrument's own output.

## 1. The repair, and why it is not simply the `grep` half's shape

A command name **ends a token**. In the shell spelling the next character is whitespace; in the list
spelling it is the closing quote of its own string literal. That is a fact about tokenising rather
than a judgement about the word — `mg-44da`'s guard, one half along — and it is the whole rule:

```
_FIND_SPACE = r"\bfind\s+[^\n|]*"                    # tranche 7, and mg-0e77's
_FIND_TOKEN = r"\bfind\b(?=[\s\"'])[^\n|]{0,24}?"    # the rule
```

The obvious repair — give `find` the `grep` half's own shape, `find` then any 24 characters — is
**rejected, and the measurement is why**, printed in `out_permuted.txt` section 5:

| shape | exposed on | fires on |
|---|---|---|
| `find` + whitespace *(tranche 7, and mg-0e77's)* | 90 lines | 1 hit |
| `find` + any 24 chars *(the grep half's own shape)* | 328 lines | 1 hit |
| `find` + whitespace or quote **(the rule)** | 115 lines | 1 hit |

**All three fire on the same single hit**, so the estate's counts cannot tell the three designs apart
at all. The choice is made on the *exposure* column and not on any delta. The rejected shape newly
admits 238 lines and they are **Python** — `doc.find(x)`, `def find(a)`, `pred["find"]` — in a corpus
where the word is a method far more often than a command; `find(` is a call in Python's grammar and
there is no spelling of `find(1)` whose next character is `(`.

## 2. Both directions, and both are zero — said plainly rather than dressed up

The repair removes **0** hits and adds **0**: `80 → 80`, because the estate at `12aa5f8` contains no
`find(1)` in the list spelling *at all*. An over-count repair that removes nothing and an under-count
repair that adds nothing **look identical from the delta**, and only one of them is this one. What
carries this tranche is the exposure table, the 25 newly-admitted lines (every one printed, none
carrying a `-type`/`-name` in the window), and two controls:

- **`N25` leaves `KNOWN_DEFECT`** the way `N18` did — in the tranche that did the thing its own text
  asked to be told about. It is now `(False, False, True)` across mg-0e77's rule, tranche 7's, and
  the rule.
- **`N26` is planted**, because the estate has no instance: `line.find(sep, line.index("-name"))`
  fires under the rejected shape and not under the rule. `0` lines at `12aa5f8` separate them, which
  is exactly why asserting the difference from the pattern rather than running it would have been
  reading a regex.

**Every axis pins the axes it is not measuring.** Section 4 now counts **five** rules side by side,
and tranche 7's row pins `finds="space"` for the reason tranche 7 pinned `flags="loose"` on the three
before it: letting this tranche's find repair into that row would republish `80` as a number
measuring two changes. `pinnable.WALK_BOUNDARY` exists for the same reason — the account of *which
directories `mg-44da` silenced* must be read at `mg-44da`'s rule.

## 3. The correction: two sentences whose entire content was *"go and check"*

Found by **cross-referencing, not by reading** — the same way the last two tranches found their
corrections:

- `pinnable.py` said `--recursive` staying lit was *"a control (`P24`) rather than a claim"*. **No
  `P24` has ever existed.** It is now `P22`, and **`P24` is burned**: issuing it to a new control
  would make that dead pointer *resolve*, to a control about something else, which is strictly worse
  than leaving it dangling.
- `permuted.py`'s section 2 credited its literal-matching half to a control this suite has never
  issued. It is `P14`. **This one was the worse of the two**, because the number it named *is* a real
  control — of `state_ratchet_e331` — so a reader who went looking found something, and it was about
  something else. `P25` therefore resolves per **site**, not per name.

**The repair is an instrument and not a rewording** (`mg-937c`'s rule), because a hand-fixed pointer
is exactly as unbacked as the one it replaces. `P25` cross-references every `[NPC]<n>` in this
directory's `.py`/`.sh`/`.md` against the controls `selftest_20ee.py` defines. Foreign references are
legal, **declared**, and *measured* — the owning directory must really run a control by that name, or
the escape hatch would excuse any pointer at all, which is `P15`'s shape one file over.

**`P25` fired on itself the first time it ran**, on the `FOREIGN` literal in its own source — a
declaration, not a pointer. That is this directory's own rule (*a remedy is an artifact of the same
kind as the defect it remedies*) arriving live rather than as a paragraph, and the exemption written
for it is the narrowest one that is true: the register may name its own entries and nothing else.

## 4. What this tranche leaves — reported at the low water mark

- **`N27` takes `N25`'s place in `KNOWN_DEFECT`, so the tuple turns over rather than shrinking.** A
  list spelling whose argument runs past the 24-character window is still invisible —
  `["find", os.path.join(root, sub), "-type", "f"]`. That is `P5`'s declared limit reaching the half
  nobody had measured it on: **the repair for an under-count leaves an under-count**, which is the
  defect class arriving inside its own remedy. A tranche that let the count fall from 5 to 4 would be
  publishing a smaller number for a defect that only moved.
- **Widening the window is the next change, and its own false-positive direction is unmeasured** —
  which is, word for word, the sentence tranche 7 wrote about *this* tranche's subject.
- **`out_pinnable_3b51.txt` is still a dated hand-run that no suite re-takes.** Unchanged in kind
  from tranche 7, and not re-taken here for the same reason: it needs a dirty tree and a subject
  suite run.
- **The four figures tranche 7 published were recomputed and they stand** — `92/71/47`, `90/69/46`,
  `83/63/45`, `80/60/43`. The work item filed for this tranche carried the observation that *a
  published figure in this estate has roughly a one-tranche half-life unless somebody recomputes it*;
  recomputing these four is the test, and on these four it did not bite.

### It bit somewhere else: `out_consumers.txt` moves `196 → 198`, and **neither** `+1` is a surprise

The first is main's — `code/image_closure_3da1/run_all.sh` arrived at `3a1b0ff` (`mg-3da1`) while
this branch was open. **The second is tranche 7's own transcript having shipped stale at its own
commit, for the second tranche running.** At `ccd925c` the tree held **197** files named
`run_all.sh` and the transcript committed there said **196** — the same off-by-one, measured on the
pre-rebase tree and committed against the post-rebase one, that tranche 7's *own commit message*
diagnosed for the `194 → 196` move a paragraph earlier.

**This branch adds zero files** (`git diff --name-only --diff-filter=A origin/main...HEAD` is empty),
which is what makes the split a measurement rather than an inference. The lesson is not that anybody
was careless: `consumers.py` reads the **live index** by design, so its figure is a function of *when
you ran it* and not of the commit you attach it to, and every rebase re-opens the hole. **The figure
with the short half-life was the one no `AS_OF` pins** — which is this directory's whole subject,
arriving on its own transcript twice.

---

# Tranche 9 (`mg-e8b0`) — the work-list is itself a transcript, and nothing re-takes it

`mg-e8b0`'s ticket asks for two things and one of them had already been done. **Item 1 — R3's prose
over-count — is repaired**: `mg-e5f3` did it at tranche 6, `mg-44da` and `mg-23af` narrowed it twice
more, and `N18` left `KNOWN_DEFECT` on the way. That was checked before anything was built, because a
ticket is a claim about the tree at the moment it was filed and this one was filed three tranches ago.

**Item 2 is the live one**: *"the remaining 25 must be SCORED, not eyeballed."* Taking it literally
means running one, and the cheapest name on the list is the one tranche 1's own §"What remains" hands
the next tranche:

> the small ones (`species_remainder_f8fa` at `2+/2-`, `species_repair_a4ef` at `2+/4-`) are cheap

`sh code/species_remainder_f8fa/run_all.sh` **reproduces byte-identically** at `07a2fd0`. It is not
stale, and it is not stale because `e29ba2a` **pinned it** — `pin: w3_scope READS ITS CORPUS AT A
DECLARED COMMIT` — and **that commit is this arc's own, `mg-6e4f`, tranche 2**, landed one tranche
after the sentence offering the instrument as cheap remaining work was written. The sentence has
stood through four tranches since.

**That is not *"somebody moved underneath us"*, which was this tranche's first draft and was wrong.**
The count knew: tranche 3 reports `26 remain`, which is 32 less tranche 1's five less this one. **The
name did not.** A count is not a record of *which*, and the reader picking the next instrument reads
the name.

## 1. `out_ground_truth.txt` has the property every instrument on it is on it for

Its own header says what it is: **one dated run**, ~70 minutes, executing instrument code, against
*"the working tree at `5a62e8c`"*. `run_all.sh` does not run it and says why. So it is a committed
transcript whose subject keeps moving underneath it — and **it has had exactly one commit in its
life**, which `out_worklist.txt` prints rather than this paragraph asserting it. `mg-0e77` published
*"25 instruments remain"*; `mg-885d` and `mg-e5f3` each restated it *"unchanged"*; `mg-44da` and
`mg-23af` restated nothing and re-took nothing either. **Unchanged was the claim, and it was
inherited rather than measured** — four tranches since anybody asked.

`worklist.py` asks the repository instead. Every figure it prints is a function of two commits — the
sweep's tree, parsed out of the sweep's own header sentence rather than re-typed, and `AS_OF` — read
through `git show` and `git log`. **`out_worklist.txt` therefore reproduces byte-identically**, which
is the only honest arrangement for the file whose subject is that `out_ground_truth.txt` cannot, and
it is in `run_all.sh` for `permuted.py`'s reason: it executes no instrument code and needs no dirty
tree.

**Measured at `07a2fd0`, `110` commits after the sweep's tree** — and this table is a *reading of
`out_worklist.txt`*, which is where it is computed. **Moving `AS_OF` moves every number in it**, and
a successor that moves the pin owes this paragraph a re-take. Saying so is not a formality: the
figure this tranche was told by is a figure in exactly this position, four tranches old.

| | |
|---|---|
| candidate rows recorded | **44** — 32 `DIFFERS`, 9 `REPRODUCES`, 3 `NO_RUN_ALL` |
| directories moved since the sweep | **12** |
| of those, a pin landed **by content** | **8** — the verdict |
| of those, a pin landed **by subject** | **9** — the wide net |
| rows already declaring a revision at `AS_OF` | **36 of 44** |

## 2. The answer is one-directional, and that is the whole honest statement of it

Repo movement can prove a recorded row **wrong**. It can **never** prove one right: an instrument
whose directory has not been touched since the sweep may have gone stale anyway, **because what moved
is its corpus** — which is the defect class this entire arc exists for. So the rows are printed
`FALSIFIED` / `NOT FALSIFIED` and never `DIFFERS` / `REPRODUCES`, and this file **does not replace**
`ground_truth.sh`. It is a prefilter with the backstop named at the site, in the form `census.py`
already states its own.

Two more limits are printed where they are read, rather than kept in a docstring:

- **A pin is not a repair.** Both rules say a revision was *declared*, not that the transcript now
  reproduces — `pinnable.py`'s `R2` fires on `b0ae`, which is pinned and drifts by design.
- **The unaccounted count is a low water mark.** `named in this record` is a substring count, so an
  instrument the record names *for any other reason* reads as accounted for. **`N28` asserts that
  with its live instance** and joins `KNOWN_DEFECT`: `species_remainder_f8fa` is named exactly once,
  in the sentence calling it cheap remaining work, so the rule scores the arc as knowing about a pin
  whose existence its own sentence denies. The instrument prints **the sentence** and not just the
  count, which is what lets a reader see it at the site.

## 3. Two rules for *"a pin landed"*, and the verdict rests on the narrower

| | rule | fires |
|---|---|---|
| **A** | the commit **subject** matches `pin:` | 9 rows |
| **B** | the commit's **diff to that directory** adds a hex token `git cat-file -e` resolves | 8 rows |

Rule B is `pinnable.py`'s `R2` read across one commit. They are printed side by side because **they
disagree on real rows here, in both directions** — one `(directory, commit)` pair each, both pinned
as `P27`:

- **A not B** — `code/species_extent_d633` at `e29ba2a`. The commit calls itself a pin and its diff
  *there* declares no revision: the pin landed in `code/species_remainder_f8fa`, which the same commit
  touches. **A subject is a property of a commit, and a commit touches several directories.** The
  instrument computes *which* directory of a commit's own diff gained the revision and prints it, so
  the over-count is **attributed** rather than declared.
- **B not A** — `code/absent_step_7ae5` at `6af53b9`, `fix: REPIN a4_novelty TO A main-REACHABLE
  COMMIT`. A revision declared under a verb the convention does not cover — and it is `mg-daba`'s own
  defect being repaired, which is exactly the commit a subject-only rule must not miss.

## 4. `wants an AS_OF`, measured per instrument for all 44 rows

`mg-4020` established that *"drifts"* and *"wants an `AS_OF`"* are different properties and that the
second must be measured **per instrument**. It measured three, at ~45 minutes each, because
`pinnable.py` classifies a diff and so needs the suite run and not restored. **`R2`'s half needs no
diff**, so it can be asked of every row at a commit: **36 of 44 rows already declare a revision that
resolves**, 27 of them among the recorded `DIFFERS`.

That is not *"36 are pinned"* — it carries `R2`'s declared over-count unchanged, and a declared
revision may be a **control's** rather than the corpus read's. It means *go and read why*. The number
a successor wants is the residue: **the recorded-`DIFFERS` rows that declare no revision and that no
pin has falsified**, which nothing on record has yet given a reason to skip.

## 5. The re-run — the half only running the suites can answer

`worklist.py --rerun` reads a fresh `ground_truth.sh` output beside the recorded one. It is a
**dated hand-run** in exactly the sense `out_ground_truth.txt` is, and for the same reason: it
executes instrument code, so no build path may take it. `out_worklist_rerun.txt` is that run, against
the working tree at `07a2fd0`, and it **names the rows it did not re-run** rather than reporting a
partial re-take as a complete one.

**Every verdict that moved, moved `DIFFERS` → `REPRODUCES`, and every one is attributed to a pin** —
five of this arc's own and one, `species_remainder_f8fa`, that the arc's *name* did not know about.
So the re-run and the git half agree, which is the only cross-check either of them has.

### The one that did not move, and it is the finding

**`code/anchor_drift_96df` was pinned at `c42c221` (tranche 1) and still drifts** — `5+/5-`, re-run
by hand and restored. Its drift is not an address and no `AS_OF` in this repository can reach it:

```
-  its origin/main             : 949c43926b6e
+  its origin/main             : bec18a04e34c
-  is that still the remote main: YES -- the pinned table has not yet gone stale
+  is that still the remote main: NO -- THE PIN HAS MOVED; the ticket's table is stale
```

The instrument reads **a different repository** — `/Users/daniel/research/one_third_width_three` —
and reports whether `mg-688c`'s pinned table is still current there. It has stopped being current.
So:

- **A verdict moved**, and per `mg-20ee`'s own discrimination that is a **finding, reported and not
  absorbed**. The transcript is restored, not committed: committing it would bank a foreign
  repository's `HEAD` into this one, which is `anchor_drift_96df`'s own subject.
- **The instrument is working.** This is the line it exists to print, printing it. `DIFFERS` here is
  not staleness of the kind this arc repairs, and a tranche that "fixed" it would be **silencing the
  only alarm on the board**.
- **It is a third class, and `pinnable.py` has no rule for it.** `R1` is an address in no commit;
  `R2` is a revision already declared. This is an address in **another repository** — outside the
  reach of any `AS_OF` for a third distinct reason. Reported, not built: a rule about foreign repos
  is a change whose false-positive direction nobody has measured, which is the sentence three
  tranches running have written about their successor's subject.

## 6. What this tranche leaves — reported at the low water mark

**The re-take, over the 43 rows it covers:** `31` were recorded `DIFFERS` and **`25` still are**. Six
moved, all in the same direction.

> ⚠️ **The two `25`s are different quantities and they are equal by coincidence.** The record's `25`
> is a count of *work items remaining*, carried forward by hand since `mg-0e77`. This `25` is a count
> of *rows whose transcripts still fail to reproduce* at `07a2fd0`, over 43 rows. **They are not even
> the same set**: `anchor_drift_96df` is *in* this one and *out* of that one — tranche 1's table
> lists it as landed. That is the section above, arriving from the counting side.

- **`census_remainder_f8e5` was not re-run**, for the reason the original sweep gives for the same
  row: its worker does not terminate in a usable time (killed at 37 minutes there; killed here too).
  The instrument names it rather than letting a partial re-take read as a complete one.
- **`ground_truth.sh` restores the candidate, and candidates run *other* suites.** `dee4`'s runner
  executes `alias_agreement_06d1`; a killed sweep left `face_geometry_audit_f1b2` modified, outside
  the candidate list and outside the restore. **Restored, not committed**, and *not* reported as a
  finding about that directory: a transcript from a run somebody killed is not evidence. The
  side-effect note in `ground_truth.sh`'s header understates its blast radius, and that is worth a
  successor's attention.
- **`out_consumers.txt` moves `198` → `200`, and neither `+1` is this branch's.** Both are main's:
  `code/lever_shape_9b6b/run_all.sh` at `96c38ad` and `code/subset_consumability_99f4/run_all.sh` at
  `21356d5`. Checked rather than assumed, and the check is the one that mattered: at `828a0fa` the
  tree held **198** files named `run_all.sh` and tranche 8's transcript said **198**, so — unlike
  tranches 6 and 7 — **that transcript was *not* stale at its own commit**. The expectation this
  tranche carried was refuted, and it is recorded as refuted.
- **`out_census.txt` does not move**, checked rather than assumed, and `out_worklist.txt` is a new
  `out_*.txt` in a directory `census.py` scans. Its one `RED_TOKEN` is `CAUGHT` inside a **quoted
  commit subject** at line 133, so `mg-9876`'s arm row is a directory-level membership this directory
  already had. This branch adds zero whole-output membership sites.
- **`out_pinnable_3b51.txt` is still a dated hand-run that no suite re-takes**, unchanged in kind
  since tranche 7 and not re-taken here for the same reason: it needs a dirty tree.
- **The operator-valued transcripts are still unowned** (`mg-724a` / `mg-f771`), and the `2 353` slip
  in `docs/OneThird-Landscape-Repair-IndependentAudit.md` still belongs to whoever owns that document.

### `N28` moved off its own instance, deliberately

The live instance — tranche 1's *"the small ones … are cheap"* — **is annotated in this commit**, so
the trap is closed for the next reader. `N28` therefore asserts **the rule** and not that sentence:
*accounting* for a pin and *offering the same instrument as remaining work* score identically under a
substring count, and the two strings it plants are the real ones. Had the control stayed on the
sentence, closing the trap would have turned it **red**, and a later tranche could have "repaired"
the control by re-opening the trap. It joins `KNOWN_DEFECT`, which grows `5 → 6`.

---

# Tranche 10 (`mg-0bf1`) — a mention is not a **date**, and `N28`'s account of its own remedy was wrong

`mg-e8b0` found the defect and declared the limit. `N28`:

> `named in this record` is a **substring count**, so a sentence *accounting* for a pin and a
> sentence *offering the same instrument as remaining work* score **identically**. […] What turning
> this green would mean: somebody taught the rule to read what a sentence **says**, which is a rule
> about English — that is why this is a **limit** and not a bug.

**The first half is true and the second half is wrong, and the correction is this tranche.** The
difference between accounting and offering is not in the English. It is in the **date**:

> A sentence **accounting** for a pin is **necessarily younger** than the pin.
> A sentence **offering** the instrument is **older**.

The field that separates them was in the repository the whole time, and the rule was throwing it
away. `git blame` at a declared commit puts it back. The instrument is `exemplars.py`, it ships in
`run_all.sh`, and its transcript reproduces byte-identically for `worklist.py`'s reason: every figure
is a function of **one commit** — including **this file**, which is one of its subjects, so editing
the README cannot move `out_exemplars.txt`.

## 1. Per **(record, name)**, not per line — and the first draft was per line

Per line the rule is useless, and measuring it is what said so: **290 mention lines** are older than
a pin on the instrument they name, against **140 (record, name) pairs**. The 150 that drop out are
one fact about this estate:

> **A correction here is a younger sentence, not an edit to an older one.**

Tranche 3 headed a section *"the next candidate, diagnosed but **not** pinned — `landscape_repair_audit_3b51`"*.
Tranche 4 landed that pin. Tranche 3's section still says it and always will. Per line it reads as a
live defect; it is not one, because **the answer is the next section**. So the rule takes a record's
**newest** mention of an instrument — its *last word* — and asks whether a pin landed after **that**.

The two halves compose rather than compete: the substring count says whether the record names it, the
blame date says **whether it has named it since**.

## 2. What it measures, and the one direction it can answer in

At `AS_OF = 0cb0fa4`, over **44** work-list rows and **572** markdown records:

| | |
|---|---|
| `(record, name)` pairs | **352** |
| **OVERTAKEN** — a pin landed after the record's last word | **140** |
| … in the named instrument's **own** record | 22 |
| … in a **foreign** record — the verdict | **118** |

**`OVERTAKEN` is one-directional**, which is `worklist.py`'s `FALSIFIED` / `NOT FALSIFIED` discipline
one field along. It proves the record's last word is *older than a pin on its subject*. It does not
prove the sentence is wrong — a pin is not a repair. And **`NOT OVERTAKEN` proves nothing at all**:
the named instrument may have gone stale with no pin landing on it, which is the defect class this
whole arc exists for.

*Self* and *foreign* are kept apart because they are not the same claim. A directory's own README
pre-dating a pin on that directory is ordinary. A **foreign** record is a reader somewhere else in
the estate whose last word about this instrument is older than a change to it — `mg-e8b0`'s shape.

## 3. The ticket's claim is **too wide**, and the commits column is what says so

`mg-0bf1` carries one transferable claim: *wherever a remaining-count and a named exemplar are
published together, the count will stay right and the name will rot.* Read *"together"* as **the same
markdown section** — document structure, not prose, so this half does not smuggle back in the rule
about English §1 avoids. **Both dates are measured, not one**: a file measuring the name's age while
*asserting* the count's would be the defect this arc reports.

**11 of 352** pairs are published beside a count at all. Of those: **2** have the younger count, **2**
the younger name, and **7 have both fields written in one commit and never touched again**.

> The count in those records did not stay right by being **maintained**. It stayed right because
> **nothing in the record is maintained**, and a name beside it would rot exactly as fast.

The narrowed claim the corpus does support — and the commits column is where a reader sees which
records are which, the extremes being **14** commits and **1**:

> **In a record that is *appended to*, the summary line is restated every tranche and the offer list
> is not.**

That is a property of a **running log**, not of counts and names. This directory's own README is the
log: in `## What remains`, the offer list is `f26d5be` (tranche 1) and the count beside it is
`0cb0fa4` (tranche 9) — **eight tranches apart, in one section**.

## 4. The zero is **falsifiable**, which is the only reason it is worth printing

The instance this rule was built from **was closed in the commit before `AS_OF`** — tranche 9
annotated tranche 1's sentence — so at `AS_OF` the rule correctly reports this record as accounted
for. **A rule that reports nothing is indistinguishable from a rule that sees nothing.** So the same
rule is asked the same pair one commit earlier, and `P30` requires it to fire:

| revision | mentions | newest | verdict |
|---|---|---|---|
| `0cb0fa4^` | 1 | `f26d5be` (tranche 1) | **OVERTAKEN by `e29ba2a`** |
| `0cb0fa4` | 7 | `0cb0fa4` (tranche 9) | NOT OVERTAKEN |

**The rule moved because the record did.** Both halves are asserted: turning either one green alone
means the rule stopped depending on the record, or stopped depending on the repository.

## 5. What this tranche leaves — reported at the low water mark

**`N28` stays in `KNOWN_DEFECT`, and `N29` says where its limit actually went.** This tranche does
*not* turn `N28` green: `worklist.py`'s `named` field is still a substring count, and the date lives
in a **new rule in a new file**. What the date buys is an **impossibility** — an older sentence
*cannot* be an accounting — which is the only thing a rule can have. It does **not** identify
accounting: a younger sentence *might* be one and need not be.

> `N29`'s instance is real and it is in this record. The newest mention of
> `landscape_repair_audit_3b51` here is tranche 6's sentence about **two directories going silent in
> a grep census** — which says nothing whatever about the pin tranche 4 landed on it, and closes the
> pair anyway. So `N28`'s remedy survives unchanged: **the instrument prints the sentence.**

- **`N30` — zero mentions is zero pairs.** One work-list row, `code/summary_guard_audit_407f`, is
  named by **no** record in the tree, and this rule is blind to it at every revision by construction.
  It is the one figure in `out_exemplars.txt` that **grows when the corpus gets worse**.
- **Blame is the last touch, not the origin.** A reflow re-dates a sentence it did not change, so
  **140 is a low water mark**. Declared rather than left to be discovered.
- **`P31` — a directory name is a whole token**, which is `mg-23af`'s rule arriving in a new file on
  a new subject, and it costs **52 lines**. One work-list row is a *subdirectory* whose basename is
  an ordinary English word — `code/mirror_staleness_cdd5/prerepair` — and the loose spelling matches
  inside every `k1_prerepair.py` in the estate. **Both directions are real data rather than a
  plant:** the path spelling in this README still fires, because `/` is not a word character.
- **The order index assumes a linear history**, and there are **0** merge commits at `AS_OF` because
  the refinery rebases. Counted rather than assumed — the day that changes, the count says so.
- **`docs/FACTS.md` and `docs/CONCEPTS.md` get no entry**, for `mg-3da1`'s reason a fourth time:
  every measurement here is consumed by this landing, which fails the registry's own homelessness
  test. `STATE.md` is untouched, so the ratchet is untouched and no twin re-pin is owed.

### It bit again: `out_consumers.txt` moves `200` → `202`, and **tranche 9's own transcript was stale at its own commit**

Neither `+1` is this branch's, checked rather than assumed: `code/lstar_code_9d9e/run_all.sh` at
`3561300` and `code/lever_test_5987/run_all.sh` at `de9709c`, both main's, both landed **while
tranche 9's branch was open**. The tree at `0cb0fa4` holds **202** files named `run_all.sh` and the
transcript committed there says **200**.

That is the third time in four tranches — `mg-e5f3`'s and `mg-44da`'s transcripts went stale the same
way, and `mg-23af`'s did not. The diagnosis has not changed and does not need re-deriving:
`consumers.py` reads the **live index** by design, so its figure is a function of *when you ran it*
and not of the commit you attach it to, and every rebase re-opens the hole.

**Reported and not repaired, and this is the second tranche to decline it** — which is worth saying
plainly, because a sentence that three tranches have written and none has acted on is *this arc's own
subject arriving in its own record*. The reason is unchanged and is a scope reason rather than a
difficulty one: giving `consumers.py` an `AS_OF` changes what its published figure **means** (live
tree → declared commit) and would move a number this branch is not measuring, in the same commit as
a claim about something else. **This branch's own `202` carries exactly the same property**, and
will be wrong the moment a `run_all.sh` lands on main before it merges. `out_exemplars.txt` cannot
go stale that way and `out_consumers.txt` can, in one directory, which is the whole difference an
`AS_OF` makes.

---

# Tranche 11 (`mg-ede8`) — the transcript that has no fixed point, and **5 of its 8 committed versions were already wrong when they were written**

Three tranches wrote the diagnosis and none acted on it. Tranche 10's own words:

> `consumers.py` reads the **live index** by design, so its figure is a function of *when you ran it*
> and not of the commit you attach it to, and every rebase re-opens the hole. […] **This branch's own
> `202` carries exactly the same property.**

It did. **`182d93b`, the commit carrying that paragraph, holds `202` in its transcript and `203` in
its tree** — so the sentence declining the repair shipped inside the fifth instance of the thing it
was declining. That is not carelessness and being careful will not close it, which tranche 7 had
already demonstrated by diagnosing the drift in the commit message of the commit that was carrying
it.

**What this tranche does is not the `AS_OF` the last three declined.** Pinning `consumers.py` would
change what its figure *means* — live tree → declared commit — and the reason it is unpinned is
good: it must answer about *the tree you are about to change*. What was missing is not a pin. It is
**an instrument that can tell whether a committed transcript was already wrong at its own commit**,
and there was none: `mg-f771`'s `g0` sees the transcript *move*, and cannot see that the committed
one was stale to begin with.

`liveindex.py`, in `run_all.sh`, `out_liveindex.txt`.

## 1. The measurement, and it needs no instrument execution at all

A figure is re-derivable at an arbitrary commit **exactly when it is a function of the tracked path
list alone**. Then the number the transcript printed can be compared with the number the tree
*carrying that transcript* implies — `git ls-tree -r --name-only`, and nothing else. No suite is
run, no worktree is touched, and **today's rule is never run against an old tree**, which is the
comparison that would conflate *the corpus moved* with *the instrument changed*.

Four of `out_consumers.txt`'s figures are in that class: `subject scripts`, the two halves of the
unique/shared split, and the shared-basename counts. Every version of the transcript, at `AS_OF
2901996`:

| commit | tranche | said | tree | |
|---|---|---|---|---|
| `182d93b` | 10 `mg-0bf1` | 202 | 203 | **STALE** −1 |
| `0cb0fa4` | 9 `mg-e8b0` | 200 | 202 | **STALE** −2 |
| `828a0fa` | 8 `mg-23af` | 198 | 198 | agrees |
| `ccd925c` | 7 `mg-44da` | 196 | 197 | **STALE** −1 |
| `93ead80` | 6 `mg-e5f3` | 194 | 195 | **STALE** −1 |
| `820ade4` | 3 `mg-4020` | 193 | 193 | agrees |
| `d3dd664` | 2 `mg-6e4f` | 192 | 192 | agrees |
| `3d9ad71` | 2 `mg-6e4f` | 193 | 192 | **STALE** +1 |

**Every claim the record already made about this reproduces**, which is the only reason the two it
did *not* make are worth anything: tranche 10 said `mg-e5f3`'s and `mg-44da`'s went stale and
`mg-23af`'s did not, and all three come back exactly that way.

## 2. The drift goes **both ways**, and only one direction had ever been looked for

`3d9ad71` — **the commit that created this transcript** — printed `193` into a tree holding `192`.
Its count was too **high**: the census was taken on a tree carrying *more* of the named file than the
commit that carries the answer. `consumers.py`'s own header describes the event in prose —

> `run_all.sh (193 files)` became `(192)` the day main folded one suite into another

— and the transcript beside that sentence is the one carrying the stale `193`. Reporting only the
low direction would have made this a census of *"main landed something while I was open"*, which is a
smaller claim than the true one: **the figure is a function of when it was taken, in whichever
direction the estate happened to move.**

## 3. Why the live half is on **stderr** and gates nothing

The staleness is created by the **merge queue**. The refinery rebases the branch onto a main that has
landed directories since the run, and that rebase happens *after the last moment anything on the
branch can run*. So no instrument on the branch can prevent it, and a gate here would be red for
reasons the author cannot act on — `mg-724a`'s recorded/gated split, arriving on a live-index figure.

`liveindex.py` therefore prints its live check on **stderr**: *the committed transcript is stale for
this tree right now*. It reads the **committed** copy and not the worktree one, and that is the whole
design — `run_all.sh` regenerates `out_consumers.txt` two lines earlier, so a comparison against the
worktree copy would be a figure compared with itself and would pass on every run. It fires today, on
this branch, before this branch's own refresh.

**What would actually close it, none of which is done here:** a refinery that re-runs the producer and
amends after the rebase; or a figure that stops being live-index-valued, which contradicts the reason
`consumers.py` is unpinned.

## 4. What this tranche leaves — reported at the low water mark

- **`N31` — `AGREES` is one-directional**, and it is `worklist.py`'s `FALSIFIED` / `NOT FALSIFIED`
  discipline one subject along. `STALE` is a proof; `AGREES` covers four figures out of a transcript
  that has many. The prose count, the named-in-no-tracked-file count and the whole of sections A, B
  and C are **content**-valued and are invisible here — re-deriving those means running today's rule
  against an old tree. `N31` joins `KNOWN_DEFECT` (8 → 9) and **nothing leaves**.
- **The registry is one row, and that is a statement about this directory and not the estate.** One
  transcript *here* reads the live index; nothing scans `code/` for the others, so a live-index
  producer one directory over is invisible at every revision. That is `N30`'s shape on a new subject.
- **The remedy exhibited the defect it remedies, on its own first run** — and `P34` is what caught it.
  With the shared-basename line emptied, the first reader returned *zero pairs* and the comparison
  graded it **STALE**: a census reporting a finding about a figure it had failed to read, which is
  `git_grep_l`'s original defect one file over. The reader was tightened rather than the plant
  relaxed, and it took **two** clauses, because an empty payload reconstructs exactly.
- **A second mixture, reported and not repaired.** `consumers.py` builds its frequency table from
  `git ls-files` — the **index** — and runs its section A/B/C greps against **HEAD**. On a clean tree
  those are one tree; on a dirty one the counts and the listings answer about different trees with
  nothing saying so. It belongs to `consumers.py`.
- **`out_pinnable_3b51.txt`** is still a dated hand-run that no suite re-takes, **1 of the 80
  surviving hits is still prose inside a `print(...)`**, `N27`'s 24-character `find(1)` window is
  still open, and **`P24` is burned** and must never be issued.
- **This branch's own `out_consumers.txt` carries the same property** and will be wrong the moment a
  `run_all.sh` lands on main before it merges — which is now a *measurable* claim rather than a
  warning, because `liveindex.py` will say so at the next commit that writes the file.

---
# Tranche 12 (`mg-5058`) — which declared limits are **date questions**, and the two that provably are not

**RENUMBERED ON LANDING, AND THE RENAMING IS RECORDED RATHER THAN QUIETLY DONE.** This section was
written as tranche 11 against `182d93b`. `mg-ede8`'s tranche 11 merged while this branch sat in the
merge queue and issued `P32`, `P33`, `P34` and `N31` to `liveindex.py` — a different instrument
about a different subject. Numbers in this directory are **never reissued** (`BURNED`, and the
control above it), so this tranche's six controls became `P35`, `P36`, `P37`, `P38`, `P39` and
`N32`, in that order, and the heading became tranche 12. **Not one word of the argument moved** —
only the labels — and the map is printed here so a reader holding this branch's own commit message,
which names the old numbers, can follow it.


Tranche 10 closed with one question, and it is the whole of this tranche:

> is **any** remaining *"read what the sentence says"* rule in this estate likewise a date question
> wearing semantic clothes?

**The answer is yes for one more and provably no for two, and the interesting half is the no.** A
limit is not shown to need English by nobody having found a rule — that is an absence of evidence,
and this arc does not publish those. It is shown by a **collision witness**: two real lines whose
readings are opposite and whose **commit is the same**. Every commit-level field — sha, date, author,
order index, what landed before and after — is then literally identical across the two readings, so
**no** rule reading any of them can separate the pair. That is an impossibility rather than a failure
to find something, which is the only thing a rule can have.

The instrument is `semantic.py`, it ships in `run_all.sh`, and its transcript reproduces
byte-identically for `exemplars.py`'s reason with one of its own on top: **two of its four rows read
their declaration out of `selftest_20ee.py`, which this branch edits**, and one of its population
figures counts that same file — so a version reading off disk would have its numbers moved by the
commit that adds its own controls. `P35` replaces `open` for the entire scan, the estate census
included.

## 1. One rule, four rows

Every row is the same question asked of a different declared limit:

> Given two witnesses whose readings are opposite, and an **event** in the repository that one
> reading puts before them and the other after — does the event lie **strictly between** them in
> commit order?

| | |
|---|---|
| the witnesses share a commit | **COLLIDES** — no event can lie between them. **Proved.** |
| the row's field separates them | **SEPARATED** — this field decides *these two*. A candidate rule, not a theorem. |
| neither | **NOT SEPARATED**, which proves nothing |

**One-directional, and the direction is the opposite of `exemplars.py`'s.** There the rule *firing*
was the informative answer; here it is the rule *failing to separate*. Both files publish the
direction their evidence can actually carry.

**Where the class labels come from, which is not from me.** A collision witness is worth nothing if
the two readings are the author's opinion, so each row's labels are taken from the record that
*declared* the limit — `mg-aaf4`'s §7 names its own MENTION unit, this directory's `N28` names its
own two sentences — and the declaration is **checked present at `AS_OF`**, printed with its file, so
a row whose declaration has been deleted reads `GONE` rather than standing as a claim about a
document that no longer says it (`P37`, both halves deletion-tested).

## 2. The verdict

At `AS_OF = 182d93b`, over **43** prose-scoped declarations of *"cannot tell / distinguish /
separate"* in **37** tracked files (**209** loose in `.py`/`.md`/`.sh`, and **77** more in `.txt`
excluded as echoes of the `.py` that printed them):

| row | limit | verdict |
|---|---|---|
| `R1` | ACCOUNTING vs OFFERING — `N28`, the one tranche 10 closed | **SEPARATED** by the pin `e29ba2a` |
| `R2` | a **younger** mention: ACCOUNTING vs a **quotation of the offer** — `N29` | **COLLIDES** at `0cb0fa4` |
| `R3` | a strike marker **USED** vs **MENTIONED** — `mg-aaf4` §7 | **COLLIDES** at `522c1f3` |
| `R4` | a **transcript** recording a failure vs a **pre-registration** recording a refuted prediction — `mg-9876`'s `a4` §3 | **SEPARATED** by the arm's first commit |

The criterion that falls out of the four is one sentence:

> **A semantic-looking distinction is a date question exactly when the two readings put the text on
> opposite sides of an event that is itself a commit.**

`R1` has one — the pin. `R4` has one — the first commit of an arm. `R3` has **none**: *what this
marker is for* is not an event in the repository at all, so there are not two dates to order, which
is why it collides rather than merely failing to separate.

## 3. `R2` is the sharpest row, and it is this record's own

`R2` **has** an event and collides anyway. Its two witnesses are `README.md:117` and `README.md:1060`,
943 lines apart, both written by `0cb0fa4`:

| line | reading |
|---|---|
| 117 | *"`species_remainder_f8fa` was **pinned at `e29ba2a`**"* — an **accounting** |
| 1060 | *"the small ones (`species_remainder_f8fa` at `2+/2-` …) are cheap"* — **not** one: it is tranche 1's offer, **quoted** |

**And line 1060 is the same English sentence as line 111**, which is `R1`'s first witness and which
the date decides correctly. Tranche 9 quoted it while annotating it.

> **A quotation moves the sentence without moving the event.** The date is a property of the touch
> and the reading is a property of the words, and a quotation is where those two come apart on
> purpose. This is *"blame is the last touch, not the origin"* — tranche 10's own declared limit —
> arriving from the other side: there a reflow re-dates a sentence nobody changed, here a quotation
> re-dates one somebody deliberately reproduced.

## 4. The new date row, measured over the estate and not over two lines

`R4`'s field is an impossibility of exactly tranche 10's shape: **a suite's transcript is written by
an arm, so it cannot pre-date every arm of its own directory.** A file that does is not that suite's
transcript, whatever tokens it contains — and no English is read anywhere.

| | |
|---|---|
| `PREDICTIONS.md` in the tree | **129** |
| … **provably** pre-registered (older than every arm) | **90** |
| … born with an arm, so not provable here | 39 |
| directories where `a4`'s red-token row fires | **154** of 233 |
| … where it fires **only** through a `PREDICTIONS.md` | **5** |
| … of those, the date **proves** it is not a transcript | **3** |

The five are named in the transcript. `code/c3_audit_a94c3` is the witness, and its single red token
is a sentence *forbidding* the word: *"Reporting `P4` as `REFUTED` would be wrong"*. **Reported and
not repaired** — the row is `mg-9876`'s, and a branch that re-scoped another instrument's detector to
make its own number read better would be doing the worse thing (`mg-99f4`'s shape, whose `+1` was a
`PREDICTIONS.md`).

**One-directional again**: *older than every arm* proves it is not a transcript; **born with an arm
proves nothing**, and 39 of the 129 are in that state.

## 5. What this tranche leaves — reported at the low water mark

- **`N32` — the registry is a hand judgement, and this file cannot decide it.** Which of the 43
  declarations are about reading a sentence, and which reading each witness carries, are read by a
  person. The control is asserted on the row that is its own instance: `R2`'s two witnesses **agree
  on every field the repository has** and **disagree only in a sentence somebody wrote into
  `REGISTRY`**. That is precisely why the row proves what it proves, and precisely why the labels are
  derived from nothing. The remedy is the one `N28` named: **the instrument prints the sentence.**
- **A label could be derived from the field it is tested against, and `R4`'s first draft was.** The
  pre-registration witness was labelled *"committed before any arm of its directory"* — the field
  verbatim — so the row would have asserted that the field separates two labels the field had
  assigned. **A circle that passes.** The label is now what a reader can check in the file (it is that
  directory's only red token and it sits in a sentence forbidding the word) and the date is the only
  thing measured. Found by the rule this directory applies to itself: *a remedy is an artifact of the
  same kind as the defect.*
- **A collision is about the witnesses, not about the whole limit.** It kills a *proposed rule* —
  every rule reading commit-level metadata — and is not a proof that the limit is unclosable by any
  means. A rule reading **document structure**, as `exemplars.py` §3 does, is not a rule reading a
  commit.
- **39 of the 43 are untested**, because a witness pair is a hand judgement and this tranche affords
  four. Section 1 of the transcript lists every site. The one worth naming is `mg-9876`'s own *"a
  regex cannot tell an arm from a `print`"*, whose two readings — `mg-585e`'s `loose_red` control and
  `lib585e.py`'s guarded `if old not in text:` — sit in one directory and **two** commits, so that row
  needs a witness pair this tranche did not have.
- **Both `git grep` prefilters are wider than the rules they feed**, which is the only safe direction
  and is asserted in both (`P38`): a wider prefilter may hand over files the rule then rejects and
  **cannot hide one**. The measured confirmation is a level up — the estate census was run *both
  ways* at `AS_OF`, prefiltered and reading every tracked `.txt`/`.md`, and the two transcripts are
  byte-identical.
- **`P25` fired on this branch, and on exactly what it is for.** `semantic.py`'s `grep_files`
  docstring said *"`P39` runs it"* before any `P39` existed — a sentence whose entire content is *go
  and check*, naming somewhere with nothing at it, which is the defect `mg-23af` built that control
  from. It was caught by running the suite, not by reading, and the repair is the control rather than
  the sentence: `P39` now runs the tolerance, on a needle assembled from pieces so it cannot find
  itself (`C5`'s rule).
- **`KNOWN_DEFECT` grows `8` → `9` and the suite `57` → `63` controls**, all green. `STATE.md` is
  untouched so the ratchet is untouched and no twin re-pin is owed; `docs/FACTS.md` and
  `docs/CONCEPTS.md` get no entry for `mg-3da1`'s reason a fifth time, every measurement here being
  consumed by this landing.

### It bit a fourth time: `out_consumers.txt` moves `202` → `203`, and the `+1` is **main's**

The tree at `182d93b` holds **203** files named `run_all.sh` and the transcript committed there says
**202**. The `+1` is `code/verdict_invariance_585e/run_all.sh` at `83a33c4` — `mg-585e`'s landing,
which merged while tranche 10's branch was open. Checked rather than assumed: this branch adds **no**
`run_all.sh`.

That is the fourth tranche in five whose consumers transcript shipped stale at its own commit. The
diagnosis has not changed: `consumers.py` reads the **live index** by design, so its figure is a
function of *when you ran it* rather than of the commit you attach it to. **Reported and not
repaired, and this is the third tranche to decline it** — the reason is unchanged and is scope rather
than difficulty, and **this branch's own `203` carries exactly the same property**. `out_census.txt`,
`out_permuted.txt`, `out_worklist.txt` and `out_exemplars.txt` do **not** move, checked against the
dirty worktree rather than assumed, because all four are pinned.

`mg-9876`'s arm census does not move either, and all three numerators were checked with `a4`'s own
predicates rather than inferred: this branch adds **zero** directories, **zero** whole-output
membership sites (`semantic.py` and the new controls contribute none), **zero** new
negative-control basenames, and the `RED_TOKEN` membership this directory already had — `CAUGHT`
inside a quoted commit subject in `out_worklist.txt` — is unchanged, so `out_semantic.txt` carrying
`REFUTED` adds nothing the row counts.

---

# Tranche 13 (`mg-3ebf`) — the residue was **1 row and not 5**, and the two things the ticket asked for turned out to be one thing

`mg-e8b0`'s tranche 10 handed a successor two items in priority order. **Item 1** was the residue:
`out_worklist.txt` section 4's five rows, *"the rows nothing on record has yet given a reason to
skip"*. **Item 2** was one observation about one **pinned** instrument, `anchor_drift_96df`, whose
transcript still drifts because its address is in **another repository** — filed as a third class
`pinnable.py` has no rule for, and expressly **not built**:

> Reported, not built — a rule about foreign repos is a change whose false-positive direction nobody
> has measured.

**They are the same item.** Working item 1 by hand produced item 2's class, four more times, inside
the residue.

## 1. Four of the five residue rows read a corpus **no `AS_OF` of this repository reaches**

All five suites were run, their worktree diffs read, `pinnable.py` run on each, and their scripts
read at `AS_OF`. Every foreign root below was found **by hand, before any rule existed**:

| row | root | |
|---|---|---|
| `summary_guard_audit_407f` | `SRC2 = "/Users/daniel/research/one_third_width_three"` | another repository |
| `superseded_descent_688c` | `MIRROR_REPO` = the same, and `MG_ROOT = ~/.macguffin` | both |
| `verdict_delivery_bf3f` | `MG_DEFAULT = ~/.macguffin` | the `mg` store |
| `landing_audit_sweep_64cb` | `STORE = ~/.macguffin/work`, `EVENTS = …/events.jsonl` | the `mg` store |
| `eps_spec_sweep_372e` | — **nothing** | **the one clean row** |

So the sentence the record has carried forward is **true about the prefilter and false about the
work**. Conditions 1–3 cost about forty-five minutes each and on those four they **cannot succeed**:
there is no commit here whose content decides what those transcripts print. `407f` is the sharpest —
its committed transcript records six `[FINDING]`s about `census_repair_f3ff` that the re-run does not
reproduce, and `census_repair_f3ff` **has had no commit since the sweep**. The verdict moved because
the *foreign* repository did.

**The residue is `code/eps_spec_sweep_372e`.** That is the deliverable, and it is a
subtraction rather than an addition.

## 2. `R4`, and the guard is where the measurement went

> **R4 A CORPUS ROOT OUTSIDE THIS REPOSITORY.** A tracked script in the subject **binds a
> module-level constant** to a string literal naming an absolute or home-relative filesystem root.

R4 is **decidable, not heuristic**, which is why it is worth having beside `R1`'s `check-ignore` and
`R2`'s `cat-file -e`: `~/.macguffin` is not in this repository, and that is a fact about where the
path points rather than a guess about intent.

**The `bound` guard is not cosmetic and its absence is what the ticket was worried about.** Without
it R4 fires on **28 of 44** rows and on **3 of the 8 rows a pin has already landed on** — including
`landscape_repair_1953`, which is `pinnable.py`'s **own** named example of the shape `mg-20ee`'s
remedy was built for. A rule waving off the estate's model pinning is not conservative, it is wrong.
With it: **9 rows**, and the one pinned row left is **`anchor_drift_96df`** — the ticket's own
instance, and the pinned row whose transcript still drifts. `P49` plants the amputation and requires
both halves.

**The argument for the guard, so it can be argued with:** a corpus root is bound to a name because
the instrument refers to it repeatedly; an inline path is an argument to one call. Every true
positive is a named constant; the three false positives read by hand first are all inline —
`"/docs/"`, `"/**/mg-*.md"`, `"/bin/sh"`.

**And it was fitted to this corpus, which is said out loud rather than glossed.** It was chosen
*after* reading those three, so the 44-row counts are the sample it was fitted to and **not
independent evidence for it**. What is independent is the direction, and `P47` pins it: the four
hand-read roots must survive, and `372e` must stay silent.

## 3. The false-positive direction, which is what the ticket said nobody had

Four designs, scored from **one walk** so the comparison cannot be about four slightly different
walkers:

| shape | literals | rows | **pinned rows** |
|---|---|---|---|
| naive line match (comments included) | 120 | — | — |
| ast, any outside literal + arena | 65 | 28 | **3** |
| + docstrings excluded | 65 | 28 | 3 |
| + arena excluded | 29 | 13 | 2 |
| **+ bound to a module constant (the rule)** | **16** | **9** | **1** |

**One column bought nothing and it says so.** Excluding docstrings removes **0** literals on this
corpus — `REQUIRED-INERT`, kept for the shape and not for a number it did not move. Reporting it as
load-bearing because it is *reasonable* would be the defect `permuted.py` found under its own
`18 of 129`.

**`tempfile.mkdtemp` is counted and is not in the rule.** An arena path is in no commit *by
construction*, but **its content is written by the instrument itself**, so it is not a foreign
corpus. It drifts only when the path is **printed** — `407f`'s transcript does carry its arena path —
and that is a property of the transcript, which `R1` reads and this file does not. It is **half of
all the firing**.

### The precision, adjudicated by hand at both grains

Every literal the rule fires on was read at `AS_OF` and graded, as **data** in `foreign.py`'s source
so `P48` can check the grades still cover what the rule does, in both directions:

- **11 of 16 literals** and **7 of 9 rows** are `CORPUS` — a true foreign corpus root.
- **1** is `SELF`: `/Users/daniel/research/onethird_program`, this repository spelled absolutely. No
  `AS_OF` reaches it either, but its remedy is **relativisation, not a pin**, so it is counted apart.
- **4** are the declared over-count, and **the 2 false rows are named**: `runner_exit_audit_dee4` and
  `runner_exit_c2b3`, both on `/bin/sh` (and one `/%s/`).

**The over-count stops there and is declared rather than tuned away.** `/bin/sh` is outside this
repository and that is true and useless — but telling the **corpus** an instrument reads from the
**tool** it runs is the difference between an instrument's subject and its evidence, which
`pinnable.py` already records as not decidable from the token. A fourth guard fitted to a
sixteen-literal sample would be the fourth thing chosen after seeing the answer.

## 4. Why this is not already `R1`, measured rather than asserted

`git check-ignore` answers **no** for every root in §1 — `var/folders/…`, `…/one_third_width_three`,
`…/.macguffin/work`. `R1` *did* fire on `407f`, and that is exactly why it must not be read as
coverage: it matched `Users/daniel/.pogo/polecats/<name>/…` against **`.pogo/` in
`.git/info/exclude`** — this repository's ignore configuration accidentally matching a path *outside*
the repository. Right answer, wrong mechanism; change one line of that file and the only hit
disappears while the class does not. On the other three foreign rows `R1` printed `none`, and **`none`
reads to its reader as residue**, which is how four unreachable rows got onto a work-list.

## 5. The remedy exhibited the defect it remedies, and it was found by running it

`classify_root`'s **first draft called `os.path.realpath`** on each literal and compared against this
worktree and the repository's common git dir. Both halves read the machine — so `out_foreign.txt`
would have been a **function of where the repository is on disk** while its docstring claimed every
figure was a function of one commit. A transcript that reproduces for exactly one operator is tranche
1's third class, arriving inside the instrument built to find addresses outside the repository.

Found by **running it**: exactly **one** literal in the 44 rows came back `SELF`, and only because
this checkout happens to live there. **The repair was to delete the question, not to compare better**
— an absolute path to your own checkout is not reachable by an `AS_OF` either, so excluding it was
never right, it merely looked tidy. `classify_root` now touches **no filesystem at all** and that
literal is carried in `ADJUDICATED` under its own grade. `P46` asserts both the three verdicts **and
the removal**, because a reintroduced `SELF_ROOTS` would make these figures machine-dependent again
and an arm checking only the verdicts would not see it.

### And it fails its own rule: `R4` fires on `foreign.py`, **11 times**

Every hit is the `ADJUDICATED` table — a **grade sheet**, not a corpus read. **The detector contains
the tokens it detects**, which is the README's §4 for the *fifth* time in this arc, and §4's remedy
does not apply: it says assemble the needle at runtime, and a table of adjudicated literals cannot
avoid containing those literals (`pinnable.py`'s `R3` makes the same argument about its own regex).

**The count is on `stderr`, and that is the rule arriving in the directory whose subject it is.**
`foreign.py` does not exist at `AS_OF`, so there is no commit to read it at and the grading must read
the **worktree** — a branch-dependent figure, which on stdout would make `out_foreign.txt` a function
of the tree rather than of one commit. That is `README D4` and `liveindex.py`'s arrangement.
`P50` keeps it on the build path instead, and asserts the **split**: `foreign.py`'s self-hits must be
*exactly* the `ADJUDICATED` keys, and `selftest_20ee.py` and `worklist.py` must be at **0** — so a
foreign root introduced anywhere else here goes red rather than being absorbed into *"it always fires
on itself"*.

`foreign.py` is also **outside its own population by arithmetic rather than by rule** — the `AS_OF`
predates it, so it is not tracked at the commit it reports on and cannot appear in the 44. That is
`pathlist.py`'s declared shape: an exemption nobody wrote and nobody should rely on.

## 6. `foreign.py` is **on the build path**, which is the four-tranche complaint answered

`pinnable.py` cannot be, because it classifies a **worktree diff** and so requires a suite to have
been run and not restored — which is why `out_pinnable_3b51.txt`, `out_pinnable_a4ef.txt` and
`out_pinnable_b0ae.txt` are one dated hand-run each that **no suite re-takes**, declared in the same
words since tranche 7. R4 needs no diff: it reads tracked scripts at a declared commit through
`git ls-tree` and `git show`. Every figure is a function of **one commit**, so `out_foreign.txt`
reproduces **byte-identically** and the file is in `run_all.sh` — `worklist.py`'s, `exemplars.py`'s
and `semantic.py`'s arrangement, arriving on the class that was carrying the complaint.

`worklist.py` gains **`residue_rows`** and nothing else: section 4's three-clause prefilter extracted
to a function so `foreign.py` calls it instead of re-spelling it, because two spellings could publish
different residues with no reader able to tell which was wrong (`mg-1344`'s `P5`). **A pure
extraction is a claim**, so `P45` runs both spellings and `out_worklist.txt` is byte-identical across
the change.

## 7. What tranche 13 leaves

- **`eps_spec_sweep_372e` is the residue**, and conditions 1–3 on it are the next tranche's cheapest
  real work. `pinnable.py` fires **no** pre-condition on it and R4 is silent.
- **The four foreign rows are a different question and a bigger one.** `688c` and `64cb` read a
  repository and a store that **have** revisions; pinning against those is a real remedy this arc has
  never attempted. **Do not commit a foreign repository's `HEAD` into this one.**
- **`anchor_drift_96df` is still unowned and its alarm is still ringing** — `mg-688c`'s pinned table
  needs re-deriving, which is that directory's work. Unchanged from tranche 10.
- **`N34`** is the declared limit and runs in the **safe** direction: the population is the 44
  work-list rows and nothing scans `code/` for the rest, and R4 matches **literals**, so an
  environment variable or an assembled path is invisible. Both errors make the foreign class look
  **smaller**, so `9` and `4 of 5` are **low water marks** and *"the residue is 1 row"* can only
  shrink.
- **`census_remainder_f8e5` was not re-run**, for the reason the original sweep gives: its worker
  does not terminate in a usable time. Unchanged, and restated because any tranche quoting the
  re-run's counts must quote them over the rows it covers.
- **`KNOWN_DEFECT` grows `11` → `12` and the suite `73` → `80` controls**, all green — 41 positive,
  31 negative. `STATE.md` is untouched so the ratchet is untouched and no twin re-pin is owed;
  `docs/FACTS.md` gets **no** entry (`mg-3da1`'s homelessness test an eighth time — every measurement
  here is consumed by this landing) and `docs/CONCEPTS.md` no row.

### It bit again: `out_consumers.txt` moves `205` → `209`, and **not one of the four is this branch's**

The tree at `HEAD` holds **209** files named `run_all.sh` and the transcript committed at `d94de4f`
says **205**. The four are `code/empty_vs_zero_3c92/run_all.sh` (`mg-3c92`),
`code/label_vs_computation_68ef/run_all.sh` (`mg-68ef`),
`code/oscillation_discharge_365a/run_all.sh` (`mg-365a`) and
`code/prerebase_reading_cd8d/run_all.sh` (`mg-cd8d`) — all **main's own** landings whose consumers
refresh main did not take — **attributed by diffing the `run_all.sh` list at both commits rather than
assumed**. This branch adds **no** `run_all.sh`.

**Two of the four arrived during the rebase, which is the mechanism rather than an anecdote.** The
figure read `207` before `git rebase origin/main` and `209` after, because `mg-3c92` and `mg-68ef`
landed while this branch was open. That diagnosis is unchanged and is still declined for scope:
`consumers.py` reads the **live index** by design, so its figure is a function of *when you ran it*,
and **this branch's own `209` will be wrong the moment another `run_all.sh` lands before it merges** —
the refinery's rebase happening after the last moment anything on the branch can run.

`out_census.txt`, `out_permuted.txt`, `out_worklist.txt`, `out_exemplars.txt`, `out_liveindex.txt`
and `out_pathlist.txt` do **not** move, checked against the dirty worktree rather than assumed,
because all of them are pinned.

---

<<<<<<< HEAD
# Tranche 14 (`mg-528e`) — the residue is pinned, and the pre-condition that cleared it was wrong about it

Tranche 13 subtracted four rows from the work-list's residue and left **one**:
`code/eps_spec_sweep_372e`, the row with no foreign corpus root, on which
`pinnable.py` fires nothing and `R4` is silent. **Conditions 1–3 are paid on it
here**, which is the first time this arc has closed a residue to zero rather than
reporting one — and working it produced a defect in the instrument that had
screened it, which is the same shape tranche 13's own §1 has.

## 1. The pin, and the residue is TWELVE FILES

`AS_OF = dafe759` — `mg-372e`'s own landing, an ancestor of `origin/main`
(condition 1), and the commit that carries all three scripts and all three
transcripts. **Not its parent**, which is worth saying because AS_OF rule 2 says
otherwise for the general case: this sweep **edits the documents it sweeps**, so the
state it read is the post-edit one.

**Condition 2, scored by `permuted.py --declare` against declarations committed
BEFORE the transcripts were regenerated:** `PERMUTATION + DECLARED RESIDUE` on all
three, **0 undeclared** on each. `out_s2_classify.txt` and `out_s3_control.txt`
permute by **0** and their entire residue is the **six-line `AS_OF` block** — the
cleanest condition 2 has come back on this arc, and both were **byte-identical** at
`AS_OF` before the header existed.

**And `s1`'s census reproduced FILE FOR FILE, 50 of 50.** Every file the committed
transcript lists carries exactly its committed count at `AS_OF`. The whole
`288 → 406` gap is **twelve files that were not in the tree the sweep read**:
eleven are `mg-eaa1`'s landing (117 hits) which landed **three commits earlier**
while `mg-372e`'s branch was open and which the refinery's rebase put underneath;
the twelfth is `out_s1_census.txt` itself, **the census counting its own
not-yet-written transcript** — tranche 1's third defect, still live in a row four
tranches of prefiltering had left standing.

So `mg-188d`'s *"the population is the whole repository"* is confirmed **and
sharpened**: at HEAD the drift is 87 files and unbounded, at the carrying commit it
is twelve and eleven of them are one other ticket's landing.

**Condition 3:** `0 CONFIRMED, 1 UNCONFIRMED` — `code/rendered_twin_pin_9bc2`, which
names those scripts in a **docstring** and does not run them. The census's own
backstop was run rather than reasoned about: `9bc2`'s suite across this change
leaves its committed transcripts **byte-identical**.

**And condition 3 missed a real consumer, in a shape `consumers.py` has no rule
for.** `code/rate_sweep_910c/out_mg372e_rerun.txt` is a **committed copy of `s1`'s
page**, taken by hand at `mg-910c`'s own time and reading `423` — a *third* dated
value beside the committed `288` and the pinned `406`. No script in `910c` produces
it (`run_all.sh` there runs `r1`/`r2`/`r3` and nothing else), so there is no
execution to find and no filename to grep: **it is a consumer by COPY.** That is
`consumers.py`'s section D limit in a new shape, and it runs in the *unsafe*
direction for a reader, because the copy carries no `AS_OF` and nothing will ever
re-take it. **Reported, not repaired** — the file is `mg-910c`'s.

## 2. `N36` — `R3` printed `none` about a walk that really is unordered

`pinnable.py` cleared this row with *"every corpus read this rule can see is either
an ordered read of a commit or sorted by the subject itself."* **It was wrong**, and
the transcript the instrument produced proves it: the committed `COLLISION` list is
in **directory-enumeration order**, and the pinned read permutes 11 of 85 core
positions.

`R3` finds the `os.walk`; the `ORDERED` guard suppresses it because
`sorted(filenames)` is in the enclosing block. That sorts files **within** a
directory and says nothing about the order the **directories** are visited in.
Amputate `ORDERED` and the rule finds it at once — which is `N36`'s second element
rather than an assertion.

**The direction is the unsafe one**, and that is why it is `N` and not a repair:
`R3`'s misses read to their reader as *nothing to declare*, so a transcript with no
fixed point looks pinnable. **Not repaired here** — widening `ORDERED` is a rule
change whose false-positive direction nobody has measured, and the two instruments
tranche 1 pinned to byte-identity are each `os.walk` + `sorted(out)` a few lines
below, which is exactly the shape the guard was written for.

## 3. A pin can delete the question a section asks, and this one nearly did

`s2` and `s3` are **checks**, not censuses. Pinning their corpus freezes their
verdict at `AS_OF`, so a `~~` deleted from a repaired document tomorrow would stop
being caught — `pinnable.py`'s own `state_relocation_audit_b0ae` finding arriving
inside a pin this arc chose to land. **Paid rather than glossed**: the pinned reading
is on **stdout** (the committed transcript) and the same check re-run against the
**working tree** is on **stderr** and in the **exit code** (`mg-724a`'s
recorded/gated split, `liveindex.py`'s and `foreign.py`'s arrangement).

That made the exit code load-bearing, which forced a repair `mg-188d` had recorded
and left: `run_all.sh` piped every script through **`tee`**, whose exit status is
`tee`'s, so every alarm was swallowed by the runner. It writes-then-moves now.
**Two things retire with it** — the README's *"do NOT use `sh run_all.sh` to look,
it destroys the dated readings"* warning (a successful run is byte-identical and
leaves `git status` clean), and its *"WHAT WOULD CHANGE THIS"* hand instruction,
which now runs on every invocation.

## 4. What this tranche does not do

- **The four foreign rows are still not pinned against their foreign revisions.**
  Unchanged from tranche 13, and still a decision rather than a task: it needs a
  second repository, which is a second work item and not a polecat's to reach into.
- **`anchor_drift_96df` is still unowned and its alarm still rings.**
- **`N34`'s estate-wide population is still unmeasured** — nothing scans `code/` for
  foreign roots outside the 44 work-list rows.
- **`out_pinnable_*.txt` are still dated hand-runs no suite re-takes**, but the
  complaint is now answered for one more class: `P56` re-takes **this pin's own
  condition 2** on the build path, with the shipped declarations, at every gate.
- `consumers.py` is still unpinned and its index/HEAD mixture unrepaired.

## 5. Renumbered on landing, and the map is printed — the FOURTH collision in four landings

This branch issued `P51`, `P52`, `P53` and `N35`. **`mg-6219`'s `figures.py` landed
those same four names while this branch sat in the merge queue**, so they became

| issued on the branch | landed as |
|---|---|
| `P51` the residue row's condition 2 | **`P56`** |
| `P52` s3's detector is s2's detector | **`P57`** |
| `P53` the corpus read is anchored | **`P58`** |
| `N35` R3's `ORDERED` suppressed a real walk | **`N36`** |

and **not one word of the argument moved**. A number in this directory is never
reissued — that is what `BURNED` is for and `P25` enforces it. The map is also in
the `KNOWN_DEFECT` comment beside `N36`, so a reader holding this branch's
pre-rebase commit message (which names the old numbers) can follow it. That is
`mg-bdc0`'s and `mg-6219`'s own resolution a third and fourth time, and it is a
fact about the namespace rather than about any branch.

## 6. The one census figure this branch really moves, and the residue it leaves

`| tee` sites: **30 → 27** in **11 → 10** directories, and all three removed lines
are this branch's own — `code/eps_spec_sweep_372e/run_all.sh:5`, `:6` and `:7`,
read off the sweep's diff rather than assumed. `out_gate.txt` carries the new
`audit.sweep_tee_sites observed=27` and is committed on `g0`'s own `DISAGREES`
grading; its wall-clock half (`48.0s → 106.8s`) is a reading of a **loaded box**
and is not a claim about anything.

**`out_a4_sweep.txt` is RESTORED and not committed, and that leaves a residue that
is said out loud rather than left to be found.** `g0` grades it `CORPUS` — its pin
moved `dca19cc6a31f → 338f086294f9` and its population `232 → 239`, which is main's
drift and not this branch's — and its standing instruction is *"restore it rather
than committing it; the refresh is owed by whoever trips the bound."* Instruction
followed. **The cost:** a4's committed transcript goes on listing three `| tee`
sites at lines that no longer contain one, which is `mg-23af`'s dead-pointer shape
in a transcript. Committing it instead would bank main's `232 → 239` inside a
pinning commit, which is the error the rule exists to prevent. The smaller wrong
was chosen; whoever trips a4's bound clears both in one run.
=======
# Tranche 14 (`mg-6b2d`) — the transcripts nothing re-takes, and the one this arc was filed about **cannot be re-taken at all**

**RENUMBERED ON LANDING, AND THE MAP IS PRINTED RATHER THAN THE RENAMING QUIETLY DONE — the third
such collision in four landings in this one namespace.** This section was written as tranche 13
against `637b046` and issued `P45`–`P50` and `N34`. `mg-3ebf`'s `foreign.py` merged while this branch
sat in the merge queue and landed **those same seven names**, about a different instrument and a
different subject. A number in this directory is **never reissued** (`BURNED`, and `P25` enforces
it), so this tranche's seven became `P51`, `P52`, `P53`, `P54`, `P55`, `P56` and `N35`, **in that
order**, and the heading became tranche 14. **Not one word of the argument moved** — only the labels
— and the map is here so a reader holding this branch's own pre-rebase commit message, which names
the old numbers, can follow it. `mg-5058` recorded the first collision and `mg-bdc0` the second;
three in four landings is a fact about the **namespace** and not about any branch.

**`AS_OF` was re-pinned `637b046` → `9d6bbfa` on the rebase, and the arm refused rather than
answering.** See section 1: the hand table has five rows and not three because of it.

**The ticket's first remainder was already discharged before this branch opened, and that is checked
rather than assumed.** `mg-6b2d` carries `mg-44da`'s remainder and names `N25` — *R3's `find` half
requires a following SPACE, so `["find", root, "-type", "f"]` is invisible to it* — as the item worth
taking first. **`mg-23af` took it**, four tranches ago and under this README's own tranche-8 heading:
`selftest_20ee.py` runs `N25 find(1) in the LIST spelling — WAS INVISIBLE, NOW SEEN`, it is green,
`N25` has left `KNOWN_DEFECT`, and `N27` took its place carrying the under-count the repair left
behind. So the ticket's item 1 is closed and item 2 — *1 of the 80 surviving hits is prose inside a
`print(...)`* — is `pinnable.code_only`'s own declared limit, unchanged in kind and still declared in
its docstring. **What is left is item 3, and it turned out not to be a refresh.**

## 1. The remainder that was real, and what happened when it was taken

> `out_pinnable_3b51.txt` still says `R3 FIRES ON THIS DIRECTORY SIX TIMES` — a literal tranche 6
> replaced with a computed count in `pinnable.py`. It is a dated hand-run that **no suite re-takes**.

All three of this directory's `out_pinnable_*.txt` were re-taken by hand during this tranche. **Each
failed for a different reason and not one of them is *nobody got round to it*.** Two more rows joined
on the rebase, and **the arm's own refusal put them there** — see below the table.

| transcript | what happened when it was re-taken |
|---|---|
| `out_pinnable_3b51.txt` | **CANNOT BE RE-TAKEN AT ANY REVISION.** `sh code/landscape_repair_audit_3b51/run_all.sh` ran to exit 0 in 63 s and left `git status` **empty**, so `pinnable.py` refused with *"is EMPTY, and this instrument classifies a drift it is given rather than one it produces"* (exit 1). **The pin tranche 4 landed on that subject worked.** |
| `out_pinnable_a4ef.txt` | **Re-takeable, and its input is not repo state.** The `a4ef` suite's whole drift is `__pycache__` residue — files git is configured never to track, which `R1` exists to name. |
| `out_pinnable_b0ae.txt` | **Re-takeable, its input *is* repo state, and still declined.** `bash code/state_relocation_audit_b0ae/run_all.sh` ran to exit 0 in 25 s and moved `out_b8_findability.txt`, whose `B8.2` is *"about the repo as it stands"* by declaration. Its value is a function of `HEAD`, and `HEAD` moves under the refinery's rebase **after the last moment anything on this branch can run**. |
| `out_worklist.txt` | **Re-taken by the suite on this branch, and it did not move.** `mg-3ebf` edited `worklist.py` at `AS_OF` and did not move this transcript, whose last commit is tranche 10's `0cb0fa4` — so the rule flags it, `CODE`, correctly. It is also on `run_all.sh` and pinned at `07a2fd0`, and it reproduced **byte-identically**. |
| `out_worklist_rerun.txt` | **Not re-taken, and the reason is its input.** `worklist.py`'s `--rerun` mode is fed by `ground_truth.sh` — about 70 minutes, executing every candidate instrument and writing-then-restoring directories under `code/`, which `run_all.sh`'s own header declares as the reason it is off every build path. |

**The table refused on its own author, and that is why it has five rows and not three.** It was
written at `637b046` naming the three `out_pinnable_*` transcripts. Re-pinning `AS_OF` to `9d6bbfa`
on the rebase made the scan flag two rows the table did not name, and section 5 of the transcript
**exited 2** rather than print a table that had stopped covering its subject. *The first revision this
arm was asked about that was not the one it was written at is the one that caught it* — which is the
strongest thing a refusal can do, and worth more than the three rows it was built for.

**`out_worklist.txt` is the demonstration that `OVERTAKEN` is not `WRONG`**, which until now this
section could only assert: a row can be flagged and be demonstrably current at the same time. Its
witness is **0**, the only signal section 4 could have given, and a zero is not evidence of anything.

The first row is still the finding. `out_pinnable_3b51.txt` is not stale-and-refreshable; it is a record of
a state the repository **no longer has**, because the instrument's own recommendation was adopted.
A rule that reported it as work to do would be sending its reader to a run that refuses.

### The `a4ef` row is measured by construction, not argued

On a clean checkout the `a4ef` suite's `out_s1_extent.txt` declines **6** entries. Creating **three
empty directories** by hand —

```
code/species_7d75/__pycache__   code/species_repair_6f61/__pycache__   code/species_remainder_f8fa/__pycache__
```

— makes that transcript **byte-identical to the committed one** at **9**. So this suite has *no*
repository-caused drift at `AS_OF`: the entire drift `out_pinnable_a4ef.txt` classifies is three
directories that exist because somebody once ran three other suites in the same worktree. Re-taking
the page would publish one operator's execution history in place of another's.

**This confirms a sentence this README already carried and never demonstrated.** Tranche 9's
annotation says `species_repair_a4ef` *"is `mg-4020`'s R1 instance and is **not pinnable at all**"* —
which is true, and the reason is now a construction rather than a reading: no `AS_OF` can reach a
directory git is configured never to track, so there is nothing for a pin to fix. The record was
right; what it did not have is the three-directory experiment.

### What all three agree on, and no committed transcript says

**Every committed `pinnable` transcript in this directory describes a TWO-RULE instrument.**
`pinnable.py` has had **three** since tranche 6 (`mg-e5f3` added `R3`). Both re-takes that *could* be
taken print `THIS INSTRUMENT ANSWERS ITS OWN THREE RULES` and a whole `R3 UNORDERED WALKS` section —
**26 diff lines each, measured**. Section 4 of `out_overtaken.txt` sees that from the **source alone**,
without running anything, and those two files are the ground truth it was checked against.

## 2. One file names the class, so the instrument answers about the class

`out_pinnable_3b51.txt` is one member of a property nothing measures: **a committed transcript whose
producer has moved since the transcript was written.** `mg-f771`'s `g0` sees a watched transcript
*move*; it cannot see one that never gets the chance. `mg-ede8`'s `liveindex.py` asks whether a
figure was already wrong at its own commit, and `mg-bdc0`'s `pathlist.py` then measured that method
free on **0 of 840**. This is the neighbouring question and it is cheaper than either: not *is this
figure wrong*, but **has the thing that computes it moved since**.

`overtaken.py` ships in `run_all.sh` — `exemplars.py`'s reason exactly, and **not** `pinnable.py`'s or
`pathlist.py`'s: it executes no instrument code and needs no dirty tree, so its transcript reproduces
byte-identically and costs about 3 s.

```
 3265  tracked path(s) at AS_OF 9d6bbfa
 1125  committed transcript(s) under code/
  855  paired to a producer by pathlist.py's convention — IMPORTED, not re-spelled
  270  transcript(s) that convention does NOT reach
   30  recovered by the trailing-segment widening
   29  adjudicated TRUE by hand;  1 adjudicated FALSE
  884  pairs examined
   32  OVERTAKEN — the producer's source at AS_OF differs from its source at
        the commit that last wrote the transcript
    6  ARCHIVAL BY NAME — preserved on purpose
   26  LIVE:  23 where the producer's CODE moved,  3 PROSE-ONLY
```

## 3. The strict rule cannot see the file this arm was filed from

`out_pinnable_3b51.txt` is `pinnable.py` **with an argument**, so `pinnable_3b51.py` does not exist
and the pair is in `pathlist.py`'s **270 unreached** rather than in its 855. **The widening is not an
enhancement — it is the difference between answering the ticket and reporting a number about somebody
else.** It strips trailing `_`-separated segments until a producer of that name exists in the same
directory, and its 30 candidates are adjudicated in a **hand table the arm refuses over** if it is
incomplete or names a pair the matcher did not find.

**One of the 30 is false, and it is excluded by the table and not by the matcher.**
`code/state_suppression_repair_5f7c/out_run_all_a74f_PRE5f7c.txt` is paired to that directory's own
`run_all.sh`; its README says in so many words that it is
`code/state_delegation_repair_a74f/out_run_all.txt` **as it stood before this repair** — a *foreign*
directory's transcript, copied in. No rule over basenames can read a sentence. `P53` asserts that the
matcher **still produces** that candidate, because a matcher tightened until its output is clean
proves nothing.

## 4. Two directions that are not the same direction, and both are printed

`OVERTAKEN` is a proof **about the producer** and not about the transcript, and the two ways of
over-reading it are separated on the page rather than in a sentence.

- **`PROSE-ONLY` is a column, not a filter.** A producer whose docstring grew cannot print anything
  different. That it is only **3 of 26** is the measurement; a page that dropped them silently would
  publish the same **23** with no way to check it. The split is `pinnable.code_only`'s, **imported**,
  so this arm cannot disagree with `permuted.py` section 4 about what prose is.
- **`ARCHIVAL BY NAME` is `OVERTAKEN` by design and is not a finding.** This estate preserves
  transcripts of a past state on purpose — `_PREREPAIR`, `_FIRSTFORM`, `_FIRSTRUN`, `_before` — and
  those go `OVERTAKEN` the moment the repair they precede lands. `P55` measures the marker in **both**
  directions, and the halves that matter are the negative ones: `out_pinnable_3b51.txt` and
  `out_a1_vacuity_n7.txt` carry a trailing segment that is an **argument**, and a marker wide enough
  to eat those would make `26` an artifact of the marker.

## 5. The witness — the only half of *"is it actually stale"* that costs nothing

For each `OVERTAKEN` row with a Python producer: how many long single-line string literals exist in
the producer at `AS_OF`, did **not** exist at the transcript's own commit, and do **not** appear
anywhere in the committed transcript. **19 of 32** are positive.

**It is a witness and not a proof, in both directions, and that is stated at the section.** A regex, a
dict key and an unreachable branch's message all count, so a positive **over**-states; and a zero is
not evidence of freshness, because a producer can change what it prints without adding a literal at
all. `P56` asserts the half that makes it a witness rather than a count of edits: a new literal that
is **already in the transcript** must contribute nothing.

**And a positive witness does not mean re-takeable.** `out_pinnable_3b51.txt` scores 34 and cannot be
re-taken at any revision. Both facts are on the page.

## 6. What this tranche leaves — reported at the low water mark

`N35` joins `KNOWN_DEFECT` and **nothing leaves** (12 → 13), and it is `N31`'s limit arriving on a
different rule. **`NOT OVERTAKEN` proves nothing at all**: a transcript goes stale when its **corpus**
moves and its producer does not, which is exactly how `out_consumers.txt` has shipped stale at its own
commit in 5 of its 8 versions, and no rule here can see one of those. The direction is what makes the
published figure safe — every error of this kind makes `OVERTAKEN` look **smaller** — so **32 of 884
is a low water mark**.

**The 240 still outside the pairing after the widening are counted, not dropped.** They are the
convention's residue, and a census that reports a number because it never looked is this directory's
oldest named defect.

**This file is outside its own population, by arithmetic and not by rule**, and section 6 of the
transcript says so rather than leaving it to be found: `AS_OF` is older than `overtaken.py`, so
`out_overtaken.txt` is not tracked at the commit it reports on and cannot appear in the 884. Graded
by hand it is **not** `OVERTAKEN` and cannot become so — it is in `run_all.sh`, which is the whole
difference between this page and the five in section 1.

**Its own witness is a whole-output membership test — `mg-9876` section 1's smell — and it is kept.**
Found with `a4_sweep.py`'s *own* detector run over this branch's files rather than by eye: exactly one
site, `if v not in text` in `grade()`. It is not harmless (a literal that appears in the transcript
for an unrelated reason suppresses a real witness), there is no line-structured alternative that is
correct because a literal is printed *inside* a longer line, and its error direction is the one
already declared — the witness **under**-states. Renaming the variable so the detector misses it,
with the semantics unchanged, is precisely what a census that gates teaches its subjects to do.

**Reflexively, `R3` fires on `overtaken.py` zero times** — checked by running
`pinnable.unordered_walks` over it rather than by reading — and this branch adds **zero** planted
needles to `selftest_20ee.py`'s 19.

### `out_consumers.txt` does **not** move, which has not happened for six tranches

Four of the last six tranches found this figure already wrong at its own commit, and every one of the
last five committed a refresh. **This branch commits none, because there is nothing to refresh:**
`9d6bbfa` holds **209** files named `run_all.sh` and the transcript `mg-3ebf` committed there says
**209**. This branch adds **zero** `run_all.sh`, so `liveindex.py` is silent and the re-run reproduces
byte-identically.

That is a fact about the **timing of this rebase** and not a repair: the property `mg-ede8` measured
is unchanged, and this branch's own `209` will be wrong the moment a `run_all.sh` lands on main
before it merges. **It moved 205 → 209 on the pre-rebase tree** — all four main's, attributed by
diffing the `run_all.sh` list at both commits — and `mg-3ebf`'s landing took exactly that refresh
between the two runs. The figure a branch publishes here is a function of *when the refinery
scheduled it*, which is the arc's own finding arriving as a piece of luck rather than as a defect.

### The `a4` census moves `222` → `223` in `77` → `78`, and the delta is **mine**

Attributed by running `a4_sweep.py` **with and without** this branch's new file rather than by eye
(`mg-c15e`'s method). The whole delta is `asof_census_20ee:1` — the membership site declared above —
and `220 → 222` in `76 → 77`, plus the population `232 → 239` directories, is main's own movement
whose census refresh main did not take. The `| tee` count stands still at **30**, `NEITHER, though the
directory ships code` stands still at **27**, and `ships a file named for negative/self/positive-control`
does not move: `overtaken.py` is not such a name and this directory already qualifies through
`selftest_20ee.py`.

`out_gate.txt`'s audit byte count moves `55076` → `55096` beside the twin's **unchanged** `11818`,
and the `+20` is attributed by measurement rather than assumed: `a4_sweep.py`'s own output is
**16045** bytes without this branch's file and **16065** with it, the same twenty. `./build.sh` was
run on the rebased tree and `g0` graded the four moved transcripts itself (`mg-4020`) — `2 NOISE`
(`alias_agreement`'s two, wall-clock only), `1 CORPUS` (`out_a4_sweep.txt`, with `g0` printing
*"Restore it rather than committing it — the refresh is owed by whoever trips the bound, not by this
branch"*, an instruction followed rather than second-guessed) and **`1 DISAGREES`**, `out_gate.txt`,
which this branch commits. Nothing in `code/asof_census_20ee/` appears in that list at all: **all ten
of its transcripts reproduce byte-identically on the rebased tree**, `out_consumers.txt` included.

`STATE.md` is untouched so the ratchet is untouched and no twin re-pin is owed; `docs/FACTS.md` gets
**no** entry (`mg-3da1`'s homelessness test — every measurement here is consumed by this landing) and
`docs/CONCEPTS.md` no row. This directory is **not** in `build.sh` and this tranche does not put it
there: nothing here is a property the estate must hold, and a measurement that gates is one its
subjects learn to spell around — the first thing they would spell around being the pairing
convention, which is only worth having while nobody is scored on it.

**Nothing in the 26 live rows is repaired.** Each belongs to the directory that wrote it, twenty-one
of them are somebody else's — the other five are this directory's own and are section 1's table — and
a refresh here would move twenty-one committed transcripts for a measurement nobody asked to be
binding.

### `pathlist.py` had **no tranche section and no mention at all**, and the claim I wrote about it was refuted mid-rebase

`mg-bdc0` landed a whole instrument — `pathlist.py`, five controls, `N33`, its own transcript — with
**no tranche section**, and at `9d6bbfa` `mg-bdc0` was named **zero** times in this file — this
section is the first, which is the same self-refuting shape as the `pathlist` count below and is
said here rather than left to be caught. So this
heading is *tranche 14* because 13 is the last number this file used, **not** because it is the
fourteenth landing: the numbering is hand-typed and nothing checks it.

**This paragraph was written at `637b046` saying `grep -c pathlist` returned 0, and by the time the
branch rebased it was 2 — so it is corrected rather than defended.** `mg-3ebf`'s tranche 13 landed
while this branch was open and mentions `pathlist.py` twice, both times **in passing, in sentences
about something else**: *"`pathlist.py`'s declared shape: an exemption nobody wrote"* and a line
listing transcripts that did not move.

That makes the point sharper rather than weaker, and it is `N29` exactly. `exemplars.py`'s rule is
that *a record's newest mention of an instrument is its last word about it*; `pathlist.py` now has a
last word, and **neither sentence accounts for anything `mg-bdc0` did**. A younger sentence **may**
be an accounting and need not be one — which is what `N29` asserts and what these two sentences are
the smallest available instance of. The zero itself was `N30`'s shape (*an instrument no record
mentions has no last word and is invisible to the rule at every revision*) arriving inside the
directory that issued `N30`, and it was true for every one of the 8 commits between
`pathlist.py`'s landing at `d94de4f` and this branch's rebase.

Reported and not repaired beyond this: writing `mg-bdc0`'s tranche section is `mg-bdc0`'s to write,
and a section invented by somebody who did not do the work is a record of nothing.
>>>>>>> 8b7c5bb (measure: THE TICKET'S FIRST ITEM WAS DISCHARGED FOUR TRANCHES AGO AND ITS LAST ITEM CANNOT BE DONE AT ALL — the transcript this arc was filed about is not stale-and-refreshable, it is a record of a state the repository no longer has, because the pin it recommended WORKED.  AND THE INSTRUMENT THIS TRANCHE BUILT REFUSED ON ITS OWN AUTHOR DURING THE REBASE, WHICH IS THE BEST THING IN THE BRANCH.  mg-6b2d carries mg-44da's remainder and names N25 first — R3's find half requires a following SPACE, so the LIST spelling is invisible.  mg-23af TOOK IT: `N25 find(1) in the LIST spelling — WAS INVISIBLE, NOW SEEN` is green, N25 has LEFT KNOWN_DEFECT, and N27 took its place carrying the under-count the repair left.  Item 2 is pinnable.code_only's own declared limit, still 1 of the 80 hits at 12aa5f8, unchanged in kind.  SO THE WORK IS ITEM 3, AND IT TURNED OUT NOT TO BE A REFRESH.  ALL THREE out_pinnable_*.txt WERE RE-TAKEN BY HAND AND EACH FAILED FOR A DIFFERENT REASON, NONE OF WHICH IS `NOBODY GOT ROUND TO IT`.  (1) out_pinnable_3b51.txt CANNOT BE RE-TAKEN AT ANY REVISION: `sh code/landscape_repair_audit_3b51/run_all.sh` ran to exit 0 in 63 s and left `git status` EMPTY, so pinnable.py refused with `is EMPTY, and this instrument classifies a drift it is given rather than one it produces` — tranche 4's pin removed the drift, and the instrument's own recommendation destroyed its subject.  (2) out_pinnable_a4ef.txt is re-takeable and ITS INPUT IS NOT REPO STATE, MEASURED BY CONSTRUCTION RATHER THAN ARGUED: on a clean checkout the a4ef suite declines 6 entries, and creating THREE EMPTY DIRECTORIES by hand — code/species_7d75/__pycache__, code/species_repair_6f61/__pycache__, code/species_remainder_f8fa/__pycache__ — makes its transcript BYTE-IDENTICAL to the committed one at 9.  That suite has NO repository-caused drift at AS_OF and re-taking the page would publish one operator's execution history in place of another's; it also turns this README's own sentence `species_repair_a4ef is not pinnable at all` from a reading into a construction, no AS_OF being able to reach a directory git will never track.  (3) out_pinnable_b0ae.txt is re-takeable, its input IS repo state (B8.2 is `about the repo as it stands` BY DECLARATION) and is STILL DECLINED, because its value is a function of HEAD and HEAD moves under the refinery's rebase after the last moment anything on this branch can run.  ALL THREE AGREE ON ONE THING NO COMMITTED TRANSCRIPT SAYS: every committed pinnable transcript here describes a TWO-RULE instrument, pinnable.py has had THREE since tranche 6, and both re-takes that COULD be taken print a whole `R3 UNORDERED WALKS` section — 26 diff lines each, measured.  ONE FILE NAMES THE CLASS, SO THE INSTRUMENT ANSWERS ABOUT THE CLASS.  overtaken.py asks whether a committed transcript's PRODUCER has moved since the transcript was written — not `is this figure wrong` (mg-ede8's question, free on 0 of 840 by mg-bdc0's own measurement) but `has the thing that computes it moved since`.  It needs NO instrument execution and NO dirty tree, one `git log --name-only` walk and two `git show` per candidate, so out_overtaken.txt reproduces BYTE-IDENTICALLY and it IS in run_all.sh, which is exemplars.py's reason and NOT pinnable.py's.  THE FUNNEL, EVERY LOSS COUNTED WHERE IT HAPPENS, at AS_OF 9d6bbfa: 3265 tracked, 1125 transcripts under code/, 855 paired by pathlist.pairs_at IMPORTED AND NOT RE-SPELLED, 270 unreached, 30 recovered by a trailing-segment widening, 29 adjudicated TRUE BY HAND, 884 examined, 32 OVERTAKEN — 6 ARCHIVAL BY DESIGN and 26 LIVE, of which 23 CODE and 3 PROSE-ONLY.  THE STRICT RULE CANNOT SEE THE FILE THIS ARM WAS FILED FROM, which is the funnel's own subject arriving in it: out_pinnable_3b51.txt is `pinnable.py` WITH AN ARGUMENT, so pinnable_3b51.py does not exist and the pair sits in pathlist.py's 270 rather than its 855 — the widening is the difference between answering the ticket and reporting a number about somebody else.  ONE OF THE 30 IS FALSE AND IS EXCLUDED BY THE TABLE, NOT BY THE MATCHER: out_run_all_a74f_PRE5f7c.txt is code/state_delegation_repair_a74f/out_run_all.txt copied in before a repair — its own README says so IN A SENTENCE, and no rule over basenames can read a sentence — so P53 asserts that the matcher STILL PRODUCES that candidate, a matcher tightened until its output is clean proving nothing.  THE HAND TABLE REFUSED ON ITS OWN AUTHOR AND THAT IS WHY IT HAS FIVE ROWS AND NOT THREE.  It was written at 637b046 naming the three out_pinnable_*; the rebase onto mg-3ebf's landing re-pinned AS_OF to 9d6bbfa, and mg-3ebf EDITS worklist.py WITHOUT MOVING out_worklist.txt — so the scan flagged two rows the table did not name and section 5 EXITED 2 rather than print a table that had stopped covering its subject.  The first revision this arm was asked about that was not the one it was written at is the one that caught it.  AND ONE OF THE TWO IS THE DEMONSTRATION THIS SECTION COULD PREVIOUSLY ONLY ASSERT: out_worklist.txt is OVERTAKEN, CODE, correctly — and it is on run_all.sh, pinned at 07a2fd0, and REPRODUCES BYTE-IDENTICALLY, so a row can be flagged and demonstrably current at once.  Its witness is 0, the only signal section 4 could have given, and a zero is evidence of nothing.  The other, out_worklist_rerun.txt, is a fourth transcript nothing re-takes and its reason is neither a pin nor a dirty tree: its input is ground_truth.sh, ~70 minutes, which run_all.sh's own header declares as why it is off every build path.  TWO WAYS OF OVER-READING THE 32 ARE SEPARATED ON THE PAGE RATHER THAN IN A SENTENCE.  PROSE-ONLY is a COLUMN and not a filter — a docstring that grew cannot change what a producer prints, it is 3 of 26, and the split is pinnable.code_only's IMPORTED so this arm cannot disagree with permuted.py section 4 about what prose is.  ARCHIVAL BY NAME is OVERTAKEN BY DESIGN and is not a finding — _PREREPAIR, _FIRSTFORM, _FIRSTRUN, _before — and P55 measures the marker in BOTH directions, the halves that matter being the NEGATIVE ones: out_pinnable_3b51.txt and out_a1_vacuity_n7.txt carry a trailing segment that is an ARGUMENT, and a marker wide enough to eat those would make 26 an artifact of the marker.  THE WITNESS IS THE ONLY HALF OF `IS IT ACTUALLY STALE` THAT COSTS NOTHING and it is a WITNESS IN BOTH DIRECTIONS, said at the section: 19 of 32 rows have at least one long string literal that is new in the producer and absent from the transcript, a regex and an unreachable branch's message both count so a positive OVER-states, and a ZERO is not evidence of freshness at all.  ITS GROUND TRUTH IS THE TWO RE-TAKES: it scores 60 on a4ef and b0ae and both really do move.  AND A POSITIVE WITNESS DOES NOT MEAN RE-TAKEABLE — 3b51 scores 34 and cannot be re-taken at any revision, which is on the page.  SEVEN CONTROLS, SUITE GREEN AT 87 (80 -> 87, 47 positive and 32 negative), every one firing overtaken.grade ITSELF on a planted pair rather than a re-statement of it (P34's discipline three instruments along), and P51 runs FIRST because the headline is a SMALL NUMBER and a narrowed pairing, a widening that recovered nothing or a comparison that can no longer see a difference each publish a smaller one for free.  N35 JOINS KNOWN_DEFECT (12 -> 13) AND NOTHING LEAVES: NOT OVERTAKEN PROVES NOTHING AT ALL — a transcript goes stale when its CORPUS moves and its producer does not, which is the exact shape out_consumers.txt has shipped in 5 of its 8 versions, and the control PLANTS it and requires the wrong answer.  Its DIRECTION is what makes the figure safe: every error of this kind makes OVERTAKEN look SMALLER, so 32 of 884 is a LOW WATER MARK.  RENUMBERED ON LANDING AND THE MAP IS PRINTED — THE THIRD SUCH COLLISION IN FOUR LANDINGS IN THIS ONE NAMESPACE.  This branch issued P45-P50 and N34 and headed its section tranche 13; mg-3ebf's foreign.py landed THOSE SAME SEVEN NAMES and that same number while this branch sat in the merge queue, and a number in this directory is NEVER REISSUED (that is what BURNED is for and P25 enforces it) — so this tranche's seven became P51, P52, P53, P54, P55, P56 and N35, in that order, and the heading became tranche 14.  NOT ONE WORD OF THE ARGUMENT MOVED.  mg-5058 recorded the first collision and mg-bdc0 the second; three in four landings is a fact about the NAMESPACE and not about any branch.  THREE DEFECTS OF MY OWN ARE DECLARED RATHER THAN TIDIED.  (1) THIS FILE IS OUTSIDE ITS OWN POPULATION BY ARITHMETIC AND NOT BY RULE — AS_OF is older than overtaken.py, so out_overtaken.txt is not tracked at the commit it reports on; graded by hand it is NOT OVERTAKEN and cannot become so, being in run_all.sh, which is the whole difference between this page and the five in section 5.  (2) ITS OWN WITNESS IS A WHOLE-OUTPUT MEMBERSHIP TEST — mg-9876 section 1's smell — FOUND WITH a4_sweep.py's OWN DETECTOR OVER THIS FILE RATHER THAN BY EYE: exactly one site, `if v not in text` in grade().  IT IS KEPT, and not because it is harmless: a literal appearing in the transcript for an unrelated reason SUPPRESSES a real witness.  There is no line-structured alternative that is correct, a literal being printed INSIDE a longer line; the error direction is the one already declared; and renaming the variable to miss the detector with the semantics unchanged is exactly what a census that gates teaches its subjects to do.  (3) MY OWN CLAIM ABOUT pathlist.py WAS REFUTED MID-REBASE AND IS CORRECTED RATHER THAN DEFENDED: this section was written at 637b046 saying `grep -c pathlist README.md` returned 0 — N30's shape inside the directory that ISSUED N30, mg-bdc0 having landed a whole instrument with no tranche section — and mg-3ebf's landing made it 2, both times IN PASSING in sentences about something else.  That is N29 exactly: a younger sentence MAY be an accounting and need not be, and neither of those two accounts for anything mg-bdc0 did.  THE CENSUS IS ATTRIBUTED BY RUNNING a4 BOTH WITH AND WITHOUT THIS DIRECTORY'S NEW FILE rather than by eye (mg-c15e's method), and RE-TAKEN AFTER THE REBASE: 222 -> 223 candidate sites in 77 -> 78 directories and THE WHOLE DELTA IS `asof_census_20ee:1`, mine; the 220 -> 222 in 76 -> 77 and the population 232 -> 239 directories are main's own landings whose refresh main did not take.  The `| tee` count stands still at 30, `NEITHER, though the directory ships code` stands still at 27, `ships a file named for negative/self/positive-control` does not move, and R3 fires on overtaken.py ZERO times with ZERO new planted needles in selftest_20ee.py's 19.  out_gate.txt's audit byte count moves 55076 -> 55096 beside the twin's UNCHANGED 11818, and the +20 is MEASURED: a4_sweep.py's own output is 16045 bytes without this file and 16065 with it, the same twenty.  out_consumers.txt DOES NOT MOVE, WHICH HAS NOT HAPPENED FOR SIX TRANCHES: 9d6bbfa holds 209 run_all.sh and the transcript mg-3ebf committed there says 209, this branch adds zero, and liveindex.py prints `the committed transcript agrees with this tree on every path-list-valued figure`.  THAT IS A FACT ABOUT THE TIMING OF THIS REBASE AND NOT A REPAIR — it moved 205 -> 209 on the PRE-rebase tree, all four main's and attributed by diffing the run_all.sh list at both commits, and mg-3ebf took exactly that refresh between the two runs.  ALL TEN of this directory's transcripts reproduce BYTE-IDENTICALLY on the rebased tree.  ./build.sh RAN and g0 graded the four moved transcripts ITSELF rather than by eye (mg-4020): 2 NOISE restored, 1 CORPUS restored on g0's own printed instruction, and 1 DISAGREES — out_gate.txt — committed.  A SENTENCE OF main's WAS REPAIRED IN PASSING AND IS DECLARED: selftest_20ee.py's GREEN summary enumerates the instruments its controls cover and named neither foreign.py nor overtaken.py, so both clauses are added.  THE CONFLICTED TRANSCRIPT WAS RESOLVED BY RE-RUNNING ITS PRODUCER AND NOT BY HAND (mg-54b1): out_selftest_20ee.txt came out of the rebase carrying FOUR conflict markers that `git add -A` would have committed, and regenerating it removed them.  STATE.md untouched so the ratchet is untouched and no twin re-pin is owed, docs/FACTS.md gets NO entry (mg-3da1's homelessness test) and docs/CONCEPTS.md no row, and this directory is still NOT in build.sh — a measurement that gates is one its subjects learn to spell around, and the first thing they would spell around is the pairing convention (mg-6b2d))
