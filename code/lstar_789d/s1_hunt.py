"""s1 -- THE HUNT.  Outcome (b) is worth as much as outcome (a), so it is attacked first.

THE SCALAR THIS SCRIPT COMPUTES.  Write

    v_F(P) = M^2 / (2 gamma)          -- (F) FAILS  iff  v_F > 1
    v_L(P) = mu_pref * Delta / gamma  -- (L*)'s CONCLUSION FAILS iff v_L > 1

then (L*) is exactly the statement that no poset has both above 1, i.e.

    LSTAR(n) := max over primitive P on [n] of  min(v_F, v_L)   <=  1.

LSTAR(n) is to (L*) what c_or(n) is to the disjunction: one number per n whose crossing
of 1 is the whole event.  Nothing in the corpus has computed it.

WHERE THE HUNT IS AIMED, AND WHY THERE.  (L*) rearranges to

    Delta_P * (rho_P - 1)  <=  1 - Delta_P  =  min_i (S_P)_ii ,

so the room it leaves shrinks to nothing as the least-pinned element becomes free.  The
(F)-failing posets are exactly the ones with a thin cut between two internally-mixing
blocks, and those drive Delta -> 1.  So the hunt maximises v_L on the (F)-failing set,
which is the same thing as asking: can rho - 1 outrun min_i (S_P)_ii?

WHY THE SCREEN CANNOT HIDE A COUNTEREXAMPLE.  Posets are scored with mu_ub >= mu_pref,
an EXHIBITED nonincreasing f.  So v_L^ub >= v_L, and every genuine counterexample scores
above 1 on the screen.  A screen that can only OVER-state the hunted quantity cannot
lose it.  (This is the direction repaired in lib789d.mu_ub_float -- see its docstring.)

THE LABELLING IS PART OF THE DATA.  The population is NATURALLY LABELLED posets, and
gamma, Delta, M and mu_pref all move when the labelling moves, because A_P couples
element index to position index.  So the hunt's move set includes label transpositions,
not only cover relations.  That is a whole coordinate the family studies never varied.
"""

import sys, time, random
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lib789d import (P789, gen_posets, height, relabel_natural,
                     fam_chain_plus_points, fam_bipartite_minus, fam_blocks)

random.seed(20260810)


def score(P):
    g = P.gamma_float()
    if g <= 1e-13:
        return None
    M = float(P.M())
    D = float(P.Delta())
    mu = P.mu_ub_float()[0]
    if mu == float("inf"):
        return None
    vF = M * M / (2.0 * g)
    vL = mu * D / g
    return dict(gamma=g, M=M, Delta=D, mu=mu, vF=vF, vL=vL, J=min(vF, vL))


# =============================================================================
print("=" * 78)
print("S1.1  LSTAR(n) EXHAUSTIVELY, n = 3..7")
print("=" * 78)
print("  n | primitive |  LSTAR(n)  | argmax dn                    |   v_F     v_L")
sys.stdout.flush()
for n in (3, 4, 5, 6, 7):
    t0 = time.time()
    best, arg, bs, ct = -1.0, None, None, 0
    for dn in gen_posets(n):
        P = P789(dn, n)
        if not P.primitive():
            continue
        ct += 1
        s = score(P)
        if s is None:
            continue
        if s["J"] > best:
            best, arg, bs = s["J"], dn, s
    print("  %d | %9d | %10.6f | %-28s | %.5f %.5f   (%.0fs)"
          % (n, ct, best, str(arg), bs["vF"], bs["vL"], time.time() - t0))
    sys.stdout.flush()

# =============================================================================
print()
print("=" * 78)
print("S1.2  THE TWO MECHANISMS, AND WHETHER THEY COMBINE")
print("=" * 78)
print("""
  (F) failing and rho > 1 come from OPPOSITE structures, and that -- not any scalar
  inequality -- is what (L*) is about.

    mechanism (F)-fail : a THIN CUT between two internally-mixing blocks.  1 - Delta is
                         then about 1/b with b the larger block, so the room (L*) leaves
                         for rho - 1 SHRINKS like 1/n.
    mechanism rho > 1  : a FREE element whose natural LABEL disagrees with where the
                         Fiedler vector wants it (chain + point).

  A route to a counterexample has to run both at once.  Every combination the families
  allow is run below.
""")
rows = []

print("  A. near-complete bipartite K_{a,b} minus one relation  (the (F)-fail mechanism)")
print("     a  b |  n | gamma    | Delta   |   M     | v_F     | rho     | v_L")
for a in range(2, 8):
    for b in range(2, 8):
        if a + b > 13:
            continue
        dn, n = fam_bipartite_minus(a, b, [(a - 1, b - 1)])
        P = P789(dn, n)
        if not P.primitive():
            continue
        s = score(P)
        if s is None:
            continue
        print("     %d  %d | %2d | %.6f | %.5f | %.5f | %.5f | %.5f | %.5f"
              % (a, b, n, s["gamma"], s["Delta"], s["M"], s["vF"], s["mu"] / s["gamma"], s["vL"]))
        rows.append((s["J"], dn, n, "bip"))
