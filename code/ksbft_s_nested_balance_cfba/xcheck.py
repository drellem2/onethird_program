"""xcheck.py (mg-cfba): cross-check nb.c against the independent Python ideal DP of mg-ce69 (lib.analyse)
and against explicit enumeration of linear extensions, on random small posets; plus nestedness classifier checks."""
import random, subprocess, sys
from fractions import Fraction
sys.path.insert(0, "../ksbft_q2_both_ends_ce69")
from lib import analyse, extensions, upmasks, fmt, closure

def rand_poset(n, p, rnd):
    dn = [0] * n
    for j in range(n):
        for i in range(j):
            if rnd.random() < p:
                dn[j] |= 1 << i
    return closure(dn)

def stats_py(dn):
    n = len(dn); up = upmasks(dn)
    exts = extensions(dn); e = len(exts)
    pos = [{v: k for k, v in enumerate(L)} for L in exts]
    d = dN = dP = 0; nb = nbN = nn = 0
    for a in range(n):
        for b in range(a + 1, n):
            if dn[a] >> b & 1 or dn[b] >> a & 1: continue
            B = sum(1 for q in pos if q[a] < q[b]); pp = Fraction(B, e); m = min(pp, 1 - pp)
            nested = (dn[a] & ~dn[b] == 0) or (dn[b] & ~dn[a] == 0) or (up[a] & ~up[b] == 0) or (up[b] & ~up[a] == 0)
            bal = Fraction(1, 3) <= pp <= Fraction(2, 3)
            d = max(d, m); nb += bal; nn += not nested
            if nested: dN = max(dN, m); nbN += bal
            if (dn[a] & ~dn[b] == 0) or (dn[b] & ~dn[a] == 0): dP = max(dP, m)
    return e, float(d), float(dN), nb, nbN, nn, float(dP)

rnd = random.Random(20260926)
ps = [rand_poset(rnd.randint(3, 8), rnd.choice([0.15, 0.3, 0.5]), rnd) for _ in range(400)]
ps.append(closure([0, 0, 1, 2, 0, 16])[:0] or [0, 1, 3, 0, 8, 24])  # 3+3: two 3-chains
out = subprocess.run(["./nb"], input="\n".join(fmt(d) for d in ps) + "\n", capture_output=True, text=True).stdout.split("\n")
bad = 0
for dn, line in zip(ps, out):
    t = line.split()
    e, d, dN, nb, nbN, nn, dP = stats_py(dn)
    got = (float(t[1]), float(t[2]), float(t[3]), int(t[4]), int(t[5]), int(t[6]))
    if abs(got[0] - e) > 0.5 or abs(got[1] - d) > 1e-5 or abs(got[2] - dN) > 1e-5 or got[3:] != (nb, nbN, nn) or abs(float(t[9]) - dP) > 1e-5:
        bad += 1; print("MISMATCH", fmt(dn), line, (e, d, dN, nb, nbN, nn))
print(f"xcheck: {len(ps)} posets vs explicit enumeration, mismatches {bad}")
sep = sum(1 for dn, line in zip(ps, out) if int(line.split()[4]) > int(line.split()[5]))
sepP = sum(1 for dn, line in zip(ps, out) if abs(float(line.split()[9]) - float(line.split()[3])) > 1e-9)
print(f"classifier discrimination (controls): posets with a NON-nested balanced pair {sep}; with deltaP != deltaN {sepP}")
print("3+3 line (expect exactly 1 non-nested pair, the middle pair):", out[len(ps) - 1])
