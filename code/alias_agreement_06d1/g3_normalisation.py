"""g3 — THE NORMALISATION FIELD.  The declarations, and the seven ways they are refused.

mg-479c.  mg-06d1's check compares VALUES and goes RED when two names for one quantity
disagree.  It had no representation for two names denoting one quantity IN DIFFERENT
NORMALISATIONS, so a factor of 2 between two live conventions and a genuine 2x error were
the same signal.  `libnorm` holds the field; `g1_values.py` shows the two false directions
separating on real captured columns; THIS arm is about the DECLARATIONS themselves and
costs nothing, because it recomputes no tree.

WHY IT IS A SEPARATE ARM AND NOT PART OF g1.  g1's 30 s is one recompute of twelve trees.
Everything here is a property of two committed JSON files and one committed transcript, so
it runs in milliseconds and — this is the part that matters — it still runs when g1 is RED.
A declaration file that has gone self-contradictory is exactly the thing an author needs to
be told about while the values are also disagreeing, and g1 stops at its own finding by
design (its step 3, mg-e331's D4 read and not repeated).

THE DECLARATIONS ARE PRINTED IN FULL ON EVERY RUN, GREEN AS WELL AS RED.  That is not
verbosity.  P6 of PREDICTIONS-mg-479c.md filed, in advance, that a declared factor is an
unfalsifiable escape hatch: an operator facing a real 2x disagreement can silence it by
declaring a factor of 2, and nothing in this machinery can tell that edit from a correct
one.  Printing every factor on every run puts each such edit into a committed transcript
that mg-f771's control compares against the tree, so the edit is at least LOUD.  It is not
closed and README §7 says so.
"""

import os
import re
import sys
import time
from fractions import Fraction

import libagree as A
import libnorm as NM

HERE = os.path.dirname(os.path.abspath(__file__))
MAP_PATH = os.path.join(os.path.dirname(HERE), "unitmap_audit_9f91", "out_m1_map.txt")

t0 = time.time()
BL = A.load_baseline()
NORM = NM.load()

print("g3  THE NORMALISATION FIELD — mg-479c, per NAME and not per quantity")
print()
print("  semantics   raw = factor(n) * canonical,  so canonical = raw / factor(n)")
print("  factor      a rational function of n in exact integer coefficients; the constant")
print("              is the degree-0 case and {num:[1],den:[1]} is a PASS-THROUGH")
print("  undeclared  REFUSED (exit 2).  Never defaulted to `same`.")

# ------------------------------------------------------------------ N0  the declarations
A.banner("N0  THE DECLARATIONS, PRINTED IN FULL — every factor, on every run, green or red")
print("""
  Every pinned name below, with the convention it declares and the factor that would be
  applied before comparison.  A `1` reads as `1` and not as a blank: the point of the field
  is that silence is no longer a value it can take.""")
print()
for g in BL["groups"]:
    tol, frame = NM.tolerance_for(NORM, g)
    convs = {NORM.convention_of(m) for m in g["members"]}
    print("  %-24s %2d names   tol %.3e (%s frame)   %d convention(s)"
          % (g["label"], len(g["members"]), tol, frame, len(convs)))
    for m in g["members"]:
        e = NORM.entry(m)
        print("      %-52s %-14s x %s"
              % ("%s:%s" % tuple(m),
                 "UNDECLARED" if e is None else e["convention"],
                 "UNDECLARED" if e is None else NM.factor_str(e["factor"])))
print()
print("  illustrative (parsed and validated; NEVER compared — no tree computes these):")
for k in sorted(NORM.illustrative):
    e = NORM.illustrative[k]
    print("      %-52s %-14s x %s" % (k, e["convention"], NM.factor_str(e["factor"])))

# ------------------------------------------------------------------ N1  the live verdict
A.banner("N1  THE LIVE DECLARATIONS — completeness, provenance, and the two agreement rules")
BAD = NM.validate(NORM, BL)
print()
n_pinned = sum(len(g["members"]) for g in BL["groups"])
print("  %d of %d pinned names declared · %d identity · %d convention(s) across %d groups"
      % (sum(1 for g in BL["groups"] for m in g["members"] if NORM.entry(m) is not None),
         n_pinned,
         sum(1 for g in BL["groups"] for m in g["members"]
             if NM.is_identity(NORM.factor_of(m))),
         len({NORM.convention_of(m) for g in BL["groups"] for m in g["members"]}),
         len(BL["groups"])))
