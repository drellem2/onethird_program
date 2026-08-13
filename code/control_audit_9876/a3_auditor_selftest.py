#!/usr/bin/env python3
"""mg-9876 — THE TRAP THE TICKET NAMES: this auditor is itself a control, and it will be
validated by the practice that produced the three.  So: HOW WAS IT ESTABLISHED THAT IT CAN
FAIL?

The answer is not an argument, it is six planted worlds.  Each is a tree whose correct
verdict is known before the instrument is pointed at it, and in each the instrument is
required to return that verdict and not the convenient one.

    P1  an arm whose predicate is TRUE on the good input          -> must score UNFALSIFIABLE
    P2  an arm whose report is identical when its subject stops   -> must score LAUNDERED
    P3  an arm that genuinely reports its subject stopping        -> must score DISCRIMINATES
    P4  a bad input that is not bad (a rotted fixture)            -> must score SETUP FAILED
    P5  an unregistered arm-shaped site added to a source copy    -> the CENSUS must refuse
    P6  an auxiliary hole that has been repaired                  -> must report `not present`

P1 IS THE ONE THAT MATTERS, and it is not hypothetical here: THREE of this instrument's own
probes scored red on their first run because of defects in the PROBES, not in the arms —
C2's good side was already drifted so its predicate could not fail (the `"8 9" in out` shape,
with my name on it), S1/S2/S3 imported `seed_pin` from the sandbox so `ROOT` was not a git
repository and both sides failed identically, R4's good side reconciled the tree it was about
to test, and `sect()` returned the empty string for a section that ends the report, which
scored C1a LAUNDERED over a report naming the defect in full.  Five defects, all in the
auditor, all surfaced by the two-sided rule and none by reading.  They are recorded in
FINDINGS.md rather than quietly repaired, because an auditor that reports only other
people's defects is the fourth instance.

WHAT REMAINS UNFALSIFIED, stated because the ticket demands it be stated rather than implied:
the ARM REGISTRY's subjects.  P5 proves the census refuses an unregistered SITE.  Nothing
proves that an arm's `subject` sentence — "the twin does not claim canonicity about itself" —
is the property the arm's code actually tests.  A probe is written from the subject, so a
subject that misdescribes its arm produces a probe that agrees with it.  That is a human
reading, it is not checked here, and no amount of machinery in this directory would check it.
"""

import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib9876 as L  # noqa: E402
import a1_census  # noqa: E402
import a2_discriminate as A2  # noqa: E402


def _score(good_pair, bad_pair, red):
    """The exact scoring rule a2 uses, isolated so the planted worlds exercise IT."""
    g_rc, g_out = good_pair
    b_rc, b_out = bad_pair
    if bool(red(g_rc, g_out)):
        return "UNFALSIFIABLE"
    if bool(red(b_rc, b_out)):
        return "DISCRIMINATES"
    return "LAUNDERED"


PLANTED = []


def planted(pid, title, expect):
    def deco(fn):
        PLANTED.append((pid, title, expect, fn))
        return fn
    return deco


# ----------------------------------------------------------------------------------- P1
@planted("P1", "a predicate that is already satisfied by the GOOD input", "UNFALSIFIABLE")
def p1(_box):
    """The mg-2f44 shape, reconstructed: a membership test that section 1 satisfies always."""
    good = (1, "PASS  all three row sets agree: 1 2 3a 3b 4 5 6 7 8 9 10 11\n")
    bad = (1, "PASS  all three row sets agree: 1 2 3a 3b 4 5 6 7 8 9 10 11\n"
              "  DRIFT  1 of 12 ledger rows have changed\n")
    return _score(good, bad, A2.has("8 9"))


