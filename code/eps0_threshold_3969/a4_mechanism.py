"""mg-3969 / A4 — WHAT KILLS THE TRANSFER, and how far the ceiling can move.

A2 exhibits an n-free upper bound on the threshold of the F-free repaired
statement in its either-side form.  A single witness is a number; a mechanism
is a prediction.  This file asks, of every either-side failure found
exhaustively to n = NMAX:

  * how thin can the interface be when the transfer fails (the ceiling);
  * how much INTERIOR SLACK the side's balanced pairs had.

Op-Form Claim 3.3 says minimality cannot be strengthened to give interior
slack, because a poset attains delta = 1/3 exactly.  If every failure here
turns out to have zero interior slack, then Claim 3.3's abstract objection is
not a technicality: it is the entire failure mechanism, and the ceiling is a
statement about zero-slack sides rather than about thin interfaces.
"""

from fractions import Fraction
import sys

from lib3969 import (poset_iter, linear_extensions, delta1, p_matrix,
                     balanced_pairs, induced, is_chain)

LO, HI = Fraction(1, 3), Fraction(2, 3)


def side_pairs(n, rel, exts, S, pP):
    """[(p_side, p_in_P)] over pairs balanced in the induced subposet on S,
    or None when S is a chain."""
    m, sub, idx = induced(rel, S)
    if is_chain(m, sub):
        return None
    sub_ex = linear_extensions(m, sub)
    bal = balanced_pairs(m, sub, sub_ex)
    inv = {i: e for e, i in idx.items()}
    out = []
    for (a, b), pS in bal.items():
        x, y = inv[a], inv[b]
        key = (x, y) if (x, y) in pP else (y, x)
        p = pP[key] if key == (x, y) else 1 - pP[key]
        out.append((pS, p))
    return out


def slack(pS):
    """Interior slack of a balanced-in-side pair: distance from the endpoints
    of [1/3,2/3].  Zero means the pair sits exactly on an endpoint."""
    return min(pS - LO, HI - pS)


def main(nmax=6):
    print("=" * 78)
    print("mg-3969 / A4 — failure mechanism of the either-side transfer, n<=%d" % nmax)
    print("=" * 78)
    fails = []
    for n in range(3, nmax + 1):
        for rel in poset_iter(n):
            exts = linear_extensions(n, rel)
            pP = p_matrix(n, rel, exts)
            for k in range(1, n):
                A, B = set(range(k)), set(range(k, n))
                sa = side_pairs(n, rel, exts, A, pP)
                sb = side_pairs(n, rel, exts, B, pP)
                if sa is None or sb is None:
                    continue
                allp = sa + sb
                if not allp:
                    continue
                if any(LO <= p <= HI for (_, p) in allp):
                    continue                       # transfer succeeded
                fails.append((delta1(n, rel, exts, k), n, k,
                              max(slack(pS) for (pS, _) in allp),
                              len(allp), sorted(rel)))
        print("  n=%d swept (%d failures so far)" % (n, len(fails)))
        sys.stdout.flush()

    if not fails:
        print("\nNo either-side failure at any eps — no ceiling from this population.")
        return

    fails.sort()
    print("\n%d either-side failures.  Sorted by interface thinness:" % len(fails))
    print("  %-10s %-10s %-3s %-3s %-10s %s"
          % ("Delta_1", "float", "n", "k", "max slack", "#bal pairs"))
    for e, n, k, sl, cnt, rel in fails[:12]:
        print("  %-10s %-10.6f %-3d %-3d %-10s %d" % (e, float(e), n, k, sl, cnt))

    emin = fails[0][0]
    print("\n>>> CEILING: eps_0(U_either) <= %s = %.6f, uniformly in n."
          % (emin, float(emin)))
    print(">>> (one violator at one n bounds every n-free threshold, at every n)")

    slacks = sorted({f[3] for f in fails})
    print("\ndistinct max-interior-slack values over ALL %d failures: %s"
          % (len(fails), [str(s) for s in slacks]))
    if slacks == [Fraction(0)]:
        print(">>> EVERY failure has ZERO interior slack: in each one, every")
        print(">>> balanced-in-side pair sits EXACTLY on an endpoint of")
        print(">>> [1/3,2/3].  Op-Form Claim 3.3's objection is not a technical")
        print(">>> nicety — it is the whole failure mechanism, and the ceiling")
        print(">>> above is a fact about zero-slack sides, not about thin")
        print(">>> interfaces.  PREDICTION this makes, which is testable and")
        print(">>> which I did NOT test: a transfer statement that assumed any")
        print(">>> fixed interior slack c>0 on the side would have no violator")
        print(">>> in this population at all.")
    else:
        print(">>> Failures occur with strictly positive interior slack too, so")
        print(">>> the mechanism is NOT only the Claim 3.3 endpoint gap.")
        pos = [f for f in fails if f[3] > 0]
        e, n, k, sl, cnt, rel = min(pos)
        print(">>> thinnest positive-slack failure: eps=%s slack=%s n=%d k=%d rel=%s"
              % (e, sl, n, k, rel))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 6)
