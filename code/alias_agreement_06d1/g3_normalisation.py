"""g3 — THE NORMALISATION FIELD ITSELF.  The declarations, the representation, and item 4.

mg-479c gives the alias index a normalisation field PER NAME.  g1 is where the field is
USED — the comparison happens in the canonical frame and the RED message reports the factor
applied.  This arm is where the field is CHECKED, and it runs first for the same reason g2
runs before g1: it costs 0.2 s against g1's 30 s and it is a VALIDITY precondition.  If the
declarations are self-contradictory, or a pinned name has none, then every one of g1's
twelve `agree` lines is a comparison in a frame nobody can name.

WHAT IS HERE
------------
  G3a  THE INVENTORY, printed on every run — green as well as red.  A declared factor is
       the one thing in this gate an operator can use to silence a real disagreement
       (README §7), and a factor that only becomes visible when something breaks is
       invisible.  So all 71 are counted and every non-identity one is named, always.
  G3b  THE REPRESENTATION, unit-tested.  Exact `Fraction` arithmetic, a float coefficient
       REFUSED, a vanishing denominator REFUSED, and `is_identity` reading the rational
       FUNCTION and not its value at the n this population happens to contain.
  G3c  THE WORKED EXAMPLE, re-derived and not asserted.  `eps_spec`/`eps_c3ca` is one of
       the ticket's own three examples and its factor is `6n^2/(n^2-1)` — n-DEPENDENT.  It
       is checked against mg-9f91's committed table of exact rationals at every n in it,
       and the same table's "what a flat factor of 6 gets wrong at small n" is re-derived
       here because it is the corpus's own evidence that a per-name CONSTANT factor would
       have been the wrong representation.
  G3d  SIX PLANTED WORLDS, including the one that scores ticket item 4: this ticket
       registers NOTHING about the (L*)/(M#) `mu_pref^2` gap, and N7 goes RED if that ever
       stops being true.

WHAT IS NOT HERE
----------------
No mathematics, and no verdict on any ambiguity.  Ticket item 4: "DO NOT RESOLVE ANY
EXISTING AMBIGUITY AS PART OF THIS."  The eps pair is not ambiguous — mg-c3ca states the
identity and mg-9f91 tabulates it — so carrying it decides nothing.  STATE.md:172's
`mu_pref^2` IS ambiguous, is mg-5e82's, and is left exactly where it is.
"""

import json
import os
import re
import sys
from fractions import Fraction

import libagree as A
import libnorm as N

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.dirname(HERE)
MAP_PATH = os.path.join(CODE, "unitmap_audit_9f91", "out_m1_map.txt")
CITE_PATH = os.path.join(CODE, "c3_audit_a94c3", "a1_algebra.py")
CITE_TEXT = "eps_spec / eps_c3ca = 6 n^2 / (n^2 - 1)"

BL = A.load_baseline()
PINNED = [tuple(m) for g in BL["groups"] for m in g["members"]]
GROUPS = [(g["label"], ["%s:%s" % tuple(m) for m in g["members"]]) for g in BL["groups"]]

print("g3  THE NORMALISATION FIELD — mg-479c")
print()

try:
    DECLS = N.load()
except N.NormError as exc:
    print("  REFUSED — %s" % exc)
    sys.exit(A.BROKEN)

PROBLEMS = []


def fail(msg):
    PROBLEMS.append(msg)
    print("  PROBLEM  %s" % msg)


# ------------------------------------------------------------------ G3a  the inventory
A.banner("G3a  THE INVENTORY — every declaration, and every non-identity factor, always")
print()
print("  %d declarations   %d pinned names   %d worked-example names"
      % (len(DECLS.decls), len(PINNED),
         sum(len(b["names"]) for b in DECLS.examples.values())))

undeclared = [m for m in PINNED if not DECLS.has(m)]
if undeclared:
    fail("%d pinned name(s) with NO declared normalisation: %s"
         % (len(undeclared), ", ".join("%s:%s" % m for m in undeclared)))

try:
    N.check_consistency(DECLS.decls, GROUPS)
    print("  convention <-> factor consistency over %d groups: OK" % len(GROUPS))
except N.NormError as exc:
    fail(str(exc))

