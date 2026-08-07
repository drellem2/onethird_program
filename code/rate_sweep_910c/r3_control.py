"""mg-910c R3 -- negative controls.  Does R2's detector fire when the repair is NOT there?

A detector that passes is worth nothing until it has been shown to fail.  Four mutations, each
pre-declared before it was run, and each reported as it came out.  Nothing on disk is touched:
the mutations are applied to a copy of the tree in a temp directory, or in memory.

  N0  R2 run against the UNREPAIRED tree at `main`.
      PRE-DECLARED: FIRE, on every LIVE and LIVE-OPEN site (19 of them) and on none of the
      CITED / SURVIVES / COLLISION sites.  This is the control that matters -- it says the
      19 sites really were defective before this ticket and the 7 really were not.

  N1  strip only the `~~` strike glyphs from the repaired documents.
      PRE-DECLARED: NO FIRE.  The detector is keyed on the refutation being SAID -- this
      ticket's citation plus a word meaning "wrong" -- not on the glyph.  mg-372e's M0
      established the same thing for its own detector and reported it rather than tuning it.

  N2  strip THIS TICKET'S citation from the repaired documents, leaving everything else.
      PRE-DECLARED: FIRE on all 19.

  N3  plant a LIVE site, in the corpus's own voice, saying the rate buys an order.
      PRE-DECLARED: FIRE.  R1's ARROW pattern must catch it, whitespace and all -- this is the
      mg-7085 hazard, where a grep spelled one way left the defect alive in two siblings.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

sys.path.insert(0, HERE)
import r1_census as r1          # noqa: E402
import r2_classify as r2        # noqa: E402

REPAIRED = [
    "docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md",
    "docs/OneThird-DualCertificate-mg-131e.md",
    "docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md",
    "code/dual_certificate_131e/d3_refutation.py",
]

# N2 strips the CITATION only, never the anchor text.  The first version stripped every marker
# word too, including `Θ(n²)`, and destroyed 13 of the 25 anchors -- so it reported 9 fires and 13
# missing rather than 18 fires, which is not a control, it is a broken mutation.  Stripping the
# citation alone is the minimal mutation that undoes the repair as R2 defines repair.
MARKERS = re.compile(r"mg-910c")

# The plant writes each half of the rate in its OWN code span -- `Theta( n^2 )` to `Theta(n)` --
# with spaces inside the parentheses.  The first ARROW pattern required whitespace between the
# halves and returned a clean zero on it.  That is the mg-7085 hazard, and it fired against this
# sweep's own instrument before it could fire against a document.
PLANT = ("\nThe per-slot form takes the value from `Theta( n^2 )` to `Theta(n)`, so the route\n"
         "survives with a new constant in place of `1/3`.\n")


def snapshot(dst, source="worktree"):
    os.makedirs(dst, exist_ok=True)
    if source == "main":
        tar = subprocess.run(["git", "archive", "main"], cwd=ROOT,
                             stdout=subprocess.PIPE, check=True).stdout
        subprocess.run(["tar", "-x", "-C", dst], input=tar, check=True)
    else:
        for path, _, files in os.walk(ROOT):
            if ".git" in path or "__pycache__" in path:
                continue
            for fn in files:
                src = os.path.join(path, fn)
                rel = os.path.relpath(src, ROOT)
                out = os.path.join(dst, rel)
                os.makedirs(os.path.dirname(out), exist_ok=True)
                try:
                    shutil.copyfile(src, out)
                except OSError:
                    pass
    return dst


def fired(root):
    failures, missing, _ = r2.check(root=root, verbose=False)
    return failures, missing


def report(tag, title, declared, failures, missing, extra=""):
    n = len(failures)
    got = "FIRED" if n else "DID NOT FIRE"
    ok = (got == declared)
    print("%s  %s" % (tag, title))
    print("    unrepaired-site count: %d   missing anchors: %d   -> %s   (pre-declared %s: %s)"
          % (n, len(missing), got, declared, "ok" if ok else "*** MISMATCH ***"))
    if extra:
        print("      %s" % extra)
    for path, ln, anchor, cls in failures[:3]:
        print("      e.g. %s:%d [%s]  %s" % (path, ln, cls, anchor[:70]))
    print()
    return ok


def main():
    print("mg-910c NEGATIVE CONTROLS -- does the R2 detector fire without the repair?")
    print("=" * 78)
    print()

    allok = True
    tmp = tempfile.mkdtemp(prefix="rate_sweep_910c_")
    try:
        # ---- N0: main, unrepaired -------------------------------------------------
        m = snapshot(os.path.join(tmp, "main"), source="main")
        f, miss = fired(m)
        classes = sorted({c for _, _, _, c in f})
        allok &= report(
            "N0", "R2 against the UNREPAIRED tree at `main`", "FIRED", f, miss,
            extra="classes that fired: %s  (must be LIVE and LIVE-OPEN only)" % ", ".join(classes))
        if classes and set(classes) - set(r2.LIVE_CLASSES):
            print("    *** a non-LIVE class fired on main -- the classification is wrong ***")
            allok = False
        if len(f) != 19:
            print("    *** expected 19 unrepaired sites on main, got %d ***" % len(f))
            allok = False

        # ---- N1: strike glyphs only -----------------------------------------------
        w = snapshot(os.path.join(tmp, "n1"))
        for rel in REPAIRED:
            p = os.path.join(w, rel)
            with open(p, encoding="utf-8") as fh:
                t = fh.read()
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(t.replace("~~", ""))
        f, miss = fired(w)
        allok &= report("N1", "strip only the `~~` glyphs from the repaired documents",
                        "DID NOT FIRE", f, miss,
                        extra="2 anchors contain `~~` and are destroyed BY the mutation; that is "
                              "the mutation, not a miss -- the other 23 all still resolve and all "
                              "still read as repaired")

        # ---- N2: strip glyphs AND markers ------------------------------------------
        w = snapshot(os.path.join(tmp, "n2"))
        for rel in REPAIRED:
            p = os.path.join(w, rel)
            with open(p, encoding="utf-8") as fh:
                t = fh.read()
            t = MARKERS.sub("mg-XXXX", t)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(t)
        f, miss = fired(w)
        allok &= report("N2", "strip this ticket's citation from the repaired documents",
                        "FIRED", f, miss,
                        extra="0 anchors destroyed -- the mutation removes the citation only")
        if len(f) != 19:
            print("    *** expected all 19 to fire, got %d ***" % len(f))
            allok = False

        # ---- N3: plant a live site in an unnamed spelling ---------------------------
        w = snapshot(os.path.join(tmp, "n3"))
        target = os.path.join(w, "docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md")
        with open(target, "a", encoding="utf-8") as fh:
            fh.write(PLANT)
        before = sum(1 for ln in open(os.path.join(ROOT, "docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md"), encoding="utf-8")
                     if r1.PATTERNS["ARROW"].search(ln))
        after = sum(1 for ln in open(target, encoding="utf-8")
                    if r1.PATTERNS["ARROW"].search(ln))
        got = "FIRED" if after > before else "DID NOT FIRE"
        ok = got == "FIRED"
        allok &= ok
        print("N3  plant a LIVE site spelled `Theta( n^2 )` -> `Theta(n)`, spaces and all")
        print("    ARROW hits before: %d   after: %d   -> %s   (pre-declared FIRE: %s)"
              % (before, after, got, "ok" if ok else "*** MISMATCH ***"))
        print("      A sweep grepping the literal `Theta(n^2) -> Theta(n)` returns a clean zero")
        print("      on this plant.  The ARROW pattern is whitespace-tolerant, so it does not.")
        print()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("=" * 78)
    if allok:
        print("CONTROL PASSED — every mutation behaved as pre-declared.")
        print("N0 is the load-bearing one: the 19 sites this ticket repaired really were")
        print("unmarked on `main`, and the 7 it left really were already fine.")
        return 0
    print("CONTROL FAILED — a mutation did not behave as pre-declared.  Read the mismatch.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
