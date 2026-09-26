"""witness.py (mg-ce69): exact dumps of the witnesses of docs/KSBFT-Q2-both-ends.md, with an independent
cross-check (explicit enumeration of linear extensions, no ideal DP) wherever e(P) <= 200000.

  B7_m  = first 7 elements of P9 (an ideal) + zigzag tail of m elements   (one-ended; WIN_bot fails)
  Q_m   = (P9 + tail m) with its dual glued on top                         (both ends; WIN fails at both)
For each: n, e, range, connected, every incomparable pair inside a bottom window with its exact law,
every balanced pair with its exact law.
"""
import sys
from fractions import Fraction
from lib import parse, fmt, analyse, extensions, upmasks, inc, rng, connected, windows, bal_pairs, balanced
from longtail import grow, dual, glue


def dump(tag, dn, check=True):
    e, B, _ = analyse(dn)
    n = len(dn)
    up = upmasks(dn)
    cross = "skipped (e too large)"
    if check and e <= 200000:
        L = extensions(dn)
        ok = len(L) == e
        if ok:
            where = [{v: i for i, v in enumerate(ext)} for ext in L]
            for a in range(n):
                for b in range(n):
                    if a != b and sum(1 for w in where if w[a] < w[b]) != B[a][b]:
                        ok = False
        cross = "enumeration AGREES" if ok else "ENUMERATION DISAGREES"
    bot, top = windows(dn)
    print(f"{tag}: {fmt(dn)}")
    print(f"   n={n} e={e} range={rng(dn)} {'connected' if connected(dn) else 'DISCONNECTED'}; cross-check: {cross}")
    seen = set()
    for w in bot:
        for a in w:
            for b in w:
                if a < b and inc(dn, up, a, b) and (a, b) not in seen:
                    seen.add((a, b))
                    p = Fraction(B[a][b], e)
                    print(f"   bottom-window P[{a}<{b}] = {p} = {float(p):.5f}{'  BALANCED' if balanced(p) else ''}")
    for a, b, p in bal_pairs(dn, e, B):
        print(f"   balanced P[{a}<{b}] = {p} = {float(p):.5f}")
    sys.stdout.flush()
    return cross


def main():
    P9 = parse("9 0 0 2 2 3 b 2b 2f 7f")
    B7 = [m & 0x7f for m in P9[:7]]
    res = []
    for m in (0, 3, 6):
        res.append(dump(f"B7_{m}", grow(B7, m, 1)))
    res.append(dump("B7_20", grow(B7, 20, 1), check=False))
    for m in (0, 14):
        lo = grow(P9, m, 1)
        res.append(dump(f"Q_{m}", glue(lo, dual(lo), 1), check=False))
    bad = [r for r in res if "DISAGREES" in r]
    print("RESULT", "cross-checks agree" if not bad else "CROSS-CHECK FAILED")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