print()
print("  %-24s %-6s %-11s %s" % ("group", "names", "frame", "conventions / factors"))
for (label, keys), g in zip(GROUPS, BL["groups"]):
    members = [tuple(k.split(":", 1)) for k in keys]
    try:
        frame, why = N.tolerance_frame(members, DECLS)
    except N.NormError as exc:
        fail(str(exc))
        continue
    convs = sorted({DECLS.convention_for(m) for m in members})
    non_id = [(m, DECLS.factor_for(m)) for m in members
              if not DECLS.factor_for(m).is_identity()]
    desc = ("%d convention, identity throughout" % len(convs)) if not non_id else \
        "%d conventions; " % len(convs) + ", ".join("%s:%s x%s" % (m[0], m[1], f.as_text())
                                                    for m, f in non_id)
    print("  %-24s %-6d %-11s %s" % (label, len(members), frame, desc))
    if frame == "CANONICAL" and DECLS.canonical_tolerance(label) is None:
        fail("%s is in a CANONICAL frame with no canonical-frame tolerance recorded" % label)

want = BL.get("normalisation_digest")
have = DECLS.digest_over(PINNED)
print()
print("  pinned-restricted declaration digest: %s   baseline recorded: %s   %s"
      % (have, want, "MATCH" if have == want else "MOVED"))
if have != want:
    fail("the declarations for the pinned names have moved since BASELINE.json was cut")

# ------------------------------------------------------------------ G3b  representation
A.banner("G3b  THE REPRESENTATION — exact, and the refusals are part of it")
print()

SB = A.Scoreboard(base_red=bool(PROBLEMS))


def refuses(thunk):
    try:
        thunk()
        return None
    except N.NormError as exc:
        return str(exc)


unit = [
    ("identity [1]/[1] is the identity", N.ONE.is_identity() is True),
    ("[2]/[2] is the identity (reduced, not compared literally)",
     N.Factor([2], [2]).is_identity() is True),
    ("[0,2]/[0,2] is the identity (a common n cancels)",
     N.Factor([0, 2], [0, 2]).is_identity() is True),
    ("6n^2/(n^2-1) is NOT the identity",
     N.Factor([0, 0, 6], [-1, 0, 1]).is_identity() is False),
    ("6n^2/(n^2-1) at n=3 is exactly 27/4",
     N.Factor([0, 0, 6], [-1, 0, 1]).at(3) == Fraction(27, 4)),
    ("the value is a Fraction and not a float",
     isinstance(N.Factor([0, 0, 6], [-1, 0, 1]).at(5), Fraction)),
    ("x2 and x1/2 are different factors",
     N.Factor([2], [1]) != N.Factor([1], [2])),
]
for name, ok in unit:
    print("  %-62s %s" % (name, "ok" if ok else "FAILED"))
    if not ok:
        fail("representation unit check failed: %s" % name)

# ---- N11  THE POPULATION TRAP.  A factor that happens to equal 1 at n = 3,4,5 — the whole
#           of POP-PRIM — and 2 at n = 6 is NOT the identity, and treating it as one because
#           the current population stops at 5 would hide it exactly when the population
#           widens.  `is_identity` reads the rational FUNCTION, not its values here.
trap = N.Factor([-59, 47, -12, 1], [1])           # 1 + (n-3)(n-4)(n-5): 1 at n=3,4,5; 7 at n=6
at345 = [trap.at(n) for n in (3, 4, 5)]
SB.arm_outcome("N11 a factor equal to 1 at every n in POP-PRIM but not identically 1",
               "RED", "RED" if not trap.is_identity() else "GREEN",
               "value at n=3,4,5 = %s, at n=6 = %s; is_identity() = %s"
               % ([str(v) for v in at345], trap.at(6), trap.is_identity()))

# ---- N12  A FLOAT COEFFICIENT IS REFUSED.  An inexact factor is the one thing a
#           normalisation must never be: it would put a rounding into the canonical frame
#           and then be compared against a tolerance of 0.000e+00.
SB.arm_outcome("N12 a float coefficient in a factor", "REFUSAL",
               "REFUSAL" if refuses(lambda: N.Factor([1.5], [1])) else "GREEN",
               (refuses(lambda: N.Factor([1.5], [1])) or "")[:96])

# ---- N13  A DENOMINATOR THAT VANISHES IN THE POPULATION.  Not a rounding problem: it is a
#           declaration that does not apply at that n, and it is refused rather than skipped.
SB.arm_outcome("N13 a denominator vanishing at an n in the population", "REFUSAL",
               "REFUSAL" if refuses(lambda: N.Factor([1], [-3, 1]).at(3)) else "GREEN",
               (refuses(lambda: N.Factor([1], [-3, 1]).at(3)) or "")[:96])

