"""T3 -- BIDIGARE'S THEOREM, TESTED AS AN EQUALITY.

mg-af28 section 2.6 named this bridge and did not follow it:

    "Bidigare's theorem ... is the documented route from face-monoid algebras
     into the Hopf/tower programme ... (as stated in the secondary literature;
     I did not read Bidigare's thesis)"

Aguiar-Mahajan state it as Theorem 10.13 of "Monoidal Functors, Species and
Hopf Algebras":

    "Theorem 10.13 (Bidigare).  The descent algebra is isomorphic to
     (Sigma[n]^{S_n})^op."

and define the descent algebra in Section 10.8.1 as the span of

    d_T := sum over { w : des(w) subset T } of w,      T subset [n-1].

This file BUILDS both algebras from those definitions and compares them
structure constant by structure constant.  Nothing is cited into the
comparison: the descent algebra is built inside kS_n from permutations, the
invariant algebra is built inside kSigma_n from set compositions, and the two
never share a line of code.

  T3a  S_n-orbits of set compositions of [n] ARE the compositions of n, with
       |O_alpha| the multinomial coefficient.
  T3b  The orbit sums span a SUBALGEBRA: O_alpha . O_beta is constant on
       orbits.  dim = 2^(n-1).
  T3c  The d_T span a subalgebra of kS_n (Solomon).  dim = 2^(n-1).
       |{w : des(w) subset T(alpha)}| = |O_alpha|.
  T3d  THE COMPARISON.  Four candidate identifications are run --
       {isomorphism, anti-isomorphism} x {two composition conventions in kS_n}
       -- and exactly which ones hold is reported.  Three of the four are the
       control: if the harness cannot separate them, T3d proves nothing.
"""

import sys
from math import factorial
from itertools import permutations
from collections import Counter
from fractions import Fraction
from kern7d75 import set_compositions, sc_product, compositions

NMAX = 5
bad = 0


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)


def _prod(xs):
    r = 1
    for x in xs:
        r *= x
    return r


def comp_of(F):
    return tuple(len(B) for B in F)


def subset_of_comp(alpha):
    out = []
    s = 0
    for a in alpha[:-1]:
        s += a
        out.append(s)
    return frozenset(out)


def descents(w):
    return frozenset(i for i in range(1, len(w)) if w[i - 1] > w[i])


hdr("T3a  S_n-orbits of set compositions = compositions of n")
print()
print("   n  |Sigma_n|  #orbits  #compositions  2^(n-1)  orbit sizes ="
      " multinomial")
for n in range(1, NMAX + 1):
    SC = set_compositions(n)
    orb = Counter(comp_of(F) for F in SC)
    comps = compositions(n)
    ok1 = set(orb) == set(comps)
    ok2 = all(orb[a] == factorial(n) // 1 // _prod(factorial(x) for x in a)
              for a in comps) if True else False
    bad += (not ok1) + (not ok2) + (len(comps) != 2 ** (n - 1))
    print("  %2d %10d %8d %14d %8d  %s"
          % (n, len(SC), len(orb), len(comps), 2 ** (n - 1),
             "yes" if (ok1 and ok2) else "NO"))
print()

hdr("T3b  the orbit sums span a subalgebra of kSigma_n -- structure constants")
print()
SIG = {}
for n in range(1, NMAX + 1):
    SC = set_compositions(n)
    comp = {F: comp_of(F) for F in SC}
    by = {}
    for F in SC:
        by.setdefault(comp[F], []).append(F)
    comps = sorted(by)
    # tally[(a,b)][H] = number of (F,G) in O_a x O_b with F.G = H
    tally = {}
    for a in comps:
        for b in comps:
            tally[(a, b)] = Counter()
    for F in SC:
        ca = comp[F]
        for G in SC:
            tally[(ca, comp[G])][sc_product(F, G)] += 1
    notconst = 0
    C = {}
    for a in comps:
        for b in comps:
            t = tally[(a, b)]
            row = Counter()
            for g in comps:
                vals = {t[H] for H in by[g]}
                if len(vals) > 1:
                    notconst += 1
                row[g] = t[by[g][0]]
            C[(a, b)] = row
    SIG[n] = (comps, C)
    bad += notconst
    print("  n=%d  |Sigma_n|=%-5d #orbits=%-3d  products not constant on"
          " orbits: %d" % (n, len(SC), len(comps), notconst))
print()
print("  Constant on orbits for every pair, at every n <= %d: the orbit sums"
      % NMAX)
print("  do span a subalgebra, and its structure constants are the C below.")
print()

hdr("T3c  Solomon's descent algebra, built inside kS_n")
print()
SOL = {}
print("   n  |S_n|  #subsets T  d_T closed under product  |{w:des(w)<=T}| ="
      " |O_alpha|")