print("  seeded_from_measured_spread re-checked against BASELINE.json: %d names"
      % sum(1 for e in NORM.live.values() if "seeded_from_measured_spread" in e))
if BAD:
    for code, where, why in BAD:
        print("  REFUSED  %-22s %s" % (code, where))
        print("             %s" % why)
    print("\n  g3 REFUSES.  This is exit 2 and not exit 1: nothing here is a claim about a "
          "number.")
    sys.exit(A.BROKEN)
print("  0 refusals.")

# ------------------------------------------------------------------ N2  the digest
A.banner("N2  THE DIGEST — over the declarations RESTRICTED TO THE PINNED MEMBERS")
print("""
  Restricted, and the restriction is this ticket's own thesis applied to its own remedy:
  a digest that moved because somebody declared a normalisation for an UNPINNED name would
  put the gate RED for a non-reason, which is the failure mg-479c is about.  Arm D4 plants
  exactly that and requires the digest not to move.

  The digest is a SPEED BUMP AND NOT A CONTROL, and it is worth saying which.  It makes an
  edit to a pinned declaration a two-place edit; anybody willing to update both gets past
  it.  What actually makes such an edit loud is N0 above, printed into a committed
  transcript that code/gate_fixed_point_f771 compares against the tree on every merge.""")
recomputed = NM.digest_of(NORM, BL)
print()
print("  pinned in NORMALISATION.json : %s" % NORM.pinned_digest)
print("  recomputed here              : %s   %s"
      % (recomputed, "match" if recomputed == NORM.pinned_digest else "MISMATCH"))
if recomputed != NORM.pinned_digest:
    print("\n  g3 REFUSES — the pinned declarations were edited without the digest.")
    sys.exit(A.BROKEN)

# ------------------------------------------------------------------ N3  n-dependence
A.banner("N3  THE FACTOR IS A RATIONAL FUNCTION OF n, AND THE CORPUS ALREADY NEEDED ONE")
print("""
  A CONSTANT per-name factor cannot represent one of the three examples the ticket itself
  names.  `code/c3_audit_a94c3/a1_algebra.py:14` states eps_spec = 6 E[inv_e]/(n^2 - 1) and
  eps_c3ca = E[inv_e]/n^2, so eps_spec/eps_c3ca = 6n^2/(n^2 - 1) -> 6.  This arm does not
  take that on the statement's word: it reads the EXACT RATIONALS that
  code/unitmap_audit_9f91/out_m1_map.txt tabulates for both quantities, and checks the
  DECLARED factor against the ratio COLUMN of that table in Fraction arithmetic.  The
  table is CARRIED, not retyped — the rows below are parsed out of the committed
  transcript, so a change to either quantity's definition arrives here as a mismatch.""")
rows = []
with open(MAP_PATH) as fh:
    for line in fh:
        # `      n  eps_c3ca  eps_spec  ratio  ratio-6` — five whitespace-separated fields,
        # the first an integer and the next three exact rationals.
        f = line.split()
        if len(f) != 5 or not f[0].isdigit():
            continue
        try:
            rows.append((int(f[0]), Fraction(f[1]), Fraction(f[2]), Fraction(f[3])))
        except (ValueError, ZeroDivisionError):
            continue
print()
print("  read %d rows from %s"
      % (len(rows), os.path.relpath(MAP_PATH, os.path.dirname(HERE))))
F_SPEC = NORM.illustrative["c3_audit_a94c3:eps_spec"]["factor"]
F_C3CA = NORM.illustrative["unitmap_audit_9f91:eps_c3ca"]["factor"]
print("  declared factor for eps_spec (canonical frame = eps_c3ca): %s"
      % NM.factor_str(F_SPEC))
print()
print("        n   eps_c3ca            eps_spec            tabulated ratio    declared "
      "factor    ratio - 6")
