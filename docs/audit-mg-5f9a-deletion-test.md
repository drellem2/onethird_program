# Independent audit of mg-5f9a / `5cae82c` — the instrumented predicate

**Work item:** mg-d0e2 (pre-filed in the same action as its parent mg-5f9a).
**Subject:** `5cae82c` — *"NO THIRD REASON — the predicate now RETURNS the gate it returned at
and the signs it read, and the deletion test that caught the last version now CHANGES the
artifact"*.
**Instrument:** `code/face_geometry_audit_d0e2/` (`run_all.sh`, 26 s, 25 claims, 0 BROKEN,
3 findings). Nothing under `code/face_geometry/` is written by it.

---

## Verdict

**The repair is real, and it is the right move.** This is the third attempt at one sentence
(mg-8a12 → mg-da45 → mg-5f9a). The first two wrote a reason *beside* the predicate and both were
wrong about it. This one did what its ticket asked: it did **not** write a third reason. It made
`face_complex.absorb_trace` return the gate it returned at, made `absorbable_by_diagonal_twist` a
one-line wrapper over it, and deleted `deciding_gate` outright.

**The deletion test bites now, and I ran it on more gates than the repair did.** Nine mutations,
predictions registered before every run, **8 of 9 matched**. The one miss is reported below and is
not the old defect returning.

**The substance is not weakened.** mg-1c80's n = 8 antichain sweep regenerates **byte-identically**
against the repaired tree, as does mg-da45's landing verifier (25 claims, 0 BROKEN, exit 0, and
`verify_landing.py` carries no mg-5f9a edit).

Three findings follow. **None of them touches a mathematical claim**, and none is the lineage's
recurring defect. The largest is that the repair's own published number — *"43 scored rows, 0 label
change(s)"* — comes from a check that cannot detect a label change.

---

## 1. The deletion test, on every gate the explanation names

`face_complex.ABSORB_GATES` names four gates: `shape`, `diagonal`, `magnitude`, `parity`. The
artifact's sentences name all four. mg-5f9a's own `d2_deletion.py` runs the deletion on **two** of
them (`diagonal`, `magnitude`) plus an ordering swap and the sign counter. I re-derived the
mutations from the source text of `absorb_trace` rather than importing the repair's, generated my
own baseline, and ran all four gates plus five more.

Baseline first: `controls.py` regenerates its committed `controls_output.txt` **byte-identically**,
**20,738 bytes, exit 0**.

| # | mutation | artifact | bytes | exit | predicted | |
|---|---|---|---|---|---|---|
| P1 | delete gate `diagonal` (`s_i^2 = 1`) | **CHANGES** | 20738 → 20738 | 0 | changed / 0 | ✅ |
| P2 | delete gate `magnitude` (`\|s_i s_j\| = 1`) | **CHANGES** | 20738 → 20588 | 1 | changed / 1 | ✅ |
| P3 | delete gate `parity` | **BYTE-IDENTICAL** | 20738 → 20738 | 0 | changed / 1 | ❌ **miss** |
| P4 | delete gate `shape` | **BYTE-IDENTICAL** | 20738 → 20738 | 0 | identical / 0 | ✅ |
| P5 | stop counting `signs_read` | **CHANGES** | 20738 → 20735 | 0 | changed / 0 | ✅ |
| P6 | swap the two forced gates' order | **CHANGES** | 20738 → 20738 | 0 | changed / 0 | ✅ |
| P7 | delete `diagonal` from `gate_violations` | **CHANGES** | 20738 → 20729 | 0 | changed / 0 | ✅ |
| P8 | delete `magnitude` from `gate_violations` | **CHANGES** | 20738 → 20729 | 0 | changed / 0 | ✅ |
| P9 | invert `diagonal_moves` (the routing) | **CHANGES** | 20738 → 23522 | 1 | changed / 1 | ✅ |

**Both directions, reported explicitly, as the ticket requires.**

