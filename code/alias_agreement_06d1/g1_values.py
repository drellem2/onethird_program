"""g1 — THE AGREEMENT CHECK.  12 quantities, 71 names, 12 trees, compared for the first time.

mg-0d1b measured that these agree.  Nothing has ever ASKED again.  This is the arm that
asks, on every merge, and goes RED naming both aliases when two names for one quantity
disagree beyond the tolerance mg-0d1b measured.

STRUCTURE, AND WHY IT IS THIS ORDER
-----------------------------------
  1. capture the 80 columns once (the whole cost of this suite — see README §1)
  2. score the UNMUTATED input
  3. IF IT IS RED, print the finding and stop.  Do not run the planted worlds.
  4. otherwise plant eight worlds in the CAPTURED MATRIX and check each

Step 3 is not an optimisation, it is mg-e331's defect D4 read and not repeated.  That
ticket composed two individually correct rules — "a probe satisfied by the good input is
UNFALSIFIABLE" and "any UNFALSIFIABLE makes the verdict BROKEN" — into a ratchet that
became structurally incapable of reporting its own finding: the instant the real input
went over the line, every probe was satisfied by it, the verdict flipped to BROKEN, and
the remedy text could never print.  It was not fail-open, which is exactly why it would
have survived.  Here, a real disagreement is a RED with a finding, and the planted worlds
are reported NOT RUN rather than laundered into UNFALSIFIABLE.

WHY THE WORLDS ARE PLANTED IN THE MATRIX AND NOT IN THE TREES
-------------------------------------------------------------
Recomputing 12 trees costs 30 s; eight worlds recomputed would cost four minutes on every
merge.  The columns are captured once and the mutations are applied to COPIES of that
captured data, so the whole falsification suite costs milliseconds.  Every mutation is
DERIVED from a value a tree actually produced — one ULP, a multiple of the pinned
tolerance — rather than typed as a literal known-bad, per mg-9876's rule: a hand-typed
fixture is one the instrument was built around.
"""

import math
import sys
import time

import libagree as A

L = A.L
t0 = time.time()

BL = A.load_baseline()
POP_ALL = L.population(L.POP_SPEC)
POP_PRIM = [(n, dn) for (n, dn) in POP_ALL if L.primitive_here(dn, n)]

print("g1  THE AGREEMENT CHECK — mg-0d1b's 12 measured groups, compared")
print()
print("  population POP-PRIM   %d posets of %d   (tolerances are stated over this set)"
      % (len(POP_PRIM), len(POP_ALL)))
print("  pinned      %d groups   %d names   %d trees"
      % (len(BL["groups"]),
         sum(len(g["members"]) for g in BL["groups"]),
         len({m[0] for g in BL["groups"] for m in g["members"]})))

if len(POP_PRIM) != BL["derived_from"]["alias_groups.json"]["POP_PRIM"]:
    print("\n  REFUSED — the population moved (%d now, %d when the tolerances were "
          "measured).  Every tolerance below is stated over the recorded population and "
          "none of them means anything over a different one." % (
              len(POP_PRIM), BL["derived_from"]["alias_groups.json"]["POP_PRIM"]))
    sys.exit(A.BROKEN)

# ------------------------------------------------------------------ 1. capture
A.banner("G1a  RECOMPUTE — every scalar by the tree that owns it, through its own entry point")
t_cap = time.time()
COLS, KIND, BROKEN_TREES = A.capture(POP_PRIM)
t_cap = time.time() - t_cap
print()
print("  %d columns from %d trees in %.1fs%s"
      % (len(COLS), len(L.ADAPTERS) - len(BROKEN_TREES), t_cap,
         "   %d TREE(S) FAILED TO RUN" % len(BROKEN_TREES) if BROKEN_TREES else ""))
for tree, why in sorted(BROKEN_TREES.items()):
    print("      BROKEN  %-28s %s" % (tree, why))

bad_spread = A.selfcheck_spread(COLS, BL["groups"])
print("  spread self-check against lib0d1b.spread on every pinned pair: %d mismatches"
      % bad_spread)
if bad_spread:
    print("\n  REFUSED — this file's pairwise walk and lib0d1b's `spread()` disagree, so "
          "the number being compared is not the number the tolerance was measured with.")
    sys.exit(A.BROKEN)

# ------------------------------------------------------------------ 2. the unmutated verdict
A.banner("G1b  THE COMPARISON — pinned membership, mg-0d1b's tolerances, unmodified")
print()
VERDICTS, BASE_RED = A.check_groups(COLS, BROKEN_TREES, BL)
A.report(VERDICTS)

# A READING, NOT A GATE.  Seven of the twelve tolerances are 0.000e+00, so those rows are
# exact-equality checks and the suite's usefulness rests on this recompute being
# bit-reproducible.  It is therefore MEASURED on every run rather than assumed: how many
# groups reproduce the baseline's observed spread to the last bit.  A group that drifts
# below its tolerance is not RED — a tolerance is a ceiling, and reddening on any change
# at all would be the instrument arm W3 exists to rule out — but a falling count here is
# the early warning that this host's arithmetic is not the host the baseline was cut on.
exact = sum(1 for v, g in zip(VERDICTS, BL["groups"])
            if v["spread"] == g["observed_at_baseline"])
