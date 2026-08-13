"""d3 — the correction: the image DOES tighten, inside the cell, by exactly `d`.

THE CLAIM THIS ARM IS ABOUT is the one this work item carries in its own title:

    "The image characterisation is EXACT and therefore CANNOT TIGHTEN ANYTHING:
     conv(R_n) = M_n because the image contains every vertex, so every inequality
     valid on the image is valid on the whole body"

The clause before the colon does not follow from the clause after it, and the counter-measurement
is in `mg-c776`'s OWN instrument, one section past the one the title paraphrases.  Both readings
are reproduced here, side by side, on independent code:

  READING A -- global, and the hypothesis read on the POSET.  `conv(R_n) = M_n`, `conv(R_n ∩ H)
  = M_n`, no inequality separates, ratio `1`.  TRUE, and `d1` re-proves it.

  READING B -- inside the convex cell of hypothesis (1) read on the MEASURE.  The image reaches
  a `d`-fraction of the ceiling and no more, where `d = m/C(n,2)` is the incomparability density.
  `mg-c776` `c2.4` measures ratios `2/3, 1/3, 1/5, 4/15` at `n = 3..6`.  That is a REAL
  tightening -- at `n = 5` the image ceiling is a FIFTH of the body's -- and "cannot tighten
  anything" is reading A stated without reading B beside it.

WHAT SEPARATES THE TWO IS `d1.4`'s dividing line and nothing else.  Reading A's hypothesis
excludes no vertex of `M_n` (a total order's `delta` is a maximum over the empty set), so the
hull is the whole body.  Reading B's excludes `n! - 1` of them, leaving `delta_id`, so the hull
is a proper subset and a linear ceiling over it can be -- and is -- strictly smaller.

THE CORRECTION IS TO THE PARAPHRASE AND NOT TO THE DELIVERABLE.  `code/image_geometry_c776/`
`README.md` §1 already states the careful version -- *"no fact about the image can move `eps`
except through `d`"* -- and the deliverable's §3 prints the `c2.4` table under the heading
*"Where the comparison is NOT vacuous"*.  What travelled into the work item title, and from
there into anything a dispatcher reads, was the half without the qualifier.

AND THE TIGHTENING IS NOT AN OPENING, WHICH IS WHY THIS IS A CORRECTION AND NOT A REOPENING.
The factor is `d`, so the image converts row 8's wall into *how large can `d` be for a FROZEN
poset* -- which is residual **(R)**, already on `STATE.md`'s board, already ordered, and whose
own `STATE.md` §6 entry records that a search for a frozen-conditional upper bound on `d`
returns zero.  The line does not die; it lands on a residual that was already there.
"""

from fractions import Fraction

import lib3da1 as L

FAIL = []
THIRD = Fraction(1, 3)


def check(ok, name, detail):
    print(f"  [{'GREEN' if ok else 'RED  '}] {name}")
    for line in detail.split("\n"):
        print(f"       {line}")
    if not ok:
        FAIL.append(name)


def head(t):
    print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


def in_cell(pi, n):
    """The cell of hypothesis (1) with L* = identity: every pair flipped at most 1/3, i.e.
    P(j before i) <= 1/3 for i < j."""
    return all(1 - pi[(i, j)] <= THIRD for (i, j) in L.pairs(n))


# ---------------------------------------------------------------------------------------
head("d3.1  the population restriction is DERIVED, and checked against the full population")

# An image point in the cell cannot have a comparable pair oriented the wrong way: if j < i in
# P then pi[(i,j)] = 0, so the flip 1 - 0 = 1 exceeds 1/3.  So only subrelations of the identity
# chain can contribute, and enumerate_chain_subposets is exact rather than a sample.
rows = []
for n in (3, 4, 5):
    U = L.all_perms(n)
    full = [(P, L.uniform_image(P, n, U)[0]) for P in L.enumerate_posets(n)]
    from_full = {P for P, pi in full if in_cell(pi, n)}
    chain = {P for P in L.enumerate_chain_subposets(n)}
    rows.append((n, len(full), len(chain), len(from_full), from_full <= chain))
