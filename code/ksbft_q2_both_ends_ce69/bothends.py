"""bothends.py (mg-ce69): long both-ends witnesses (doc sec. 3.4).

Q_m = P9 grown by m tail elements (rule r=1 of longtail.py: each new element above all but the previous one),
then the dual of (P9 grown by m) glued on top with a staircase seam (glue(.., r=1)).  For each m: n, range,
connectedness (indecomposable), WIN at bottom and top (should both FAIL), worst window margins, and where the
balanced pairs are (min distance, in the natural labelling, from either end window).  Exact Fractions.
Firing control: the same report on 6 0 0 2 2 3 f grown the same way must show WIN_bot HOLDING (its (u,v) pair
is exactly 1/2 by the u<->v automorphism, and the tail preserves that automorphism).
"""
import sys
from fractions import Fraction
from lib import parse, fmt, analyse, upmasks, inc, rng, connected, windows, bal_pairs, win_holds
from longtail import grow, dual, glue, window_report


def report(dn, tag):
    e, B, _ = analyse(dn)
    bot, top = windows(dn)
    wb = set().union(*map(set, bot))
    wt = set().union(*map(set, top))
    bp = bal_pairs(dn, e, B)
    inside_b = win_holds(dn, e, B, "bot")
    inside_t = win_holds(dn, e, B, "top")
    touch = sum(1 for a, b, _ in bp if a in wb or b in wb or a in wt or b in wt)
    mb = window_report(dn, e, B, "bot")
    mt = window_report(dn, e, B, "top")
    print(f"{tag}: n={len(dn)} range={rng(dn)} {'conn' if connected(dn) else 'DISC'} "
          f"WIN_bot={'holds' if inside_b else 'FAILS'} WIN_top={'holds' if inside_t else 'FAILS'} "
          f"margin_bot={float(mb):+.4f} margin_top={float(mt):+.4f} "
          f"#balanced={len(bp)} #touching_a_window={touch} "
          f"balanced_pairs={[(a, b) for a, b, _ in bp][:12]}")
    sys.stdout.flush()
    return inside_b, inside_t


def main():
    P9 = parse("9 0 0 2 2 3 b 2b 2f 7f")
    for m in (0, 2, 4, 6, 10, 14):
        lo = grow(P9, m, 1)
        dn = glue(lo, dual(lo), 1)
        report(dn, f"Q_m m={m}")
    print("-- one-ended P9 + tail, larger m (bottom window only):")
    for m in (30, 45, 60):
        dn = grow(P9, m, 1)
        e, B, _ = analyse(dn)
        print(f"  m={m} n={len(dn)} range={rng(dn)} conn={connected(dn)} WIN_bot={'holds' if win_holds(dn, e, B, 'bot') else 'FAILS'} margin_bot={float(window_report(dn, e, B, 'bot')):+.6f}")
        sys.stdout.flush()
    print("-- control: 6 0 0 2 2 3 f grown (WIN_bot must HOLD):")
    W6 = parse("6 0 0 2 2 3 f")
    ok = True
    for m in (0, 4, 10):
        dn = grow(W6, m, 1)
        e, B, _ = analyse(dn)
        h = win_holds(dn, e, B, "bot")
        ok &= h
        print(f"  m={m} n={len(dn)} WIN_bot={'holds' if h else 'FAILS'}")
    print("CONTROL", "FIRES" if ok else "DID_NOT_FIRE")


if __name__ == "__main__":
    main()
