"""mg-3969 / A2 — the threshold that IS measurable, and what it is worth.

A1 showed the CONSUMABLE statement's threshold cannot be measured.  What
mg-3ce3 measured, and what the corpus has been calling `eps_0`, is the
threshold of a strictly stronger statement, asserted for ALL posets rather
than only for counterexamples:

    U_either(eps): Delta_1(A,B) <= eps and neither side a chain
                   ==> a pair balanced in P[A] OR in P[B] is still in
                       [1/3,2/3] in P.
    U_smaller(eps): the same but the pair must come from the SMALLER side.

U => S, so any lower bound on U's threshold is a lower bound on the
consumable one; and an UPPER bound on U's threshold is exhibitable, whereas
an upper bound on S's is not (A1).

This sweep is exhaustive over every poset on n <= NMAX elements at every
prefix cut -- a population mg-3ce3 did not cover (it sampled n = 8,9,10 and
built n <= 16 families).  Exact rationals throughout.
"""

from fractions import Fraction
import sys

from lib3969 import (poset_iter, linear_extensions, delta1, p_matrix,
                     balanced_pairs, induced, is_chain, incomparable)

LO, HI = Fraction(1, 3), Fraction(2, 3)


def side_report(n, rel, exts, S):
    """(has_balanced_in_side, survives) for the induced subposet on S."""
    m, sub, idx = induced(rel, S)
    if is_chain(m, sub):
        return None, None                      # chain: supplies no pair
    sub_ex = linear_extensions(m, sub)
    bal = balanced_pairs(m, sub, sub_ex)       # pairs balanced INSIDE the side
    if not bal:
        return False, False
    inv = {i: e for e, i in idx.items()}
    pP = p_matrix(n, rel, exts)
    surv = False
    for (a, b) in bal:
        x, y = inv[a], inv[b]
        key = (x, y) if (x, y) in pP else (y, x)
        p = pP[key] if key == (x, y) else 1 - pP[key]
        if LO <= p <= HI:
            surv = True
            break
    return True, surv


def main(nmax=6):
    print("=" * 78)
    print("mg-3969 / A2 — the UNIFORM transfer threshold, exhaustive to n=%d" % nmax)
    print("=" * 78)

    fail_small = []        # (eps, n, rel, k)
    fail_either = []
    nc_exact_fail = 0      # NC4: the deliberately-wrong predicate
    cuts = both_nonchain = 0

    for n in range(3, nmax + 1):
        for rel in poset_iter(n):
            exts = linear_extensions(n, rel)
            for k in range(1, n):
                cuts += 1
                A, B = set(range(k)), set(range(k, n))
                hasA, survA = side_report(n, rel, exts, A)
                hasB, survB = side_report(n, rel, exts, B)
                if hasA is None or hasB is None:
                    continue                    # a side is a chain
                both_nonchain += 1
                eps = delta1(n, rel, exts, k)
                S = A if len(A) <= len(B) else B
                hasS, survS = (hasA, survA) if S is A else (hasB, survB)
                if hasS and not survS:
                    fail_small.append((eps, n, rel, k))
                if (hasA or hasB) and not (survA or survB):
                    fail_either.append((eps, n, rel, k))
                # NC4: exact preservation p^P == p^side is a WRONG predicate;
                # it must fail somewhere or this instrument cannot tell
                # predicates apart.
                m, sub, idx = induced(rel, A)
                if not is_chain(m, sub):
                    sub_ex = linear_extensions(m, sub)
                    bal = balanced_pairs(m, sub, sub_ex)
                    pP = p_matrix(n, rel, exts)
                    for (a, b), pS in bal.items():
                        inv = {i: e for e, i in idx.items()}
                        x, y = inv[a], inv[b]
                        key = (x, y) if (x, y) in pP else (y, x)
                        p = pP[key] if key == (x, y) else 1 - pP[key]
                        if p != pS:
                            nc_exact_fail += 1
                            break
        print("  n=%d done (cuts so far %d, both-non-chain %d)" % (n, cuts, both_nonchain))
        sys.stdout.flush()

    print("\ncuts examined: %d ; both sides non-chain: %d" % (cuts, both_nonchain))
    print("[NC4] exact-preservation (deliberately wrong) predicate failed at "
          "%d cuts.  %s" % (nc_exact_fail,
                            "FIRES." if nc_exact_fail else "DID NOT FIRE — DEFECT."))

    print("\n--- U_smaller: smaller-side-only reading ---")
    print("failing cuts: %d" % len(fail_small))
    if fail_small:
        fail_small.sort(key=lambda t: t[0])
        e, n, rel, k = fail_small[0]
        print("SMALLEST eps at which U_smaller FAILS: %s = %.6f  (n=%d, k=%d)"
              % (e, float(e), n, k))
        print("witness poset (strict relations, ground set 0..%d): %s"
              % (n - 1, sorted(rel)))
        print(">>> hence the UNIFORM-in-n threshold for U_smaller satisfies")
        print(">>>     eps_0(U_smaller) <= %s = %.6f" % (e, float(e)))
        print(">>> This is an n-FREE UPPER BOUND: one violator at one n bounds")
        print(">>> every uniform threshold, at every n.")
        for e, n, rel, k in fail_small[:5]:
            print("    eps=%-12s n=%d k=%d rel=%s" % (str(e), n, k, sorted(rel)))
    else:
        print("no failure — no upper bound obtainable from this population.")

    print("\n--- U_either: either-side reading (what Step 6 can use) ---")
    print("failing cuts: %d" % len(fail_either))
    if fail_either:
        fail_either.sort(key=lambda t: t[0])
        e, n, rel, k = fail_either[0]
        print("SMALLEST eps at which U_either FAILS: %s = %.6f (n=%d,k=%d) rel=%s"
              % (e, float(e), n, k, sorted(rel)))
        print(">>> eps_0(U_either) <= %s, n-free upper bound." % e)
    else:
        print(">>> NO VIOLATION AT ANY eps, up to and including eps = 1.")
        print(">>> So this population yields NO upper bound on eps_0(U_either):")
        print(">>> exhaustively to n=%d the either-side transfer is UNCONDITIONAL," % nmax)
        print(">>> which is a stronger statement than any threshold claim and is")
        print(">>> consistent with mg-3ce3's 0 RED events over 6681 posets.")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 6)
