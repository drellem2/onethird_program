# Independent audit mg-e7bc: the repaired check, run on the broken artifact

**Item:** mg-e7bc, pre-filed in the same action as its parent mg-04a8.
**Subject:** `c7f9673` — mg-04a8's repair of mg-d0e2's OUTSTANDING 1 and OUTSTANDING 2.
**Instrument:** `code/face_geometry_audit_e7bc/` (`run_all.sh`, ~90 s, **25 claims, 0
BROKEN, exit 0**; g1 8, g2 7, g3 5, g4 5). Mutations, row parser, summary parser and
corruption generators re-derived from the source rather than imported from the subject's
`kern5f9a.py` or from mg-d0e2's `kernd0e2.py`. Nothing under `code/face_geometry/` is
written; every battery run goes to a copy in a temporary directory.

**Verdict: the repair is real and the primary measurement is unambiguous — the repaired
check EXITS 1 on the artifact where every row reads `[FAIL]`, the broken artifact is kept
and committed, and the deletion test bites on 9 of 9 measured with this audit's own
mutations.** Eight findings, none of them a retreat. The sharpest is that the `shape`
gate has **two** `return` statements, mg-04a8 deletes them together, and **deleting the
first one alone still leaves the artifact byte-identical** — the exact state mg-d0e2 found
the whole gate in, one level down.

---

## 1. The primary measurement — the exit code

`checkrun.py` wraps mg-04a8's `check_labels` unmodified and turns its verdict into a
process status: **0 = the check says yes, 1 = the check goes RED**. Everything fed to it
(row population, baseline `CANNOT FAIL` set, registration) is derived by this audit.

| artifact | shipped check | repaired check |
|---|---|---|
| the committed artifact, untouched | 0 | **0** |
| `positive_control_all_fail.txt` — all 43 rows `[FAIL]` | 0 | **1** |
| MINE: all 43 rows `[PASS]`, incl. both `[CANNOT FAIL]` | 0 | **1** |
| MINE: exactly ONE `[PASS]` flipped to `[FAIL]` | 0 | **1** |
| MINE: exactly ONE `[CANNOT FAIL]` demoted to `[PASS]` | 0 | **1** |
| MINE: rows untouched, the SUMMARY names a false failure | 0 | **1** |
| MINE: one scored row LINE deleted outright | 1 | **0** |

- **The broken artifact is kept and committed** — `git ls-files --error-unmatch` succeeds,
  and it is still byte-equal to this audit's own all-`[FAIL]` retagging of the *current*
  `controls_output.txt` (23,666 bytes, 43 of 43 rows reading `[FAIL]`). It is not a
  control describing a previous artifact.
- The shipped check on that same artifact reports `45 rows, 0 label change(s)` and
  **holds** — mg-d0e2's F2 reproduced from a re-derivation of its four lines rather than
  quoted.
- **The repair is not tuned to the one known-bad example.** Four corruptions of this
  audit's own — varying the direction, the scale, the channel and the sign of the
  error — each drive it red.
- **Population named:** `controls_output.txt`, 23,680 bytes, 43 scored rows (41 `[PASS]`,
  2 `[CANNOT FAIL]`, 0 `[FAIL]`), summary naming the same 2.

**This audit keeps its own control too**: `code/face_geometry_audit_e7bc/pc_all_pass.txt`,
every row promoted to `[PASS]` — the opposite direction and the more dangerous one, since
it is what a battery that had stopped checking anything would print. It is regenerated and
compared on every run, so drift is loud.

### FINDING 1 — the extent of the guard (scope, not a refutation)

Predicted exit 1, **observed 0, and the miss is kept.** A corruption that **deletes** a
scored row line leaves the repaired check green, while the *shipped* check goes red on it.
The repaired check derives an expectation for each row **present**, so a row that is gone
contributes no expectation; the shipped check compared row **counts**, which is the one
thing it did compare. The label claim mg-04a8 makes is about labels and is sound. But its
sentence "an artifact whose rows have been edited — by a corruption, a bad merge, or a
hand — disagrees with its own summary, and the check below is what notices" is wider than
what the code does.

