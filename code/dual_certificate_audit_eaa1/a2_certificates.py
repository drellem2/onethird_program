"""mg-eaa1 A2 -- AUDIT CHECK 1: verify the `<=` direction at n = 3,4,5 BY SUBSTITUTION.

My brief: "A certificate is checkable in a way an LP run is not - so check it, do not re-run
the LP."  There is a wrinkle mg-131e's deliverable creates and this script has to deal with
honestly: **mg-131e does not commit its tier-2 multiplier vectors to disk.**  `d1` regenerates
them from `budgeted_dual` at run time and prints only counts.  So "verify mg-131e's
certificate by substitution" is not literally available for the 1 / 18 / 388 tier-2 branches;
what IS available, and is strictly stronger as an audit, is to build MY OWN certificate for
every branch on MY OWN rows and verify THAT by substitution.  If my family discharges every
branch at the same bound, mg-131e's claim is confirmed by an object it never saw.

So, per branch `C` at n = 3,4,5:

  A2.1  TIER 0, THE n-INDEXED ONE, AS A THEOREM.  `lam = 0, t = 1 on every cap row, s = 0`.
        Verified by substitution, and additionally checked to hold with EQUALITY on every
        column -- which is the whole reason it is a theorem rather than a computation, and
        the reason its bound is exactly |I_active|/3.
  A2.2  EVERY BRANCH DISCHARGED AT <= (n-1)/3, by tier 0 where that suffices and by a dual I
        find myself where it does not.  Every vector, however found, is then re-checked by
        `verify_dual`, which shares no code with the finder.
  A2.3  THE PRIMAL CLASS OF EACH BRANCH, on my own simplex, so vacuous certificates (bounds
        on a maximum over the empty set) are separated from informative ones.  mg-131e
        reports the informative-hard sequence as 0, 0, 2; this reproduces it or does not.
  A2.4  STRONG DUALITY on every feasible branch: my primal optimum == my dual optimum.
  A2.5  THE TWO INFORMATIVE HARD BRANCHES AT n = 5, PRINTED IN FULL as multiplier vectors --
        the data mg-131e's transcripts do not carry.
  A2.6  MUTATION CONTROL: shave and sign-flip a multiplier and require the verifier to reject.
        Without this an "all pass" line is consistent with a verifier that passes anything.
"""

import sys
import time
from fractions import Fraction as F

import lib_eaa1 as L

NS = [int(a) for a in sys.argv[1:]] or [3, 4]

fails = []


def ok(cond, msg, quiet_ok=False):
    if not cond:
        print(f"  [FAIL] {msg}")
        fails.append(msg)
    elif not quiet_ok:
        print(f"  [OK ] {msg}")
    return cond


print("=" * 90)
print("A2  THE `<=` DIRECTION AT n = 3,4,5, RE-CERTIFIED FROM SCRATCH ON MY OWN ROWS")
print("=" * 90)

