"""T3, T7, T8 -- testing the hypotheses of the branching-graph programme's own
definitions against what we actually have.

T3  Stanley's differential condition DU - UD = rI, and the same condition
    restricted to the ranks below the top (so that the trivial finiteness
    obstruction at 1-hat is not the whole story).  Run with POSITIVE CONTROLS:
    the two known 1-differential posets, Young's lattice and the
    Young-Fibonacci lattice, must pass; J(P) is then tested against them.

T7  Bergeron-Li axiom (2) for a tower of algebras -- an injective UNITAL
    algebra map A_m (x) A_n -> A_{m+n}.  The natural candidate here is block
    concatenation F(P) x F(Q) -> F(P + Q).  Measured: it is an injective
    semigroup homomorphism and it is NOT unital.

T8  Brown 2000 §4.3's hypothesis is a finite DISTRIBUTIVE lattice.  Which of
    the standard branching graphs satisfy it?
"""

import sys
from core_af28 import (poset_classes, ideals_of, moves_from_chains, partitions,
                       young_fibonacci, move_product, compatible)

OUT = sys.stdout


# ------------------------------------------------------------------- T3 -----

def updown_report(name, elems, rank, covers_up):
    """Check DU - UD = rI.  `covers_up[x]` lists the elements covering x.
    Returns (r_full, ok_full, r_trunc, ok_trunc, top_rank)."""
    idx = {x: i for i, x in enumerate(elems)}
    N = len(elems)
    covers_dn = {x: [] for x in elems}
    for x in elems:
        for y in covers_up[x]:
            covers_dn[y].append(x)
    maxrank = max(rank[x] for x in elems)

    def DU(x):
        v = {}
        for y in covers_up[x]:
            for z in covers_dn[y]:
                v[z] = v.get(z, 0) + 1
        return v

    def UD(x):
        v = {}
        for y in covers_dn[x]:
            for z in covers_up[y]:
                v[z] = v.get(z, 0) + 1
        return v

    def check(pred):
        r = None
        for x in elems:
            if not pred(x):
                continue
            a, b = DU(x), UD(x)
            diff = {}
            for k, v in a.items():
                diff[k] = diff.get(k, 0) + v
            for k, v in b.items():
                diff[k] = diff.get(k, 0) - v
            diff = {k: v for k, v in diff.items() if v != 0}
            if list(diff.keys()) != [x]:
                return (None, False)
            if r is None:
                r = diff[x]
            elif r != diff[x]:
                return (None, False)
        return (r, r is not None and r >= 1)

    r_full, ok_full = check(lambda x: True)
    r_tr, ok_tr = check(lambda x: rank[x] <= maxrank - 1)
    return r_full, ok_full, r_tr, ok_tr, maxrank


def young_lattice(maxrank):
    elems = [()]
    for r in range(1, maxrank + 1):
        elems.extend(partitions(r))
    rank = {x: sum(x) for x in elems}
    es = set(elems)
    covers = {}
    for x in elems:
        up = []
        for i in range(len(x) + 1):
            y = list(x)
            if i == len(x):
                y.append(1)
            else:
                y[i] += 1
            y = tuple(y)
            if y == tuple(sorted(y, reverse=True)) and y in es:
                up.append(y)
        covers[x] = up
    return elems, rank, covers


