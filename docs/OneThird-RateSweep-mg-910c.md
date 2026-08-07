# The `Θ(n²) → Θ(n)` RATE sweep — `mg-372e` swept the formula, this sweeps the rate

`mg-910c` · instrument [`code/rate_sweep_910c/`](../code/rate_sweep_910c/) ·
subject `mg-00a1` ([`OneThird-GrowthRate-mg-00a1.md`](OneThird-GrowthRate-mg-00a1.md)) ·
predecessor `mg-372e` (`dafe759`)

---

## 0. The count, first

> **26 sites classified. 19 LIVE and repaired. 7 left, each named with its reason.**
> Plus **104 line-hits across 32 files** reached only by the deliberately over-wide collision
> nets, all left, and the generated twin `docs/state-of-the-wall.html` checked and **clean**.

| class | n | disposition |
|---|---|---|
| **LIVE** — asserted as current | **9** | struck in place, `mg-00a1` cited beside each |
| **LIVE-OPEN** — asserted as an *open question* | **10** | struck in place; the question is closed, not open |
| **CITED** — already named as refuted, or inside a strike that says so | 3 | LEFT |
| **SURVIVES** — a correct `Θ(n)` statement about ONE branch | 2 | LEFT, and protected |
| **COLLISION** — `Θ(n²)`/`Θ(n)`, a different quantity | 2 listed (+32 files) | LEFT, and said so |

Every row is in [`code/rate_sweep_910c/r2_classify.py`](../code/rate_sweep_910c/r2_classify.py)
with its anchor text, the pattern that found it (or `-` if reading found it), and its reason.
`r2` **checks** the 19; `r3` runs it against the unrepaired tree at `main` and confirms all 19
were unmarked there and all 7 were already fine.

**Files repaired — four:**

| file | sites |
|---|---|
| `docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md` | 10 (of 14 classified) |
| `docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md` | 4 (of 6) |
| `docs/OneThird-DualCertificate-mg-131e.md` | 2 (of 3) |
| `code/dual_certificate_131e/d3_refutation.py` | 1 (docstring; output byte-identical after) |

---

## 1. What is now on the page

`mg-00a1` proved the disjunctive per-slot value is **`Θ(n²)`, SUPERLINEAR**. So:

* `mg-200d`'s `§0` HEADLINE — *"per-slot adjacency symmetry buys a factor that grows with `n`,
  not a constant"* — is **REFUTED**. What it buys is a **constant factor of at most `6`**.
* `mg-131e`'s `§5` item 2 — *"`mg-200d`'s `Θ(n²) → Θ(n)` headline is not refuted"* — is
  **FALSE**, and the caveat it attached to itself is what came true.
* The rate is **not unknown**. Ten sites said it was; that is the second-largest class here.

None of that is re-derived. `mg-00a1`'s construction is cited and not restated, per the ticket.

---

## 2. Why `mg-372e` did not catch this, and why that is not a criticism

`mg-372e` swept `ε_spec = 2/(n+1)` — the **FORMULA** — and swept it well: 13 LIVE sites struck
across two documents, and it named the `COLLISION` class that saved three more. It could not
have caught the rate:

1. **The rate is a different string.** A document can carry a correct strike of the formula and
   assert the rate one paragraph later. `mg-6bc2` and `mg-200d` both do.
2. **It ran before `mg-00a1` returned.** At that moment the rate was *"three points and no
   proof"* — thin, but not false. `mg-372e` said exactly that and left the headline standing
   **deliberately**, recording the decision in its banner. On its evidence that was right.

`mg-372e`'s own sweep still **PASSES** unchanged against every strike made here, and its four
negative controls still fire as pre-declared. Checked, not assumed.

**The one thing that has gone stale in it** is its `s2` allowlist entry *"the headline left"*,
which the README above it classes as *"true as written"*. It is no longer true as written. That
instrument is **not** edited and its outputs are **not** regenerated — the decision it records
was correct when made — and a section in
[`code/eps_spec_sweep_372e/README.md`](../code/eps_spec_sweep_372e/README.md) now says so.

