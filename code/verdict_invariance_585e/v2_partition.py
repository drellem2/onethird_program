#!/usr/bin/env python3
"""mg-585e v2 — WHERE EXACTLY IS THE OSCILLATION?  Located by running, not by reading.

v1 counts the flips.  This arm asks which BYTES flip, and it answers by running the real
`g0_fixed_point.py` against sandbox repositories that differ in exactly one thing.

    green   a miniature repo whose one watched transcript is untouched.
    noise   the same, with only a wall-clock number moved in the worktree copy.
    red     the same, with a COUNT moved — a difference the normaliser must not forgive.

The arm run is the ONE IN code/gate_fixed_point_f771, copied into each sandbox and executed
as a subprocess.  Not re-implemented here: a re-spelling would make every line below a
statement about the re-spelling (mg-d2c2, and mg-f771's own g1 obeys the same rule by feeding
`verdict_for` rather than a copy of it).

WHY A SANDBOX AND NOT THIS REPOSITORY.  The question is "what does g0's stdout do when the
verdict changes", and changing the verdict in THIS repository means dirtying a real committed
transcript.  A sandbox makes the two trees differ in one controlled byte and makes the run
hermetic — no clock in the compared text except the one field, no dependence on what else
happens to be modified in the worktree at the moment the gate runs.

THE COMPARISON EATS DECIMAL SECONDS AND NOTHING ELSE, with `lib585e.scrub_seconds`, which is
written in this directory rather than imported from `lib_f771`.  Same shape, different file,
and the reason is in lib585e's docstring: an agreement test computed with the subject's own
normaliser is a consistency check wearing a measurement's clothes.

EXITS 0 if every partition lands where §3 says it must, 1 if any does not, 2 if a sandbox
could not be built.
"""

import difflib
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib585e as L  # noqa: E402

W = 92


def rule(ch="-"):
    print(ch * W)