for n in NS:
    t0 = time.time()
    target = F(n - 1, 3)
    print(f"\n### n = {n}   target (n-1)/3 = {target}   branches 2^C(n,2) = "
          f"{2 ** len(L.all_pairs(n))}")

    stats = {"empty": 0, "infeasible": 0, "zero": 0, "positive": 0}
    tier = {0: 0, "mine": 0, "none": 0}
    tier_by_class = {}
    max_bound = None
    informative_hard = []
    attaining = []
    sd_checked = sd_fail = 0
    eq_on_every_column = True

    for C in L.all_branches(n):
        perms, rows, c, labels = L.program(n, C)
        if not perms:
            stats["empty"] += 1
            continue

        # ---- A2.1 tier 0, verified AND checked for equality on every column
        y0 = L.trivial_dual(rows, labels)
        cert0 = L.verify_dual(rows, c, y0)
        if not cert0.ok:
            ok(False, f"n={n} C={sorted(C)}: TRIVIAL DUAL IS NOT FEASIBLE -- {cert0!r}")
        acc = [F(0)] * len(c)
        for i, (co, _, _) in enumerate(rows):
            if y0[i]:
                for j, v in co.items():
                    acc[j] += y0[i] * v
        if any(acc[j] != c[j] for j in range(len(c))):
            eq_on_every_column = False
            ok(False, f"n={n} C={sorted(C)}: trivial dual does NOT hold with equality "
                      f"on every column")
        act = L.active_pairs(n, C)
        if cert0.bound != F(len(act), 3):
            ok(False, f"n={n} C={sorted(C)}: trivial bound {cert0.bound} != |I_active|/3 = "
                      f"{F(len(act), 3)}")

        # ---- A2.3 primal class, my own simplex
        kind, val, mu = L.classify_branch(n, C)
        stats[kind] += 1

        # ---- A2.2 discharge the branch at <= target
        if cert0.bound <= target:
            which, bound, y = 0, cert0.bound, y0
        else:
            y = L.find_dual(rows, c, target)
            if y is None:
                which, bound = "none", None
                ok(False, f"n={n} C={sorted(C)}: NO dual with bound <= {target} exists")
            else:
                cert = L.verify_dual(rows, c, y)
                if not cert.ok:
                    ok(False, f"n={n} C={sorted(C)}: my own dual FAILS substitution -- "
                              f"{cert!r}")
                    which, bound = "none", None
                else:
                    which, bound = "mine", cert.bound
                    if bound > target:
                        ok(False, f"n={n} C={sorted(C)}: bound {bound} exceeds {target}")
        tier[which] = tier.get(which, 0) + 1
        tier_by_class[(kind, which)] = tier_by_class.get((kind, which), 0) + 1
        if bound is not None and (max_bound is None or bound > max_bound):
            max_bound = bound
        if which == "mine" and kind in ("positive", "zero"):
            informative_hard.append((sorted(C), kind, val, cert0.bound, y, rows, c, labels))

        # ---- A2.4 strong duality where the branch is feasible
        if kind in ("positive", "zero"):
            dv, ystar = L.dual_min(rows, c)
            sd_checked += 1
            if dv != val:
                sd_fail += 1
                ok(False, f"n={n} C={sorted(C)}: strong duality FAILS, primal {val} "
                          f"vs dual {dv}")
            cstar = L.verify_dual(rows, c, ystar)
            if not (cstar.ok and cstar.bound == val):
                sd_fail += 1
                ok(False, f"n={n} C={sorted(C)}: dual optimum fails substitution {cstar!r}")
            if val == target:
                attaining.append((sorted(C), len(L.all_pairs(n)) - len(C), len(act),
                                  cert0.bound, which))

    print(f"  primal classes                  : empty={stats['empty']}, "
          f"infeasible={stats['infeasible']}, zero={stats['zero']}, "
          f"positive={stats['positive']}")
    print(f"  certificate needed              : tier0(trivial, n-indexed)={tier[0]}  "
          f"mine(solver-found, then substituted)={tier['mine']}  none={tier['none']}")
    print(f"  tier x primal class             : "
          f"{ {k: v for k, v in sorted(tier_by_class.items(), key=repr)} }")
    print(f"  strong duality                  : {sd_checked} feasible branches, "
          f"{sd_fail} failures")
    ok(eq_on_every_column,
       f"n={n}: the trivial dual holds with EQUALITY on every column of every branch "
       f"-- so it is a theorem, not a computation")
    ok(tier["none"] == 0 and max_bound is not None and max_bound <= target,
       f"n={n}: EVERY branch discharged at <= {target}   (max certified bound over "
       f"branches = {max_bound})")
    print(f"  INFORMATIVE hard branches (feasible AND needing more than tier 0): "
          f"{len(informative_hard)}")
    for Cs, kind, val, tb, y, rows, c, labels in informative_hard:
        print(f"      C={Cs}  {kind}  val={val}  trivial bound={tb}")
    print(f"  branches attaining {target}: {len(attaining)}")
    for Cs, nI, nact, tb, which in attaining:
        print(f"      C={Cs}  |I|={nI} active={nact}  trivial bound={tb}  tier={which}")
    print(f"  [{time.time() - t0:.1f}s]")

    # ---- A2.5 the informative certificates PRINTED IN FULL
    if informative_hard:
        print()
        print(f"  --- n={n}: THE INFORMATIVE CERTIFICATES, AS DATA "
              f"(mg-131e's transcripts print counts, not vectors) ---")
        for Cs, kind, val, tb, y, rows, c, labels in informative_hard:
            print(f"  C = {Cs}   val = {val}   my certificate bound = "
                  f"{L.verify_dual(rows, c, y).bound}")
            for i, lab in enumerate(labels):
                if y[i]:
                    name = ("lam" if lab[0] == "sum" else
                            f"t{lab[1]}" if lab[0] == "cap" else f"s{lab[1]},k={lab[2]}")
                    print(f"        {name:<22} = {y[i]}")

print()
print("=" * 90)
print("A2.6  MUTATION CONTROL -- the verifier must REJECT a broken certificate.")
print("      Without this, 'all pass' is consistent with a verifier that passes anything.")
print("=" * 90)
n = max(NS)
C = {3: frozenset({(0, 2)}), 4: frozenset({(0, 2), (0, 3), (1, 3)}),
     5: frozenset({(0, 2), (0, 3), (1, 4), (2, 4)})}[n]
perms, rows, c, labels = L.program(n, C)
y0 = L.trivial_dual(rows, labels)
ok(L.verify_dual(rows, c, y0).ok, f"n={n}: unmutated trivial dual verifies (positive control)")
cap_i = next(i for i, lab in enumerate(labels) if lab[0] == "cap")
shaved = list(y0)
shaved[cap_i] = F(9, 10)
ok(not L.verify_dual(rows, c, shaved).ok,
   f"n={n}: SHAVED cap multiplier (1 -> 9/10) is REJECTED")
flipped = list(y0)
flipped[cap_i] = F(-1)
mf = L.verify_dual(rows, c, flipped)
ok(not mf.ok and mf.sign_bad,
   f"n={n}: SIGN-FLIPPED cap multiplier (1 -> -1) is REJECTED on the SIGN condition")
sym_i = next((i for i, lab in enumerate(labels) if lab[0] == "sym"), None)
if sym_i is not None:
    free_neg = list(y0)
    free_neg[sym_i] = F(-7)
    fc = L.verify_dual(rows, c, free_neg)
    ok(not fc.sign_bad,
       f"n={n}: a NEGATIVE multiplier on a free (==) row is NOT a sign violation "
       f"-- the verifier is not rejecting by blanket nonnegativity")
short = list(y0)[:-1]
try:
    L.verify_dual(rows, c, short)
    ok(False, f"n={n}: a wrong-length multiplier vector was accepted")
except ValueError:
    ok(True, f"n={n}: a wrong-length multiplier vector raises rather than silently padding")

print()
print("=" * 90)
print(f"A2 RESULT: {'ALL CHECKS PASS' if not fails else str(len(fails)) + ' FAILURES'}")
for f in fails:
    print("   FAILED:", f)
print("=" * 90)
sys.exit(1 if fails else 0)
