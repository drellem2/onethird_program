#!/usr/bin/env python3
"""mg-3902 a1 — what does the EXISTING control say about a pin that is provably false?

WHY THIS FILE EXISTS.  `a3_negative_control.py` shows that `a2_pin_resolves.py` catches five
ways the pin can lie.  On its own that is a claim about a checker written alongside its own
tests.  The number that makes the checker worth its slot on the merge critical path is a
different one: **how many of those inputs the control that already exists says nothing about.**

So this script takes two inputs that state a falsehood about which `STATE.md` the twin
renders, and runs each through BOTH:

  * `code/rendered_twin_pin_9bc2/twin_pin.py` — the six-section control, unchanged by mg-3902;
  * `code/twin_disposition_audit_3902/a2_pin_resolves.py` — the new one.

A `CLEAN` in the OLD column is the finding. The input is false, consistently false in both
copies of the provenance string, and the instrument built to remove unfalsifiable provenance
claims says nothing.

THE OLD COLUMN IS ASSERTED TO BE UNMODIFIED, NOT ASSUMED.  mg-3902 wrote a section 7 into
`twin_pin.py`, ran it, and backed it out (see README).  If a later ticket lands that section,
this script's OLD column stops being 'the control as shipped' and starts being 'the control
including the repair' — and the table would quietly become a comparison of a thing with
itself.  So the file is compared against `origin/main` and the run REFUSES if it differs,
rather than printing a table whose meaning has changed underneath it.

Run:  python3 code/twin_disposition_audit_3902/a1_prerepair.py
"""

import hashlib
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PIN_REL = "code/rendered_twin_pin_9bc2/twin_pin.py"
OLD = os.path.join(ROOT, PIN_REL)

sys.path.insert(0, HERE)
import a2_pin_resolves as A2  # noqa: E402
import a3_negative_control as A3  # noqa: E402

BASE_REF = "origin/main"


def mut_wrong_real_commit(text):
    """Repoint the pin at a REAL commit whose STATE.md is not the digested one.

    Derived from git at run time, never typed: the pinned commit is precisely what every
    reconciliation moves, and mg-2f44 demonstrated in this lineage that a fixture spelling it
    out can expire SILENTLY.
    """
    sha = re.search(r"\n  state-sha256: ([0-9a-f]{64})", text)
    pinned = re.search(r"\n  commit: ([0-9a-f]{7,40})", text)
    if not sha or not pinned:
        return None
    rc, revs = A2.git("rev-list", "--max-count=60", "HEAD", "--", "STATE.md")
    if rc != 0:
        return None
    for rev in revs.split():
        rc2, blob = A2.git("show", f"{rev}:STATE.md", binary=True)
        if rc2 == 0 and hashlib.sha256(blob).hexdigest() != sha.group(1):
            if rev[:7] == pinned.group(1):
                continue
            return text.replace(pinned.group(1), rev[:7])
    return None


def mut_nonexistent_commit(text):
    pinned = re.search(r"\n  commit: ([0-9a-f]{7,40})", text)
    if not pinned:
        return None
    return text.replace(pinned.group(1), "0" * len(pinned.group(1)))


def mut_orphan_but_byte_identical(text):
    """Repoint the pin at an ORPHAN commit whose STATE.md IS the digested one (mg-daba).

    The other two rows are false about the DIGEST, which is the half both columns were
    already arguing about.  This one is TRUE about the digest and false about ancestry — the
    conflict case, and the one `c308368` actually was.  It is the strongest row in the table
    precisely because the falsehood is invisible to any amount of hashing: the bytes check
    out, and no merge will ever bring the commit they check out at into `main`.
    """
    pinned = re.search(r"\n  commit: ([0-9a-f]{7,40})", text)
    if not pinned:
        return None
    orphan = A3._an_orphan_commit_with_the_pinned_state(pinned.group(1))
    if orphan is None or orphan == pinned.group(1):
        return None
    return text.replace(pinned.group(1), orphan)


MUTATIONS = [
    ("pin repointed at a REAL commit carrying a DIFFERENT STATE.md", mut_wrong_real_commit),
    ("pin AND visible line both name a commit THAT DOES NOT EXIST", mut_nonexistent_commit),
    ("pin at an ORPHAN commit whose STATE.md is BYTE-IDENTICAL", mut_orphan_but_byte_identical),
]


