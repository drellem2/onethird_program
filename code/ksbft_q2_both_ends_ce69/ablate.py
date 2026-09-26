"""ablate.py (mg-ce69): is P9's balance an interaction of its two ends?  (doc sec. 3.3)

For P9 and the n=11 range-6 record, replace everything above a bottom ideal I by the zigzag tail (longtail.grow,
r=1), which has no gadget and, in its interior, no balanced pair (P[i<i+1] -> 0.72).  If a balanced pair of P
survives with the same two elements when the top end is sent far away, it is a ONE-END pair, not an interaction.
Prints, for each ideal I (natural-labelling prefix, which is an ideal), P[a<b] of P's balanced pairs in the
one-ended poset I + tail(m), m = 20, plus WIN at the bottom and the gadget data (dominance on {x} u U, XYZ).
"""
import sys
from fractions import Fraction
from lib import parse, analyse, upmasks, inc, rng, connected, windows, bal_pairs, win_holds, chain_bottom, THIRD, TWOTHIRD
from longtail import grow


def gadget(dn, e, B, pos):
    n = len(dn)
    up = upmasks(dn)
    out = []
    for x in range(n):
        if dn[x]:
            continue
        Z = [y for y in range(n) if inc(dn, up, x, y)]
        C = chain_bottom(dn, Z)
        rest = [z for z in Z if z not in C]
        U = [v for v in rest if not any(dn[v] >> w & 1 for w in rest)]
        k = len(C)
        s = Fraction(sum(pos[x][:k]), e)
        Sk = Fraction(sum(pos[x][:k + 1]), e)
        pu = {u: Fraction(B[x][u], e) for u in U}
        out.append((x, C, U, s, Sk, pu))
    return out


def main():
    for name, s, prefixes in (("P9", "9 0 0 2 2 3 b 2b 2f 7f", (4, 5, 6, 7, 8, 9)),
                              ("rec11", "11 0 0 2 2 3 b 2b 2f af bf 1ff", (4, 5, 6, 7, 8, 9, 10, 11))):
        P = parse(s)
        e, B, pos = analyse(P)
        bp = bal_pairs(P, e, B)
        print(f"== {name}: balanced pairs of P: " + ", ".join(f"({a},{b})={p}" for a, b, p in bp))
        for g in gadget(P, e, B, pos):
            x, C, U, s_, Sk, pu = g
            if len(U) >= 2:
                print(f"   bottom gadget x={x} C={C} U={U} S_(k-1)={s_} S_k={Sk} P[x<u]={ {u: str(p) for u, p in pu.items()} } "
                      f"XYZ: S_k >= prod ? {Sk >= eval('*'.join(str(p) for p in pu.values()) if pu else '1', {'Fraction': Fraction}) if False else Sk >= __import__('math').prod(pu.values())}")
        for t in prefixes:
            I = [m & ((1 << t) - 1) for m in P[:t]]
            assert all((P[i] & ~((1 << t) - 1)) == 0 for i in range(t)), "prefix not an ideal"
            Q = grow(I, 20, 1)
            eq, Bq, _ = analyse(Q)
            up = upmasks(Q)
            vals = []
            for a, b, _ in bp:
                if a < t and b < t:
                    if inc(Q, up, a, b):
                        p = Fraction(Bq[a][b], eq)
                        vals.append(f"({a},{b})={float(p):.4f}{'*' if THIRD <= p <= TWOTHIRD else ''}")
                    else:
                        vals.append(f"({a},{b})=comparable")
            print(f"   I=first {t:2d} + tail20: n={len(Q)} range={rng(Q)} {'conn' if connected(Q) else 'DISC'} "
                  f"WIN_bot={'holds' if win_holds(Q, eq, Bq, 'bot') else 'FAILS'} "
                  f"balanced pairs of Q within first 12: {[(a, b) for a, b, _ in bal_pairs(Q, eq, Bq) if b < 12]}  P-pairs: {' '.join(vals)}")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
