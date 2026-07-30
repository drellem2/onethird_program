# Independent audit of the `mg-58da` repair (`673b4c0`)

**`mg-321d`.** Instrument: `code/branching_audit_321d/`. Target of the enquiry:
`673b4c0` — `mg-58da`'s answer to the two questions `mg-d330` (`f9f8220`) left
open about `code/branching_audit_a218/c1_branching.py`, and its widening of that
script.

Pre-filed in the same action as its parent. Nothing here was written by the
author of the work it audits.

This instrument is calibrated before it is believed: `selftest_321d.py` passes
**60 assertions** over its own reader, its anchoring property in both
directions, and its report parsers for the pre- and post-repair population
wordings. And every figure below is read back out of this document, **at its
own site**, and compared against the committed run by `h5_doccheck.py`, whose
gates are deletion-tested one figure at a time.

---

## 0. The bottom line, derived from the rows below

| | what was asked | answer | where |
|---|---|---|---|
| **1** | were **A** and **B** kept separate? | **YES.** Opposite answers, different scripts, no cross-reads — and each re-derived independently here | `h1` |
| **2** | did **B**'s re-run at the old revision actually happen, with the revision named? | **YES.** Re-done here from scratch at `286d5030902d09a7eb336a4a5dec18bf7b9de64c`: **198 cells, 0 disagreements, exit 0, byte-identical** to the record committed there | `h1 (iv)` |
| **3** | does each of the **24** have a status? | **YES, 24 of 24**, and my census on my own reader matches `g3`'s **rows**, which match `g3`'s **summary**, which match the document | `h1 (v)–(vii)` |
| **4** | was the agreement across **all five** re-established, or only the changed one re-run? | **ALL FIVE WERE RE-RUN.** The five named from disk, attributed by commit, run in place; every source in the tree that states the 24 agrees with the target — **10 of 10 pairs, 24 of 24 cells**. `c3` is red and stays **OPEN**, as `mg-58da` states | `h3` |
| **5** | is the narrowing at the grain of the blindness? | **INSIDE `c1`, YES — per cell.** **IN `mg-58da`'S OWN PROVENANCE APPARATUS, NO**, at two sites, and **the repair's own commit trips both** | `h2`, `h4 (M2)` |

### FINDINGS

| | | severity |
|---|---|---|
| **G-1** | **`g1_provenance.py` exits 1 on the tree as committed**, with a finding its own section (iv) refutes. Its committed output says `FINDINGS 0` and its `PREDICTIONS.md` says `ACTUAL 0 HIT`; both were recorded before this commit existed | the grain error, site 1 |
| **G-2** | **`g4_fleet.py`'s set-level attribution is false at HEAD**: it says `ed9cde4` touched 2 of the five and this ticket touched 0. `git log` says one each. Its own **row** is right; only the **summary** drifts | the grain error, site 2 |
| **G-3** | **The documented `REPRODUCE` command does not reproduce the committed record.** `./run_all.sh` in `code/branching_audit_58da/` gives `g1` 1 finding where the committed `out_g1_provenance.txt` has 0 | consequence of G-1 |
| **M-1** | **`g1`'s byte-for-byte confirmation of the committed record never reads the file in the tree.** Corrupt it, then delete it — `g1` still prints `BYTE-IDENTICAL`. **0 of 3 probes fire** | chosen here |
| **M-2** | **The narrowing covers ABSENCE but not MISREAD.** Same six cells, two targets one line apart: `SELF 6 / FIND 0` becomes `SELF 0 / FIND 6` | chosen here |
| **S-1** | the set-level property does not hold: **4 of 5** green, `c3_withdrawal.py` open. Re-derived, **not new** — `mg-58da` books it and states it | not new |

**What is *not* found:** no defect in the mathematics, none in the 24-cell
census, none in `B`'s reproduction, and no merged verdict.

---

## 1. Were the two questions actually kept separate?

> **A** — are the 24 findings real? (about the **parser**)
> **B** — does the 198-cell reproduction stand? (about **provenance**)

A single verdict written across both — *"the instrument is sound"* — answers
neither and reads as answering both. So the check is not whether the document
*says* they are separate. Three things a merged verdict could not survive:

