"""mg-00a1 -- controls for `lib00a1`.  EXITS 1 ON ANY FAILURE.

Five of the nine groups are MUTATIONS: they break the witness on purpose and require the
verifier to notice.  A verifier that cannot fail is not a verifier, and the whole verdict of
`s1` rests on `verify_measure` actually checking what it says it checks.

Usage:  python3 selftest00a1.py
"""

import sys
from fractions import Fraction as F
from itertools import combinations, permutations

import lib00a1 as L
from lp200d import Infeasible, flips, relaxation

FAILS = []


def check(group, name, cond, detail=""):
    status = "ok  " if cond else "FAIL"
    if not cond:
        FAILS.append(f"{group}/{name}")
    print(f"  [{status}] {group}: {name}{('   ' + detail) if detail else ''}")


def main():
    print("=" * 92)
    print("mg-00a1 selftest -- 9 control groups, 5 of them mutations")
    print("=" * 92)
    print()

    # ---------------------------------------------------------------- 1
    print("GROUP 1 -- column generation agrees with brute force over all n!")
    for n in (3, 4, 5, 6):
        allp = list(permutations(range(n)))
        for I in (L.consecutive(n), L.staircase_I(n), L.band(n, 2), frozenset()):
            C = L.comparable_from_I(n, I)
            brute = sorted(p for p in allp if not (flips(p) & C))
            mine = sorted(L.linear_extensions(n, C))
            check("G1", f"n={n} |I|={len(I)}", brute == mine,
                  f"{len(mine)} columns")
    print()

    # ---------------------------------------------------------------- 2
    print("GROUP 2 -- transitive closure on hand cases")
    check("G2", "consecutive branch's C is already closed",
          L.is_transitively_closed(4, L.comparable_from_I(4, L.consecutive(4))))
    check("G2", "{(0,1),(1,2)} closes to include (0,2)",
          L.transitive_closure(3, frozenset({(0, 1), (1, 2)}))
          == frozenset({(0, 1), (1, 2), (0, 2)}))
    check("G2", "staircase branch is transitively closed at n=6,8,10",
          all(L.is_transitively_closed(n, L.comparable_from_I(n, L.staircase_I(n)))
              for n in (6, 8, 10)))
    print()

    # ---------------------------------------------------------------- 3
    print("GROUP 3 -- my exact LP agrees with mg-200d's relaxation() on a branch sweep")
    agree = tot = 0
    for n in (4, 5):
        allp = L.pairs_of(n)
        rs = range(len(allp) + 1) if n == 4 else range(0, 4)
        for r in rs:
            for sub in combinations(allp, r):
                I = frozenset(sub)
                tot += 1
                try:
                    a = L.branch_value_exact(n, I)[0]
                except Infeasible:
                    a = None
                try:
                    b = relaxation(n, "slot_eq", comparable=L.comparable_from_I(n, I))[0]
                except Infeasible:
                    b = None
                if a == b:
                    agree += 1
    check("G3", "exact values agree", agree == tot, f"{agree}/{tot} branches")
    print()

    # ---------------------------------------------------------------- 4
    print("GROUP 4 -- the witness is feasible and hits its closed form (n = 4..14)")
    for n in range(4, 15):
        v = L.verify_measure(n, L.witness(n), L.staircase_I(n))
        check("G4", f"n={n}", v["ok"] and v["E_inv"] == L.witness_target(n),
              f"E[inv]={v['E_inv']} target={L.witness_target(n)}")
    print()

    # ---------------------------------------------------------------- 5  MUTATION
    print("GROUP 5 -- MUTATION: perturb one cascade weight -> symmetry must break")
    n = 10
    mu = dict(L.witness(n))
    key = L._cascade(n // 2, 2)
    mu[key] = mu[key] + F(1, 1000)
    v = L.verify_measure(n, mu, L.staircase_I(n))
    check("G5", "mass no longer 1", v["mass"] != 1)
    check("G5", "verifier reports NOT ok", not v["ok"])
    mu2 = dict(L.witness(n))
    mu2[L._cascade(n // 2, 2)] += F(1, 1000)
    mu2[L._cascade(n // 2, 3)] -= F(1, 1000)          # mass-preserving perturbation
    v2 = L.verify_measure(n, mu2, L.staircase_I(n))
    check("G5", "mass-preserving perturbation still caught (symmetry)",
          v2["mass"] == 1 and bool(v2["sym_violations_on_I"]) and not v2["ok"],
          f"{len(v2['sym_violations_on_I'])} slot violations")
    print()

    # ---------------------------------------------------------------- 6  MUTATION
    print("GROUP 6 -- MUTATION: wrong Markov parameter in the fence -> symmetry must break")
    for m, bad_p in ((5, F(1, 2)), (6, F(1, 3)), (6, F(1, 10))):
        n = 2 * m
        good = F(1, m - 1)
        if bad_p == good:
            continue
        mu = {}
        w = F(1, 3 * (m - 1))
        for t in range(1, m):
            k = L._cascade(m, t)
            mu[k] = mu.get(k, F(0)) + w
        from itertools import product
        for bits in product((0, 1), repeat=m):
            pr = F(1, 2)
            for k2 in range(1, m):
                pr *= bad_p if bits[k2] == bits[k2 - 1] else 1 - bad_p
            k = L._fence(m, frozenset(i for i in range(m) if bits[i]))
            mu[k] = mu.get(k, F(0)) + F(2, 3) * pr
        v = L.verify_measure(n, mu, L.staircase_I(n))
        check("G6", f"n={n} p={bad_p} (correct is {good})",
              v["mass"] == 1 and not v["ok"],
              f"{len(v['sym_violations_on_I'])} slot violations")
    print()

    # ---------------------------------------------------------------- 7  MUTATION
    print("GROUP 7 -- MUTATION: an atom flipping a COMPARABLE pair must be caught")
    n = 8
    mu = dict(L.witness(n))
    intruder = (1, 0, 2, 3, 4, 5, 7, 6)
    bad = (7, 6, 5, 4, 3, 2, 1, 0)                     # reversal: flips everything
    mu[bad] = F(1, 100)
    v = L.verify_measure(n, mu, L.staircase_I(n))
    check("G7", "comparable pairs reported flipped", bool(v["comparable_pairs_flipped"]),
          f"{len(v['comparable_pairs_flipped'])} pairs")
    check("G7", "verifier reports NOT ok", not v["ok"])
    check("G7", "control: the reversal really is outside the branch",
          bool(flips(bad) & L.comparable_from_I(n, L.staircase_I(n))))
    check("G7", "control: a legal atom is NOT reported",
          not (flips(intruder) & L.comparable_from_I(n, L.staircase_I(n))))
    print()

    # ---------------------------------------------------------------- 8  MUTATION
    print("GROUP 8 -- MUTATION: push a flip over the cap -> max_flip must exceed 1/3")
    n = 10
    m = n // 2
    mu = dict(L.witness(n))
    mu[L._fence(m, frozenset({0}))] += F(1, 20)
    mu[L._fence(m, frozenset())] -= F(1, 20)
    v = L.verify_measure(n, mu, L.staircase_I(n))
    check("G8", "max_flip now exceeds 1/3", v["max_flip"] > F(1, 3), str(v["max_flip"]))
    check("G8", "verifier reports NOT ok", not v["ok"])
    print()

    # ---------------------------------------------------------------- 9  MUTATION
    print("GROUP 9 -- MUTATION: a negative atom must be caught, and the trivial dual bounds")
    n = 8
    mu = dict(L.witness(n))
    k = L._cascade(4, 1)
    mu[k] = -mu[k]
    v = L.verify_measure(n, mu, L.staircase_I(n))
    check("G9", "negative atom reported", bool(v["negative_atoms"]))
    check("G9", "verifier reports NOT ok", not v["ok"])
    for n in (6, 8, 10):
        td, _ = L.trivial_dual_bound(n, L.staircase_I(n))
        val = L.branch_value_exact(n, L.staircase_I(n))[0]
        check("G9", f"trivial dual >= value at n={n}", td >= val, f"{td} >= {val}")
    print()

    print("=" * 92)
    if FAILS:
        print(f"FAILURES ({len(FAILS)}): " + ", ".join(FAILS))
        return 1
    print("ALL CONTROL GROUPS PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
