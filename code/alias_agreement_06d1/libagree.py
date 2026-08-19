"""libagree — the agreement check, and NOT a second opinion about any number.

mg-0d1b built the index; this file cashes it.  `code/alias_index_0d1b/INDEX.md` records 11
quantities aliased across up to 13 names in up to 11 trees, with ZERO disagreements in 12
measured groups, and mg-0d1b's own reading of that result is this ticket:

    "the hazard is SILENCE, not error.  Twelve independent instruments compute the same
     twelve quantities and nothing has ever compared them.  EVERY ROW IS A CONTROL THE ARC
     HAS ALREADY PAID FOR AND HAS NEVER CASHED."

THIS FILE ADDS NO MATHEMATICS, for the same reason `lib0d1b` adds none: an agreement it
computed would be an agreement with ME.  Every scalar still comes from the tree that owns
it, through that tree's own entry point, via `lib0d1b`'s adapters — this module imports
`lib0d1b` rather than reimplementing it, so the numbers compared here are byte-for-byte
the numbers mg-0d1b measured its tolerances over.  `spread()` in particular is IMPORTED,
not re-derived: a tolerance is only meaningful against the distance function that produced
it.

THE ONE DESIGN DECISION THAT MAKES THIS A GATE AND NOT A RE-RUN OF x3
---------------------------------------------------------------------
`x3_values.py` forms alias groups FROM the values and reads the names afterwards.  That is
the correct instrument for DISCOVERY and it is the wrong one for a gate, because its
failure mode is silence in exactly the case the gate exists for:

    if `chain_iv_c_81ff:lambda2_bracket` stopped agreeing with the other eight gamma names,
    x3's clustering would put it in its own cluster, print "8 names in 8 trees" instead of
    nine, and EXIT 0.

A group that quietly loses a member is the defect, not the report of it.  So the gate pins
the MEMBERSHIP from `BASELINE.json` — mg-0d1b's own machine output, frozen — and asks only
whether the pinned members still agree.  Arm W5 of `g1_values.py` demonstrates this rather
than asserting it: it plants a drifted column and shows the value-blind clustering rule
staying GREEN on the same input this check calls RED.

WHAT RED MEANS, AND WHAT IT DOES NOT MEAN
-----------------------------------------
RED means two names for one quantity disagree beyond the tolerance mg-0d1b measured.  It
does NOT mean either of them is wrong, and this module deliberately offers no way to say
which.  Per the ticket: a disagreement is a FINDING and gets a ticket, not a quiet
reconciliation — there is no `--refresh`, no `--accept`, and no rule that prefers the more
recently edited tree.  Rewriting the expectation to match the observation is the laundering
this arc keeps paying for.

--- mg-479c -------------------------------------------------------------------------------
THE COMPARISON NOW HAPPENS IN THE CANONICAL FRAME, AND A THIRD OUTCOME EXISTS.

mg-06d1's check could not tell a NORMALISATION from a DISAGREEMENT: a factor of 2 between
two live conventions and a genuine 2x error were the same signal.  `check_groups` therefore
canonicalises every pinned column through `libnorm` BEFORE comparing, reports the factor it
applied in the RED message, and adds a third outcome beside GREEN and RED:

    REFUSE   a pinned name has no declared normalisation, or a group carries a non-identity
             factor against a tolerance measured in the raw frame.  Exit 2, not 1 — an
             undeclared field means the comparison could not be made, which is a different
             fact from two numbers disagreeing, and this suite's exit convention already
             distinguishes them.

`check_groups` therefore returns `(verdicts, n_red, refusals)` where it returned a pair.
Nothing about the twelve pinned groups changes today: all 71 names are in the identity
normalisation, the identity is a PASS-THROUGH and not a multiply by 1.0, and arm N1 measures
the bit-identity of all 71 canonical columns against the raw ones rather than arguing it.
"""

import json
import math
import os
import sys

