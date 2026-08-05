# mg-0120 — the auditor's own record was partly a constant

`code/state_delegation_audit_16eb/claims16eb.py` is named **"THE CLAIMS mg-0049 ADDED,
CHECKED"**. Six of the seventeen rows it prints carried the verdict as a **literal**. A
constant returns the same answer on every tree it is ever run against: it reported the same
thing before mg-a74f's repair, after it, and would report the same thing on an empty
repository. For those six rows the quantity computed was not a measurement, whatever the row
was called.

All six are now computed, and **every one of them has been shown returning both answers**.

---

## The headline, in one table

| | |
|---|---|
| constants on the printed path | **6 of 17**, not 4 — two were the literal **`True`** |
| verdicts now computed | **17 of 17** (a seventh literal remains at line 72 and is *meant* to — it is a guard branch) |
| proven capable of both answers | **6 of 6** — 4 by history, 6 by construction, and the harness rejects a pinned stand-in |
| the arc's published cardinality | **six** |
| the same program at `bd24efc` with every verdict computed | **SEVEN** |
| the anchor `739f7bd` | **DISPLACED by a rebase, not lost** — identical `patch-id` to `cfd2af5`, which is on `main` |
| anchors repository-wide, against `main` | 373 tokens: **256 LIVE, 57 DISPLACED, 0 STALE, 0 DEAD** |

---

## 1. THE POPULATION IS SIX, NOT FOUR — and the difference is where the finding is

The ticket names four literal `False`s at lines 94, 142, 194, 217. Read with `ast`, the file
has **16 `claim()` call sites** and prints **17 rows**, and **seven sites** pass a constant:

| site | literal | on the printed path? |
|---|---|---|
| `:72` | `False` | **no** — guard branch, fires only if the sentence it is about has been deleted |
| `:94` | `False` | yes |
| `:142` | `False` | yes |
| `:156` | **`True`** | yes |
| `:178` | **`True`** | yes |
| `:194` | `False` | yes |
| `:217` | `False` | yes |

Over the population of **17 printed rows**, **6 are constants**. The guard at `:72` is not
counted as a defect and is not touched: it runs only when its sentence has been deleted, which
makes it a deliberate alarm, and mg-65eb marked the difference.

**Why the two extra rows matter more than the four the ticket names.** Recomputed at
`bd24efc`, all four literal `False`s come out **BROKEN**. They were pinned to the answer a
measurement would have given, so they cost the arc nothing. A literal **`True`** is a
different animal: it is a row that **cannot report a problem**, and it sits inside the
numerator of the file's own headline count. §4 is where that bill comes due.

---

## 2. WHAT EACH ROW COMPUTES NOW

| row | the sentence | how it is computed | at `HEAD` |
|---|---|---|---|
| `:94` | the two tables cannot drift apart quietly in **either** direction | three drifts **constructed** and run through `delta_control.py` as it stands, plus a **no-op control on every call** | **holds** |
| `:142` | exit 1 is "a region … NO LONGER PRESENTED TO A READER" | the bullet is **located** first; where it is asserted, both directions are refuted by construction on two GFM renderers | **RESPECIFIED** |
| `:156` | presentation.py: "NOTHING CHANGED EXCEPT ONE MESSAGE AND FOUR SELF-TEST CASES" | the **commit range** `db2b77d..5594c69`, docstrings stripped from both sides, at the grain of an executable statement | **BROKEN** |
| `:178` | COVERAGE.md's R1/R2 table: exit 0 against mg-bee1, exit 1 against mg-0049 | the claimed pair **read out of the table**, the observed pair **read out of mg-5644's own re-run transcript**, joined row by row | **holds** |
| `:194` | both batteries "re-run in section 7 of run_all.sh" | the section is **resolved by its COMMAND**, never by its title | **holds** |
| `:217` | R5: `<details>` at the top **SUPPRESSES NOTHING** | R5 is **located** first; where asserted, the two conjuncts (bytes on the page / reader reached) are measured **separately** | **RESPECIFIED** |

**`14 hold · 1 BROKEN · 2 RESPECIFIED`, summing to 17.**

