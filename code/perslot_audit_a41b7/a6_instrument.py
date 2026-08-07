"""a6_instrument — a DIFFERENTIAL AUDIT of mg-200d's reporting code.

pm-onethird's re-pointing (mail 2026-08-07 21:02): mg-200d's CONCLUSIONS are already
refuted downstream, but its INSTRUMENT is load-bearing, because mg-131e and mg-00a1
both ran their own witnesses through `lp200d.measure_report`.  If that reporting code
is wrong, it is wrong under two LIVE results.

So this script does not check mg-200d's answers.  It checks its MEASURING DEVICE, by
running it side by side with mine -- written from the definitions, not from its source
-- on measures chosen to hit the places a reporting bug would hide:

  * the two-atom law, the uniform measure, single atoms
  * measures on the disjunctive optimal branches (where downstream witnesses live)
  * SUB-PROBABILITY measures (mass != 1) -- mg-6bc2's original defect, and the one
    class where a reporting function can be silently wrong
  * measures with an ASYMMETRY planted at one known (slot, pair), so the violation
    lists have a known right answer rather than merely agreeing with each other

Agreement between two implementations of the same wrong idea proves nothing, so every
comparison below is also checked against a HAND-COMPUTED expected value where one
exists, and three mutations are fed in that both implementations must REJECT.
"""
import sys
from fractions import Fraction as F
import liba41b7 as L

sys.path.insert(0, "../perslot_symmetry_200d")
import lp200d as T   # noqa: E402   -- AUDIT TARGET

ok = 0
bad = []


def check(name, cond, detail=""):
    global ok
    if cond:
        ok += 1
    else:
        bad.append((name, detail))
    print("  %s  %s%s" % ("PASS" if cond else "FAIL", name,
                          "" if cond else "   %s" % detail))


def mine(n, atoms):
    return L.report(n, L.measure_from_atoms(n, atoms))


def compare(n, atoms, label):
    """Run both reporters on the same measure and compare every shared field."""
    m = mine(n, atoms)
    t = T.measure_report(n, dict(atoms))
    check("%s: mass agrees (%s)" % (label, m["mass"]), m["mass"] == t["mass"],
          "mine %s theirs %s" % (m["mass"], t["mass"]))
    check("%s: E[inv] agrees (%s)" % (label, m["einv"]), m["einv"] == t["E_inv"],
          "mine %s theirs %s" % (m["einv"], t["E_inv"]))
    if m["flips"]:
        check("%s: max flip agrees (%s)" % (label, max(m["flips"].values())),
              max(m["flips"].values()) == t["max_flip"],
              "mine %s theirs %s" % (max(m["flips"].values()), t["max_flip"]))
    mine_slot = set((p, k) for (k, a, b) in m["slot_violations"] for p in [(a, b)])
    theirs_slot = set(tuple(v) for v in t["slot_eq_violations"])
    check("%s: per-slot violation SET agrees (%d)" % (label, len(mine_slot)),
          mine_slot == theirs_slot,
          "mine\\theirs %s   theirs\\mine %s"
          % (sorted(mine_slot - theirs_slot)[:3], sorted(theirs_slot - mine_slot)[:3]))
    mine_agg = set(m["agg_violations"].keys())
    theirs_agg = set(tuple(v) for v in t["agg_eq_violations"])
    check("%s: aggregate violation SET agrees (%d)" % (label, len(mine_agg)),
          mine_agg == theirs_agg,
          "mine\\theirs %s   theirs\\mine %s"
          % (sorted(mine_agg - theirs_agg)[:3], sorted(theirs_agg - mine_agg)[:3]))
    return m, t


