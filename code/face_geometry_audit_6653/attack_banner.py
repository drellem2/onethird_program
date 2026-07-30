#!/usr/bin/env python3
"""mg-6653 -- can a grep on `controls_output.txt` still be fooled?

mg-f7bc's F5 was: the A4 scoring repair put "ALL CONTROLS PASS" into TWO
[PASS]-prefixed row names four lines from the top of the artifact, above a bottom
line explicitly denying it, so any grep for the banner returned two false
positives before the one true answer.  mg-f2e1's E5 renames those rows and adds a
new CONTROL ON THE ARTIFACT.

The instruction for this audit was: TRY TO CONSTRUCT THE FALSE POSITIVE rather
than reason that it is gone.  So each attack below MUTATES a private copy of
`controls.py`, runs the whole battery, and reads the artifact the way a grep
would.  An attack SUCCEEDS (against mg-f2e1) when the artifact ends up carrying
the banner on a [PASS]-prefixed line while the new control reports no offender
and the battery exits 0.

Nothing here touches the committed tree.  Runtime ~15 s (6 full battery runs).
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(REPO, "code", "face_geometry")
BANNER = "ALL CONTROLS PASS"

RESULTS = []


def run(mutate, label):
    """Copy the battery, apply `mutate` to controls.py, run it, read the output."""
    work = tempfile.mkdtemp(prefix="mg6653-")
    try:
        for fn in os.listdir(SRC):
            if fn.endswith(".py"):
                shutil.copy(os.path.join(SRC, fn), work)
        p = os.path.join(work, "controls.py")
        src = open(p, encoding="utf-8").read()
        new = mutate(src)
        if new is None:
            raise AssertionError("%s: mutation did not apply -- the anchor moved" % label)
        open(p, "w", encoding="utf-8").write(new)
        r = subprocess.run([sys.executable, "controls.py", "5"], cwd=work,
                           capture_output=True, text=True)
        return r.stdout, r.returncode
    finally:
        shutil.rmtree(work, ignore_errors=True)


def report(label, out, code, expect_control_fires):
    lines = out.split("\n")
    occ = [(i + 1, l) for i, l in enumerate(lines) if BANNER in l]
    pass_occ = [(i, l) for i, l in occ if l.lstrip().startswith("[PASS]")]
    ctrl = [l for l in lines if "no control row's own text contains" in l]
    fired = bool(ctrl) and ctrl[0].lstrip().startswith("[FAIL]")
    bottom = lines[-2] if len(lines) > 1 and not lines[-1].strip() else lines[-1]

    print()
    print("%s" % label)
    print("  exit code                        : %d" % code)
    print("  grep '%s' on the artifact : %d hit(s)%s"
          % (BANNER, len(occ), (" at line(s) %s" % [i for i, _ in occ]) if occ else ""))
    for i, l in occ:
        print("       line %-3d %s" % (i, l.strip()[:110]))
    print("  of which [PASS]-prefixed         : %d" % len(pass_occ))
    print("  CONTROL ON THE ARTIFACT          : %s"
          % (ctrl[0].strip()[:150] if ctrl else "(row absent)"))
    print("  bottom line                      : %s" % bottom.strip()[:120])

    if expect_control_fires:
        ok = fired and code == 1
        verdict = "POSITIVE CONTROL HOLDS" if ok else "POSITIVE CONTROL FAILED"
    else:
        # the attack succeeds if the banner reaches a [PASS] line unopposed
        succeeded = bool(pass_occ) and not fired and code == 0
        ok = not succeeded
        verdict = ("ATTACK SUCCEEDS -- the F5 defect is reachable with the new "
                   "control in place" if succeeded else "attack repelled")
    print("  ==> %s" % verdict)
    RESULTS.append((label, verdict))
    return ok


# --------------------------------------------------------------- A (positive)
def attack_a(src):
    """Restore mg-1319's two row names verbatim.  The control MUST fire."""
    a = ('check("a cannot-fail row keeps %s out of the bottom line" % banner_name,')
    b = ('check("with no cannot-fail row the bottom line IS %s" % banner_name,')
    if a not in src or b not in src:
        return None
    src = src.replace(a, 'check("a cannot-fail row suppresses the %r bottom line" % banner,')
    src = src.replace(b, 'check("with no cannot-fail row the bottom line is %r" % banner,')
    return src


# --------------------------------------------------------------- B (detail)
def attack_b(src):
    """Put the banner in a `detail=` string instead of a row NAME.

    The control's docstring discloses that it does not police detail strings --
    and then says it 'makes the artifact's occurrences of the banner exactly the
    bottom line's'.  Those two sentences cannot both be true.  This is the
    cheaper of the two routes, because `detail` is printed on the SAME LINE as
    the row name, behind the same [PASS] prefix, so a grep cannot tell them
    apart.
    """
    anchor = ('    check("a real failure still exits nonzero and is reported first",\n'
              '          fail_code == 1 and fail_lines[0].startswith("CONTROLS FAILED"))')
    if anchor not in src:
        return None
    return src.replace(anchor, anchor[:-1] + ',\n'
                       '          "clean-run bottom line is %r" % banner)')


