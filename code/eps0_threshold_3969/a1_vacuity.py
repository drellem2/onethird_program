"""mg-3969 / A1 — THE CONSUMABLE THRESHOLD IS NOT MEASURABLE.

What this measures, and why it is the whole point of the ticket.

The statement Step 6 consumes is (mg-345e 5.1):

    S(eps):  Delta_1(A,B) <= eps  ==>  (i) P has a 1/3-balanced pair
                                       OR (iii-exact) a pair balanced in
                                          P[A] or P[B] is still in [1/3,2/3] in P.

`eps_0` is the largest eps at which S(eps) holds.  This script establishes,
by exhaustive enumeration in exact rationals, that on EVERY poset a machine
can exhibit, S(eps) is satisfied by disjunct (i) ALONE, at eps = 1 -- i.e.
with no threshold at all -- because disjunct (i) is exactly the 1/3--2/3
conjecture, which holds on every poset anyone has ever computed.

Consequence: no computation can bound `eps_0` for S.  The number the corpus
calls `eps_0` (0.20, mg-3ce3) is the threshold of a DIFFERENT and STRICTLY
STRONGER statement -- the (iii-exact) transfer asserted for ALL posets, not
only for counterexamples.  A2 measures that one.

Controls are reported inline; a control that does not fire is a defect.
"""

from fractions import Fraction
import sys

from lib3969 import (poset_iter, linear_extensions, delta, delta1, phi,
                     balanced_pairs, incomparable, induced, is_chain)

THIRD = Fraction(1, 3)


