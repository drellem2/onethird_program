# Landing mg-d0e2: the two gates nothing reached, and a check that could not fail

**Item:** mg-04a8. **Closes:** mg-d0e2's OUTSTANDING 1 and OUTSTANDING 2, and the
requirement that audit attached to the repair.
**Code:** `code/face_geometry/controls.py`, `code/face_geometry/face_complex.py`,
instrument in `code/face_geometry_instr_5f9a/` (`run_all.sh`, 73 s, 56 claims, 0 BROKEN).

mg-d0e2 booked mg-5f9a's repair as real and did not re-open it. This lands the two things
it left open. Neither is a mathematical result; both are about whether the checks that
report the mathematics can fail.

---

## OUTSTANDING 1 — two of nine deletions moved nothing. Now nine of nine move

mg-d0e2 ran the deletion test on nine mutations of the code this battery's sentences
name. Seven moved the artifact. Two did not: **`absorb_trace`'s two `shape` returns and
its `parity` contradiction branch**. Deleting either left `controls_output.txt`
byte-identical at 20,738 bytes with every row green.

**The cause was measured, not guessed, and it is not that the branches are wrong.**
Across the four populations this section fed the predicate before these rows existed — 297
NC4 biting pairs + 306 brute-force pairs + 82 NC3 pairs + 172 instrument pairs = **857** —
the number of pairs decided at the parity gate is **0**, and the number with a shape
mismatch anywhere is **0**. (mg-d0e2's measurement, re-derived by its own `e2_parity.py`
and scored under `d4`; the constructed pairs below are a fifth set and are not in it.) A predicate that had lost the ability to reject a contradictory sign system, or to
notice that the two sides are not the same shape, would have agreed with every question
the battery asked and every row would still have been green.

**So the two branches are exercised on constructed pairs, and the answer they are scored
against is derived rather than written down.** `controls.absorbable_bruteforce` is the
definition enumerated over all 2^m sign vectors; it shares no line of code with
`absorb_trace`, and it compares with `mat_eq`, so a shape mismatch is simply an equality
no sign vector satisfies. Two new rows in NEGATIVE CONTROL 4's instrument-check block:

| row | pairs | what they are |
|---|---|---|
| the `shape` branch | 3 | 2×2 against 3×3; same order but **ragged** (the second `shape` return); and an accepting pair, identical 2×2 |
| the `parity` branch | 2 | a **contradictory** system — `s0s1 = +1` and `s0s2 = +1` force `s1s2 = +1`, and the pair demands `s1s2 = −1`; and an accepting pair on the same support, `s = (+1,−1,−1)` |

Each list carries a pair the branch must **accept** as well as one it must reject.
Without that, the row would pass on a predicate that answered "not absorbable" to
everything — the [CANNOT FAIL] defect this section already carries one scar from.