sys.stdout.flush()


def bip_plus_points(a, b, drops, p, ptlabels=None):
    """K_{a,b} minus `drops`, plus p free points.  `ptlabels` lets the free points be
    labelled anywhere in the natural order -- the coordinate the families never varied."""
    n = a + b + p
    ds = set(drops)
    rel = [0] * n
    for j in range(b):
        m = 0
        for i in range(a):
            if (i, j) not in ds:
                m |= 1 << i
        rel[a + j] = m
    dn = relabel_natural(rel, n)
    return dn, n


print()
print("  B. K_{a,b} minus one relation PLUS p free points  (both mechanisms at once)")
print("     a  b  p |  n | v_F     | rho     | Delta   | v_L")
for a in range(3, 7):
    for b in range(3, 7):
        for p in (1, 2):
            if a + b + p > 13:
                continue
            dn, n = bip_plus_points(a, b, [(a - 1, b - 1)], p)
            P = P789(dn, n)
            if not P.primitive():
                continue
            s = score(P)
            if s is None:
                continue
            print("     %d  %d  %d | %2d | %.5f | %.5f | %.5f | %.5f"
                  % (a, b, p, n, s["vF"], s["mu"] / s["gamma"], s["Delta"], s["vL"]))
            rows.append((s["J"], dn, n, "bip+pt"))
sys.stdout.flush()

print()
print("  C. THE LABELLING SWEEP -- same underlying poset, every natural labelling")
print("""     For each underlying poset below, every linear extension is used as the
     natural labelling and the best min(v_F, v_L) over labellings is reported, with the
     best v_L over the (F)-FAILING labellings alongside.  This is the coordinate the
     corpus's families hold fixed.""")
print("     poset                         |  n | labellings | best min(vF,vL) | best v_L | vF")


def all_natural_labellings(cover, n, cap=40000):
    """Every natural labelling (= every linear extension) of the poset given by `cover`
    (bitmask of predecessors, arbitrary indices), as `dn` tuples."""
    cl = relabel_natural(cover, n)
    if cl is None:
        return []
    # rebuild closure in ORIGINAL indices
    clo = list(cover)
    for _ in range(n):
        new = []
        for i in range(n):
            m, acc = clo[i], clo[i]
            while m:
                j = (m & -m).bit_length() - 1
                m &= m - 1
                acc |= clo[j]
            new.append(acc)
        if new == clo:
            break
        clo = new
    out = []
    order = []
    seen = 0

    def rec():
        if len(out) >= cap:
            return
        nonlocal seen
        if len(order) == n:
            pos = {v: p for p, v in enumerate(order)}
            dn = []
            for p in range(n):
                v = order[p]
                m, mask = clo[v], 0
                while m:
                    j = (m & -m).bit_length() - 1
                    m &= m - 1
                    mask |= 1 << pos[j]
                dn.append(mask)
            out.append(tuple(dn))
            return
        for i in range(n):
            if seen >> i & 1:
                continue
            if clo[i] & ~seen:
                continue
            order.append(i)
            seen |= 1 << i
            rec()
            seen &= ~(1 << i)
            order.pop()

    rec()
    return out


def cover_bip_plus_pts(a, b, drops, p):
    n = a + b + p
    ds = set(drops)
    rel = [0] * n
    for j in range(b):
        m = 0
        for i in range(a):
            if (i, j) not in ds:
                m |= 1 << i
        rel[a + j] = m
    return rel, n


LABEL_CASES = [
    ("K_{3,3} - 1 relation", cover_bip_plus_pts(3, 3, [(2, 2)], 0)),
    ("K_{3,3} - 1  + 1 pt", cover_bip_plus_pts(3, 3, [(2, 2)], 1)),
    ("K_{4,3} - 1  + 1 pt", cover_bip_plus_pts(4, 3, [(3, 2)], 1)),
    ("K_{4,4} - 1", cover_bip_plus_pts(4, 4, [(3, 3)], 0)),
    ("K_{4,4} - 1  + 1 pt", cover_bip_plus_pts(4, 4, [(3, 3)], 1)),
    ("K_{5,4} - 1  + 1 pt", cover_bip_plus_pts(5, 4, [(4, 3)], 1)),
    ("K_{5,5} - 1", cover_bip_plus_pts(5, 5, [(4, 4)], 0)),
]
for name, (cover, n) in LABEL_CASES:
    labs = all_natural_labellings(cover, n, cap=6000)
    bestJ, bestvL, bestvF = -1.0, -1.0, 0.0
    for dn in labs:
        P = P789(dn, n)
        if not P.primitive():
            continue
        s = score(P)
        if s is None:
            continue
        if s["J"] > bestJ:
            bestJ = s["J"]
        if s["vF"] > 1.0 and s["vL"] > bestvL:
            bestvL, bestvF = s["vL"], s["vF"]
        rows.append((s["J"], dn, n, "label:" + name))
    print("     %-29s | %2d | %10d | %15.6f | %8.5f | %.4f"
          % (name, n, len(labs), bestJ, bestvL, bestvF))
    sys.stdout.flush()