def main(nmax=6):
    print("=" * 78)
    print("mg-3969 / A1 — is the CONSUMABLE threshold eps_0 measurable at all?")
    print("=" * 78)

    # ---------------------------------------------------------- positive control
    # Op-Form Claim 3.3's endpoint poset P0 = {a<b} + {c}: delta = 1/3 EXACTLY.
    n0, rel0 = 3, frozenset({(0, 1)})          # 0<1, 2 isolated
    e0 = linear_extensions(n0, rel0)
    d0 = delta(n0, rel0, e0)
    print("\n[PC1] endpoint poset {a<b} u {c}: |L| = %d, delta = %s  (expect 3, 1/3)"
          % (len(e0), d0))
    assert len(e0) == 3 and d0 == THIRD, "PC1 FAILED — delta code is wrong"
    print("      PC1 fires: delta = 1/3 exactly, zero interior slack.")

    # ---------------------------------------------------------- negative controls
    # NC1: a chain has Delta_1 = 0 at every prefix and no incomparable pair.
    for n in (4, 6):
        rel = frozenset((i, j) for i in range(n) for j in range(i + 1, n))
        ex = linear_extensions(n, rel)
        ds = [delta1(n, rel, ex, k) for k in range(1, n)]
        assert all(d == 0 for d in ds), "NC1 FAILED"
        assert delta(n, rel, ex) is None, "NC1 FAILED (chain has a delta)"
    print("[NC1] chain: Delta_1 = 0 at every prefix, delta undefined.  FIRES.")

    # NC2: antichain, Op-Form 4.2's hand computation Delta_1 = (n-k)/n for k<=n/2.
    for n in (4, 5, 6):
        rel = frozenset()
        ex = linear_extensions(n, rel)
        for k in range(1, n // 2 + 1):
            got, want = delta1(n, rel, ex, k), Fraction(n - k, n)
            assert got == want, "NC2 FAILED n=%d k=%d %s != %s" % (n, k, got, want)
            assert phi(n, rel, ex, k) == want, "NC2 FAILED (Phi != Delta_1)"
    print("[NC2] antichain: Delta_1 = Phi = (n-k)/n for k <= n/2 at n=4,5,6.  FIRES.")
    print("      (this is Op-Form 4.2's hand computation, and Lemma 2.1's")
    print("       Phi = Delta_1 identity, reproduced independently)")

    # NC5: COMPLETENESS OF THE ENUMERATION.  `poset_iter(n)` yields the posets
    # admitting the identity as a linear extension.  If it is complete, then
    # counting (labelled poset, linear extension) pairs two ways must agree:
    #     n! * |poset_iter(n)|  ==  sum over ALL labelled posets of e(P).
    # The right-hand side is computed from a DIFFERENT enumeration (all 3^C(n,2)
    # orientations of all pairs, transitivity-filtered), so a systematic gap in
    # poset_iter cannot cancel.  A weaker check -- "the count is large" -- would
    # not catch a missing isomorphism class.
    import math
    from itertools import product
    for n in (3, 4, 5):
        lhs = math.factorial(n) * sum(1 for _ in poset_iter(n))
        prs = [(i, j) for i in range(n) for j in range(i + 1, n)]
        rhs = 0
        for choice in product((0, 1, 2), repeat=len(prs)):
            rel = set()
            for (i, j), c in zip(prs, choice):
                if c == 1:
                    rel.add((i, j))
                elif c == 2:
                    rel.add((j, i))
            if any(b == c2 and (a, d) not in rel
                   for (a, b) in rel for (c2, d) in rel):
                continue                        # not transitive
            rhs += len(linear_extensions(n, frozenset(rel)))
        assert lhs == rhs, "NC5 FAILED at n=%d: %d != %d" % (n, lhs, rhs)
        print("[NC5] n=%d: %d! x %d posets = %d = sum of e(P) over all labelled "
              "posets.  FIRES." % (n, n, lhs // math.factorial(n), lhs))

    # --------------------------------------------------------------- the sweep
    print("\n%-3s %9s %9s %9s %9s %9s" %
          ("n", "posets", "nonchain", "cuts", "no-bal-P", "maxD1"))
    grand = dict(posets=0, nonchain=0, cuts=0, nobal=0, maxd1=Fraction(0))
    per_n = []
    for n in range(3, nmax + 1):
        c = dict(posets=0, nonchain=0, cuts=0, nobal=0, maxd1=Fraction(0))
        for rel in poset_iter(n):
            c["posets"] += 1
            ex = linear_extensions(n, rel)
            d = delta(n, rel, ex)
            if d is None:                       # chain: excluded by the conjecture
                continue
            c["nonchain"] += 1
            if d < THIRD:
                c["nobal"] += 1                 # a counterexample to 1/3--2/3
            for k in range(1, n):
                c["cuts"] += 1
                e = delta1(n, rel, ex, k)
                if e > c["maxd1"]:
                    c["maxd1"] = e
        per_n.append((n, c))
        for key in ("posets", "nonchain", "cuts", "nobal"):
            grand[key] += c[key]
        grand["maxd1"] = max(grand["maxd1"], c["maxd1"])
        print("%-3d %9d %9d %9d %9d %9s" %
              (n, c["posets"], c["nonchain"], c["cuts"], c["nobal"], c["maxd1"]))
        sys.stdout.flush()

    print("\nTOTAL: %d posets, %d non-chain, %d prefix cuts."
          % (grand["posets"], grand["nonchain"], grand["cuts"]))

    # ------------------------------------------------------------- the verdict
    print("\n[NC3] max Delta_1 observed = %s  (hand bound: Delta_1 <= 1 always,"
          % grand["maxd1"])
    print("      since |A\\sigma(A)| = |sigma(A)\\A| <= min(|A|,|B|)).")
    assert grand["maxd1"] <= 1, "NC3 FAILED — Delta_1 exceeded its hand bound"
    print("      NC3 FIRES: the bound is respected and it is ATTAINED"
          if grand["maxd1"] == 1 else "      NC3 FIRES: bound respected.")

    print("\n>>> posets with NO 1/3-balanced pair (i.e. disjunct (i) FAILS): %d"
          % grand["nobal"])
    if grand["nobal"] == 0:
        print(">>> DISJUNCT (i) HOLDS AT EVERY ONE OF THE %d CUTS, AT eps = 1."
              % grand["cuts"])
        print(">>> Therefore S(eps) is TRUE AT eps = 1 for every poset in this")
        print(">>> population, i.e. the CONSUMABLE threshold measured here is")
        print(">>> eps_0 = 1, n-free, and CARRIES NO INFORMATION.  The measurement")
        print(">>> is vacuous BY CONSTRUCTION, not by accident of the population:")
        print(">>> S(eps)'s non-vacuous content lives only on posets with")
        print(">>> delta < 1/3, and none exist at any n <= %d (and none are" % nmax)
        print(">>> known at ANY n).  NO COMPUTATION CAN PIN eps_0 FOR S.")
    else:
        print(">>> A COUNTEREXAMPLE TO THE 1/3--2/3 CONJECTURE WAS FOUND. "
              "That is not a threshold result; stop and report it.")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 6)
