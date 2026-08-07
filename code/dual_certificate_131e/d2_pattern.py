"""mg-131e D2 -- ARE THE MULTIPLIERS n-INDEXED OR AD HOC?  The question the ticket exists for.

D1 produces the certificates.  This script answers what they are worth, in three parts.

PART A -- the piece that IS n-indexed, and it is a theorem, not a fit.
    The trivial dual (lambda = 0, t = 1 on every cap row, s = 0) is dual-feasible in EVERY
    branch at EVERY n, with bound `|I_active|/3`.  On the branch `I = {(i,i+1)}` there are
    exactly `n-1` cap rows, so the bound is exactly `(n-1)/3`; and mg-200d's 3-atom fence
    attains it.  Hence

        THEOREM.  On the branch I = {consecutive pairs}, val = (n-1)/3 EXACTLY, every n.

    Both directions, no solver on either side.  This is checked here at n = 3..8 by building
    mg-200d's own rows and running the arithmetic verifier against them.

PART B -- the piece that is NOT, and why three points cannot say otherwise.
    A branch needs a non-trivial multiplier exactly when `|I_active| > n-1`.  Among branches
    that are primal-FEASIBLE -- the only ones where a certificate certifies anything -- there
    are ZERO such branches at n = 3, ZERO at n = 4, and TWO at n = 5.  So the phenomenon the
    ticket asks about first occurs at n = 5 and the evidence for a pattern in n is ONE point.
    Predicted in advance as P8.

PART C -- and on that one point the natural n-indexed guess is PROVABLY unavailable.
    On the two hard branches the whole dual OPTIMAL FACE has `lambda <= -1`.  So no certificate
    of the shape "lambda = 0, t an indicator vector" exists there at all -- not merely "I did
    not find one".  The face extremes are computed here, per multiplier.

Nothing in this file is evidence for the conjecture.  D3 refutes it at n = 6.
"""

import sys
import time
from fractions import Fraction as F

from lib131e import (Infeasible, active_pairs, all_branches, branch_class, branch_lp,
                     branch_columns, consecutive_pairs, incomparable, row_kind, solve_dual,
                     trivial_dual, verify_dual)
from lp200d import flips as _flips
from lp200d import inv_count, measure_report, pairs_of, solve_max
from lib131e import _dual_rows, _expand, _objective_row, _split_layout,\
    cap_pairs_of_branch

NS = [int(a) for a in sys.argv[1:]] or [3, 4, 5]


def fence_atoms(n):
    """mg-200d's 3-atom lower-bound construction, copied so PART A needs no import of v3."""
    atoms = {tuple(range(n)): F(1, 3)}
    for r in (0, 1):
        p = list(range(n))
        for i in range(r, n - 1, 2):
            p[i], p[i + 1] = p[i + 1], p[i]
        atoms[tuple(p)] = atoms.get(tuple(p), F(0)) + F(1, 3)
    return atoms


# ------------------------------------------------------------------------------- PART A

print("=" * 84)
print("PART A  THE n-INDEXED PIECE.  On the branch I = {consecutive pairs}, the TRIVIAL dual")
print("        gives exactly (n-1)/3 and mg-200d's fence attains it -- so val = (n-1)/3 there")
print("        EXACTLY, at every n, with a solver on neither side.")
print("=" * 84)

