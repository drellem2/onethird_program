# The `c1_branching.py` parser: are the findings real, and does the reproduction stand?

**`mg-58da`.** Instrument: `code/branching_audit_58da/`. Target of the enquiry:
`code/branching_audit_a218/c1_branching.py` and the 24 findings it raised on a
re-run, reported by `mg-d330` (`f9f8220`).

> **These are two questions with two different answers and they are answered
> separately below. Neither verdict covers the other.**

---

## 0. The bottom line, derived from the rows below and not asserted

| | question | answer | where it is measured |
|---|---|---|---|
| **B** | does the 198-cell reproduction still stand? | **YES, at `286d5030902d`** — re-run there, **198 cells, 0 disagreements, exit 0, byte-identical to the committed record**. And **redone at HEAD**, where it comes out **stronger**: the 24 cells that were cardinalities are now **labelled sets** | `g1`, `g2` |
| **A** | are the 24 findings real? | **NO — 24 of 24 are PARSER ARTIFACTS. 0 CONFIRMED, 0 UNKNOWN.** The target states the datum at every one of the 24 cells, in a strictly richer form, and it **agrees** | `g3` |
| | are the **174 non-findings** real? | **YES** — 7 of 7 corruption probes on those channels fire. Their `0 disagreements` is a measurement, not a silence | `g3` |
| | does the **set-level** property hold? | **4 of 5.** `c3_withdrawal.py` is red and stays **OPEN** — mg-d330's second finding, not this ticket's | `g4` |
| | anything new? | **yes, one:** mg-d330's `e4` gate on the exit-code sentence is a **presence test** and cannot see a marker beside it. Found by making this ticket's own correction. Booked, **not** worked around | `g4 (vii)` |

---

## 1. QUESTION B — provenance. Settled by re-running, which is cheap.

`c1_branching.py` reads **exactly one** external file. That is not assumed; it
is read out of the script's source — the script contains exactly one `open()`:

```
txt = open(TARGET_OUT).read()      #  ../branching_locate_db09/out_t1_tl.txt
```

Everything else it prints, it measures.

| part of the reproduction | `286d5030` → `d1dd84d2` |
|---|---|
| `c1_branching.py` | **unchanged** — `sha256 bddeb6c4f57f70cb…` at both |
| `kern_a218.py` (the measuring half) | **unchanged** — `sha256 70356cbca847bc20…` at both |
| `out_t1_tl.txt` (the one file it reads) | **changed by `ed9cde4`**, and by nothing else |

**The re-run at `286d5030902d`:**

```
SELF-ERRORS 0   FINDINGS 0   TOTAL BAD 0   exit 0
  vertex counts           24 cells compared
  vertex dimensions       53 cells compared
  edge multiplicities    121 cells compared
  TOTAL CELLS            198
```

and it is **byte-identical** to the `out_c1_branching.txt` committed at that
revision (`sha256 671349aa9c70d350…` both sides).

> **Re-stated with the revision named, which is what a reproduction needs:**
>
> **At `286d5030902d`, mg-a218's `c1_branching.py` — a third instrument sharing
> no code with the two it audits — measured the branching graph of `TL_n(β)` for
> `β ∈ {3,2,1,0}` and `1 ≤ n ≤ 6` and agreed with mg-e8b8's committed
> `out_t1_tl.txt` in all 198 cells.**

### Did the measurement move, or only the comparison?

`c1`'s output has three parts: **(i)** its own vertex sets, **(ii)** its own edge
table, **(iii)** the comparison against the target. Parts (i) and (ii) read
nothing outside the instrument. Run against the old target and against the new
one, they are **byte-identical — 125 lines, `sha256 a8db5dbd4c758765…` both
ways.** No mathematics moved. The whole question is about **reading**.

### And it needed redoing, because `ed9cde4` did touch the read path

`mg-13b2` replaced `T1b2 (i)`'s count table with the labelled vertex **sets** —
on `c1`'s *own* finding X1, which said the count was the defect. So the datum
did not vanish; it changed **rendering**, from 24 cardinalities to 24 labelled
sets. A cardinality is a function of a set, so **the new form determines the old
and the old does not determine the new.**

**Redone at HEAD** (`g2`), with the cells recovered by a parser sharing no line
with `c1`'s:

