"""s6 -- P9 scored.  The entrywise-nonnegativity certificate for copositivity:

    Q - tN entrywise >= 0  =>  Q - tN copositive  =>  mu_pref >= t,
    so   e(P) := min_{k,l} Q_kl/N_kl   is a VALID LOWER bound on mu_pref;
    and  d(P) := min_k Q_kk/N_kk = min_k R(psi_k)  is a valid UPPER bound.
    e <= mu_pref <= d always, so if the min over ALL (k,l) is attained on the DIAGONAL
    the sandwich CLOSES and mu_pref = d exactly, in O(n^2) with no face enumeration.
P9 bet that closes at >= 50% of primitive posets at n <= 6.
"""
from fractions import Fraction
from libc50b import gen_posets, Poset, mu_exhaustive
print("  n | primitive | sandwich closes | mean (d-e)/d")
for n in (4, 5, 6):
    tot = closes = 0; acc = 0.0; bad = 0
    for dn in gen_posets(n):
        P = Poset(dn, n)
        if not P.primitive(): continue
        tot += 1
        m = n - 1
        vals = [(Fraction(n * P.QI[i][j], 2 * P.LE * P.NI[i][j]), i == j)
                for i in range(m) for j in range(m) if P.NI[i][j] > 0]
        e = min(vals)[0]
        d = min(v for v, dg in vals if dg)
        mu, _ = mu_exhaustive(P)
        if float(e) > mu + 1e-9: bad += 1          # control: e must be a LOWER bound
        if e == d: closes += 1
        acc += float(d - e) / float(d) if d else 0.0
    print("  %d | %9d | %6d (%5.1f%%)  | %.4f      [lower-bound violations: %d]"
          % (n, tot, closes, 100.0 * closes / tot, acc / tot, bad))
