"""g1 — THE AGREEMENT CHECK.  12 quantities, 71 names, 12 trees, compared for the first time.

mg-0d1b measured that these agree.  Nothing has ever ASKED again.  This is the arm that
asks, on every merge, and goes RED naming both aliases when two names for one quantity
disagree beyond the tolerance mg-0d1b measured.

STRUCTURE, AND WHY IT IS THIS ORDER
-----------------------------------
  1. capture the 80 columns once (the whole cost of this suite — see README §1)
  2. score the UNMUTATED input, IN THE CANONICAL FRAME (mg-479c)
  3. IF IT IS RED, print the finding and stop.  Do not run the planted worlds.
     IF IT REFUSED, print what could not be compared and stop, with exit 2 and not 1.
  4. otherwise plant eight worlds in the CAPTURED MATRIX and check each (G1c)
  5. then six more in COPIES OF THE DECLARATION TABLE, on the same matrix (G1d, mg-479c)

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

import copy
import math
import re
import sys
import time
from fractions import Fraction

import libagree as A
import libnorm as N

L = A.L
t0 = time.time()

BL = A.load_baseline()
POP_ALL = L.population(L.POP_SPEC)
POP_PRIM = [(n, dn) for (n, dn) in POP_ALL if L.primitive_here(dn, n)]
NS = [n for (n, _dn) in POP_PRIM]

# mg-479c — the declarations the comparison happens through.  Loaded BEFORE the 30 s
# capture, because a file that cannot be parsed should cost 0.2 s to find out about and not
# half a minute, and because a gate that captures first and refuses second has spent the
# whole cost of the run to say it could not run.
try:
    DECLS = N.load()
except N.NormError as exc:
    print("g1  REFUSED before capture — %s" % exc)
    sys.exit(A.BROKEN)

# The declarations the comparison runs through must be the ones the baseline was cut
# against, or the twelve tolerances are stated in a frame nobody pinned.  The digest is over
# the declarations RESTRICTED TO THE PINNED MEMBERS — see mkbaseline.py — so declaring a
# normalisation for a name this gate does not pin does NOT redden it.
_want = BL.get("normalisation_digest")
_have = DECLS.digest_over([tuple(m) for g in BL["groups"] for m in g["members"]])
if _want != _have:
    print("g1  REFUSED before capture — NORMALISATION.json's declarations for the 71 pinned "
          "names hash to %s; BASELINE.json was cut against %s.  The frame the comparison "
          "happens in has moved and the twelve tolerances are no longer stated in it.  "
          "Re-cut the baseline in the same commit as the declaration, with a reason."
          % (_have, _want))
    sys.exit(A.BROKEN)

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
A.banner("G1b  THE COMPARISON — pinned membership, mg-0d1b's tolerances, canonical frame")
print()
VERDICTS, BASE_RED, REFUSALS = A.check_groups(COLS, BROKEN_TREES, BL,
                                              decls=DECLS, ns=NS)
A.report(VERDICTS)

if REFUSALS:
    A.banner("g1 RESULT — REFUSED.  THE COMPARISON WAS NOT MADE.")
    print("""
  %d group(s) could not be compared.  This is NOT a disagreement and must not be filed as
  one: the gate is saying it does not know what frame two names are in, which is a
  different fact from two numbers differing.  mg-479c, item 3: an undeclared normalisation
  is REFUSED, never defaulted to `same`, because defaulting is the FALSE PASS direction of
  that ticket with the volume turned all the way down.
""" % len(REFUSALS))
    for kindname, label, detail in REFUSALS:
        print("  %-26s %s" % (kindname, label))
        print("      %s" % detail)
    print()
    print("  (%d groups checked, %.1fs)" % (len(VERDICTS), time.time() - t0))
    sys.exit(A.BROKEN)

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


def check(cols, broken=None, tol_override=None, decls=None, normalise=True):
    _v, red, ref = A.check_groups(cols, broken or {}, BL, tol_override=tol_override,
                                  decls=decls or DECLS, ns=NS, normalise=normalise)
    return red, _v, ref


def outcome(cols, **kw):
    """GREEN / RED / REFUSAL — the three-valued verdict mg-479c's arms are scored against."""
    red, _v, ref = check(cols, **kw)
    return ("REFUSAL" if ref else ("RED" if red else "GREEN")), _v, ref


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
red, vs, _r = check(A.mut_add_at(COLS, KEY1, IDX1, ulp))
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
red, vs, _r = check(A.mut_add_at(COLS, KEY2, IDX2, 2 * TOL_G))
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
    red, _vs, _r = check(A.mut_add_at(COLS, KEY2, best_idx, eps3))
    SB.arm("W3 sub-tolerance (%.3e < %.3e) on the same column must stay GREEN"
           % (eps3, TOL_G), False, red)