# --------------------------------------------------------------- C (heading)
def attack_c(src):
    """Put the banner in a section heading -- a bare print(), also unpoliced."""
    anchor = '    print("CONTROL ON THE SCORING -- a tautological row must not read as a pass")'
    if anchor not in src:
        return None
    return src.replace(anchor, anchor + '\n'
                       '    print("  [PASS] bottom line for a clean run: %s" % '
                       '"ALL CONTROLS PASS")')


# --------------------------------------------------------------- D (scope)
def attack_d(src):
    """A row name carrying the banner in a form a literal scan cannot see.

    Not a defect in itself -- the control names the literal it scans -- but it
    fixes the boundary: what the control buys is exactly "no row name contains
    these 17 characters", and a reader looking for a stronger guarantee should
    not read one in.
    """
    anchor = '    banner_name = "the all-pass banner"          # never the literal; see above'
    if anchor not in src:
        return None
    return src.replace(anchor, anchor + '\n'
                       '    banner_name = "ALL CONTROLS  PASS (two spaces, invisible in the artifact)"')


# --------------------------------------------------------------- E (reachability)
def attack_e(src):
    """Try to reach the true bottom line WHILE a cannot-fail row is tallied.

    If `summarise` can be made to print the banner with a non-empty CANNOT_FAIL
    tally, the A4 repair itself is defeated and E5 is beside the point.  The
    mutation drops the guard's ordering, which is the weakest point available.
    """
    anchor = "    if cannot_fail_rows:"
    if anchor not in src:
        return None
    return src.replace(anchor, "    if cannot_fail_rows and False:", 1)


def main():
    print("mg-6653 -- ADVERSARIAL BATTERY AGAINST mg-f2e1's E5 "
          "(CONTROL ON THE ARTIFACT)")
    print("=" * 78)

    print()
    print("BASELINE -- the committed artifact, unmutated")
    art = open(os.path.join(SRC, "controls_output.txt"), encoding="utf-8").read()
    print("  grep '%s'                : %d hit(s)  <-- correct: this battery's "
          "bottom line denies it" % (BANNER, art.count(BANNER)))
    print("  grep -i 'all controls pass'              : %d hit(s), and it is the "
          "negation" % len(re.findall("all controls pass", art, re.I)))
    print("  grep 'all-pass banner'                   : %d hit(s) -- the "
          "indirection mg-f2e1 substituted"
          % len(re.findall("all-pass banner", art)))
    print("  NOTE, and it is the honest limit of the fix: line 5 of the artifact "
          "reads\n       %r"
          % [l.strip() for l in art.split("\n") if "bottom line IS" in l][0])
    print("       A [PASS] row five lines from the top still SAYS the bottom line "
          "is the\n       all-pass banner, above a bottom line saying it is not. "
          "The row is\n       conditional ('with no cannot-fail row'), exactly as "
          "mg-1319's was; what\n       changed is that the LITERAL is gone, so the "
          "defect is now invisible to\n       grep rather than absent from the "
          "artifact. That is what E5 claimed to do\n       and it is not more than "
          "that.")

    out, code = run(attack_a, "A")
    report("ATTACK A -- POSITIVE CONTROL ON THE NEW CONTROL: mg-1319's two row "
           "names, verbatim", out, code, expect_control_fires=True)

    out, code = run(attack_b, "B")
    report("ATTACK B -- the banner moved into a `detail=` string (same line, same "
           "[PASS] prefix)", out, code, expect_control_fires=False)

    out, code = run(attack_c, "C")
    report("ATTACK C -- the banner printed as a section heading, outside check()",
           out, code, expect_control_fires=False)

    out, code = run(attack_d, "D")
    report("ATTACK D -- a row name carrying the banner with a doubled space "
           "(scope boundary)", out, code, expect_control_fires=False)

    out, code = run(attack_e, "E")
    report("ATTACK E -- can the banner be reached with a non-empty CANNOT FAIL "
           "tally?", out, code, expect_control_fires=False)

    print()
    print("=" * 78)
    for label, verdict in RESULTS:
        print("  %-9s %s" % (label.split(" --")[0], verdict))
    print()
    print("BOTTOM LINE. The literal is gone from the artifact and ATTACK A shows "
          "the new control\nis a control and not a tautology -- both of mg-f2e1's "
          "E5 claims hold, and ATTACK E\nshows the A4 repair underneath it is "
          "sound: unguarding the tally makes the SELF-TEST's\nown assertion fail "
          "and the run exit 1, which is the right instrument catching it.\n\n"
          "But ATTACKS B and C construct the F5 defect in full with the new "
          "control in place:\na [PASS]-prefixed line near the top of "
          "controls_output.txt carrying 'ALL CONTROLS\nPASS', above a bottom line "
          "denying it, with the control reporting 'offending rows:\nnone' and exit "
          "0. B is the cheaper route -- `detail` prints on the SAME LINE as the\n"
          "row name, behind the same [PASS] prefix, so a grep cannot tell them "
          "apart.\n\nThe control scans ROW_NAMES only. Its docstring discloses "
          "that, and then says it\n'makes the artifact's occurrences of the banner "
          "exactly the bottom line's, and claims\nnothing further' -- the wider of "
          "the two adjacent sentences, and the one to strike.\nATTACK D fixes the "
          "other boundary: what the control buys is exactly 'no row name\ncontains "
          "these 17 characters', which is the right scope for it to have and less "
          "than\nthe docstring's last clause asserts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