**Measured, from mg-d0e2's own instrument run unmodified against this tree**
(`d4_auditor_rerun.py`, which runs that audit's `e1`, `e2` and `e3` as subprocesses and
scores what they say — it is the strongest evidence available about this repair, and it
costs one subprocess to use, since its nine mutations were re-derived from the source of
`absorb_trace` precisely so as not to be the subject's own instrument):

```
delete gate 'shape'    23680 -> 24879  CHANGED  exit 1     (was: 20738 -> 20738, exit 0)
delete gate 'parity'   23680 -> 24767  CHANGED  exit 1     (was: 20738 -> 20738, exit 0)
THE DELETION TEST NOW BITES ON 9 OF 9.
```

Exactly one row fails in each case, and it is the row built for that branch.

**No reason was written for those two.** mg-d0e2 was explicit that writing one is the
defect this lineage has produced three times. What is written is what they are: branches
no population reached, now reached by pairs built for them.

---

## OUTSTANDING 2 — the repair's own check held on an artifact where every row read [FAIL]

The shipped check published "AFTER-1: every scored row keeps its label and its condition
— 43 rows, 0 label change(s)". `d2_deletion.py` selected rows by substring and compared
`a.split(" ")[1]`; row lines are indented two spaces, so **that token is the empty string
for every row in either text**. mg-d0e2 ran it on an artifact with every row flipped to
`[FAIL]` and it reported 0 label changes and HELD.

**The parsing bug is not the defect.** The check measured the **stability** of the labels
between two runs, and stability is a property a wrong label has too. Fixing only the
parsing would leave a check that still passes whenever a mutation that ought to break a
row meets a battery too blind to notice — both leave the labels where they were.

**So the labels are now compared against an expected value derived four other ways**, none
of them the row markers being checked:

1. **the fail-set registered beside each mutation before it ran** — which rows must read
   `[FAIL]`, named by a substring of the row's own text;
2. **the process exit status**, which `summarise` computes from the FAIL tally, not from
   the printed rows;
3. **the summary block** at the bottom, built from the same tallies by a different
   function than the one that prints the rows;
4. **the CANNOT FAIL set carried from the unmutated run** — it has to come from there,
   because `summarise` returns as soon as anything failed and never prints that list on a
   failing run, which is exactly when it is needed.

Plus one clause that closes the hole the repair could have opened: **each registered row
name must match exactly one row.** A registration naming a row that does not exist matches
nothing, contributes no expectation, and would pass — which is precisely the state
AFTER-5 and AFTER-6 were in before the rows they name were written. A prediction that
cannot be located is not a weaker prediction; it is none.

### Demonstrated on the broken artifact, which is kept and committed

`code/face_geometry_instr_5f9a/positive_control_all_fail.txt` — the committed artifact
with every scored row's marker replaced by `[FAIL]` and **nothing else touched**. Leaving
the bottom-line summary alone is what makes it a corrupted artifact rather than a failing
run, and that disagreement between the two channels is what the repaired check finds. It
is generated, not stored by hand, and a scored claim fails if it stops being exactly the
flip of the live artifact — a positive control describing a previous artifact tests
nothing about this one.

Run on it, both checks, from this repository's own code rather than quoted from the audit:

```
THE SHIPPED CHECK, VERBATIM:  'every scored row keeps its label and its condition
                               -- 45 rows, 0 label change(s)',  HOLDS = True
THE REPAIRED CHECK:            43 scored row(s); 43 mismatch(es); 43 row(s) read [FAIL]
                               and the summary block lists 0   ->  RED
```

And a control on the repaired check itself, three inputs, no battery run: it says yes on
the unmutated artifact with nothing registered; it goes red when a row registered as
failing did not fail (**the wrong-but-stable case**); and it goes red on a registration
naming no row at all.

---

## The requirement mg-d0e2 attached, and it is the generalisable half

> For every check this repair touches or adds, state IN THE CODE: "this check's answer
> would differ under change X."

Implemented as a required argument. `claim()` in `d2_deletion.py` and `d4_auditor_rerun.py`
takes `differs_under` and prints it under every claim, so the transcript carries it too:

```
  [HOLDS ] AFTER-1: 43 scored row(s); every label equals the independently derived ...
        WOULD DIFFER UNDER: a row reading [FAIL] that the registered prediction and the
        summary block do not name, or a row this mutation was predicted to break still
        reading [PASS].  NOT under a label that is merely the same as the baseline's --
        that is the shipped check, and it holds on an artifact where every row reads [FAIL]
```

Writing them is where this repair found its own worst clause. The claim that reproduces
the shipped check's vacuity is scored **TRUE** — the defect is real — and naming what
would change its answer forced the honest sentence: *nothing available to a corruption of
the artifact; its answer is fixed by the indentation and cannot depend on any label.*

The two new rows in `controls.py` carry theirs as a block comment at
`UNREACHED_GATE_PAIRS`, naming the deletion that flips each — and both deletions are run
in `d2_deletion.py` rather than argued.

**"Can it fire?" is necessary and not sufficient.** Both vacuous checks this repository
produced that afternoon could fire in principle. Each was blind to the specific defect it
was read as guarding, by checking a property invariant under exactly that failure — a
figure present *somewhere*, a label *unchanged*.

---

## A third check of the same kind, found while repairing these two

Not on mg-d0e2's list; found by asking the "would differ under" question of every check
this file already had.

**The BEFORE half read the branch `main`.** It was the pre-repair tree only until mg-5f9a
merged. After that, its first claim — "main's committed `controls_output.txt` regenerates
from main's sources" — was a statement that this tree regenerates from itself, true under
every possible defect. And the deletion it then attempted did not apply: **running the
shipped file today stops at `BEFORE-1: anchor occurs 0 times in main's face_complex.py`.**

It is pinned to `5cae82c^` (`kern5f9a.PRE_REPAIR_REF`), the commit before the
instrumentation, and the transcript records the resolved sha. `d1_trace.py`'s "this tree's
predicate vs the pre-repair one, 516 pairs, 0 differ" had the same rot and is pinned the
same way. A check pinned to a branch answers a question about whatever that branch holds
today; a check pinned to a commit answers the question it was written to ask.

---

## Numbers, re-measured here rather than carried

- Battery: **43 scored rows** (41 + the two added here), 2 [CANNOT FAIL], 0 failures,
  exit 0, 23,680 bytes. `probe_output_n6.txt` is **byte-identical** — no mathematics moved.
- Instrument: `run_all.sh`, 73 s, **56 claims, 0 BROKEN**, exit 0 (d1 16, d2 25, d3 6, d4 9).
- mg-d0e2's own `e1_deletion.py`, unmodified: **9 of 9 mutations change the artifact.**
- Nothing retreated, scored in `d4` rather than asserted: its `e2_parity.py` is **0 BROKEN**
  (the 297/306/82/172 split and the 57-of-297 disagreement are untouched), and its
  `e3_seams.py` is **2 BROKEN**, both of them frozen literals of the same kind as its row
  count — it asserts the artifact says `lines scanned: 62` and `40 row names among them`,
  and the artifact now says **64** and **42**, both computed live by the row that owns
  them and both correct. Two of its three findings about mg-5f9a are **gone**: F3 (the
  43-versus-41 row count) and F4 (the stale docstring).
- `code/face_geometry_landing_da45/out_verify.txt` regenerated: **1 line**, the artifact's
  byte count, 20,738 → 23,680. Its own `run_all.sh` says that file reads the live tree and
  "will drift when controls.py's counts next change", which is what happened. Still 25
  claims, 0 BROKEN, exit 0, and `verify_landing.py` itself is not edited.

## Disclosures

1. **mg-d0e2's committed transcripts are not touched**, the treatment mg-5f9a gave
   mg-1c80's `a6_mutations.py`. But there is a difference and it is stated rather than
   left: `a6_mutations.py` degraded and still exited 0, while **`e1_deletion.py` exits 1
   against this tree**. Exactly one of its claims is BROKEN and it is its frozen row count
   — it asserts 41, the number it measured at `5988134`, and this tree has 43. `d4`
   scores that, so a *different* claim of that audit going broken would fail this
   instrument rather than pass unnoticed. Its two prediction MISSes are both in the good
   direction: it predicted `shape` byte-identical (it now changes) and predicted `parity`
   changed against mg-5f9a (it now does).
2. **mg-5f9a's published "43 rows" was a substring count of an artifact carrying 41**
   (mg-d0e2's F3), and this repair takes the artifact to a genuine 43. **The coincidence
   is named at both doc sites** so the old figure is not read as having been right.
3. **AFTER-2's fail-set was registered wrong** — row I4 rather than the
   union-find-versus-brute-force row. Kept in the code under `MISREGISTERED` and stated in
   the corrected landing section rather than edited away.
4. **F4 is closed as a side effect and disclosed as one.** `absorb_trace`'s docstring said
   `controls.deciding_gate` "is a call to this function"; that name has no referent —
   mg-5f9a deleted it outright, which `d1_trace.py` asserts in the AST. The docstring now
   says what shipped.
5. **No scoring change to any existing row**, and no mathematics touched. The two rows
   added are instrument checks on the predicate, in the block that already holds the
   union-find-versus-brute-force check; every pre-existing row keeps its label and its
   condition — verified by the repaired label check and not by the one it replaced.
6. **mg-d0e2's F5-adjacent items and mg-1c80's F3/F5 stand open**; this item was the two
   OUTSTANDING halves and the requirement attached to them.
7. **`run_all.sh` still does not use `| tee`** — a pipeline's status is the last command's,
   so `tee` would mask a verifier exiting 1 (mg-f922).