---

## 2. The deletion test, applied by this audit — 9 of 9, both directions

Eleven mutations, re-derived from the current source text. **11 of 11 predictions
matched.** Baseline regenerates byte-identically at 23,680 bytes, exit 0.

| | mutation | bytes | verdict | exit |
|---|---|---|---|---|
| D1 | delete gate `shape` (BOTH returns) | 24,879 | CHANGED | 1 |
| D2 | delete gate `diagonal` | 23,680 | CHANGED | 0 |
| D3 | delete gate `magnitude` | 23,530 | CHANGED | 1 |
| D4 | delete gate `parity` (contradiction branch) | 24,767 | CHANGED | 1 |
| D5 | stop counting `signs_read` | 23,677 | CHANGED | 0 |
| D6 | swap the two forced gates' order | 23,680 | CHANGED | 0 |
| D7 | delete `diagonal` from `gate_violations` | 23,671 | CHANGED | 0 |
| D8 | delete `magnitude` from `gate_violations` | 23,671 | CHANGED | 0 |
| D9 | invert `diagonal_moves` (the routing) | 26,464 | CHANGED | 1 |
| E1\* | **MINE:** delete ONLY the FIRST `shape` return | 23,680 | **BYTE-IDENTICAL** | 0 |
| E2\* | **MINE:** delete ONLY the SECOND `shape` return | 24,879 | CHANGED | 1 |

**Deleted-and-changed: 9 of the 9 mg-d0e2 ran. Deleted-and-identical: none of them.**

**The route taken on the two was INSTRUMENTATION, not explanation**, and that is read off
the rows rather than off the commit message: each of D1 and D4 makes **exactly one** row
fail, and it is the row built for that branch. Both are scored rows in the artifact, not
`measured, not scored` bullets. The ticket's forbidden third generation — writing "a
reason it does not have" — did not happen.

### FINDING 2 (floor, not scope) — the first `shape` return is still invisible

Nothing in the ticket's lists names this. `absorb_trace`'s `shape` gate has two `return`
statements; `d2_deletion.py` deletes them together, on the stated ground that "they are
one gate, and deleting one of two would leave the other answering."

That sentence is **true**, and it is the reason the branch is uncovered rather than a
reason it need not be. Deleting `if m != len(B): return Trace(False, "shape", 0)` **alone**
leaves the artifact byte-identical at 23,680 bytes, every row green, exit 0 — precisely
the state mg-d0e2 found the whole gate in. Cause, measured: the pair built for it is 2×2
against 3×3, and with the first return gone it falls into the loop, where
`len(A[0]) = 2 ≠ 3 = len(B[0])` fires the **second** return and answers `False` at gate
`shape` identically. The row's clause "the 2 built to be REJECTED return at the `shape`
gate on 2 of 2" is satisfied with one of the two returns doing all the work.

A pair with `len(A) != len(B)` and **no ragged row** would separate them.

---

## 3. The "WOULD DIFFER UNDER" statements, tested by making the change

**Population:** the instrument scores **56** claims across four scripts; **34** carry a
statement (d2 25/25, d4 9/9). Five statements were tested — chosen for being load-bearing
on the repair's own account of itself. **4 of 5 predictions matched; 0 of the 5 statements
survived the test as written.**

### FINDING 3 — the requirement is implemented in 2 of the 4 scripts

`out_d1_trace.txt` (16 claims) and `out_d3_reintroduction.txt` (6 claims) carry **none**;
their `claim()` is still `def claim(text, ok, detail="")`. This is not a matter of scope:
`d1_trace.py` **was edited by this same commit**, and the one differs-under sentence it
gained went into a **code comment**, where the transcript a reader checks does not carry
it. 22 of 56 claims state nothing.

