#!/usr/bin/env python3
r"""
IDENTIFICATION CHECK 3, not new mathematics.

Brown, "Semigroups, rings, and Markov chains" (2000), section 4.3, verbatim:

  "If L is a finite distributive lattice, there is a LRB S whose elements are
   chains 0 = x_0 < x_1 < ... < x_l = 1.  To construct the product of two such
   chains, we use the second factor to refine the first ...  We can therefore
   use the results of Section 4.2 to analyze a random walk on the maximal
   chains of L, driven by weights on arbitrary chains."

Take L = J(P), the lattice of order ideals of P (every finite distributive
lattice is of this form, by Birkhoff).  This script checks that Brown's S is
the programme's monoid F(P) of P-compatible ordered set partitions, ON THE
NOSE -- same elements, same product, same chambers.

  C1  the map  (x_0 < ... < x_l)  |-->  (x_1\x_0, x_2\x_1, ..., x_l\x_{l-1})
      is a BIJECTION from the set of 0-to-1 chains in J(P) onto the set of
      P-compatible ordered set partitions of P.
  C2  it carries Brown's product ("use the second factor to refine the first")
      to the programme's product (blockwise intersection, ordered
      lexicographically by (block of x, block of y)).
  C3  it carries the MAXIMAL chains of J(P) onto the one-block-per-element
      partitions, i.e. onto the linear extensions of P.

If C1-C3 hold then the programme's monoid, product, and state space are the
ones Brown names in section 4.3, and its spectral theorem is his Theorem 2 via
his section 4.2 -- which is what the accompanying landscape document reports.

Self-contained apart from poset/partition plumbing imported from
identify_lattice.py.  Exact combinatorics, no floating point.
"""

import sys

from identify_lattice import (transitive_closure, iso_classes,
                              linear_extensions, is_connected)


# ------------------------------------------------------- the two objects ----

def order_ideals(n, rel):
    """All down-sets of P, as frozensets."""
    below = {j: {i for (i, jj) in rel if jj == j} for j in range(n)}
    out = []
    for mask in range(1 << n):
        S = {i for i in range(n) if mask >> i & 1}
        if all(below[j] <= S for j in S):
            out.append(frozenset(S))
    return out


def chains_0_to_1(n, rel):
    """All chains 0hat = x_0 < x_1 < ... < x_l = 1hat in J(P), as tuples of
    ideals.  l >= 1 except for n = 0."""
    ideals = sorted(order_ideals(n, rel), key=lambda s: (len(s), sorted(s)))
    top = frozenset(range(n))
    bot = frozenset()
    out = []

    def rec(cur):
        if cur[-1] == top:
            out.append(tuple(cur))
            return
        for I in ideals:
            if cur[-1] < I:
                rec(cur + [I])

    rec([bot])
    return out


def p_compatible_ordered_partitions(n, rel):
    """The programme's moves: ordered set partitions (B_1,...,B_k) of [n] such
    that i < j in P implies block(i) <= block(j)."""
    out = []

    def rec(remaining, acc):
        if not remaining:
            out.append(tuple(acc))
            return
        elts = sorted(remaining)
        # every nonempty subset of the remaining elements as the next block
        for mask in range(1, 1 << len(elts)):
            B = frozenset(elts[k] for k in range(len(elts)) if mask >> k & 1)
            rest = remaining - B
            # compatibility: nothing in rest may be strictly below anything in B
            ok = True
            for (a, b) in rel:
                if b in B and a in rest:
                    ok = False
                    break
            if ok:
                rec(rest, acc + [B])

    rec(frozenset(range(n)), [])
    return out


# ---------------------------------------------------------- the two maps ----

def chain_to_partition(chain):
    return tuple(chain[i + 1] - chain[i] for i in range(len(chain) - 1))


def partition_to_chain(pi):
    cur = frozenset()
    out = [cur]
    for B in pi:
        cur = cur | B
        out.append(cur)
    return tuple(out)


# ------------------------------------------------------------- products -----

def programme_product(x, y):
    """The programme's product: non-empty intersections B_p & C_q, ordered
    lexicographically by (p, q).  'y first, then x' in the note's phrasing."""
    out = []
    for B in x:
        for C in y:
            I = B & C
            if I:
                out.append(I)
    return tuple(out)


def brown_product(chain_x, chain_y):
    """Brown's product in section 4.3: 'use the second factor to refine the
    first'.  The chain x is refined by inserting, inside each step
    x_{p-1} < x_p, the intermediate ideals x_{p-1} | (x_p & y_q) for
    q = 1..l(y), keeping only strict increases."""
    out = [chain_x[0]]
    for p in range(1, len(chain_x)):
        lo, hi = chain_x[p - 1], chain_x[p]
        for q in range(1, len(chain_y)):
            z = lo | (hi & chain_y[q])
            if z != out[-1]:
                out.append(z)
        if out[-1] != hi:
            out.append(hi)
    return tuple(out)


# ---------------------------------------------------------------- checks ----