import libnorm as NORM                                                # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX_DIR = os.path.join(os.path.dirname(HERE), "alias_index_0d1b")
sys.path.insert(0, INDEX_DIR)

import lib0d1b as L                                                  # noqa: E402

BASELINE_PATH = os.path.join(HERE, "BASELINE.json")


# ------------------------------------------------------------------ exit convention
#
# Shared with code/control_gate_724a and code/state_ratchet_e331 so that `build.sh`'s
# "worst suite exit wins" rule composes: 0 green, 1 a control fired, 2 refused/broken.
GREEN, RED, BROKEN = 0, 1, 2


def banner(s):
    print()
    print("=" * 78)
    print(s)
    print("=" * 78)


# ------------------------------------------------------------------ capture

def finite(v):
    """Is this value one that `spread()` will actually compare?

    `lib0d1b.spread` skips positions where either side is None, NaN or infinite.  A gate
    that did not track WHICH positions those are could watch a column decay to all-None
    and report a spread of 0.0 over the empty set — agreement by absence.  The baseline
    therefore records the comparable count per column and `check_groups` treats a change
    in it as RED in either direction.
    """
    return v is not None and v == v and not math.isinf(v)


def capture(pop):
    """{(tree, name): [value per poset]} over `pop`, computed by the owning trees.

    An adapter that RAISES is not allowed to be a silent gap: the tree is recorded as
    broken and `check_groups` turns every group that pinned one of its names RED.  A
    corpus edit that makes a tree unloadable removes it from every agreement it was
    party to, which is the same loss of a control as a numeric drift and is reported the
    same way.
    """
    cols, kind, broken = {}, {}, {}
    for tree, ad, _f in L.ADAPTERS:
        try:
            per_poset = []
            for (n, dn) in pop:
                native = ad(dn, n)
                per_poset.append((native, L.composed(tree, native)))
        except Exception as exc:                                     # noqa: BLE001
            broken[tree] = "%s: %s" % (type(exc).__name__, exc)
            continue
        names = set()
        for native, comp in per_poset:
            names |= set(native) | set(comp)
        for nm in names:
            col = []
            for native, comp in per_poset:
                col.append(comp[nm] if nm in comp else native.get(nm))
            cols[(tree, nm)] = col
            kind[(tree, nm)] = "COMPOSED" if nm in per_poset[0][1] else "native"
    return cols, kind, broken


# ------------------------------------------------------------------ the comparison

def worst_pair(cols, members):
    """(spread, a, b, poset_index, va, vb) over the pinned members — the WHOLE point.

    `lib0d1b.max_intra` returns the magnitude alone.  A gate that printed only a magnitude
    would tell an author that something moved by 3e-7 and leave them to find which two of
    thirteen names it was; the ticket asks for RED "naming both aliases", so this returns
    the pair and the poset that achieve the maximum.  `selfcheck_spread` proves this walk
    agrees with `lib0d1b.spread` rather than assuming it.
    """
    best = (0.0, None, None, None, None, None)
    for i, a in enumerate(members):
        for b in members[i + 1:]:
            ca, cb = cols[a], cols[b]
            for idx, (x, y) in enumerate(zip(ca, cb)):
                if not (finite(x) and finite(y)):
                    continue
                d = abs(x - y)
                if d > best[0]:
                    best = (d, a, b, idx, x, y)
    return best


def selfcheck_spread(cols, groups):
    """My pairwise walk vs `lib0d1b.spread`, on every pinned pair.  Returns #mismatches.

    Reimplementing a distance function in order to name its argmax is exactly how a check
    ends up measuring something slightly different from the tolerance it is checked
    against.  So the reimplementation is CHECKED against the original on the real data,
    every run, rather than argued to be equivalent.
    """
    bad = 0
    for g in groups:
        ms = [tuple(m) for m in g["members"] if tuple(m) in cols]
        for i, a in enumerate(ms):
            for b in ms[i + 1:]:
                mine = worst_pair(cols, [a, b])[0]
                theirs = L.spread(cols[a], cols[b])
                theirs = 0.0 if theirs is None else theirs
                if abs(mine - theirs) > 0:
                    bad += 1
    return bad