ok_decl = ok_ratio = ok_flat = 0
for n, c3ca, spec, ratio in rows:
    declared = NM.factor_at(F_SPEC, n) / NM.factor_at(F_C3CA, n)
    ok_ratio += (ratio == spec / c3ca)      # the transcript's own column, self-consistent
    ok_decl += (declared == ratio)
    ok_flat += (Fraction(6) == ratio)
    print("  %7d   %-17s   %-17s   %-16s   %-16s   %+.3e"
          % (n, c3ca, spec, ratio, declared, float(ratio - 6)))
print()
print("  the tabulated ratio column equals eps_spec/eps_c3ca at            %2d of %d n"
      % (ok_ratio, len(rows)))
print("  the DECLARED rational function reproduces that ratio at           %2d of %d n"
      % (ok_decl, len(rows)))
print("  a CONSTANT factor of 6 reproduces it at                           %2d of %d n"
      % (ok_flat, len(rows)))
print("""
  A constant field could not have held this, and that was known BEFORE the representation
  was chosen — H2 of PREDICTIONS-mg-479c.md, filed 2026-08-10 and scored as a REPORT at
  zero credit.  The last column is what a flat 6 costs: it is still 6.001e-04 out at
  n = 100 and only reaches 6 in the limit.

  THIS PAIR IS ILLUSTRATIVE.  Neither name is pinned, no lib0d1b adapter produces either,
  and nothing in g1 compares them.  What it demonstrates is that the REPRESENTATION is
  strong enough for the examples the ticket names; it is not a control on the pair.""")
if ok_decl != len(rows) or ok_ratio != len(rows):
    print("\n  g3 REFUSES — the declared factor does not reproduce the committed table.")
    sys.exit(A.BROKEN)

# ------------------------------------------------------------------ N4  planted worlds
A.banner("N4  PLANTED DECLARATION WORLDS — every refusal, falsified")
print("""
  Declarations are mutated in memory on a deep copy, exactly the way mg-06d1's arms mutate
  captured columns.  A planted world that had to be WRITTEN to NORMALISATION.json in order
  to run would be a live declaration about a name nothing computes — E6 of this ticket's
  pre-registration — so none of them is.""")

SB = A.Scoreboard(base_red=False)
FIRST = "%s:%s" % tuple(BL["groups"][0]["members"][0])
SECOND = "%s:%s" % tuple(BL["groups"][0]["members"][1])
LABEL0 = BL["groups"][0]["label"]


def codes(d):
    return sorted({c for c, _w, _y in NM.validate(d, BL)})


def state(d):
    return "REFUSED" if NM.validate(d, BL) else "GREEN"


# D0 — the UNMUTATED declarations, scored FIRST.  mg-9876's guard: a probe already
#      satisfied by the good input is UNFALSIFIABLE and is not a pass.
SB.arm_state("D0 the live declarations, unmutated, must be GREEN (scored first)",
             "GREEN", state(NORM), "0 refusals")

# D1 — the one the ticket is about.  An undeclared normalisation is not "the same".
SB.arm_state("D1 a pinned name's declaration REMOVED — undeclared must REFUSE, never "
             "default to `same`", "REFUSED",
             state(NM.planted(NORM, remove=[FIRST])), "; ".join(codes(
                 NM.planted(NORM, remove=[FIRST]))))

# D2 — one convention cannot carry two factors.
D2 = NM.planted(NORM, live={FIRST: {"convention": NORM.convention_of(FIRST.split(":")),
                                    "factor": {"num": [2], "den": [1]},
                                    "derivation": "PLANTED", "source": "D2"}})
SB.arm_state("D2 factor 2 declared under the SAME convention as its peers — must REFUSE",
             "REFUSED", state(D2), "; ".join(codes(D2)))

# D3 — two names in the same normalisation are in the same convention.
D3 = NM.planted(NORM,
                live={FIRST: dict(NORM.live[FIRST], convention="phantom")},
                conventions={"phantom": {"description": "PLANTED", "source": "D3"}})