for n in range(1, NMAX + 1):
    W = list(permutations(range(1, n + 1)))
    des = {w: descents(w) for w in W}
    subs = []
    for m in range(1 << (n - 1)):
        subs.append(frozenset(i + 1 for i in range(n - 1) if m >> i & 1))
    subs = sorted(subs, key=lambda T: (len(T), sorted(T)))
    members = {T: [w for w in W if des[w] <= T] for T in subs}
    idx = {w: i for i, w in enumerate(W)}
    # two composition conventions
    def mulA(u, v):        # (u.v)(i) = u(v(i))
        return tuple(u[v[i] - 1] for i in range(n))

    def mulB(u, v):        # (u.v)(i) = v(u(i))
        return tuple(v[u[i] - 1] for i in range(n))

    tabs = {}
    for name, mul in (("A", mulA), ("B", mulB)):
        C = {}
        closed = True
        for S in subs:
            for T in subs:
                acc = Counter()
                for u in members[S]:
                    for v in members[T]:
                        acc[mul(u, v)] += 1
                # express acc in the d_U basis.  d_U = sum_{des(w) <= U} w,
                # so the coefficient of w in sum_U r_U d_U depends on w only
                # through des(w).  Hence acc must be CONSTANT on each descent
                # class -- checked, not assumed (the first version of this
                # file summed over the class instead, and T3c reported the
                # descent algebra as not closed, which is how it was caught).
                exact = {}
                for V in subs:
                    vals = {acc[w] for w in W if des[w] == V}
                    if len(vals) != 1:
                        closed = False
                        exact[V] = None
                    else:
                        exact[V] = vals.pop()
                if any(v is None for v in exact.values()):
                    C[(S, T)] = Counter()
                    continue
                r = {}
                for U in sorted(subs, key=lambda X: -len(X)):
                    r[U] = exact[U] - sum(r[X] for X in subs if U < X)
                chk = Counter()
                for U in subs:
                    if r[U]:
                        for w in members[U]:
                            chk[w] += r[U]
                if chk != Counter({k: v for k, v in acc.items() if v}):
                    closed = False
                row = Counter({U: r[U] for U in subs if r[U]})
                C[(S, T)] = row
        tabs[name] = (C, closed)
    SOL[n] = (subs, tabs, members)
    sizes_ok = all(len(members[subset_of_comp(a)]) ==
                   factorial(n) // _prod(factorial(x) for x in a)
                   for a in compositions(n))
    bad += (not tabs["A"][1]) + (not tabs["B"][1]) + (not sizes_ok)
    print("  %2d %6d %11d  A:%-5s B:%-5s %35s"
          % (n, len(W), len(subs), tabs["A"][1], tabs["B"][1],
             "yes" if sizes_ok else "NO"))
print()

hdr("T3d  THE COMPARISON -- four candidate identifications, three are controls")
print()
print("  Candidate: O_alpha  <->  d_{T(alpha)}.")
print("  iso  : c^gamma_{alpha,beta}(Sigma) = c^gamma_{alpha,beta}(Sol)")
print("  anti : c^gamma_{alpha,beta}(Sigma) = c^gamma_{beta,alpha}(Sol)")
print("  crossed with the two composition conventions A and B in kS_n.")
print()
print("   n   iso/A  anti/A   iso/B  anti/B      (mismatching pairs)")
res = {}
for n in range(1, NMAX + 1):
    comps, C = SIG[n]
    subs, tabs, _ = SOL[n]
    line = []
    for conv in ("A", "B"):
        D = tabs[conv][0]
        for mode in ("iso", "anti"):
            miss = 0
            for a in comps:
                for b in comps:
                    S, T = subset_of_comp(a), subset_of_comp(b)
                    lhs = C[(a, b)]
                    rhs = D[(S, T)] if mode == "iso" else D[(T, S)]
                    for g in comps:
                        if lhs[g] != rhs.get(subset_of_comp(g), 0):
                            miss += 1
            line.append(miss)
            res[(n, conv, mode)] = miss
    print("  %2d %7d %7d %7d %7d" % (n, line[0], line[1], line[2], line[3]))
print()
holds = [(c, m) for c in ("A", "B") for m in ("iso", "anti")
         if all(res[(n, c, m)] == 0 for n in range(2, NMAX + 1))]
fails = [(c, m) for c in ("A", "B") for m in ("iso", "anti")
         if any(res[(n, c, m)] != 0 for n in range(2, NMAX + 1))]
print("  HOLDS at every n in 2..%d: %s" % (NMAX, holds if holds else "NONE"))
print("  FAILS somewhere            : %s" % (fails if fails else "NONE"))
print()
if not holds:
    print("  NO identification holds -- Bidigare's theorem is NOT reproduced")
    print("  by this construction of the two algebras.")
    bad += 1
elif not fails:
    print("  ALL FOUR hold, so the comparison is VACUOUS -- the three controls")
    print("  did not fire and T3d establishes nothing.")
    bad += 1
else:
    print("  %d of 4 hold and %d fail, so the comparison is discriminating."
          % (len(holds), len(fails)))
    print("  Bidigare's Theorem 10.13 is REPRODUCED here from the two")
    print("  definitions, with no step taken on the theorem's authority.")
print()
print("=" * 78)
print("T3 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
