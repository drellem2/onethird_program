"""mg-c929 s2 -- windows do NOT convert to inversions in general.

Two disjoint chains a_1<...<a_m and b_1<...<b_m (width 2).  Linear extensions = lattice paths,
uniform.  Exact over all C(2m,m) extensions for m <= MMAX.  Reports
  W   = sum_x (a_x - 1)   (= sum_x win(x)/2 - n; window occupancy, s1 check CW)
  I_h = E[inv against the height order]  (height order = a_1,b_1,a_2,b_2,... by symmetry)
  I_* = sum over incomparable pairs of min(p,1-p)   (the least E[inv] any fixed order can have)
If I_*/W grows without bound, no inequality E[inv] <= C * sum win can hold for all posets.
This poset HAS balanced pairs (a_i, b_i have p = 1/2), so it says nothing about the
no-balanced-pair class -- it is the witness that the conversion needs that hypothesis.
"""
import itertools, sys, math

MMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10
print("%3s %4s %10s %10s %10s %9s %12s" % ("m", "n", "W", "I_h", "I_*", "I_*/W", "I_*/n^1.5"))
for m in range(1, MMAX + 1):
    n = 2 * m
    N = 0; W = 0; less = {}
    tot_ih = 0
    # element ids: a_i -> ('a',i), b_i -> ('b',i); height order index: a_i -> 2i, b_i -> 2i+1
    for Apos in itertools.combinations(range(1, n + 1), m):
        Aset = set(Apos)
        Bpos = [p for p in range(1, n + 1) if p not in Aset]
        N += 1
        # window: a_i's predecessor is a_{i-1}; elements strictly between are all b's
        for chain in (Apos, Bpos):
            prev = 0
            for p in chain:
                W += p - prev - 1
                prev = p
        for i in range(m):
            for j in range(m):
                key = (i, j)
                less[key] = less.get(key, 0) + (Apos[i] < Bpos[j])
                # height order: a_i before b_j iff 2i < 2j+1 iff i <= j
                if (i <= j) != (Apos[i] < Bpos[j]):
                    tot_ih += 1
    W /= N; Ih = tot_ih / N
    Istar = sum(min(v / N, 1 - v / N) for v in less.values())
    print("%3d %4d %10.4f %10.4f %10.4f %9.4f %12.4f" % (m, n, W, Ih, Istar, Istar / W if W else float('nan'), Istar / n ** 1.5))
