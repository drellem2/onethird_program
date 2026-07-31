# Landing mg-c4c8: the third rung is removed, and the declaration is computed

> **SUPERSEDED IN ONE PLACE by mg-f7e1 (2026-07-31), and only in one.** Everything about the
> DERIVED DECLARATION below stands and was confirmed by mg-0b07 against a patch changed in two
> directions. What does not stand is section 1's conclusion: `[len(row) for row in A] !=
> [len(row) for row in B]` has no boolean operator — that count is exact — but it is still a
> DISJUNCTION, and its ORDER half could be taken out with the width half standing for
> byte-identical, exit 0. The `or` is back, both halves are swept, and the instrument's bound is
> now a count printed beside its results. Full record:
> `docs/landing-mg-0b07-implicit-disjunction.md`.

**Item:** mg-64b6. **Closes:** mg-c4c8's OPEN 1 and OPEN 2.
**Code:** `code/face_geometry/face_complex.py`, `code/face_geometry/controls.py`,
instrument in `code/face_geometry_instr_5f9a/` (`run_all.sh`, 83 claims, 0 BROKEN).

mg-c4c8 booked the mg-9220 repair as real: the deletion test **is** per return,
`absorb_trace`'s six returns are visible 6 of 6 under individual deletion, the inert
return is removed rather than annotated, and the control still exits 1. None of that is
re-opened here. What it left open is two things, and they are one thing:

**The grain error recurred one level finer. The two returns became two CLAUSES of one
condition, and deleting the first clause alone moved not one byte. And the DECLARED UNIT
— the mechanism mg-9220 introduced to make grain self-describing — understated its own
patch on 8 of 11.**

---

## 1. OPEN 1 — the rung is removed rather than descended

mg-9220 merged the two `shape` returns into

```python
if m != len(B) or any(len(A[i]) != len(B[i]) for i in range(m)):
    return Trace(False, "shape", 0)
```

Two clauses. mg-c4c8 deleted the first alone: **byte-identical, exit 0, every row green** —
mg-e7bc's sentence with `return` replaced by `clause`. Gate → return → clause is three rungs
of one regress, and the ticket's instruction was to fix the clause and **stop chasing rungs**.

**The two clauses were saying one thing.** `absorb_trace` now says it once:

```python
if [len(row) for row in A] != [len(row) for row in B]:
    return Trace(False, "shape", 0)
```

There is **no boolean operator**, so there is no clause under that `return` for a fourth
rung to bite on. That is not an argument — `d2_deletion.py` reads the clause population out
of the syntax tree and counts **0 deciding clauses in `absorb_trace`**; a boolean operator
returning to any of its conditions makes that claim red and gives the sweep below a row with
no registered prediction, which is also red.

### The deletion test now runs at clause granularity, over an enumerated population

Section **PER CLAUSE**. Every top-level clause of every boolean condition that decides a
`return` in `face_complex.py` — read from the tree, not listed — deleted **alone**, with the
rest of its condition and its statement left standing, and the whole battery run:

| function | clause | artifact | exit |
|---|---|---|---|
| `gate_violations` guard | 1, 2 | BYTE-IDENTICAL | 0 |
| `diagonal_moves` guard | 1, 2 | BYTE-IDENTICAL | 0 |
| `Poset.leq` value | 1, 2 | BYTE-IDENTICAL | 0 |
| `Poset.comparable` value | 1, 2, 3 | BYTE-IDENTICAL | 0 |

**9 of 9 predictions matched**, and every one of the nine was run by mg-c4c8's H2 on the
tree this commit starts from — said in the transcript rather than presented as foresight.
`posets.py` carries **2 more** deciding clauses (`_is_transitively_closed`); they are outside
the predicate layer this deletion test mutates, they are **named** in the transcript, and no
claim here covers them.

### And the sweep is shown going red on the real defect

A sweep in which nothing is ever red is a sweep nobody has tested, and after this commit no
clause deletion in the predicate layer moves anything. So the same sweep runs against
**`b6bc2ef`** — mg-9220's own commit, the last one whose `absorb_trace` has a two-clause
`shape` condition, checked by walking the history rather than asserted:

| clause | artifact | exit |
|---|---|---|
| 1 — `m != len(B)` | **BYTE-IDENTICAL, 23,684** | 0 |
| 2 — `any(len(A[i]) != len(B[i]) …)` | **CHANGED → 24,887** | 1 |

**mg-c4c8's F1, reproduced rather than quoted**, and the sweep's positive control at once:
the firing path is the real defect on the real tree that had it, not a corruption built to
make a check fire.

### The clause was not deleted, because it was not inert

mg-c4c8 measured the clause moving **1,608 decisions** when cut from the live condition — inert
as a battery input, load-bearing as a predicate. So "remove the statement that does nothing",
which is what mg-9220 did one rung up, is **not** available here. What is available is saying
the same thing without an operand, and that is what is measured:

**Over 28,900 pairs across 85 shape profiles the merged two-clause form and this form agree on
the OUTCOME — decision, gate label and raised exception — on 28,900 of 28,900.** Not "the same
decision": the same answer by all three channels. The population is indexed by **shape profile**
(every row-width tuple of length 0..3, widths 0..3, filled two ways) because shape is what the
condition reads — mg-9220's entry-indexed 7,921 could not separate two shapes that differ in a
row width nobody enumerated, which is how mg-c4c8's F5 went unnoticed there.

The artifact does not move for this rewrite: `controls_output.txt` goes 23,684 → **23,695**
on **one line**, and that line is a row's own prose — "which `m != len(B)` alone does not see"
named a code fragment that no longer exists and now reads "which comparing the two ORDERS alone
does not see". `probe_output_n6.txt` is byte-identical.

---

## 2. OPEN 2 — the declaration is derived from the patch

mg-9220's declarations were **written**. Eight of eleven said "one `return` statement" for a
patch that removed the `return` **together with the `if` that guards it**, and `AFTER-5`
removed a two-clause condition as well. A declaration that understates its patch makes the
deletion evidence look finer-grained than it is, invisibly, because the declaration is what a
reader consults instead of the diff.

**Nothing in the mutation table states a size any more.** `kern5f9a.unit_removed` parses the
tree **before and after each patch** and reports what went; `d2` prints it on the line the
result is read on:

```
AFTER-5 -- delete the one `shape` return: artifact CHANGES (predicted CHANGES), exit 1
  [UNIT REMOVED, DERIVED FROM THE PATCH: 1 `return`, 0 other statement(s),
   0 boolean clause(s), 6 syntax node(s) in all, from `absorb_trace`;
   string(s) removed with it: 'shape']