---

## 3. The trap, and the two classes that exist because of it

**`Θ(n²)` is the correct answer for several other things in this corpus, including
`mg-00a1`'s own new theorem.** A sweep on the string would have struck the result that
motivated the sweep. Left, deliberately, and named:

* the baseline `C(n,2)/3 = n(n−1)/6`;
* the **two-atom law**'s `Θ(n²)` inversions (obstruction 4, `STATE.md:135`, and the one hit in
  the HTML twin);
* `(LIB-const)`'s `Θ(n²)` against `(LIB)`'s `O(n)` in `Operative-Form`;
* an inversion **radius**;
* the Hodge side's `2^{Θ(n)}` headline — 6 files;
* `LIBweak`'s `Θ(n)`-mobility configurations — 9 files.

**And two `Θ(n)` statements about the per-slot value itself are CORRECT and must not be
struck.** Both are about **one branch**, and a max-over-all-branches result does not touch them:

* `mg-131e` §2's **consecutive-pairs branch theorem**: `val = (n−1)/3` **exactly**, every `n`,
  both directions, no solver.
* the `(5n−8)/12` **chord sub-family**.

The strikes below them say so in as many words, because the risk after a refutation this loud is
a reader taking it further than it goes.

---

## 4. What the sweep does not touch

* **`STATE.md`.** It carries the rate at `:167` and `:168`. `mg-bb87` owns those sites and is
  held behind another `STATE.md` writer. Counted by `r1`, not listed by `r2`, not edited.
* **`docs/state-of-the-wall.html`.** Checked, as the ticket required. It is a **2026-07-19**
  rendering that predates `mg-200d` entirely, it already carries its own staleness banner, and
  it carries **no per-slot rate claim at all** — its single `Θ(n²)` is the two-atom law.
  **0 LIVE sites.**
* **The frozen-poset conjecture, and `mg-131e`'s refutation of the formula.** Untouched. The
  disjunctive value is an *upper bound* on the conjecture; this is that upper bound getting
  worse, which says nothing about the statement underneath.
* **The mathematics.** Not audited and not re-derived, per the ticket.

---

## 5. Three controls failed on first run, against code written minutes earlier

Reported because a sweep whose controls all passed first time has not been tested.

* **`N3` did not fire.** The plant writes each half of the rate in its own code span —
  `` `Theta( n^2 )` to `Theta(n)` `` — and the first `ARROW` pattern required *whitespace*
  between the halves, so backticks defeated it. **This is the `mg-7085` hazard, and it fired
  against this sweep's own instrument before it could fire against a document.** Widening the
  pattern then found **one further real site** on `main` — `mg-200d:60`, written
  `` from `Θ(n²)` to `Θ(n)` `` — which the first pattern returned a clean zero on. Reading had
  already found it; the control proved the grep had not.
* **`N0` found 7 unrepaired sites on `main`, not 19.** The detector accepted `mg-00a1` *or*
  `mg-910c` as the citation — and `mg-372e`'s strikes **already cite `mg-00a1`, as the open
  question.** Citing `mg-00a1` is what a `LIVE-OPEN` defect *does*; it is not evidence of
  repair. That is this ticket's whole thesis, arriving as a bug in its own detector.
* **`N2` destroyed 13 of its own 26 anchors** by stripping every marker word, `Θ(n²)` included,
  which is *in* the anchors. A mutation that deletes what it is measuring is not a control.

**Four sites were not reachable by any pattern and were found by reading** — three table cells
and strike-notes reading `unknown`, and one presupposition whose own content is true and whose
implied contrast is now false (`mg-6bc2`'s *"does not move `E[inv_e]` out of `Θ(n²)`"*, which is
correct about the **aggregate** form and misleads about the per-slot one). They are in the table
with pattern `-`. That is the honest form of *"grep is not enough"*.

`r2`'s check, stated at the strength it has, is *"`mg-910c` touched this block and said
something in it was wrong"*. The substance is the classification table, not the regex, and the
table is written out per row so it can be disagreed with per row.