# ------------------------------------------------------------------ G3c  worked example
A.banner("G3c  THE WORKED EXAMPLE — eps_spec / eps_c3ca, re-derived from mg-9f91's table")
print("""
  THE TICKET'S OWN SECOND EXAMPLE, and the reason the factor is a rational function of n and
  not a constant.  code/c3_audit_a94c3/a1_algebra.py states
  `eps_spec / eps_c3ca = 6 n^2 / (n^2 - 1) -> 6`, and mg-9f91 tabulates both quantities as
  exact rationals.  The declared factor is checked against that table at every n in it.""")
print()

if not os.path.exists(MAP_PATH):
    fail("mg-9f91's table is gone (%s) — the worked example has no source" % MAP_PATH)
    rows = []
else:
    rows = []
    for line in open(MAP_PATH):
        parts = line.split()
        if len(parts) >= 4 and re.fullmatch(r"\d+", parts[0]) and "/" in parts[1]:
            try:
                rows.append((int(parts[0]), Fraction(parts[1]), Fraction(parts[2]),
                             Fraction(parts[3])))
            except (ValueError, ZeroDivisionError):
                pass

with open(CITE_PATH) as fh:
    cited = CITE_TEXT in fh.read()
print("  the identity %r is still in %s: %s"
      % (CITE_TEXT, os.path.relpath(CITE_PATH, CODE), cited))
if not cited:
    fail("the worked example's identity is no longer where it is cited from")

EX = DECLS.examples.get("eps", {}).get("names", {})
fac = EX.get("a94c3-doc:eps_c3ca", {}).get("factor")
spec_fac = EX.get("a94c3-doc:eps_spec", {}).get("factor")
if fac is None or spec_fac is None:
    fail("the eps worked example is not in NORMALISATION.json")
else:
    print("  declared: eps_spec x%s (canonical);  eps_c3ca x%s"
          % (spec_fac.as_text(), fac.as_text()))
    print()
    print("  %5s %14s %14s %16s %16s %6s" %
          ("n", "eps_c3ca", "eps_spec", "declared factor", "c3ca x factor", "exact"))
    bad = 0
    flat6_err = []
    for n, c3ca, spec, ratio in rows:
        f = fac.at(n)
        got = c3ca * f
        ok = (got == spec)
        bad += 0 if ok else 1
        if len(flat6_err) < 5:
            flat6_err.append((n, float(spec - c3ca * 6)))
        if n <= 12:
            print("  %5d %14s %14s %16s %16s %6s"
                  % (n, c3ca, spec, f, got, "yes" if ok else "NO"))
    print("  ... %d rows in the table, %d checked, %d mismatches" % (len(rows), len(rows), bad))
    SB.arm_outcome("N14 the declared n-dependent factor reproduces mg-9f91's table exactly",
                   "GREEN", "GREEN" if (rows and bad == 0) else "RED",
                   "%d of %d rows exact in Fraction arithmetic" % (len(rows) - bad, len(rows)))
    print()
    print("  WHAT A CONSTANT FACTOR WOULD HAVE GOT WRONG — re-derived here, and it is why a")
    print("  per-name constant field would have been unable to say what this corpus knows:")
    for n, err in flat6_err:
        print("      n=%-4d eps_c3ca x 6  is wrong by %+.4f" % (n, err))
    SB.arm_outcome("N15 a CONSTANT factor of 6 does NOT reproduce the table",
                   "RED", "RED" if any(abs(e) > 1e-12 for _n, e in flat6_err) else "GREEN",
                   "largest error among the smallest n printed above: %+.4f"
                   % max((e for _n, e in flat6_err), key=abs))

# ------------------------------------------------------------------ G3d  planted worlds
A.banner("G3d  PLANTED WORLDS — including the one that scores ticket item 4")
print()


def planted(mutate):
    """Re-parse a MUTATED COPY of the committed file, through the real loader.

    The mutation is applied to the parsed JSON and handed back to `Declarations`, so the
    refusal being scored is the one the shipped constructor raises and not a re-statement of
    it in the arm.
    """
    raw = json.loads(json.dumps(DECLS.raw))
    mutate(raw)
    try:
        d = N.Declarations(raw)
        N.check_consistency(d.decls, GROUPS)
        return None
    except N.NormError as exc:
        return str(exc)


