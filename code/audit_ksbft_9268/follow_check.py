#!/usr/bin/env python3
"""follow_check.py (mg-9268) -- END-TO-END soundness + completeness probe of
the KSBFT-I search, independent of both search implementations' layer code.

For random ordinal-indecomposable posets P of range <= D (n up to NMAX):
  1. compute P's canonical order here (non-decreasing down-degree, ties by
     down-mask over earlier positions, block by block: Lemma 2a);
  2. ask `aud D 58 follow` to walk P's path through the search tree
     (the walk goes through aud's real generator, so a completeness bug in
     the generator shows up as MISSED, a wrong prune as CUT);
  3. verify the outcome FROM SCRATCH with Python integers / Fractions:
     - CERT k: V_k(prefix) enumerated by brute force equals V_k(P) (the safe
       cut, Lemma 2b), every J contains a,b with rho_J in [1/3,2/3], AND the
       pair's exact probability in the whole P is in [1/3,2/3];
     - LP k: same V_k check; each listed pair is one-sided as claimed;
       sum_q lam_q a_qJ >= 0 exactly for every J (Gordan, Lemma 4); AND at
       least one listed pair is balanced in the whole P;
     - ENDED: delta(P) >= 1/3 exactly.
  Every P's delta is also checked directly.
usage: follow_check.py AUD_BINARY D COUNT NMAX SEED [exact|any] [extra aud flags, e.g. badcut]
"""
import random, subprocess, sys
from fractions import Fraction

LO, HI = Fraction(1, 3), Fraction(2, 3)
EXACT = False   # set by the 6th argument 'exact': keep only posets of range exactly D, n >= 2D


def closure(n, rel):
    below = [set() for _ in range(n)]
    for (i, j) in rel:
        below[j].add(i)
    for j in range(n):          # rel only has i<j in index order, so one pass in order closes it
        acc = set(below[j])
        for i in list(below[j]):
            acc |= below[i]
        below[j] = acc
    return below


def rand_poset(n, D, rng):
    """random poset on 0..n-1 (index order is a linear extension) with range <= D, or None"""
    w = rng.randint(2, 2 * D)
    p = rng.random()
    rel = set()
    for j in range(n):
        for i in range(max(0, j - 3 * D), j):
            if j - i >= w or rng.random() < p * (j - i) / w:
                rel.add((i, j))
    below = closure(n, rel)
    inc = [n - 1 - len(below[x]) - sum(1 for y in range(n) if x in below[y]) for x in range(n)]
    if max(inc) > D or max(inc) == 0 or (EXACT and max(inc) != D):
        return None
    return below


def indecomposable(below, order):
    n = len(order)
    pos = {x: i for i, x in enumerate(order)}
    for c in range(1, n):
        first = set(order[:c])
        if all(first <= below[order[i]] for i in range(c, n)):
            return False
    return True


def canonical(below):
    n = len(below)
    d = [len(below[x]) for x in range(n)]
    order = []
    for dv in sorted(set(d)):
        block = [x for x in range(n) if d[x] == dv]
        pos = {x: i for i, x in enumerate(order)}
        for x in block:
            assert below[x] <= set(order), "down-set not in earlier blocks"
        key = lambda x: sum(1 << pos[y] for y in below[x])
        order += sorted(block, key=key)
    return order


def masks(below, order):
    pos = {x: i for i, x in enumerate(order)}
    return [sum(1 << pos[y] for y in below[x]) for x in order]


def downsets(dm, n, k=None):
    """all down-sets (as masks) of the poset on positions 0..n-1 (dm = down masks), by size"""
    layers = [{0}]
    for s in range(n):
        nxt = set()
        for I in layers[-1]:
            for z in range(n):
                if not I >> z & 1 and dm[z] & ~I == 0:
                    nxt.add(I | 1 << z)
        layers.append(nxt)
        if k is not None and s + 1 == k:
            break
    return layers


def ext_counts(dm, J, pairs):
    """#linear extensions of subposet J, and for each (a,b) #with a before b"""
    elems = [z for z in range(64) if J >> z & 1]
    f = {0: 1}
    order = sorted(downsets_within(dm, J), key=lambda m: bin(m).count("1"))
    for I in order:
        if I == 0:
            continue
        f[I] = sum(f[I & ~(1 << z)] for z in elems if I >> z & 1 and all(not (I >> y & 1) or not (dm[y] >> z & 1) for y in elems))
    g = {J: 1}
    for I in reversed(order):
        if I == J:
            continue
        g[I] = sum(g[I | 1 << z] for z in elems if not I >> z & 1 and dm[z] & J & ~I == 0)
    tot = f[J]
    assert g[0] == tot
    res = {}
    for (a, b) in pairs:
        res[(a, b)] = sum(f[I] * g[I | 1 << b] for I in order if I >> a & 1 and not I >> b & 1 and dm[b] & J & ~I == 0)
    return tot, res


