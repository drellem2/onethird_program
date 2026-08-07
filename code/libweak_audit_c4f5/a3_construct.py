#!/usr/bin/env python3
"""a3_construct — AUDIT TARGET 3: DEMAND THE CANDIDATE SPACE AND BUILD WHAT IT FORBIDS.

mg-c3ca's Sec.3 verdict is a NEGATIVE about a BLOCKER:

    "(LIB-weak) is NOT blocked by the arc's named obstruction. The obstruction lives at
     O(1) crossers. (LIB-weak) does not notice a configuration until Theta(n) of them
     occur SIMULTANEOUSLY -- a hypothesis a factor n stronger than anything the
     obstruction supplies. The corpus's own evidence points the other way at that scale:
     width-3 caps simultaneous deep crossings at boundedly many per shared chain
     (Bwall Sec.4), and mg-a1ec Prop. 5.3 says (B) fails only via a FEW elements."

So the object the last sentence says the corpus argues against is:
    Theta(n) elements, each of Theta(n) inversion mass, simultaneously.

THIS FILE BUILDS IT.  Three times, exactly, with no sampling.

P20 (filed in advance) warns me off the error of reading Sec.3 as a claim that no such
object EXISTS.  It is not.  Sec.3 claims the obstruction does not TRANSFER.  What is
tested here is the SUPPORTING SENTENCE, which is a different and weaker thing than the
verdict it supports -- and the two are worth separating precisely because a reader takes
the support as evidence for the verdict.
"""
import sys
from fractions import Fraction
import lib_c4f5 as L

print("=" * 78)
print("a3_construct -- building the Theta(n)-elements-of-Theta(n)-mass configuration")
print("EXACT integer/Fraction arithmetic throughout.  No sampling. No tolerance.")
print("=" * 78)

print()
print("-" * 78)
print("A. CONSTRUCTION 1 -- C_p (+) A_q : q free points sharing ONE p-chain")
print("-" * 78)
print("This is precisely `q elements each block-crossing the SAME Theta(n) chain`.")
print("%4s %3s %3s %10s %10s %12s %12s %10s" %
      ("n", "p", "q", "e(P)", "delta", "E_maj", "E_maj/n^2", "#m_x>=n/4"))
for k in (2, 3, 4, 5, 6, 7):
    p = q = k
    n = p + q
    P = L.chain_plus_antichain(p, q)
    a = L.analyse(P)
    mm = L.m_maj(a)
    em = L.E_maj(a)
    big = sum(1 for v in mm if v >= Fraction(n, 4))
    print("%4d %3d %3d %10d %10s %12s %12.5f %10d"
          % (n, p, q, a["eP"], a["delta"], em, float(em) / (n * n), big))
print()
print("VERDICT A: the configuration EXISTS as a poset, at every size, exactly.")
print("  delta = 1/2 at every size -- maximally UNFROZEN, because the q free points are")
print("  mutually exchangeable.  So the object exists and is not a counterexample.")

print()
print("-" * 78)
print("B. CONSTRUCTION 2 -- C_p (+) C_q : the same mobility with NO free pair")
print("-" * 78)
print("Construction 1's delta = 1/2 comes entirely from the free-free pairs.  Remove")
print("them by making the mobile elements a CHAIN.  Every element of the shorter chain")
print("is still incomparable to the whole of the longer one, so the mobility survives.")
print("%4s %3s %3s %12s %10s %12s %12s %10s" %
      ("n", "p", "q", "e(P)", "delta", "E_maj", "E_maj/n^2", "#m_x>=n/4"))
for k in (2, 3, 4, 5, 6, 7, 8, 9, 10):
    p = q = k
    n = p + q
    P = L.two_chains(p, q)
    a = L.analyse(P)
    mm = L.m_maj(a)
    em = L.E_maj(a)
    big = sum(1 for v in mm if v >= Fraction(n, 4))
    print("%4d %3d %3d %12d %10s %12s %12.5f %10d"
          % (n, p, q, a["eP"], a["delta"], em, float(em) / (n * n), big))
print()
print("VERDICT B: still delta = 1/2, and now for a DIFFERENT reason -- the two middle")
print("  elements of the two chains are exchangeable by the reflection symmetry.")
print("  E_maj/n^2 is bounded away from 0 and every element has Theta(n) mass.")

