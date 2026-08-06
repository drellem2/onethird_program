"""P3 — a test of THIS document's own forward vector, built so it can kill it.

The forward vector (§5 of the README): a (LIB-weak) violation needs Theta(n)
elements of Theta(n) mobility; among Theta(n) macroscopic windows inside [n]
two must be NEARLY IDENTICAL by pigeonhole; and two incomparable elements with
nearly identical position laws ought to be near-balanced, contradicting frozen.

The middle step is pigeonhole and is not in doubt.  The LAST step is the
micro-lemma this probe tests, in its MARGINAL form:

    (MW)  min(p, 1-p) >= c * (1 - TV(law(pos x), law(pos y)))   for x || y,

with TV the total-variation distance between the absolute-position laws.  If
(MW) held with c >= 1/3 the vector would close the last step.  A pair with
(1 - TV) large and min(p, 1-p) small REFUTES (MW) and is the outcome this
probe is built to be able to report.

POPULATION: every naturally labelled poset on n elements, n = 3..6, that is
            not a chain; and within it, every incomparable pair.
GRAIN:      one incomparable pair (x,y) of one naturally labelled poset.
"""

import sys
from itertools import combinations

from lib_c3ca import down_masks, naturally_labelled_posets

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6


def extensions(n, down):
    """Yield every linear extension as a tuple of elements in position order."""
    out = []
    cur = []

    def rec(placed):
        if len(cur) == n:
            out.append(tuple(cur))
            return
        for x in range(n):
            if placed >> x & 1:
                continue
            if down[x] & ~placed:
                continue
            cur.append(x)
            rec(placed | 1 << x)
            cur.pop()

    rec(0)
    return out


print("P3 — testing (MW) on the marginal position laws.")
print("POPULATION: all naturally labelled non-chain posets, n = 3..6;")
print("GRAIN: one incomparable pair of one such poset.")
print()

worst = []            # (1-TV, min(p,1-p), n, pairs, x, y)
counts = {}
for n in range(3, NMAX + 1):
    pairs_seen = 0
    refuters = []
    band_min = {0.5: 1.0, 0.7: 1.0, 0.75: 1.0, 0.8: 1.0, 0.85: 1.0,
                0.9: 1.0, 0.99: 1.0}
    # s* = sup{ 1-TV : the pair is NOT balanced, i.e. min(p,1-p) < 1/3 }.
    # "1-TV > s* implies balanced" is exactly the statement the pigeonhole
    # needs, so s* is the sharp readout, not the linear form.
    s_star = -1.0
    s_star_witness = None
    for rel in naturally_labelled_posets(n):
        down = down_masks(n, rel)
        les = extensions(n, down)
        tot = len(les)
        pos = [[0] * n for _ in range(n)]        # pos[x][i] = #LEs with x at slot i
        before = [[0] * n for _ in range(n)]     # before[x][y] = #LEs with x before y
        for le in les:
            where = [0] * n
            for i, x in enumerate(le):
                pos[x][i] += 1
                where[x] = i
            for x, y in combinations(range(n), 2):
                if where[x] < where[y]:
                    before[x][y] += 1
                else:
                    before[y][x] += 1
        for x, y in combinations(range(n), 2):
            if (x, y) in rel:
                continue
            pairs_seen += 1
            p = before[y][x] / tot            # Pr[y before x]
            mn = min(p, 1 - p)
            tv = 0.5 * sum(abs(pos[x][i] - pos[y][i]) for i in range(n)) / tot
            sim = 1 - tv
            for t in band_min:
                if sim >= t and mn < band_min[t]:
                    band_min[t] = mn
            if mn < 1 / 3 - 1e-12 and sim > s_star:
                s_star = sim
                s_star_witness = (sorted(rel), x, y, mn)
            if sim >= 0.5 and mn < 1 / 3:
                refuters.append((sim, mn, sorted(rel), x, y))
    counts[n] = pairs_seen
    print(f"n = {n}: {pairs_seen} incomparable pairs (GRAIN: pair x poset)")
    for t in sorted(band_min):
        v = band_min[t]
        print(f"  min of min(p,1-p) over pairs with 1-TV >= {t:.2f} : "
              f"{v:.6f}" + ("   [no such pair]" if v == 1.0 else ""))
    print(f"  pairs with 1-TV >= 0.5 AND min(p,1-p) < 1/3 (refutes (MW) at c=1/3): "
          f"{len(refuters)}")
    print(f"  s* = sup{{1-TV : NOT balanced}} = {s_star:.6f}   "
          f"(so '1-TV > {s_star:.6f} => balanced' holds on this whole population)")
    if s_star_witness:
        rel, x, y, mn = s_star_witness
        print(f"    s* witness: pair ({x},{y}), min(p,1-p) = {mn:.6f}, relation {rel}")
    if refuters:
        refuters.sort(key=lambda r: (r[1], -r[0]))
        for sim, mn, rel, x, y in refuters[:3]:
            print(f"    REFUTER: 1-TV = {sim:.6f}, min(p,1-p) = {mn:.6f}, "
                  f"pair ({x},{y}), relation {rel}")
    print()

print("Reading: (MW) at c = 1/3 is what the forward vector would need from the")
print("MARGINAL laws.  Any refuter above means the marginal form is false and the")
print("vector must be run on the CONDITIONAL windows I_x(tau) instead — which is")
print("where mg-a1ec Prop. 4.1 lives anyway.")