# ---- W4  THE DRIFT-OUT, and the reason membership is pinned.  A column moved a whole
#          unit away from its group is the failure this ticket exists for.  The same
#          mutated matrix is then handed to mg-0d1b's OWN value-blind clustering rule,
#          which is what a gate built by re-running x3 would have used.
MUT4 = A.mut_add_all(COLS, KEY2, 1.0)
red, vs, _r = check(MUT4)
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
red, vs, _r = check(A.mut_drop(COLS, KEY2))
kinds = {p[0] for grp in vs for p in grp["problems"]}
SB.arm("W5 the name %s:%s stops being produced" % KEY2, True, red,
       "reported as %s" % ", ".join(sorted(kinds)))

# ---- W6  COMPARABILITY.  One value becomes uncomputable.  `spread()` SKIPS it, so on an
#          exact group the DISAGREE test cannot fire — only the pinned comparable count
#          can.  The arm therefore checks that COMPARABILITY is the reason, not merely
#          that something went red.
red, vs, _r = check(A.mut_blank_at(COLS, KEY1, IDX1))
kinds = {p[0] for grp in vs for p in grp["problems"]}
SB.arm("W6 %s:%s becomes uncomputable at one poset (exact group)" % KEY1, True, red,
       "reported as %s%s" % (", ".join(sorted(kinds)),
                             "" if kinds == {"COMPARABILITY"} else
                             "  <-- expected COMPARABILITY alone"))

# ---- W7  TREE-BROKEN.  A tree that no longer loads removes itself from every agreement
#          it was party to.  That is the same loss of a control as a numeric drift.
red, vs, _r = check(A.mut_drop(COLS, KEY2), broken={KEY2[0]: "planted: module failed to load"})
kinds = {p[0] for grp in vs for p in grp["problems"]}
SB.arm("W7 the tree %s fails to load" % KEY2[0], True, red,
       "reported as %s" % ", ".join(sorted(kinds)))

# ---- W8  THE DECORATIVE TOLERANCE, demonstrated.  W2's mutation is re-checked against a
#          plausible round number somebody might have typed instead of carrying the
#          record.  It passes.  This is the ticket's step 2 as a measurement rather than
#          as a warning: "a check with a tolerance looser than the observed agreement is
#          decorative", and here is the exact input it fails to see.
red, _vs, _r = check(A.mut_add_at(COLS, KEY2, IDX2, 2 * TOL_G), tol_override=1e-6)
SB.arm("W8 the SAME mutation as W2, checked at a typed 1e-6 instead of the carried "
       "%.3e, must go GREEN — the decorative tolerance, demonstrated" % TOL_G,
       False, red,
       "a gate written from the ticket's own rounded quote would be this one")

UNSAT = SB.print_and_score()

# ------------------------------------------------------------------ 4. mg-479c
#
# THE NORMALISATION ARMS.  mg-06d1's check could not tell a normalisation from a
# disagreement, and the two failures are the same missing bit read from opposite ends: a
# FALSE RED on two conventions that agree modulo a factor, and a FALSE PASS on a genuine 2x
# error dismissable as "just a normalisation difference".  N3 and N4 plant one each, on the
# same captured matrix and the same real columns, so they cost milliseconds and no
# re-capture.  Every mutation below is DERIVED from a value a tree produced — a column
# DOUBLED, not a literal — per the same rule the W arms follow.
A.banner("G1d  mg-479c — THE NORMALISATION ARMS.  Six worlds, and the identity measured")
print("""
  The twelve pinned groups contain NO normalisation pair today: all 71 names are declared in
  the identity normalisation and this ticket is inert on them, which is the ticket's own
  `WHY NOT HIGH`.  So the machinery is falsified here against declarations planted in copies
  of the real declaration table, in both directions — a factor that is REAL and must not go
  red, and a factor that is ABSENT where the values differ and must.""")

SBN = A.Scoreboard(base_red=bool(BASE_RED))