def analyse(n, verbose=False):
    res = {'classes': 0, 'C1_bad': 0, 'C2_bad': 0, 'C2_pairs': 0,
           'C3_bad': 0, 'moves': 0}
    for rel in iso_classes(n):
        res['classes'] += 1
        chains = chains_0_to_1(n, rel)
        moves = p_compatible_ordered_partitions(n, rel)
        res['moves'] += len(moves)

        # ---- C1: bijection
        img = [chain_to_partition(c) for c in chains]
        if len(set(img)) != len(img) or set(img) != set(moves):
            res['C1_bad'] += 1
            print("  C1 FAIL n=%d rel=%s |chains|=%d |moves|=%d"
                  % (n, sorted(rel), len(chains), len(moves)), file=sys.stderr)
            continue
        # and the inverse map really inverts
        if any(partition_to_chain(chain_to_partition(c)) != c for c in chains):
            res['C1_bad'] += 1
            print("  C1 INVERSE FAIL n=%d" % n, file=sys.stderr)
            continue

        # ---- C2: the products correspond
        bad2 = False
        for cx in chains:
            for cy in chains:
                res['C2_pairs'] += 1
                lhs = chain_to_partition(brown_product(cx, cy))
                rhs = programme_product(chain_to_partition(cx),
                                        chain_to_partition(cy))
                if lhs != rhs:
                    bad2 = True
                    if verbose:
                        print("     C2 %s * %s : brown=%s programme=%s"
                              % (cx, cy, lhs, rhs), file=sys.stderr)
        if bad2:
            res['C2_bad'] += 1
            print("  C2 FAIL n=%d rel=%s" % (n, sorted(rel)), file=sys.stderr)

        # ---- C3: maximal chains <-> linear extensions
        maximal = [c for c in chains if len(c) == n + 1]
        les = linear_extensions(n, rel)
        as_words = set()
        for c in maximal:
            pi = chain_to_partition(c)
            as_words.add(tuple(next(iter(B)) for B in pi))
        if as_words != {tuple(w) for w in les}:
            res['C3_bad'] += 1
            print("  C3 FAIL n=%d rel=%s" % (n, sorted(rel)), file=sys.stderr)
    return res


def worked_example():
    n = 4
    rel = transitive_closure(n, {(0, 1), (2, 3)})
    names = "abcd"
    chains = chains_0_to_1(n, rel)
    moves = p_compatible_ordered_partitions(n, rel)
    maximal = [c for c in chains if len(c) == n + 1]
    print()
    print("The worked example P = {a<b, c<d}")
    print("  chains 0->1 in J(P)                 : %d" % len(chains))
    print("  P-compatible ordered partitions     : %d   (the note says 26)  %s"
          % (len(moves), "OK" if len(moves) == 26 else "MISMATCH"))
    print("  maximal chains in J(P)              : %d" % len(maximal))
    print("  linear extensions of P              : %d   (the note says 6)   %s"
          % (len(linear_extensions(n, rel)),
             "OK" if len(linear_extensions(n, rel)) == 6 else "MISMATCH"))
    print("  |J(P)| (order ideals)               : %d" % len(order_ideals(n, rel)))
    print()
    print("  A sample product, both ways (x = (ac|bd), y = (a|b|cd)):")
    x = (frozenset({0, 2}), frozenset({1, 3}))
    y = (frozenset({0}), frozenset({1}), frozenset({2, 3}))
    cx, cy = partition_to_chain(x), partition_to_chain(y)
    lhs = chain_to_partition(brown_product(cx, cy))
    rhs = programme_product(x, y)

    def show(pi):
        return "|".join("".join(names[i] for i in sorted(B)) for B in pi)
    print("    Brown  (refine chain x by chain y) : %s" % show(lhs))
    print("    note   (blockwise intersection)    : %s" % show(rhs))
    print("    agree: %s" % ("YES" if lhs == rhs else "NO"))


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print("=" * 78)
    print("IDENTIFICATION CHECK 3: is the programme's monoid F(P) the LRB that")
    print("Brown names in section 4.3 -- chains in the distributive lattice")
    print("J(P), multiplied by refining the first factor by the second?")
    print("Brown, J. Theoret. Probab. 13 (2000) 871-938, arXiv:math/0006145.")
    print("=" * 78)
    print()
    print("%-4s %-9s %-10s %-22s %-24s %-20s" %
          ("n", "classes", "moves", "C1 chains <-> moves",
           "C2 products correspond", "C3 max <-> lin ext"))
    for n in range(1, nmax + 1):
        r = analyse(n)
        print("%-4d %-9d %-10d %-22s %-24s %-20s" % (
            n, r['classes'], r['moves'],
            "%d bad of %d" % (r['C1_bad'], r['classes']),
            "%d bad of %d pairs" % (r['C2_bad'], r['C2_pairs']),
            "%d bad of %d" % (r['C3_bad'], r['classes'])))
    worked_example()
    print()
    print("=" * 78)
    print("0 bad throughout means F(P) is not merely LIKE Brown's section-4.3")
    print("left regular band: it IS it, under the ideal-difference bijection.")
    print("=" * 78)


if __name__ == '__main__':
    main()
