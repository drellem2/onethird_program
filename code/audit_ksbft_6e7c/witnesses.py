"""witnesses.py (audit mg-6e7c): recompute every witness number mg-ce69 cites, with aud.py only.
Q_m is rebuilt from the doc's PROSE (sec. 3.4 + bothends.py docstring), not from the author's code, and compared
with the author's printed Q_4 string.  Exits 1 on any mismatch with the doc's numbers."""
import sys
import random
from fractions import Fraction as F
from aud import parse, close, ups, incp, rangeD, conn, probs, brute, prob_aug, ladders, count_ext, T1, T2

BAD = []


def check(tag, got, want):
    ok = got == want
    print(f"  [{'ok' if ok else 'MISMATCH'}] {tag}: got {got} want {want}")
    if not ok:
        BAD.append(tag)


def fmt(dn):
    return " ".join([str(len(dn))] + [format(m, "x") for m in dn])


def grow(dn, m):
    """each new element is above every current element except the most recent one"""
    dn = list(dn)
    for _ in range(m):
        n = len(dn)
        dn.append(((1 << n) - 1) & ~(1 << (n - 1)))
    return close(dn)


def grow_r(dn, m, r):
    dn = list(dn)
    for _ in range(m):
        n = len(dn)
        dn.append(((1 << n) - 1) & ~sum(1 << j for j in range(max(0, n - r), n)))
    return close(dn)


def dual(dn):
    n = len(dn)
    up = ups(dn)
    return [sum(1 << (n - 1 - j) for j in range(n) if up[n - 1 - i] >> j & 1) for i in range(n)]


def glue(lo, hi):
    """hi on top of lo: everything of hi above everything of lo, except hi's first element is not above lo's last"""
    a = len(lo)
    out = list(lo)
    for i, m in enumerate(hi):
        below = (1 << a) - 1
        if i == 0:
            below &= ~(1 << (a - 1))
        out.append((m << a) | below)
    return close(out)


def an(dn):
    e, Bc = probs(dn)
    return e, (lambda a, b: F(Bc[a][b], e))


def windows(dn):
    n = len(dn)
    up = ups(dn)
    bot = [{x} | {y for y in range(n) if incp(dn, up, x, y)} for x in range(n) if dn[x] == 0]
    top = [{x} | {y for y in range(n) if incp(dn, up, x, y)} for x in range(n) if up[x] == 0]
    return bot, top


def balpairs(dn, P):
    n = len(dn)
    up = ups(dn)
    return [(a, b) for a in range(n) for b in range(a + 1, n) if incp(dn, up, a, b) and T1 <= P(a, b) <= T2]


def win(dn, P, side):
    bot, top = windows(dn)
    W = bot if side == 0 else top
    return any(a in w and b in w for w in W for a, b in balpairs(dn, P))


def margin(dn, P, side):
    n = len(dn)
    up = ups(dn)
    bot, top = windows(dn)
    W = bot if side == 0 else top
    best = None
    for w in W:
        for a in w:
            for b in w:
                if a < b and incp(dn, up, a, b):
                    p = P(a, b)
                    d = min(abs(p - T1), abs(p - T2)) * (-1 if T1 <= p <= T2 else 1)
                    best = d if best is None or d < best else best
    return best


def nested(dn, up, a, b):
    return (dn[a] & ~dn[b] == 0) or (dn[b] & ~dn[a] == 0) or (up[a] & ~up[b] == 0) or (up[b] & ~up[a] == 0)


P9 = parse("9 0 0 2 2 3 b 2b 2f 7f")
B7 = parse("7 0 0 2 2 3 b 2b")
REC11 = parse("11 0 0 2 2 3 b 2b 2f af bf 1ff")
W8 = parse("8 0 0 0 4 4 6 16 2f")
W6 = parse("6 0 0 2 2 3 f")
Y8 = parse("8 0 0 2 2 3 b 1b 2f")


