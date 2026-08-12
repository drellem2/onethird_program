#!/usr/bin/env python3
"""mg-a518 — the positive control ON THE CONTROLS.

controls_a518.py is a negative control: it mutates the store and requires the
detector to speak.  This asks the next question, which is the one the arc keeps
paying for — CAN THAT CONTROL FAIL AT ALL?  Four planted worlds, each one a way
controls_a518.py could go green while measuring nothing, and each must be caught.

P1 IS NOT HYPOTHETICAL.  It is the defect the control shipped with and failed on
its first run: a store copied WITHOUT mtime preservation ages nothing, so every
unanswered audit sits in WAITING instead of SILENT and every mutation arm comes
back `pass`.  That is a control that cannot fire, reporting green, inside the
remedy for a detector that could not fire and reported green.  The guard is now
in copy_store(); this proves the guard bites rather than asserting it does.

Exit: 0 all planted worlds caught, 1 one was not, 2 refused before deciding.
"""

import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import controls_a518 as C  # noqa: E402


def main():
    results = []
    print("mg-a518 — POSITIVE CONTROL ON THE CONTROLS")
    print("=" * 78)

    # ---- P1: the mtime guard --------------------------------------------
    print("\n[P1] a store copied WITHOUT mtime preservation must REFUSE, not pass.")
    print("     This is D1 — the defect this control actually shipped with.")
    src = os.path.join(os.path.expanduser("~"), ".macguffin", "work")
    if not os.path.isdir(src):
        print("     REFUSED: no store to copy")
        return 2
    tmp = tempfile.mkdtemp(prefix="a518-x1-")
    try:
        real_copy2 = shutil.copy2
        shutil.copy2 = shutil.copy  # the exact mistake, planted
        try:
            C.copy_store(src, os.path.join(tmp, "flat"))
            caught = False
            detail = "copy_store accepted a store whose mtimes were destroyed"
        except C.Refused as exc:
            caught = True
            detail = str(exc)
        finally:
            shutil.copy2 = real_copy2
        print(f"     {'CAUGHT' if caught else 'MISSED'}: {detail}")
        results.append(("P1", caught))

        # ---- P2: the same copy, done right, must NOT refuse --------------
        print("\n[P2] the same copy done correctly must NOT refuse — a guard that refuses")
        print("     everything is not a guard, it is an outage.")
        try:
            C.copy_store(src, os.path.join(tmp, "good"))
            ok, detail = True, "copy_store accepted a correctly-preserved copy"
        except C.Refused as exc:
            ok, detail = False, f"copy_store refused a GOOD copy: {exc}"
        print(f"     {'CAUGHT' if ok else 'MISSED'}: {detail}")
        results.append(("P2", ok))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ---- P3: a mutation that mutates nothing -----------------------------
    print("\n[P3] strip_tag must report FALSE when the tag it was told to remove is")
    print("     absent.  An arm whose mutation silently did nothing observes the")
    print("     UNMUTATED store and reports `as expected` — green for no reason.")
    tmp = tempfile.mkdtemp(prefix="a518-x1b-")
    try:
        p = os.path.join(tmp, "item.md")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("---\nid: mg-0000\ntags: [alpha, beta-followup]\n---\n\n# t\n")
        absent = C.strip_tag(p, "gamma-followup")
        present = C.strip_tag(p, "beta-followup")
        with open(p, encoding="utf-8") as fh:
            left = [l for l in fh.read().split("\n") if l.startswith("tags:")][0]
        ok = (absent is False) and (present is True) and left == "tags: [alpha]"
        print(f"     absent tag -> {absent} (want False); present tag -> {present} (want True)")
        print(f"     line after removal: {left!r} (want 'tags: [alpha]')")
        print(f"     {'CAUGHT' if ok else 'MISSED'}")
        results.append(("P3", ok))

        # ---- P4: a prefix tag must not be half-removed -------------------
        print("\n[P4] removing `mg-5cba-followup` must NOT damage a tag that CONTAINS it.")
        print("     A string-replace implementation passes every arm above and corrupts")
        print("     the store — and the detector matches successors by SUBSTRING, so a")
        print("     mangled neighbour changes the answer without changing the arm.")
        q = os.path.join(tmp, "item2.md")
        with open(q, "w", encoding="utf-8") as fh:
            fh.write("---\nid: mg-0001\ntags: [mg-5cba-followup, mg-5cba-followup-x]\n---\n\n# t\n")
        C.strip_tag(q, "mg-5cba-followup")
        with open(q, encoding="utf-8") as fh:
            left2 = [l for l in fh.read().split("\n") if l.startswith("tags:")][0]
        ok4 = left2 == "tags: [mg-5cba-followup-x]"
        print(f"     line after removal: {left2!r} (want 'tags: [mg-5cba-followup-x]')")
        print(f"     {'CAUGHT' if ok4 else 'MISSED'}")
        results.append(("P4", ok4))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ---- P5: the parser must not invent a population ---------------------
    print("\n[P5] population() must return None on a detail it cannot parse, and")
    print("     silent_ids() must return the empty set on a `pass`.  A parser that")
    print("     guesses turns 'I could not read the report' into 'the report was clean'.")
    unparseable = C.population({"detail": "not configured — [audit_successor] names no repos"})
    passrow = C.silent_ids({"status": "pass", "detail": "no merged audit has gone unanswered"})
    warnrow = C.silent_ids({
        "status": "warn",
        "detail": "2 merged audit(s) answered by NOTHING after 4h: mg-07fd (silent 1h, "
                  "merged x), mg-5cba (silent 2h, merged y). Read each one and file a "
                  "repair ticket referencing it (`mg new --depends=mg-9999 ...`)",
    })
    ok5 = unparseable is None and passrow == set() and warnrow == {"mg-07fd", "mg-5cba"}
    print(f"     unparseable detail -> {unparseable} (want None)")
    print(f"     pass row -> {passrow or 'set()'} (want empty)")
    print(f"     warn row -> {sorted(warnrow)} (want ['mg-07fd', 'mg-5cba'] — and NOT the")
    print("       mg-9999 in the remedy sentence, which is an example and not a finding)")
    print(f"     {'CAUGHT' if ok5 else 'MISSED'}")
    results.append(("P5", ok5))

    print("\n" + "=" * 78)
    missed = [name for name, ok in results if not ok]
    for name, ok in results:
        print(f"  {name}: {'satisfactory' if ok else 'MISSED'}")
    if missed:
        print(f"\nPOSITIVE CONTROL VERDICT: FIRED — {', '.join(missed)} did not behave")
        return 1
    print(f"\nPOSITIVE CONTROL VERDICT: CLEAN — {len(results)} of {len(results)} planted")
    print("worlds caught, including the one this control actually shipped with.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