def run_old(twin_text):
    """`twin_pin.py` over the real STATE.md and a twin carrying twin_text."""
    with tempfile.TemporaryDirectory() as tmp:
        tp = os.path.join(tmp, "twin.html")
        with open(tp, "w", encoding="utf-8") as fh:
            fh.write(twin_text)
        proc = subprocess.run(
            [sys.executable, OLD, "--state", os.path.join(ROOT, "STATE.md"), "--twin", tp],
            capture_output=True, text=True)
        return proc.returncode


def run_new(twin_text):
    code, _lines = A2.report(twin_text)
    return code


def main():
    rc, _ = A2.git("rev-parse", "--git-dir")
    if rc != 0:
        print("REFUSED: no git repository at ROOT.  Both columns below resolve the pin")
        print("         against history and there is none, so the table would be vacuous.")
        return 0

    # The OLD column must be the control AS SHIPPED.  See the module docstring.
    rc, remote = A2.git("show", f"{BASE_REF}:{PIN_REL}", binary=True)
    if rc != 0:
        print(f"REFUSED: cannot read {PIN_REL} at {BASE_REF} — the OLD column has no")
        print("         definition, so nothing below would mean what it says.")
        return 2
    with open(OLD, "rb") as fh:
        local = fh.read()
    if local != remote:
        print(f"REFUSED: {PIN_REL} differs from {BASE_REF}.")
        print("         The OLD column is supposed to be the control AS SHIPPED.  If a repair")
        print("         has landed there, this table is comparing the new check against a copy")
        print("         of itself, and a green would mean nothing.  Re-read the README's")
        print("         'why this is a separate suite' section before touching this file.")
        return 2

    twin_text = open(os.path.join(ROOT, "docs", "state-of-the-wall.html"),
                     encoding="utf-8").read()

    print("=" * 86)
    print("mg-3902 a1 — what the EXISTING control says about a provably false pin")
    print("=" * 86)
    print(f"  OLD : {PIN_REL} (verified identical to {BASE_REF})")
    print("  NEW : code/twin_disposition_audit_3902/a2_pin_resolves.py")
    print()
    print("  A `CLEAN` in the OLD column is the finding: the input is false, consistently")
    print("  false in BOTH copies of the provenance string, and the instrument built to")
    print("  remove unfalsifiable provenance claims says nothing.")
    print()

    # THE CONTROL COMES FIRST.  If the unmutated twin is not clean under both, every row
    # below is uninterpretable and this must say so rather than print a table.
    b_old, b_new = run_old(twin_text), run_new(twin_text)
    print(f"  CONTROL (no mutation)   old exit {b_old}   new exit {b_new}")
    if b_old != 0 or b_new != 0:
        print("  REFUSED: the unmutated twin is not clean under both controls, so 'the old one")
        print("           missed it' would be unsupported.")
        return 2
    print()

    rows, failures = [], 0
    for name, fn in MUTATIONS:
        mutated = fn(twin_text)
        if mutated is None or mutated == twin_text:
            rows.append((name, "SETUP FAILED", "SETUP FAILED"))
            failures += 1
            continue
        o, n = run_old(mutated), run_new(mutated)
        rows.append((name,
                     "CLEAN — MISSED IT" if o == 0 else f"caught (exit {o})",
                     f"caught (exit {n})" if n != 0 else "CLEAN — HOLE"))
        if n == 0:
            failures += 1

    w = max(len(r[0]) for r in rows)
    print(f"  {'input':<{w}}  {'OLD (as shipped)':<20}  NEW")
    print("  " + "-" * (w + 40))
    for name, o, n in rows:
        print(f"  {name:<{w}}  {o:<20}  {n}")
    print()

    missed = sum(1 for _n, o, _x in rows if o.startswith("CLEAN"))
    caught = sum(1 for _n, _o, x in rows if x.startswith("caught"))
    print(f"  VERDICT: the shipped control is CLEAN on {missed} of {len(rows)} inputs that")
    print("           state a falsehood about which STATE.md this page renders;")
    print(f"           a2_pin_resolves.py catches {caught} of {len(rows)}.")
    if failures:
        print(f"  {failures} row(s) established nothing — read them, do not average them.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