allA = True
for n in range(3, 9):   # n = 9 already enumerates 9! columns; the STATEMENT is a proof,
    #                    this loop is only its illustration, so it stops where it stops
    cons = consecutive_pairs(n)
    C = frozenset(pr for pr in pairs_of(n) if pr not in cons)
    perms, rows, c = branch_lp(n, C)
    y = trivial_dual(rows)
    chk = verify_dual(rows, c, y)
    ncap = sum(1 for r in rows if row_kind(r) == "cap")
    mu = fence_atoms(n)
    rep = measure_report(n, mu)
    # the lower bound's own feasibility, written out rather than trusted
    flipped = set()
    for p in mu:
        flipped |= _flips(p)
    lower_ok = (rep["mass"] == 1
                and rep["max_flip"] <= F(1, 3)
                and not (flipped & C)
                and not [v for v in rep["slot_eq_violations"] if v[0] in set(cons)])
    ok = (chk.ok and ncap == n - 1 and chk.bound == F(n - 1, 3)
          and lower_ok and rep["E_inv"] == F(n - 1, 3))
    allA = allA and ok
    print(f"  n={n:>2}  cap rows = {ncap} (= n-1: {ncap == n - 1})   trivial-dual bound = "
          f"{str(chk.bound):>6} (verified: {chk.ok})   fence E[inv] = {str(rep['E_inv']):>6}"
          f"  feasible-there: {lower_ok}   -> upper == lower: {'YES' if ok else 'NO'}")
print(f"  ==> val = (n-1)/3 on the consecutive-pairs branch at every n in 3..8: "
      f"{'HOLDS' if allA else 'FAILS'}")
print("      This is n-INDEXED and it is a proof.  It is also about ONE branch out of")
print("      2^C(n,2), and the `<=` direction is a statement about ALL of them.")


# ------------------------------------------------------------------------------- PART B

print()
print("=" * 84)
print("PART B  WHEN IS A NON-TRIVIAL MULTIPLIER NEEDED AT ALL?  Only when |I_active| > n-1.")
print("        Counted separately for FEASIBLE branches (informative) and INFEASIBLE ones")
print("        (vacuous -- a bound on a maximum over the empty set).  PREDICTIONS P12.")
print("=" * 84)

hard_by_n = {}
for n in NS:
    t0 = time.time()
    tot = need = feas_need = infeas_need = 0
    hard = []
    for C in all_branches(n):
        tot += 1
        perms, rows, c = branch_lp(n, C)
        chk = verify_dual(rows, c, trivial_dual(rows))
        assert chk.ok
        if chk.bound <= F(n - 1, 3):
            continue
        need += 1
        kind, val, _ = branch_class(n, C)
        if kind in ("zero", "positive"):
            feas_need += 1
            hard.append((sorted(C), kind, val, chk.bound))
        else:
            infeas_need += 1
    hard_by_n[n] = hard
    print(f"  n={n}: {tot} branches; {need} need more than the trivial dual"
          f"  ({infeas_need} on INFEASIBLE branches = vacuous,"
          f"   {feas_need} on FEASIBLE branches = informative)   [{time.time() - t0:.1f}s]")
    for row in hard:
        print(f"        informative hard branch: C={row[0]}  {row[1]}  val={row[2]}"
              f"  trivial bound={row[3]}")
    sys.stdout.flush()

print()
print("=" * 84)
print("PART B2  THE MECHANISM n <= 5 CANNOT SHOW.  At every value-positive branch, does the")
print("         optimum flip any NON-CONSECUTIVE pair?  If it never does, the value is")
print("         capped by the n-1 consecutive pairs for a reason n <= 5 makes invisible --")
print("         and D3's n = 6 refutation is exactly a branch where one finally can.")
print("=" * 84)

for n in NS:
    t0 = time.time()
    pos = nonc = 0
    for C in all_branches(n):
        kind, val, mu = branch_class(n, C)
        if kind != "positive":
            continue
        pos += 1
        q = {}
        for p, w in mu.items():
            for pr in _flips(p):
                q[pr] = q.get(pr, F(0)) + w
        if any(v for pr, v in q.items() if pr[1] != pr[0] + 1):
            nonc += 1
    print(f"  n={n}: {pos} value-positive branches; {nonc} of them have an optimum that flips"
          f" a NON-CONSECUTIVE pair   [{time.time() - t0:.1f}s]")
    sys.stdout.flush()
print("  (the optimum reported is one vertex of the optimal face, so `0` means `no reported")
print("   optimum does`, not `no optimal measure can`.  It is still the thing that changes")
print("   at n = 6, where q on a non-consecutive pair is 1/6 and IS the whole excess.)")

