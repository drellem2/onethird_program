"""a2_disjunctive — mg-41b7's independent re-solve of mg-200d's disjunctive value.

The disjunction, stated from the mathematics rather than from mg-200d's prose:

    with `e` the identity and a linear extension of the (hypothetical) poset P, each
    pair {x,y} with x<y is EITHER comparable -- and then Pr[y before x] = 0 -- OR
    incomparable -- and then swapping an adjacent x,y is an involution of L(P), so
    J_k(x,y) = J_k(y,x) at EVERY slot k.

So the realisable set is a union of 2^C(n,2) polytopes indexed by the declared
comparable set C, and the exact value is the max over branches:

    branch(C):  support   = arrangements with no pair of C flipped
                cap rows  = Pr[flip {x,y}] <= 1/3    for {x,y} not in C
                sym rows  = J_k(x,y) = J_k(y,x)      for {x,y} not in C, every slot k
                objective = max E[inv_e]

Two exact facts used to make n = 6 tractable, both proved in the audit note:

  (R1) E[inv] = sum over pairs of the flip probability, and comparable pairs contribute
       0, so  value(branch C) <= |I|/3  where I is the incomparable set.  A branch can
       therefore only beat (n-1)/3 if |I| >= n.
  (R2) If C is not transitively closed, branch(C) has the SAME support as
       branch(closure(C)) -- both are the linear extensions of closure(C) -- but a
       SUPERSET of its rows.  So value(branch C) <= value(branch closure(C)) and the
       maximum over all branches equals the maximum over transitively closed branches.

usage:  python3 a2_disjunctive.py 3 4 5           # exhaustive over every branch
        python3 a2_disjunctive.py --min-inc 6 6   # only |I| >= 6, which by (R1) is the
                                                  # complete test of "> (n-1)/3"
"""
import sys
from fractions import Fraction as F
import liba41b7 as L


def closure(n, C):
    """Transitive closure of a set of increasing pairs (a,b), a<b."""
    C = set(C)
    changed = True
    while changed:
        changed = False
        for (a, b) in list(C):
            for (c, d) in list(C):
                if b == c and (a, d) not in C:
                    C.add((a, d))
                    changed = True
    return frozenset(C)


def branch_rows(n, C, P_all):
    """(support indices, rows, objective) for the branch with comparable set C."""
    keep = [s for s in P_all
            if not any(L.pos(s, b) < L.pos(s, a) for (a, b) in C)]
    if not keep:
        return None
    idx = {s: j for j, s in enumerate(keep)}
    I = [p for p in L.pairs(n) if p not in C]
    rows = [L.row_normalisation(n, keep)]
    for (a, b) in I:
        c = {j: F(1) for j, s in enumerate(keep) if L.pos(s, b) < L.pos(s, a)}
        if c:
            rows.append((c, "<=", F(1, 3)))
    rows.extend(L.rows_perslot_symmetry(n, keep, pairset=I))
    obj = L.objective_inv(n, keep)
    return keep, rows, obj, I


def solve_branch(n, C, P_all):
    b = branch_rows(n, C, P_all)
    if b is None:
        return None
    keep, rows, obj, I = b
    r = L.solve(len(keep), rows, obj)
    return r, keep, rows, obj, I


def run(n, min_inc=0, transitive_only=False, verbose_top=True):
    P_all = L.perms(n)
    prs = L.pairs(n)
    npair = len(prs)
    best = None
    nfeas = 0
    nbranch = 0
    nskip_nontrans = 0
    max_inc_pos = 0
    for mask in range(1 << npair):
        C = frozenset(prs[i] for i in range(npair) if mask >> i & 1)
        I = [p for p in prs if p not in C]
        if len(I) < min_inc:
            continue
        if transitive_only and closure(n, C) != C:
            nskip_nontrans += 1
            continue
        nbranch += 1
        out = solve_branch(n, C, P_all)
        if out is None:
            continue
        r, keep, rows, obj, Ib = out
        if r.status != "optimal":
            continue
        nfeas += 1
        if r.value > 0:
            max_inc_pos = max(max_inc_pos, len(Ib))
        if best is None or r.value > best[0]:
            best = (r.value, C, r, keep, rows, obj, Ib)
    return best, nfeas, nbranch, nskip_nontrans, max_inc_pos


def main(argv):
    min_inc = 0
    transitive_only = False
    ns = []
    i = 0
    while i < len(argv):
        if argv[i] == "--min-inc":
            min_inc = int(argv[i + 1]); i += 2
        elif argv[i] == "--transitive-only":
            transitive_only = True; i += 1
        else:
            ns.append(int(argv[i])); i += 1
    for n in ns or [3, 4]:
        base = F(n * (n - 1), 6)
        conj = F(n - 1, 3)
        print("=" * 78)
        print("n = %d   baseline C(n,2)/3 = %s   mg-200d's (n-1)/3 = %s   "
              "min |I| filter = %d   transitive-only = %s"
              % (n, base, conj, min_inc, transitive_only))
        best, nfeas, nbranch, nskip, max_inc_pos = run(n, min_inc, transitive_only)
        print("  branches examined %d   feasible %d   skipped non-transitive %d"
              % (nbranch, nfeas, nskip))
        if best is None:
            print("  NO FEASIBLE BRANCH under this filter -- so no branch beats the filter's floor")
            sys.stdout.flush()
            continue
        val, C, r, keep, rows, obj, I = best
        print("  MAX over branches: E[inv] = %s   eps_spec = %s   x baseline = %s"
              % (val, L.eps_spec(n, val), val / base))
        print("  (n-1)/3 = %s -> %s        2/(n+1) = %s -> %s"
              % (conj, "MATCH" if val == conj else "DIFFERS  <-- !!",
                 F(2, n + 1),
                 "MATCH" if L.eps_spec(n, val) == F(2, n + 1) else "DIFFERS  <-- !!"))
        print("  attained on comparable C = %s" % (sorted(C) or "{} (all incomparable)"))
        print("  incomparable there |I| = %d   (n-1 = %d);  max |I| over value>0 branches = %d"
              % (len(I), n - 1, max_inc_pos))
        print("  C transitively closed: %s" % (closure(n, C) == C))
        pe = L.check_primal(len(keep), rows, obj, r.x, r.value)
        de = L.check_dual(len(keep), rows, obj, r.y, r.value)
        print("  primal verifies: %s   dual certificate verifies: %s"
              % ("YES" if pe == [] else "NO %s" % pe[:3],
                 "YES" if de == [] else "NO %s" % de[:3]))
        print("  witness (%d atoms):" % len(r.x))
        for j, v in sorted(r.x.items(), key=lambda t: -t[1]):
            print("      mass %-8s  %s  inv=%d"
                  % (v, "".join(map(str, keep[j])), L.inv(keep[j])))
        # verify the witness against the FULL constraint story, by substitution
        x_full = {}
        allidx = {s: j for j, s in enumerate(L.perms(n))}
        for j, v in r.x.items():
            x_full[allidx[keep[j]]] = v
        rep = L.report(n, x_full)
        bad = [k for k in rep["slot_violations"] if (k[1], k[2]) in I]
        print("  witness check by substitution: mass=%s  E[inv]=%s  max flip=%s"
              % (rep["mass"], rep["einv"], max(rep["flips"].values())))
        print("    per-slot symmetry violated on INCOMPARABLE pairs: %d  (must be 0)" % len(bad))
        print("    comparable pairs with nonzero flip: %d  (must be 0)"
              % len([p for p in C if rep["flips"][p] != 0]))
        sys.stdout.flush()


if __name__ == "__main__":
    main(sys.argv[1:])