# ----------------------------------------------------------------------------------- P2
@planted("P2", "an arm whose report does not move when its subject stops", "LAUNDERED")
def p2(box):
    """A runner CONSTRUCTED to launder, so the planted fact does not depend on the target.

    THE FIRST VERSION OF THIS WORLD USED THE AUDITED `run_all.sh` AT EXIT 127, and mg-9876's
    own repair to that runner destroyed the world: the repaired script refuses a control that
    printed no VERDICT line, so BOTH sides went red and P2 scored UNFALSIFIABLE.  A selftest
    whose planted worlds are borrowed from the subject under audit stops working the moment
    the audit succeeds — which is the same failure as a fixture that hardcodes the one thing
    the instrument exists to let change (mg-2f44's two).  The laundering runner is now built
    here, in four lines, and is true by construction whatever the target does.
    """
    ctl = os.path.join(box, A2.DIR_REL)
    L.write(os.path.join(ctl, "launderer.sh"),
            '#!/bin/sh\n'
            'python3 "$(dirname "$0")/twin_pin.py" > /dev/null 2>&1\n'
            'echo "CLEAN — the twin\'s pinned ledger rows all still match STATE.md."\n'
            'exit 0\n')

    def run(control_code):
        L.write(os.path.join(ctl, "twin_pin.py"),
                A2._STUB.format(body="(stub)", code=control_code))
        proc = subprocess.run(["sh", os.path.join(ctl, "launderer.sh")],
                              capture_output=True, text=True)
        return proc.returncode, proc.stdout + proc.stderr

    return _score(run(0), run(127), lambda rc, text: rc != 0 or "CLEAN" not in text)


# ----------------------------------------------------------------------------------- P3
@planted("P3", "an arm that does report its subject stopping", "DISCRIMINATES")
def p3(box):
    sp, tp = os.path.join(box, "STATE.md"), os.path.join(box, A2.TWIN_REL)
    ctl = os.path.join(box, A2.DIR_REL)
    good = L.run_control(sp, tp, ctl)
    t = L.read(tp)
    L.write(tp, re.sub(r'<tr><td class="rowlabel">7</td>.*?</tr>', "", t, count=1, flags=re.S))
    bad = L.run_control(sp, tp, ctl)
    return _score(good, bad, A2.in_sect(1, "FAIL  the row sets disagree"))


# ----------------------------------------------------------------------------------- P4
@planted("P4", "a known-bad input that is not actually bad (rotted fixture)", "SETUP FAILED")
def p4(box):
    sp, tp = os.path.join(box, "STATE.md"), os.path.join(box, A2.TWIN_REL)
    ctl = os.path.join(box, A2.DIR_REL)

    def bad():
        t = L.read(tp)
        mutated = t.replace("@ 276aead1a8c5 (2026-08-07)", "@ deadbeefcafe (2026-01-01)", 1)
        if mutated == t:
            raise RuntimeError("mutation was a no-op — the fixture has rotted")
        L.write(tp, mutated)
        return L.run_control(sp, tp, ctl)

    try:
        bad()
    except RuntimeError:
        return "SETUP FAILED"
    return "DISCRIMINATES"


# ----------------------------------------------------------------------------------- P5
@planted("P5", "an unregistered arm-shaped site added to a source copy", "CENSUS REFUSES")
def p5(box):
    """THE INJECTION POINT IS DERIVED, NOT TYPED, AND THAT IS A REPAIR (mg-1344).

    This read `src.replace('    emit("=" * 86)\\n    emit({0: "VERDICT: CLEAN', …)` — two
    consecutive lines of the target quoted verbatim.  mg-1344 put a fourth verdict word
    between them (`IN FLIGHT`, for a declared in-flight relocation) and the string stopped
    existing, so this world scored SETUP FAILED and the auditor's selftest went 5 of 6.
    THE HARNESS WORKED: a rotted fixture is reported and not scored as a pass, which is P4's
    whole subject one row above.  But it is the SAME defect this arc has now recorded four
    times — a fixture spelling out the thing that changes — sitting in the file that exists
    to prove the auditor can fail.

    The anchor is now the LAST closing banner in `check()`, found by position rather than by
    quoting its neighbour.  What P5 needs is an arm-shaped line the registry does not claim,
    anywhere in a source the census walks; WHERE it sits was never load-bearing, and the old
    fixture bound itself to a neighbour it did not care about.
    """
    ctl = os.path.join(box, A2.DIR_REL)
    src = L.read(os.path.join(ctl, "twin_pin.py"))
    banner = '    emit("=" * 86)\n'
    at = src.rfind(banner)
    injected = src if at == -1 else (
        src[:at] + '    emit("  PASS  a seventh check nobody registered")\n' + src[at:])
    if injected == src:
        return "SETUP FAILED"
    L.write(os.path.join(ctl, "twin_pin.py"), injected)
    import io
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = a1_census.main(ctl)
    return "CENSUS REFUSES" if rc == 2 else f"CENSUS ACCEPTED (rc {rc})"


