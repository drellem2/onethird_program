"""census.py (audit mg-6e7c): independent re-count of mg-ce69's census columns, plus theorem checks.
For every poset in the given files with connected incomparability graph:
  STEP   Thm 1.4(a): steps along every nested ladder (primal + dual) non-increasing       (must be 0)
  SLV    Thm 1.4(c): hypotheses met but no rung balanced                                 (must be 0)
  DBL    Lemma 1.5: down(x)=down(b), up(x)<=up(b), m>=1  =>  t_1 = t_0 and t_0 <= 1/2      (must be 0)
  EQV    SL fires <=> a nested (primal or dual) balanced pair exists, per poset            (must be 0; proven in the audit)
  SL, GOOD (Zaguia: full ladder with P[x<b] <= 1/2), STRUCT (Cor 1.6: opposite full-chain ladders), NESTBAL
  (n <= 8 only) PINCH: Lemma 1.2 event identity vs ordinal-sum condition, every minimal x, every t (must be 0)
  (n <= 8 only) CPRE: Lemma 1.1(4) P[x<b] = s + (1-s) P_R[x<b], every Y-gadget, every b in Z - C  (must be 0)
Controls (must be > 0): CH1 = step increases when H1 is dropped; CWIN = SL conclusion with [0.34,0.66];
  CDBL = t_1 != t_0 when up(x)<=up(b) is dropped; CPINCH = sloppy ordinal-sum condition disagrees;
  CCPRE = the identity with s = P[x < c_{k-1}] (one rung short) fails.
Usage: python3 census.py [--small] FILE...   prints one line per file and a TOTAL line."""
import sys
from fractions import Fraction as F
from aud import ups, incp, conn, probs, ladders, chainbot, rangeD, close, T1, T2
from pinch import pinch_levels_event, pinch_levels_struct

LO, HI = F(34, 100), F(66, 100)
HALF = F(1, 2)


def restrict(dn, keep):
    idx = {v: i for i, v in enumerate(keep)}
    return [sum(1 << idx[w] for w in keep if dn[v] >> w & 1) for v in keep]


def steps_of(r, full):
    s = [r[0]] + [r[i] - r[i - 1] for i in range(1, len(r))]
    if full:
        s.append(1 - r[-1])
    return s


def one(dn, c, small, wit):
    n = len(dn)
    up = ups(dn)
    e, Bc = probs(dn)
    P = lambda a, b: F(Bc[a][b], e)
    sl = good = False
    asserts = {}
    for dual in (False, True):
        for x, b, ch, full, r in ladders(dn, up, P, dual):
            st = steps_of(r, full)
            if any(st[i + 1] > st[i] for i in range(len(st) - 1)):
                c["STEP"] += 1
            if r[0] <= T2 and r[-1] >= T1:
                sl = True
                if not any(T1 <= p <= T2 for p in r):
                    c["SLV"] += 1
                if not any(LO <= p <= HI for p in r):
                    c["CWIN"] += 1
            if full and r[0] <= HALF:
                good = True
            if full:
                # asserted order in P: primal (x;b) asserts x before b; dual (x;b) asserts b before x
                key = (min(x, b), max(x, b))
                asserts.setdefault(key, set()).add((x, b) if not dual else (b, x))
            d, u = (up, dn) if dual else (dn, up)
            if d[x] == d[b] and len(ch) >= 2:
                if u[x] & ~u[b] == 0:
                    if st[1] != st[0] or st[0] > HALF:
                        c["DBL"] += 1
                elif st[1] != st[0]:
                    c["CDBL"] += 1
    # control CH1: pairs violating H1
    for x in range(n):
        for b in range(n):
            if incp(dn, up, x, b) and dn[x] & ~dn[b]:
                W = [w for w in range(n) if (w == b or up[b] >> w & 1) and not (w == x or up[x] >> w & 1)]
                ch, full = chainbot(dn, W)
                r = [P(x, cc) for cc in ch]
                st = steps_of(r, full)
                if any(st[i + 1] > st[i] for i in range(len(st) - 1)):
                    c["CH1"] += 1
    struct = any(len(v) == 2 for v in asserts.values())
    nestbal = any(incp(dn, up, a, b) and T1 <= P(a, b) <= T2 and (dn[a] & ~dn[b] == 0 or up[a] & ~up[b] == 0)
                  for a in range(n) for b in range(n))
    c["posets"] += 1
    c["SL"] += sl
    c["GOOD"] += good
    c["STRUCT"] += struct
    c["NESTBAL"] += nestbal
    c["EQV"] += sl != nestbal
    if not struct:
        wit.append(("STRUCT_FAILS", rangeD(dn), dn))
    if not good:
        wit.append(("GOOD_FAILS", rangeD(dn), dn))
    if small:
        for x in range(n):
            if dn[x]:
                continue
            ev = pinch_levels_event(dn, x)
            if ev != pinch_levels_struct(dn, x):
                c["PINCH"] += 1
            if ev != pinch_levels_struct(dn, x, sloppy=True):
                c["CPINCH"] += 1
            Z = [z for z in range(n) if incp(dn, up, x, z)]
            C, fullZ = chainbot(dn, Z)
            if not C or fullZ:
                continue
            rest = [z for z in Z if z not in C]
            U = [v for v in rest if not any(dn[v] >> w & 1 for w in rest if w != v)]
            if len(U) < 2:
                continue
            k = len(C)
            s = P(x, C[k - 1])                     # = P[|J| <= k-1]
            s_bad = P(x, C[k - 2]) if k >= 2 else F(0)
            keep = [v for v in range(n) if v not in C]
            R = restrict(dn, keep)
            eR, BR = probs(R)
            xi = keep.index(x)
            for b in rest:
                pR = F(BR[xi][keep.index(b)], eR)
                if P(x, b) != s + (1 - s) * pR:
                    c["CPRE"] += 1
                if P(x, b) != s_bad + (1 - s_bad) * pR:
                    c["CCPRE"] += 1
            c["gadgets"] += 1


def main(args):
    small = False
    if args and args[0] == "--small":
        small = True
        args = args[1:]
    keys = ["posets", "SL", "GOOD", "STRUCT", "NESTBAL", "STEP", "SLV", "DBL", "EQV", "PINCH", "CPRE", "gadgets",
            "CH1", "CWIN", "CDBL", "CPINCH", "CCPRE"]
    tot = dict.fromkeys(keys, 0)
    for f in args:
        c = dict.fromkeys(keys, 0)
        wit = []
        for line in open(f):
            a = line.split()
            n = int(a[0])
            if n < 2:
                continue
            dn = close([int(t, 16) for t in a[1:1 + n]])
            if not conn(dn):
                continue
            one(dn, c, small, wit)
        print("file", f.split("/")[-1], " ".join(f"{k}={v}" for k, v in c.items()))
        from collections import Counter
        for kind in ("STRUCT_FAILS", "GOOD_FAILS"):
            L = [(r, d) for k, r, d in wit if k == kind]
            print(f"  {kind}: {len(L)} by range {dict(sorted(Counter(r for r, _ in L).items()))}"
                  + ("".join(f"\n    {' '.join([str(len(d))] + [format(m, 'x') for m in d])} range {r}" for r, d in L) if len(L) <= 8 else ""))
        sys.stdout.flush()
        for k in keys:
            tot[k] += c[k]
    print("TOTAL", " ".join(f"{k}={v}" for k, v in tot.items()))


if __name__ == "__main__":
    main(sys.argv[1:])