SB.arm_state("D3 a DIFFERENT convention declared with the SAME factor — a phantom "
             "convention, must REFUSE", "REFUSED", state(D3), "; ".join(codes(D3)))

# D4 — E9 of the pre-registration, shipped as an arm.  A declaration for an UNPINNED name
#      must not redden anything and must not move the digest.  A gate that went red
#      because somebody declared a name it does not pin would be this ticket's own thesis
#      arriving inside its remedy.
D4 = NM.planted(NORM, live={"some_tree_ffff:some_name": {
    "convention": NM.load().live[FIRST]["convention"],
    "factor": {"num": [3], "den": [1]},
    "derivation": "PLANTED — a name no adapter produces and no group pins.",
    "source": "D4"}})
SB.arm_state("D4 a declaration ADDED for an UNPINNED name — must stay GREEN and must NOT "
             "move the digest (E9: a red for a non-reason, inside the remedy)", "GREEN",
             state(D4) if NM.digest_of(D4, BL) == NORM.pinned_digest else "REFUSED",
             "digest %s, unchanged: %s"
             % (NM.digest_of(D4, BL), NM.digest_of(D4, BL) == NORM.pinned_digest))

# D5 — a factor that is not a factor.
D5 = NM.planted(NORM, live={FIRST: dict(NORM.live[FIRST], factor={"num": [0], "den": [1]})})
SB.arm_state("D5 a factor of ZERO — must REFUSE (a normalisation cannot annihilate its "
             "quantity)", "REFUSED", state(D5), "; ".join(codes(D5)))

# D6 — E1 of the pre-registration, as a live check rather than as a promise.  The identity
#      declarations are SEEDED from mg-0d1b's measured agreement; a seed that no longer
#      matches the record is a derivation that has rotted, and a rotted derivation is the
#      71 hand-written assertions this ticket refused to make.
D6 = NM.planted(NORM, live={FIRST: dict(NORM.live[FIRST],
                                        seeded_from_measured_spread=1.25e-9)})
SB.arm_state("D6 the quoted measured spread edited away from BASELINE.json's — must "
             "REFUSE (E1: the derivation is checked, not decorative)", "REFUSED",
             state(D6), "; ".join(codes(D6)))

# D7 — a convention id that names nothing.
D7 = NM.planted(NORM, live={FIRST: dict(NORM.live[FIRST], convention="not-in-the-map")})
SB.arm_state("D7 a convention id that is not defined in `conventions` — must REFUSE",
             "REFUSED", state(D7), "; ".join(codes(D7)))

# D8 — the tolerance frame, from the declaration side.  E4: silently rescaling the frame
#      the comparison happens in, while keeping the number that governs it, is this
#      ticket's own defect one level up.
D8 = NM.planted(NORM,
                live={FIRST: {"convention": "half", "factor": {"num": [1], "den": [2]},
                              "derivation": "PLANTED", "source": "D8"}},
                conventions={"half": {"description": "PLANTED", "source": "D8"}})
SB.arm_state("D8 a non-identity factor with the group's RAW-frame tolerance left in place "
             "— must REFUSE rather than rescale (E4)", "REFUSED", state(D8),
             "; ".join(codes(D8)))

# D9 — and the other side of the same rule: a canonical tolerance sitting unused is a
#      number nobody checked, waiting to take effect on the next declaration edit.
D9 = NM.planted(NORM, tolerances={LABEL0: {"tolerance": 1.0, "source": "PLANTED"}})
SB.arm_state("D9 a canonical tolerance declared for a group whose members are ALL identity "
             "— unused, must REFUSE", "REFUSED", state(D9), "; ".join(codes(D9)))

UNSAT = SB.print_and_score()

# ------------------------------------------------------------------ N5  decides nothing
A.banner("N5  WHAT THIS TICKET DECIDED, MEASURED: NOTHING")
print("""
  Item 4 of mg-479c: DO NOT RESOLVE ANY EXISTING AMBIGUITY AS PART OF THIS.  Settling
  whether STATE.md's row is in the halved or the doubled form was mg-5e82's business and a
  mathematical question; this ticket builds the machinery to REPRESENT the answer, not to
  decide it.  mg-5e82 has since settled that row — STATE.md now reads `mu_pref^2/2 IN THIS
  ROW'S OWN NORMALISATION (settled mg-5e82...)` and names mg-479c as carrying the general
  hazard — so there is nothing left here to decide even by accident.  It is measured
  anyway, because "proves an absence" is the shape of claim this arc keeps getting wrong
  and a measured absence is at least checkable.""")