print()
print("-" * 78)
print("C. CONSTRUCTION 3 -- BREAK THE SYMMETRY: C_p (+) C_q with p != q")
print("-" * 78)
print("If delta = 1/2 is forced by a symmetry, an asymmetric pair of chains should")
print("push it down.  How far does it go, and what does E_maj/n^2 do as it falls?")
print("%4s %3s %3s %10s %12s %12s" % ("n", "p", "q", "delta", "E_maj", "E_maj/n^2"))
rows = []
for n in range(4, 15):
    best = None
    for p in range(1, n):
        q = n - p
        P = L.two_chains(p, q)
        a = L.analyse(P)
        if a["delta"] is None:
            continue
        em = L.E_maj(a)
        if best is None or a["delta"] < best[0]:
            best = (a["delta"], p, q, em)
    d, p, q, em = best
    rows.append((n, float(d), float(em) / (n * n)))
    print("%4d %3d %3d %10s %12s %12.5f" % (n, p, q, d, em, float(em) / (n * n)))
print()
print("VERDICT C: the minimum delta over two-chain posets stays at or near 1/2.")
print("  Two chains cannot get near frozen. The mobility is real; the freezing is not.")

print()
print("-" * 78)
print("D. THE FRONTIER -- max E_maj/n^2 AS A FUNCTION OF A CEILING ON delta")
print("-" * 78)
print("This is the measurement that decides whether Theta(n) mass and near-freezing can")
print("COEXIST, and it is not in mg-c3ca: its Sec.6 reports max E_maj on the family at")
print("the MINIMUM delta only, which is one point of this curve.")
print()
print("If max E_maj/n^2 stays bounded away from 0 as the delta ceiling falls toward 1/3,")
print("(LIB-weak) is under threat at reachable n.  If it collapses, (LIB-weak) looks safe")
print("at reachable n -- which is EVIDENCE ABOUT THE BOUNDARY and not about the limit.")
print()
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
CEILS = [Fraction(1, 2), Fraction(9, 20), Fraction(2, 5), Fraction(3, 8),
         Fraction(7, 20), Fraction(17, 50), Fraction(1, 3)]
print("%5s" % "n", end="")
for c in CEILS:
    print("%12s" % ("<=%s" % c), end="")
print()
for n in range(3, NMAX + 1):
    best = {c: None for c in CEILS}
    cnt = {c: 0 for c in CEILS}
    for P in L.gen_natural_posets(n):
        a = L.analyse(P)
        if a["delta"] is None:
            continue
        em = L.E_maj(a)
        for c in CEILS:
            if a["delta"] <= c:
                cnt[c] += 1
                if best[c] is None or em > best[c]:
                    best[c] = em
    print("%5d" % n, end="")
    for c in CEILS:
        if best[c] is None:
            print("%12s" % "EMPTY", end="")
        else:
            print("%12.5f" % (float(best[c]) / (n * n)), end="")
    print()
    print("%5s" % "  (#)", end="")
    for c in CEILS:
        print("%12d" % cnt[c], end="")
    print()
print()
print("  The `(#)` row is the population size behind each cell.  A cell over an EMPTY")
print("  or tiny population and a cell over a large one print identically otherwise,")
print("  which is mg-c3ca's own recorded defect 4 and is avoided here by printing both.")

print()
print("-" * 78)
print("E. THE SAME FRONTIER, PRIMITIVE ONLY (the population the architecture admits)")
print("-" * 78)
print("%5s" % "n", end="")
for c in CEILS:
    print("%12s" % ("<=%s" % c), end="")
print()
for n in range(3, NMAX + 1):
    best = {c: None for c in CEILS}
    cnt = {c: 0 for c in CEILS}
    for P in L.gen_natural_posets(n):
        a = L.analyse(P)
        if a["delta"] is None or not a["primitive"]:
            continue
        em = L.E_maj(a)
        for c in CEILS:
            if a["delta"] <= c:
                cnt[c] += 1
                if best[c] is None or em > best[c]:
                    best[c] = em
    print("%5d" % n, end="")
    for c in CEILS:
        print("%12s" % ("EMPTY" if best[c] is None else "%.5f" % (float(best[c]) / (n * n))), end="")
    print()
    print("%5s" % "  (#)", end="")
    for c in CEILS:
        print("%12d" % cnt[c], end="")
    print()

print()
print("=" * 78)
print("a3_construct done.")
print("=" * 78)