| | | |
|---|---|---|
| the two answers are **opposite** | B: **YES, at `286d5030902d`**; A: **NO — 24 of 24 parser artifacts** | ✅ |
| they are produced by **different programs** with independent exit codes | `g1`, `g2` answer B; `g3` answers A; each ends `sys.exit(1 if (SELF or FIND) else 0)` | ✅ |
| **neither reads the other's conclusion** | occurrences of any `out_g*.txt` inside `g1`/`g2`/`g3`: **NONE** | ✅ |

Both are then **re-derived here**, on this instrument's own reader, and both
agree. `h1` books **0 findings**.

---

## 2. QUESTION B — the re-run happened, and it is re-done here

`mg-58da` did not use the assertion form. It could not: `ed9cde4` **did** touch
the file `c1` reads, and the document says so and redoes the comparison at HEAD.
The re-run at the old revision is re-done here from scratch, independently of
`g1`:

```
c1_branching.py @ 286d5030  vs  out_t1_tl.txt @ 286d5030
   SELF-ERRORS 0   FINDINGS 0   TOTAL BAD 0   exit 0
   vertex                  24 cells compared
   vertex dimensions       53 cells compared
   edge multiplicities    121 cells compared
   TOTAL CELLS            198
```

and against the record committed at that revision:

```
re-run    sha256 671349aa9c70d350d1b8b141762b25d587af8a0821ccbcd454c662bfb4efcc34
committed sha256 671349aa9c70d350d1b8b141762b25d587af8a0821ccbcd454c662bfb4efcc34
BYTE-IDENTICAL.
```

**The revision is named in full and it resolves.** The document writes
`286d5030902d`; `git rev-parse` gives
`286d5030902d09a7eb336a4a5dec18bf7b9de64c`, which is where `mg-a218` took the
audit. Checked, not assumed.

> **B, re-stated on this instrument's own re-run:** at
> `286d5030902d09a7eb336a4a5dec18bf7b9de64c`, `mg-a218`'s `c1_branching.py`
> compared **198** cells against `mg-e8b8`'s committed `out_t1_tl.txt` and
> disagreed in **0** of them.

---

## 3. QUESTION A — all 24, and none of them silently dropped

The population is fixed at **24 first**, and every one of the 24 is accounted
for whatever its status. A residual `UNKNOWN` bucket would be honest; a
reduction of 24 to a smaller number without saying what happened to the rest
would not be.

The unrepaired `c1` raises **24** vertex-cell findings against the HEAD target.
My reader — subsection-anchored, no regex, sharing no line with `c1`'s, `c2`'s
or `lib58da`'s — finds **24 of 24** cells stated in the target's subsection (i).
Classified one at a time:

| | |
|---|---|
| **CONFIRMED** (target states it and disagrees) | **0** of 24 |
| **PARSER ARTIFACT** (target states it, in this or a stronger form, and agrees) | **24** of 24 |
| **UNKNOWN** (target does not determine it) | **0** of 24 |
| **ACCOUNTED FOR** | **24** of 24 |

And the census is checked in the direction that catches a summary drifting from
its rows:

| | |
|---|---|
| rows in `g3`'s own table carrying a class label | **24** |
| my classification vs `g3`'s **rows**, per bucket | **agree, 3 of 3** |
| `g3`'s **summary** vs `g3`'s own **rows** | **agree, 3 of 3** |
| the document's three buckets, summed | **24** |

---

## 4. The set-level property — all five, not just the changed one

**The five, named from disk rather than from a list**: the `c<digit>_*.py` that
`mg-a218`'s own `run_all.sh` runs — `c1_branching.py`, `c2_vertexsets.py`,
`c3_withdrawal.py`, `c4_seam.py`, `c5_record.py`. `g4`'s hard-coded list matches
what is on disk, so no sixth member is hiding. Not among them, and named so:
`selftest_a218.py`, `c0_repro.sh`, `kern_a218.py`.

**Attributed by commit**, over the whole directory, `286d5030..HEAD`:

| file | commits |
|---|---|
| `c1_branching.py` | **`673b4c00`** (this ticket) |
| `c2_vertexsets.py` | **`ed9cde49`** (`mg-13b2`) |
| `c3_withdrawal.py`, `c4_seam.py`, `c5_record.py` | untouched |
| `kern_a218.py`, `run_all.sh`, `selftest_a218.py`, `c0_repro.sh` | untouched |