def check_groups(cols, broken, baseline, tol_override=None,
                 decls=None, ns=None, normalise=True):
    """Every pinned group in its CANONICAL frame.  Returns (verdicts, n_red, refusals).

    Four ways a group goes RED, and only the first is a "disagreement" in the everyday
    sense.  The other three are the shapes silence actually takes:

      DISAGREE           two pinned names differ, AFTER NORMALISING, by more than the
                         recorded tolerance.
      MEMBERSHIP-LOST    a pinned name is no longer produced at all.
      TREE-BROKEN        the tree that owns a pinned name no longer loads or runs.
      COMPARABILITY      a pinned name is still produced but is None/NaN/inf at a
                         different number of posets than when the tolerance was measured,
                         so the agreement is now being asserted over a different set.

    And two ways it REFUSES, which are not reds (mg-479c):

      UNDECLARED-NORMALISATION   a pinned name has no entry in NORMALISATION.json.  Never
                                 defaulted to "same": defaulting is the FALSE PASS direction
                                 of mg-479c with the volume turned all the way down.
      TOLERANCE-FRAME            the group carries a non-identity factor and the tolerance
                                 it is being checked against was measured in the raw frame.

    `normalise=False` is the PRE-mg-479c comparison — raw values, no declarations consulted.
    It is not a strawman: arm N2 measures that on the real input the two paths produce
    identical verdicts, and `x1_wrongway.py` runs the blob-pinned pre-479c `libagree.py`
    itself.  It exists so the wrong-way demonstration is a demonstration and not an argument.
    """
    if normalise and decls is None:
        raise NORM.NormError(
            "check_groups was asked to compare in the canonical frame with no declarations.  "
            "Refusing rather than falling back to the raw comparison: a caller that silently "
            "got the pre-479c behaviour when it asked for the canonical one is the FALSE PASS "
            "direction of mg-479c, in this module's own call signature.")
    verdicts, red, refusals = [], 0, []
    for g in baseline["groups"]:
        pinned = [tuple(m) for m in g["members"]]
        tol = g["tolerance"] if tol_override is None else tol_override
        problems = []

        missing = [m for m in pinned if m not in cols]
        for m in missing:
            if m[0] in broken:
                problems.append(("TREE-BROKEN", m, broken[m[0]]))
            else:
                problems.append(("MEMBERSHIP-LOST", m, "no longer produced by its tree"))

        present = [m for m in pinned if m in cols]
        for m in present:
            want = g["comparable"]["%s:%s" % m]
            got = sum(1 for v in cols[m] if finite(v))
            if got != want:
                problems.append(("COMPARABILITY", m,
                                 "comparable at %d posets, baseline recorded %d"
                                 % (got, want)))

        # ---- mg-479c: into the canonical frame, or refuse to compare at all
        frame, why, applied, ccols = "RAW (pre-479c path)", "", {}, cols
        if normalise:
            try:
                ccols, applied = NORM.canonicalise(cols, present, decls, ns)
                frame, why = NORM.tolerance_frame(present, decls)
            except NORM.NormError as exc:
                refusals.append(("UNDECLARED-NORMALISATION", g["label"], str(exc)))
                verdicts.append({"label": g["label"], "tolerance": tol, "spread": None,
                                 "n_pinned": len(pinned), "n_present": len(present),
                                 "problems": problems, "frame": "REFUSED", "why": str(exc),
                                 "applied": {}, "refused": True})
                if problems:
                    red += 1
                continue
            if frame == "CANONICAL" and tol_override is None:
                ct = decls.canonical_tolerance(g["label"])
                if ct is None:
                    refusals.append((
                        "TOLERANCE-FRAME", g["label"],
                        "%s, but the tolerance %.6e is mg-0d1b's max spread of RAW values.  "
                        "It is not rescalable — members with different factors admit no "
                        "single multiplier — so it is not stated in the frame this "
                        "comparison happens in.  Record a canonical-frame tolerance for "
                        "this group in NORMALISATION.json with its measured source."
                        % (why, tol)))
                    verdicts.append({"label": g["label"], "tolerance": tol, "spread": None,
                                     "n_pinned": len(pinned), "n_present": len(present),
                                     "problems": problems, "frame": "REFUSED", "why": why,
                                     "applied": applied, "refused": True})
                    if problems:
                        red += 1
                    continue
                tol = ct["tolerance"]

        sp, a, b, idx, va, vb = worst_pair(ccols, present) if len(present) > 1 \
            else (0.0, None, None, None, None, None)
        if len(present) > 1 and sp > tol:
            detail = ["spread %.6e > tolerance %.6e at poset #%d (%s frame)"
                      % (sp, tol, idx, frame),
                      "%s:%s = %.17g   vs   %s:%s = %.17g"
                      % (a[0], a[1], va, b[0], b[1], vb)]
            if normalise:
                ra, rb = cols[a][idx], cols[b][idx]
                if (ra, rb) != (va, vb):
                    detail.append("raw (before normalising): %.17g   vs   %.17g" % (ra, rb))
                detail.extend(NORM.describe_pair(a, b, ra, rb, decls))
            problems.append(("DISAGREE", (a, b), "\n             ".join(detail)))

        verdicts.append({"label": g["label"], "tolerance": tol, "spread": sp,
                         "n_pinned": len(pinned), "n_present": len(present),
                         "problems": problems, "frame": frame, "why": why,
                         "applied": applied, "refused": False})
        if problems:
            red += 1
    return verdicts, red, refusals


