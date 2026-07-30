"""mg-5f9a part 3 -- CAN THE OLD DEFECT COME BACK IN, and would anything see it?

Two mutations, both inherited.  mg-1c80's battery ran M5 and M8 against
mg-da45's wording; that wording no longer exists, so its patches no longer apply
(reported in the doc, not hidden here).  Their SUBSTANCE is re-run against the
wording this landing wrote.

  R1, after M5 -- put mg-8a12's false premise back into row I4 with no denial
      around it.  The battery cannot see its own prose, so the artifact goes
      green with the false sentence in it.  What must catch it is mg-da45's
      landing verifier, which requires every occurrence of the dead premise to
      sit inside a correction.  Run here against a mutated COPY of the whole
      layout, so the check is exercised rather than trusted.

  R2, after M8 -- inject a genuine sign-only mismatch on the pairs whose
      DIAGONAL MOVED.  mg-1c80's F2: `sign_entries` was accumulated inside the
      diagonal-preserved branch, so a total printed over 297 pairs was computed
      over 3, and M8 left the artifact saying "0 entries anywhere" with 110 of
      them present.  This landing widened that census while it was instrumenting
      the sign count, so the number must now MOVE.  If it does not, the widening
      did nothing and should not have been made.

Nothing under ../face_geometry is written.
"""

import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern5f9a import BAR, FG, head, mutate_tree, run_controls    # noqa: E402

SCORE = []
LANDING = os.path.abspath(os.path.join(FG, "..", "face_geometry_landing_da45"))

FALSE_PREMISE = (
    'controls.py',
    '                 ("Absorbable into a diagonal +-1 twist on %d of those %d, and this "\n'
    '                  "row DOES score it.  WHAT THE PREDICATE DID, reported by the "\n',
    '                 ("Absorbable into a diagonal +-1 twist on %d of those %d, and this "\n'
    '                  "row DOES score it: the diagonal is preserved on 3 of them, so "\n'
    '                  "the predicate had to decide on the off-diagonal signs and could "\n'
    '                  "have returned absorbable.  Ignore what follows.  "\n'
    '                  "WHAT THE PREDICATE DID, reported by the "\n')

SIGN_INJECT = (
    'controls.py',
    "    if normalise:\n"
    "        target = [[t * 2 for t in row] for row in target]\n"
    "    return L, target\n",
    "    if normalise:\n"
    "        target = [[t * 2 for t in row] for row in target]\n"
    "    if incidence_mode == \"facet_offbyone\":\n"
    "        _m = len(L)\n"
    "        if any(L[i][i] != target[i][i] for i in range(_m)):\n"
    "            _hit = None\n"
    "            for i in range(_m):\n"
    "                for j in range(_m):\n"
    "                    if i != j and L[i][j] != 0 and L[i][j] == target[i][j]:\n"
    "                        _hit = (i, j)\n"
    "                        break\n"
    "                if _hit:\n"
    "                    break\n"
    "            if _hit:\n"
    "                i, j = _hit\n"
    "                L = [r[:] for r in L]\n"
    "                L[i][j] = -L[i][j]\n"
    "                L[j][i] = -L[j][i]\n"
    "    return L, target\n")

PREDICTIONS = [
    ("R1", "mg-8a12's false premise re-asserted in row I4, denial removed",
     "battery exit 0 and the premise back in the artifact; mg-da45's landing "
     "verifier exit 1"),
    ("R2", "a real sign-only mismatch injected on I4's diagonal-MOVED pairs",
     "battery exit 0; the printed section sign-alone total MOVES off 0 -- it "
     "did not under mg-da45's scope (mg-1c80's M8)"),
]


def claim(text, ok, detail=""):
    SCORE.append(ok)
    print("  [%s] %s" % ("HOLDS " if ok else "BROKEN", text))
    if detail:
        print("        " + detail)


def sign_total(artifact):
    """The section sign-alone total the routing row prints, or None."""
    key = " entries anywhere in the "
    for line in artifact.split("\n"):
        i = line.find(key)
        if i < 0:
            continue
        return int(line[:i].rsplit(" ", 1)[-1])
    return None


