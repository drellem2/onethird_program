#!/usr/bin/env python3
"""a5 — HOW THIS INSTRUMENT CAN FAIL, DEMONSTRATED.

mg-9876 states the trap this directory is standing in: "The instrument you build to audit the
controls is itself a control, and it will be validated by the same practice that produced the
three.  Say explicitly how you established that YOUR checker can fail.  If you cannot, say so
— an unfalsified auditor of unfalsified checks is the fourth instance."

a2, a3 and a4 each carry their own two-sided control over the thing they measure (a2 §3, a3
§5, a4 §4).  What is left is the machinery underneath a4, which those three do not touch: the
ANATOMY classifier and the RECORDER.  Both are planted here against worlds whose answer is
known in advance and typed out beside them.

§3 IS THE WORLD THAT MATTERS.  a4 rewrites source files in place, and several instruments in
this corpus read their own source.  §3 plants exactly that: a probe that notices it has been
rewritten and exits 3.  a4 is required to report the directory NOT-REACHED-BY-a4 with the
reason and to count NOTHING from it — including the answers the recorder had already
collected before the probe reached its exit.  An arm that quietly counted those would be
measuring itself and reporting the result as a fact about the tree, which is this ticket's
subject committed by its instrument.

D8, KEPT: my first version of that world pinned its own sha256, which is a FIXED POINT — the
pin is of the file the pin is inside — so it exited 3 on its own BASELINE, the two runs
agreed at 3, and the guard never fired.  A planted world that is broken before the mutation
cannot show anything, and it is mg-9876's C2 ("its good side was ALREADY DRIFTED so its
predicate could not fail") in my own selftest.  The marker is now assembled at run time.

EXIT 0 = every world answered as predicted.  EXIT 1 = at least one did not, and every verdict
in a4 that depends on the failing piece is withdrawn by a4 itself.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import liba397 as L  # noqa: E402
import a4_membership as A  # noqa: E402

# --------------------------------------------------------------------------------------
# the anatomy worlds: source, the line c9876's regex would report, and the answer required
# --------------------------------------------------------------------------------------
ANATOMY_WORLDS = [
    ("W1 a live membership test in an if",
     'def f(out):\n    if "8 9" in out:\n        return 1\n    return 0\n',
     2, "SITE", "branch"),
    ("W2 the same test spread over two lines — the SECOND line",
     'def f(out):\n    ok = ("8 9" in out\n          and "X" not in out)\n    return ok\n',
     3, "SECOND-LINE-OF", None),
    ("W3 the construction QUOTED inside a docstring",
     'def f(out):\n    """the old line read: if "8 9" in out:"""\n    return 0\n',
     2, "NOT-A-MEMBERSHIP-TEST", None),
    ("W4 the answer reaches a print and stops",
     'def f(out):\n    print("marker present:", "8 9" in out)\n    return 0\n',
     2, "SITE", "print"),
    ("W5 an assert",
     'def f(out):\n    assert "8 9" in out\n',
     2, "SITE", "assert"),
]


def anatomy_world(label, src, line, want_anat, want_role):
    tmp = tempfile.mkdtemp(prefix="a397_a5_")
    try:
        p = os.path.join(tmp, "probe.py")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(src)
        rec = A.anatomy([{"dir": "planted", "file": os.path.relpath(p, L.ROOT),
                          "line": line, "src": src.split("\n")[line - 1]}])[0]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    ok = rec["anatomy"] == want_anat and (want_role is None or rec["role"] == want_role)
    return ok, rec


# --------------------------------------------------------------------------------------
# the recorder worlds
# --------------------------------------------------------------------------------------
RECORDER_PROBE = '''
import sys
out = "the healthy report says all rows agree: 1 2 3 8 9 10"
hit_true = "8 9" in out
hit_false = "IMPOSSIBLE-NEEDLE-a397" in out
if hit_false:
    unreachable = "never" in out
print("done", hit_true, hit_false)
'''

RECORDER_RUNNER = '#!/bin/sh\ncd "$(dirname "$0")"\npython3 probe.py > out_probe.txt\n'

# A probe that NOTICES IT HAS BEEN REWRITTEN.  The marker is assembled at run time so the
# uninstrumented file does not contain it — a pinned sha256 would have been the more obvious
# construction and it is a FIXED POINT (the pin is of the file the pin is in), which is why
# the first version of this world exited 3 on its own baseline and the guard never fired.
SELF_DIGESTING = '''
import sys
src = open(__file__).read()
MARK = "_a39" + "7R"
out = "the report"
ok = "report" in out
if MARK in src:
    sys.exit(3)
print("not rewritten")
'''


def recorder_world():
    """Plant a directory, run it through a4's own measure_dir, and require the three answers.
    The directory lives inside code/ because measure_dir navigates by `code/<name>` and by
    git — planting it anywhere else would be testing a different function."""
    name = "_a397_planted_recorder"
    d = os.path.join(L.CODE, name)
    os.makedirs(d, exist_ok=True)
    sitedir = tempfile.mkdtemp(prefix="a397_site_")
    try:
        with open(os.path.join(sitedir, "sitecustomize.py"), "w", encoding="utf-8") as fh:
            fh.write(A.SITECUSTOMIZE)
        with open(os.path.join(d, "probe.py"), "w", encoding="utf-8") as fh:
            fh.write(RECORDER_PROBE)
        with open(os.path.join(d, "run_all.sh"), "w", encoding="utf-8") as fh:
            fh.write(RECORDER_RUNNER)
        seen, note = A.measure_dir(name, [os.path.join(d, "probe.py")], sitedir)
        return seen, note
    finally:
        shutil.rmtree(d, ignore_errors=True)
        shutil.rmtree(sitedir, ignore_errors=True)


def self_digest_world():
    """A file that notices it has been rewritten.  Instrumenting it inserts the recorder's
    name, the instrumented run exits 3 where the baseline exits 0, and a4 must refuse the
    directory rather than report the answers it collected before the exit."""
    name = "_a397_planted_selfdigest"
    d = os.path.join(L.CODE, name)
    os.makedirs(d, exist_ok=True)
    sitedir = tempfile.mkdtemp(prefix="a397_site_")
    try:
        with open(os.path.join(sitedir, "sitecustomize.py"), "w", encoding="utf-8") as fh:
            fh.write(A.SITECUSTOMIZE)
        p = os.path.join(d, "probe.py")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(SELF_DIGESTING)
        with open(os.path.join(d, "run_all.sh"), "w", encoding="utf-8") as fh:
            fh.write(RECORDER_RUNNER)
        return A.measure_dir(name, [p], sitedir)
    finally:
        shutil.rmtree(d, ignore_errors=True)
        shutil.rmtree(sitedir, ignore_errors=True)


def main():
    print("=" * 92)
    print("mg-a397 a5 — HOW THIS INSTRUMENT CAN FAIL, DEMONSTRATED")
    print("=" * 92)
    print()
    ok = True

    print("§1  THE ANATOMY CLASSIFIER, ON FIVE PLANTED FILES")
    print("-" * 92)
    for label, src, line, want_a, want_r in ANATOMY_WORLDS:
        good, rec = anatomy_world(label, src, line, want_a, want_r)
        ok = ok and good
        print(f"    {'ok ' if good else 'BROKEN'}  {label:52} -> {rec['anatomy']}"
              f"/{rec['role']}  (want {want_a}/{want_r})")
    print()

    print("§2  THE RECORDER, ON A PLANTED DIRECTORY a4 RUNS FOR ITSELF")
    print("-" * 92)
    print("    probe.py holds three membership tests whose answers are known: one TRUE on")
    print("    the healthy world, one FALSE, and one inside a branch that cannot be entered.")
    seen, note = recorder_world()
    print(f"    measure_dir note: {note}")
    got = {k.rsplit(":", 2)[1]: v for k, v in seen.items()}
    want = {"4": (1, 0), "5": (0, 1)}
    for line, expect in sorted(want.items()):
        have = got.get(line, "NEVER-REACHED")
        good = have == expect
        ok = ok and good
        print(f"      {'ok ' if good else 'BROKEN'}  probe.py:{line} answered "
              f"(true,false)={have} (want {expect})")
    unreached = "7" not in got
    ok = ok and unreached
    print(f"      {'ok ' if unreached else 'BROKEN'}  probe.py:7 NEVER-REACHED "
          f"(want NEVER-REACHED)")
    print()

    print("§3  THE WORLD WHERE INSTRUMENTING CHANGES THE RUN")
    print("-" * 92)
    print("    A probe that notices it has been rewritten.  The instrumented run exits 3")
    print("    where the baseline exits 0, and a4 must count NOTHING from that directory —")
    print("    including the one answer the recorder collected before the probe exited.")
    seen2, note2 = self_digest_world()
    good = (not seen2) and "instrumentation changed the run" in note2
    ok = ok and good
    print(f"      {'ok ' if good else 'BROKEN'}  note: {note2}")
    print(f"              answers counted: {len(seen2)} (want 0)")
    print()

    print("§4  WHAT THIS DIRECTORY DOES NOT ESTABLISH")
    print("-" * 92)
    print("    (1) a4 measures the check's answer on the HEALTHY world only.  FALSE-ON-GOOD")
    print("        says the check is not already satisfied; it does NOT say the check would")
    print("        fire.  Only a2 runs its subject both ways, and only over 19 sites.")
    print("    (2) POLARITY is read off the needle by a regex over words like FAIL and")
    print("        Traceback.  A negative-control expectation whose marker is an ordinary")
    print("        English phrase is read as POSITIVE and lands in CANNOT-TELL.  That is a")
    print("        conservative error and it is the reason CANNOT-TELL is large.")
    print("    (3) THE REGISTRY'S SUBJECT SENTENCES ARE NOT TOUCHED, for the reason c9876")
    print("        gives: a probe is written FROM the subject, so a subject that misdescribes")
    print("        its arm yields a probe that agrees with it.  Nothing here claims to")
    print("        settle that and nothing here should be read as having tried.")
    print()

    print("a5 RESULT: " + ("every planted world answered as predicted"
                           if ok else "AT LEAST ONE WORLD DID NOT ANSWER — see above"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