| | |
|---|---|
| cells recovered from the HEAD target | **24 of 24** |
| recovered **counts** agreeing with `c1`'s measurement | **24 of 24** |
| recovered **sets** agreeing with `c1`'s measurement | **24 of 24** |
| `T1b2 (ii)` — the 53 dimension and 121 edge cells — across `ed9cde4` | **identical, cell for cell** |
| **total** | **198 cells compared, 0 disagreements** |

and the recovery is **calibrated**: each of the 24 cells is corrupted in turn and
required to go red **at that cell and nowhere else** — **24 of 24 probes fire**,
and restoring the target returns all 24 to green.

**Four independent kernels, 6 of 6 pairs agreeing on all 24 cells:**
`t1_tl.py` (mg-db09, 1st), `b1_branching.py` (mg-2060, 2nd), `kern_a218.py`
(mg-a218, 3rd), `kern_d330.py` (mg-d330, 4th).

**The reproduction is not weakened by the repair. It is strengthened.** 24 cells
that could only be compared as cardinalities are now compared as labelled sets —
and 10 of the 36 same-level pairs that a count column showed as **equal** are
separated by the set column.

---

## 2. QUESTION A — the parser. The count carries no information until each is checked.

> A blind parser produces findings **and non-findings** with equal confidence.

### 2.1 The mechanism, measured rather than guessed

`c1` finds the vertex counts with one regex and compares with one expression:

```python
m = re.match(r"\s*(\d)\s+((?:\d+\s+){5}\d+)\s*$", line)
...
if tgt_counts.get(beta, [None] * 6)[n - 1] != mine_c:
    finding("vertex COUNT disagrees at beta=%d n=%d: target %s, mine %d" ...)
```

A cell the regex never filled is compared as `None`, and `None` differs from
every integer. **Absence is rendered as disagreement.**

| lines in `T1b2` matching that regex | |
|---|---|
| at `286d5030` — where the reproduction was taken | **4** (one row per parameter × 6 counts = the 24 cells) |
| at `d1dd84d2` — HEAD | **0** |

### 2.2 The 24, classified one at a time

Three boxes, filled by measurement, none by inheritance from another:

* **CONFIRMED** — the target states the datum and it disagrees with `c1`.
* **PARSER ARTIFACT** — the target states the datum, in this or a stronger form,
  and it **agrees**; the word *"disagrees"* is false and the accusation is the
  parser's.
* **UNKNOWN** — the target does not determine the datum at all.

| | |
|---|---|
| **CONFIRMED** | **0** of 24 |
| **PARSER ARTIFACT** | **24** of 24 |
| **UNKNOWN** | **0** of 24 |

Every one of the 24 names a cell where the target states the vertex set — e.g.
`β = 3, n = 6`: target `[0:1,1:5,2:9,3:5]` → 4, `c1` `[0:1,1:5,2:9,3:5]` → 4 —
and it agrees with `c1`'s own measurement **label for label**. **The target does
not disagree with `c1` anywhere.**

### 2.3 The half a count cannot answer: the **174 non-findings**

`c1` reports **0 disagreements** over 53 dimension cells and 121 edge cells on
the HEAD target. A parser blind in those channels would report the same `0` —
and the run would look *better*, not worse. So each channel was corrupted and the
**direction predicted before the probe**:

| probe | predicted | actual | fires |
|---|---|---|---|
| one digit of one **edge** cell (β=1, `[L(4,2)]` of `L(5,2) dim 1`) | RED | RED | ✅ |
| one digit of a **multiplicity-2** edge (β=1, `[L(3,0)]` of `L(4,1)`) | RED | RED | ✅ |
| one digit of one **dimension** cell (β=1, `L(6,2) dim 9 → 8`) | RED | RED | ✅ |
| **deleting** a whole `L(n,p)` row (β=1, `L(5,2) dim 1`) | RED | RED | ✅ |
| **deleting** every edge row of one parameter block (β = 0) | RED | RED | ✅ |
| **null probe** — a prose line inside `T1b2`, no figure touched | green | green | ✅ |
| **control** on the count channel **at `286d5030`, where it was live** | RED | RED | ✅ |

**7 of 7.** The 174 cells go red under a one-digit change, so their agreement is
a measurement. The 24 vertex cells go red under **nothing** — they compare
against a value that is not there — while the *same channel at the old revision*
goes red on a one-digit change, which is what a live channel looks like. **The
two are distinguished by the probes, not by the counts.**

### 2.4 The defect is real, and it is `c1`'s

Confirmed here, not re-opened: `mg-d330` booked it first.

* the blindness is booked as **FINDINGS** against the target rather than as
  **SELF-ERRORS** against the instrument;
