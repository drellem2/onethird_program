"""longtail.py (mg-ce69): probe of the candidate lemma 'one-end WIN for long posets' (doc sec. 3.4).

Candidate (CONJECTURED in mg-5f14 sec. 5 as the live local form): for n >= n_0(D), every P in Pi_D has a
balanced pair inside {x} u Inc(x) for some extreme x at the bottom (WIN_bot) [or at the top].
Probe: take a base B (natural labelling = a linear extension) whose bottom window is balance-free, and grow it
upward by m tail elements, each placed above every current element except the last r in insertion order
(a new maximal element whose down-set is an ideal; range grows by at most r per side).  Report, as m grows,
WIN_bot, the range, the smallest distance of a bottom-window pair law from [1/3,2/3], and whether P is connected.
Then glue the dual on top (P_long u P_long^op joined by the same tail rule) to get a both-ends instance.
This is a targeted counterexample probe of one candidate, not a census.
"""
import sys
from fractions import Fraction
from lib import parse, fmt, analyse, upmasks, inc, rng, connected, windows, bal_pairs, THIRD, TWOTHIRD


def grow(dn, m, r):
    dn = list(dn)
    for _ in range(m):
        n = len(dn)
        dn.append(((1 << n) - 1) & ~sum(1 << j for j in range(max(0, n - r), n)))
    return dn


def dual(dn):
    n = len(dn)
    up = upmasks(dn)
    # element i of the dual is element n-1-i of P
    return [sum(1 << (n - 1 - j) for j in range(n) if up[n - 1 - i] >> j & 1) for i in range(n)]


def glue(lo, hi, r):
    """lo below, hi above; every element of hi is above every element of lo except the last r of lo
    for hi's first r elements (a staircase seam), making G(P) connected across the seam."""
    a, b = len(lo), len(hi)
    dn = list(lo)
    for i in range(b):
        lower = hi[i] << a
        base = (1 << a) - 1
        excl = sum(1 << j for j in range(max(0, a - r + i), a)) if i < r else 0
        dn.append(lower | (base & ~excl))
    return dn


def margin(p):
    return min(abs(p - THIRD), abs(p - TWOTHIRD)) * (1 if not (THIRD <= p <= TWOTHIRD) else -1)


def window_report(dn, e, B, side):
    n = len(dn)
    up = upmasks(dn)
    bot, top = windows(dn)
    W = bot if side == "bot" else top
    worst = None
    for w in W:
        for a in w:
            for b in w:
                if a < b and inc(dn, up, a, b):
                    mg = margin(Fraction(B[a][b], e))
                    worst = mg if worst is None or mg < worst else worst
    return worst  # negative => a balanced pair inside some window (WIN holds at that end)


def main():
    bases = {"P9": "9 0 0 2 2 3 b 2b 2f 7f", "rec11": "11 0 0 2 2 3 b 2b 2f af bf 1ff"}
    for name, s in bases.items():
        base = parse(s)
        for r in (1, 2, 3):
            row = []
            for m in (0, 2, 4, 8, 12, 16, 20):
                dn = grow(base, m, r)
                e, B, _ = analyse(dn)
                w = window_report(dn, e, B, "bot")
                row.append((m, len(dn), rng(dn), connected(dn), float(w)))
            print(f"{name} r={r}: " + "  ".join(f"m={m}(n={n},D={d},{'conn' if c else 'DISC'}) worstmargin={w:+.4f}" for m, n, d, c, w in row))
            sys.stdout.flush()


if __name__ == "__main__":
    main()