**All five re-run in place — 5 of 5**, stdout captured in this instrument and
never redirected into a committed output:

| script | committed @`286d5030` | live at HEAD |
|---|---|---|
| `c1_branching.py` | 0/0 exit 0 | 0/0 exit **0** |
| `c2_vertexsets.py` | 0/1 exit 1 | 0/0 exit **0** |
| `c3_withdrawal.py` | 0/0 exit 0 | 0/1 exit **1** |
| `c4_seam.py` | 0/1 exit 1 | 0/0 exit **0** |
| `c5_record.py` | 0/1 exit 1 | 0/0 exit **0** |

### And the figures — measured, not assumed, including which members carry any

*"Do the figures agree across all of them"* presupposes that all of them state
figures. **2 of the five do** (`c1`, `c2`); **3 state none** (`c3`, `c4`, `c5`
are text and record checks over prose and git history). For those three the
question is **vacuous**, and it is reported as vacuous rather than as agreement.

Every source in the tree that states the 24, read here by this instrument:

| source | cells | vs target |
|---|---|---|
| the target `out_t1_tl.txt` (`mg-e8b8`, 1st) | 24/24 | 24/24 |
| `c1_branching.py` live (`mg-a218`, 3rd) | 24/24 | 24/24 |
| `c2_vertexsets.py` live (`mg-a218`, 3rd) | 24/24 | 24/24 |
| `out_b1_branching.txt` (`mg-2060`, 2nd) | 24/24 | 24/24 |
| `out_e1_vertexsets.txt` (`mg-d330`, 4th) | 24/24 | 24/24 |

**10 of 10 pairs agree at all 24 cells.**

`c0_repro.sh` on a scratch copy of the tree regenerates the target's committed
outputs: **5 of 5 IDENTICAL**, exit 0.

**The corroboration was restored, and it was restored at the right level.** Not
"the changed one runs": the other four were run too, and four independent
kernels plus the target agree cell for cell. `c3_withdrawal.py` is red and
**OPEN** — `mg-d330`'s second finding, which `mg-58da` books and does not work
around. Re-derived here; not closed here either.

---

## 5. THE GRAIN ERROR IS INSIDE THE FIX — and the fix's own commit trips it

Inside `c1`, the narrowing **is** at the grain of the blindness: the blind unit
is a **cell**, and the `SELF-ERROR` branch is per cell. Deleting the six
`beta = 2` set rows produces exactly six self-errors and touches no other cell.
That part is right.

`mg-58da`'s **provenance apparatus** is not. Two sites, one root: a provenance
question answered at the grain of a **container** — a file, and *"whatever is
not yet committed"* — rather than at the grain of the thing asked about: a
**measurement**, and a **commit**.

### G-1 — `g1` asks "did the measuring half change" and measures a file sha

The two grains give **opposite answers**:

| | |
|---|---|
| **file grain**: `c1_branching.py` `286d5030 → HEAD` | `bddeb6c4f57f70cb… → 8bacc19be4d85a57…` **CHANGED** |
| **file grain**: `kern_a218.py` — the file `g1` itself labels *"the measuring half"* | `70356cbca847bc20…` **SAME** |
| **measurement grain**: both script revisions, **the same target** | sections (i)+(ii) **byte-identical**, 125 lines, `sha256 a8db5dbd4c758765…` |
| **measurement grain**: `c1`'s own 24 vertex sets, both revisions | **all 24 equal** |

`g1` books the file difference as

> `FINDING: code/branching_audit_a218/c1_branching.py changed between 286d5030 and HEAD; the measuring half of the reproduction is not the same code`

and **exits 1**. The document's own §1 — *"Did the measurement move, or only the
comparison?"* — is the argument that this grain is wrong, and `g1`'s own section
(iv) is the check that measures at the right grain. The repair edited the
comparing half only. **The instrument that certifies the provenance of the
repair is tripped by the repair.**

### G-3 — so the documented reproduce command does not reproduce

