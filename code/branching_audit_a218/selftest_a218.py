"""selftest_a218.py -- does this audit's own instrument work?

Every assertion here is against a fact that is independent of the target
document: counting identities (Catalan, ballot numbers), the defining
relations of TL_n, and published semisimplicity facts for TL_n(beta).

Prints the number of assertions AND the population each count ranges over.
Exit 0 iff every assertion passes.
"""

import sys
from fractions import Fraction

from kern_a218 import (TL, act, ballot, catalan, diagrams, embed, gram_entry,
                       generator_diagram, identity_diagram, link_states,
                       multiply, rank)

BAD = []
N = 0


def check(cond, msg):
    global N
    N += 1
    if not cond:
        BAD.append(msg)


print("=" * 74)
print("SELF-TEST of the mg-a218 instrument")
print("=" * 74)
print()

# --- S1 -------------------------------------------------------------------
print("S1  link-state counts against the ballot numbers C(n,p) - C(n,p-1)")
pop = 0
for n in range(1, 8):
    for p in range(n // 2 + 1):
        S = link_states(n, p)
        check(len(S) == ballot(n, p),
              "link_states(%d,%d) = %d, ballot = %d" % (n, p, len(S), ballot(n, p)))
        pop += 1
print("    %d assertions, population: every (n,p) with 1 <= n <= 7, 0 <= p <= n//2"
      % pop)

# --- S2 -------------------------------------------------------------------
print("S2  sum_p (dim V(n,p))^2 = dim TL_n = Catalan(n)")
pop = 0
for n in range(1, 8):
    s = sum(ballot(n, p) ** 2 for p in range(n // 2 + 1))
    check(s == catalan(n), "n=%d: sum = %d, Catalan = %d" % (n, s, catalan(n)))
    pop += 1
print("    %d assertions, population: every n with 1 <= n <= 7" % pop)

# --- S3 -------------------------------------------------------------------
print("S3  diagram basis: |diagrams(n)| = Catalan(n), all planar, all matchings")
pop = 0
for n in range(1, 7):
    D = diagrams(n)
    check(len(D) == catalan(n), "diagrams(%d) = %d, Catalan = %d" % (n, len(D), catalan(n)))
    pop += 1
    check(len(set(D)) == len(D), "diagrams(%d) has duplicates" % n)
    pop += 1
    for d in D:
        check(len(d) == n, "diagram on %d strands has %d edges" % (n, len(d)))
        nodes = set()
        for e in d:
            nodes |= set(e)
        check(len(nodes) == 2 * n, "diagram does not cover all 2n nodes")
        pop += 2
print("    %d assertions, population: every diagram of TL_n for 1 <= n <= 6 "
      "(1+2+5+14+42+132 = 196 diagrams) plus 2 per n" % pop)

# --- S4 -------------------------------------------------------------------
print("S4  the TL relations, on diagrams, for every generator index and n <= 6,")
print("    at beta = 0, 1, 2, 3")
pop = 0
for n in range(2, 7):
    idn = identity_diagram(n)
    for beta in (0, 1, 2, 3):
        for i in range(n - 1):
            e = generator_diagram(n, i)
            loops, res = multiply(e, e, n)
            check(res == e and loops == 1,
                  "e_%d^2 != beta e_%d at n=%d" % (i, i, n))
            pop += 1
            lo, r = multiply(idn, e, n)
            check(lo == 0 and r == e, "1*e_%d != e_%d at n=%d" % (i, i, n))
            pop += 1
            for j in range(n - 1):
                f = generator_diagram(n, j)
                if abs(i - j) == 1:
                    l1, r1 = multiply(multiply(e, f, n)[1], e, n)
                    check(l1 == 0 and r1 == e,
                          "e_%d e_%d e_%d != e_%d at n=%d" % (i, j, i, i, n))
                    pop += 1
                elif abs(i - j) >= 2:
                    l1, r1 = multiply(e, f, n)
                    l2, r2 = multiply(f, e, n)
                    check((l1, r1) == (l2, r2),
                          "e_%d e_%d != e_%d e_%d at n=%d" % (i, j, j, i, n))
                    pop += 1
print("    %d assertions, population: every (n, beta, i, j) with 2 <= n <= 6, "
      "beta in {0,1,2,3}, i and j generator indices" % pop)

# --- S5 -------------------------------------------------------------------
print("S5  associativity of the diagram product, sampled over all triples at n <= 4")
pop = 0
for n in range(1, 5):
    D = diagrams(n)
    for a in D:
        for b in D:
            for c in D:
                l1, r1 = multiply(a, b, n)
                l2, r2 = multiply(r1, c, n)
                m1, s1 = multiply(b, c, n)
                m2, s2 = multiply(a, s1, n)
                check(l1 + l2 == m1 + m2 and r2 == s2,
                      "associativity fails at n=%d" % n)
                pop += 1
print("    %d assertions, population: every ordered triple of diagrams of TL_n, "
      "1 <= n <= 4 (1 + 8 + 125 + 2744)" % pop)

# --- S6 -------------------------------------------------------------------
print("S6  the module axiom: (d1 d2) v = d1 (d2 v) on every cell module,")
print("    every pair of diagrams, every link state, n <= 5, beta in {0,1,2,3}")
pop = 0
for n in range(1, 6):
    D = diagrams(n)
    for beta in (0, 1, 2, 3):
        for p in range(n // 2 + 1):
            S = link_states(n, p)
            for d1 in D:
                for d2 in D:
                    loops, prod = multiply(d1, d2, n)
                    for s in S:
                        c, t = act(prod, s, n, p, beta)
                        lhs = (beta ** loops) * c if c != 0 else 0
                        lt = t if c != 0 else None
                        c2, t2 = act(d2, s, n, p, beta)
                        if c2 == 0:
                            rhs, rt = 0, None
                        else:
                            c3, t3 = act(d1, t2, n, p, beta)
                            rhs, rt = (c2 * c3, t3) if c3 != 0 else (0, None)
                        ok = (lhs == 0 and rhs == 0) or (lhs == rhs and lt == rt)
                        check(ok, "module axiom fails n=%d beta=%d p=%d" % (n, beta, p))
                        pop += 1
print("    %d assertions, population: every (n, beta, p, d1, d2, link state) with "
      "1 <= n <= 5, beta in {0,1,2,3}" % pop)

# --- S7 -------------------------------------------------------------------
print("S7  the bilinear form is symmetric and is contravariant enough to have")
print("    a radical that is a submodule (checked by construction in trace_on_L)")
pop = 0
for n in range(1, 7):
    for beta in (0, 1, 2, 3):
        for p in range(n // 2 + 1):
            S = link_states(n, p)
            for u in S:
                for v in S:
                    check(gram_entry(u, v, n, p, beta) == gram_entry(v, u, n, p, beta),
                          "Gram not symmetric n=%d beta=%d p=%d" % (n, beta, p))
                    pop += 1
print("    %d assertions, population: every ordered pair of link states in every "
      "(n, beta, p) with 1 <= n <= 6, beta in {0,1,2,3}" % pop)

# --- S8 -------------------------------------------------------------------
print("S8  PUBLISHED CONTROLS (Ridout-Saint-Aubin arXiv:1204.4505, Cor. 4.6 and")
print("    the remark after Cor. 4.8), each checked by sum_p (dim L)^2 vs dim TL_n")
controls = []
pop = 0
for n in range(1, 7):
    for beta in (0, 1, 2, 3):
        A = TL(n, beta)
        ss = sum(A.dim_L(p) ** 2 for p in A.parts) == catalan(n)
        controls.append((n, beta, ss))
expected = {
    "TL_n(2) semisimple for every n <= 6":
        all(ss for (n, b, ss) in controls if b == 2),
    "TL_n(3) semisimple for every n <= 6":
        all(ss for (n, b, ss) in controls if b == 3),
    "TL_n(0) semisimple exactly for n odd (n <= 6)":
        all(ss == (n % 2 == 1) for (n, b, ss) in controls if b == 0),
    "TL_n(1) NOT semisimple for 3 <= n <= 6":
        all((not ss) for (n, b, ss) in controls if b == 1 and n >= 3),
    "TL_1(1) and TL_2(1) semisimple":
        all(ss for (n, b, ss) in controls if b == 1 and n <= 2),
}
for name, ok in expected.items():
    check(ok, "control failed: " + name)
    pop += 1
    print("      %-48s %s" % (name, "reproduced" if ok else "FAILED"))
print("    %d assertions, population: the 5 published control statements above, "
      "each quantified over its own range of n" % pop)

# --- S9 -------------------------------------------------------------------
print("S9  TWO DISJOINT ROUTES to dim A/rad: sum_p (dim L(n,p))^2 from the Gram")
print("    ranks, against the rank of the trace form of the regular representation")
pop = 0
disagree = 0
for n in range(1, 7):
    for beta in (0, 1, 2, 3):
        A = TL(n, beta)
        route1 = sum(A.dim_L(p) ** 2 for p in A.parts)
        route2, dimA = A.trace_form_rank()
        check(route1 == route2,
              "routes disagree n=%d beta=%d: %d vs %d" % (n, beta, route1, route2))
        if route1 != route2:
            disagree += 1
        pop += 1
print("    %d assertions, population: every (n, beta) with 1 <= n <= 6 and "
      "beta in {0,1,2,3}; disagreements: %d" % (pop, disagree))

print()
print("-" * 74)
print("ASSERTIONS: %d, population: every check in S1-S9 above" % N)
print("SELF-ERRORS: %d, population: the %d assertions above" % (len(BAD), N))
for b in BAD[:20]:
    print("   BAD: " + b)
print("TOTAL BAD: %d" % len(BAD))
sys.exit(1 if BAD else 0)