def main():
    print("== 1. engines agree (ideal DP vs explicit enumeration vs added-relation count), all incomparable pairs")
    for name, dn in (("W6", W6), ("B7", B7), ("P9", P9), ("W8", W8), ("Y8", Y8), ("rec11", REC11)):
        e, P = an(dn)
        L = brute(dn)
        pos = {x: [] for x in range(len(dn))}
        up = ups(dn)
        mism = 0
        for a in range(len(dn)):
            for b in range(len(dn)):
                if incp(dn, up, a, b):
                    bf = F(sum(1 for l in L if l.index(a) < l.index(b)), len(L))
                    if bf != P(a, b) or prob_aug(dn, a, b, e) != bf:
                        mism += 1
        check(f"{name} e & pair laws, 3 engines", (e, len(L), mism), (len(L), len(L), 0))

    print("== 2. Doubling table (doc sec. 1.4): P[2<3], P[2<5] = 2 P[2<3]")
    Q4 = glue(grow(P9, 4), dual(grow(P9, 4)))
    author_Q4 = parse("26 0 0 2 2 3 b 2b 2f 7f ff 1ff 3ff 7ff fff 1fff 3fff 7fff ffff 1ffff 3ffff fffff 3ffff 1fffff 7ffff ffffff 3fffff")
    check("Q_4 rebuilt from prose == author's printed Q_4 (closed masks)", Q4, author_Q4)
    want = {"P9": (F(59, 197), F(118, 197)), "B7": (F(17, 62), F(17, 31)),
            "rec11": (F(247, 750), F(247, 375)), "Q4": (F(809911, 2673421), F(1619822, 2673421))}
    for name, dn in (("P9", P9), ("B7", B7), ("rec11", REC11), ("Q4", Q4)):
        e, P = an(dn)
        up = ups(dn)
        check(f"{name} (P[2<3],P[2<5])", (P(2, 3), P(2, 5)), want[name])
        check(f"{name} Lemma 1.5 hypotheses down(2)=down(3), up(2)<=up(3)", (dn[2] == dn[3], up[2] & ~up[3] == 0), (True, True))
    e4, _ = an(Q4)
    check("Q4 e", e4, 2673421)
    check("Q4 e by plain recursion", count_ext(Q4), 2673421)

    print("== 3. G1 at the bottom gadget (doc Prop 2.3 remark)")
    for name, dn, wu, wv, wS in (("P9", P9, F(161, 197), F(138, 197), F(124, 197)),
                                 ("rec11", REC11, F(119, 150), F(173, 250), F(46, 75))):
        e, P = an(dn)
        # S_1 = P[|J|<=1] = P[0 before 2 and 0 before 3]  (audited identity at j=k)
        L = brute(dn)
        S1 = F(sum(1 for l in L if l.index(0) <= 1), len(L))
        check(f"{name} P[0<2],P[0<3],S_1", (P(0, 2), P(0, 3), S1), (wu, wv, wS))
        check(f"{name} XYZ S_1 >= P[0<2]P[0<3] and both > 2/3", (S1 >= P(0, 2) * P(0, 3), P(0, 2) > T2, P(0, 3) > T2), (True, True, True))

    print("== 4. balanced pairs of every witness: are they all nested (primal or dual)?")
    for name, dn in (("W6", W6), ("P9", P9), ("B7", B7), ("rec11", REC11), ("W8", W8), ("Y8", Y8), ("Q4", Q4)):
        e, P = an(dn)
        up = ups(dn)
        bp = balpairs(dn, P)
        nn = [p for p in bp if not nested(dn, up, *p)]
        print(f"  {name}: balanced {[(a, b, str(P(a, b))) for a, b in bp]}  non-nested: {nn}")
        if nn:
            BAD.append(name + " non-nested balanced pair")
    e, P = an(W8)
    check("W8 minima laws P[0<1],P[0<2],P[1<2]", (P(0, 1), P(0, 2), P(1, 2)), (F(9, 28), F(10, 49), F(65, 196)))
    check("W8 P[1<2] = 1/3 - 1/588", P(1, 2), T1 - F(1, 588))
    e, P = an(Y8)
    up = ups(Y8)
    L = ladders(Y8, up, P)
    lad = [(x, b, ch, full, r) for x, b, ch, full, r in L if x == 2 and b == 4]
    check("Y8 ladder (2;4<6): chain, first rung", [(ch, str(r[0])) for x, b, ch, full, r in lad], [([4, 6], "6/11")])

    print("== 5. Q_m (doc table 3.4) rebuilt from prose; separation Prop 3.1 for n >= 8D-1")
    for m in (0, 2, 4, 6, 10, 14):
        lo = grow(P9, m)
        dn = glue(lo, dual(lo))
        e, P = an(dn)
        n = len(dn)
        D = rangeD(dn)
        wb, wt = win(dn, P, 0), win(dn, P, 1)
        mb, mt = margin(dn, P, 0), margin(dn, P, 1)
        bp = balpairs(dn, P)
        up = ups(dn)
        allnested = all(nested(dn, up, a, b) for a, b in bp)
        depth = max(min(b, n - 1 - a) for a, b in bp)
        sep = None
        if n >= 8 * D - 1:
            bot, top = windows(dn)
            sep = all(dn[t] >> s & 1 for B in bot for T in top for s in B for t in T)
        print(f"  m={m:2d} n={n} range={D} conn={conn(dn)} WIN_bot={'holds' if wb else 'FAILS'} WIN_top={'holds' if wt else 'FAILS'} "
              f"margin_bot={float(mb):+.5f} margin_top={float(mt):+.5f} bal={bp} all_nested={allnested} max_depth_from_nearer_end={depth} "
              f"separation(n>=8D-1)={sep} e={e}")
        if D != 5 or not conn(dn) or wb or wt or not allnested:
            BAD.append(f"Q_{m}")
        if m == 14:
            check("Q_14 e", e, 40440798401)
            check("Q_14 separation", sep, True)

    print("== 6. ablation: does B7's balanced triangle survive ANY tail? (doc 3.3 'survives any tail')")
    random.seed(6)
    for label, top in (("tail r=1 m=20", lambda d: grow_r(d, 20, 1)),
                       ("tail r=2 m=20", lambda d: grow_r(d, 20, 2)),
                       ("tail r=3 m=20", lambda d: grow_r(d, 20, 3))):
        dn = top(B7)
        e, P = an(dn)
        up = ups(dn)
        vals = {(a, b): (P(a, b) if incp(dn, up, a, b) else None) for a, b in ((2, 4), (2, 5), (4, 5))}
        s = " ".join(f"{k}={'cmp' if v is None else f'{float(v):.4f}' + ('*' if T1 <= v <= T2 else '')}" for k, v in vals.items())
        print(f"  B7 + {label}: range={rangeD(dn)} conn={conn(dn)} WIN_bot={'holds' if win(dn, P, 0) else 'FAILS'}  {s}")
    # random range-bounded tops: new element above a random ideal containing everything except <= 2 recent elements
    surv = 0
    tot = 0
    for trial in range(40):
        dn = list(B7)
        for _ in range(8):
            n = len(dn)
            k = random.choice((1, 2, 2, 3))
            ex = random.sample(range(max(0, n - 4), n), min(k, n - max(0, n - 4)))
            m = ((1 << n) - 1) & ~sum(1 << j for j in ex)
            dn.append(m)
            dn = close(dn)
            # keep the down-set of the new element an ideal: close() handles it; drop if range blows up
        if rangeD(dn) > 6 or not conn(dn):
            continue
        tot += 1
        e, P = an(dn)
        up = ups(dn)
        ok3 = all(incp(dn, up, a, b) and T1 <= P(a, b) <= T2 for a, b in ((2, 4), (2, 5), (4, 5)))
        surv += ok3
    print(f"  random tops (8 new elements, range<=6, connected): triangle (2,4),(2,5),(4,5) all balanced in {surv}/{tot}")

    print("== 7. another both-ends instance, built by me: B7 + tail(m) glued to its dual")
    for m in (2, 8):
        lo = grow(B7, m)
        dn = glue(lo, dual(lo))
        e, P = an(dn)
        print(f"  B7-based m={m}: n={len(dn)} range={rangeD(dn)} conn={conn(dn)} WIN_bot={'holds' if win(dn, P, 0) else 'FAILS'} "
              f"WIN_top={'holds' if win(dn, P, 1) else 'FAILS'} margins={float(margin(dn, P, 0)):+.4f}/{float(margin(dn, P, 1)):+.4f} bal={balpairs(dn, P)}")

    print("== 8. P9 pinch: Inc(0) = {1} + {2,3}; pinch levels")
    from pinch import pinch_levels_event, pinch_levels_struct
    check("P9 x=0 pinch levels (event, structural)", (pinch_levels_event(P9, 0), pinch_levels_struct(P9, 0)), ([0], [0]))

    print("RESULT", "ALL MATCH" if not BAD else f"MISMATCHES {BAD}")
    return 0 if not BAD else 1


if __name__ == "__main__":
    sys.exit(main())