* `c1`'s own population line then reads `vertex counts: 24 cells compared` where
  **0** were compared against any value the target states in the form it reads.

---

## 3. The repair, and its deletion test

`c1_branching.py` is widened, with the note and its reason in the source, per
this repo's convention. Three things change and each is load-bearing:

1. the **set** form is read and preferred where present — a **stronger**
   comparison than the audit originally made, not a weaker one;
2. the **count** form is still read, so a re-run at `286d5030` still compares all
   24 cells and still agrees;
3. **a cell the target does not state is a `SELF-ERROR`, not a `FINDING`.** This
   is the actual defect. A finding is a statement about the target, and *"I could
   not find it"* is not one.

**Deletion-tested in the direction that matters** — direction predicted first:

| target handed to the widened `c1` | predicted | actual | |
|---|---|---|---|
| the HEAD target (SET form) | exit 0, self 0, find 0, **24 compared**, form SET | as predicted | ✅ |
| the `286d5030` target (COUNT form) — backward compatibility | exit 0, self 0, find 0, **24 compared**, form COUNT | as predicted | ✅ |
| the HEAD target with all 24 set rows **deleted** | exit 1, **self 24, find 0**, 0 compared, form NEITHER | as predicted | ✅ |

and the move is shown, on the *same* blinded input:

```
c1 @ 286d5030 (unrepaired) :  SELF  0   FINDINGS 24   exit 1
c1 widened                 :  SELF 24   FINDINGS  0   exit 1
```

**The committed `out_c1_branching.txt` is not regenerated** — a committed audit
output is the record of what that audit found, not a live gate (the call
`mg-a318` made for `mg-8a5c`, and `mg-13b2` for `c2`). `g1` re-runs the script at
`286d5030` and confirms that file **byte for byte**, so the record is *checkable*
rather than merely preserved.

`§10` of `OneThird-Bratteli-Path-Algebras-Mge8b8Repair-IndependentAudit.md` is
corrected in place: its present-tense *"`c2`, `c4` and `c5` exit `1`"* is struck
and replaced by a table of all three revisions. It was `mg-d330`'s F9, and this
ticket's own change moves it again — leaving it would be the same defect one
commit later.

---

## 4. The set-level property — the grain this whole item is about

> **Widening one member of a mutually-corroborating set is not a local edit,
> because the corroboration was the point.**

**The five are** `c1_branching.py`, `c2_vertexsets.py`, `c3_withdrawal.py`,
`c4_seam.py`, `c5_record.py`. Not among them, and named so: `selftest_a218.py`
(tests the kernel, not the target, and prints no `TOTAL BAD`), `c0_repro.sh` (a
reproduction harness that re-runs the *target's* instrument), `kern_a218.py` (the
kernel the five share).

| | touched | |
|---|---|---|
| `ed9cde4` (mg-13b2) | **1 of 5** | `c2_vertexsets.py` |
| `mg-58da` (this ticket) | **1 of 5** | `c1_branching.py` |
| `kern_a218.py` | **0** | unchanged by both — no mathematics moved at any point |

**This is the shape of the failure.** `ed9cde4` widened `c2` because a re-run
would otherwise have scored its own repair as `c2`'s `SELF-ERROR`. `c1` had the
same stale parser reading the same rewritten block and was not widened with it.
One member was made to tell the truth on a re-run and its sibling was left
telling a falsehood — and the falsehood was **louder**, because `c1` books its
blindness as findings against the target.

### The five, at three revisions

| script | committed @ `286d5030` | after `ed9cde4` | after `mg-58da` |
|---|---|---|---|
| `c1_branching.py` | 0/0 exit **0** | 0/24 exit **1** | 0/0 exit **0** |
| `c2_vertexsets.py` | 0/1 exit **1** | 0/0 exit **0** | 0/0 exit **0** |
| `c3_withdrawal.py` | 0/0 exit **0** | 0/1 exit **1** | 0/1 exit **1** |
| `c4_seam.py` | 0/1 exit **1** | 0/0 exit **0** | 0/0 exit **0** |
| `c5_record.py` | 0/1 exit **1** | 0/0 exit **0** | 0/0 exit **0** |

### WHAT HOLDS

* the members that measure the vertex cells still **agree with each other**:
  `c1` vs `c2`, **24 of 24**;
