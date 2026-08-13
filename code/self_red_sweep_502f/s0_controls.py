#!/usr/bin/env python3
"""mg-502f — THE PLANTED WORLDS.  Does the detector detect, does the guard refuse, and is
the mechanism they are about real?

THREE FAMILIES, and the first is the one that matters most, because a sweep that reports
GREEN is only worth the demonstration that it can report RED.

  M  THE MECHANISM.  Not asserted — computed, with mg-f771's OWN decision function.
     `lib_f771.verdict_for(committed, worktree)` is the thing that grades every tracked
     transcript on every merge, and f771 isolated it on purpose so that controls could
     exercise it without a repository ("isolated so that `g1_controls.py` tests THIS and
     not a re-spelling").  M1-M3 hand it the real committed bytes of a real transcript
     against the states a shell redirect actually leaves that file in.
  D  THE DETECTOR.  Eight sources it must classify, five of them shapes that a real
     instance had and an earlier draft of the rules missed.
  G  THE GUARD.  Real file descriptors, a real repository, five worlds.

EXITS 0 if every world scored as required, 1 if one did not, 2 if this arm broke.
"""

import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib_502f as L      # noqa: E402
import guard_502f as G    # noqa: E402
sys.path.insert(0, os.path.join(L.ROOT, "code", "gate_fixed_point_f771"))
import lib_f771 as F      # noqa: E402

W = 92
ROWS = []


def rule(ch="-"):
    print(ch * W)


def score(tag, claim, got, want):
    ok = got == want
    ROWS.append((tag, ok))
    print("  %-5s %-58s %-11s %s"
          % (tag, claim[:58], str(got)[:11], "AS REQUIRED" if ok else "*** FAILED ***"))
    if not ok:
        print("        wanted %r, got %r" % (want, got))
    return ok


# ------------------------------------------------------------------ D: planted sources

SRC_ONE_HOP = '''
import subprocess, os
ROOT = "/repo"
def go(cmd):
    return subprocess.run(cmd, capture_output=True)
def main():
    return go(["sh", os.path.join(ROOT, "build.sh")])
'''

SRC_DIRECT = '''
import subprocess
subprocess.run(["sh", "build.sh"])
'''

SRC_PROSE = '''
"""This module explains that ./build.sh is the gate."""
import subprocess
def f():
    print("run ./build.sh yourself")
    subprocess.run(["git", "status"])
'''

SRC_DOCSTRING_ONLY = '''
"""./build.sh is named here and nowhere else."""
def f():
    return 1
'''

SRC_SELF_WRITER = '''
import subprocess, io, sys
def main():
    subprocess.run(["sh", "build.sh"])
def go():
    buf = io.StringIO(); sys.stdout = buf
    main()
    with open("out_w.txt", "w") as fh:
        fh.write(buf.getvalue())
'''

SRC_GUARDED = SRC_SELF_WRITER + '''
import guard_502f
guard_502f.refuse_if_self_red("w.py")
'''

SRC_HANDSHAKE = '''
import subprocess
subprocess.run(["sh", "g.sh"], env={"BUILD_SH_RAN_THE_SUITES": "1"})
'''

SRC_BROKEN = 'def f(:\n    pass\n'