**Deleted and CHANGED — seven of nine.** The two that matter most are P1 and P2, and they change
the artifact in *different* ways, which is the signature of an honest instrument:

- **P1 (`diagonal`) changes no decision and still moves the bytes.** Exit stays 0; all 41 scored
  rows keep their labels (re-derived with a real label comparison, not the repair's — see §3);
  exactly **two** lines move, and they are the two that report where the predicate went: row I4 and
  the `WHERE THE PREDICATE RETURNED` gate table. That is what *"the reason is produced by the code
  path"* means operationally, and it is precisely the test mg-da45's version failed.
- **P2 (`magnitude`) changes a decision.** Exit **1**, one row goes `[FAIL]`, the artifact loses two
  lines. Row I4's three diagonal-preserving pairs violate the magnitude gate **alone**, so that
  gate really is load-bearing there — which is exactly the narrower claim the artifact now makes
  about them, and no longer the wide one mg-da45 made.

P6 confirms the artifact's own caveat: reversing the order of the two forced gates changes no
answer and still moves the same two lines. P7/P8 show the exhaustive companion `gate_violations` is
load-bearing on four lines each. P9 shows the routing is scored, not decorative.

**Deleted and IDENTICAL — two of nine, and one was predicted.**

- **P4 (`shape`) — expected and harmless.** No pair in any population the battery builds has a shape
  mismatch, and the artifact's *"Shape unchanged on 61/61"* is measured by `controls.py`'s own
  guard, not by this gate. Nothing claims the predicate's shape gate decides anything, so nothing
  is falsified. I registered "identical" in advance for this reason.
- **P3 (`parity`) — the miss.** Discussed next.

---

## 2. The one prediction miss: the parity gate is unreached

Deleting `return Trace(False, "parity", signs_read)` — the union-find's contradiction branch —
leaves the artifact **byte-identical** and the battery exiting **0**. I predicted it would break the
brute-force agreement row. It does not.

**This is not the old defect, and I want to be exact about why.** mg-da45 printed a gate name **as
the reason** its rows answered as they did, and deleting that gate changed nothing — the name was
false. Nothing in this artifact says the parity gate decides any row. Its sentences say **0 pairs
reach it**, which is a true statement that the deletion cannot disturb. The label `"parity"` is also
emitted on the *accepting* return, so the trace table's `0 parity` column is unaffected either way.

What the deletion does show is narrower and worth having. Measured over every population the battery
feeds the predicate:

| population | pairs | shape | diagonal | magnitude | parity | reached parity | **rejected at parity** |
|---|---|---|---|---|---|---|---|
| NC4 biting (poset, mutation) pairs | 297 | 0 | 237 | 60 | 0 | 0 | **0** |
| the `\|L(P)\| ≤ 8` brute-force agreement row | 306 | 0 | 153 | 45 | 108 | 108 | **0** |
| NC3's facet-parity corruption, biting posets | 82 | 0 | 0 | 0 | 82 | 82 | **0** |
| the two instrument-check rows' pairs | 172 | 0 | 86 | 0 | 86 | 86 | **0** |
| **all four** | **857** | | | | | | **0** |

The NC4 split, 237 diagonal + 60 magnitude + 0 parity, reproduces the artifact's per-row table
(15+57, 82+0, 82+0, 58+3) exactly, re-derived without importing the repair's instrument.

**F1 (new, minor, not a regression). The one row that exists to test the union-find cannot fail on a
broken parity rule.** That row is *"the union-find absorbability decision agrees with brute force
over all 2^m sign vectors on 306/306 (poset, mutation) pairs with |L(P)| ≤ 8"*, and it is the only
thing standing between *"absorbable on 0/61"* and a solver that says what it likes about signs. Over
its 306 pairs it exercises the forced gates and the **accepting** parity path 108 times, and the
**rejecting** one never. A predicate that had lost the ability to reject a contradictory sign system
would agree with brute force on all 306 and the row would pass.

Demonstrated rather than argued: the pair `A = [[0,1,1],[1,0,1],[1,1,0]]`,
`B = [[0,1,-1],[1,0,1],[-1,1,0]]` encodes `s₀s₁ = +1, s₁s₂ = +1, s₀s₂ = -1`. The shipped predicate
decides it at the parity gate (`gate='parity'`, `absorbable=False`, `signs_read=3`) and brute force
over all 2³ sign vectors agrees. **No pair of its kind is among the 306.** The branch is live,
reachable code, simply not reached by anything this battery constructs.

This is a gap in the battery, not a false sentence in the artifact, and it predates mg-5f9a.

---

## 3. F2 — the repair's own "no label changed" check compares the empty string

`d2_deletion.py:167-177` establishes the repair's headline safety property, published in the commit
message, twice in the landing doc, and twice in `out_d2_deletion.txt`:

> AFTER-1: every scored row keeps its label and its condition — **43 rows, 0 label change(s)**

It extracts rows by substring and then compares `a.split(" ")[1]` between baseline and mutant. Row
lines in this artifact are **indented two spaces**, so `"  [PASS] I4 …".split(" ")[1]` is `''`. The
token compared is the empty string for **all 43** lines, in both texts, always.

**Demonstrated, not asserted.** Run the repair's own comparison, transcribed verbatim, against an
artifact in which *every* row has been flipped to `[FAIL]`:

```
      -> '43 rows, 0 label change(s)', check HOLDS = True
```

The label half of the claim is **vacuous**. What survives is the length comparison, which does catch
a row appearing or vanishing — and that is what actually fired for the magnitude deletion (68 → 66
lines).

**The conclusion the check was used to support is nevertheless TRUE.** My E1 re-derives it with a
real label comparison over line-initial markers and gets **0 label changes** for both P1 and P6. So
the repair's finding stands; the check it published is not what established it. Given that this
lineage's whole subject is *"a control asserting something it does not have"*, a check that cannot
fail is worth naming in it.

**F3 — the row population is 41, published as 43.** Counted by substring the artifact has 43 lines
carrying a marker; counted as rows (marker starts the line) it has **41** — 39 `[PASS]` + 2
`[CANNOT FAIL]`. The two over-counted lines are both *"measured, not scored"* bullets that merely
**mention** `[CANNOT FAIL]` in their prose:

- `* the absorbability predicate — which after mg-8a12 scores ONE row (I4) …`
- `* row scoring, and who owns it: every row above is vacuous …`

The artifact says in terms that lines in that block *"are measurements, not rows"*. The rest of the
same sentence is right: 2 rows carry `[CANNOT FAIL]`, 0 failures, exit 0.

---

## 4. F4 — a stale name inside the repair's own central docstring

The removal of `deciding_gate` is **complete in code**: `controls.py` defines no gate procedure, no
function and no alias, and `d1_trace.py` asserts that absence in the AST. Every other surviving
mention of the name is either the repair's own narrative describing what it deleted, or mg-1c80's
committed audit transcripts — correctly left as the records they are.

One is not. `face_complex.absorb_trace`'s docstring — the docstring of the predicate this entire
repair is about — still reads:

> So the label is produced here and `controls.deciding_gate` is a call to this function, not a
> second implementation of it.

**`controls.deciding_gate` does not exist.** It describes a design that was considered and *not*
shipped: mg-5f9a deleted the function outright rather than making it a thin wrapper, which is the
stronger choice and the one its commit message announces. The sentence is the weaker plan left
behind, sitting in the one place a future reader is most likely to trust, and the repair's own
instrument is what proves it wrong.

Cheap to fix and it changes no number.

---

## 5. What did not move

- **Substance, n = 8 — CONFIRMED, not weakened.** mg-1c80's antichain sweep (46,232 words,
  n = 2..8) regenerates **byte-identically** against the repaired tree: 1,973 bytes, exit 0. The
  mismatch census (2·n! magnitude mismatches, exactly 2 per row, 0 sign-only, diagonal preserved,
  gate `magnitude`) is unchanged at every n from 3 to 8.
