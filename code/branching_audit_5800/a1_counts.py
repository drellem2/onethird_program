"""A1 -- the corrected fractions, from my own enumeration and my own canonical
form.  Targets in mg-41aa / 504ab6c:

  * 62/318 at n=6, 149/2 045 at n=7, 360/16 999 at n=8
  * the straight column 1,1,2,3,4,6,8,12 "reproduced UNCHANGED"
  * "AT n <= 3 EVERY POSET IS A SKEW SHAPE POSET (1/1, 2/2, 5/5)"
  * mg-41aa's §7 attack 2: the n x n box bound.  Grown here at EVERY n
    from 1 to 8, not just to n = 5.

Denominators are NOT carried from anywhere: they are enumerated by
kern5800.enumerate_posets and then cross-checked against A000112 as
published.
"""
import sys, time
from kern5800 import (canon, decode, enumerate_posets, skew_shapes,
                      skew_cell_poset, straight_shapes)

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8

# OEIS A000112, unlabelled posets on n elements, n = 1..10.  Transcribed from
# the published sequence, used only as a CROSS-CHECK on the enumeration below.
A000112 = {1: 1, 2: 2, 3: 5, 4: 16, 5: 63, 6: 318, 7: 2045, 8: 16999,
           9: 183231, 10: 2567284}

print("=" * 78)
print("A1  THE CORRECTED FRACTIONS, RE-ENUMERATED")
print("=" * 78)

t0 = time.time()
ps = enumerate_posets(NMAX)
print("\nall posets, enumerated by ADD-A-MAXIMAL-ELEMENT (%.1fs):" % (time.time() - t0))
mismatch = 0
for n in range(1, NMAX + 1):
    ref = A000112[n]
    flag = "OK " if len(ps[n]) == ref else "BAD"
    if len(ps[n]) != ref:
        mismatch += 1
    print("  n=%d  mine=%-6d  A000112=%-6d  %s" % (n, len(ps[n]), ref, flag))
print("  A000112 disagreements: %d" % mismatch)

# ------------------------------------------------------- skew / straight sets

def skew_set(n, box):
    return {canon(*skew_cell_poset(s)) for s in skew_shapes(n, box)}

def straight_set(n):
    return {canon(*skew_cell_poset(s)) for s in straight_shapes(n)}

print("\nskew cell poset classes (box = n) and straight cell poset classes:")
skew = {}
straight = {}
for n in range(1, NMAX + 1):
    t = time.time()
    skew[n] = skew_set(n, n)
    straight[n] = straight_set(n)
    print("  n=%d  skew=%-5d straight=%-4d  all=%-6d  (%.1fs)"
          % (n, len(skew[n]), len(straight[n]), len(ps[n]), time.time() - t))

print("\nCONTAINMENT CONTROL -- straight subset skew subset all:")
bad = 0
for n in range(1, NMAX + 1):
    a = straight[n] <= skew[n]
    b = skew[n] <= set(ps[n])
    if not (a and b):
        bad += 1
        print("  n=%d  straight<=skew:%s  skew<=all:%s  BAD" % (n, a, b))
print("  containment failures: %d" % bad)

# ------------------------------------------------------- the published table

print("\nTHE TABLE mg-41aa WRITES INTO THE DOCUMENT, RE-DERIVED:")
CLAIMED = {4: (3, 11, 16), 5: (4, 26, 63), 6: (6, 62, 318),
           7: (8, 149, 2045), 8: (12, 360, 16999)}
disagree = 0
print("  n | straight (claimed) | skew (claimed) | all (claimed)")
for n in sorted(CLAIMED):
    if n > NMAX:
        continue
    cs, ck, ca = CLAIMED[n]
    ms, mk, ma = len(straight[n]), len(skew[n]), len(ps[n])
    row = "  %d | %4d (%4d)        | %4d (%4d)   | %6d (%6d)" % (n, ms, cs, mk, ck, ma, ca)
    if (ms, mk, ma) != (cs, ck, ca):
        row += "   <-- DISAGREES"
        disagree += 1
    print(row)
print("  rows disagreeing with mg-41aa: %d" % disagree)

print("\naf28's STRAIGHT column, which the repair says is reproduced UNCHANGED:")
AF28_STRAIGHT = [1, 1, 2, 3, 4, 6, 8, 12]
mine = [len(straight[n]) for n in range(1, NMAX + 1)]
print("  af28: %s" % AF28_STRAIGHT[:NMAX])
print("  mine: %s" % mine)
print("  straight-column disagreements: %d"
      % sum(1 for a, b in zip(AF28_STRAIGHT, mine) if a != b))

# -------------------------------------------- "at n<=3 EVERY poset is skew"

print("\nTHE n <= 3 CLAIM -- 'AT n<=3 EVERY POSET IS A SKEW SHAPE POSET (1/1, 2/2, 5/5)':")
for n in range(1, 5):
    missing = set(ps[n]) - skew[n]
    print("  n=%d  skew %d of %d  %s" % (n, len(skew[n]), len(ps[n]),
          "ALL" if not missing else "%d NOT skew" % len(missing)))
    if missing and n == 4:
        for c in sorted(missing)[:3]:
            up = decode(n, c)
            rel = [(i, j) for i in range(n) for j in range(n) if (up[i] >> j) & 1]
            print("      a poset at n=4 that is NOT skew: relations %s" % rel)

# ------------------------------------------------- box-growth control at ALL n

print("\nBOX-GROWTH CONTROL (mg-41aa's own §7 attack 2), run at EVERY n to %d:" % NMAX)
moves = 0
for n in range(1, NMAX + 1):
    counts = []
    for box in (n, n + 1, n + 2):
        counts.append(len(skew_set(n, box)))
    same = len(set(counts)) == 1
    if not same:
        moves += 1
    print("  n=%d  box n,n+1,n+2 -> %s  %s" % (n, counts, "stable" if same else "MOVED"))
print("  movements: %d" % moves)

print("\nSUMMARY a1_counts: A000112 disagreements %d; containment failures %d; "
      "table rows disagreeing %d; straight-column disagreements %d; box movements %d"
      % (mismatch, bad, disagree,
         sum(1 for a, b in zip(AF28_STRAIGHT, mine) if a != b), moves))
