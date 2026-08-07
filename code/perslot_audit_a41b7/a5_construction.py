"""a5_construction — the >= direction, and the two side claims, checked independently.

mg-200d's document splits its result in two and this script checks both halves
separately, because they have different kinds:

  >=  direction:  an explicit construction giving E[inv] = (n-1)/3 in SOME branch,
                  claimed as a THEOREM for every n.  Checked here at n = 3..20 by
                  substitution -- no LP, so nothing can be hidden in a solver.
  <=  direction:  a conjecture at landing.  Not checked here; see a3_n6.py.

Also checked, because they are the other two numbers the document publishes:

  * the SOUND BRANCH-FREE surrogate  J_k(y,x) <= J_k(x,y)  buys nothing  (= C(n,2)/3)
  * the sound DISJUNCTIVE AGGREGATE value is  2/3, 5/3, 7/3  at n = 3,4,5

The construction used here is MINE, derived before mg-200d's §4.2 was read: take the
poset in which i < j exactly when j >= i+2, so the incomparable pairs are the n-1
CONSECUTIVE pairs; then

    mu = (1/3) d_id + (1/3) d_A + (1/3) d_B,
    A = product of the adjacent transpositions (i,i+1) over EVEN i,
    B = product of the adjacent transpositions (i,i+1) over ODD  i.

A and B are products of disjoint adjacent transpositions, and even/odd is a proper
2-colouring of the path on the n-1 consecutive pairs, so each consecutive pair is
flipped by exactly one of the three atoms: every flip probability is exactly 1/3 and
E[inv] = (n-1)/3.

usage: python3 a5_construction.py
"""
import sys
from fractions import Fraction as F
import liba41b7 as L
from a2_disjunctive import closure, solve_branch


def construction(n):
    """(comparable set C, measure as {arrangement: weight})."""
    C = frozenset((i, j) for i in range(n) for j in range(i + 2, n))
    e = list(range(n))

    def swaps(par):
        s = e[:]
        for i in range(par, n - 1, 2):
            s[i], s[i + 1] = s[i + 1], s[i]
        return tuple(s)

    atoms = {}
    for a in (tuple(e), swaps(0), swaps(1)):
        atoms[a] = atoms.get(a, F(0)) + F(1, 3)
    return C, atoms


print("=" * 78)
print(">= DIRECTION: the (n-1)/3 construction, checked by SUBSTITUTION at n = 3..20")
print("   (no LP is used here, so no solver can be hiding anything)")
print("=" * 78)
bad = 0
for n in range(3, 21):
    C, atoms = construction(n)
    I = [p for p in L.pairs(n) if p not in C]
    rep = L.report_atoms(n, atoms)          # sparse: does NOT enumerate S_n
    target = F(n - 1, 3)
    # every claim the construction has to meet, checked one at a time
    c_mass = rep["mass"] == 1
    c_val = rep["einv"] == target
    c_cap = all(v <= F(1, 3) for v in rep["flips"].values())
    c_comp = all(rep["flips"][p] == 0 for p in C)
    c_sym = all((k[1], k[2]) not in I for k in rep["slot_violations"])
    c_trans = closure(n, C) == C
    c_incs = len(I) == n - 1
    okall = all((c_mass, c_val, c_cap, c_comp, c_sym, c_trans, c_incs))
    if not okall:
        bad += 1
    print("  n=%-3d atoms=%d  E[inv]=%-8s (n-1)/3=%-8s  mass:%s cap:%s comp-q0:%s "
          "per-slot-sym:%s |I|=%d=n-1:%s C-transitive:%s  eps_spec=%s   %s"
          % (n, len(atoms), rep["einv"], target,
             "Y" if c_mass else "N", "Y" if c_cap else "N", "Y" if c_comp else "N",
             "Y" if c_sym else "N", len(I), "Y" if c_incs else "N",
             "Y" if c_trans else "N", L.eps_spec(n, rep["einv"]),
             "OK" if okall else "*** FAILS ***"))
