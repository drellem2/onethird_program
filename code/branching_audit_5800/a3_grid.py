"""A3 -- X2, the grid, and the negatives that survive around it.

mg-41aa's replacement claim: Brown's worked p x q grid IS the interval
[(q), (q+p, q)] of Young's lattice.  Three separate objects are built from
three separate definitions and compared:

  G   = the product of integer intervals {0..p} x {0..q}     (no J, no cells)
  JC  = J(C_p + C_q), ideals of a disjoint union of chains
  I   = [(q), (q+p,q)] as PARTITIONS under containment       (no cells)

and the surviving NEGATIVES are attacked:

  N1  "C_p + C_q is a straight cell poset D_lam in 0 of 25 cases"
  N2  the grid is not [0, lam] for ANY lam -- checked over every lam of the
      right size, not just the reason
"""
import sys
from kern5800 import (canon, ideals, ideal_lattice, interval_poset,
                      partitions_between, straight_shapes, skew_cell_poset,
                      shape_to_mu_lam, skew_shapes)

PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6

print("=" * 78)
print("A3  X2 -- THE GRID, AND WHAT IS STILL NEGATIVE AROUND IT")
print("=" * 78)


def grid(p, q):
    """{0..p} x {0..q} built directly as a product of two integer intervals."""
    els = [(a, b) for a in range(p + 1) for b in range(q + 1)]
    n = len(els)
    pos = {e: i for i, e in enumerate(els)}
    up = [0] * n
    for e in els:
        for f in els:
            if e != f and e[0] <= f[0] and e[1] <= f[1]:
                up[pos[e]] |= 1 << pos[f]
    return n, tuple(up), els


def chain_sum(p, q):
    """C_p + C_q as a poset on p+q elements: 0<..<p-1 and p<..<p+q-1."""
    n = p + q
    up = [0] * n
    for i in range(p):
        for j in range(i + 1, p):
            up[i] |= 1 << j
    for i in range(p, n):
        for j in range(i + 1, n):
            up[i] |= 1 << j
    return n, tuple(up)


print("\n[R3] THREE CONSTRUCTIONS COMPARED, p,q = 1..%d" % PMAX)
bad_gj = bad_gi = bad_size = 0
npairs = 0
for p in range(1, PMAX + 1):
    for q in range(1, PMAX + 1):
        npairs += 1
        gn, gup, _ = grid(p, q)
        cn, cup = chain_sum(p, q)
        jn, jup, _ = ideal_lattice(cn, cup)
        mu, lam = (q,), (q + p, q)
        inn, iup, iels = interval_poset(mu, lam)
        if canon(gn, gup) != canon(jn, jup):
            bad_gj += 1
        if canon(gn, gup) != canon(inn, iup):
            bad_gi += 1
            print("   BAD p=%d q=%d: grid !~ [%s,%s]" % (p, q, mu, lam))
        if inn != (p + 1) * (q + 1):
            bad_size += 1
            print("   BAD p=%d q=%d: |[mu,lam]| = %d, expected %d"
                  % (p, q, inn, (p + 1) * (q + 1)))
print("  pairs: %d" % npairs)
print("  grid !~ J(C_p + C_q):            %d" % bad_gj)
print("  grid !~ [(q),(q+p,q)]:           %d   <-- the constructed claim" % bad_gi)
print("  |[mu,lam]| != (p+1)(q+1):        %d" % bad_size)

# also: the skew shape (q+p,q)/(q) really is C_p + C_q as a CELL poset
bad_cell = 0
for p in range(1, PMAX + 1):
    for q in range(1, PMAX + 1):
        sh = ((q, q + p), (0, q))
        k, kup = skew_cell_poset(sh)
        cn, cup = chain_sum(p, q)
        if (k, canon(k, kup)) != (cn, canon(cn, cup)):
            bad_cell += 1
print("  cell poset of (q+p,q)/(q) !~ C_p + C_q:  %d" % bad_cell)

# ------------------------------------------------- N1: the surviving negative

print("\n[N1] THE SURVIVING NEGATIVE -- 'C_p + C_q is a straight cell poset in 0 of N'")
print("  attacked by CONSTRUCTION: every lam of the right size is built and")
print("  compared, not just the ones a reason rules out.")
hits = 0
tested = 0
for p in range(1, PMAX + 1):
    for q in range(1, PMAX + 1):
        cn, cup = chain_sum(p, q)
        target = canon(cn, cup)
        straight = {canon(*skew_cell_poset(s)) for s in straight_shapes(p + q)}
        tested += 1
        if target in straight:
            hits += 1
            print("   HIT p=%d q=%d: C_p + C_q IS some D_lam" % (p, q))
print("  pairs tested: %d;  C_p + C_q is a straight cell poset in %d of them" % (tested, hits))
print("  (reason, independent of the measurement: D_lam contains the cell (1,1),")
print("   which is below every cell, so D_lam has a MINIMUM; C_p + C_q with")
print("   p,q >= 1 has two minimal elements.  The measurement agrees.)")

# ------------------------------------------------ N2: not [0,lam] for ANY lam

print("\n[N2] THE GRID IS NOT [0,lam] FOR ANY lam -- checked over every lam,")
print("  which is more than the struck sentence's reason established.")
hits2 = 0
for p in range(1, min(PMAX, 5) + 1):
    for q in range(1, min(PMAX, 5) + 1):
        gn, gup, _ = grid(p, q)
        g = canon(gn, gup)
        for sh in straight_shapes(p + q):
            mu, lam = shape_to_mu_lam(sh)
            m, up, _ = interval_poset(mu, lam)
            if canon(m, up) == g:
                hits2 += 1
                print("   HIT p=%d q=%d lam=%s" % (p, q, lam))
print("  grid ~ [0,lam] for some lam: %d of %d pairs" % (hits2, min(PMAX, 5) ** 2))

# ------------------------------- and the grid IS an interval [mu,lam], p,q>=1

print("\n[N2'] ... AND YET IT IS AN INTERVAL [mu,lam].  Both halves at once:")
for p, q in [(1, 1), (2, 3), (3, 3), (5, 5)]:
    if p > PMAX or q > PMAX:
        continue
    gn, gup, _ = grid(p, q)
    m, up, els = interval_poset((q,), (q + p, q))
    print("  p=%d q=%d: |grid|=%d  |[(%d),(%d,%d)]|=%d  isomorphic: %s"
          % (p, q, gn, q, q + p, q, m, canon(gn, gup) == canon(m, up)))

print("\nSUMMARY a3_grid: pairs %d; grid!~J(C+C) %d; grid!~[(q),(q+p,q)] %d; "
      "size wrong %d; cell-poset mismatch %d; C_p+C_q straight-hits %d; "
      "grid-is-[0,lam] hits %d"
      % (npairs, bad_gj, bad_gi, bad_size, bad_cell, hits, hits2))