### FINDING 4 — one literal, eight uses, inverted for one of them

`run_case` prints the same sentence under all 8 of its byte-comparison claims: *"deleting a
gate that no row's answer depends on — which is what AFTER-5 and AFTER-6 used to be, and
what BEFORE-1 still is."* For BEFORE-1 — the one case whose registered prediction is
BYTE-IDENTICAL — that is what makes the claim **hold**, not what would make it differ.
Measured by making the change (E1\* above): artifact byte-identical, exit 0, and a claim
predicting BYTE-IDENTICAL still holds. The requirement is "state what would alter *this*
answer", and a constant cannot.

### FINDING 5 — the positive control's differs-under names a reversion that cannot move it

*Predicted CONFIRMED; observed REFUTED, and the miss is kept.* The claim "THE REPAIRED
CHECK ON THE SAME ARTIFACT GOES RED" says its answer would differ under "the repaired
check reverting to a comparison against the baseline's own labels". Made: a
baseline-label comparison **also goes red** on that artifact — all 43 labels moved, so
stability is exactly what it does not have. What restores green there is the shipped
`a.split(' ')[1]` token, which the sentence does not mention.

mg-04a8's prose — "stability is what a wrong label has too" — is **right**, and it is
measured here on the input where it bites: on the wrong-but-stable case (a row registered
as failing that did not fail) the reversion does flip the answer from RED to green. The
statement is simply attached to the one claim whose input it cannot move, so the
transcript reads as though the positive control tests the stability semantics. It does
not; mg-04a8's own `c2` control does.

*(This audit's own prediction made the same conflation of the shipped check's parsing bug
with its semantics, and running it is what caught that.)*

### FINDING 6 — "…or to a substring row scan" does not