def t3(maxn=6, ctrl_rank=8):
    print("=" * 78, file=OUT)
    print("T3  Stanley's differential condition DU - UD = rI on J(P), with the", file=OUT)
    print("    two known 1-differential posets as POSITIVE CONTROLS.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("  CONTROLS (must pass on the ranks below the top; the top rank of a", file=OUT)
    print("  truncation never can, since U kills it):", file=OUT)
    e, rk, cv = young_lattice(ctrl_rank)
    rf, of_, rt, ot, mr = updown_report("Young", e, rk, cv)
    print("    Young's lattice   to rank %d: %d elements; whole: %s; ranks<=%d: r=%s %s"
          % (ctrl_rank, len(e), "r=%s" % rf if of_ else "FAILS", mr - 1, rt,
             "PASS" if ot else "FAILS"), file=OUT)
    ranks, cov = young_fibonacci(ctrl_rank)
    elems = [w for r in sorted(ranks) for w in ranks[r]]
    rk2 = {w: sum(w) for w in elems}
    rf2, of2, rt2, ot2, mr2 = updown_report("YF", elems, rk2, cov)
    print("    Young-Fibonacci   to rank %d: %d elements; whole: %s; ranks<=%d: r=%s %s"
          % (ctrl_rank, len(elems), "r=%s" % rf2 if of2 else "FAILS", mr2 - 1, rt2,
             "PASS" if ot2 else "FAILS"), file=OUT)
    print(file=OUT)
    print("  TEST -- J(P) for every poset P:", file=OUT)
    print("   n  classes   J(P) differential   J(P) differential below the top", file=OUT)
    passers = []
    for n in range(1, maxn + 1):
        cls = poset_classes(n)
        cf = ct = 0
        for up in cls:
            ids = ideals_of(up)
            rank = {I: bin(I).count("1") for I in ids}
            idset = set(ids)
            covers = {}
            for I in ids:
                covers[I] = [J for J in ids
                             if rank[J] == rank[I] + 1 and I & J == I]
            _, okf, _, okt, _ = updown_report("J(P)", ids, rank, covers)
            cf += okf
            ct += okt
            if okt:
                passers.append((n, up))
        print("  %2d  %7d   %17d   %31d" % (n, len(cls), cf, ct), file=OUT)
    print(file=OUT)
    print("  The posets whose J(P) satisfies the condition below the top:", file=OUT)
    for n, up in passers:
        print("    n=%d  up-sets %s" % (n, list(up)), file=OUT)
    print(file=OUT)
    print("  Reading: the condition fails at 1-hat for EVERY finite J(P) because", file=OUT)
    print("  U(1-hat) = 0 while UD(1-hat) contains 1-hat, so no finite lattice", file=OUT)
    print("  with a maximum is a differential poset.  The truncated column is", file=OUT)
    print("  there so that this trivial obstruction is not doing all the work.", file=OUT)
    print(file=OUT)
    return passers


# ------------------------------------------------------------------- T7 -----

def shift_move(x, k):
    return tuple(B << k for B in x)


def disjoint_union(upP, upQ):
    m = len(upP)
    return tuple(list(upP) + [r << m for r in upQ])


def t7(maxn=3):
    print("=" * 78, file=OUT)
    print("T7  Bergeron-Li axiom (2) for a tower of algebras: an injective UNITAL", file=OUT)
    print("    algebra map A_m (x) A_n -> A_{m+n}.  Candidate: concatenation", file=OUT)
    print("    F(P) x F(Q) -> F(P + Q).", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("  |P| |Q|  pairs   lands in F(P+Q)  injective  homomorphism  unital", file=OUT)
    tot_bad_land = tot_bad_inj = tot_bad_hom = tot_unital = tot_cases = 0
    for np_ in range(1, maxn + 1):
        for nq in range(1, maxn + 1):
            bad_land = bad_hom = 0
            noninj = 0
            unital = 0
            cases = 0
            for upP in poset_classes(np_):
                for upQ in poset_classes(nq):
                    cases += 1
                    R = disjoint_union(upP, upQ)
                    FP = moves_from_chains(upP)
                    FQ = moves_from_chains(upQ)
                    FR = set(moves_from_chains(R))
                    img = {}
                    for x in FP:
                        for y in FQ:
                            z = x + shift_move(y, np_)
                            if z not in FR:
                                bad_land += 1
                            img.setdefault(z, []).append((x, y))
                    if len(img) != len(FP) * len(FQ):
                        noninj += 1
                    for x1 in FP:
                        for x2 in FP:
                            for y1 in FQ:
                                for y2 in FQ:
                                    lhs = move_product(x1 + shift_move(y1, np_),
                                                       x2 + shift_move(y2, np_))
                                    rhs = (move_product(x1, x2)
                                           + shift_move(move_product(y1, y2), np_))
                                    if lhs != rhs:
                                        bad_hom += 1
                    idP = ((1 << np_) - 1,)
                    idQ = ((1 << nq) - 1,)
                    idR = ((1 << (np_ + nq)) - 1,)
                    if idP + shift_move(idQ, np_) == idR:
                        unital += 1
            tot_cases += cases
            tot_bad_land += bad_land
            tot_bad_inj += noninj
            tot_bad_hom += bad_hom
            tot_unital += unital
            print("  %3d %3d  %5d   %14s  %9s  %12s  %s"
                  % (np_, nq, cases,
                     "0 bad" if bad_land == 0 else "%d BAD" % bad_land,
                     "%d/%d" % (cases - noninj, cases),
                     "0 bad" if bad_hom == 0 else "%d BAD" % bad_hom,
                     "%d/%d" % (unital, cases)), file=OUT)
    print(file=OUT)
    print("  Concatenation is an injective SEMIGROUP homomorphism (%d cases, %d bad"
          % (tot_cases, tot_bad_land + tot_bad_hom), file=OUT)
    print("  landings/products, %d non-injective) and is UNITAL in %d of %d cases:"
          % (tot_bad_inj, tot_unital, tot_cases), file=OUT)
    print("  it sends (1_P, 1_Q) to the two-block move, not to 1_{P+Q}.  So the", file=OUT)
    print("  map exists but does NOT satisfy Bergeron-Li axiom (2) as stated.", file=OUT)
    print("  Whether some other map does, this test does not decide.", file=OUT)
    print(file=OUT)
    return tot_bad_land, tot_bad_inj, tot_bad_hom, tot_unital, tot_cases


# ------------------------------------------------------------------- T8 -----

def lattice_report(name, elems, leq):
    """Is (elems, leq) a lattice, and is it distributive?  Brute force."""
    n = len(elems)
    L = [[leq(a, b) for b in elems] for a in elems]
    join = [[None] * n for _ in range(n)]
    meet = [[None] * n for _ in range(n)]
    is_lat = True
    for i in range(n):
        for j in range(n):
            ub = [k for k in range(n) if L[i][k] and L[j][k]]
            lb = [k for k in range(n) if L[k][i] and L[k][j]]
            mins = [k for k in ub if all(m == k or not L[m][k] for m in ub)]
            maxs = [k for k in lb if all(m == k or not L[k][m] for m in lb)]
            if len(mins) != 1 or len(maxs) != 1:
                is_lat = False
            else:
                join[i][j] = mins[0]
                meet[i][j] = maxs[0]
    if not is_lat:
        return False, None
    dist = True
    witness = None
    for a in range(n):
        for b in range(n):
            for c in range(n):
                lhs = meet[a][join[b][c]]
                rhs = join[meet[a][b]][meet[a][c]]
                if lhs != rhs:
                    dist = False
                    if witness is None:
                        witness = (elems[a], elems[b], elems[c])
    return True, (dist, witness)


def t8(rank=6):
    print("=" * 78, file=OUT)
    print("T8  Brown 2000 §4.3's hypothesis is a finite DISTRIBUTIVE lattice.", file=OUT)
    print("    Which standard branching graphs meet it?", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("  Tested on INTERVALS [0-hat, x], not on truncations: a truncation of", file=OUT)
    print("  an infinite lattice at rank r is not a lattice at all (two elements", file=OUT)
    print("  of top rank lose their join), so it would answer the wrong question.", file=OUT)
    print(file=OUT)

    def sub(a, b):
        return len(a) <= len(b) and all(a[k] <= b[k] for k in range(len(a)))
    bad_y = 0
    n_y = 0
    for n in range(0, rank + 1):
        for lam in ([()] if n == 0 else partitions(n)):
            elems = [mu for m in range(n + 1)
                     for mu in ([()] if m == 0 else partitions(m)) if sub(mu, lam)]
            lat, res = lattice_report("Y", elems, sub)
            n_y += 1
            if not (lat and res[0]):
                bad_y += 1
    print("  Young's lattice: every interval [0, lambda] with |lambda| <= %d" % rank, file=OUT)
    print("      %d intervals, non-distributive: %d" % (n_y, bad_y), file=OUT)

    ranks, cov = young_fibonacci(rank)
    elems_all = [w for r in sorted(ranks) for w in ranks[r]]
    up = {w: set(cov[w]) for w in elems_all}
    changed = True
    while changed:
        changed = False
        for w in elems_all:
            new = set(up[w])
            for v in up[w]:
                new |= up[v]
            if new != up[w]:
                up[w] = new
                changed = True

    def leq(a, b):
        return a == b or b in up[a]
    bad_yf = 0
    n_yf = 0
    first = None
    notlat = 0
    for w in elems_all:
        elems = [v for v in elems_all if leq(v, w)]
        lat2, res2 = lattice_report("YF", elems, leq)
        n_yf += 1
        if not lat2:
            notlat += 1
            continue
        if not res2[0]:
            bad_yf += 1
            if first is None:
                first = (w, res2[1])
    print("  Young-Fibonacci: every interval [0, w] with rank(w) <= %d" % rank, file=OUT)
    print("      %d intervals, not a lattice: %d, non-distributive: %d"
          % (n_yf, notlat, bad_yf), file=OUT)
    if first:
        print("      smallest witness: w = %s, failing triple (a,b,c) = %s"
              % (first[0], first[1]), file=OUT)
    print(file=OUT)
    print("  Reading: of the two 1-differential LATTICES (Stanley 1988 for", file=OUT)
    print("  Young's; Byrnes 2012 that there are no others), only Young's is", file=OUT)
    print("  distributive -- the Young-Fibonacci lattice is modular but not", file=OUT)
    print("  distributive.  So Brown §4.3's construction reaches the Young graph", file=OUT)
    print("  and does not reach the other one.", file=OUT)
    print(file=OUT)
    return (n_y, bad_y, n_yf, bad_yf, first)


if __name__ == "__main__":
    p = t3()
    t7res = t7()
    t8res = t8()
    print("=" * 78, file=OUT)
    print("SUMMARY t_branching: T3 truncated-passers %d; T7 unital %d of %d;"
          % (len(p), t7res[3], t7res[4]), file=OUT)
    print("  T8 Young intervals non-distributive %d of %d; Young-Fibonacci"
          " intervals non-distributive %d of %d"
          % (t8res[1], t8res[0], t8res[3], t8res[2]), file=OUT)
    print("=" * 78, file=OUT)
