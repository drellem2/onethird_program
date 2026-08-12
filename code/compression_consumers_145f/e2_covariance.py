"""e2 -- the (B-cov) residual, which is the strongest-looking candidate on the board.

STATE.md:180-193 orders three residuals and puts (B-cov) first: *"break the wrong-signed
same-side covariance"* (FKG/XYZ force it >= 0), *"the sharp edge"*, and *"the object three
separate routes converge on"* (mg-dcae, mg-8f56, mg-a58f).  compression.tex:102 advertises

    "There are NO COVARIANCE TERMS WHATSOEVER inside a compressed fiber."

so the shapes appear to match, and this arm exists to test that rather than to assume it.

TWO FINDINGS, and the second is the quantitative one.

 (e2.1)  The covariance the identity kills is ZERO FOR A TRIVIAL REASON and is not (B-cov)'s.
         Inside an odd fiber every pair indicator is either a free Bernoulli on its own
         2-block or CONSTANT; distinct free blocks are disjoint.  So Cov(s_xy, s_uv | C_o) = 0
         identically -- verified at every fiber of every poset in the population.  The
         (B-cov) covariance Cov(s_xy, s_xz) is a BETWEEN-fiber quantity: by the law of total
         variance it lives entirely in Var(E[pos_x | C_o]), which the identity does not
         compute.

 (e2.2)  THE IDENTITY'S SHARE OF THE (B) QUANTITY IS BOUNDED BY 1/4, UNIFORMLY.
         E Var(pos_x | C_o) = (1/4) sum_{y || x} A^o_xy <= 1/4, because sum_y A^o_xy is the
         probability that x sits in a free odd 2-block at all.  Meanwhile Var(pos_x) reaches
         (n^2 - 1)/12 on the antichain.  So the fraction of Var(pos_x) that the identity
         computes is O(n^-2) and the rest is exactly the term it is silent on.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib145f as L  # noqa: E402

ok = True

POP = ([(3, p) for p in L.all_posets(3)]
       + [(4, p) for p in L.all_posets(4)]
       + [(5, p) for p in L.sample_posets(5, 50, 5)]
       + [(6, p) for p in L.sample_posets(6, 25, 23)])


def signed_pair_indicator(LEs, x, y):
    """s_xy(L) = 1{x <_L y}, as a rational vector."""
    return [Fraction(1) if L_.index(x) < L_.index(y) else Fraction(0) for L_ in LEs]


# ---------------------------------------------------------------------------------------
L.banner("e2.1  the covariance the identity kills is identically ZERO, at every fiber")
print("  For every poset, every odd fiber, and every pair of DISTINCT incomparable pairs,")
print("  the within-fiber covariance of the two pair indicators.  If this is ever nonzero")
print("  the note's :102 claim is false; if it is always zero the claim is true and says")
print("  nothing about (B-cov), whose covariance is between fibers.")
nonzero = 0
checked = 0
for (n, lt) in POP[:120]:
    LEs = L.linear_extensions(n, lt)
    inc = L.incomparable_pairs(n, lt)
    if len(inc) < 2:
        continue
    ind = {p: signed_pair_indicator(LEs, *p) for p in inc}
    for _, idxs in L.fibers(LEs, L.odd_blocks(n)).items():
        m = len(idxs)
        for a in range(len(inc)):
            for b in range(a + 1, len(inc)):
                u, v = ind[inc[a]], ind[inc[b]]
                mu = sum(u[k] for k in idxs) / Fraction(m)
                mv = sum(v[k] for k in idxs) / Fraction(m)
                cov = sum((u[k] - mu) * (v[k] - mv) for k in idxs) / Fraction(m)
                nonzero += (cov != 0)
                checked += 1
ok &= L.verdict(nonzero == 0, "within-fiber Cov(s_xy, s_uv) over every (fiber, pair, pair)",
                f"{nonzero} nonzero / {checked}")

# ---------------------------------------------------------------------------------------
L.banner("e2.2  and the (B-cov) covariance is NONZERO and WRONG-SIGNED, between fibers")
print("  C_x := sum_{y != z, both || x} Cov(s_xy, s_xz).  FKG/XYZ force it >= 0; STATE.md")
print("  calls beating that 'the sharp edge'.  Reported beside the identity's within-fiber")
print("  term for the same statistic.")
print()
print(f"  {'n':>2} {'poset':>6} {'x':>2} {'Var(pos_x)':>12} {'EVar(pos_x|C_o)':>16} "
      f"{'share':>9} {'C_x':>12}")
pos_cnt = neg_cnt = zero_cnt = 0
worst_share = None
rows = 0
for (n, lt) in POP:
    LEs = L.linear_extensions(n, lt)
    inc = L.incomparable_pairs(n, lt)
    if not inc:
        continue
    A_o, _ = L.adjacency_probs(n, lt, LEs)
    for x in range(n):
        nb = [y for y in range(n) if y != x
              and ((min(x, y), max(x, y)) in A_o)]
        if len(nb) < 2:
            continue
        px = [Fraction(L_.index(x)) for L_ in LEs]
        vx = L.variance(px)
        ind = {y: signed_pair_indicator(LEs, x, y) for y in nb}
        C = Fraction(0)
        for i in range(len(nb)):
            for j in range(len(nb)):
                if i != j:
                    C += L.covariance(ind[nb[i]], ind[nb[j]])
        within = sum(A_o[(min(x, y), max(x, y))] for y in nb) / 4
        if C > 0:
            pos_cnt += 1
        elif C < 0:
            neg_cnt += 1
        else:
            zero_cnt += 1
        if vx > 0:
            sh = within / vx
            if worst_share is None or sh < worst_share:
                worst_share = sh
        rows += 1
print(f"  ({rows} (poset, element) rows; per-row printing suppressed, summary follows)")
print(f"  same-side covariance C_x:  > 0 at {pos_cnt},  = 0 at {zero_cnt},  < 0 at {neg_cnt}")
ok &= L.verdict(neg_cnt == 0, "C_x >= 0 everywhere -- the FKG/XYZ wrong sign, reproduced",
                f"{pos_cnt} strictly positive")
print(f"  smallest observed share EVar(pos_x|C_o)/Var(pos_x) = {L.fr(worst_share)}")

# ---------------------------------------------------------------------------------------
L.banner("e2.3  THE UNIFORM CAP: E Var(pos_x | C_o) <= 1/4 at EVERY poset and every x")
print("  Because E Var(pos_x|C_o) = (1/4) sum_{y||x} A^o_xy and sum_y A^o_xy = Pr[x lies in")
print("  a free odd 2-block] <= 1.  Checked directly against the fiber computation.")
over = 0
checked = 0
maxv = Fraction(0)
for (n, lt) in POP:
    LEs = L.linear_extensions(n, lt)
    A_o, A_e = L.adjacency_probs(n, lt, LEs)
    for x in range(n):
        px = [Fraction(L_.index(x)) for L_ in LEs]
        for (blocks, A) in ((L.odd_blocks(n), A_o), (L.even_blocks(n), A_e)):
            w = L.e_cond_var(px, LEs, blocks)
            pred = sum(A[(min(x, y), max(x, y))] for y in range(n)
                       if y != x and (min(x, y), max(x, y)) in A) / 4
            if w != pred:
                over += 1
            maxv = max(maxv, w)
            checked += 1
ok &= L.verdict(over == 0, "E Var(pos_x|C) equals the adjacency formula", f"{over} / {checked}")
ok &= L.verdict(maxv <= Fraction(1, 4), "and never exceeds 1/4",
                f"max observed = {maxv} = {L.fr(maxv)}")

# ---------------------------------------------------------------------------------------
L.banner("e2.4  against the antichain, where Var(pos_x) = (n^2 - 1)/12 exactly")
print(f"  {'n':>3} {'Var(pos_x)':>12} {'EVar(pos_x|C_o)':>16} {'share':>14}")
for n in (3, 4, 5, 6, 7):
    lt = L.antichain(n)
    LEs = L.linear_extensions(n, lt)
    px = [Fraction(L_.index(0)) for L_ in LEs]
    v = L.variance(px)
    w = L.e_cond_var(px, LEs, L.odd_blocks(n))
    assert v == Fraction(n * n - 1, 12), (n, v)
    print(f"  {n:>3} {str(v):>12} {str(w):>16} {L.fr(w / v):>14}")
print("""
  The share falls like Theta(n^-2).  This is mg-409a section 4's alpha(A_n) <= 6/(n(n+1))
  seen from the (B) side rather than the spectral side, and it is the same mechanism: a
  degree-one statistic's within-fiber variance is a bounded local quantity, while the (B)
  quantity it would have to control is global.""")

L.banner("e2  RESULT")
print("  ok" if ok else "  NOT ok")
sys.exit(0 if ok else 1)
