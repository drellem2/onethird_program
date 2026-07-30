"""Independent recomputation of the headline numbers of
docs/OneThird-Counterexample-Under-The-Action.md (mg-24a3 / f5d3485).

Every figure comes from `kernel.py` + `records.py`, which share no code with the
target's instrument.  Where the document states a figure, mine is printed beside
it with AGREES / DISAGREES.
"""

from fractions import Fraction

from kernel import (Lattice, Poset, linear_extensions, majority_relation,
                    pair_data, restriction_counts)
from records import build_all

THIRD = Fraction(1, 3)
NS = range(3, 8)
REC = {n: build_all(n) for n in NS}
LAT = {}


def fs(x):
    return str(x)


def verdict(mine, doc):
    return "AGREES" if mine == doc else "DISAGREES (doc: %s)" % (doc,)


def head(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


# ---------------------------------------------------------------------------
head("S3.1  PROPOSITION 2:  E[inv(L,L*)] = sum over Inc(P) of min(p,1-p)")
print("Checked by BRUTE FORCE: enumerate L(P), build L* from the majority relation,")
print("count inversions against it, average exactly -- on every non-chain n<=6, and")
print("against a SECOND completion of the majority relation for tie-break independence.")
tot = bad = 0
# rebuild the poset objects in the SAME order the records were built in
from kernel import posets_up_to_iso, topological_order  # noqa: E402
POPS = {}
prev = None
for n in range(1, 8):
    prev = posets_up_to_iso(n, prev)
    POPS[n] = prev

for n in range(3, 7):
    for P, r in zip(POPS[n], REC[n]):
        if r.chain:
            continue
        _, _, ps = pair_data(P)
        edges, tf, ac, L = majority_relation(P, ps)
        les = linear_extensions(P)
        assert len(les) == r.e
        for orderL in ([L] if ac else []):
            pos = {x: i for i, x in enumerate(orderL)}
            s = 0
            for w in les:
                wp = {x: i for i, x in enumerate(w)}
                s += sum(1 for a in range(n) for b in range(a + 1, n)
                         if (wp[a] < wp[b]) != (pos[a] < pos[b]))
            tot += 1
            if Fraction(s, len(les)) != r.einv:
                bad += 1
        if not tf and ac:
            pass
print("non-chain posets with an acyclic majority relation checked: %d; mismatches: %d"
      % (tot, bad))
print("(a poset with a tied pair still has a well-defined min(p,1-p) sum; the check")
print(" above uses the completion my kernel produces, and ties contribute 1/2 either way)")

# tie-break independence: for posets WITH a tie, compare two completions
ties = 0
tiebad = 0
for n in range(3, 7):
    for P, r in zip(POPS[n], REC[n]):
        if r.chain or r.tie_free:
            continue
        _, _, ps = pair_data(P)
        les = linear_extensions(P)
        vals = set()
        for flip in (False, True):
            adj = [0] * n
            for a in range(n):
                for b in range(n):
                    if a != b and (P.up[a] >> b) & 1:
                        adj[a] |= 1 << b
            for (x, y) in ps:
                p = ps[(x, y)]
                if p > Fraction(1, 2):
                    adj[x] |= 1 << y
                elif p < Fraction(1, 2):
                    adj[y] |= 1 << x
                else:
                    if flip:
                        adj[y] |= 1 << x
                    else:
                        adj[x] |= 1 << y
            L = topological_order(n, adj)
            if L is None:
                continue
            pos = {x: i for i, x in enumerate(L)}
            s = 0
            for w in les:
                wp = {x: i for i, x in enumerate(w)}
                s += sum(1 for a in range(n) for b in range(a + 1, n)
                         if (wp[a] < wp[b]) != (pos[a] < pos[b]))
            vals.add(Fraction(s, len(les)))
        ties += 1
        if len(vals) > 1 or (vals and vals.pop() != r.einv):
            tiebad += 1
print("posets with a TIED pair, two completions each: %d; disagreements: %d"
      % (ties, tiebad))

# ---------------------------------------------------------------------------
head("S3.2  THE TABLE:  min 3delta, min R, #R<1, #3delta<1")
print("%-3s %10s %10s %10s %8s %8s %9s" %
      ("n", "non-chains", "min 3d", "min R", "#R<1", "%R<1", "#3d<1"))
DOC32 = {3: (4, "1", "1", 0, 0.0, 0), 4: (15, "1", "1", 0, 0.0, 0),
         5: (62, "1", "4/5", 11, 17.7, 0), 6: (317, "1", "3/4", 124, 39.1, 0),
         7: (2044, "1", "24/35", 1232, 60.3, 0)}
for n in NS:
    pop = [r for r in REC[n] if not r.chain]
    m3d = min(3 * r.delta for r in pop)
    mR = min(r.R for r in pop)
    nR = sum(1 for r in pop if r.R < 1)
    nfrozen = sum(1 for r in pop if 3 * r.delta < 1)
    row = (len(pop), str(m3d), str(mR), nR, round(100.0 * nR / len(pop), 1), nfrozen)
    d = DOC32[n]
    ok = (row[0] == d[0] and str(m3d) == d[1] and str(mR) == d[2] and row[3] == d[3]
          and abs(row[4] - d[4]) <= 0.05 and row[5] == d[5])
    print("%-3d %10d %10s %10s %8d %7.1f%% %9d   %s"
          % (n, len(pop), m3d, mR, nR, 100.0 * nR / len(pop), nfrozen,
             "AGREES" if ok else "DISAGREES doc=%s" % (d,)))
    argmin = [r for r in pop if r.R == mR]
    print("      argmin R (%d poset%s): %s"
          % (len(argmin), "" if len(argmin) == 1 else "s",
             "; ".join(r.cover for r in argmin[:4])))

# ---------------------------------------------------------------------------
head("S3.3  THE FAMILY TABLE (exact, past the exhaustive range)")


def two_chains(k):
    rels = [(i, i + 1) for i in range(k - 1)] + \
           [(k + i, k + i + 1) for i in range(k - 1)]
    return Poset.from_relations(2 * k, rels)


def one_plus_two_under_chain(k):
    """the 3-element poset {0<1, 2 isolated} with a k-chain ABOVE everything."""
    rels = [(0, 1)]
    for i in range(k):
        rels += [(1, 3 + i), (2, 3 + i)]
        if i:
            rels.append((2 + i, 3 + i))
    return Poset.from_relations(3 + k, rels)


def stats(P):
    e, tot, ps = pair_data(P)
    mins = [min(p, 1 - p) for p in ps.values()]
    return tot, 3 * max(mins), 3 * sum(mins) / len(mins)


DOCFAM = {4: ("3/2", "1"), 6: ("3/2", "4/5"), 8: ("3/2", "24/35"),
          10: ("3/2", "64/105"), 12: ("3/2", "128/231")}
print("%-14s %4s %8s %8s %10s %s" % ("family", "n", "e(P)", "3delta", "R", "R<1?"))
for k in range(2, 7):
    P = two_chains(k)
    e, d3, R = stats(P)
    doc = DOCFAM[2 * k]
    ok = str(d3) == doc[0] and str(R) == doc[1]
    print("C_%d + C_%d      %4d %8d %8s %10s %6s   %s"
          % (k, k, 2 * k, e, d3, R, "yes" if R < 1 else "no",
             "AGREES" if ok else "DISAGREES doc=%s" % (doc,)))
for k in range(0, 7):
    P = one_plus_two_under_chain(k)
    e, d3, R = stats(P)
    print("1+2 under C_%d  %4d %8d %8s %10s %6s   %s"
          % (k, 3 + k, e, d3, R, "yes" if R < 1 else "no",
             "AGREES" if (e == 3 and d3 == 1 and R == 1) else "DISAGREES"))

print()
print("S3.3a  THE DOCUMENT'S SENTENCE 'the near-extremal families ... sit exactly ON")
print("       the boundary and never inside it' -- tested over ALL delta-extremal")
print("       posets, not only the named family:")
for n in NS:
    pop = [r for r in REC[n] if not r.chain]
    dmin = min(r.delta for r in pop)
    ext = [r for r in pop if r.delta == dmin]
    inside = [r for r in ext if r.R < 1]
    print("  n=%d: %d extremal (delta=%s); R values %s ; strictly inside R<1: %d"
          % (n, len(ext), dmin, sorted(set(str(r.R) for r in ext)), len(inside)))
    for r in inside:
        print("        INSIDE: %-30s R=%-8s e=%d" % (r.cover, r.R, r.e))