def with_decl(key, convention, num=(1,), den=(1,), canon_tol=None):
    """A copy of the live declarations with ONE name re-declared.  Never a hand-built table.

    Copying the real table and moving one entry keeps every other declaration exactly as
    committed, so an arm that fires is firing on the change and not on a fixture.

    `canon_tol` is the SECOND HALF of registering a normalisation, and it is separate here
    because the two halves have to be planted separately — see D2 in README §7.  A group
    that gains a non-identity factor is no longer governed by mg-0d1b's raw-frame tolerance,
    so a registrant declares BOTH the factor and a canonical-frame tolerance.  N6 plants the
    first half alone (and must REFUSE); N3 plants both (and must go GREEN).
    """
    d = copy.copy(DECLS)
    d.decls = dict(DECLS.decls)
    d.tolerances = dict(DECLS.tolerances)
    if convention is None:
        del d.decls[key]
    else:
        d.decls[key] = {"convention": convention,
                        "factor": N.Factor(list(num), list(den)),
                        "source": "PLANTED by g1 arm — not committed"}
    if canon_tol is not None:
        label, tol = canon_tol
        d.tolerances[label] = {"tolerance": tol,
                               "source": "PLANTED by g1 arm — not committed"}
    return d


def scale_col(cols, key, mult):
    """Multiply a whole column by an exact rational.  The mutation the ticket is about."""
    c = A.clone(cols)
    c[key] = [None if v is None else float(v * mult) for v in c[key]]
    return c


# ---- N1  THE IDENTITY IS A PASS-THROUGH, MEASURED ON ALL 71 COLUMNS.  `v * 1.0 == v` for
#          every finite float, so a multiply would be harmless today — and would make seven
#          exact-equality rows depend on that staying true of whatever a tree returns next.
#          Filed in advance as E3, and this is the measurement rather than the argument.
PINNED = [tuple(m) for g in BL["groups"] for m in g["members"]]
CAN, APPLIED = N.canonicalise(COLS, PINNED, DECLS, NS)
same_obj = sum(1 for m in PINNED if CAN[m] is COLS[m])
same_bits = sum(1 for m in PINNED
                if all((x is y) or (x == y and repr(x) == repr(y))
                       for x, y in zip(CAN[m], COLS[m])))
SBN.arm_outcome("N1 identity canonicalisation is a PASS-THROUGH on all %d pinned columns"
                % len(PINNED),
                "GREEN", "GREEN" if (same_obj == len(PINNED)) else "RED",
                "%d of %d columns returned as the SAME LIST OBJECT, %d of %d bit-identical; "
                "%d group(s) in a non-identity frame"
                % (same_obj, len(PINNED), same_bits, len(PINNED),
                   sum(1 for v in VERDICTS if v.get("frame") == "CANONICAL")))

# ---- N2  THE WRONG-WAY PATH IS THE SHIPPED PATH.  `normalise=False` is the pre-479c
#          comparison; N3's demonstration is worth nothing unless the two agree on the real
#          input.  Measured, not argued (filed in advance as E7).  `x1_wrongway.py` runs the
#          BLOB-PINNED pre-479c libagree.py itself, off the gate.
raw_v, raw_red, raw_ref = A.check_groups(COLS, BROKEN_TREES, BL, normalise=False)
same_verdict = (raw_red == BASE_RED and not raw_ref and
                all(rv["spread"] == cv["spread"] and
                    len(rv["problems"]) == len(cv["problems"])
                    for rv, cv in zip(raw_v, VERDICTS)))
SBN.arm_outcome("N2 the pre-479c raw comparison and the canonical one agree on the REAL "
                "input", "GREEN", "GREEN" if same_verdict else "RED",
                "%d/%d spreads identical, both %d red, %d refusals — so N3's wrong-way "
                "demonstration is of the shipped behaviour and not of a strawman"
                % (sum(1 for rv, cv in zip(raw_v, VERDICTS)
                       if rv["spread"] == cv["spread"]), len(VERDICTS),
                   raw_red, len(raw_ref)))

# ---- N3  THE FALSE RED, AND THE WHOLE POINT.  A column DOUBLED and DECLARED doubled is two
#          live conventions of one quantity.  It must go GREEN under mg-479c — and the same
#          input through the pre-479c path is shown RED beside it, which is the measurement
#          that this ticket changed something.
KEYN = ("chain_iv_c_81ff", "lambda2_bracket")
DOUBLED = scale_col(COLS, KEYN, Fraction(2))
G_GAMMA = group_by_label("gamma")
D_OK = with_decl("%s:%s" % KEYN, "gamma (doubled convention, PLANTED)", (1,), (2,),
                 canon_tol=("gamma", G_GAMMA["tolerance"]))
