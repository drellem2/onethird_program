"""A1 -- the one POSITIVE claim of mg-af28 (ledger B1), re-tested as an equality
from a disjoint instrument.

mg-af28 B1: "J(D_lambda) is the interval [0, lambda] of Young's lattice, by the
map 'ideal -> shape', and the maximal chains of J(D_lambda) are SYT(lambda) with
e(D_lambda) = f^lambda."

What is disjoint here:
  * the poset is carried as frozenset down-sets, not up-set bitmasks;
  * the ideal lattice is built by downward closure of subsets;
  * the interval [0, lambda] is built by generating Young's lattice as a GRAPH
    from the ADD-A-CORNER cover rule and then taking the down-set of lambda in
    the transitive closure -- af28 built it by direct containment filtering of
    partitions.  If the two agree, containment and the cover-rule closure agree;
  * f^lambda is computed by the BRANCHING RECURSION, not the hook length formula;
  * the order isomorphism is checked in BOTH directions on all pairs, and I also
    check it is a LATTICE isomorphism (meet and join preserved), which af28 did
    not check;
  * SYT are matched by a bijection from linear extensions built through the
    tableau (value -> cell) encoding, and separately counted.

A1 also runs the piece af28's headline needs but did not test: that the
Gelfand-Tsetlin index-set statement is about PATHS FROM THE BOTTOM of the
branching graph, i.e. that maximal chains of [0, lambda] and maximal chains of
J(D_lambda) are the same set under the same bijection.
"""

import sys
from kern6ad0 import (partitions, contains, straight_poset, ideals, cells,
                      linear_extensions, n_linear_extensions, f_lambda,
                      is_lattice_and_distributive)

OUT = sys.stdout


def young_interval_by_covers(lam):
    """The interval [0, lambda] of Young's lattice, generated from the
    ADD-A-CORNER cover rule and closed downwards from lambda.

    Deliberately NOT built by filtering partitions for containment: the covers
    are generated, the reachability is computed, and containment is then a
    CONCLUSION to be compared, not the definition used."""
    n = sum(lam)

    def down_covers(mu):
        """the partitions covered by mu (remove one removable corner)"""
        out = []
        for i in range(len(mu)):
            if i + 1 == len(mu) or mu[i] > mu[i + 1]:
                nu = list(mu)
                nu[i] -= 1
                while nu and nu[-1] == 0:
                    nu.pop()
                out.append(tuple(nu))
        return out

    seen = {lam}
    frontier = [lam]
    cov = {}
    while frontier:
        nxt = []
        for mu in frontier:
            dc = down_covers(mu)
            cov[mu] = dc
            for nu in dc:
                if nu not in seen:
                    seen.add(nu)
                    nxt.append(nu)
        frontier = nxt
    cov.setdefault((), [])
    # transitive closure -> the order relation on the interval
    elems = sorted(seen, key=lambda m: (sum(m), m))
    below = {m: set() for m in elems}
    for m in elems:
        for c in cov.get(m, []):
            below[m].add(c)
    changed = True
    while changed:
        changed = False
        for m in elems:
            new = set(below[m])
            for c in list(below[m]):
                new |= below[c]
            if new != below[m]:
                below[m] = new
                changed = True
    return elems, below


def maximal_chains(elems, below):
    """Maximal chains from the minimum to the maximum, as tuples."""
    top = max(elems, key=lambda m: sum(m))
    covers_up = {m: [] for m in elems}
    for a in elems:
        for b in elems:
            if a in below[b] and not any(
                    (a in below[c]) and (c in below[b]) for c in elems
                    if c != a and c != b):
                covers_up[a].append(b)
    res = []

    def rec(cur, path):
        if cur == top:
            res.append(tuple(path))
            return
        for nxt in covers_up[cur]:
            rec(nxt, path + [nxt])
    rec((), [()])
    return res


def shape_of(I, cs, nrows):
    rows = [0] * nrows
    for a in I:
        rows[cs[a][0]] += 1
    while rows and rows[-1] == 0:
        rows.pop()
    return tuple(rows)


