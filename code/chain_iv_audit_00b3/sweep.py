"""sweep — one exhaustive pass over the naturally labelled posets on [n], cached.

Produces, per PRIMITIVE poset: (gap, min_k Q_k as an exact Fraction, argmin k, down-masks).
`c` is NOT stored: it is a function of the two, and storing it would let a downstream
script quote a `c` whose gap it never saw.  Every consumer recomputes it at the print
site from `(1 - minQ)/(1 - gap)`.

The cache lives OUTSIDE the repository (scratch), because a committed 86 277-row table is
a number nobody can check and the sweep that makes it takes under two minutes.
"""

import os
import sys
from fractions import Fraction as F

import lib00b3 as L
import tridiag as TD

CACHE = os.environ.get(
    "MG00B3_CACHE",
    "/private/tmp/claude-501/-Users-daniel--pogo-polecats-q00b3/"
    "85db5637-1ab2-42c8-9deb-0d4a97793397/scratchpad/mg00b3cache")


def _path(n):
    return os.path.join(CACHE, f"sweep_n{n}.txt")


def compute(n):
    rows = []
    for down in L.all_posets(n):
        if not L.is_primitive(n, down):
            continue
        T, N = L.transport_int(n, down)
        Q = L.prefix_Q_all(n, T, N)
        mq = min(Q)
        k = Q.index(mq) + 1
        gap = TD.lambda2(n, L.L_floats(n, T, N))
        rows.append((down, gap, mq, k))
    return rows


def load(n, verbose=True):
    p = _path(n)
    if os.path.exists(p):
        rows = []
        with open(p) as fh:
            for line in fh:
                a, b, c, d = line.split()
                rows.append((tuple(int(x) for x in a.split(",")),
                             float(b), F(c), int(d)))
        return rows
    if verbose:
        print(f"  [sweep] computing n={n} (no cache) ...", file=sys.stderr)
    rows = compute(n)
    os.makedirs(CACHE, exist_ok=True)
    with open(p, "w") as fh:
        for down, gap, mq, k in rows:
            fh.write("%s %.17g %s %d\n" % (",".join(str(x) for x in down), gap, mq, k))
    return rows


def informative(rows):
    """Drop the posets where lambda_std = 0 (gap = 1); `c` is undefined there."""
    return [r for r in rows if r[1] < 1.0 - 1e-12]


def c_of(row):
    return (1.0 - float(row[2])) / (1.0 - row[1])


def C3gap_of(row):
    return float(row[2]) / row[1]


if __name__ == "__main__":
    for n in (int(x) for x in sys.argv[1:]):
        rows = load(n)
        inf = informative(rows)
        print(f"n={n}: primitive {len(rows)}, informative {len(inf)}, "
              f"min c {min(c_of(r) for r in inf):.6f}")
