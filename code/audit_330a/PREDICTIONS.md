# PREDICTIONS — mg-330a, the independent audit of the mg-8d5e anchor-and-term repair (`dfa263c`)

Committed **BEFORE any script of this instrument exists**. Written at
`be06d367` (HEAD of `polecat-330a` at the time of writing), against `dfa263c`
— *"docs+repair: THE ANCHOR IS DERIVED FROM THE PROPERTY, PINNED AND
COMPARED…"* — and its parent audit `mg-2c77`.

Every row below is what I expect **before** the run. **Misses are kept as
written**, with what was wrong recorded beside them in `README.md` and in the
transcripts. Nothing here is edited after a run; corrections go in an
**ADDENDUM** block at the bottom of the row's section.

---

## ONE DISCLOSURE, MADE BEFORE ANYTHING ELSE

`code/branching_audit_e34a/k1_prerepair.py` was **launched before this file was
written** — I started it in the background while still reading, because the
repair's own `run_all.sh` says it takes about ten minutes and I did not want it
on the critical path. **Its transcript has not been read at the time of
writing.** I therefore still write down what I expect it to print (P-K1
below), but the reader should know the process was already running: the
prediction is honest, the *ordering* is not clean, and pretending otherwise
would be the exact failure this arc exists to catch. Booked, not smoothed.

No other script — mine or anyone's — has been run at the time of writing.

---

## THE SCRIPTS I INTEND TO WRITE, AND THEIR EXIT CODES

Convention (copied from `code/repair_8d5e/run_all.sh`, so the ruler is theirs
and not a second one that agrees today): every `s*.py` exits `0` iff
`SELF-ERRORS == 0` **and** `FINDINGS == 0`. A non-zero exit means *"this
script has something to report"*, never *"this script is broken"*.

| script | what it does | predicted exit | why |
|---|---|---|---|
| `selftest_330a.py` | my own instrument's assertions | **0** | if it is not 0 nothing below can be read |
| `s1_anchors.py` | **enumerate every revision anchor in the repo**, resolve each, print the pair it resolves to against the pair its prose claims; classify property-derived / pinned / history-derived | **1** | see P-1c — I expect at least one finding |
| `s2_perturb.py` | build the failure: a **cosmetic** commit to `g1_provenance.py` in a clone, at HEAD **and** at a commit where the defect is still present | **0** | I expect the repair to hold |
| `s3_kernel_half.py` | re-derive **both columns** of the kernel-half confirmation from scratch — not by reading k1 | **0** | I expect 0/0/0 vs 1/1/3 to reproduce |
| `s4_term.py` | the term: 39 / 17 / 22 by an independent walk; the qualifier at all 15 sites; **and the same rule re-scoped to HEAD** | **0** | I expect the repair's own numbers to hold |
| `s5_preserve.py` | the four inputs, the second conspiring pair, the edge probe, `AND NOTHING ELSE` | **0** | `dfa263c` touched none of `code/audit_2c77/` |

**Worst exit predicted: 1**, from `s1_anchors.py` alone.

## FOREIGN SCRIPTS I INTEND TO RE-RUN, AND THEIR EXIT CODES

| script | predicted exit | why |
|---|---|---|
| `code/branching_audit_e34a/k1_prerepair.py` | **1** (P-K1) | its committed transcript ends `TOTAL BAD: 1`, and the cancelling-pair finding is a standing one the repair did not claim to close |
| `code/branching_audit_e34a/selftest_e34a.py` | **0** | |
| `code/audit_2c77/q1_reason.py` | **0** | committed `TOTAL BAD: 0`; the repair did not touch its subject except `kern5f9a.py`'s comment |
| `code/audit_2c77/q2_bound_edge.py` | **0** | committed `TOTAL BAD: 0` |
| `code/audit_2c77/q3_operands.py` | **0** | the repair claims A-2's census finding is gone; q3's other two findings were the qualifier sites and the `not determined` column |
| `code/audit_2c77/q4_prerepair.py` | **1** | the repair says q4 STILL FIRES and calls it a defect in the auditor |

`q3` at **0** is the one I am least sure of: q3 booked **3** findings and the
repair only claims to have closed the census one. If q3 comes back `1` or `2`
that is a **miss on my side**, not a defect in the repair, and it stays here as
written.

---

## THE SUBSTANTIVE PREDICTIONS

