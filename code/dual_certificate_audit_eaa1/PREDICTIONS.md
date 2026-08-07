# `mg-eaa1` — predictions for the INDEPENDENT AUDIT of `mg-131e`'s dual certificates

**Committed before any script of this audit exists, and before one byte of
`code/dual_certificate_131e/`, of `docs/` for `mg-131e`, or of `STATE.md` has been read.**

Parent under audit: `b7b6941` — *"finding+instrument+docs: THE <= DIRECTION IS CERTIFIED AT
n=3,4,5 AND IS FALSE AT n=6 — mg-200d's eps_spec = 2/(n+1) IS A SMALL-n COINCIDENCE, AND THE
ROUTE HAS NO TARGET TO PROVE (mg-131e)"*.

`STATE.md` as of this writing is at **`491d42c79f7628c18cb7a5d197faa9f4600cd6c1`** (`mg-b488`),
confirmed by `git log -1 -- STATE.md` in this worktree, and that is the SHA this audit will
name. I have **not** read the file yet.

---

## 0. DISCLOSURES — what I already knew before writing a single prediction

These are **hand measurements and prior exposure**, not predictions. They are listed here so
that no hit below can be sold as blind foresight. Several of this ticket's numbered checks are
already partly answered by my own dispatch prompt, and saying so is the point of this section.

**H1 — MY DISPATCH PROMPT CONTAINS THE PARENT'S HEADLINE.** The commit subject quoted above is
in the "recent activity" block of my prompt. So I already know, before reading anything, that
`mg-131e` claims (a) certificates at `n = 3,4,5` and (b) that the `<=` direction is **FALSE at
n = 6**. **This guts check 3 of my brief as written.** My brief instructs me to "extrapolate
the claimed pattern to n = 6, construct the predicted dual, and check it is feasible and
attains `(n-1)/3 = 5/3`". If the parent already reports the value at `n = 6` exceeds `5/3`,
then **no such dual exists and its absence is the parent's own result, not my refutation of
it.** I will still do an `n = 6` computation, but I will report it for what it is: an
independent check **of the refutation**, not an out-of-sample test of a pattern the parent
claims. I pre-commit to not dressing it up as the latter.

**H2 — THE PARENT'S OWN PREDICTIONS COMMIT IS ALSO IN MY PROMPT.** `e40e047`'s subject
discloses four things about the argument I am about to audit: that the **TRIVIAL** dual is
feasible in every branch at every `n` and discharges every branch with `|I| <= n-1` "as a proof
rather than a computation"; that it certifies the attaining branch at `n=3` and `n=4` and
**FAILS at n=5**; that an "active-pairs refinement" also fails at `n=5` by hand; and that `P8`
pre-commits the answer may be **NEITHER** of the ticket's two offered answers. So I know the
shape of the deliverable's argument, and my P3/P4/P6 below are **informed**, not blind.

**H3 — THE MAYOR'S DISPATCH NOTE TOLD ME THE n=6 OUTCOME A SECOND TIME.** It states that
"pm-onethird refuted 2/(n+1) at n=6 tonight and fixed mg-b488 before it could land a false
formula". So two independent channels reached me with the answer before I started.

**H4 — I READ `mg-200d`'s TRANSCRIPTS FIRST.** Before writing predictions I read
`code/perslot_symmetry_200d/out_v2_n34.txt` and `out_v2_n5.txt` in full. I therefore already
hold, by reading and not by computation: per-slot disjunctive values `2/3, 1, 4/3` at
`n = 3,4,5`; the attaining branches `{(0,2)}`, `{(0,2),(0,3),(1,3)}`,
`{(0,2),(0,3),(1,4),(2,4)}`; that the `n=5` attaining branch is **not** transitive; and the
three-atom `1/3`-each witnesses at each `n`. Any "reproduction" of those numbers below is a
**reproduction**, and I will label it so in the verdict.

**H5 — I READ THE PARENT-OF-PARENT'S SOLVER IN FULL.** `lp200d.py` (350 lines) and
`v2_disjunctive.py`, before predicting. I know the constraint system's exact shape: one
equality row `Σ μ = 1`; one `<= 1/3` cap row per **non-comparable** pair whose flipping-column
set is non-empty; and, per non-comparable pair `(x,y)` and per slot `k`, one equality row with
coefficient `[y before x at slot k] − [x before y at slot k]` and rhs `0`. Comparable pairs
carry **no** row at all and their flipping columns are **deleted from the variable set** before
the LP is built. This is what I will rebuild independently.

**H6 — HAND MEASUREMENT, DONE BEFORE PREDICTING.** In the `n=3` attaining branch
`comparable = {(0,2)}`, the surviving column set is exactly `{012, 021, 102}` — the three
permutations placing `0` before `2` — so that LP has **three variables**. Its dual is
correspondingly tiny and I expect to be able to check it by hand as well as by machine. The
objective is `(0+1+1)/3 = 2/3`, which is `(n-1)/3`. So P2 at `n=3` is close to a formality and
I say so rather than banking it.