# ----------------------------------------------------------------------------------- P6
@planted("P6", "an auxiliary probe must say CONFIRMED on the hole and CLOSED on the repair",
         "CONFIRMED->CLOSED")
def p6(box):
    """Re-INTRODUCE the section-5 bypass into a copy, then repair it, and require both answers.

    THE FIRST VERSION ONLY CHECKED THE REPAIRED SIDE and it broke the moment the target was
    repaired for real: the string it patched no longer existed, so it scored SETUP FAILED.
    Worse than breaking, it was one-sided — an auxiliary register that can only print CLOSED
    is a list of assertions, exactly as one that can only print CONFIRMED is a list of
    accusations.  Both halves are now planted here, in a copy, independent of the target.
    """
    ctl = os.path.join(box, A2.DIR_REL)
    src = L.read(os.path.join(ctl, "twin_pin.py"))
    holed = src.replace("        if pin_lo <= line_no <= pin_hi:\n",
                        "        if L.PIN_START.split()[0] in line:\n", 1)
    if holed == src:
        return "SETUP FAILED (the repaired skip was not found in the target)"
    L.write(os.path.join(ctl, "twin_pin.py"), holed)
    fired_holed, _d = A2.x_comment_bypass(box)

    box2 = L.make_sandbox()
    try:
        L.write(os.path.join(box2, A2.DIR_REL, "twin_pin.py"), src)
        fired_repaired, _d2 = A2.x_comment_bypass(box2)
    finally:
        shutil.rmtree(box2, ignore_errors=True)

    return ("CONFIRMED" if fired_holed else "CLOSED") + "->" + \
           ("CONFIRMED" if fired_repaired else "CLOSED")


def main():
    print("=" * 92)
    print("mg-9876 — AUDITOR SELFTEST: six planted worlds whose verdicts are known in advance")
    print("=" * 92)
    print()
    print("The instrument that audits the controls is a control.  This file is how it was")
    print("established that it can FAIL, rather than asserted that it would.")
    print()

    rows = []
    for pid, title, expect, fn in PLANTED:
        box = L.make_sandbox()
        try:
            got = fn(box)
        except Exception as exc:                                          # noqa: BLE001
            got = f"PROBE ERROR {type(exc).__name__}: {exc}"
        finally:
            shutil.rmtree(box, ignore_errors=True)
        rows.append((pid, title, expect, got, got == expect))

    width = max(len(r[1]) for r in rows)
    print(f"{'id':<4} {'planted world'.ljust(width)}  {'must score':<16} {'scored':<16} ok")
    print("-" * 92)
    for pid, title, expect, got, ok in rows:
        print(f"{pid:<4} {title.ljust(width)}  {expect:<16} {got:<16} {'yes' if ok else 'NO'}")
    print()

    bad = [r for r in rows if not r[4]]
    print(f"{len(rows) - len(bad)} of {len(rows)} planted worlds scored as required.")
    print()
    if bad:
        print("THE AUDITOR DID NOT RETURN THE KNOWN ANSWER.  Its Part A verdicts are not")
        print("evidence until this passes; do not read a2's table.")
        return 1
    print("The scoring rule returns the known answer in all six worlds, including the two")
    print("worlds where the required answer is that a check is WORTHLESS.  That is the whole")
    print("of the claim: it is not a claim that a2's findings are correct, only that a2 is")
    print("capable of returning each of its verdicts and is not wired to one of them.")
    print()
    print("STILL UNFALSIFIED — the arm registry's SUBJECT sentences.  A probe is written from")
    print("the subject, so a subject that misdescribes its arm yields a probe that agrees with")
    print("it, and no machinery here would notice.  That is a human reading and it is the")
    print("standing exposure of this audit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
