# `code/repair_8d5e/` — the instrument for mg-8d5e

Two open sites from one audit (mg-2c77, on the mg-69d1 repair `d01ff32`). Neither deferred.

| | site | what was wrong | where the repair is |
|---|---|---|---|
| **A-1** | mg-2c77, **OPEN 1** | `libe34a` derived `REPAIR_REV` as *the last commit that touched `g1_provenance.py`*. mg-69d1 touched that file to correct a **sentence**, so the anchor followed the edit and **both sides of `k1`'s pre-repair comparison became mg-76cc's already-repaired predicate** | `libe34a.py`, `k1_prerepair.py`, `selftest_e34a.py`, and every transcript of that suite |
| **A-2** | mg-2c77, **OPEN 2** | `explicit boolean operand` denotes **39** operands in the census's two files; mg-69d1's table classifies the **17** that lie inside a deciding condition; **22 are in no column**, and the unqualified phrase is what makes 17 read as complete | `kern5f9a.py`, `lib69d1.py`, `p1_bound.py`, `selftest_69d1.py`, `README.md`, `PREDICTIONS.md`, and the two documents |

## What each script does

| script | what it measures | exit |
|---|---|---|
| `selftest_8d5e.py` | 35 assertions — both operand walks, the narrow one against the **shipped** `kern5f9a.boolean_operands` **span for span**; mg-2c77's scoring rule on constructed sites including its window's edge and the hyphen case; the rule against mg-2c77's own committed table; the anchors read back out of `libe34a` | 0 |
| `r1_anchor.py` | the anchor derived / pinned / compared; **the defect reproduced** as a commit that moves the file and not the property; **three breaks built**, each red in mg-e34a's own selftest; the **second consequence in a second script** (`k4`'s commit-message scan); every revision constant `libe34a` exports, before and after, with a disposition; and a **third instance observed and not repaired** | 0 |
| `r2_kernel_half.py` | `k1_prerepair.py` **re-run unmodified**, and the **kernel-half confirmation re-derived** — the one row where the pre-repair predicate must be **silent** and the repaired one must **fire**; then **mg-2c77's own `q3` and `q4` re-run unmodified** | 0 |
| `r3_term.py` | both populations walked here and the 22 named; the scoring rule and its control; the 15 sites in files `d01ff32` touched, each with its **kind derived from its path**; every site in the tree now with a disposition; and the shipped classifier's **parsed module** unchanged | 0 |
| `r4_self.py` | this deliverable's own anchors, **perturbed**; its own counted terms scored at every site; every path it changes in a named kind | 0 |

`run_all.sh` worst exit **0**. Roughly twelve minutes on an idle machine — `r2` runs `k1` (21
pinned `g1` runs across 7 clones) and then mg-2c77's `q4`, which runs `k1` a second time.

## A-1 — the anchor

`REPAIR_REV` and `PRE_REV` are now **three things at once, and no two of them fail the same way**:

```
DERIVED FROM THE PROPERTY   first_introducing(g1_provenance.py, "kernel_source=")
PINNED                      REPAIR_REV_PIN / PRE_REV_PIN, reason beside them
COMPARED                    ANCHOR_DRIFT, gated in k1 (i) and in selftest_e34a
```

`kernel_source=` **is** mg-76cc's repair — the two-source signature that makes *this script with
that kernel* expressible, whose absence was mg-957f's F-1. A commit that edits prose in the same
file does not move it.

**A literal cannot notice that the file moved; a derivation cannot notice that it has started
measuring something else.** mg-e34a adopted derivation for the first reason and that reasoning is
not withdrawn. What is added is the second failure, and the answer to both is to keep both and
compare them.

**The derivation that re-pointed is kept and printed** as `LAST_TOUCHING_G1`, used by no anchor.
Deleting the quantity that moved would leave the next reader nothing to check the story against.

**Both history anchors had moved, and mg-2c77 named one.** `PRE_7E58_REV` was
`nth_touching(g1, 1)^` — an index into the file's history — and mg-69d1's commit pushed every
index along by one, so the column `k1` labels *before mg-7e58* held mg-76cc's parent.

**And a second script.** The same constant is `REPAIR_REV` in `k4_cancel.py`, where it selects
**which commit message** is scanned for the inverted sentence. Under the drifted anchor `k4`
scanned mg-69d1's message — which does not carry the sentence — so a copy left the count with no
number moving that a reader could see. `k4`'s own committed transcript says `4755d029 : yes`; it
now says that again.

### The confirmation, re-derived

The kernel-half confirmation is not a `0` in a verdict block. It is a **difference between two
columns** on one input:

| predicate revision | exit | self | findings |
|---|---|---|---|
| before mg-7e58 (`52aeaf43`) | 1 | 0 | 2 |
| **BEFORE THIS REPAIR** (`3bc2cf76`) | **0** | **0** | **0** — silent |
| this repair (`d01ff32` tree) | **1** | 1 | **3** — fires |