def norm_summary(v):
    """The normalisation column, printed on EVERY row, green as well as red.

    A factor that only becomes visible when something breaks is invisible, and a declared
    factor is the one thing in this gate an operator can use to silence a real disagreement
    (README §7).  So it is on the green lines too.
    """
    if not v.get("applied"):
        return ""
    non_id = [(m, f) for m, f in sorted(v["applied"].items()) if not f.is_identity()]
    if not non_id:
        return "  norm identity x%d" % len(v["applied"])
    return "  norm %s" % ", ".join("%s:%s x%s" % (m[0], m[1], f.as_text())
                                   for m, f in non_id)


def report(verdicts, quiet=False):
    for v in verdicts:
        if v.get("refused"):
            print("  REFUSE %-24s %2d/%2d names   %s"
                  % (v["label"], v["n_present"], v["n_pinned"], v["why"]))
        if v["problems"]:
            print("  RED    %-24s %2d/%2d names   spread %s   tol %.3e%s"
                  % (v["label"], v["n_present"], v["n_pinned"],
                     "n/a" if v["spread"] is None else "%.3e" % v["spread"],
                     v["tolerance"], norm_summary(v)))
            for kindname, who, detail in v["problems"]:
                if kindname == "DISAGREE":
                    a, b = who
                    print("           %s — %s:%s  vs  %s:%s" % (kindname, a[0], a[1],
                                                                b[0], b[1]))
                    print("             %s" % detail)
                else:
                    print("           %s — %s:%s" % (kindname, who[0], who[1]))
                    print("             %s" % detail)
        elif not v.get("refused") and not quiet:
            print("  agree  %-24s %2d names   spread %.3e   tol %.3e%s"
                  % (v["label"], v["n_present"], v["spread"], v["tolerance"],
                     norm_summary(v)))


# ------------------------------------------------------------------ planted worlds
#
# mg-9876's guard, adopted rather than paraphrased: the UNMUTATED input is scored FIRST,
# and a probe that is already satisfied by the good input is UNFALSIFIABLE and is never
# counted as CAUGHT.  A check that has only ever seen agreement is the exact condition
# mg-9876 was filed about, and this row of the corpus has only ever seen agreement.
#
# Every mutation below is DERIVED from the captured columns — an epsilon added to a value
# the trees actually produced — rather than typed as a literal.  A hand-typed "known bad"
# value is a fixture the instrument was built around; a perturbed real one is not.

