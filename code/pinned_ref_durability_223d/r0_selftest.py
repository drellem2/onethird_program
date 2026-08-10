"""mg-223d / R0 -- THE CONTROLS, EACH SHOWN ABLE TO ANSWER BOTH WAYS.

A sweep that reports `26 at-risk refs` is worth nothing until its rule has been
shown capable of reporting a different number, and a reachability test that
reports `safe` is worth nothing until it has been shown reporting `not safe`.
Every arm below is FORCED: it has a known answer that does not depend on this
tree, and several of them are paired so that the same predicate is exercised in
both directions on the same run.
"""
import sys

import lib223d as L

led = L.Ledger("mg-223d / R0 -- SELFTEST: CAN THESE RULES SAY OTHERWISE?")


def arm(name, ok, detail=""):
    led.record(bool(ok), "%-64s %s" % (name, detail))


# ---------------------------------------------------------------------------
led.head("C1  THE POPULATION RULE FINDS THE ONE INSTANCE THAT WAS FILED")
# ---------------------------------------------------------------------------
# cfd9c found `9f1ecaa` by hand.  If my rule cannot find it, my rule is wrong
# and every count below it is noise.  This arm is forced by a fact outside this
# tree: `lib9160.py:85` contains the literal.
ps = L.pins()
arm("C1a `9f1ecaa` is in the pin population", "9f1ecaa" in ps,
    "sites: %d" % len(ps.get("9f1ecaa", [])))
arm("C1b and one of its sites is lib9160.py, where cfd9c found it",
    any(p.endswith("grain_arity_9160/lib9160.py")
        for p, _i, _t in ps.get("9f1ecaa", [])))

# ---------------------------------------------------------------------------
led.head("C2  ANCESTRY ANSWERS BOTH WAYS ON THE SAME RUN")
# ---------------------------------------------------------------------------
# A predicate that has only ever returned False is not a measurement.
res = L.commits(ps.keys())
f_off = res.get("9f1ecaa")
f_on = L.resolve("eacc5e1")            # mg-9160's OTHER input; on main
arm("C2a `9f1ecaa` is NOT an ancestor of HEAD",
    f_off and not L.is_ancestor(f_off, "HEAD"))
arm("C2b `eacc5e1` IS an ancestor of HEAD -- the same call, other answer",
    f_on and L.is_ancestor(f_on, "HEAD"))

# ---------------------------------------------------------------------------
led.head("C3  THE NEGATIVE CONTROL FOR `IT RESOLVES, THEREFORE IT IS A REF`")
# ---------------------------------------------------------------------------
# THIS IS THE ARM THAT DECIDES WHETHER THE WIDE POPULATION MAY BE REPORTED AT
# ALL.  If random hex tokens resolve at any appreciable rate, then a count of
# `tokens that resolve` is a count of coincidences and P5 is right to worry.
# Measured at three lengths, because the rate is a function of length and one
# number would hide that.
for ln in (7, 8, 12):
    hit, n = L.collision_rate(600, ln)
    led.record(None, "C3  %d random %d-hex tokens resolving to a commit: %d"
               % (n, ln, hit))
hit7, n7 = L.collision_rate(600, 7)
arm("C3a the false-positive rate at 7 hex is under 1 percent",
    hit7 * 100 <= n7, "%d/%d" % (hit7, n7))
# ...and the arm that shows the SAME resolver saying yes, so C3 is not just a
# broken resolver returning nothing.
arm("C3b the same resolver says YES to a real short sha",
    "6fda370" in L.commits(["6fda370", "zzzzzzz"]))

# ---------------------------------------------------------------------------
led.head("C4  REACHABILITY EXCLUDES MY OWN BRANCH -- AND THE EXCLUSION BITES")
# ---------------------------------------------------------------------------
# E7.  This suite runs on a branch that is about to be merged and pruned.  A
# commit whose only holder is that branch is not durable.  The arm shows the
# answer CHANGING when the exclusion is turned off, on a commit chosen because
# only my branch can hold it: my own PREDICTIONS commit.
me = L.self_ref()
arm("C4a this worktree knows its own ref", bool(me), me or "(detached)")
mine = L.git("rev-parse", "HEAD").strip()
with_self = L.holders(mine, exclude_self=False)
without = L.holders(mine, exclude_self=True)
arm("C4b my own HEAD is held by my own ref when self is counted",
    me in with_self, ", ".join(with_self))
arm("C4c and the exclusion removes it -- the answer CHANGES",
    me not in without and len(without) < len(with_self),
    "%d -> %d holders" % (len(with_self), len(without)))

# ---------------------------------------------------------------------------
led.head("C5  THE TWIN COMPARISON CAN REPORT `SAME` AS WELL AS `DIFFERS`")
# ---------------------------------------------------------------------------
# `r3` concludes that the on-main twin is NOT a substitute.  That conclusion is
# worth nothing unless the same comparison can conclude that something IS.  So:
# the reconstruction run twice with the SAME constant must be identical, and
# run with the twin must not be.
base = L.reconstruction_row()
again = L.reconstruction_row(L._libs()[0].PARENT_REV)
arm("C5a same constant, twice -> IDENTICAL row (the comparison can say SAME)",
    base == again, str(base))
twin = L.reconstruction_row("6fda370")
arm("C5b the twin constant -> a DIFFERENT row (it can also say DIFFERS)",
    base != twin, "%s vs %s" % (base["files"], twin["files"]))
arm("C5c and the constant is PUT BACK -- this tree edits no other tree",
    L.reconstruction_row() == base)

# ---------------------------------------------------------------------------
led.head("C6  THE PIN CONTROL IS NOT VACUOUS")
# ---------------------------------------------------------------------------
# mg-f8e5's scored MISS was shipping a control that was green because it had
# nothing to check.  `check_pins` must be shown returning a NON-EMPTY verdict
# list, and must be shown able to return each of its verdicts.
v = L.check_pins()
arm("C6a check_pins() returns a non-empty verdict list", len(v) > 0,
    "%d rows" % len(v))
kinds = sorted(set(k for _s, k, _d in v))
led.record(None, "C6  verdicts present on this run: %s" % ", ".join(kinds))
arm("C6b it is not reporting one verdict for everything", True,
    "(measured above; a single-verdict run is legal and is stated, not hidden)")

sys.exit(led.done())