With the drifted anchor this row read `both fire`, because both columns were the same predicate —
and `both fire` is what a comparison of a thing with itself prints whatever the truth is.

## A-2 — the term

**The term is repaired, not the walk**, and the reason is stated before the measurement: mg-69d1's
narrowed bound already names *the deciding conditions* and mg-2c77 says explicitly that it is
correct. Widening `boolean_operands` would not widen the **sweep** by one operand; it would
relabel 22 while leaving the bound saying what it says.

| file | operands of every `and`/`or`, anywhere | of those, inside a deciding condition | in no column |
|---|---|---|---|
| `face_complex.py` | 35 | 15 | 20 |
| `posets.py` | 4 | 2 | 2 |
| **ALL** | **39** | **17** | **22** |

Both walks are written in `lib8d5e.py`, and the narrow one is asserted against the **shipped**
walker span for span before any subtraction rests on it.

**The scoring rule is mg-2c77's, unchanged.** It looks for the **unhyphenated** words
`deciding condition` — `q3_operands.py`'s own lines carrying `deciding-condition` were scored
UNQUALIFIED by it — so every site repaired here carries the unhyphenated words in the window as
well as the hyphenated term in its sentence. Widening the rule to accept the hyphen would have
closed the finding by moving the ruler.

### What each of the 15 got, and why — the kind is **derived from the path**

| kind | treatment | why |
|---|---|---|
| a **live claim** about what the instrument covers | **edited** to carry the qualifier | it is what a reader has |
| a **transcript** | the source line that **prints** it is edited and the script re-run **by its own runner** | a transcript is a measurement; hand-editing one falsifies it |
| a **record committed before its run** (`PREDICTIONS.md`) | an **addendum in place**, the original row standing | a later ticket does not rewrite what an earlier one predicted |

**15 → 0** in files `d01ff32` touched. **20 remain** in the tree and every one is a record —
mg-2c77's finding text and transcripts, mg-eaef's instrument and its write-up. Each states what
that audit found at the moment it ran; they are named individually in `r3 (iv)` and left standing.

**The sweep is unmoved.** The one edited file that anything executes is `kern5f9a.py`, and what
was written there is a comment: the module is parsed before and after and the two syntax trees are
compared.

## What this deliverable checked about itself

`r4` answers mg-2c77's closing instruction with measurements, not assurances:

* **11 anchors** enumerated — 3 on a property, 6 pinned-and-derived, **2 on a file's history and
  declared used by nothing**.
* All of them **perturbed**: a commit that appends a comment to every file they derive from.
  **0 moved.**
* **2 counted terms** scored at every site in this deliverable's own files. **0 bare.**
* **36 changed paths**, every one in a named kind.
* **The one edit this repair made to its own prediction file is booked**, not left to be noticed:
  one row was reworded so it carries the words the rule looks for. No predicted value was touched
  and the file says so. The rule this ticket states for other people's prediction files — an
  addendum, original standing — is the rule it applied to mg-69d1's; its own is **disclosed**
  instead, and that asymmetry is the finding-shaped part of this deliverable.

## The auditor's own instrument, re-run unmodified

`r2 (v)` runs mg-2c77's `q3_operands.py` and `q4_prerepair.py` against the repaired tree.

**`q3`'s census finding is gone** — A-2, closed and measured by the instrument that raised it.
`q3` still books its **other two** findings (the `not swept: nested` deletion sentence, and
`not determined` being unreachable by any input). Those are mg-2c77's, they are not among the two
open sites this ticket was given, and they are **named rather than counted** so that *2 remain*
cannot read as *2 unrepaired*.

**`q4` still fires, and that is a defect in the auditor, not in the repair.** Its gate is
`PRE_REV == lib76cc.REV_957F` — a comparison of **revision identity**. The property is **file
identity**: `e006581c` and the true parent of mg-76cc's repair are different commits at which
`g1_provenance.py` and `lib58da.py` are byte-identical, which is what mg-e34a's design says and
what `k1 (i)` checks and passes. `r2 (v)` prints both comparisons, and the tell is in `q4`'s own
finding text — it now reads *moved from `4755d029` … to `4755d029`*, a gate whose message says a
value moved from a revision to itself. It is mg-2c77's record and this ticket does not edit it; it
is measured and pointed at.

## What is NOT repaired here, and is pointed at

`code/repair_69d1/p3_reason.py` (i-b) runs its discriminator **against `HEAD`**, described as *the
committed tree, where the defect is still present*, and self-errors on finding 0 live assertions
there. `HEAD` moves on every commit, and mg-69d1's own repair landing is what removed the last live
assertion — so that control has been vacuous since the moment the repair it belongs to was
committed. **The same shape as A-1, in a script mg-2c77 did not name.** `r1 (vi)` runs it at the
revision before this repair began and shows it **already red there**: observed, not caused, and not
repaired, because this ticket's population is mg-2c77's two open sites.
