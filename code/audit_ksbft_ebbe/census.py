"""census.py (audit mg-ebbe): reads aud.c output lines for the full n<=9 census and reports
NB / PNB / DNB failures, Lemma 1.1 and Doubling violations, and every non-chain poset with deltaN = 1/3 exactly
(nested balance only on the boundary), split by decomposability and primality (own code, below).
Usage: python3 census.py a1.txt ... a9.txt"""
import sys
from collections import Counter


def parse(s):
    a = s.split()
    return [int(t, 16) for t in a[1:1 + int(a[0])]]


def ups(dn):
    n = len(dn)
    return [sum(1 << j for j in range(n) if dn[j] >> i & 1) for i in range(n)]


def comp(dn, a, b):
    return dn[a] >> b & 1 or dn[b] >> a & 1


def components(dn, verts, edge):
    verts = list(verts); seen = set(); comps = []
    for v in verts:
        if v in seen: continue
        st = [v]; seen.add(v); c = [v]
        while st:
            u = st.pop()
            for w in verts:
                if w not in seen and edge(u, w):
                    seen.add(w); st.append(w); c.append(w)
        comps.append(c)
    return comps


def indecomposable(dn):
    """both comparability graph and incomparability graph connected (n>=2)"""
    n = len(dn); V = range(n)
    c1 = components(dn, V, lambda u, w: comp(dn, u, w))
    c2 = components(dn, V, lambda u, w: u != w and not comp(dn, u, w))
    return len(c1) == 1 and len(c2) == 1


def is_module(dn, up, M):
    for v in range(len(dn)):
        if M >> v & 1: continue
        below = [(dn[m] >> v & 1) for m in range(len(dn)) if M >> m & 1]
        above = [(up[m] >> v & 1) for m in range(len(dn)) if M >> m & 1]
        if len(set(below)) > 1 or len(set(above)) > 1: return False
    return True


def prime(dn):
    n = len(dn); up = ups(dn)
    for M in range(1, 1 << n):
        k = bin(M).count("1")
        if 2 <= k <= n - 1 and is_module(dn, up, M): return False
    return True


def rng(dn):
    n = len(dn)
    return max(sum(1 for b in range(n) if b != a and not comp(dn, a, b)) for a in range(n))


def main():
    tot = Counter(); ties = []; openfail = []
    for f in sys.argv[1:]:
        for line in open(f):
            pos, rest = line.split(" | ")
            kv = dict(t.split("=") for t in rest.split())
            n = int(pos.split()[0])
            tot["posets", n] += 1
            if kv["chain"] == "1": continue
            tot["nonchain", n] += 1
            e = int(kv["e"])
            for k in ("NB", "PNB", "DNB"):
                if kv[k] != "1": tot[k + "_fail", n] += 1
            if int(kv["trap"]): tot["trap_mismatch", n] += 1
            if int(kv["dbl"]): tot["dbl_viol", n] += 1
            tot["dbl_tested", n] += int(kv["dblcnt"])
            if int(kv["nn"]): tot["has_nonnested", n] += 1
            if kv["dP"] != kv["dN"]: tot["PNB_nontrivial(dP<dN)", n] += 1
            if kv["Bopen"] == "0":
                tot["open_1323_fail", n] += 1
                if indecomposable(parse(pos)): tot["open_1323_fail_indecomposable", n] += 1
            if kv["NBopen"] == "0":
                openfail.append((n, pos, kv))
            if 3 * int(kv["dN"]) == e: ties.append((n, pos, kv))
    for key in sorted(tot, key=lambda t: (t[1], t[0])): print(f"{key[0]:>14} n={key[1]}: {tot[key]}")
    print("OPEN-window NB fails (no nested pair strictly inside (1/3,2/3)), non-chain:")
    by = Counter()
    for n, pos, kv in openfail:
        dn = parse(pos); ind = indecomposable(dn); pr = ind and prime(dn)
        by[n, ind, pr] += 1
        if ind: print(f"  n={n} {pos}  e={kv['e']} d={kv['d']} dN={kv['dN']} indecomp prime={pr} range={rng(dn)} Bopen={kv['Bopen']}")
    for k in sorted(by): print(f"  count n={k[0]} indecomposable={k[1]} prime={k[2]}: {by[k]}")
    print(f"deltaN = 1/3 exactly: {len(ties)} posets; indecomposable ones: "
          f"{sum(1 for n, p, kv in ties if indecomposable(parse(p)))}")


if __name__ == "__main__":
    main()