**H7 — I HAVE NOT READ**, at prediction time: anything under `code/dual_certificate_131e/`,
any `docs/` file for `mg-131e`, `STATE.md`, or `mg-131e`'s merged diff. I have read the
**ticket body** `mg show mg-131e` in full, including all three addenda.

---

## 1. PREDICTIONS

### On the certificates themselves

**P1 (85%).** `code/dual_certificate_131e/` exists and contains `PREDICTIONS.md`, a `README.md`,
a solver/verifier module, and committed `out_*.txt` transcripts, matching this corpus's house
shape.

**P2 (80%).** Every dual certificate the parent publishes for `n = 3, 4, 5` verifies under **my
own independent substitution in exact rationals**: dual feasible on every column, and dual
objective exactly `(n-1)/3`. I am betting the certificates are *correct*; the audit's risk is
elsewhere.

**P3 (70%, INFORMED BY H2 — NOT BLIND).** At `n = 3` and `n = 4` the certificate is the
**trivial** dual: the value is reached from the cap rows and the normalisation alone, with
**zero** weight on any per-slot symmetry row.

**P4 (60%, INFORMED BY H2).** At `n = 5` the trivial dual does **not** attain, and the published
certificate there carries non-zero symmetry multipliers — or the parent reports that it could
not produce one of the same shape.

**P5 (90%).** The certified program is the **DISJUNCTIVE branch** program, not the literal
all-pairs program. Concretely I predict I will find, for each certified `n`: a non-empty
`comparable` set; the flipping columns of those pairs **absent** from the variable list; and a
**primal** feasible point in that same branch with objective exactly `(n-1)/3`. If the
certified program were the literal all-pairs one it would be **infeasible** (`mg-200d`'s
theorem) and its "dual certificate" would certify nothing — that is check 2 of my brief and the
cheapest way to fail it is not to look.

**P5a (95%).** If I find any certificate whose branch has `comparable = ∅` at `n >= 3`, that is
the literal program and I score check 2 **FAIL** regardless of how clean the arithmetic is.
Pre-committing the rule now so I cannot soften it later.

### On the verdict — the thing my brief says needs the most scrutiny

**P6 (75%, A REPRODUCTION, NOT A HIT — SEE H1/H2/H3).** The parent's verdict is **neither** of
the ticket's two offered answers. It is a third: the conjectured *value* `(n-1)/3` is **false at
n = 6**, so the question "are the multipliers n-indexed?" has no target — there is no identity
to prove for all `n`. I am recording this as a prediction only to date-stamp that I could not
have discovered it; I was told it twice.

**P7 (65%).** The `n = 6` refutation is carried by a **primal** object — one feasible point in
one legal branch with `E[inv] > 5/3` — and **not** by an exhaustive sweep of the 32768 branches.
A single feasible point is checkable by substitution, which is what makes the refutation cheap
and auditable; an exhaustive `n=6` run is what the ticket forbade.

**P8 (70%).** I independently construct, in exact rationals and from my own constraint builder,
a legal disjunctive branch at `n = 6` and a probability measure feasible in it with
`E[inv] > 5/3`. That is the whole refutation and it does not need the parent's code.

**P8a (40%).** The `n = 6` per-slot disjunctive value is `>= 2` (i.e. `eps_spec >= 12/35`, versus
the conjectured `2/7 = 10/35`). Lower confidence than P8 because I am predicting a *magnitude*,
not just a strict inequality.

**P8b (30%).** My independently-found `n = 6` witness has the same value as the parent's. Low,
because I expect to find *a* violating branch rather than *the* optimum, and because the
optimum over 32768 branches is exactly what neither of us is supposed to compute.

### On the four things that can go wrong in the writeup

**P9 (80%).** The writeup states its normalisation explicitly as **equality** `Σ μ = 1`, as the
19:12 addendum demanded, and the LP it actually ran uses `==` and not `<=`. I will check the
code, not the sentence.

**P10 (70%).** **No tightness claim has crept in.** No sentence asserts the bound is attained by
a real poset at `n = 4` or `n = 5`. `mg-200d`'s own transcript is careful here — at `n=4` it
prints "NOT in M_n" and at `n=5` it prints no realisability line at all because the branch is
not transitive — so the parent had a correct model in front of it.

**P11 (70%).** The `>=` / `<=` split survives: the writeup does not report "the value is
`(n-1)/3`" flat. Note this one is *helped* by the `n=6` refutation — once `<=` is false at
`n=6`, conflating the directions becomes hard to do accidentally.