**The third state is not a hedge.** Two rows quote a sentence mg-a74f then rewrote. Such a row
has not become true — it has become **moot**. Reporting it `holds` would put a green row in
the numerator for a measurement nobody took, which is the defect this ticket is about, one
level up. `claim()` now takes `None` and the summary prints three states that sum to the
population.

**The one BROKEN row is the one that was pinned `True`.** `presentation.py`'s header says
nothing changed except one message and four self-test cases. Two live statements in
`region_record` are neither:

```
+ region_record   _d, _content = strip_quotes(doc.lines[first])
+ region_record   opens_on_heading = doc.state[first] == RENDERED and _d == 0 and (_ATX.match(...))
```

The old row justified its `True` with a fact about a **different property** — that the eleven
certified presentation digests are byte-identical to `db2b77d`'s. That fact is true. It is not
this sentence. Both are now printed on the row, so a reader can see the two apart.

---

## 3. THE FLIP HARNESS — because a computation nobody has seen move is still not a check

`flip_0120.py`. **A control nobody has seen fail is not evidence**, and an expression that
returns `False` today is indistinguishable from the literal `False` it replaced until someone
has seen it return something else.

**Tier 1 — history.** Each verdict evaluated at `bd24efc` and at the working tree. **4 of 6
move on two real trees nobody built for this purpose**, so there is nothing of mine in them:

| row | `bd24efc` | working tree | |
|---|---|---|---|
| `:94` | BROKEN | holds | **moved** |
| `:142` | BROKEN | RESPECIFIED | **moved** |
| `:156` | BROKEN | BROKEN | same |
| `:178` | holds | holds | same |
| `:194` | BROKEN | holds | **moved** |
| `:217` | BROKEN | RESPECIFIED | **moved** |

**Tier 2 — construction.** Each row is also handed an input built to reach a value history
does not produce, and **the value being reached for is declared before the run**, so the
transcript says REACHED or MISSED instead of printing a number and leaving the reader to work
out whether it was the one being aimed at. **6 of 6 REACHED.** Two of them reach `holds` for
rows that no revision of this repository makes hold — `:142` with E1 neutralised and
`<details open>`, and `:217` with `<details open>` — which is the only way to show those two
can report a pass at all.

**The harness's own control.** Two stand-ins, one pinned to the literal `False` and one to the
literal `True` — the exact shape this repair removed — are put through the identical Tier-1
path. Both must come back **NOT PROVEN CAPABLE OF BOTH ANSWERS**, and `flip_0120.py` exits
non-zero on itself if either does not.

**Read strictly:** a row is PROVEN only if **both `holds` and `BROKEN`** have been observed.
`RESPECIFIED` does not substitute for either. **6 of 6 PROVEN.**

---

## 4. THE QUESTION THE TICKET EXISTS FOR — and the answer is not the reassuring one

> *"Then find out whether any conclusion in the arc rests on those four rows — that is the
> question this ticket exists for, and it is not answered by fixing the file."*

**Yes. The conclusion is the cardinality SIX**, and `rests0120.py` measures it over every
tracked `.py`/`.md`/`.sh` at `main` (917 files; grain: a file, counted once): **15 files
publish the figure, 8 of them instruments or accounts of this arc.** The number is what
mg-a74f's commit subject, its README table, `claims_a74f.py`'s own banner, and mg-65eb's
`six65eb.py` — *a program named after it* — are all built on.

**IT DOES NOT SURVIVE.** The repaired `claims16eb.py`, copied into a throwaway worktree at
`bd24efc` with every other row left exactly as mg-16eb wrote it and **run**:

```
PUBLISHED  (mg-16eb's own committed out_claims.txt)   6 BROKEN of 17
RE-DERIVED (every verdict computed)                   7 BROKEN of 17     DISAGREE
BROKEN here and not there:  presentation.py:24
```

**The seventh row is one of the two that were pinned `True`.** The four literal `False`s cost
this arc nothing. The literal `True` cost it a finding, and it went unnoticed for two audits
because **a row pinned `True` cannot report a problem** and every downstream check of the
*number* passed.