# =============================================================================
print()
print("=" * 78)
print("S1.3  LOCAL SEARCH -- hill-climb on min(v_F, v_L) at n = 8..12")
print("=" * 78)
print("""  Moves: add a relation, delete a relation, or TRANSPOSE two adjacent labels when
  the elements are incomparable.  Objective min(v_F, v_L) with mu_ub in place of
  mu_pref, so it can only OVER-state the target.  Every restart is reported.
""")


def neighbours(dn, n):
    out = []
    for i in range(n):
        m = dn[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            rel = list(dn)
            rel[i] = dn[i] & ~(1 << j)
            d2 = relabel_natural(rel, n)
            if d2 is not None:
                out.append(d2)
    for i in range(n):
        for j in range(i):
            if dn[i] >> j & 1:
                continue
            rel = list(dn)
            rel[i] = dn[i] | (1 << j)
            d2 = relabel_natural(rel, n)
            if d2 is not None:
                out.append(d2)
    # label transpositions: swap labels k, k+1 when incomparable
    for k in range(n - 1):
        if dn[k + 1] >> k & 1:
            continue
        perm = list(range(n))
        perm[k], perm[k + 1] = perm[k + 1], perm[k]
        rel = [0] * n
        for i in range(n):
            m, mask = dn[i], 0
            while m:
                j = (m & -m).bit_length() - 1
                m &= m - 1
                mask |= 1 << perm.index(j)
            rel[perm.index(i)] = mask
        d2 = tuple(rel)
        ok = all(d2[i] >> i == 0 for i in range(n))
        if ok:
            out.append(d2)
    return out


def random_start(n):
    while True:
        dn = []
        for i in range(n):
            mask = 0
            for j in range(i):
                if random.random() < 0.35:
                    mask |= 1 << j
            m = mask
            while m:
                j = (m & -m).bit_length() - 1
                m &= m - 1
                mask |= dn[j]
            dn.append(mask)
        dn = tuple(dn)
        P = P789(dn, n)
        if P.primitive() and P.gamma_float() > 1e-12:
            return dn


BEST = {}
for n in range(8, 13):
    t0 = time.time()
    bestJ, bestdn, bestS = -1.0, None, None
    restarts = {8: 12, 9: 10, 10: 8, 11: 6, 12: 5}[n]
    for r in range(restarts):
        dn = random_start(n)
        P = P789(dn, n)
        s = score(P)
        cur = s["J"] if s else -1.0
        for _ in range(80):
            improved = False
            for d2 in neighbours(dn, n):
                P2 = P789(d2, n)
                if not P2.primitive():
                    continue
                s2 = score(P2)
                if s2 is None:
                    continue
                if s2["J"] > cur + 1e-12:
                    cur, dn, s = s2["J"], d2, s2
                    improved = True
            if not improved:
                break
        if cur > bestJ:
            bestJ, bestdn, bestS = cur, dn, s
        print("    n=%2d restart %2d -> %.6f   (v_F %.5f  v_L %.5f  rho %.6f  Delta %.6f)"
              % (n, r, cur, s["vF"], s["vL"], s["mu"] / s["gamma"], s["Delta"]))
        sys.stdout.flush()
    BEST[n] = (bestJ, bestdn, bestS)
    print("    n=%2d  BEST %.6f  at %s   (%.0fs)" % (n, bestJ, str(bestdn), time.time() - t0))
    print("         v_F %.6f  v_L %.6f  rho %.6f  Delta %.6f  gamma %.6f  height %d"
          % (bestS["vF"], bestS["vL"], bestS["mu"] / bestS["gamma"], bestS["Delta"],
             bestS["gamma"], height(bestdn, n)))
    sys.stdout.flush()

print()
print("=" * 78)
print("S1.4  VERDICT OF THE HUNT")
print("=" * 78)
hits = [(n, v) for n, v in BEST.items() if v[0] > 1.0]
famhits = [r for r in rows if r[0] > 1.0]
if hits or famhits:
    print("  *** CANDIDATE COUNTEREXAMPLES -- handing to exact treatment ***")
    for n, v in hits:
        print("    search n=%d  %s  J=%.6f" % (n, str(v[1]), v[0]))
    for J, dn, n, tag in famhits:
        print("    %s n=%d  %s  J=%.6f" % (tag, n, str(dn), J))
else:
    print("  NO candidate anywhere.  min(v_F, v_L) <= 1 at every poset examined, and the")
    print("  screen OVER-states v_L, so nothing was hidden by it.")
    print("  best per n from the search (NOT a maximum over its n):")
    for n in sorted(BEST):
        print("    n=%2d  %.6f   " % (n, BEST[n][0]))
    if rows:
        J, dn, n, tag = max(rows)
        print("  best over all family/labelling members: %.6f  at %s (n=%d, %s)"
              % (J, str(dn), n, tag))