* and with every instrument in the tree: `out_t1_tl.txt` (1st), `c1` live (3rd),
  `out_e1_vertexsets.txt` (4th), `out_b1_branching.txt` (2nd) — **24 of 24**,
  **6 of 6 pairs**;
* `c0_repro.sh` still regenerates the target's five committed outputs — **5 of
  5 IDENTICAL**, exit 0;
* **4 of the five are green.**

### WHAT DOES NOT — stated, not worked around

**`c3_withdrawal.py` exits 1**, and it is **OPEN**. Its finding is `mg-d330`'s
second: `mg-13b2`'s own new `t5_labels.py` and its committed output carry the
withdrawn phrases as **search needles** with no marker beside them, and `c3`
sweeps for exactly those phrases. It is a real finding against the repaired tree.
Nothing here touches it. `g4` books it as a **FINDING and exits 1** — because
the set-level property is that *all five* are green, and saying otherwise would
be the defect this ticket exists to name.

### A NEW FINDING, produced by making this ticket's own correction

**`mg-d330`'s `e4_rerun.py` gate on the exit-code sentence is a PRESENCE TEST.**
Quoted from its source:

```python
CLAIM = "`c2`, `c4` and `c5` exit `1`"
if CLAIM in adoc:  ... finding(...)
else:              selferr("could not locate ...")
```

It has exactly two states — **PRESENT** and **ABSENT** — and no state for
**PRESENT AND MARKED**. Evaluated on three variants, direction predicted first:

| variant of the document | predicted | e4's gate says | |
|---|---|---|---|
| as this ticket leaves it — sentence **struck**, correction table beside it | finding | finding | ✅ |
| the same, with the sentence **deleted outright** | self-error | self-error | ✅ |
| a hypothetical **unstruck** restatement | finding | finding | ✅ |

So a sentence struck in place with a correction beside it is
**indistinguishable** from one left standing, and `e4`'s finding text — which
says the sentence was *"left unchanged and unmarked"* — is now **false of the
tree** while its exit code is unchanged.

**NOT REPAIRED HERE, and the reason is this ticket in miniature.** The sentence
could be rewritten to make the substring vanish and `e4` would go green. That
would satisfy the gate without informing the reader and leave the gate exactly as
blind as it is. Marking in place is right for the reader; `e4`'s inability to see
the marker is a finding **against `e4`**, and it is booked as one rather than
worked around. `e4` is `mg-d330`'s committed instrument and is not this ticket's
to edit.

This is the same shape as `mg-8a5c`/`mg-a318` — *"the gate is a presence
test"* — one instrument over.

### The general point

**A change to one instrument in a corroborating set cannot be checked by running
that instrument**, because a parser that has been made to agree with a target
agrees with it. It is checked by running the **other** members and the **other**
instruments against the same cells, and by making the changed member **fail** on
an input it genuinely cannot read.

That is the grain: a property that lives **between** the instruments rather than
inside any one of them, and it is the fourth flavour of the same failure this
arc has now produced — after scope, extent and granularity.

---

## 5. NOT CLAIMED

That `c3_withdrawal.py`'s finding is closed, or examined beyond re-running it and
reading its output; that anything in the target's mathematics is wrong or right
beyond the 198 cells named; that a fifth Temperley–Lieb kernel was built (it was
not, deliberately — see the instrument's README); that the corruption batteries
are exhaustive over all 198 cells (they are exhaustive over the 24 vertex cells,
and are 7 named probes on the other 174); that `mg-d330`'s other findings were
re-derived; that any search here was exhaustive.

## 6. REPRODUCE

```
cd code/branching_audit_58da && ./run_all.sh    # ~1 min, pure Python 3, NO NETWORK
```

Committed outputs: `out_selftest_58da.txt`, `out_g1_provenance.txt`,
`out_g2_redo.txt`, `out_g3_findings.txt`, `out_g4_fleet.txt`.

**Exit codes are the finding channel.** Every `g*.py` exits `0` iff
`SELF-ERRORS == 0` **and** `FINDINGS == 0`. **`g4` exits `1`, and it was
predicted to** — `c3` is red. `PREDICTIONS.md` holds the exit code *and the
substantive answer* predicted for each script before it was run, with the one
miss kept as written: I predicted my own probe labels would be right, and three
of them named `β = 0` for rows sitting in the `β = 1` block. Every probe still
fired. A probe that fires with a wrong label is a bookkeeping error; a probe that
does not fire is a dead channel.

Nothing in this instrument writes into `code/branching_audit_a218/` or
`code/branching_locate_db09/`.