**What this does NOT establish**, and it is the part worth being careful about: that any
conclusion of mg-a74f or mg-65eb is *wrong*. A repair classified by six rows is not refuted by
a seventh — it is **incomplete**. The seventh row's claim (`presentation.py`'s header) is
still false on the repaired tree and **no one has repaired it**, this repair included. It is
left open in §7 rather than fixed here, because fixing it means editing the sentence of a
control this ticket does not scope.

---

## 5. THE ANCHOR — displaced, not lost, and the two look identical

mg-65eb: `739f7bd`, carrying mg-a74f's own integrity claim, is not an ancestor of `main`,
while `git cat-file -e` — the idiom mg-a74f's own code is written in — passes it.

The ticket asks the right question: **is it unreachable, or merely SHA-displaced by a
rebase?** `git merge-base --is-ancestor` gives exit 1 either way. They are told apart by the
**diff**:

```
git patch-id --stable  739f7bd  ->  17a7bca3c7be2fc4f9ab736294b06230a11c5cc0
git patch-id --stable  cfd2af5  ->  17a7bca3c7be2fc4f9ab736294b06230a11c5cc0   IDENTICAL
trees    fd6b2f46e401  vs  1dbf04714ec2      differ
parents  bd24efc9fdb3  vs  b469d6791aaf      differ   — which is what a rebase IS
cfd2af5 is an ancestor of main                          yes
```

**DISPLACED.** The property was never violated; the pointer rotted. `mg-a74f/README.md` is
re-pointed at `cfd2af5`, and **the sentence that carried the anchor is corrected too** — it
said *"a sha, not `HEAD~n`, so a rebase cannot quietly move it"*, and a rebase quietly moved
it. A sha is immune to **renumbering**, which is what `HEAD~n` suffers; it is not immune to
**displacement**. The sentence claimed the second immunity and had earned only the first.

**The twin rule's own control (§C of `anchors0120.py`).** `anchor65eb.py:twin_of` finds the
twin by matching the commit **subject**. A subject is a label somebody typed. Rather than
argue that it could collide, this repair **constructs the collision** in a throwaway
repository: a real predictions commit on a branch, an impostor with the same formulaic subject
and different content, both landed on `main` with the impostor nearer the tip.

```
the SUBJECT rule (anchor65eb.py:twin_of) picks   e67fa3f   THE IMPOSTOR — the wrong commit
the PATCH-ID rule (this file) picks              f26d42f   the rebased twin
```

The section **exits non-zero unless patch-id is right AND subject is wrong**, so it cannot
print a green line it has not earned. It exited non-zero twice while being built.

**The population re-measured, against `main` rather than `HEAD`.** mg-65eb measured 24 tokens
over the four directories mg-a74f touches — a neighbourhood, which cannot answer "how common
is this". Over **every tracked `.py`/`.md`/`.sh`/`.txt` in the repository (1404 files)**:

| bucket | distinct tokens | occurrences |
|---|---|---|
| ANCHOR-LIVE | 256 | 5212 |
| **ANCHOR-DISPLACED** | **57** | **390** |
| ANCHOR-STALE | 0 | 0 |
| ANCHOR-DEAD | 0 | 0 |
| NOT-A-REVISION | 60 | 138 |

Two grains, both printed, because they are different numbers: a token named 60 times is one
row in the first column and 60 in the second.

**`739f7bd` is not a mistake anybody made.** 57 anchors in this repository are displaced by
exactly the same mechanism: every arc pre-registers predictions on a polecat branch, names
that branch's sha in its own prose, and is then rebased by the refinery. **0 are STALE and 0
are DEAD** — nothing is lost, and the alarm level for "pointer rotted" is not the alarm level
for "evidence gone". `anchors0120.py` therefore fails on STALE and DEAD and **counts**
DISPLACED without failing on it; that is a judgement, it is argued in the file's header, and a
reader may reasonably want the opposite policy.

mg-65eb's own figure **reproduces exactly** at `main` today: 26 files, 24 distinct tokens, 139
occurrences, 23 LIVE and 1 not — the one it called STALE and this file calls DISPLACED,
because this file has a bucket for the distinction and that one is the whole point.

---

## 6. THE PREDICTIONS, SCORED — including the ones I lost