print()
print("  bit-reproducibility: %d of %d groups reproduce the baseline's observed spread "
      "exactly (%d of them are exact-equality rows)"
      % (exact, len(VERDICTS), sum(1 for g in BL["groups"] if g["tolerance"] == 0.0)))

if BASE_RED:
    A.banner("g1 RESULT — RED.  A DISAGREEMENT IS A FINDING.")
    print("""
  %d of %d groups above are RED.  Two or more names for ONE quantity now disagree, or a
  name that was party to an agreement has stopped being computed.

  WHAT TO DO — and what NOT to do.

    DO   file a ticket naming BOTH aliases and both trees, quoting the poset index and
         the two values printed above.  One of them is wrong; this check does not know
         which, and deliberately offers no way to say.

    DO NOT resolve it by picking the more recent tree, and DO NOT widen the tolerance in
         BASELINE.json.  The tolerances there are mg-0d1b's MEASURED agreement, carried
         and not invented; a tolerance edited to admit an observation is the observation
         deleted.  There is no --refresh mode in this suite for that reason.

  THE PLANTED WORLDS ARE NOT RUN.  They falsify a check against a GOOD input, and this
  input is not good.  Reporting them here as UNFALSIFIABLE — and letting that make the
  verdict BROKEN — is mg-e331's defect D4, in which a merge failed telling its author the
  instrument was broken rather than telling them what it had found.
""" % (BASE_RED, len(VERDICTS)))
    print("  (%d groups checked, %.1fs)" % (len(VERDICTS), time.time() - t0))
    sys.exit(A.RED)

# ------------------------------------------------------------------ 3. planted worlds
A.banner("G1c  POSITIVE CONTROL — eight planted worlds, and the good input scored first")
print("""
  THIS ROW OF THE CORPUS HAS ONLY EVER SEEN AGREEMENT.  mg-0d1b found 0 disagreements in
  12 groups, which is the condition mg-9876 was filed about: a control that has never
  fired is indistinguishable from one that cannot.  So the check is falsified here, on
  every run, against mutations derived from the columns the trees just produced.""")

SB = A.Scoreboard(base_red=bool(BASE_RED))


def check(cols, broken=None, tol_override=None):
    _v, red = A.check_groups(cols, broken or {}, BL, tol_override=tol_override)
    return red, _v


def group_by_label(label):
    for g in BL["groups"]:
        if g["label"] == label:
            return g
    raise SystemExit("g1: no pinned group labelled %r" % label)


# ---- W1  one ULP on an EXACT group.  The tightest statement available: `leak(A_1)` is
#          pinned at tolerance 0.000e+00, so the smallest change float arithmetic can
#          represent must be RED.  A tolerance that had been rounded up "for safety"
#          anywhere would fail this arm.
g_leak = group_by_label("leak(A_1)")
KEY1 = tuple(g_leak["members"][0])
IDX1 = A.first_comparable(COLS, KEY1)
v = COLS[KEY1][IDX1]
ulp = math.nextafter(v, math.inf) - v
red, vs = check(A.mut_add_at(COLS, KEY1, IDX1, ulp))
named = [p for grp in vs for p in grp["problems"] if p[0] == "DISAGREE"]
SB.arm("W1 one ULP (%.3e) on %s:%s, exact group `leak(A_1)`" % (ulp, KEY1[0], KEY1[1]),
       True, red,
       "names %s:%s vs %s:%s" % (named[0][1][0][0], named[0][1][0][1],
                                 named[0][1][1][0], named[0][1][1][1]) if named else
       "RED but not as a DISAGREE — the arm fired for the wrong reason")

# ---- W2  TWICE the pinned tolerance on the tightest non-exact group.  Derived from the
#          record, not typed: this is the arm that says the gamma row's 4.666e-10 is a
#          real threshold at the right order of magnitude.
g_gam = group_by_label("gamma")
TOL_G = g_gam["tolerance"]
KEY2 = ("chain_iv_c_81ff", "lambda2_bracket")
IDX2 = A.first_comparable(COLS, KEY2)
red, vs = check(A.mut_add_at(COLS, KEY2, IDX2, 2 * TOL_G))
named = [p for grp in vs for p in grp["problems"] if p[0] == "DISAGREE"]
SB.arm("W2 2x tolerance (%.3e) on %s:%s, group `gamma`" % (2 * TOL_G, KEY2[0], KEY2[1]),
       True, red,
       "names %s:%s vs %s:%s" % (named[0][1][0][0], named[0][1][0][1],
                                 named[0][1][1][0], named[0][1][1][1]) if named else "")