- **mg-da45's landing verifier** regenerates **byte-identically** (6,001 bytes, exit 0, *"25
  claim(s) scored; 0 BROKEN"*), and `verify_landing.py` carries no mg-5f9a edit — last touched by
  `f024985`, mg-da45's own commit. Only its committed *output* was regenerated, for the byte count
  17,964 → 20,738 and one occurrence count 2 → 1.
- **Disclosure checked and accurate.** That verifier's closing prose still reads *"the file now
  MEASURES which gate settled it"* — the framing mg-1c80 refuted. mg-5f9a's commit says in terms
  that it left this as another item's artifact rather than editing it. That is what it did.

### The agreement number the ticket asks for

The ticket asks: if the repair wrote prose again, how many of the 297 pairs does the prose agree
with the predicate on? **It did not write prose.** The label is emitted at the `return` that fired,
so the printed gate and the predicate's gate are the same object:

| | agreement over the 297 NC4 biting pairs |
|---|---|
| the shipped label vs the predicate | **297 of 297**, by construction |
| mg-da45's `deciding_gate` vs the same | **240 of 297** — differing on **57** |

mg-1c80's *"57 of 297"* re-measured, not quoted. *(For the record: this audit's ticket phrases it as
a relabelling **"agreeing on 57"**. The measurement is that it **disagrees** on 57 and agrees on 240.
mg-5f9a's commit and landing doc both state it the right way round.)*