### P-1 — every derived anchor points where the sentence says

* **P-1a.** All four rows of `libe34a.anchor_rows()` will print `agrees`:
  `4755d029 / 3bc2cf76 / 4372fae9 / 52aeaf43`. `ANCHOR_DRIFT` will be empty.
* **P-1b.** `LAST_TOUCHING_G1` will resolve to `d01ff32d` and be **21 commits
  apart** from `REPAIR_REV`; `NTH_TOUCHING_1^` will resolve to `3bc2cf76`
  under a label that says *before mg-7e58*, **9 commits** from `52aeaf43`.
  These are the numbers the committed `out_k1_prerepair.txt` prints, and I
  expect them to be **unchanged at HEAD** because nothing since `dfa263c` has
  touched `g1_provenance.py`.
* **P-1c.** **A FINDING.** `ANCHOR_DRIFT` is gated in exactly **two** places —
  `k1_prerepair.py (i)` and `selftest_e34a.py`. `k4_cancel.py` **consumes
  `REPAIR_REV`** (it is the anchor that selects which commit message is
  scanned — the second site the repair itself found) **and does not gate on
  `ANCHOR_DRIFT`**; neither do `k2_five.py` (which reads `PRE_7E58_REV`) or
  `k3_undisturbed.py`. I predict I will confirm this, and that a drifted
  anchor is therefore **loud only if the selftest or k1 is run**, and silent in
  the very script whose count moved. I predict `0` of `k2`, `k3`, `k4` carry
  the gate.
* **P-1d.** **The sweep for a fourth.** The repair found two anchors the audit
  did not name and asks whether there is a third. I predict the repo-wide
  population of **history-derived** revision anchors (a revision obtained from
  `git log … -- <path>`, or an index into such a list, rather than from a
  property or a literal) is **small — I predict 2 to 4 sites outside
  `libe34a.py`**, and I predict **at least one of them is load-bearing**
  (used by something that prints a number). I name in advance the one I
  already suspect, from the repair's own commit message:
  `code/repair_69d1/p3_reason.py (i-b)`, which anchors its control on `HEAD`.
  If the answer is **0 outside `libe34a.py`**, that is a miss and it stays.

### P-2 — the constructed failure

* **P-2a.** At HEAD, a **cosmetic** commit appended to `g1_provenance.py` in a
  clone will move `LAST_TOUCHING_G1` (to the new commit) and **not** move
  `first_introducing(g1, "kernel_source=")`. `ANCHOR_DRIFT` stays empty.
* **P-2b.** So the repaired anchor does **not literally refuse** on a cosmetic
  edit — **it reports the change**, in the `history / property / apart`
  table, and the `apart` distance grows by 1 (21 → 22). I predict the correct
  reading of *"refuses rather than follows"* here is **reports**, and I
  predict the refusal is reserved for the case where the two disagree. I
  will therefore **also** build the refusal case explicitly (a commit that
  moves the property marker) and expect `ANCHOR_DRIFT` non-empty and
  `selftest_e34a.py` **red**.
* **P-2c. THE CONTROL.** The same cosmetic commit applied in a clone pinned to
  `e2577e5` (the commit **before** the repair) will make `REPAIR_REV` follow
  the edit **silently** — the old code will name the cosmetic commit as
  *"mg-76cc's repair"* and its parent as *"the pre-repair predicate"*, with no
  drift row anywhere, because there was nothing to disagree with. I predict
  the defect **reproduces at `e2577e5` and does not at HEAD**.

### P-3 — the confirmation is a DIFFERENCE, not a zero

* **P-3a.** Re-derived **from scratch**, at the kernel bend (`kern_a218.py`:
  `dim L(n,p)` one too big), the predicate at `3bc2cf76` will be **SILENT** —
  exit 0, self 0, findings 0 — and the predicate at HEAD will **FIRE** —
  exit 1, self 1, findings 3. `0/0/0` vs `1/1/3`.
* **P-3b.** The two columns are **genuinely two predicates**: the source of
  `g1_provenance.py` at `3bc2cf76` and at HEAD will differ, and specifically
  `kernel_source=` will be **absent** at `3bc2cf76` and **present** at HEAD.
  That absence is what makes the comparison non-vacuous, and I predict it is
  the *only* thing that has to be true for the vacuity of the old, drifted
  comparison to be established: under the drifted anchor both columns were
  `e5787e11`-side sources that **both** carry `kernel_source=`.
