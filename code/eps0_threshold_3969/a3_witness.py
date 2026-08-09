"""mg-3969 / A3 — the U_either witness, re-derived by a DIFFERENT code path.

A2's headline number (an n-free UPPER bound on the uniform transfer
threshold) rests on one witness.  A bug in `linear_extensions` would produce
a phantom violator, so this file recomputes everything by brute force over
`itertools.permutations` filtered by the relation -- sharing NO code with the
recursive extension builder -- and prints the whole certificate so it can be
checked by hand.

It also answers the question the witness immediately raises: is the failure
an artefact of looking at a cut that is not the thinnest?  Every prefix cut
of the witness is reported with its own Delta_1 and its own verdict.
"""

from fractions import Fraction
from itertools import combinations, permutations
import sys

LO, HI = Fraction(1, 3), Fraction(2, 3)

# The two witnesses A2 reports, on ground set 0..5.
W_EITHER = (6, 3, [(0, 2), (0, 3), (0, 4), (0, 5), (1, 4), (1, 5), (2, 4), (3, 4)])
W_SMALL = (6, 3, [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 3), (1, 4),
                  (1, 5), (2, 4), (3, 4), (3, 5)])


def brute_exts(n, rel):
    """Every linear extension, by filtering all n! permutations.  sigma[a] is
    the element at position a."""
    rel = set(rel)
    out = []
    for sigma in permutations(range(n)):
        pos = {e: a for a, e in enumerate(sigma)}
        if all(pos[a] < pos[b] for (a, b) in rel):
            out.append(sigma)
    return out


def pairs_p(n, rel, exts):
    rel = set(rel)
    inc = [(x, y) for x, y in combinations(range(n), 2)
           if (x, y) not in rel and (y, x) not in rel]
    N = len(exts)
    out = {}
    for (x, y) in inc:
        c = 0
        for sigma in exts:
            pos = {e: a for a, e in enumerate(sigma)}
            if pos[x] < pos[y]:
                c += 1
        out[(x, y)] = Fraction(c, N)
    return out


def d1(n, rel, exts, k):
    A = set(range(k))
    t = sum(len(A - set(s[:k])) for s in exts)
    return Fraction(t, len(exts)) / min(k, n - k)


def sub_rel(rel, S):
    S = sorted(S)
    idx = {e: i for i, e in enumerate(S)}
    return len(S), [(idx[a], idx[b]) for (a, b) in rel if a in idx and b in idx], idx


def report(name, n, kstar, rel):
    print("=" * 78)
    print("%s — witness on ground set 0..%d" % (name, n - 1))
    print("=" * 78)
    print("strict relations: %s" % sorted(rel))
    exts = brute_exts(n, rel)
    print("|L(P)| = %d   (brute force over %d! = %d permutations)"
          % (len(exts), n, len(list(permutations(range(1))))*0 or __import__('math').factorial(n)))
    pP = pairs_p(n, rel, exts)
    dlt = max(min(p, 1 - p) for p in pP.values())
    print("delta(P) = %s = %.6f   -> P %s a 1/3-balanced pair, so DISJUNCT (i)"
          % (dlt, float(dlt), "HAS" if dlt >= Fraction(1, 3) else "LACKS"))
    print("   %s and the CONSUMABLE statement S is satisfied here at eps = 1."
          % ("FIRES" if dlt >= Fraction(1, 3) else "FAILS"))

    print("\nevery prefix cut:")
    print("  %-3s %-12s %-10s %-9s %-9s %s"
          % ("k", "Delta_1", "float", "A chain?", "B chain?", "U_either verdict"))
    for k in range(1, n):
        A, B = set(range(k)), set(range(k, n))
        e = d1(n, rel, exts, k)
        verdicts = []
        anyhas = False
        anysurv = False
        for S in (A, B):
            m, sub, idx = sub_rel(rel, S)
            if len(sub) == m * (m - 1) // 2:
                verdicts.append("chain")
                continue
            sex = brute_exts(m, sub)
            sp = pairs_p(m, sub, sex)
            bal = [pr for pr, p in sp.items() if LO <= p <= HI]
            if not bal:
                verdicts.append("no-bal-in-side")
                continue
            anyhas = True
            inv = {i: e2 for e2, i in idx.items()}
            surv = []
            for (a, b) in bal:
                x, y = inv[a], inv[b]
                key = (x, y) if (x, y) in pP else (y, x)
                p = pP[key] if key == (x, y) else 1 - pP[key]
                surv.append((x, y, sp[(a, b)], p, LO <= p <= HI))
            if any(s[4] for s in surv):
                anysurv = True
            verdicts.append("bal=%d surv=%d" % (len(surv), sum(1 for s in surv if s[4])))
        chains = [v == "chain" for v in verdicts]
        if any(chains):
            v = "SKIP (a side is a chain)"
        elif not anyhas:
            v = "SKIP (no balanced-in-side pair anywhere)"
        elif anysurv:
            v = "holds"
        else:
            v = "*** FAILS ***"
        print("  %-3d %-12s %-10.6f %-9s %-9s %s | %s"
              % (k, e, float(e), verdicts[0], verdicts[1], v, ""))

    # full certificate at the reported cut
    k = kstar
    A, B = set(range(k)), set(range(k, n))
    print("\nCERTIFICATE at the reported cut k = %d  (A = %s, B = %s), "
          "Delta_1 = %s = %.6f" % (k, sorted(A), sorted(B), d1(n, rel, exts, k),
                                   float(d1(n, rel, exts, k))))
    for label, S in (("A", A), ("B", B)):
        m, sub, idx = sub_rel(rel, S)
        inv = {i: e2 for e2, i in idx.items()}
        print("  side %s = %s, induced relations %s"
              % (label, sorted(S), sorted((inv[a], inv[b]) for (a, b) in sub)))
        if len(sub) == m * (m - 1) // 2:
            print("    CHAIN — supplies no pair")
            continue
        sex = brute_exts(m, sub)
        sp = pairs_p(m, sub, sex)
        for (a, b), pS in sorted(sp.items()):
            x, y = inv[a], inv[b]
            key = (x, y) if (x, y) in pP else (y, x)
            p = pP[key] if key == (x, y) else 1 - pP[key]
            mark = "BALANCED-IN-SIDE" if LO <= pS <= HI else "not balanced in side"
            keep = "STAYS in [1/3,2/3]" if LO <= p <= HI else "LEAVES [1/3,2/3]"
            print("    pair (%d,%d): p_side = %-8s p_P = %-8s  %s -> %s"
                  % (x, y, pS, p, mark, keep))
    print()


if __name__ == "__main__":
    n, k, rel = W_EITHER
    report("U_either (the either-side / endgame form Step 6 can use)", n, k, rel)
    n, k, rel = W_SMALL
    report("U_smaller (the smaller-side-only reading)", n, k, rel)