print("   n | all posets | chain subposets | image points IN the cell | cell set inside chain set")
print("  ---+------------+-----------------+--------------------------+--------------------------")
for n, a, c, f, ok in rows:
    print(f"   {n} | {a:10d} | {c:15d} | {f:24d} | {ok}")
check(all(ok for *_, ok in rows),
      "every poset whose image lies in the cell is a subrelation of the identity chain",
      "Checked exhaustively against the FULL labelled population at n = 3,4,5, where both\n"
      "routes are affordable.  The restriction is what makes n = 6 reachable (2^15 candidates\n"
      "instead of 3^15) and it is exact, not a sample: a comparable pair the other way puts a\n"
      "coordinate at 0, whose flip is 1, and the cell allows at most 1/3.")

# ---------------------------------------------------------------------------------------
head("d3.2  the ceiling on the cell — C(n,2)/3, attained by the two-atom law")

rows = []
for n in (3, 4, 5, 6):
    ceiling = Fraction(len(L.pairs(n)), 3)
    rev = tuple(reversed(range(n)))
    two_atom = L.marginal([(tuple(range(n)), Fraction(2, 3)), (rev, Fraction(1, 3))], n)
    rows.append((n, ceiling, L.inv_e(two_atom, n), in_cell(two_atom, n)))
print("   n | C(n,2)/3 | E[inv_e] at (2/3)delta_id + (1/3)delta_rev | in the cell")
print("  ---+----------+--------------------------------------------+------------")
for n, c, v, ok in rows:
    print(f"   {n} | {L.fmt(c):8s} | {L.fmt(v):42s} | {ok}")
check(all(c == v and ok for _, c, v, ok in rows),
      "the cell ceiling is C(n,2)/3 and the two-atom law attains it, at n = 3..6",
      "Every coordinate's flip is capped at 1/3 by the cell and the two-atom law sits at exactly\n"
      "1/3 on all C(n,2) of them, so the bound is ATTAINED and not merely valid.  This is the\n"
      "point mg-6bc2 Claim 3.1 / mg-0fc6 a3.3 carry for all n; it is rebuilt here so the ratio\n"
      "below is this instrument's own quotient rather than two instruments' numbers divided.")

# ---------------------------------------------------------------------------------------
head("d3.3  THE IMAGE INSIDE THE CELL — mg-c776 c2.4's table, independently reproduced")

print("   n | ceiling on K | best image point in K | ratio  | m  | d = m/C(n,2) | e(P)")
print("  ---+--------------+-----------------------+--------+----+--------------+------")
table = []
for n in (3, 4, 5, 6):
    U = L.all_perms(n)
    ceiling = Fraction(len(L.pairs(n)), 3)
    best, arg, arg_e = Fraction(-1), None, None
    for P in L.enumerate_chain_subposets(n):
        pi, ext = L.uniform_image(P, n, U)
        if not in_cell(pi, n):
            continue
        v = L.inv_e(pi, n)
        if v > best:
            best, arg, arg_e = v, P, len(ext)
    d, m = L.density(arg, n)
    ratio = best / ceiling
    table.append((n, ceiling, best, ratio, m, d, arg_e))
    print(f"   {n} | {L.fmt(ceiling):12s} | {L.fmt(best):21s} | {L.fmt(ratio):6s} | "
          f"{m:2d} | {L.fmt(d):12s} | {arg_e}")