`out_g1_provenance.txt` as committed reads `FINDINGS: 0 / TOTAL BAD: 0`, and
`PREDICTIONS.md` records `P2  g1_provenance.py  ACTUAL 0  HIT`. Both were taken
while the change was still uncommitted. Run `./run_all.sh` on the tree as
delivered and `g1` gives `FINDINGS 1`, exit 1. The prediction was honestly made
and honestly recorded; it stopped being true when the commit landed.

### G-2 — `g4` attributes by "is it committed yet"

```python
if sha@286d5030 != sha@HEAD:      touched_13b2.append(f)
if sha@HEAD     != sha@worktree:  touched_58da.append(f)
```

True for exactly as long as the change is uncommitted. On the tree as
committed, `g4` prints

```
of the five, touched by ed9cde4 (mg-13b2) : 2 -- c1_branching.py, c2_vertexsets.py
of the five, touched by mg-58da           : 0 -- none
```

**`ed9cde4` never touched `c1_branching.py`** — `git show --name-only ed9cde4`
lists `c2_vertexsets.py` and nothing else in that directory. The verdict
paragraph in `g4 (vii)` repeats it, and the column header is the hard-coded
literal `d1dd84d2 -> working` while the column is computed from `HEAD`.

**BELIEVE THE ROWS.** `g4`'s own row is right — it prints
`c1_branching.py  CHANGED (673b4c00)`, from `git log`. Only the summary drifts.
This is the same shape `mg-8aae` found one instrument over, and it lands on
**the exact question this audit's ticket asks**: *name the five, confirm which
were touched*. The set-level instrument answers it falsely on the tree it ships.

Both are cheap to close and neither is closed here: `g1` should compare the
**measurement** (it already computes it, in section (iv)) or scope the file sha
to `kern_a218.py`; `g4` should attribute with `commits_touching`, which it
already calls for the row it prints beside the summary.

---

## 6. The two things this audit chose — floor, not scope

Neither is named by any list in the ticket. Both are picked because they are the
arc's own shape one level in. Both are deletion-tested, with a null probe beside
them and the direction predicted first.

### M-1 — the record check certifies a blob against itself

The document's §3 says the committed `out_c1_branching.txt` is *"checkable
rather than merely preserved"*, because `g1` re-runs the script at `286d5030`
and confirms the file byte for byte. What `g1` compares is:

```python
out_old, rc_old = L.run_c1(old_target, script_rev=L.REV_A218)
committed = L.git_show(L.REV_A218, L.A218_DIR + "/out_c1_branching.txt")
```

**Both sides are objects in git at `286d5030`.** Neither opens the file sitting
in the tree today. Deletion-tested on three trees:

| tree handed to `g1` | predicted | `g1`'s record check |
|---|---|---|
| unmodified (**null probe** — must not fire) | `BYTE-IDENTICAL` | `BYTE-IDENTICAL` ✅ |
| record's own `TOTAL BAD: 0 → 99` **on disk** | `BYTE-IDENTICAL` | `BYTE-IDENTICAL` ✅ |
| record **deleted from the worktree entirely** | `BYTE-IDENTICAL` | `BYTE-IDENTICAL` ✅ |

**0 of 3 fire**, and the null probe is among them, so the check is not merely
insensitive — it is looking somewhere else. What is checkable is git's copy;
preservation of the reader's copy is exactly what is not checked. The worktree
copy is in fact identical today (`sha256 671349aa9c70d350…`), so this is a
**blindness**, not a wrong answer. It is the `mg-a318` shape — *the gate does
not read the figure at the site* — one instrument over.

### M-2 — the narrowing covers ABSENCE but not MISREAD

The repair adds a third branch: a cell the target **does not state** is a
`SELF-ERROR`. Correct, and per cell. It adds nothing for a cell the parser
**mis-reads**. The count regex is unchanged and anchored to nothing:

```python
m = re.match(r"\s*(\d)\s+((?:\d+\s+){5}\d+)\s*$", line)
```

Seven integers, first field one digit, anywhere in `T1b2`, first match wins.
`mg-58da`'s **own** `lib58da.py` records the problem, in the docstring of the
reader it wrote to avoid it — *"which is what `c1` does and is why `c1`'s parser
can be fooled by an unrelated row of digits"*. Noticed, avoided in the new
reader, not fixed in the old one and not booked.