got, vs_ok, ref_ok = outcome(DOUBLED, decls=D_OK)
_wv, wrong_red, _wref = A.check_groups(DOUBLED, BROKEN_TREES, BL, normalise=False)
can_spread = [v["spread"] for v in vs_ok if v["label"] == "gamma"][0]
SBN.arm_outcome("N3 %s:%s DOUBLED, DECLARED x1/2 and given a canonical-frame tolerance — "
                "two live conventions, must be GREEN" % KEYN, "GREEN", got,
                "THE FALSE RED THE TICKET IS ABOUT: the SAME input through the pre-479c raw "
                "comparison is RED at %d group(s), spread 1.000e+00 against a tolerance of "
                "4.666e-10; after normalising the spread is %s, back at the group's measured "
                "agreement.  On a gate that blocks merges, a red for a non-reason is how "
                "gates get disabled."
                % (wrong_red, "n/a" if can_spread is None else "%.3e" % can_spread))

# ---- N4  THE FALSE PASS, AND IT IS THE HALF AN OPERATOR CANNOT SEE.  The same doubled
#          column, this time declared in the SAME convention as everything else — i.e. a
#          genuine 2x error.  It must go RED, and the message must SAY the two names share a
#          convention, because that sentence is the difference between "file a ticket" and
#          "oh, that's just units".
got, vs_bad, _rb = outcome(DOUBLED)
disagrees = [p for grp in vs_bad for p in grp["problems"] if p[0] == "DISAGREE"]
said_same = any("SAME CONVENTION" in p[2] for p in disagrees)
said_ratio = any(re.search(r"= (EXACTLY )?(2/1|1/2)\b", p[2]) for p in disagrees)
SBN.arm_outcome("N4 the SAME doubled column with NO factor declared — a genuine 2x error, "
                "must be RED", "RED", got,
                "message names the ratio as a simple rational (2/1 or 1/2): %s;  says the two "
                "names are in the SAME declared convention: %s  <-- the sentence that tells an "
                "operator this is a defect and not units" % (said_ratio, said_same))

# ---- N5  THE UNDECLARED NAME.  Ticket item 3: refuse, do not default to `same`.  And the
#          outcome must be REFUSAL and not RED — an instrument declining to answer is a
#          different fact from a control firing, and this suite's exit convention (2 vs 1)
#          already separates them.  A two-valued arm cannot express that, which is why
#          `Scoreboard.arm_outcome` exists.
got, _v5, ref5 = outcome(COLS, decls=with_decl("%s:%s" % KEYN, None))
SBN.arm_outcome("N5 %s:%s loses its declaration — must REFUSE, not default to `same`" % KEYN,
                "REFUSAL", got,
                "reported as %s" % (", ".join(sorted({r[0] for r in ref5})) or "nothing"))

# ---- N6  THE TOLERANCE FRAME.  A group that gains a non-identity member is being checked
#          against a number mg-0d1b measured in the RAW frame.  It is not rescalable —
#          members with different factors admit no single multiplier — so the gate must
#          REFUSE rather than compare in one frame against a tolerance stated in another.
#          Filed in advance as E4; this is this ticket's own defect one level up, planted.
got, _v6, ref6 = outcome(COLS, decls=with_decl("%s:%s" % KEYN,
                                               "gamma (doubled convention, PLANTED)",
                                               (1,), (2,)))
SBN.arm_outcome("N6 a non-identity factor against mg-0d1b's RAW-frame tolerance — must "
                "REFUSE", "REFUSAL", got,
                "reported as %s" % (", ".join(sorted({r[0] for r in ref6})) or "nothing"))

UNSAT += SBN.print_and_score()

# ------------------------------------------------------------------ result
A.banner("g1 RESULT")
print("  %d groups agree at mg-0d1b's measured tolerances; %d falsification arms "
      "unsatisfactory." % (len(VERDICTS), UNSAT))
print("  recompute %.1fs · falsification %.2fs · total %.1fs"
      % (t_cap, time.time() - t0 - t_cap, time.time() - t0))
sys.exit(A.BROKEN if UNSAT else A.GREEN)