expected_ratio = [Fraction(2, 3), Fraction(1, 3), Fraction(1, 5), Fraction(4, 15)]
expected_best = [Fraction(2, 3), Fraction(2, 3), Fraction(2, 3), Fraction(4, 3)]
check([t[3] for t in table] == expected_ratio and [t[2] for t in table] == expected_best,
      "the ratios are 2/3, 1/3, 1/5, 4/15 and the maxima 2/3, 2/3, 2/3, 4/3 — term for term",
      "mg-c776 c2.4's table, reproduced from an independent poset enumerator, an independent\n"
      "linear-extension routine and an independent marginal.  THE IMAGE CEILING IS STRICTLY\n"
      "BELOW THE BODY'S at every n here, and at n = 5 it is a FIFTH of it.")

check(all(ratio == d for _, _, _, ratio, _, d, _ in table),
      "AND THE RATIO IS EXACTLY d, the incomparability density — an identity, not a fit",
      "The maximiser sits at flip exactly 1/3 on each of its m incomparable pairs and at 0 on\n"
      "the rest, so its E[inv_e] is m/3 and the quotient with C(n,2)/3 is m/C(n,2) = d.  Both\n"
      "sides are exact rationals and they agree as rationals, at every n measured.")

check(all(best == Fraction(m, 3) for _, _, best, _, m, _, _ in table),
      "the maximum is m/3 exactly, so the whole cell reading is carried by ONE number, m",
      "That is what makes the tightening a REDUCTION rather than an improvement: it converts\n"
      "row 8's question into 'how large can m be for a frozen poset', which is residual (R).\n"
      "F23 (mg-6ff4) is the same statement from the boundary side -- every member of the\n"
      "boundary class has every incomparable pair at flip exactly 1/3, so eps_spec = d*n/(n+1)\n"
      "EXACTLY, the supply bound attained with zero slack.")

# ---------------------------------------------------------------------------------------
head("d3.4  THE TWO READINGS, SIDE BY SIDE — and which one the work-item title carries")

n = 5
U = L.all_perms(n)
V = L.vertices(n)
R = [L.uniform_image(P, n, U)[0] for P in L.enumerate_posets(n)]
c_worst = {p: -1 for p in L.pairs(n)}        # maximised by E[inv_e], i.e. the reversal vertex
global_body = max(L.inv_e(v, n) for v in V)
global_image = max(L.inv_e(pi, n) for pi in R)
cell_body = Fraction(len(L.pairs(n)), 3)
cell_image = [t[2] for t in table if t[0] == n][0]

print(f"   at n = {n}:\n")
print("   reading                                          | body ceiling | image ceiling | ratio")
print("  --------------------------------------------------+--------------+---------------+-------")
print(f"   A  global, hypothesis (1) read on the POSET      | {L.fmt(global_body):12s} | "
      f"{L.fmt(global_image):13s} | {L.fmt(global_image / global_body)}")
print(f"   B  inside the cell, read on the MEASURE          | {L.fmt(cell_body):12s} | "
      f"{L.fmt(cell_image):13s} | {L.fmt(cell_image / cell_body)}")

check(global_image == global_body and cell_image < cell_body,
      "reading A gives ratio 1 and reading B gives ratio 1/5 — BOTH are correct",
      "Reading A is the work item's title and it is true: the image reaches the body's ceiling\n"
      "exactly, because the reversal vertex IS an image point.  Reading B is mg-c776 c2.4 and\n"
      "it is also true.  `CANNOT TIGHTEN ANYTHING` is reading A carrying reading B's absence,\n"
      "and the fix is one clause: no inequality separates the image, AND restricting to it\n"
      "inside the cell buys exactly the factor d.\n"
      "WHAT IS ACTUALLY CLOSED is the shape mg-c776's ticket ranked first -- a CUT, hence any\n"
      "LP/SDP/lift-and-project route.  That closure is exact and d1 generalises it to every\n"
      "realizability restriction there will ever be.  What is NOT closed is d, and d is (R).")

print("\nRESULT: " + ("GREEN — all checks passed" if not FAIL else f"RED — {FAIL}"))
raise SystemExit(1 if FAIL else 0)