def run_world(world):
    tmp = tempfile.mkdtemp(prefix="mg585e-%s-" % world)
    try:
        L.build_sandbox(tmp, world)
        return L.run_g0(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def split_at_section2(text):
    """Everything before the `§2` heading, and everything from it on.  §2 is where g0's own
    structure puts the outcome; the split is on that heading and not on a line number, so a
    prose edit above it does not silently move the boundary."""
    lines = text.splitlines(True)
    for i, ln in enumerate(lines):
        if ln.startswith("§2"):
            return "".join(lines[:i]), "".join(lines[i:])
    return text, ""


def main():
    print("=" * W)
    print("mg-585e v2  WHERE THE OSCILLATION LIVES — the real g0, run against controlled trees")
    print("=" * W)
    print()

    try:
        results = {w: run_world(w) for w in ("green", "noise", "red")}
        # A second run of the green world, on a FRESH sandbox, to separate verdict-dependence
        # from run-to-run jitter.  Without it, "the two stdouts differ" cannot be attributed.
        green2 = run_world("green")
    except L.Refused as exc:
        print("REFUSED — %s" % exc)
        return 2

    print("§1  THE THREE TREES AND WHAT g0 SAID ABOUT THEM")
    rule()
    print("  Identical repositories but for one line of one watched transcript.")
    print()
    print("  %-8s %-6s %s" % ("tree", "exit", "the verdict line g0 printed (seconds scrubbed)"))
    for w in ("green", "noise", "red"):
        rc, out, _ = results[w]
        verdict = [ln for ln in out.splitlines() if ln.startswith("VERDICT")]
        # SCRUBBED BEFORE IT IS PRINTED, and this line is the reason this arm exists.  The
        # first draft printed g0's verdict line verbatim, wall clock and all, and THIS
        # TRANSCRIPT FAILED TO REPRODUCE ON ITS SECOND RUN (`0.03s` -> `0.04s`) — mg-f771's
        # own README D4 happening again inside the directory that is describing it.  Caught by
        # running the suite twice and comparing, not by reading.
        print("  %-8s %-6d %s"
              % (w, rc, L.scrub_seconds(verdict[0] if verdict else "(none)")[:66]))
    print()

    failures = []

    # C-positive: the sandbox must actually produce the verdicts it claims to, or every
    # agreement below is agreement between two greens and says nothing.
    if results["red"][0] != 1 or results["green"][0] != 0 or results["noise"][0] != 0:
        failures.append("the sandboxes did not produce the verdicts they exist to produce")

    print("§2  RUN-TO-RUN JITTER ON A FIXED TREE")
    rule()
    a, b = results["green"][1], green2[1]
    same_raw = a == b
    same_scrubbed = L.scrub_seconds(a) == L.scrub_seconds(b)
    # WHETHER THE RAW BYTES MATCHED GOES TO STDERR AND NOT HERE.  It is a function of whether
    # two runs happened to round to the same hundredth of a second, which is the definition of
    # not-repo-state, and putting it in a tracked file made this arm fail to reproduce on its
    # second run.  README D4's remedy, applied to the arm that quotes README D4.
    sys.stderr.write("mg-585e v2: two green sandboxes, raw stdout identical: %s\n"
                     % ("yes" if same_raw else "no"))
    print("  two independent green sandboxes, stdout identical after decimal")
    print("  seconds are scrubbed                                           %s"
          % ("YES" if same_scrubbed else "NO"))
    if not same_scrubbed:
        failures.append("green stdout is not stable across two runs even after scrubbing")
        for ln in list(difflib.unified_diff(L.scrub_seconds(a).splitlines(),
                                            L.scrub_seconds(b).splitlines(),
                                            lineterm="", n=0))[:12]:
            print("      %s" % ln[:86])
    print()
    print("  This is the control that makes §3 attributable.  Whatever moves between the red")
    print("  and green trees moves BECAUSE of the verdict, not because two runs of anything")
    print("  differ.")
    print()

    print("§3  RED AGAINST GREEN — WHICH PART OF THE TRANSCRIPT MOVED")
    rule()
    red_out = L.scrub_seconds(results["red"][1])
    green_out = L.scrub_seconds(results["green"][1])
    noise_out = L.scrub_seconds(results["noise"][1])

    r_head, r_tail = split_at_section2(red_out)
    g_head, g_tail = split_at_section2(green_out)

    head_same = r_head == g_head
    tail_same = r_tail == g_tail
    print("  everything up to the §2 heading is identical                    %s"
          % ("YES" if head_same else "NO"))
    print("  §2 onward is identical                                          %s"
          % ("yes" if tail_same else "NO — this is the oscillation"))
    if not head_same:
        failures.append("the verdict leaks above §2 — the oscillation is wider than §2")
        for ln in list(difflib.unified_diff(g_head.splitlines(), r_head.splitlines(),
                                            lineterm="", n=0))[:12]:
            print("      %s" % ln[:86])
    if tail_same:
        # THE SURFACE THIS ARM WAS BUILT TO LOCATE IS GONE, AND THAT IS NOT THIS ARM FAILING.
        # It used to read an unmoved §2 as proof that the sandbox was vacuous.  It cannot be:
        # the C-positive check in §1 requires the three trees to return exit 1 / 0 / 0 and
        # they do, so the VERDICT really did change and the TEXT did not.  mg-c15e deleted
        # lib_f771.SELF_EXCLUDED and replaced g0's §2 with the normaliser's rule inventory, so
        # the transcript no longer records the outcome at all.  REPORTED AND NOT GRADED: a
        # suite that goes red when its own recommendation is adopted is mg-e35b's
        # red-on-improvement shape wearing this directory's clothes.
        print("  ⚠ §2 DID NOT MOVE, AND THE SANDBOX IS NOT VACUOUS — the three trees returned")
        print("    exit 1 / 0 / 0 as §1 requires, so the verdict moved and the text did not.")
        print("    THE OSCILLATING SURFACE THIS ARM LOCATED HAS BEEN REMOVED: mg-c15e deleted")
        print("    the self-exemption and made §2 the rule inventory, which is the change")
        print("    this directory exhibited and priced.  The question §6 put to pm-onethird")
        print("    is answered, and this line is the measurement that says so.")
    print()
    print("  head lines %d, and they are %s" % (len(g_head.splitlines()),
                                                 "identical" if head_same else "NOT identical"))
    print("  §2 onward: green %d line(s), red %d line(s)"
          % (len(g_tail.splitlines()), len(r_tail.splitlines())))
    print()

    print("  THE GREEN TREE AND THE NOISE TREE AGREE, WHICH IS THE OTHER HALF.  A watched")
    print("  transcript that moved but says the same thing must produce the same stdout as one")
    print("  that did not move at all, or the file would oscillate on wall-clock too.")
    print("  green stdout == noise stdout (seconds scrubbed)                 %s"
          % ("YES" if green_out == noise_out else "NO"))
    if green_out != noise_out:
        failures.append("green and noise trees produce different stdout")
    print()

    print("§4  WHAT THE PARTITION SAYS")
    rule()
    print("  The transcript splits cleanly in two and the split is g0's own §-boundary:")
    print()
    print("    §1  the watched class, the exemption, the two declared noise families")
    print("        (⚠ AS g0 STOOD WHEN THIS WAS MEASURED.  mg-c15e deleted the exemption and")
    print("         moved the outcome to the exit status, so today BOTH sections are a")
    print("         function of the instrument and §3 above reports the surface as gone.)")
    print("        — a function of the INSTRUMENT.  Invariant under the repair.")
    print("    §2  the disagreement set and the VERDICT line")
    print("        — a function of the DIFFERENCE between the committed tree and the fresh")
    print("          one, which is exactly what the repair sets to empty.")
    print()
    print("  So the oscillating part is not 'the part that depends on the verdict' in general;")
    print("  it is the part that reports a quantity THE COMMIT ITSELF ZEROES.  g0's docstring")
    print("  rule — 'only the DISAGREES list, which is repo state, is on stdout' — picks the")
    print("  wrong test: the DISAGREES list IS repo state, of the tree BEFORE the repair, and")
    print("  the file is committed into the tree AFTER it.")
    print()

    if failures:
        print("VERDICT: RED — %d partition claim(s) did not hold." % len(failures))
        for f in failures:
            print("    %s" % f)
        return 1
    # THE VERDICT LINE SAYS WHAT THIS RUN MEASURED AND NOT WHAT THE FIRST RUN DID.  It read
    # `the oscillation is confined to §2 and the VERDICT line` unconditionally, which is a
    # finding hard-coded as a conclusion — and on a tree where the surface has been removed it
    # is a sentence about a state of the instrument nobody can reach any more.  mg-2959's
    # subject, in the directory that quotes mg-2959.
    if tail_same:
        print("VERDICT: GREEN — §2 DOES NOT MOVE WITH THE VERDICT ANY MORE.  The surface this")
        print("  arm located is gone: mg-c15e deleted the self-exemption and made §2 the rule")
        print("  inventory, and the whole transcript is now invariant under the repair.")
    else:
        print("VERDICT: GREEN — the oscillation is confined to §2 and the VERDICT line, and the")
        print("  rest of the transcript is already invariant.")
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