print()
print("  cross-n availability of the thing a pattern would have to be fitted to:")
for n in NS:
    print(f"      n={n}: {len(hard_by_n[n])} informative hard branches")
print("  A pattern in n cannot be read off from a sequence that is 0, 0, k.  Whatever the")
print("  multipliers on the n = 5 hard branches look like, there is no n = 3 or n = 4")
print("  instance of the same object to compare them against.  This is P8, pre-committed.")


# ------------------------------------------------------------------------------- PART C

print()
print("=" * 84)
print("PART C  ON THAT ONE POINT, THE NATURAL n-INDEXED GUESS IS PROVABLY UNAVAILABLE.")
print("        Range of each multiplier over the whole dual OPTIMAL FACE, by LP.  A range")
print("        that excludes 0 is a shape no certificate at that branch can have.")
print("=" * 84)

BOX = F(1000)


def face_range(n, C, i):
    """[min, max] of multiplier i over {dual feasible, objective <= val(C)}, boxed at +-BOX."""
    perms, rows, c = branch_lp(n, C)
    kind, val, _ = branch_class(n, C)
    idx, nv = _split_layout(rows)
    drows = _dual_rows(rows, c, idx, nv)
    ocoef, oconst = _objective_row(rows, idx, nv)
    drows.append((ocoef, "<=", F(val) - oconst))
    for k in range(len(rows)):
        _, base = idx[k]
        drows.append(({base: F(1)}, "<=", BOX))
        if idx[k][0] == "f":
            drows.append(({base + 1: F(1)}, "<=", BOX))
    out = []
    for sign in (F(1), F(-1)):
        obj = [F(0)] * nv
        for k, v in _expand(idx, i, sign).items():
            obj[k] += v
        v, _x = solve_max(nv, drows, obj)
        out.append(sign * v)
    return out[1], out[0]


def cap_pairs(n, C):
    return cap_pairs_of_branch(n, C)


for n in NS:
    for C, kind, val, tb in hard_by_n[n]:
        Cf = frozenset(tuple(x) for x in C)
        perms, rows, c = branch_lp(n, Cf)
        caps = cap_pairs(n, Cf)
        print(f"\n  n={n}  hard branch C={C}   val={val}   trivial bound={tb}")
        ci = 0
        for i, r in enumerate(rows):
            lo, hi = face_range(n, Cf, i)
            if i == 0:
                lab = "lambda  (sum mu = 1)"
            elif row_kind(r) == "cap":
                lab = f"t{caps[ci]}"
                ci += 1
            else:
                lab = "s (per-slot symmetry)"
            note = ""
            if i == 0 and hi < 0:
                note = "   <-- lambda < 0 ON THE WHOLE FACE: NO certificate here has lambda = 0"
            if row_kind(r) == "cap" and lo == 0 and hi == 0:
                note = "   <-- forced to 0"
            print(f"      {lab:24s} range [{str(lo):>10}, {str(hi):>10}]"
                  f"{'  (boxed)' if abs(lo) == BOX or abs(hi) == BOX else ''}{note}")

print()
print("=" * 84)
print("VERDICT.  Neither of the ticket's two offered answers is the whole truth, and saying")
print("so is the point of PART B:")
print()
print("  * There IS an n-indexed dual, it is a proof at every n, and it settles the")
print("    consecutive-pairs branch exactly (PART A).  That much of the route is real.")
print("  * The `<=` direction is about ALL branches, and the branches where that dual is not")
print("    enough are, among the FEASIBLE ones, absent at n = 3 and n = 4 and present at")
print("    n = 5.  One point.  No pattern in n is fittable, in either direction (PART B).")
print("  * At that one point, the shape a pattern would have to take is excluded outright:")
print("    lambda is strictly negative across the entire dual optimal face (PART C).")
print()
print("So this instrument does not report `n-indexed` and does not report `ad hoc`.  It")
print("reports that the certificates at n = 3 and n = 4 are nearly content-free and that")
print("n = 5 is a single data point -- and then D3 settles the underlying question directly,")
print("by refuting the conjecture at n = 6.")
print("=" * 84)