```

A computed declaration **cannot disagree with its patch**, and it is correct at whatever grain
the patch operates at — which is what ends the regress rather than descending it. The gate
labels are derived too: `'shape'` is printed because that string constant left the tree, not
because anyone typed it.

**The check is demonstrated on the real mismatch.** mg-9220's eleven sentences are kept
verbatim (`UNITS_AS_SHIPPED`), with mg-c4c8's H4 reading of each quoted beside it, and measured
against the patches they were written for (`SHIPPED_PATCHES`, applied to `b6bc2ef` — the four
patches this commit narrowed are applied in their shipped form, so the comparison is about
mg-9220's work and not about this commit's):

| tag | written | measured | | tag | written | measured |
|---|---|---|---|---|---|---|
| BEFORE-1 | 0/0/1 | 0/0/1 exact | | AFTER-5 | 1/0/0 | **1/1/1** |
| BEFORE-2 | 1/0/0 | **1/1/0** | | AFTER-6 | 1/0/0 | **1/1/0** |
| AFTER-1 | 1/0/0 | **1/1/0** | | R1 | 1/0/0 | **1/1/0** |
| AFTER-2 | 1/0/0 | **1/1/0** | | R2 | 1/0/0 | **1/1/0** |
| AFTER-3 | 0/0/0 | 0/0/0 exact | | R3 | 2/0/0 | **2/2/0** |
| AFTER-4 | 0/1/0 | 0/1/0 exact | | | | |

**8 of 11 understate — reproduced from this repository's own code, not quoted from the audit.**

And the property that makes deriving a fix rather than a correction pass is scored: widen
`AFTER-5`'s patch to take out a second `return` and the declaration says **2 returns** and names
a second label, **with nothing edited anywhere**. mg-9220's sentence would go on saying "one
`return` statement" under the same widening.

**The four AFTER patches are also narrowed.** `AFTER-1`, `-2`, `-5` and `-6` now substitute
`pass` for the `return` and leave the guarding `if` standing, so mutation and declaration are the
same size **by construction** as well as by measurement — mg-c4c8's F2 named this as the
preferable of its two fixes. Every artifact verdict and exit code is unchanged, and mg-c4c8's H1
ran the same four narrow patches independently and reports the same verdicts.

---

## 3. The finest unit is stated beside the test

mg-c4c8's OPEN 1, second half: state what the evidence covers instead of letting a reader assume
it reaches all the way down. Every result line now carries, from the same measurement:

```
FINEST UNIT THIS LINE PERTURBS: one `return` statement, and nothing finer is removed
FINEST UNIT THIS LINE PERTURBS: a CONDITION of 2 clause(s) -- and the clauses inside it
                                are NOT individually tested by this line
