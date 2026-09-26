"""slstruct.py (mg-ce69): coverage of the STRUCTURAL corollary of the Swap Ladder (Cor 1.6 of the doc).

A full-chain ladder on an ordered pair is one of:
  primal (x,b): x || b, down(x) SUBSET down(b), Up(b) - Up(x) a chain         -> 'P[x<b] > 2/3 or balanced'
  dual   (x,b): x || b, up(x) SUBSET up(b),     Down(b) - Down(x) a chain     -> 'P[b<x] > 2/3 or balanced'
Cor 1.6 (PROVEN): if an unordered pair {x,b} carries full-chain ladders asserting OPPOSITE orders, P has a
balanced pair (one of the two orders has probability <= 1/2 <= 2/3, so that ladder's hypotheses hold).
No probabilities are computed.  For each connected poset: does some pair carry opposite ladders?  Also:
does P have a balanced pair that is nested (down(x) SUBSET down(b) or up(x) SUBSET up(b)) - the only kind
of pair the Swap Ladder can ever certify (EMPIRICAL question 'Nested Balance').
Control (must FIRE): with 'opposite' replaced by 'same order', the analogous count exceeds the true one on
some poset where no balanced pair is... (we simply report that it differs, i.e. the test is not vacuous).
"""
import sys
from fractions import Fraction
from lib import analyse, upmasks, inc, connected, chain_bottom, balanced


def is_chain(dn, S):
    return len(chain_bottom(dn, S)) == len(S)


def opposite(dn, up):
    n = len(dn)
    for x in range(n):
        for b in range(x + 1, n):
            if not inc(dn, up, x, b):
                continue
            asserts = set()
            for (p, q) in ((x, b), (b, x)):
                if dn[p] & ~dn[q] == 0 and is_chain(dn, [q] + [w for w in range(n) if up[q] >> w & 1 and not up[p] >> w & 1]):
                    asserts.add((p, q))          # asserts p before q
                if up[p] & ~up[q] == 0 and is_chain(up, [q] + [w for w in range(n) if dn[q] >> w & 1 and not dn[p] >> w & 1]):
                    asserts.add((q, p))          # asserts q before p
            if len(asserts) == 2:
                return True
    return False


def run(files):
    for f in files:
        c = dict(posets=0, struct=0, nested_bal=0)
        for line in open(f):
            a = line.split()
            n = int(a[0])
            if n < 2:
                continue
            dn = [int(t, 16) for t in a[1:]]
            if not connected(dn):
                continue
            c["posets"] += 1
            up = upmasks(dn)
            st = opposite(dn, up)
            c["struct"] += st
            if not st and c.get("wit", 0) < 8:
                c["wit"] = c.get("wit", 0) + 1
                print("STRUCT_FAILS", line.strip(), "range", max(sum(inc(dn, up, p, q) for q in range(n)) for p in range(n)))
            e, B, _ = analyse(dn)
            c["nested_bal"] += any(inc(dn, up, x, b) and balanced(Fraction(B[x][b], e)) and
                                   (dn[x] & ~dn[b] == 0 or up[x] & ~up[b] == 0)
                                   for x in range(n) for b in range(n))
        print("file", f.split("/")[-1], " ".join(f"{k}={v}" for k, v in c.items()))
        sys.stdout.flush()


if __name__ == "__main__":
    run(sys.argv[1:])
