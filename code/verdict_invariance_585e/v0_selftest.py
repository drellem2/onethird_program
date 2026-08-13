#!/usr/bin/env python3
"""mg-585e v0 — CONTROLS.  Can this directory's instruments fire, and where are they blind?

IT RUNS LAST AND NOT FIRST, which is the opposite of every other selftest in this estate, and
the reason is section 4: one of the controls scans the transcripts the other three arms have
just written for an absolute path.  A control that reads the PREVIOUS run's transcripts is
grading a tree nobody is about to commit.  Running last costs the property that a broken
library is caught before the arms use it — and that cost is bought back cheaply, because the
arms catch their own exceptions and print the traceback into their own transcripts, so a
broken library is loud rather than silent either way.

FOUR GROUPS:

  MUST FIRE      planted defects in THIS directory's own library.  Three of them are the
                 failure modes that would make v3's headline claim vacuous rather than wrong,
                 which is the direction that does not announce itself.

  MUST NOT FIRE  the wrong-direction worlds.  `scrub_seconds` must leave INTEGERS alone: if it
                 ate them, v2's "the two runs agree" would be agreement produced by the
                 scrubber and every count in every compared transcript would be invisible.

  REFUSE         worlds in which no verdict is available.  A sandbox that is not a git
                 repository must make the arm say so, not say nothing-is-wrong.

  THE OWN-OUTPUT SCAN  no absolute path under any checkout root may appear in a transcript
                 this directory commits.  mg-f771's whole subject is a worktree path reaching
                 a tracked file; a directory that shipped one while describing it would be
                 the joke this corpus keeps telling at its own expense.

EXITS 0 if every world lands where it must, 1 if any does not, 2 if a world could not be set
up at all.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib585e as L  # noqa: E402

W = 92
HERE = os.path.dirname(os.path.abspath(__file__))

# (id, text, expected-after-scrub, what)
SCRUB_WORLDS = [
    ("N1", "VERDICT: GREEN — 0 disagreements.  0.10s",
     "VERDICT: GREEN — 0 disagreements.  <t>s",
     "a decimal second is eaten — the one field two runs of a fixed tree differ in"),
    ("N2", "  recompute 36.4s · falsification 0.55 s · total 37.0s",
     "  recompute <t>s · falsification <t>s · total <t>s",
     "every decimal second on a line, including the spaced spelling"),
    ("N3", "VERDICT: GREEN — 20 entries", "VERDICT: GREEN — 20 entries",
     "AN INTEGER IS NOT A SECOND — the count that opened mg-f771 must survive"),
    ("N4", "  10.5seconds elapsed", "  10.5seconds elapsed",
     "`s` must be a whole token — `10.5seconds` is not a timing field"),
    ("N5", "  bytes             138325", "  bytes             138325",
     "STATE.md's byte count is repo state and must not be scrubbed away"),
]
MUST_NOT_FIRE = {"N3", "N4", "N5"}


def rule(ch="-"):
    print(ch * W)


def planted():
    """Defects planted in this directory's own library.  Each returns (id, what, outcome, ok).

    THE REMEDY IS AN ARTIFACT OF THE SAME KIND AS THE DEFECT.  This directory's claim is that
    a report of the verdict's INPUTS is safe; these three plants are the ways that claim could
    be true of a report that is reading nothing.
    """
    out = []

    # D1 — a deciding function disappears.  The digest must REFUSE rather than silently
    # cover three functions instead of four, which would be a narrower digest reporting the
    # same field name: a widening of the escape hatch that the digest was added to close.
    tmp = tempfile.mkdtemp(prefix="mg585e-d1-")
    try:
        L.build_sandbox(tmp, "green",
                        normaliser_patch=("def verdict_for(", "def verdict_for_RENAMED("))
        try:
            L.read_inputs(tmp)
            out.append(("D1", "a deciding function is renamed away", "returned a digest", False))
        except L.Refused:
            out.append(("D1", "a deciding function is renamed away", "REFUSED", True))
    except L.Refused as exc:
        out.append(("D1", "a deciding function is renamed away", "setup failed: %s" % exc, None))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # D2 — a constant in the readable inventory disappears.  Same failure mode one level up:
    # an inventory that quietly lists four of five rules is an inventory that cannot be read
    # as complete, and completeness is the only thing it is for.
    tmp = tempfile.mkdtemp(prefix="mg585e-d2-")
    try:
        L.build_sandbox(tmp, "green",
                        normaliser_patch=("\nSECONDS = re.compile", "\n_SECONDS = re.compile"))
        try:
            L.read_inputs(tmp)
            out.append(("D2", "an inventory constant is renamed away", "returned an inventory",
                        False))
        except L.Refused:
            out.append(("D2", "an inventory constant is renamed away", "REFUSED", True))
    except L.Refused as exc:
        out.append(("D2", "an inventory constant is renamed away", "setup failed: %s" % exc,
                    None))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # D3 — the sandbox's RED tree stops being red.  If the builder ever produced a tree the
    # real g0 grades green, v2 and v3 would compare two greens and report agreement.  So the
    # plant makes the red tree differ only in a TIMING, which the normaliser forgives, and
    # requires the resulting verdict to be green — i.e. it demonstrates that the difference
    # v2 and v3 rely on is doing the work, rather than asserting that it is.
    tmp = tempfile.mkdtemp(prefix="mg585e-d3-")
    try:
        L.build_sandbox(tmp, "noise")
        rc, _, _ = L.run_g0(tmp)
        ok = rc == 0
        out.append(("D3", "the red tree's difference is only a timing",
                    "g0 exit %d (green expected)" % rc, ok))
    except L.Refused as exc:
        out.append(("D3", "the red tree's difference is only a timing",
                    "setup failed: %s" % exc, None))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # D4 — the pin.  A window measured from a commit that does not resolve, or that is not
    # reachable from origin/main, is a window nobody else can re-open.
    try:
        L.require_as_of()
        out.append(("D4", "AS_OF resolves and is an ancestor of origin/main", "ok", True))
    except L.Refused as exc:
        out.append(("D4", "AS_OF resolves and is an ancestor of origin/main", str(exc)[:44],
                    False))

    return out


def refusals():
    out = []

    # R1 — a tree that is not a git repository.  g0 reads the committed copy from git; without
    # one there is nothing to compare and a green would be manufactured out of nothing.
    tmp = tempfile.mkdtemp(prefix="mg585e-r1-")
    try:
        dst = os.path.join(tmp, "code", "gate_fixed_point_f771")
        os.makedirs(dst)
        for name in ("lib_f771.py", "g0_fixed_point.py"):
            shutil.copyfile(os.path.join(L.F771_DIR, name), os.path.join(dst, name))
        rc, out_txt, _ = L.run_g0(tmp)
        out.append(("R1", "sandbox is not a git work tree", "g0 exit %d" % rc,
                    rc == 2 and "REFUSED" in out_txt))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # R2 — an unknown world.  A typo in a world name must not silently build the green tree
    # and report on it, because every finding in v2 and v3 is a comparison BETWEEN worlds.
    tmp = tempfile.mkdtemp(prefix="mg585e-r2-")
    try:
        try:
            L.build_sandbox(tmp, "reed")
            out.append(("R2", "an unknown world name", "built something", False))
        except L.Refused:
            out.append(("R2", "an unknown world name", "REFUSED", True))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # R3 — the freshness handshake, checked on the copy this directory actually runs.  v2 and
    # v3 set it; if it were ever unset every sandbox run would be a refusal and both arms
    # would be comparing two identical refusal messages and calling them agreement.
    env = dict(os.environ)
    env.pop(L.FRESH_ENV, None)
    tmp = tempfile.mkdtemp(prefix="mg585e-r3-")
    try:
        L.build_sandbox(tmp, "red")
        arm = os.path.join(tmp, "code", "gate_fixed_point_f771", "g0_fixed_point.py")
        p = subprocess.run([sys.executable, arm], capture_output=True, text=True, env=env)
        out.append(("R3", "no %s handshake" % L.FRESH_ENV, "exit %d" % p.returncode,
                    p.returncode == 2 and "REFUSED" in p.stdout))
    except L.Refused as exc:
        out.append(("R3", "no %s handshake" % L.FRESH_ENV, "setup failed: %s" % exc, None))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    return out


ABS_PATH = re.compile(r"/(?:Users|home|var|private|tmp|opt)/[^\s:'\"]*")


def own_output_scan():
    """No absolute path may reach a transcript this directory commits.

    Reads the three transcripts the other arms have just written.  The line count is printed
    beside the verdict so that a scan which found nothing because it READ nothing cannot pass
    — asof_census's P26 discipline, and the reason it exists there is that permuted.py had to
    repair exactly this in itself.
    """
    rows = []
    for name in ("out_v1_oscillation.txt", "out_v2_partition.txt", "out_v3_invariant.txt"):
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            rows.append((name, None, 0, "NOT PRESENT — this arm ran before the others"))
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        hits = ABS_PATH.findall(text)
        rows.append((name, not hits, len(text.splitlines()),
                     "clean" if not hits else "%d absolute path(s): %s" % (len(hits), hits[0])))
    return rows


def main():
    print("=" * W)
    print("mg-585e v0  CONTROLS — what these instruments catch, and what they are blind to")
    print("=" * W)
    print()

    bad = 0
    setup_failed = 0

    print("§1  THE SCRUBBER — TWO WORLDS IT MUST EAT, THREE IT MUST NOT")
    rule()
    print("  `scrub_seconds` is the only normalisation v2 applies.  Widen it and v2's")
    print("  agreement is produced by the scrubber; narrow it and v2 is red on every host.")
    print()
    for wid, text, expect, what in SCRUB_WORLDS:
        got = L.scrub_seconds(text)
        ok = got == expect
        if not ok:
            bad += 1
        direction = "  <- MUST NOT FIRE" if wid in MUST_NOT_FIRE else ""
        print("  %-4s %-9s %s%s" % (wid, "ok" if ok else "**WRONG**", what, direction))
        if not ok:
            print("       expected %r" % expect)
            print("       got      %r" % got)
    print()
    print("  IT IS NOT INDEPENDENT IN SHAPE FROM lib_f771's N2 AND THAT IS NOT CLAIMED.")
    print("  There is one obvious regex for `a decimal followed by s`; both files hold it.")
    print("  What a separate file buys is that widening N2 cannot widen this arm's agreement")
    print("  test as a side effect.  It buys nothing else.")
    print()

    print("§2  PLANTED DEFECTS IN THIS DIRECTORY'S OWN LIBRARY")
    rule()
    print("  Three of the four are ways v3's claim could be VACUOUS rather than wrong, which")
    print("  is the direction that reports green.")
    print()
    for did, what, outcome, ok in planted():
        if ok is None:
            setup_failed += 1
            tag = "SETUP FAILED"
        elif ok:
            tag = "CAUGHT" if did in ("D1", "D2") else "ok"
        else:
            tag = "**INERT**"
            bad += 1
        print("  %-4s %-44s %-30s %s" % (did, what, outcome[:30], tag))
    print()

    print("§3  WORLDS IN WHICH NO VERDICT IS AVAILABLE")
    rule()
    print("  A control that cannot say 'I could not tell' says 'nothing is wrong' instead.")
    print()
    for rid, what, outcome, ok in refusals():
        if ok is None:
            setup_failed += 1
            tag = "SETUP FAILED"
        elif ok:
            tag = "ok"
        else:
            tag = "**WRONG**"
            bad += 1
        print("  %-4s %-40s %-24s %s" % (rid, what, outcome[:24], tag))
    print()

    print("§4  THE OWN-OUTPUT SCAN")
    rule()
    print("  mg-f771's subject is a worktree path reaching a tracked file.  A directory that")
    print("  shipped one while describing it would be the defect it is reporting.")
    print()
    scanned = 0
    for name, clean, nlines, note in own_output_scan():
        if clean is None:
            setup_failed += 1
            tag = "SETUP FAILED"
        elif clean:
            tag = "ok"
            scanned += 1
        else:
            tag = "**WRONG**"
            bad += 1
        print("  %-26s %5d line(s)  %-10s %s" % (name, nlines, tag, note[:34]))
    print()
    print("  %d transcript(s) actually read.  A scan that found nothing because it read" % scanned)
    print("  nothing must not read as clean, which is why that number is here.")
    print()

    print("§5  WHAT IS NOT COVERED HERE")
    rule()
    print("  The sandboxes hold ONE watched transcript.  Nothing above says what g0 does when")
    print("  several disagree at once, and nothing needs to: v3's claim is that the proposed")
    print("  report does not mention them AT ALL, so its output is the same for one as for")
    print("  twenty.  That is an argument and not a measurement, and it is named as one.")
    print()
    print("  Nothing here runs the proposed report inside `code/gate_fixed_point_f771`.  This")
    print("  directory demonstrates and prices a change to another ticket's instrument; it")
    print("  does not make it.  README §6.")
    print()

    if setup_failed:
        print("VERDICT: REFUSED — %d world(s) could not be set up.  %d others landed wrong."
              % (setup_failed, bad))
        return 2
    if bad:
        print("VERDICT: RED — %d world(s) landed in the wrong place." % bad)
        return 1
    print("VERDICT: GREEN — %d scrubber worlds, 4 plants, 3 refusals and the own-output scan "
          "all land where they must." % len(SCRUB_WORLDS))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except BaseException:                                   # noqa: BLE001 - deliberate
        import traceback
        print()
        print("REFUSED — this arm crashed and therefore reached no verdict:")
        traceback.print_exc(file=sys.stdout)
        sys.exit(2)