```

`BEFORE-1` gets the second sentence, and it is the honest one: that mutation deletes a clause of a
two-clause condition on the pre-repair tree, and its byte-identical result is a claim about that
clause and about nothing inside it.

---

## 4. The ways this repair could be the defect it repairs

Every remedy in this lineage so far has been an artifact of the same kind as the defect and has
inherited it. The last section of `d2_deletion.py` enumerates the branches **with the run**, six
checked by a claim in the file and two carrying the reason they cannot be:

1. **The derived declaration has a grain of its own** — `return`, statement and clause are three
   *chosen* units, so a patch removing something finer (an operand, an argument) would print 0/0/0
   and understate itself exactly as the sentences did. **Checked:** every declaration also carries
   `nodes`, the count with no grain — every syntax node the patch removes — and a claim goes red on
   any mutation with nodes removed and nothing named.
2. **The declaration could be computed from a different tree than the battery runs** — the
   provenance form of the same defect. **Checked in every `run_case`:** the mutated file is read
   back off disk from the directory the battery ran in and compared byte-for-byte with the text the
   declaration was derived from.
3. **The clause sweep could be one rung coarser than the tree** (`a or (b and c)`). **Checked:** it
   counts clauses that are themselves boolean expressions and goes red if any exists.
4. **The sweep could be a check nobody has seen go red.** **Checked:** the pinned run at `b6bc2ef`,
   above.
5. **The equivalence population could be blind to what the rewrite touches**, which is what
   mg-9220's 7,921 pairs were. **Checked:** indexed by shape profile, and comparing the raised
   exception as well as the decision and the gate.
6. **The `aim` strings could acquire a size that contradicts the derived unit.** **Not checked**,
   and it cannot be without parsing English — which is the apparatus this repair removes rather than
   adds. Survivable because nothing computes from an aim and the derived unit sits on the same line.
7. **The regress could continue below a clause** — an operand of `!=`, a call, a name. **Cannot
   arise for the deletion test:** deleting an operand of a comparison does not leave a condition, so
   there is no smaller deletion at this site. A *mutation* test has a grain of its own and nothing
   here speaks for it.
8. **The four narrowed patches could have changed what the test measures.** **Checked:** verdicts
   and exit codes unchanged, and confirmed independently by mg-c4c8's H1.

---

## Numbers, re-measured here rather than carried

- Battery: **43 scored rows**, 2 [CANNOT FAIL], 0 failures, exit 0, **23,695 bytes** (23,684
  before; one row's prose). `probe_output_n6.txt` **byte-identical**.
- Instrument: `run_all.sh`, **83 claims, 0 BROKEN**, exit 0 — d1 17, **d2 44**, d3 6, d4 16
  (72 and d2 33 at mg-9220). No `| tee` (mg-f922).
- `absorb_trace`: **5 returns**, **0 deciding clauses**. `gate_violations` and `diagonal_moves`
  keep 2 clauses each and are untouched (mg-c4c8 F3).
- Equivalence: **28,900 pairs, 85 shape profiles, 28,900 identical outcomes** — decision, gate and
  exception.
- Declarations: **11 of 11 derived**; mg-9220's written ones understate on **8 of 11**.

## Disclosures

1. **mg-c4c8's F3, F4, F5 and F6 are not closed here.** F3's two inert returns
   (`gate_violations`, `diagonal_moves`) keep the two-clause form and their clauses are measured
   above and left as they are; F5's totality change is now stated in `absorb_trace`'s docstring
   because this commit's own equivalence claim rests on the same population, but the return-sweep
   F3 asks for and F4's re-anchoring and F6's row-set guard are other items. This item was OPEN 1
   and OPEN 2.
2. **Four derived artifacts were regenerated** because the artifact moved by one line:
   `controls_output.txt`, `positive_control_all_fail.txt`,
   `code/face_geometry_audit_e7bc/pc_all_pass.txt` and
   `code/face_geometry_landing_da45/out_verify.txt` (one line, the byte count). The third is inside
   an audit directory and is a *generated control*, regenerated for the reason its own claim gives;
   no transcript or finding of that audit was touched.
3. **mg-c4c8's own instrument will not reproduce its clause table against this tree**, and that is
   this commit's doing: its H2 enumerates `absorb_trace`'s two clauses from the tree, and the tree
   no longer has them. Its transcript is its record of its own run, the treatment this lineage gives
   every audit it acts on. Its H1, H3 and H4 are unaffected in kind; H4's reading table names
   mg-9220's sentences, which are preserved verbatim in `d2_deletion.py`.
4. **A new pin is a new provenance exposure**, so it is checked the way mg-c4c8's floor item checked
   the old one: `MERGED_REF` is verified to be the newest commit touching `face_complex.py` whose
   `absorb_trace` has a two-clause `shape` condition.
5. **No mathematics was touched**, no row was added or removed, no label changed, and **nothing was
   added to `controls.py` to watch the clause** — the sub-unit was removed, not detected.
6. **Section 4 was written after this item started**, in response to a mid-task instruction to
   enumerate the ways the fix could exhibit the defect it remedies. The enumeration is this
   commit's; branches 1–5 and 8 were checks the repair already carried or acquired because of it.