print("=" * 78)
print("A. both reporters on measures with a HAND-COMPUTED right answer")
print("=" * 78)
for n in (3, 4, 5, 6):
    e = tuple(range(n))
    rev = tuple(reversed(e))
    m, t = compare(n, {e: F(2, 3), rev: F(1, 3)}, "n=%d two-atom law" % n)
    check("n=%d two-atom E[inv] is C(n,2)/3 BY HAND" % n, t["E_inv"] == F(n * (n - 1), 6),
          str(t["E_inv"]))
    # hand answer for the two-atom law's per-slot violations:
    #   at slot k the only adjacent pairs present are (e_k,e_{k+1}) from e with mass 2/3
    #   and (e_{n-k-1}, e_{n-k-2}) from rev with mass 1/3.  They coincide as an unordered
    #   pair only when n-k-2 == k, i.e. n even and k = (n-2)/2, and then 2/3 != 1/3 so it
    #   is still a violation.  So EVERY slot k contributes exactly one violated pair for
    #   the e-adjacency, plus one for the rev-adjacency when they differ:
    expected = (n - 1) + (n - 1) - (1 if (n % 2 == 0) else 0)
    check("n=%d two-atom per-slot violation COUNT is the hand value %d" % (n, expected),
          len(t["slot_eq_violations"]) == expected,
          "hand %d, theirs %d" % (expected, len(t["slot_eq_violations"])))

for n in (3, 4, 5):
    P = L.perms(n)
    u = {s: F(1, len(P)) for s in P}
    m, t = compare(n, u, "n=%d uniform" % n)
    check("n=%d uniform has NO per-slot violation (hand: swap x,y is a bijection)" % n,
          t["slot_eq_violations"] == [], str(t["slot_eq_violations"][:3]))
    check("n=%d uniform E[inv] = C(n,2)/2 BY HAND" % n, t["E_inv"] == F(n * (n - 1), 4),
          str(t["E_inv"]))

print()
print("=" * 78)
print("B. SUB-PROBABILITY measures -- the class where mg-6bc2's diagnostics went wrong")
print("=" * 78)
for n in (3, 4):
    e = tuple(range(n))
    rev = tuple(reversed(e))
    # mass 2/3, exactly the shape of mg-6bc2's published n=3 support
    m, t = compare(n, {e: F(1, 3), rev: F(1, 3)}, "n=%d SUB-probability mass 2/3" % n)
    check("n=%d sub-probability mass is reported as 2/3, not silently 1" % n,
          t["mass"] == F(2, 3), str(t["mass"]))
    # and completing it must CHANGE the violation set, which is the substance of §8.1
    m2, t2 = compare(n, {e: F(2, 3), rev: F(1, 3)}, "n=%d completed to mass 1" % n)
    check("n=%d completing the measure CHANGES the aggregate violation set" % n,
          set(map(tuple, t["agg_eq_violations"])) != set(map(tuple, t2["agg_eq_violations"]))
          or len(t["agg_eq_violations"]) != len(t2["agg_eq_violations"]),
          "before %s after %s" % (t["agg_eq_violations"], t2["agg_eq_violations"]))

print()
print("=" * 78)
print("C. PLANTED asymmetry -- the violation list has a known right answer")
print("=" * 78)
# n=4: mass on 0123 and 1023 only.  Pair (0,1) at slot 0: J_0(0,1)=w1, J_0(1,0)=w2.
for (w1, w2, want) in ((F(1, 2), F(1, 2), False), (F(2, 3), F(1, 3), True)):
    atoms = {(0, 1, 2, 3): w1, (1, 0, 2, 3): w2}
    t = T.measure_report(4, atoms)
    m = mine(4, atoms)
    has = ((0, 1), 0) in set(map(tuple, t["slot_eq_violations"]))
    hasm = (0, 0, 1) in m["slot_violations"]
    check("planted (0,1)@slot0 with %s/%s: theirs reports violation=%s (want %s)"
          % (w1, w2, has, want), has == want)
    check("planted (0,1)@slot0 with %s/%s: mine agrees" % (w1, w2), hasm == has)

print()
print("=" * 78)
print("D. MUTATIONS both implementations must reject (the comparison must not be vacuous)")
print("=" * 78)
n = 4
e = tuple(range(n))
rev = tuple(reversed(e))
atoms = {e: F(2, 3), rev: F(1, 3)}
t = T.measure_report(n, atoms)
check("M1 E[inv] is NOT C(n,2)/2 (would mean flips read as 1/2)", t["E_inv"] != F(n * (n - 1), 4))
check("M2 max_flip is NOT 1/2", t["max_flip"] != F(1, 2))
check("M3 per-slot violations are NOT empty for the two-atom law",
      t["slot_eq_violations"] != [])
