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

WHAT RED COULD NOT SAY UNTIL mg-479c, AND NOW CAN
-------------------------------------------------
Until mg-479c this file compared RAW values and had no representation for two names
denoting one quantity IN DIFFERENT NORMALISATIONS.  A factor of 2 between two live
conventions and a genuine 2x error produced the identical signal, in both directions: a
FALSE RED on a gate that blocks merges, and a FALSE PASS in which a real error is
dismissable as "just a normalisation difference".  `libnorm` now holds the field, the
comparison happens AFTER canonicalising, and the RED message states the factor that was
applied and whether the two names DECLARE THE SAME CONVENTION — which is the half that
lets an operator tell the two cases apart.

`norm=None` is the pre-mg-479c path, kept and reachable, because `g1_values.py` MEASURES
the two paths agreeing on the real input rather than arguing that the identity factor is a
pass-through.
"""

import json
import math
import os
import sys

import libnorm as NM

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


def check_groups(cols, broken, baseline, tol_override=None, norm=None, pop=None):
    """Every pinned group against its recorded tolerance.  Returns (verdicts, n_red).

    Four ways a group goes RED, and only the first is a "disagreement" in the everyday
    sense.  The other three are the shapes silence actually takes:

      DISAGREE           two pinned names differ by more than the recorded tolerance.
      MEMBERSHIP-LOST    a pinned name is no longer produced at all.
      TREE-BROKEN        the tree that owns a pinned name no longer loads or runs.
      COMPARABILITY      a pinned name is still produced but is None/NaN/inf at a
                         different number of posets than when the tolerance was measured,
                         so the agreement is now being asserted over a different set.

    `norm` (a `libnorm.Declarations`) canonicalises before comparing and annotates the
    DISAGREE message with the factor applied and with whether the two names DECLARE THE
    SAME CONVENTION.  `norm=None` is the pre-mg-479c comparison, unchanged, and is what the
    falsification arms W1-W8 still run against.  COMPARABILITY is measured on the RAW
    columns deliberately: canonicalisation is a division by a nonzero rational and cannot
    change which positions are finite, so measuring it downstream would only hide a
    canonicaliser that did.
    """
    raw_cols = cols
    if norm is not None:
        cols = NM.canonicalise(cols, norm, pop)
    verdicts, red = [], 0
    for g in baseline["groups"]:
        pinned = [tuple(m) for m in g["members"]]
        if tol_override is not None:
            tol, frame = tol_override, "override"
        elif norm is not None:
            tol, frame = NM.tolerance_for(norm, g)
        else:
            tol, frame = g["tolerance"], "raw"
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
            got = sum(1 for v in raw_cols[m] if finite(v))
            if got != want:
                problems.append(("COMPARABILITY", m,
                                 "comparable at %d posets, baseline recorded %d"
                                 % (got, want)))

        sp, a, b, idx, va, vb = worst_pair(cols, present) if len(present) > 1 \
            else (0.0, None, None, None, None, None)
        if len(present) > 1 and sp > tol:
            detail = ("spread %.6e > tolerance %.6e (%s frame) at poset #%d: "
                      "%s:%s = %.17g   vs   %s:%s = %.17g"
                      % (sp, tol, frame, idx, a[0], a[1], va, b[0], b[1], vb))
            if norm is not None:
                detail += "\n             " + _norm_verdict(norm, a, b, idx, pop, raw_cols)
            problems.append(("DISAGREE", (a, b), detail))

        verdicts.append({"label": g["label"], "tolerance": tol, "spread": sp,
                         "frame": frame,
                         "n_pinned": len(pinned), "n_present": len(present),
                         "problems": problems})
        if problems:
            red += 1
    return verdicts, red


def _norm_verdict(norm, a, b, idx, pop, raw_cols):
    """The half of the RED message that tells a normalisation from a disagreement.

    A bare inequality leaves an operator unable to say whether they are looking at two
    live conventions or at a real 2x error, and that ambiguity is what makes a genuine
    error dismissable.  So the message states, for both names, the convention they DECLARE
    and the factor that was APPLIED before the comparison — and then says in one line what
    follows from the two declarations being the same or different.
    """
    n = pop[idx][0] if pop is not None and idx is not None else None
    ca, cb = norm.convention_of(a), norm.convention_of(b)
    lines = ["declared: %s:%s  %s" % (a[0], a[1], NM.describe(norm, a, n)),
             "          %s:%s  %s" % (b[0], b[1], NM.describe(norm, b, n))]
    if ca is not None and ca == cb:
        lines.append("BOTH NAMES DECLARE THE SAME CONVENTION (%r), so this residue is NOT "
                     "a normalisation difference." % ca)
        lines.append("  It is a disagreement between two implementations of one quantity "
                     "in one frame.  File a ticket.")
        if _looks_like_a_ratio(raw_cols, a, b):
            lines.append("  NOTE: the two columns are in a CONSTANT RATIO of %s across "
                         "every comparable poset.  That is the shape of an undeclared "
                         "normalisation — but the declarations above say there is none, "
                         "so either a factor is missing from this file or one of the two "
                         "trees is wrong by that factor.  The instrument cannot tell "
                         "which and does not guess."
                         % _looks_like_a_ratio(raw_cols, a, b))
    else:
        lines.append("THE NAMES DECLARE DIFFERENT CONVENTIONS (%r vs %r) and the factors "
                     "above were APPLIED before this comparison." % (ca, cb))
        lines.append("  So the spread is what is LEFT OVER after the declared "
                     "normalisation, not the normalisation itself.")
    return "\n             ".join(lines)


def _looks_like_a_ratio(cols, a, b):
    """The exact constant ratio between two raw columns, or None.

    A diagnostic and NOT a verdict: it never changes red to green or green to red, and it
    never proposes a factor to declare.  It exists because "these two columns differ by
    exactly 2 everywhere and neither declares a factor" is the single most useful sentence
    that can be printed next to a disagreement, and printing it is the difference between
    an operator who can act and one who is looking at an inequality.
    """
    if a not in cols or b not in cols:
        return None
    from fractions import Fraction
    r = None
    seen = 0
    for x, y in zip(cols[a], cols[b]):
        if not (finite(x) and finite(y)) or y == 0:
            continue
        q = Fraction(x) / Fraction(y)
        seen += 1
        if r is None:
            r = q
        elif q != r:
            return None
    if r is None or seen < 2 or r == 1:
        return None
    return str(r)


def report(verdicts, quiet=False):
    for v in verdicts:
        if v["problems"]:
            print("  RED    %-24s %2d/%2d names   spread %.3e   tol %.3e"
                  % (v["label"], v["n_present"], v["n_pinned"], v["spread"],
                     v["tolerance"]))
            for kindname, who, detail in v["problems"]:
                if kindname == "DISAGREE":
                    a, b = who
                    print("           %s — %s:%s  vs  %s:%s" % (kindname, a[0], a[1],
                                                                b[0], b[1]))
                    print("             %s" % detail)
                else:
                    print("           %s — %s:%s" % (kindname, who[0], who[1]))
                    print("             %s" % detail)
        elif not quiet:
            print("  agree  %-24s %2d names   spread %.3e   tol %.3e"
                  % (v["label"], v["n_present"], v["spread"], v["tolerance"]))


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

    def arm(self, name, expect_red, red, note=""):
        return self.arm_state(name, "RED" if expect_red else "GREEN",
                              "RED" if red else "GREEN", note)

    def arm_state(self, name, expect, got, note=""):
        """Three-state, because mg-479c added a third outcome that is neither.

        REFUSED (exit 2) is not RED (exit 1) and the difference is the whole of the
        ticket's item 3: an undeclared normalisation must fail LOUDLY as "this instrument
        cannot answer", not quietly as "these two numbers disagree".  An arm that scored
        the two the same could not tell a working refusal from a working red, so the
        expectation is a state and not a boolean.  `expect`/`got` are GREEN, RED, REFUSED.
        """
        if self.base_red and expect != "GREEN":
            out = "UNFALSIFIABLE"                    # already red before the mutation
        elif got == expect:
            out = "CAUGHT" if expect != "GREEN" else "REFUSED-CORRECTLY"
        elif expect == "GREEN":
            out = "FALSE-POSITIVE"
        elif got == "GREEN":
            out = "MISSED"
        else:
            out = "WRONG-REASON"                     # fired, but not as the state expected
        self.rows.append((name, out, note))
        return out

    def print_and_score(self):
        print()
        bad = 0
        for name, out, note in self.rows:
            print("    %-17s %s" % (out, name))
            if note:
                print("                      %s" % note)
            if out in ("MISSED", "FALSE-POSITIVE", "UNFALSIFIABLE", "WRONG-REASON"):
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