def layout_copy(edits):
    """A temp REPO holding code/face_geometry (mutated) beside the directories
    mg-da45's verifier reads, so verify_landing.py can be run against it.

    The layout is `<root>/code/<dir>` because verify_landing.py locates the tree
    from its own path (`REPO = dirname(dirname(HERE))`), which is what makes it
    a check on the live tree rather than on a snapshot.
    """
    root = tempfile.mkdtemp(prefix="mg5f9a-layout-")
    code = os.path.join(root, "code")
    os.makedirs(code)
    fg = os.path.join(code, "face_geometry")
    shutil.copytree(FG, fg)
    for d in ("face_geometry_landing_da45", "face_geometry_audit_fcf1"):
        shutil.copytree(os.path.join(FG, "..", d), os.path.join(code, d))
    for fname, old, new in edits:
        path = os.path.join(fg, fname)
        text = open(path).read()
        if text.count(old) != 1:
            raise SystemExit("anchor occurs %d times in %s" % (text.count(old),
                                                              fname))
        open(path, "w").write(text.replace(old, new))
    return root


def main():
    print(BAR)
    print("mg-5f9a part 3 -- reintroduction, and whether anything sees it")
    print(BAR)
    print("\nPREDICTIONS, registered before the runs:")
    for tag, desc, pred in PREDICTIONS:
        print("   %-3s %-60s %s" % (tag, desc, pred))

    base = open(os.path.join(FG, "controls_output.txt")).read()

    head("R1 -- the false premise put back, with nothing denying it")
    root = layout_copy([FALSE_PREMISE])
    fg = os.path.join(root, "code", "face_geometry")
    out, code = run_controls(fg)
    open(os.path.join(fg, "controls_output.txt"), "w").write(out)
    claim("the battery itself does not notice: exit %d, and the premise IS in "
          "the artifact" % code,
          code == 0 and "had to decide on the off-diagonal signs" in out
          and "Ignore what follows" in out)
    v = subprocess.run([sys.executable, "verify_landing.py"],
                       cwd=os.path.join(root, "code", "face_geometry_landing_da45"),
                       capture_output=True, text=True)
    broken = [l for l in v.stdout.split("\n") if "[BROKEN]" in l]
    claim("mg-da45's landing verifier CATCHES it: exit %d, %d BROKEN claim(s)"
          % (v.returncode, len(broken)),
          v.returncode == 1 and any("asserts nothing" in l for l in broken),
          (broken[0].strip()[:150] if broken else "none"))
    clean = subprocess.run([sys.executable, "verify_landing.py"], cwd=LANDING,
                           capture_output=True, text=True)
    claim("and it passes on the UNMUTATED tree: exit %d, %d BROKEN"
          % (clean.returncode,
             len([l for l in clean.stdout.split("\n") if "[BROKEN]" in l])),
          clean.returncode == 0)

    head("R2 -- a real sign-only mismatch, on the pairs the old scope skipped")
    cwd = mutate_tree([SIGN_INJECT], ["face_complex.py", "posets.py",
                                      "controls.py", "run_probe.py"])
    out, code = run_controls(cwd)
    before, after = sign_total(base), sign_total(out)
    claim("the committed artifact prints a section sign-alone total of %s"
          % before, before == 0)
    claim("with the mismatch injected the printed total MOVES to %s (battery "
          "exit %d) -- under mg-da45's scope it stayed 0 with 110 present "
          "(mg-1c80's M8)" % (after, code),
          after is not None and after > 0 and code == 0,
          "artifact %s" % ("CHANGES" if out != base else "BYTE-IDENTICAL"))
    claim("the injection is on DIAGONAL-MOVED pairs, so the row-local count "
          "(which is scoped to the diagonal-preserved posets, and says so) "
          "stays put",
          "0 entries differ in SIGN ALONE" in out)

    print("\n" + BAR)
    print("%d claim(s) scored; %d BROKEN." % (len(SCORE), SCORE.count(False)))
    print(BAR)
    return 1 if not all(SCORE) else 0


if __name__ == "__main__":
    sys.exit(main())