The **repaired** `c1`, four targets, directions predicted first:

| target | predicted `self/find/exit` | actual | |
|---|---|---|---|
| HEAD target untouched (**null probe**) | `0/0/0` | `0/0/0` | ✅ |
| `beta=2` SET rows deleted — **ABSENT** | `6/0/1` | `6/0/1` | ✅ |
| the same **plus one stray 7-integer row** — **MISREAD** | `0/6/1` | `0/6/1` | ✅ |
| stray row alone, SET rows intact — SET wins | `0/0/0` | `0/0/0` | ✅ |

**4 of 4.** One line apart, the same six cells move from the `SELF-ERROR`
channel to the `FINDING` channel:

```
FINDING: vertex COUNT disagrees at beta=2 n=1: target 9, mine 1
FINDING: vertex COUNT disagrees at beta=2 n=2: target 9, mine 2
FINDING: vertex COUNT disagrees at beta=2 n=3: target 9, mine 2
vertex cells: 24 cells compared, 0 not compared because this script could not read them
```

— the instrument accusing the target of stating counts it never stated, and its
population line reporting 24 compared. **That is `mg-d330`'s finding, in the
branch the repair kept.** The distinction the repair draws is *present /
absent*; the distinction that matters is *"the target said this" / "I decided
this"*. Not in the document's `NOT CLAIMED`.

---

## 7. This instrument made the same error, on its first run

`h3`'s reader for `mg-2060`'s `out_b1_branching.txt` matched only
`--- beta = b ---`; `mg-2060` writes `beta=3:`. It recovered **0 of 24** cells
and the cross-instrument comparison booked **four findings** against an
instrument that agrees with the target at 24 of 24. **Absence rendered as
disagreement, inside the instrument auditing that exact defect.**

Recorded in `h3_setlevel.py`'s source, in `PREDICTIONS.md` and in the README,
and fixed in **two** places: the pattern accepts both forms, and a source the
script cannot read is booked as a `SELF-ERROR` and **excluded from the compared
population**. The second half is the one that matters — the control-flow fix,
not the careful-reading fix — and it is the same call `mg-58da` made inside
`c1`. `h3` now prints *"sources this script could read: 5 of 5"* beside the pair
count, so a blind reader shows as a shrinking population, not as findings.

---

## 8. NOT CLAIMED

That `c3_withdrawal.py`'s finding is closed, or examined beyond re-running it;
that `G-1`, `G-2`, `G-3`, `M-1` or `M-2` are repaired here — none is, and
`code/branching_audit_58da/` and `code/branching_audit_a218/` are not written to
by this instrument; that the mathematics was re-derived (no fifth kernel was
built, deliberately — five sources already agree at 24 of 24); that `mg-d330`'s
or `mg-58da`'s other findings were re-derived; that the corruption batteries are
exhaustive (they are 3 named probes on `M-1`, 4 on `M-2`, and the 24-cell census
is exhaustive over the 24); that any search here was exhaustive.

## 9. REPRODUCE

```
cd code/branching_audit_321d && ./run_all.sh    # ~3 min, pure Python 3, NO NETWORK
```

**Exit codes are the finding channel.** Every `h*.py` exits `0` iff
`SELF-ERRORS == 0` **and** `FINDINGS == 0`. `h2`, `h3` and `h4` exit `1` and
were predicted to. `PREDICTIONS.md` holds the exit code *and* the substantive
answer predicted for each script before it was run, with the misses kept as
written — I predicted two findings from `h2` and it books three.

**And this document is gated by `h5_doccheck.py`**, which reads every published
figure **out of the line that asserts it** — refusing on an anchor that matches
zero lines or more than one — and compares it against the committed output of
the script that measured it. Each gate is deletion-tested by corrupting that
figure alone at its own site: **16 of 16 fire**, with a null probe that changes
an unrelated word and stays green. Two figures were un-gateable as first
written; the document was changed to make them gateable rather than the gate
loosened to fit the prose.

Committed outputs: `out_selftest_321d.txt`, `out_h1_questions.txt`,
`out_h2_grain.txt`, `out_h3_setlevel.txt`, `out_h4_mine.txt`,
`out_h5_doccheck.txt`.