With `scored_rows` replaced by the shipped substring selection, the check **still goes
red** on the broken artifact: the 45 lines it then treats as rows include the 2 prose
bullets, and the label mismatch on the real rows is untouched. The row scan fixed the
published **count** (mg-d0e2's F3, 43 vs 41); it is not what makes the check non-vacuous.
The two repairs are named in one sentence as though either alone would restore the defect.

### FINDING 7 — "nothing available to a corruption of the artifact" is too wide

The second half of that sentence — "its answer is fixed by the INDENTATION and cannot
depend on any label" — is exactly right and is the finding. The first half is refuted by
two corruptions: **deleting a scored row line** and **un-indenting one**. The shipped
check also compares row counts, so a corruption that removes a marker-bearing line moves
its answer without touching a label. Stated the way it should have been: *nothing
available to a corruption that preserves the set of marker-bearing lines and their
indentation.*

### FINDING 8 — the crux statement is untested and, measured, false

Both `d2_deletion.py` and `d4_auditor_rerun.py` say the two branches would go back out of
reach if the rows' "expected value [were] taken from the predicate rather than from
`absorbable_bruteforce`". It is the **sole** differs-under of d4's headline 9-of-9 claim.
Made — `truth = absorbable_bruteforce(A, B)` → `truth = tr.absorbable`:

- the substitution alone: **byte-identical**, exit 0 (the two expected values agree on an
  unmutated predicate, which is why nothing notices until a gate goes);
- substitution + delete `shape`: **CHANGED, exit 1**;
- substitution + delete `parity`: **CHANGED, exit 1**.

Cause, measured: each row scores **three** things — agreement with brute force, agreement
with the answer *registered beside each pair* before the run, and that the rejected pairs
return at the named gate. Killing the brute-force channel leaves the registered channel,
whose answers are literals in `UNREACHED_GATE_PAIRS` that no mutation of the predicate can
move. **The repair is more robust than its own statement claims** — but the statement is
still an untested assertion about a check, which is the defect one level up.

### Is X the failure the check guards against, or merely a change it notices?

- S1 (`run_case`): yes for 7 of 8 uses — a gate going dead is what the deletion test is
  for. For BEFORE-1 it is the experiment itself.
- S2 (baseline comparison): yes in kind — stability *was* the shipped semantics — but
  attached to an input it cannot move.
- S3 (substring scan): **no** — a change the check happens to survive.
- S4 (shipped-check vacuity): the statement's job is to admit the check guards against
  nothing; it overshoots by one class of corruption.
- S5 (expected value): yes in kind, but measurably not sufficient to cause the failure the
  sentence attributes to it.

---

## 4. The seam, the threshold, and the re-run

**THE THRESHOLD IS 64.** The artifact's last row is a control on itself: nothing above the
bottom line may carry the 17-char all-pass banner. It prints its extent live — *"lines
scanned: 64 (the whole artifact above this row; 42 row names among them)"* — and the row
sits at line 65, with exactly 64 lines strictly above it and 42 other scored rows. Both
extents are re-derived here from the committed file and both are right; both moved in this
commit (62 → 64, 40 → 42), which is exactly the situation that produces a stale figure
elsewhere in this repository.

**And the control that carries it fires.** The banner literal is planted in one row name
and the battery re-run: artifact changes 23,680 → 23,640 bytes, **exit 1**, exactly one
row fails, and it is the row that owns the threshold. Measured aside: the banner occurs
**0** times *below* the threshold too, because this battery has 2 `[CANNOT FAIL]` rows and
`summarise` prints the denial rather than the banner — so on this artifact the row compares
0 above against 0 anywhere, and what keeps it non-vacuous is the planted-banner run, not
the file.

**The seam: 17 anchored sentences across 5 sites, 6 figures, 0 disagreements** —
`controls_output.txt`, `out_d2_deletion.txt`, `out_d4_auditor_rerun.txt`,
`landing-mg-d0e2-vacuous-check.md`, `landing-mg-1c80-instrumented-predicate.md`. Each
figure is anchored to the sentence that asserts it **as current**, and the anchors are
listed in the source to be argued with. *This file's first version grepped `\d+ bytes` and
reported 20 disagreements, every one of them its own fault — mutant artifacts the deletion
test printed, and the pre-repair 20,738 correctly quoted as history. The instrument was
corrected, not the prediction, and the correction is recorded in the transcript.*

**The re-run:** `d2_deletion.py` and `d4_auditor_rerun.py` both regenerate their committed
transcripts **byte-identically** (16,128 and 10,431 bytes, exit 0) — the mg-a318 defect is
absent. Running the subject's full `run_all.sh` leaves `git status` clean.

---

## What was NOT audited

- The mathematics. No claim about posets, Laplacians or absorbability was re-derived here;
  this audit is entirely about whether the checks that report them can fail.
- 29 of the 34 differs-under statements. Five were tested.
- `d1_trace.py` and `d3_reintroduction.py` beyond counting their claims.
- Whether row I4's forced clause should be rescoped — mg-04a8 leaves that to its own item
  and so does this.

## What would close the findings

1. Add a `shape` pair with `len(A) != len(B)` and no ragged row, so the two returns
   separate (FINDING 2).
2. Give `d1_trace.py` and `d3_reintroduction.py` the `differs_under` parameter
   (FINDING 3).
3. Derive `run_case`'s statement from `want_change` instead of using a literal
   (FINDING 4).
4. Re-attach the positive control's statement to the token bug it actually turns on, and
   move the stability sentence to the `c2` control where it is tested (FINDINGS 5, 6).
5. Narrow "nothing available to a corruption of the artifact" to corruptions preserving
   the marker-bearing line set and its indentation (FINDING 7).
6. Restate d4's differs-under as what it is — the registered channel would also have to
   go (FINDING 8).
7. Either widen the repaired check to compare row counts, or narrow the sentence that says
   it notices edited artifacts (FINDING 1).

None of these is a retreat, and none of them touches a mathematical claim.