print("  failures: %d / 18" % bad)
sys.stdout.flush()
print("  => the >= direction %s a theorem-shaped construction: it is a 3-atom measure"
      % ("IS backed by" if bad == 0 else "is NOT backed by"))
print("     whose feasibility is checked by substitution at every n tested, so (n-1)/3")
print("     is a LOWER bound on the disjunctive value at every n in 3..20.")

print()
print("=" * 78)
print("NEGATIVE CONTROL: the mod-3 colouring mg-200d recorded as its own defect 1")
print("=" * 78)
for n in (3, 4, 5, 6):
    C = frozenset((i, j) for i in range(n) for j in range(i + 2, n))
    e = list(range(n))

    def swaps3(res):
        s = e[:]
        taken = set()
        for i in range(res, n - 1, 3):
            if i in taken or i + 1 in taken:
                continue
            s[i], s[i + 1] = s[i + 1], s[i]
            taken.add(i); taken.add(i + 1)
        return tuple(s)
    atoms = {}
    for r in (0, 1, 2):
        a = swaps3(r)
        atoms[a] = atoms.get(a, F(0)) + F(1, 3)
    rep = L.report_atoms(n, atoms)
    I = [p for p in L.pairs(n) if p not in C]
    viol = [k for k in rep["slot_violations"] if (k[1], k[2]) in I]
    print("  n=%d  E[inv]=%-6s max flip=%-6s  per-slot violations on incomparable pairs: %d %s"
          % (n, rep["einv"], max(rep["flips"].values()), len(viol),
             "<- breaks symmetry, as mg-200d recorded" if viol else ""))

print()
print("=" * 78)
print("The SOUND BRANCH-FREE surrogate  J_k(y,x) <= J_k(x,y)  -- does it buy anything?")
print("=" * 78)
for n in (3, 4, 5):
    P = L.perms(n)
    rows = [L.row_normalisation(n, P)] + L.rows_pairbias(n, P)
    # one-sided version of the per-slot rows: J_k(y,x) - J_k(x,y) <= 0
    for (c, sense, b) in L.rows_perslot_symmetry(n, P):
        rows.append(({j: -v for j, v in c.items()}, "<=", F(0)))
    obj = L.objective_inv(n, P)
    r = L.solve(len(P), rows, obj)
    base = F(n * (n - 1), 6)
    print("  n=%d  surrogate value = %-8s   baseline C(n,2)/3 = %-8s   %s"
          % (n, r.value if r.status == "optimal" else r.status, base,
             "BUYS NOTHING" if r.status == "optimal" and r.value == base else "CHANGES THE VALUE"))

print()
print("=" * 78)
print("The sound DISJUNCTIVE AGGREGATE value (mg-200d publishes 2/3, 5/3, 7/3)")
print("=" * 78)


def disj_agg(n):
    P_all = L.perms(n)
    prs = L.pairs(n)
    best = None
    for mask in range(1 << len(prs)):
        C = frozenset(prs[i] for i in range(len(prs)) if mask >> i & 1)
        keep = [s for s in P_all if not any(L.pos(s, b) < L.pos(s, a) for (a, b) in C)]
        if not keep:
            continue
        I = [p for p in prs if p not in C]
        rows = [L.row_normalisation(n, keep)]
        for (a, b) in I:
            c = {j: F(1) for j, s in enumerate(keep) if L.pos(s, b) < L.pos(s, a)}
            if c:
                rows.append((c, "<=", F(1, 3)))
        rows.extend(L.rows_aggregate_symmetry(n, keep, pairset=I))
        r = L.solve(len(keep), rows, L.objective_inv(n, keep))
        if r.status == "optimal" and (best is None or r.value > best):
            best = r.value
    return best


pub = {3: F(2, 3), 4: F(5, 3), 5: F(7, 3)}
for n in (3, 4, 5):
    v = disj_agg(n)
    print("  n=%d  disjunctive AGGREGATE = %-8s   mg-200d publishes %-8s   %s"
          % (n, v, pub[n], "MATCH" if v == pub[n] else "DIFFERS  <-- !!"))
    sys.stdout.flush()