**P12 (45%) — THE CONFLATION I AM ACTUALLY HUNTING.** At least one user-facing sentence (in the
deliverable, its commit subject, or `STATE.md`) fails to separate

  * **(A)** "the *disjunctive relaxation's* value exceeds `(n-1)/3` at `n = 6`" — established by
    one feasible point, and what the parent can have proved; from
  * **(B)** "`eps_spec <= 2/(n+1)` is **false**" — a statement about real posets in `M_n`, which
    a relaxation being loose can **never** establish.

The relaxation is an **upper** bound built on a branch family that is a strict **superset** of
real comparability patterns and imposes no transitivity. A superset relaxation failing to prove
a bound leaves the bound **open**, not false. `STATE.md`'s own landing subject at `491d42c`
reads *"eps_spec = 2/(n+1) IS ON THE PAGE AS FALSE"*, which is (B)-shaped wording for what can
only be an (A)-shaped result. **I am betting near-even that this is where the defect is, and I
am pre-committing to raise it even if every rational number in the deliverable checks out.**

**P13 (85%).** No poset enumeration, no transitivity imposed, anywhere in `mg-131e`'s code. The
one permitted use of a named relation (`uniform_le_measure`) is a *control*, and its appearance
is not a violation.

**P14 (60%).** `STATE.md` at `491d42c` carries the `n=6` refutation **at** the claim — in the
same row/paragraph a hostile reader meets `2/(n+1)`, not only in a later note. Read as a reader
who never saw the correction, per my dispatch.

### The two mistakes I am most likely to make

**P15 (35%) — MY MOST LIKELY ERROR: SCORING A SIGN CONVENTION AS MATHEMATICS.** I am building my
own constraint matrix. `lp200d.build` writes each symmetry row as `bwd − fwd = 0` and each cap
as `<= 1/3`; a dual for `max c'x, Ax <= b` has `y >= 0` on inequality rows and `y` **free** on
equality rows, with feasibility `A'y >= c`. If my row order, my row *signs*, or my free/sign
convention differs from the parent's serialisation, I will get a mismatch that is bookkeeping
and score it as a refuted certificate — or, worse, silently repair it and score a broken
certificate as a pass. **Guards, written down now so I cannot invent them afterwards:**
(i) I write my sign conventions into the verifier's docstring **before** opening the parent's
certificate format; (ii) I re-solve each branch's primal with my own solver and assert the
optimum equals `mg-200d`'s published value **and** the parent's claimed value, so the matrix is
validated before any dual touches it; (iii) if I must transform the parent's multipliers to
match my conventions, the transformation is printed explicitly in the transcript and the
untransformed vector is checked too; (iv) a **mutation control**: I perturb one multiplier and
assert the verifier reports infeasible, so a "PASS" cannot be a verifier that passes anything.

**P16 (30%) — THE SECOND ERROR: SCORING "TRIVIAL" AS "VACUOUS".** If the certificate at `n=3,4`
uses only cap rows and the normalisation, the temptation is to call it content-free. **It is
not.** A trivial dual that is genuinely feasible and attains the value is a *stronger* result
than a computed one — it is a proof for that branch at every `n`, which is precisely what H2
says the parent claims. I pre-commit: a verified trivial dual scores **PASS with a note**, never
a defect. The *separate* question — whether the trivial dual covers the branch that actually
**attains** the max, or only the easy branches — is the real one, and I will ask it explicitly.

**P17 (25%) — THE THIRD: AUDITING THE BRANCH BY ITS LABEL.** A disjunctive branch is legal only
if its comparable pairs really have `q = 0`, which `lp200d` achieves by **deleting columns**
before building rows, not by adding a constraint. If I verify only the rows I will pass a
certificate whose branch is mislabelled. **Guard, pre-committed:** for every branch I touch, my
checker asserts, for every declared-comparable pair `(i,j)` and every atom of positive mass,
that the atom does **not** flip `(i,j)` — and separately that no cap row and no symmetry row
was emitted for that pair.

---

## 2. WHAT THIS AUDIT WILL NOT DO

Pre-committed so the omissions are declared rather than discovered:

* **No exhaustive `n = 6` enumeration.** 32768 branches over 720 columns; the ticket forbade it
  and my brief says the cheap check is better. So I will be able to say the `n=6` value is
  `> 5/3` and I will **not** be able to say what it is.
* **No re-run of `mg-200d`'s `v2_disjunctive.py`.** My brief says a certificate is checkable in
  a way an LP run is not — so I check certificates. If my own solver disagrees with `mg-200d`'s
  published `n=3,4,5` values I will report the disagreement rather than resolve it.
* **No claim about realisability.** Nothing in this audit bears on whether any bound is attained
  by a poset in `M_n` at `n >= 4`, and I will not infer one from a dual.
* **No audit of `mg-76b2`'s `C_3 = 1`,** which the ticket's "what it would buy" paragraph leans
  on. Out of scope.

*Committed `2026-08-07` by `mg-eaa1` (polecat `aeaa1`), before any script of this audit exists.*