def main(maxn=7):
    print("=" * 78, file=OUT)
    print("A1  mg-af28 ledger B1, re-tested as an equality from a disjoint", file=OUT)
    print("    instrument.  Young's lattice is built here from the ADD-A-CORNER", file=OUT)
    print("    cover rule and closed downwards, NOT by containment filtering;", file=OUT)
    print("    f^lambda is the branching recursion, NOT the hook length formula.", file=OUT)
    print("=" * 78, file=OUT)
    print()
    print("   n  lambda            |J(D_l)|  |[0,l]|  ORD  LAT  e(D_l)  f^lam  SYT  CHAINS",
          file=OUT)
    bad_ord = bad_lat = bad_f = bad_ch = 0
    tot = 0
    for n in range(1, maxn + 1):
        for lam in partitions(n):
            tot += 1
            P, cs = straight_poset(lam)
            ids = ideals(P)
            elems, below = young_interval_by_covers(lam)
            img = [shape_of(I, cs, len(lam)) for I in ids]

            # (a) bijection
            bij = (len(set(img)) == len(ids) and set(img) == set(elems))
            # (b) order isomorphism both directions on every pair
            ordok = bij
            if bij:
                for a in range(len(ids)):
                    for b in range(len(ids)):
                        lhs = ids[a] <= ids[b]
                        rhs = (img[a] == img[b]) or (img[a] in below[img[b]])
                        if lhs != rhs:
                            ordok = False
            # (c) LATTICE isomorphism: meet = intersection <-> componentwise min,
            #     join = union <-> componentwise max.  af28 did not test this.
            latok = bij
            if bij:
                pos = {img[k]: ids[k] for k in range(len(ids))}
                for a in range(len(ids)):
                    for b in range(len(ids)):
                        mu, nu = img[a], img[b]
                        L = max(len(mu), len(nu))
                        mu2 = tuple(list(mu) + [0] * (L - len(mu)))
                        nu2 = tuple(list(nu) + [0] * (L - len(nu)))
                        mn = tuple(min(x, y) for x, y in zip(mu2, nu2))
                        mx = tuple(max(x, y) for x, y in zip(mu2, nu2))
                        while mn and mn[-1] == 0:
                            mn = mn[:-1]
                        while mx and mx[-1] == 0:
                            mx = mx[:-1]
                        if mn not in pos or mx not in pos:
                            latok = False
                            break
                        if pos[mn] != (ids[a] & ids[b]):
                            latok = False
                        if pos[mx] != (ids[a] | ids[b]):
                            latok = False
                    if not latok:
                        break
            if not ordok:
                bad_ord += 1
            if not latok:
                bad_lat += 1

            # (d) e(D_lambda) = f^lambda, by branching recursion
            e = n_linear_extensions(P)
            fl = f_lambda(lam)
            if e != fl:
                bad_f += 1

            # (e) maximal chains of [0,lambda] = maximal chains of J(D_lambda),
            #     matched through the same map, and both = SYT(lambda)
            mc = maximal_chains(elems, below)
            le = linear_extensions(P)
            # a linear extension gives the chain of ideals it sweeps out
            le_chains = set()
            for c in le:
                path = [()]
                cur = set()
                for e_ in c:
                    cur.add(e_)
                    path.append(shape_of(frozenset(cur), cs, len(lam)))
                le_chains.add(tuple(path))
            chok = (le_chains == set(mc) and len(mc) == fl)
            if not chok:
                bad_ch += 1

            if n >= 5:      # keep the printed table readable; totals cover all
                pass
            print("  %2d  %-16s %8d %8d  %3s  %3s  %6d %6d %4d  %s"
                  % (n, str(lam), len(ids), len(elems),
                     "." if ordok else "BAD", "." if latok else "BAD",
                     e, fl, len(mc), "." if chok else "BAD"), file=OUT)
    print(file=OUT)
    print("  partitions tested: %d" % tot, file=OUT)
    print("  order-isomorphism bad: %d" % bad_ord, file=OUT)
    print("  LATTICE-isomorphism bad (meet/join preserved): %d" % bad_lat, file=OUT)
    print("  e(D_lambda) != f^lambda: %d" % bad_f, file=OUT)
    print("  maximal chains of J(D_l) != maximal chains of [0,l], or != f^lam: %d"
          % bad_ch, file=OUT)
    print(file=OUT)
    print("  VERDICT on B1: %s" % (
        "CONFIRMED, and strengthened to a lattice isomorphism"
        if (bad_ord == bad_lat == bad_f == bad_ch == 0) else "NOT CONFIRMED"), file=OUT)
    print(file=OUT)
    return bad_ord, bad_lat, bad_f, bad_ch


if __name__ == "__main__":
    r = main()
    print("=" * 78, file=OUT)
    print("SUMMARY a1_contact: ord %d, lat %d, f %d, chains %d (all should be 0)"
          % r, file=OUT)
    print("=" * 78, file=OUT)