### Seam-check and the threshold

The artifact has now been corrected twice for the same defect, so every site stating the same fact
was compared: the artifact, the landing doc, the repair's three transcripts, mg-da45's verifier, and
mg-1c80's n = 8 record. The trace table agrees across all of them (I1 = 15/57/0, ALL = 237/60/0).
The only cross-site disagreement found is F3's 43-vs-41.

**The artifact's own control prints its extent and the extent is correct**: *"lines scanned: 62 (the
whole artifact above this row; 40 row names among them)"*. There are exactly **62** lines strictly
above that row, and the artifact carries 41 scored rows of which that row is one — so **40** is
right. **The threshold is the 17-character all-pass banner literal**, case-sensitive, and it is 17
characters. Note that this row counts row *names* correctly (40) while the repair's instrument
counts row *lines* incorrectly (43); the two live in different files and only the second is wrong.

---

## Predictions and misses

Nine registered before the runs, **8 matched**. The miss is kept:

> **P3 — delete the `parity` gate → predicted CHANGES / exit 1; observed BYTE-IDENTICAL / exit 0.**
> I reasoned that the brute-force agreement row, which compares the union-find against exhaustive
> enumeration on 306 pairs, would catch a predicate that could no longer reject. It would — if any
> of the 306 required rejecting. None does. The miss is what produced F1, and I would not have
> looked for F1 had the prediction landed.

## Reproducing

```sh
code/face_geometry_audit_d0e2/run_all.sh      # 26 s, 25 claims, 0 BROKEN, 3 findings, exit 0
```

Exit status is about this audit, not its subject: a `[FINDING]` line is a defect in mg-5f9a and does
not fail the script; a `[BROKEN]` line is a claim of this audit's own that did not hold, and does.

## Open, for whoever picks them up

- **F1** — the brute-force agreement row exercises the union-find's accepting path 108 times and its
  rejecting path never. Adding one contradictory pair to its population would close it. Predates
  mg-5f9a.
- **F2** — `d2_deletion.py:167-177` compares `split(" ")[1]`, which is `''` for every indented row.
  Its conclusion is independently true; the check is not.
- **F3** — "43 scored rows" is 41; the count includes two prose bullets.
- **F4** — `absorb_trace`'s docstring names `controls.deciding_gate`, which does not exist.