* **P-3c.** I predict `sha256(g1 @ e5787e11) == sha256(g1 @ d01ff32d)` is
  **false** but that **both carry the marker** — i.e. the drifted comparison
  was not literally byte-identical on both sides, it was *semantically* the
  same predicate. If they turn out byte-identical, better for the repair's
  claim and a miss for me.

### P-4 — the term

* **P-4a.** An independent AST walk of `face_complex.py` and `posets.py` will
  give **39** operands of every `and`/`or` anywhere, **17** of them inside a
  deciding condition, **22** in no column: `35/15/20` and `4/2/2` by file.
* **P-4b.** The 15 sites in the files `d01ff32` touched will score **15
  QUALIFIED / 0 UNQUALIFIED** under mg-2c77's own rule (the **unhyphenated**
  words `deciding condition` within 3 lines), and the rule will still score a
  site carrying only `deciding-condition` as **UNQUALIFIED** — the ruler was
  not moved.
* **P-4c.** **My own choice, named in advance** (the floor-not-scope item):
  the repair scores the term over *"the files `d01ff32` touched"* — a
  population pinned at `d01ff32`. **I will re-score the same rule over the
  whole tree at HEAD**, including the four commits that landed *after*
  `dfa263c` (`109725c`, `d3cdc95`, `8c55168`, `be06d36`) and including the
  repair's own new files. I predict **0 new unqualified LIVE claims** and
  I predict the ~20 remaining unqualified sites are **all records**
  (transcripts / commit-message quotes / prediction files). If a live claim
  has appeared since `dfa263c`, that is a finding and `s4` exits 1.

### P-5 — preserve

* **P-5a.** The **fourth input that is neither case** (`one-sided` — kern
  alone) is present in `q1_reason.py` and scores `IDENTICAL / MOVED / MOVED`,
  caught at **2 of 3** rows. Not dropped.
* **P-5b.** The **second conspiring pair of a different shape**
  (`conspiring-B`, a boolean default of `False` that adds an absent vertex, as
  against `conspiring-A`'s integer default of `0` that shifts a value) is
  present and scores `IDENTICAL / IDENTICAL / MOVED`, caught at **1 of 3**.
* **P-5c.** The edge probe: unperturbed **11**; inside all three clauses
  **12**; and **11, 11, 11** for the three outside probes (nested under a
  comprehension, in an `if` that does not return, top level in `posets.py`).
* **P-5d.** `AND NOTHING ELSE` at **11 of 11** with **0** operands removed
  from outside.
* **P-5e.** `dfa263c` edited `code/face_geometry_instr_5f9a/kern5f9a.py` (11
  lines). I predict the **parsed module is unchanged** — a comment only — and
  therefore that P-5a…P-5d are unaffected by it. I will check the parse, not
  the claim.

### P-6 — `LAST_TOUCHING_G1` is used by no anchor

* I predict `LAST_TOUCHING_G1` and `NTH_TOUCHING_1` are read in exactly
  **two** files — `k1_prerepair.py` (printed) and `selftest_e34a.py`
  (asserted **different** from the property anchor) — and by **no anchor**,
  and that deleting them would lose a **detector** (the `apart` column and two
  selftest assertions) and break **no derivation**. I will demonstrate this by
  deleting them in a clone and observing what fails.

---

## WHAT WOULD MAKE ME SAY THE REPAIR DID NOT WORK

Stated before the measurements, so that the bar cannot move afterwards:

1. A cosmetic edit to `g1_provenance.py` moves `REPAIR_REV` or `PRE_REV` at
   HEAD, **silently**. → the repair did not fix A-1.
2. The kernel-half confirmation's two columns are the **same** predicate
   (both carry `kernel_source=`, or both resolve to the same revision). → the
   confirmation is still vacuous.
3. Any of the four anchor rows resolves to a pair different from the pair its
   own prose names. → an anchor still points somewhere its sentence does not.
4. The 15 sites do not all carry the unqualified-form qualifier, or the rule
   was widened so that `deciding-condition` now scores QUALIFIED. → the
   finding was closed by moving the ruler.
5. Any of the preserved items (P-5a…P-5d) is gone or has changed value.

None of these is predicted to happen. `s1`'s predicted finding (P-1c) is a
**gap in the repair's reach**, not a failure of the two sites it closed, and
it will be reported as such.