def main():
    t0 = time.time()
    print("=" * W)
    print("mg-502f  PLANTED WORLDS — the mechanism, the detector, the guard")
    print("=" * W)
    print()

    # ------------------------------------------------------------------ M
    print("§M  THE MECHANISM, COMPUTED WITH mg-f771's OWN DECISION FUNCTION")
    rule()
    print("  A shell redirect opens its target BEFORE the process starts.  So during a run")
    print("  of `python3 s.py > code/d/out_s.txt` that file is first EMPTY and then PARTIAL,")
    print("  and `./build.sh` ends by grading it.  These rows hand f771's real")
    print("  `verdict_for(committed, worktree)` the real committed bytes of a real tracked")
    print("  transcript against exactly those two states.  Nothing is simulated and nothing")
    print("  is asserted: DISAGREES here IS the gate exiting 1.")
    print()
    # THE VICTIM IS A TRANSCRIPT THIS BRANCH DOES NOT TOUCH, and the first choice was one it
    # did.  `out_x0_exhibit.txt` is repaired by this very commit, so §M's byte count moved
    # whenever that file did and this arm's transcript moved with it — a control coupled to
    # its own branch's edits.  mg-f771's `out_g1_controls.txt` is the opposite: f771's own
    # comment records that its content depends on the PLANTED WORLDS and not on tree state,
    # which is why f771 declines to exempt it from its own watched class.  That is exactly
    # the stability §M needs, borrowed from the file that argues for it.
    victim = "code/gate_fixed_point_f771/out_g1_controls.txt"
    # THE COMMITTED BYTES, VIA f771's OWN READER, AND NOT THE WORKTREE COPY.  The worktree
    # copy is rewritten by every gate run and moves in the timing family f771 declares
    # NOISE, so a byte count taken from it moves with a rounded decimal and drags this
    # arm's own transcript with it.  The committed copy is also the correct half of the
    # comparison on its own terms: it is exactly the side `verdict_for` grades against.
    committed = F.committed_text(victim)
    partial = "".join(committed.splitlines(keepends=True)[:len(committed.splitlines()) // 3])
    print("  victim: %s  (%d lines, %d bytes)"
          % (victim, len(committed.splitlines()), len(committed.encode("utf-8"))))
    print()
    score("M1", "EMPTY — the instant the shell opens the redirect",
          F.verdict_for(committed, ""), "DISAGREES")
    score("M2", "PARTIAL — the file while the script is still running",
          F.verdict_for(committed, partial), "DISAGREES")
    score("M3", "UNTOUCHED — the control.  No redirect, no disagreement",
          F.verdict_for(committed, committed), "AGREES")
    print()
    print("  M3 IS NOT DECORATION.  Without it M1 and M2 are consistent with a function")
    print("  that returns DISAGREES for everything, which would make this whole ticket a")
    print("  report about a broken grader rather than about a broken invocation.")
    print()

    # ------------------------------------------------------------------ D
    print("§D  THE DETECTOR — eight sources it must classify")
    rule()
    print("  D1-D3 are shapes an EARLIER DRAFT OF THESE RULES GOT WRONG, kept as worlds so")
    print("  the rule cannot silently return to the version that missed a live instance.")
    print()

    def edge(src):
        lits, execs = L.py_gate_edge(src)
        return bool(lits) and bool(execs)

    score("D1", "ONE HOP: argv built, handed to a local helper (x1's shape)",
          edge(SRC_ONE_HOP), True)
    score("D2", "DIRECT: subprocess.run([\"sh\", \"build.sh\"]) (x0's shape)",
          edge(SRC_DIRECT), True)
    score("D3", "PROSE: gate only ever PRINTED, something else executed",
          edge(SRC_PROSE), False)
    score("D4", "DOCSTRING ONLY: no code literal, no exec — NOT an edge",
          edge(SRC_DOCSTRING_ONLY), False)
    score("D5", "SELF-WRITER is recognised as writing its own transcript",
          L.self_writes(SRC_SELF_WRITER, "code/d/out_w.txt"), True)
    score("D6", "A NON-WRITER is not mistaken for one",
          L.self_writes(SRC_DIRECT, "code/d/out_w.txt"), False)
    score("D7", "A GUARDED script is recognised as guarded",
          L.calls_guard(SRC_GUARDED), True)
    score("D8", "AN UNGUARDED self-writer is NOT",
          L.calls_guard(SRC_SELF_WRITER), False)
    print()
    print("  D9-D12  THE BINDING RULES, on a planted tracked set.  Each rule below caught an")
    print("  instance the rule before it missed, which is why there are three and not one.")
    print()
    planted = {"code/d/out_w.txt", "code/d/out_other.txt", "code/d/w.py", "code/d/README.md",
               "code/d/run_all.sh"}
    b_name = L.bindings("code/d/w.py", planted, {})
    score("D9", "NAME: code/d/w.py <-> code/d/out_w.txt",
          b_name, [("code/d/out_w.txt", "NAME")])
    b_arrow = L.bindings("code/d/v.py", planted,
                         {"code/d/README.md": "| `v.py` -> `out_other.txt` | the demo |"})
    score("D10", "ARROW: a README table row (x1's binding, and its ONLY one)",
          b_arrow, [("code/d/out_other.txt", "ARROW")])
    b_red = L.bindings("code/d/u.py", planted,
                       {"code/d/run_all.sh": "python3 -u u.py > out_other.txt 2>&1"})
    score("D11", "REDIRECT: a literal redirect in a runner",
          b_red, [("code/d/out_other.txt", "REDIRECT")])
    b_untracked = L.bindings("code/d/t.py", planted,
                             {"code/d/README.md": "t.py -> out_nowhere.txt"})
    score("D12", "AN UNTRACKED TARGET IS NOT A BINDING — f771 grades tracked files",
          b_untracked, [])
    print()
    print("  D13  A FILE THIS INSTRUMENT CANNOT PARSE MUST BE REPORTED, NOT SKIPPED.")
    try:
        L.py_gate_edge(SRC_BROKEN)
        broke = False
    except SyntaxError:
        broke = True
    score("D13", "an unparseable source raises rather than returning 'no edge'", broke, True)
    print()
    print("  D16-D18  THE ROUTE EXEMPTION, HELD TO ITS DECLARED SIZE.  §0 does not ask two")
    print("  directories whether they are a second route to f771, and an exemption that can")
    print("  widen silently is the unfalsifiable escape hatch lib_f771's own docstring names")
    print("  about its normaliser.  These three rows are what stops it widening.")
    exempt_route = {"code/self_red_sweep_502f/z.py":
                    'import os\nH = "BUILD_SH_RAN_THE_SUITES"\n'}
    outside_route = {"code/somewhere_else_9999/z.py":
                     'import os\nH = "BUILD_SH_RAN_THE_SUITES"\n'}
    score("D16", "the exemption is EXACTLY the two declared directories",
          L.ROUTE_EXEMPT,
          ("code/gate_fixed_point_f771/", "code/self_red_sweep_502f/"))
    score("D17", "a route planted OUTSIDE them is still caught",
          [r for r, _, _ in L.handshake_setters(outside_route)],
          ["code/somewhere_else_9999/z.py"])
    score("D18", "a route planted INSIDE one of them is suppressed",
          L.handshake_setters(exempt_route), [])
    print()
    print("  D14  THE PREFILTER CANNOT CHANGE A VERDICT — it is strictly weaker than both")
    print("  rules, so anything it drops could not have been an edge or a route.")
    score("D14", "a source with no gate literal anywhere is dropped",
          L.mentions("import os\nos.getcwd()\n"), False)
    score("D15", "a source that names the handshake is KEPT even with no gate literal",
          L.mentions(SRC_HANDSHAKE), True)
    print()

    # ------------------------------------------------------------------ G
    print("§G  THE GUARD — real file descriptors, this real repository")
    rule()
    print("  The guard asks whether stdout IS a tracked transcript, by INODE and not by")
    print("  path string, because `> out_s.txt` from the directory and `> code/d/out_s.txt`")
    print("  from the root are one situation.")
    print()
    tracked_one = os.path.join(L.ROOT, victim)
    with open(tracked_one, "r+") as fh:                     # opened WITHOUT truncating
        score("G1", "stdout IS a tracked transcript -> the guard names it",
              G.stdout_transcript(stream=fh), victim)
    other = os.path.join(L.ROOT, "code", "state_ratchet_e331", "out_x1_positive.txt")
    with open(other, "r+") as fh:
        score("G2", "a DIFFERENT tracked transcript is named, not the first",
              G.stdout_transcript(stream=fh), "code/state_ratchet_e331/out_x1_positive.txt")
    tmpd = tempfile.mkdtemp(prefix="502f-g-")
    untracked = os.path.join(L.ROOT, "code", "self_red_sweep_502f", ".out_untracked.txt")
    try:
        with open(untracked, "w") as fh:
            score("G3", "an UNTRACKED out_*.txt under code/ is NOT refused",
                  G.stdout_transcript(stream=fh), None)
    finally:
        os.unlink(untracked)
    with open(os.path.join(tmpd, "out_elsewhere.txt"), "w") as fh:
        score("G4", "a file outside the repository is NOT refused",
              G.stdout_transcript(stream=fh), None)
    with open(os.devnull, "w") as fh:
        score("G5", "a character device (/dev/null, a tty) is NOT refused",
              G.stdout_transcript(stream=fh), None)
    p = subprocess.Popen([sys.executable, "-c", "pass"], stdout=subprocess.PIPE)
    try:
        score("G6", "a PIPE is NOT refused — and CANNOT be; §3 declares it",
              G.stdout_transcript(stream=p.stdout), None)
    finally:
        p.stdout.close()
        p.wait()
    print()
    print("  G7  THE REFUSAL ITSELF FIRES, END TO END, AT EXIT 2.  A live subprocess whose")
    print("  stdout is a real tracked transcript, opened in APPEND so the world does not")
    print("  destroy the file it borrows.")
    probe = ("import sys, os\n"
             "sys.path.insert(0, %r)\n"
             "import guard_502f\n"
             "guard_502f.refuse_if_self_red('probe.py')\n"
             "print('REACHED THE BODY')\n" % HERE)
    with open(tracked_one, "a") as fh:
        r = subprocess.run([sys.executable, "-c", probe], stdout=fh,
                           stderr=subprocess.PIPE, text=True, cwd=L.ROOT)
    size_after = os.path.getsize(tracked_one)
    score("G7", "the guarded probe exits 2 rather than running", r.returncode, 2)
    score("G8", "and the refusal says which file, on stderr",
          victim in r.stderr, True)
    score("G9", "and the borrowed transcript is unchanged (append, nothing written)",
          size_after, len(committed.encode("utf-8")))
    print()
    if size_after != len(committed.encode("utf-8")):
        with open(tracked_one, "w", encoding="utf-8") as fh:
            fh.write(committed)
        print("  *** the borrowed transcript was restored from memory ***")
        print()

    print("§V  VERDICT")
    rule()
    bad = [t for t, ok in ROWS if not ok]
    for tag, ok in ROWS:
        if not ok:
            print("  FAILED: %s" % tag)
    if bad:
        print()
        print("VERDICT: RED — %d of %d worlds did not score as required.  %.2fs"
              % (len(bad), len(ROWS), time.time() - t0))
        return 1
    print("  %d of %d worlds scored as required." % (len(ROWS), len(ROWS)))
    print()
    print("VERDICT: GREEN — the mechanism is real, the detector detects, the guard refuses.")
    print("  %.2fs" % (time.time() - t0))
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