# ---- W3  BELOW the tolerance — and it must NOT go red.  Without this arm W2 could be
#          passing because the check reddens on any change at all, which is a different
#          and useless instrument.  The epsilon is computed from the headroom the data
#          actually has at the quietest poset, so the arm refuses rather than lying if
#          there is no headroom.
members_g = [tuple(m) for m in g_gam["members"]]
best_idx, best_slack = None, -1.0
for i in range(len(POP_PRIM)):
    d = 0.0
    for m in members_g:
        if m == KEY2:
            continue
        x, y = COLS[KEY2][i], COLS[m][i]
        if A.finite(x) and A.finite(y):
            d = max(d, abs(x - y))
    if TOL_G - d > best_slack:
        best_idx, best_slack = i, TOL_G - d
if best_slack <= 0:
    SB.arm("W3 sub-tolerance perturbation must stay GREEN", False, False,
           "NO HEADROOM at any poset — arm could not be planted, reported not asserted")
else:
    eps3 = best_slack / 2.0
    red, _vs = check(A.mut_add_at(COLS, KEY2, best_idx, eps3))
    SB.arm("W3 sub-tolerance (%.3e < %.3e) on the same column must stay GREEN"
           % (eps3, TOL_G), False, red)

# ---- W4  THE DRIFT-OUT, and the reason membership is pinned.  A column moved a whole
#          unit away from its group is the failure this ticket exists for.  The same
#          mutated matrix is then handed to mg-0d1b's OWN value-blind clustering rule,
#          which is what a gate built by re-running x3 would have used.
MUT4 = A.mut_add_all(COLS, KEY2, 1.0)
red, vs = check(MUT4)
clusters = L.cluster(MUT4, 1e-6)
gam_cluster = [c for c in clusters if ("lstar_789d", "gamma_float") in c]
n_after = len(gam_cluster[0]) if gam_cluster else 0
drifted_alone = any(c == [KEY2] for c in clusters)
SB.arm("W4 column DRIFTS OUT of `gamma` entirely (+1.0 at every poset)", True, red,
       "value-blind clustering on the SAME input: gamma cluster %d -> %d names, drifted "
       "column alone in its own cluster: %s, NO error raised — that rule exits 0 here"
       % (len(members_g), n_after, drifted_alone))

# ---- W5  MEMBERSHIP-LOST.  The name stops being produced.  Under a value-blind rule
#          this is simply a smaller group and is not an error at all.
red, vs = check(A.mut_drop(COLS, KEY2))
kinds = {p[0] for grp in vs for p in grp["problems"]}
SB.arm("W5 the name %s:%s stops being produced" % KEY2, True, red,
       "reported as %s" % ", ".join(sorted(kinds)))

# ---- W6  COMPARABILITY.  One value becomes uncomputable.  `spread()` SKIPS it, so on an
#          exact group the DISAGREE test cannot fire — only the pinned comparable count
#          can.  The arm therefore checks that COMPARABILITY is the reason, not merely
#          that something went red.
red, vs = check(A.mut_blank_at(COLS, KEY1, IDX1))
kinds = {p[0] for grp in vs for p in grp["problems"]}
SB.arm("W6 %s:%s becomes uncomputable at one poset (exact group)" % KEY1, True, red,
       "reported as %s%s" % (", ".join(sorted(kinds)),
                             "" if kinds == {"COMPARABILITY"} else
                             "  <-- expected COMPARABILITY alone"))

# ---- W7  TREE-BROKEN.  A tree that no longer loads removes itself from every agreement
#          it was party to.  That is the same loss of a control as a numeric drift.
red, vs = check(A.mut_drop(COLS, KEY2), broken={KEY2[0]: "planted: module failed to load"})
kinds = {p[0] for grp in vs for p in grp["problems"]}
SB.arm("W7 the tree %s fails to load" % KEY2[0], True, red,
       "reported as %s" % ", ".join(sorted(kinds)))

# ---- W8  THE DECORATIVE TOLERANCE, demonstrated.  W2's mutation is re-checked against a
#          plausible round number somebody might have typed instead of carrying the
#          record.  It passes.  This is the ticket's step 2 as a measurement rather than
#          as a warning: "a check with a tolerance looser than the observed agreement is
#          decorative", and here is the exact input it fails to see.
red, _vs = check(A.mut_add_at(COLS, KEY2, IDX2, 2 * TOL_G), tol_override=1e-6)
SB.arm("W8 the SAME mutation as W2, checked at a typed 1e-6 instead of the carried "
       "%.3e, must go GREEN — the decorative tolerance, demonstrated" % TOL_G,
       False, red,
       "a gate written from the ticket's own rounded quote would be this one")

UNSAT = SB.print_and_score()

# ------------------------------------------------------------------ result
A.banner("g1 RESULT")
print("  %d groups agree at mg-0d1b's measured tolerances; %d falsification arms "
      "unsatisfactory." % (len(VERDICTS), UNSAT))
print("  recompute %.1fs · falsification %.2fs · total %.1fs"
      % (t_cap, time.time() - t0 - t_cap, time.time() - t0))
sys.exit(A.BROKEN if UNSAT else A.GREEN)