# ---- N7  ITEM 4, SCORED.  This ticket builds the machinery to REPRESENT the (L*)/(M#)
#          normalisation question and does NOT decide it.  An absence is a weak thing to
#          claim, so it is made checkable: no declaration in this file may carry a
#          non-identity factor for a pinned name, and no key or convention may mention the
#          gap.  If mg-5e82 settles it and somebody registers a factor here, this arm goes
#          RED and whoever does it has to come and say so in this file.
FORBIDDEN = re.compile(r"mu_pref\^2|\(L\*\)|\(M#\)|lstar.*mstar", re.I)
touched = sorted(k for k, d in DECLS.decls.items()
                 if FORBIDDEN.search(k) or FORBIDDEN.search(d["convention"]))
non_identity_pinned = sorted("%s:%s" % m for m in PINNED
                             if DECLS.has(m) and not DECLS.factor_for(m).is_identity())
SB.arm_outcome("N7 mg-479c registers NOTHING about the (L*)/(M#) mu_pref^2 gap (item 4)",
               "GREEN", "GREEN" if not touched and not non_identity_pinned else "RED",
               "%d declaration(s) mention it, %d pinned name(s) carry a non-identity factor "
               "— STATE.md:172 is mg-5e82's and is untouched" % (len(touched),
                                                                 len(non_identity_pinned)))

# ---- N8  SAME CONVENTION, DIFFERENT FACTORS.  The label says two names share a frame and
#          the factors say they do not.  This is the check that makes g1's RED sentence
#          "these two names are declared to be in the SAME convention" worth anything.
first = GROUPS[0][1][0]
msg = planted(lambda raw: raw["declarations"][first].__setitem__(
    "to_canonical", {"num": [2], "den": [1]}))
SB.arm_outcome("N8 one name in a shared convention re-declared x2 — the label and the "
               "factor now contradict", "REFUSAL", "REFUSAL" if msg else "GREEN",
               (msg or "")[:120])

# ---- N9  TWO LABELS, ONE FRAME.  A second convention name with the same factor makes the
#          label decorative — and this gate's RED message invites an operator to read it as
#          meaningful.  A decorative field an operator trusts is mg-479c's defect in a new
#          costume.
second = GROUPS[0][1][1]
msg = planted(lambda raw: raw["declarations"][second].__setitem__(
    "convention", "a second name for the same frame"))
SB.arm_outcome("N9 a second convention LABEL declaring the same factor", "REFUSAL",
               "REFUSAL" if msg else "GREEN", (msg or "")[:120])

# ---- N10  AN UNPINNED NAME GAINS A DECLARATION, AND THE GATE MUST STAY GREEN.  Somebody
#           preparing mg-a397's widening declares a normalisation for a name this gate does
#           not pin.  A digest over the whole file would go RED — a red for a non-reason,
#           which is this ticket's own thesis about how gates get disabled.  Filed as E9.
raw2 = json.loads(json.dumps(DECLS.raw))
raw2["declarations"]["some_future_tree_a397:delta(P)"] = {
    "convention": "delta(P) — PLANTED, unpinned",
    "to_canonical": {"num": [1], "den": [2]},
    "source": "PLANTED by g3 arm N10 — not committed"}
d2 = N.Declarations(raw2)
SB.arm_outcome("N10 an UNPINNED name gains a declaration — the pinned digest must NOT move",
               "GREEN", "GREEN" if d2.digest_over(PINNED) == have else "RED",
               "digest %s before, %s after" % (have, d2.digest_over(PINNED)))

# ---- N16  A DECLARATION WITHOUT A SOURCE.  A factor with no provenance is a number
#           somebody typed, and this whole ticket is about a field an operator is invited to
#           trust.
msg = planted(lambda raw: raw["declarations"][first].pop("source"))
SB.arm_outcome("N16 a declaration with no `source`", "REFUSAL",
               "REFUSAL" if msg else "GREEN", (msg or "")[:120])

UNSAT = SB.print_and_score()

# ------------------------------------------------------------------ result
A.banner("g3 RESULT")
status = A.BROKEN if (PROBLEMS or UNSAT) else A.GREEN
print("  %d declarations over %d pinned names in %d groups, %d in a non-identity frame; "
      "%d problem(s), %d arm(s) unsatisfactory."
      % (len(DECLS.decls), len(PINNED), len(GROUPS),
         sum(1 for label, keys in GROUPS
             if N.tolerance_frame([tuple(k.split(":", 1)) for k in keys],
                                  DECLS)[0] == "CANONICAL"),
         len(PROBLEMS), UNSAT))
sys.exit(status)