`PREDICTIONS.md` was committed **before any script of this repair existed**, in its own commit
whose diff contains nothing but that file. **Six predictions missed.**

### Disclosures (measurements already taken; recorded as such, never scored as predictions)

| | |
|---|---|
| **D-1** the constant population is 6 of 17, not 4 | stands |
| **D-2** "nothing runs it" is true of mg-a74f's directory and false of the repository (2 files run it) | stands |
| **D-3** `739f7bd` is displaced, identical patch-id to `cfd2af5` | stands |
| **D-4** `anchor65eb.py` matches the twin on the SUBJECT | stands, and §5 constructs the case that breaks it |

### Scored

| | prediction | outcome |
|---|---|---|
| **P-1a** | all 6 computable | ✔ 6 of 6 |
| **P-1b `:94`** | holds | ✔ |
| **P-1b `:142`** | neither holds nor BROKEN — the sentence is gone | ✔ **exactly**, and it is the prediction I was least sure of |
| **P-1b `:156`** | holds | ✘ **MISS — it is BROKEN**, and it is the largest finding in this repair |
| **P-1b `:178`** | holds | ✔ |
| **P-1b `:194`** | BROKEN — "mg-a74f did not touch mg-0049's README pointer" | ✘ **MISS** — mg-a74f corrected both rows to section 8 |
| **P-1b `:217`** | BROKEN — "the sentence is still in `render0049.py` verbatim" | ✘ **MISS** — mg-a74f narrowed R5 too; it is RESPECIFIED |
| **P-1c** | ≥1 row in the third state | ✔ 2 |
| **P-2a** | 6 of 6 flip | ✔ |
| **P-2b** | ≥1 construction fails first time; `:156` named as the hardest | ✘ **MISS on the row named.** `:156`'s construction worked first time. **The prediction's substance held** — C3 (`:94`) missed its target and is on the record — but I named the wrong row and that is a miss, not a hit |
| **P-2c** | the harness rejects a pinned verdict, 1 of 1 | ✔ **2 of 2** — pinned `False` *and* pinned `True` |
| **P-3** | 2 of 6 rows need renderers; UNPROBED without them | ✔ `:142` and `:217` |
| **P-4a** | yes, and the load-bearing thing is the number six | ✔ |
| **P-4b** | ≥3 distinct files assert the figure | ✔ 15 files, 8 of them this arc's own |
| **P-4c** | **the number six SURVIVES** | ✘ **MISS, and the most consequential one.** It is **seven**. I flagged this as the prediction I could easily lose and said losing it would be "a much larger finding". It was, and it is |
| **P-5a** | mg-65eb's 23/1 reproduces at `main` | ✔ exactly — 26 files, 24 tokens, 139 occurrences |
| **P-5b** | ≥5 stale anchors repository-wide | ✔ **on substance, with the label corrected**: 57 tokens are not ancestors of `main`. **0** of them are STALE by this file's rule, because all 57 have patch-id twins and are DISPLACED. The prediction's number is comfortably beaten and its *bucket name* was wrong, which is the finding |
| **P-5c** | 0 are DEAD | ✔ 0 |
| **P-5d** | ≥4 of the not-ancestors have a patch-id twin | ✔ **57 of 57** |
| **P-6a** | ≥1 defect in my own repaired instrument, found by my own harness | ✔ **four** — §7 |
| **P-6b** | `out_claims.txt` stops reproducing; kept rather than deleted | ✔ — kept as `out_claims_PRE0120.txt` |
| **P-6c** | I will NOT wire `claims16eb.py` into mg-a74f's `run_all.sh` | ✔ — I did not, for the reason given |

**Six misses.** Three of them (`:156`, `:194`, `:217`) are the same mistake made three times:
**I predicted from mg-16eb's transcript instead of from mg-a74f's diff**, and mg-a74f had
already corrected or narrowed more than I credited it with. The fourth (P-4c) is the one the
ticket cares about.

---

## 7. DEFECTS OF THIS REPAIR, FOUND BY THIS REPAIR

Four, all found by controls written for the purpose, all kept on the record.