def clone(cols):
    return {k: list(v) for k, v in cols.items()}


def mut_add_at(cols, key, idx, eps):
    """Add eps to ONE poset's value — the smallest real disagreement."""
    c = clone(cols)
    c[key] = list(c[key])
    c[key][idx] = c[key][idx] + eps
    return c


def mut_add_all(cols, key, eps):
    """Add eps everywhere — a column that has DRIFTED OUT of its group entirely."""
    c = clone(cols)
    c[key] = [None if v is None else v + eps for v in c[key]]
    return c


def mut_blank_at(cols, key, idx):
    """One value becomes uncomputable.  `spread()` skips it; the gate must not."""
    c = clone(cols)
    c[key] = list(c[key])
    c[key][idx] = None
    return c


def mut_drop(cols, key):
    """The name stops existing.  Under value-blind clustering this is a smaller group."""
    c = clone(cols)
    del c[key]
    return c


def first_comparable(cols, key):
    for i, v in enumerate(cols[key]):
        if finite(v):
            return i
    return None


class Scoreboard(object):
    """CAUGHT / MISSED / UNFALSIFIABLE, with the unmutated verdict scored first.

    UNFALSIFIABLE is not a pass.  It is the report that a probe could not have failed on
    this input, and it is kept as its own outcome because mg-724a's exhibit found a probe
    that could not fire only by running it — the arm reported CAUGHT for a world that was
    already true before the mutation.
    """

    def __init__(self, base_red):
        self.base_red = base_red
        self.rows = []

    def arm_outcome(self, name, expect, got, note=""):
        """Three-valued arms — GREEN / RED / REFUSAL (mg-479c).

        `arm()` below can only ask "did it go red?", and mg-479c adds a world where the
        correct answer is neither: an undeclared normalisation must make the gate REFUSE
        (exit 2), and a two-valued arm would score that as CAUGHT for a red it never got, or
        as MISSED for a refusal that is exactly right.  The distinction is the ticket's own
        — a control firing and an instrument declining to answer are different facts and
        this suite's exit convention already separates them.
        """
        if self.base_red and expect != "GREEN":
            out = "UNFALSIFIABLE"
        elif got == expect == "GREEN":
            out = "REFUSED-CORRECTLY"
        elif got == expect:
            out = "CAUGHT"
        elif expect == "GREEN":
            out = "FALSE-POSITIVE"
        else:
            out = "MISSED"
        detail = "expected %s, got %s" % (expect, got)
        self.rows.append((name, out, detail + ("  ·  " + note if note else "")))
        return out

    def arm(self, name, expect_red, red, note=""):
        if self.base_red and expect_red:
            out = "UNFALSIFIABLE"                    # already red before the mutation
        elif expect_red and red:
            out = "CAUGHT"
        elif expect_red and not red:
            out = "MISSED"
        elif not expect_red and not red:
            out = "REFUSED-CORRECTLY"                # a world that must NOT go red
        else:
            out = "FALSE-POSITIVE"
        self.rows.append((name, out, note))
        return out

    def print_and_score(self):
        print()
        bad = 0
        for name, out, note in self.rows:
            print("    %-17s %s" % (out, name))
            if note:
                print("                      %s" % note)
            if out in ("MISSED", "FALSE-POSITIVE", "UNFALSIFIABLE"):
                bad += 1
        caught = sum(1 for _n, o, _t in self.rows if o == "CAUGHT")
        refused = sum(1 for _n, o, _t in self.rows if o == "REFUSED-CORRECTLY")
        print()
        print("    %d CAUGHT · %d REFUSED-CORRECTLY · %d unsatisfactory, of %d arms"
              % (caught, refused, bad, len(self.rows)))
        return bad


# ------------------------------------------------------------------ baseline io

def load_baseline():
    with open(BASELINE_PATH) as fh:
        return json.load(fh)
