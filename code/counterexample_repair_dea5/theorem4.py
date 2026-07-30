"""The target's Theorem 4, in the generality its proof has: EVERY weight.

  Theorem 4 as committed:  "For the weight uniform on all P-compatible moves and
  any non-chain P, lambda_2 = max over incomparable pairs {x,y} of s(x,y)."

  The proof in section 5.2 uses two facts and neither mentions the weight:
  lambda_X is non-increasing as X coarsens (true for any distribution on moves,
  since coarsening X can only shrink the set of moves whose level is coarser than
  or equal to X), and m_X is a combinatorial invariant of P.  So the theorem
  holds for every weight, and the general form is the one section 5.5 needs --
  the w_t family of Theorem 7 is exactly a family of non-uniform weights.

Two things are tested, both against the ACTUAL transition matrix where the matrix
is affordable:

  A.  the SPECTRUM claim -- eigenvalues of M are exactly the lambda_X with
      multiplicities m_X -- via power sums, exactly, for every weight used.
      This is what makes lambda_2 meaningful without an eigensolver.
  B.  the IDENTITY lambda_2 = max_{x||y} s(x,y), for every weight, on a wider
      population where the matrix is not built.

Weights used: the uniform-move weight; three random rational weights per poset
(fixed seed, so this re-runs identically); the w_t family of Theorem 7 at
t = 0, 1/4, 1/3, 1/2, 3/4, 1; and two deliberately degenerate weights (all mass
on one move; mass on the finest moves only) since a universal claim has to
survive the corners.
"""

import random
import sys
from fractions import Fraction

from poset import all_posets
from walk import (all_moves, transition_matrix, lambdas, multiplicities,
                  same_block_mass, lambda_2, power_sums_agree, level_of)

SEED = 20260730


def weight_families(P, moves, rng):
    """(name, weights) pairs.  Every entry is a probability distribution."""
    K = len(moves)
    out = [("uniform-move", [Fraction(1, K)] * K)]
    for r in range(3):
        raw = [Fraction(rng.randint(0, 20), rng.randint(1, 7)) for _ in range(K)]
        if sum(raw) == 0:
            raw[0] = Fraction(1)
        tot = sum(raw)
        out.append(("random-%d" % r, [x / tot for x in raw]))
    # w_t = t * (do-nothing) + (1-t) * (uniform on the finest moves)
    finest = [i for i, mv in enumerate(moves) if all(bin(B).count("1") == 1 for B in mv)]
    nothing = [i for i, mv in enumerate(moves) if len(mv) == 1]
    assert len(nothing) == 1 and finest, "w_t needs the do-nothing and finest moves"
    for t in (Fraction(0), Fraction(1, 4), Fraction(1, 3), Fraction(1, 2),
              Fraction(3, 4), Fraction(1)):
        w = [Fraction(0)] * K
        w[nothing[0]] += t
        for i in finest:
            w[i] += (1 - t) / len(finest)
        out.append(("w_t t=%s" % t, w))
    # corners: all mass on a single move
    for pick in (0, K - 1):
        w = [Fraction(0)] * K
        w[pick] = Fraction(1)
        out.append(("point mass on move %d" % pick, w))
    return out


def main():
    rng = random.Random(SEED)
    print("=" * 78)
    print("THEOREM 4 HOLDS FOR EVERY WEIGHT -- the generality its own proof has")
    print("=" * 78)
    print(__doc__.strip())
    print()

    cache = {}
    print("-" * 78)
    print("A. the SPECTRUM against the actual transition matrix, exactly")
    print("-" * 78)
    print("For each (poset, weight): build M on L(P) from the action, then check")
    print("trace(M^k) = sum_X m_X lambda_X^k for k = 1..|L(P)|.  Equality for all k")
    print("forces the eigenvalue multiset to be exactly {lambda_X with multiplicity")
    print("m_X} (Newton's identities).  Exact rationals; no eigensolver.")
    print()
    checked = bad = 0
    per_n = {}
    for n in (3, 4):
        for P in all_posets(n):
            if P.is_chain():
                continue
            moves = all_moves(P)
            mult = multiplicities(P, cache)
            for name, w in weight_families(P, moves, rng):
                M, L = transition_matrix(P, moves, w)
                lam = lambdas(P, moves, w)
                ok, k, tr, want = power_sums_agree(M, lam, mult)
                checked += 1
                per_n[n] = per_n.get(n, 0) + 1
                if not ok:
                    bad += 1
                    print("   FAIL n=%d %s weight=%s at k=%d: %s != %s"
                          % (n, P.cover_string(), name, k, tr, want))
    print("   (poset, weight) cases: %d   [n=3: %d, n=4: %d]   FAILURES: %d"
          % (checked, per_n.get(3, 0), per_n.get(4, 0), bad))
    print()

    print("-" * 78)
    print("B. the IDENTITY lambda_2 = max over incomparable pairs of s(x,y)")
    print("-" * 78)
    print("lambda_2 := max { lambda_X : m_X > 0, X not the finest partition }, i.e.")
    print("the largest eigenvalue other than the stationary 1 = lambda_finest.")
    print()
    tot = 0
    fails = 0
    byn = {}
    nonuniform = 0
    for n in (3, 4, 5):
        for P in all_posets(n):
            if P.is_chain():
                continue
            moves = all_moves(P)
            mult = multiplicities(P, cache)
            for name, w in weight_families(P, moves, rng):
                lam = lambdas(P, moves, w)
                l2 = lambda_2(lam, mult)
                s = same_block_mass(P, moves, w)
                got = max(s.values())
                tot += 1
                byn[n] = byn.get(n, 0) + 1
                if name != "uniform-move":
                    nonuniform += 1
                if l2 != got:
                    fails += 1
                    if fails <= 10:
                        print("   FAIL n=%d %s weight=%s : lambda_2=%s max s=%s"
                              % (n, P.cover_string(), name, l2, got))
    print("   (poset, weight) cases: %d  [n=3: %d, n=4: %d, n=5: %d]"
          % (tot, byn.get(3, 0), byn.get(4, 0), byn.get(5, 0)))
    print("   of which the weight is NOT the uniform-move weight: %d" % nonuniform)
    print("   FAILURES: %d" % fails)
    print()
    print("-" * 78)
    print("C. what this buys, and it is not pedantry")
    print("-" * 78)
    print("Under w_t the identity reads lambda_2 = t = max_{x||y} s_{w_t}(x,y), which")
    print("is exactly the computation Theorem 7's proof does by hand -- so Theorem 7's")
    print("lambda_2 value is a special case of Theorem 4 once Theorem 4 is stated in")
    print("the generality it has.  Section 5.5's whole argument is about weights OTHER")
    print("than the uniform-move one, and the committed statement of Theorem 4 does not")
    print("reach them.")
    print()
    print("VERDICT: the weight hypothesis in Theorem 4 is removable.  %d cases, %d"
          % (tot, fails))
    print("failures, and the proof already established it.")
    return 0 if (bad == 0 and fails == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