1. **A crash was being scored as a catch.** `v3`'s first mutation machinery re-emitted the
   whole `DELEGATED_PRESENTATION` table from a span that began at the `{` rather than at the
   name, so every mutated control lost `DELEGATED_PRESENTATION = ` and died of `NameError`
   before reaching a single check. **All three constructions scored `caught` and none of them
   ran a check.** `Worktree.control()` now returns stderr, a traceback is reported `CRASHED`
   and never as a catch, and a **no-op control runs on every call** — it was the no-op that
   caught this. mg-d075 recorded the same shape in its own repair; this is its second
   instance.
2. **A construction that patched a file the function then overwrote.** C3 wrote the patched
   `delta_control.py` into the worktree and called a function that read its base from the
   *working tree* and wrote it straight back. The construction reported **MISSED**, which is
   how it was found; `v3_two_tables` now takes `ctl_text`. Without the declared-target
   reporting this would have printed a plausible number and passed.
3. **A dependency check that answered the wrong question.** `renderers_present()` reported
   ABSENT on a machine with both renderers installed, because `render()` passed `-` to a
   bridge that takes a **path**. Two rows would have silently reported UNPROBED.
4. **A population-versus-grain slip inside the instrument written to find that class of
   slip.** `rests0120.py`'s first draft subtracted the six literal-carrying rows from the
   published BROKEN count, when only **four** of the six were in that count — the other two
   were pinned `True` and sat among the rows that held. It reported **5** where the answer is
   **7**. The repair is not a corrected formula; it is **running the program**.

A fifth, in the prose rather than the code: `run_all.sh`'s section-5 banner asserted that the
anchor would come out LIVE against `HEAD`. It does not — this branch descends from `main`, not
from `polecat-a74f`. The banner now states what the run actually shows and says why it was
wrong.

---

## 8. WHAT I DID NOT DO

- **I did not repair `presentation.py`'s header.** The seventh BROKEN row is a false sentence
  in a *control* this ticket does not scope, and repairing it means either editing that
  sentence or changing `region_record`. It is named, measured, and left open.
- **I did not re-classify mg-a74f's or mg-65eb's findings**, and nothing here says any of them
  is wrong. The finding is that the population they classified is **missing a member**.
- **I did not re-run mg-16eb's full suite** (§6 of `run_all.sh` prints the command instead).
  It re-runs mg-5644's and mg-218d's whole batteries and takes ~25 minutes; claiming a figure
  for a run I did not do is the defect this arc exists to catch.
- **I did not fix the other 57 displaced anchors.** They are enumerated with their twins in
  `out_anchors0120.txt`. Fixing them is mechanical and it is a different ticket, because the
  right *policy* — re-point every anchor after every merge, or write anchors that survive one
  — is a decision and not a measurement.
- **I did not add a third caller for `claims16eb.py`.** Two files already run it (D-2). A
  third would make the ticket's "nothing runs it" sentence look answered without changing
  whether anyone reads the answer.
- **`:142` and `:217` have never been observed returning `holds` at any revision of this
  repository.** Both reach it only under a construction built here. That is stated on the row
  rather than rounded up.
- **`v6` joins on a committed transcript rather than re-running mg-5644's battery.** The
  transcript's reproduction is `reproduce16eb.py`'s job and is not re-checked here; the row
  says so.

---

## 9. Reproducing

```sh
D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
NODE_PATH="$D/node_modules" sh code/state_claims_repair_0120/run_all.sh
```

| file | |
|---|---|
| `PREDICTIONS.md` | committed before any script of this repair existed |
| `verdicts0120.py` | the six verdicts, computed |
| `flip_0120.py` | each of the six shown returning both answers; §3 is the harness's own control |
| `rests0120.py` | what rests on the pinned rows — the cardinality, re-derived by running the program |
| `anchors0120.py` | the anchor diagnosed by content; the twin rule's control; every anchor in the repository |
| `out_*.txt` | the committed transcripts, regenerated at the commit that ships them |

**Sections 1, 3 and 4 exit 1 by design** — the flip harness fails on an unproven row, the
cardinality disagrees with what is published, and section 4 fails on STALE or DEAD anchors.
Read the exit codes before reading the findings.
