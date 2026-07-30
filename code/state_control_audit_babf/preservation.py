#!/usr/bin/env python3
"""mg-babf — DID THE REPAIR PRESERVE WHAT WAS ALREADY RIGHT?

Three things were confirmed before mg-7870 and any change to them is a defect, because this
shape of repair — replace the mechanism — is exactly where one defect gets swapped for
another.  Each is re-derived here from source, not read off a predecessor's document.

  P1  THE PINNED BATTERY IS BYTE-IDENTICAL and still reproduces out_audit.txt.
      Twice verified before this audit (mg-2216, mg-7870); this is the third.
  P2  "NOTHING WAS LOST" IS NOT RE-OPENED — the control-vs-content framing is correct.
  P3  THE THREE RECORD CORRECTIONS (A1, A2, A3) ARE TRUE, re-derived from source.

P1 is also re-established under a mutation of MINE, not mg-bd41's gutting and not mg-2216's
M06: the point of A1 is that the pinned battery's verdict does not depend on the size or
shape of the damage, and a third independent mutation is how that stops being an anecdote.
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Harness, README, quote_span, M_F1     # noqa: E402

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
PRE_REPAIR = "6b1eacf"
REPAIR = "e924590"
BATTERY = "code/state_audit_6a2f/run_all.sh"
OUT_AUDIT = "code/state_audit_6a2f/out_audit.txt"

_v = []


def verdict(pid, text, measured, ok, note=""):
    _v.append((pid, ok))
    print(f"  [{'HOLDS' if ok else 'BROKEN'}] {pid}  {text}")
    print(f"           measured: {measured}")
    if note:
        print(f"           {note}")


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args],
                          capture_output=True, text=True, check=True).stdout


def run_battery():
    p = subprocess.run(["sh", BATTERY], cwd=REPO, capture_output=True)
    return p.returncode, p.stdout


def main():
    print("mg-babf — did mg-7870's repair preserve what was already right?")
    print("=" * 86)

    # ---------------------------------------------------------------------- P1
    print()
    print("P1. THE PINNED BATTERY")
    print("-" * 22)
    d = git("diff", "--stat", PRE_REPAIR, REPAIR, "--", "code/state_audit_6a2f/").strip()
    verdict("P1.1", "code/state_audit_6a2f/ is byte-identical across the repair",
            f"git diff {PRE_REPAIR}..{REPAIR} -- code/state_audit_6a2f/ : "
            + (repr(d) if d else "EMPTY"), not d)
    d2 = git("diff", "--stat", "main", "--", "code/state_audit_6a2f/").strip()
    verdict("P1.2", "and byte-identical against main in this working tree",
            "EMPTY" if not d2 else repr(d2), not d2)

    with open(os.path.join(REPO, OUT_AUDIT), "rb") as fh:
        committed = fh.read()
    rc, got = run_battery()
    verdict("P1.3", "it still reproduces out_audit.txt byte-identically",
            f"exit {rc}; committed {len(committed)} bytes, produced {len(got)} bytes; "
            f"identical: {got == committed}", rc == 0 and got == committed)

    # P1.4 — the same conclusion under a mutation that is neither mg-bd41's nor mg-2216's
    h = Harness()

    def comment_out_f1(text):
        lines = text.split("\n")
        s, e = quote_span(text, M_F1)
        return "\n".join(lines[:s] + ["<!--"] + lines[s:e] + ["-->"] + lines[e:])

    try:
        with open(os.path.join(REPO, README), "w", encoding="utf-8") as fh:
            fh.write(comment_out_f1(h.text(README)))
        rc2, got2 = run_battery()
    finally:
        h.restore()
    verdict("P1.4",
            "the pinned battery is blind to a mutation of MINE, as it was to mg-bd41's "
            "gutting and mg-2216's M06",
            f"with b68db5d's F1 correction block HTML-commented out of the README, the "
            f"battery exits {rc2} and emits {len(got2)} bytes, identical to the committed "
            f"output: {got2 == committed}",
            got2 == committed,
            note="this HOLDS in the sense that the A1 finding is re-confirmed a third time "
                 "from a third mutation; the battery is doing exactly what it was built to "
                 "do and pinning is a feature there, which is why nothing here asks it to "
                 "change")

    # ---------------------------------------------------------------------- P2
    print()
    print('P2. "NOTHING WAS LOST" IS NOT RE-OPENED')
    print("-" * 38)
    diff = git("diff", PRE_REPAIR, REPAIR, "--", "STATE.md",
               "docs/state-history/README.md")
    removed = [l for l in diff.split("\n") if l.startswith("-") and not l.startswith("---")]
    verdict("P2.1", "the repair deletes no line of STATE.md or the state-history README",
            f"{len(removed)} removed lines in the repair's diff over those two files",
            not removed)
    touched = [l for l in git("diff", "--name-only", PRE_REPAIR, REPAIR).strip().split("\n")
               if l]
    stray = [t for t in touched
             if not (t.startswith("code/state_landing_control_2da3/")
                     or t == "docs/state-history/README.md")]
    verdict("P2.2", "the repair touches only the control's own directory and the README",
            f"files touched: {touched}", not stray)
    readme_now = open(os.path.join(REPO, README), encoding="utf-8").read()
    framing = ("**And none of this touches \"nothing was lost\", which STANDS.**"
               in readme_now)
    verdict("P2.3", "the control-vs-content framing sentence is present and unaltered",
            f'"...none of this touches \'nothing was lost\', which STANDS" present: {framing}; '
            f"unchanged across the repair: "
            f"{framing and framing == ('**And none of this touches \"nothing was lost\", '
                                       'which STANDS.**' in git('show', f'{PRE_REPAIR}:{README}'))}",
            framing)

    # ---------------------------------------------------------------------- P3
    print()
    print("P3. THE THREE RECORD CORRECTIONS, RE-DERIVED FROM SOURCE")
    print("-" * 56)

    # A3 — the ancestry.  mg-34bf's commit is 57f962f.
    parents = {}
    for rev in ("57f962f", "97cb533", "60f4dac"):
        parents[rev] = git("log", "-1", "--format=%p", rev).strip()[:7]
    chain_ok = (parents["57f962f"] == "97cb533" and parents["97cb533"] == "60f4dac")
    verdict("P3.A3", 'the ancestry: "two commits before mg-34bf\'s parent" was off by one',
            f"%p chain: 57f962f <- {parents['57f962f']} <- {parents['97cb533']}; "
            f"60f4dac is mg-34bf's parent's PARENT, not two before the parent",
            chain_ok)

    # A2 — mg-6a2f's document DID name the source, and db08b4c:STATE.md is 327 lines / 0 hits
    doc = "docs/OneThird-STATE-Restructure-IndependentAudit.md"     # mg-6a2f's document
    text = git("show", f"main:{doc}")
    named = "pm-onethird's ticket (a stale revision, line bytes)" in text
    at_line = next((k for k, l in enumerate(text.split("\n"), start=1)
                    if "pm-onethird's ticket (a stale revision, line bytes)" in l), None)
    db = git("show", "db08b4c:STATE.md")
    lines_db = len(db.split("\n")) - (1 if db.endswith("\n") else 0)
    hits_db = db.count("mg-a3d4")
    verdict("P3.A2", 'the over-claim: mg-6a2f DID name the source, and the new part is new',
            f"the phrase is in {doc} at :{at_line} (mg-2216 published :212); "
            f"db08b4c:STATE.md is {lines_db} lines with {hits_db} occurrences of mg-a3d4",
            named and lines_db == 327 and hits_db == 0)

    # A1 — the blind certification; established at P1.3/P1.4 above
    verdict("P3.A1", "the blind certification: the pinned battery cannot see the tree",
            "re-established at P1.4 from a third independent mutation "
            f"(identical output: {got2 == committed})",
            got2 == committed,
            note="and mechanically: no script in code/state_audit_6a2f/ opens the working "
                 "tree or resolves HEAD — checked next")

    scripts = [f for f in os.listdir(os.path.join(REPO, "code/state_audit_6a2f"))
               if f.endswith(".py")]
    opens_tree = []
    for f in scripts:
        with open(os.path.join(REPO, "code/state_audit_6a2f", f), encoding="utf-8") as fh:
            body = fh.read()
        if re.search(r"\bHEAD\b", body) or re.search(r"open\(\s*[\"']STATE\.md", body):
            opens_tree.append(f)
    verdict("P3.A1b",
            'the mechanical test Appendix A publishes: "does any script open the working '
            'tree or resolve HEAD?"',
            f"{len(scripts)} scripts in code/state_audit_6a2f/; "
            f"{len(opens_tree)} open STATE.md directly or mention HEAD"
            + (f": {opens_tree}" if opens_tree else ""),
            not opens_tree)

    print()
    print("=" * 86)
    bad = [p for p, ok in _v if not ok]
    print(f"{len(_v)} preservation checks: {len(_v) - len(bad)} HOLD, {len(bad)} BROKEN"
          + (f" — {bad}" if bad else ""))
    print("=" * 86)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