# The 'le' surrogate is claimed sound for uniform L(P) with e a linear extension, so it
# must HOLD there and must FAIL somewhere, or the predicate is not measuring anything.
#
#   DEFECT OF MINE, KEPT: M4 first asserted slot_le for the TWO-ATOM LAW and FAILED
#   against correct code.  It should: 3210 puts (1,0) at slot 2 with mass 1/3 while
#   J_2(0,1) = 0, so J_k(y,x) <= J_k(x,y) is violated.  The two-atom law is not a
#   uniform L(P) measure and the surrogate never claimed to cover it -- my control was
#   asserting mg-200d's conclusion about an object outside its hypothesis, which is the
#   same shape of error this arc keeps recording.  Re-pointed at the right population.
t_rev = T.measure_report(n, {e: F(1, 3), rev: F(2, 3)})
lp = T.uniform_le_measure(4, {(0, 2), (0, 3), (1, 3)})   # the n=4 optimal branch's poset
t_lp = T.measure_report(4, lp)
check("M4 slot_le HOLDS for uniform L(P), which is the population it is claimed on",
      t_lp["slot_le_violations"] == [], str(t_lp["slot_le_violations"][:3]))
check("M5 slot_le FAILS for the rev-heavy measure (predicate is not vacuous)",
      t_rev["slot_le_violations"] != [])
check("M6 slot_le also fails for the two-atom law -- so it is NOT a property of M_n",
      t["slot_le_violations"] != [])

print()
print("=" * 78)
print("E. eps_spec -- exactness of the conversion the downstream results quote")
print("=" * 78)
for (lbl, arg) in (("Fraction(10,3)", F(10, 3)), ("Fraction(1,1)", F(1, 1)),
                   ("python int 1", 1), ("python int 2", 2)):
    v = T.eps_spec(5, arg)
    check("eps_spec(5, %s) returns an exact rational, not a float" % lbl,
          not isinstance(v, float), "returned %r of type %s" % (v, type(v).__name__))
    mv = L.eps_spec(5, arg)
    check("eps_spec(5, %s) agrees with mine (%s)" % (lbl, mv), F(v) == mv,
          "theirs %r mine %s" % (v, mv))

# Does the float path ever BITE?  Only if some caller hands eps_spec a non-Fraction.
# measure_report accumulates E_inv from F(0), so it is a Fraction on every input --
# including integer weights and the empty measure.  Checked, not assumed:
kinds = set()
for atoms in ({}, {(0, 1, 2): 1, (2, 1, 0): 2}, {(0, 1, 2): F(1, 2), (2, 1, 0): F(1, 2)},
              {(0, 1, 2): 0}):
    kinds.add(type(T.measure_report(3, dict(atoms))["E_inv"]).__name__)
check("measure_report's E_inv is ALWAYS a Fraction, so live eps_spec calls stay exact",
      kinds == {"Fraction"}, "types seen: %s" % sorted(kinds))

print()
print("=" * 78)
print("F. the branch witnesses downstream work actually reports on")
print("=" * 78)
from a2_disjunctive import solve_branch   # noqa: E402
for n in (3, 4, 5):
    P_all = L.perms(n)
    prs = L.pairs(n)
    best = None
    for mask in range(1 << len(prs)):
        C = frozenset(prs[i] for i in range(len(prs)) if mask >> i & 1)
        out = solve_branch(n, C, P_all)
        if out is None or out[0].status != "optimal":
            continue
        if best is None or out[0].value > best[0].value:
            best = (out[0], out[1], C)
    r, keep, C = best
    atoms = {keep[j]: v for j, v in r.x.items()}
    compare(n, atoms, "n=%d disjunctive optimal witness" % n)
    t = T.measure_report(n, atoms)
    I = [p for p in prs if p not in C]
    onI = [v for v in t["slot_eq_violations"] if tuple(v[0]) in I]
    check("n=%d its reporter sees 0 per-slot violations on the INCOMPARABLE pairs" % n,
          onI == [], str(onI[:3]))
    check("n=%d its reporter's E_inv equals my LP optimum %s" % (n, r.value),
          t["E_inv"] == r.value, "theirs %s mine %s" % (t["E_inv"], r.value))
    sys.stdout.flush()

print()
print("PASS %d   FAIL %d" % (ok, len(bad)))
for nm, d in bad:
    print("   FAILED: %s  %s" % (nm, d))
sys.exit(1 if bad else 0)