nonident = [m for g in BL["groups"] for m in g["members"]
            if not NM.is_identity(NORM.factor_of(m))]
multi = [g["label"] for g in BL["groups"]
         if len({NORM.convention_of(m) for m in g["members"]}) > 1]
# THE GAP'S OWN LANGUAGE, and not the word `mu_pref`.  Six of the twelve pinned groups are
# ABOUT mu_pref and their seeded derivations quote the group label, so a match on the bare
# name would report nine hits that mean nothing — a red for a non-reason, in the arm whose
# subject is reds for non-reasons.  What is forbidden here is the CLAUSE: the squared form,
# the two route names, and the halved/doubled wording.
FORBIDDEN = ("(L*)", "(M#)", "(M♯)", "mu_pref^2", "mu_pref²", "μ_pref²",
             "2*mu*Delta", "2 mu Delta", "doubled form", "halved form", "mg-5e82")

def gap_language(decls):
    """Which declarations use the (L*)/(M#) clause's language.  Returns [(key, word)].

    THIS IS A `needle in haystack` TEST AND mg-9876's a4 SWEEP COUNTS IT AS A CANDIDATE.
    Its hazard is a probe that is satisfied for a reason unrelated to what it claims to
    measure, so it is ADJUDICATED here rather than left in the census: it is run BOTH WAYS
    on every run — against the live declarations, where it must find nothing, and against a
    planted declaration that does carry the clause, where it must find it.  A detector that
    has only ever returned zero is not distinguishable from one that cannot return anything
    else, which is the whole of mg-9876.
    """
    found = []
    for key, e in sorted(decls.items()):
        blob = "%s %s %s" % (e.get("convention", ""), e.get("derivation", ""),
                             e.get("source", ""))
        for w in FORBIDDEN:
            if w in blob:
                found.append((key, w))
    return found


hits = gap_language(NORM.live)
PLANT_KEY = "planted_tree:planted_name"
planted_hits = gap_language(dict(
    NORM.live, **{PLANT_KEY: {"convention": "planted",
                              "derivation": "the gap between (L*) and (M#) is mu_pref^2",
                              "source": "N5's negative control"}}))
print()
print("  pinned names carrying a NON-IDENTITY factor          : %d of %d"
      % (len(nonident), n_pinned))
print("  pinned groups carrying MORE THAN ONE convention      : %d of %d%s"
      % (len(multi), len(BL["groups"]), "   %s" % multi if multi else ""))
print("  live declarations using the (L*)/(M#) gap's language : %d%s"
      % (len(hits), "   %s" % hits if hits else ""))
print("  canonical tolerances declared                        : %d"
      % len(NORM.canonical_tolerances))
print("  ...and the same detector on a PLANTED declaration    : %d hit(s)  %s"
      % (len(planted_hits), [h for h in planted_hits if h[0] == PLANT_KEY]))
if not [h for h in planted_hits if h[0] == PLANT_KEY]:
    print("\n  g3 REFUSES — the gap-language detector did not fire on a declaration that "
          "carries\n  the clause verbatim, so the 0 above is a statement about the "
          "detector and not\n  about the declarations.")
    sys.exit(A.BROKEN)
print("""
  WHAT THIS DOES NOT ESTABLISH.  It measures that the DECLARATIONS are silent about the
  (L*)/(M#) gap.  It says nothing about the rest of the branch — that STATE.md is untouched
  is a property of the diff, not of this file, and the reader who wants it should read the
  diff.""")

# ------------------------------------------------------------------ result
A.banner("g3 RESULT")
print("  %d declarations valid; %d falsification arms unsatisfactory." % (n_pinned, UNSAT))
print("  total %.2fs" % (time.time() - t0))
sys.exit(A.BROKEN if UNSAT else A.GREEN)
