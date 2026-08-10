"""mg-fd9c / S0 -- the self-test.

TWO OF THESE ARMS ARE THE WHOLE CREDIBILITY OF THIS TREE.

  C6 / C7  are NEGATIVE CONTROLS on the oscillation detector.  This tree's
           headline is that a census map CONVERGES.  A detector that has never
           reported a cycle cannot be believed when it reports none, so C6 and
           C7 hand it two maps that provably cannot converge and require it to
           say so.  If either goes green-by-not-firing, the headline is worth
           nothing.

  C1       holds MY census composition to mg-03d1's OWN PUBLISHED NUMBERS at
           mg-9160's reconstruction.  My `census()` is a re-typing of a
           function that lives inside a probe and so cannot be imported; C1 is
           what stops that re-typing from being a second opinion nobody asked
           for.  It is the arm that can fail on a single wrong line.

Exit code = number of failed arms.
"""

import sys

import libfd9c as U

BAD = 0
CASES = []


def arm(name, got, want, note=""):
    global BAD
    ok = got == want
    CASES.append((name, ok, got, want, note))
    if not ok:
        BAD += 1


U.bar("mg-fd9c / S0 -- SELFTEST")
print("HEAD: %s" % U.head())
print()

# --------------------------------------------------------------------- C1-C2
recon = U.census(U.read_all([p for p, _r in U.G.parent_corpus()]) if False
                 else (U.B.read(p, r) for p, r in U.G.parent_corpus()))
arm("C1 census() at mg-9160's reconstruction == mg-03d1's published figures",
    tuple(recon[f] for f in U.FIELDS), (517, 1191, 246, 626, 400),
    "the forced arm: my composition against the parent's printed numbers")

idx = U.census(U.B.read(p, U.G.PARENT_REV) for p in U.G.corpus(U.G.PARENT_REV))
arm("C2 census() at the index of 9f1ecaa alone == mg-9160's published row",
    tuple(idx[f] for f in U.FIELDS), (510, 1068, 246, 626, 363),
    "the same composition at the ref that is NOT where the figures live")

# --------------------------------------------------------------------- C3-C5
paths = U.B.all_transcripts()
pres, absent, delta = U.own_weight("code/grain_arity_9160", paths)
arm("C3 emptying a tree leaves the FILE count alone", delta["files"], 0,
    "`>` truncates, it does not unlink -- this is the TRUNC fingerprint")
arm("C4 emptying a tree removes rows", delta["rows"] > 0, True)
_p2, _a2, d2 = U.own_weight("code/no_such_tree_zzzz", paths)
arm("C5 NEGATIVE CONTROL: a tree not in the corpus weighs nothing",
    tuple(d2[f] for f in U.FIELDS), (0, 0, 0, 0, 0),
    "if this fires, `own_weight` is matching on something other than the path")
_stats = U.file_stats(paths)
_fast = U.weight_of(_stats, lambda p: p.startswith("code/grain_arity_9160/"))
arm("C5b the FAST weight agrees with the reference, field for field",
    tuple(_fast[f] for f in U.FIELDS[1:]),
    tuple(delta[f] for f in U.FIELDS[1:]),
    "a speed-up that disagrees with the reference is a second answer")

# --------------------------------------------------------------------- C6-C8
base = U.census(U.read_all(paths))
arm("C6 THE ANTI-VACUITY ARM: r_fixed's own text really is counted",
    U._rows_of(U.r_fixed(base)), len(U.FIELDS),
    "0 here makes every 'converged' below true of a state nobody counted")
o, start, per = U.orbit(U.r_fixed, k=12, paths=paths)
arm("C7 the arc's own transcript shape reaches a FIXED POINT", per, 1,
    "period 1 == fixed point; this is the shape every arc probe has")
for P in (2, 3, 5):
    cyc = U.make_cycler(base["rows"], P)
    arm("C8.%d NEGATIVE CONTROL: a value-shaped transcript cycles at period %d"
        % (P, P), U.orbit(cyc, k=60, paths=paths)[2], P,
        "the detector reports the DESIGNED period, not merely 'not 1'")

# --------------------------------------------------------------------- C9-C11
bl = U.blobs()
hsha = dict(U.tree_blobs(U.git("rev-parse", "HEAD").strip()))
probe = "code/grain_arity_9160/out_s1_reproduce.txt"
arm("C9 `git cat-file` agrees with the disk for a tracked, unmodified file",
    bl.get(hsha.get(probe, "")) == U.B.read(probe), True)
arm("C10 count_rows of an empty transcript is 0", U.census([""])["rows"], 0)
bl.close()

# -------------------------------------------------------------------- C11-C14
arm("C11 state_of: a ref-pinned population is FROZEN",
    U.state_of(True, False), "FROZEN")
arm("C12 state_of: a disk glob without the observer is GROWING",
    U.state_of(False, False), "GROWING")
arm("C13 state_of: a disk glob WITH the observer is OBSERVED",
    U.state_of(False, True), "OBSERVED")
arm("C14 render_figure prints an INTERVAL for an OBSERVED figure",
    U.render_figure(1984, "OBSERVED", low=1966, ref="757f999"),
    "1966-1984 @757f999 (OBSERVED)")

# ---------------------------------------------------------------------------
print("  %-72s %s" % ("arm", "result"))
print("  " + "-" * 78)
for name, ok, got, want, note in CASES:
    print("  %-72s %s" % (name, "ok" if ok else "*** FAILED"))
    if not ok:
        print("        got  %r" % (got,))
        print("        want %r" % (want,))
    if note:
        print("        (%s)" % note)
print()
print("SELFTEST TOTAL BAD: %d" % BAD)
sys.exit(min(BAD, 120))