def downsets_within(dm, J):
    elems = [z for z in range(64) if J >> z & 1]
    seen = {0}; frontier = [0]
    while frontier:
        new = []
        for I in frontier:
            for z in elems:
                if not I >> z & 1 and dm[z] & J & ~I == 0:
                    K = I | 1 << z
                    if K not in seen:
                        seen.add(K); new.append(K)
        frontier = new
    return seen


def rho(dm, J, a, b):
    ina, inb = J >> a & 1, J >> b & 1
    if ina and inb:
        tot, r = ext_counts(dm, J, [(a, b)])
        return Fraction(r[(a, b)], tot)
    if ina:
        return Fraction(1)
    if inb:
        return Fraction(0)
    return None


def main():
    aud, D, count, nmax, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    global EXACT
    EXACT = len(sys.argv) > 6 and sys.argv[6] == "exact"
    rng = random.Random(seed)
    polys = []
    while len(polys) < count:
        n = rng.randint(2 * D if EXACT else 3, nmax)
        below = rand_poset(n, D, rng)
        if below is None:
            continue
        order = canonical(below)
        if not indecomposable(below, order):
            continue
        polys.append(masks(below, order))
    tag = f"D={D} seed={seed}: {len(polys)} random indecomposable posets (n<= {nmax})"
    verify(aud, D, polys, sys.argv[7:], tag)


def verify(aud, D, polys, extra, tag):
    inp = "".join("[" + ",".join(map(str, m)) + "]\n" for m in polys)
    out = subprocess.run([aud, str(D), "58", "follow"] + extra, input=inp, capture_output=True, text=True, check=True).stdout.split("\n")
    out = [l for l in out if l.startswith("FOLLOW")]
    assert len(out) == len(polys), (len(out), len(polys))
    stats = {}; bad = 0; deltas_min = Fraction(1)
    for dm, line in zip(polys, out):
        n = len(dm); t = line.split(); depth = int(t[2].split("=")[1]); kind = t[3]
        stats[kind] = stats.get(kind, 0) + 1
        full = (1 << n) - 1
        allpairs = [(a, b) for b in range(n) for a in range(b) if not dm[b] >> a & 1]
        tot, cnt = ext_counts(dm, full, allpairs)
        dl = max(min(Fraction(c, tot), 1 - Fraction(c, tot)) for c in cnt.values())
        deltas_min = min(deltas_min, dl)
        ok = dl >= LO
        if kind in ("MISSED", "CUT") or depth < 0:
            ok = False
        elif kind in ("CERT", "LP"):
            k = int(t[4].split("=")[1]); N = depth
            Vpre = downsets(dm[:N], N, k)[k] if k > 0 else {0}
            Vfull = downsets(dm, n, k)[k] if k > 0 else {0}
            if Vpre != Vfull:
                ok = False; print("SAFE-CUT FAILURE", dm, N, k)
            if kind == "CERT":
                for tok in t[5:]:
                    a, b = map(int, tok.split(","))
                    for J in Vpre:
                        r = rho(dm, J, a, b)
                        if r is None or not (LO <= r <= HI):
                            ok = False; print("CERT FAILURE at J", dm, N, k, a, b)
                    if not (LO <= Fraction(cnt[(a, b)], tot) <= HI):
                        ok = False; print("CERT PAIR NOT BALANCED IN P", dm, a, b)
            else:
                cert = [tuple(map(int, tok.split(","))) for tok in t[5:]]
                for J in Vpre:
                    s = Fraction(0)
                    for (a, b, side, lam) in cert:
                        r = rho(dm, J, a, b)
                        if r is None:
                            ok = False; print("LP undetermined", dm); continue
                        if side < 0 and r > HI or side > 0 and r < LO:
                            ok = False; print("LP side violated", dm, a, b)
                        s += lam * ((r - LO) if side < 0 else (HI - r))
                    if s < 0:
                        ok = False; print("LP CERT NEGATIVE at J", dm, N, k, J, s)
                if not any(LO <= Fraction(cnt[(a, b)], tot) <= HI for (a, b, _, _) in cert):
                    ok = False; print("LP SET HAS NO BALANCED PAIR IN P", dm)
        elif kind == "ENDED":
            ok = ok and depth == n and t[5] == "ok"
        if not ok:
            bad += 1; print("BAD", dm, line)
    print(f"{tag}, outcomes {stats}, min delta {deltas_min} = {float(deltas_min):.4f}, failures {bad}")


if __name__ == "__main__":
    main()
