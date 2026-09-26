"""gadget.py (mg-ce69): checks of the PROVEN gadget lemmas of docs/KSBFT-Q2-both-ends.md, sec. 1-2.

For every connected (indecomposable) poset in the given census files and every minimal x with chain bottom
C = c_1<..<c_k (k>=1) of Z = Inc(x), R = P - C:
  (A1) #{f(x) > k} = e(R)                          [Lemma 1.1: x after c_k  <=>  the extension starts C]
  (A2) #{f(x) = i+1} = e(P - C_i - x), i < k
  (A3) min(R) = {x} u U,  U = min(Z - C)
  (A4) for every pair a,b of R: B_P[a][b] = B_R[a][b] + sum_{i<k} B_{P-C_i-x}[a][b]   (x-pairs: x before b
       on every event f(x) <= k, since then x precedes everything of R - x)
Controls (must FIRE): CTRL1 uses C_{k-1} in place of C in (A1) when k >= 1 (it must fail whenever the
identity is informative);  CTRL2 drops the i = k-1 term of (A4).
Also (B) release-time monotonicity (Lemma 1.3): for every element u, the law of f(u) - max_{w<u} f(w)
(max over empty set = 0) is non-increasing; checked by explicit enumeration of extensions for n <= 7.
CTRL3 (must FIRE): the same with min_{w<u} f(w) in place of max.
Also (C) the dominance order (Lemma 2.1) is a proof by cases; its consequence 'cyclic sum in [1,2]' is checked
on every 3-antichain, with CTRL4 (must FIRE): the sum is not always in [1, 3/2].
Also (X) Shepp's XYZ inequality P[a<b, a<c] >= P[a<b]P[a<c] on every 3-antichain (literature, sanity check).
Usage: python3 gadget.py FILE...   (explicit enumeration only for n <= 7)
"""
import sys
from fractions import Fraction
from lib import analyse, upmasks, inc, chain_bottom, restrict, connected, extensions


def sub(dn, keep):
    keep = sorted(keep)
    d, _ = restrict(dn, keep)
    return d, keep


def run(files):
    cnt = dict(posets=0, gadgets=0, A1=0, A2=0, A3=0, A4=0, ctrl1=0, ctrl2=0, B=0, ctrl3=0, C=0, ctrl4=0,
               X=0, trip=0, relchecked=0)
    for f in files:
        for line in open(f):
            a = line.split()
            n = int(a[0])
            if n < 2:
                continue
            dn = [int(t, 16) for t in a[1:]]
            if not connected(dn):
                continue
            cnt["posets"] += 1
            up = upmasks(dn)
            e, B, pos = analyse(dn)
            full = set(range(n))
            for x in range(n):
                if dn[x]:
                    continue
                Z = [y for y in range(n) if inc(dn, up, x, y)]
                C = chain_bottom(dn, Z)
                k = len(C)
                if k == 0:
                    continue
                cnt["gadgets"] += 1
                Rk = full - set(C)
                dR, kR = sub(dn, Rk)
                eR, BR, _ = analyse(dR)
                after = sum(pos[x][k:])
                cnt["A1"] += after != eR
                # control 1: C_{k-1}
                dR1, _ = sub(dn, full - set(C[:k - 1]))
                if after != analyse(dR1)[0]:
                    cnt["ctrl1"] += 1
                Pi = []
                for i in range(k):
                    di, ki = sub(dn, full - set(C[:i]) - {x})
                    ei, Bi, _ = analyse(di) if di else (1, [[0]], None)
                    Pi.append((ki, ei, Bi))
                    cnt["A2"] += pos[x][i] != ei
                rest = [z for z in Z if z not in C]
                U = sorted(v for v in rest if not any(dn[v] >> w & 1 for w in rest))
                minR = sorted(kR[i] for i in range(len(kR)) if dR[i] == 0)
                cnt["A3"] += minR != sorted([x] + U)
                ix = {v: i for i, v in enumerate(kR)}
                bad = bad2 = False
                for p in kR:
                    for q in kR:
                        if p == q or not inc(dn, up, p, q):
                            continue
                        tot = BR[ix[p]][ix[q]]
                        parts = []
                        for (ki, ei, Bi) in Pi:
                            if p == x:
                                parts.append(ei)
                            elif q == x:
                                parts.append(0)
                            else:
                                jj = {v: t for t, v in enumerate(ki)}
                                parts.append(Bi[jj[p]][jj[q]])
                        bad |= tot + sum(parts) != B[p][q]
                        bad2 |= tot + sum(parts[:-1]) != B[p][q]
                cnt["A4"] += bad
                cnt["ctrl2"] += bad2
            # 3-antichains: cyclic sums and XYZ
            for p in range(n):
                for q in range(n):
                    for r in range(n):
                        if len({p, q, r}) == 3 and inc(dn, up, p, q) and inc(dn, up, q, r) and inc(dn, up, p, r):
                            cnt["trip"] += 1
                            cs = Fraction(B[p][q] + B[q][r] + B[r][p], e)
                            cnt["C"] += not (1 <= cs <= 2)
                            cnt["ctrl4"] += not (1 <= cs <= Fraction(3, 2))
            if n <= 7:
                L = extensions(dn)
                assert len(L) == e
                for u in range(n):
                    lawmax = [0] * (n + 1)
                    lawmin = [0] * (n + 1)
                    for ext in L:
                        fp = {v: i + 1 for i, v in enumerate(ext)}
                        lo = [fp[w] for w in range(n) if dn[u] >> w & 1]
                        lawmax[fp[u] - (max(lo) if lo else 0)] += 1
                        lawmin[fp[u] - (min(lo) if lo else 0)] += 1
                    cnt["relchecked"] += 1
                    cnt["B"] += any(lawmax[j + 1] > lawmax[j] for j in range(1, n))
                    cnt["ctrl3"] += any(lawmin[j + 1] > lawmin[j] for j in range(1, n))
                # XYZ by enumeration
                for p in range(n):
                    for q in range(n):
                        for r in range(q + 1, n):
                            if len({p, q, r}) == 3 and inc(dn, up, p, q) and inc(dn, up, p, r):
                                both = sum(1 for ext in L if ext.index(p) < ext.index(q) and ext.index(p) < ext.index(r))
                                cnt["X"] += both * e < B[p][q] * B[p][r]
        print("file", f, " ".join(f"{k}={v}" for k, v in cnt.items()))
        sys.stdout.flush()
    return cnt


if __name__ == "__main__":
    c = run(sys.argv[1:])
    ok = all(c[k] == 0 for k in ("A1", "A2", "A3", "A4", "B", "C", "X"))
    fire = all(c[k] > 0 for k in ("ctrl1", "ctrl2", "ctrl3", "ctrl4"))
    print("RESULT", "violations=0" if ok else "VIOLATION", "controls_fire" if fire else "CONTROL_DID_NOT_FIRE")
    sys.exit(0 if ok and fire else 1)
