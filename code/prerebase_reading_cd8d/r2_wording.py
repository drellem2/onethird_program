#!/usr/bin/env python3
"""mg-cd8d r2 — THE SURVIVING HALF OF mg-99f4, TURNED FROM AN ANECDOTE INTO A COUNT.

mg-99f4 reported that its row on mg-9876's §3 — `a committed transcript records a demonstrated
failure` — went 149 -> 150 for a reason the row's own wording does not describe: not one of its
three committed `out_*.txt` carried a RED_TOKEN, and the hit was in `PREDICTIONS.md`.  It
reported that and did NOT repair it, because the row is mg-9876's and a branch that quietly
re-scoped another instrument's detector to make its own row read better would be doing the
worse thing.  That restraint is carried here unchanged: nothing in mg-9876 is edited.

WHAT IS NEW IS THE DENOMINATOR.  One instance says the wording CAN come apart from the class;
it does not say how often it does, and `how often` is the difference between a curiosity and a
finding about the row.  So a4's OWN `RED_TOKENS` is run over every directory at a PINNED commit
and each member of the row is classified by WHICH file supplied its token:

    TRANSCRIPT   at least one `out_*.txt` in the directory carries one, so the row's wording
                 describes the membership.
    NOT A TRANSCRIPT  no `out_*.txt` does, but some other tracked `.txt`/`.md` does.  The row
                 counts the directory and its wording does not describe why.  mg-99f4 is one
                 of these and is expected to be named below.

PINNED, BECAUSE THE ANSWER IS A FUNCTION OF THE CORPUS AND THE CORPUS MOVES.  The tree is
`git archive`d at lib_cd8d.AS_OF, which is the arrangement r1 uses and for the same reason: a
figure taken against a moving `origin/main` is a figure that rots, in the directory whose whole
subject is figures that rot.  So this arm's own count cannot drift, and it does not describe
today's tree — it describes one commit, and says which.

THE DETECTOR IS a4's AND NOT A RE-SPELLING OF IT (mg-d2c2).  `RED_TOKENS` and the `.txt`/`.md`
extension pair are imported from `a4_sweep`, so this arm cannot disagree with the row it is
about; if mg-9876 rewords or re-scopes its detector, this arm follows and does not argue.

EXITS 0 always.  It is a reading and not a gate.
"""

import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_cd8d as L  # noqa: E402

W = 92


def classify(code_dir):
    """(transcript-backed, not-transcript-backed) directory names, by a4's own predicate."""
    backed, unbacked = [], []
    for name in sorted(os.listdir(code_dir)):
        path = os.path.join(code_dir, name)
        if not os.path.isdir(path):
            continue
        red_out, red_other = False, False
        for root, _dirs, filenames in os.walk(path):
            for fn in sorted(filenames):
                if not fn.endswith((".txt", ".md")):
                    continue
                body = L.A.L.read(os.path.join(root, fn))
                if not L.A.RED_TOKENS.search(body):
                    continue
                if fn.startswith("out_") and fn.endswith(".txt"):
                    red_out = True
                else:
                    red_other = True
        if red_out:
            backed.append(name)
        elif red_other:
            unbacked.append(name)
    return backed, unbacked


def main():
    print("=" * W)
    print("mg-cd8d r2 — WHAT THE ROW `a committed transcript records a demonstrated failure`")
    print("            IS ACTUALLY COUNTING, AT A PINNED COMMIT")
    print("=" * W)
    print()

    L.require_commits()

    tmp = tempfile.mkdtemp(prefix="cd8d-r2-")
    try:
        tar = L._git("archive", L.AS_OF, "code")
        if tar.returncode != 0:
            raise L.Refused("git archive %s failed" % L.AS_OF)
        p = subprocess.run(["tar", "-x", "-C", tmp], input=tar.stdout, capture_output=True)
        if p.returncode != 0:
            raise L.Refused("could not extract the corpus at %s" % L.AS_OF)
        code = os.path.join(tmp, "code")
        if not os.path.isdir(code):
            raise L.Refused("the archive produced no code/ — there is nothing to classify")
        backed, unbacked = classify(code)
        population = sum(1 for n in sorted(os.listdir(code))
                         if os.path.isdir(os.path.join(code, n)))
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)

    row = len(backed) + len(unbacked)
    print("  AS_OF %s, population %d directories under code/" % (L.AS_OF, population))
    print("-" * W)
    print("  on the row (any tracked .txt/.md carries a RED_TOKEN)  : %3d of %d"
          % (row, population))
    print("    of those, at least one out_*.txt carries one         : %3d" % len(backed))
    print("    of those, NO out_*.txt does — the row counts it and  : %3d" % len(unbacked))
    print("    its wording does not describe why")
    print()
    if population < 100 or row == 0:
        print("  THE POPULATION OR THE ROW IS IMPLAUSIBLE, so the split above is a statement")
        print("  about a tree that was not read.  Do not quote it.")
        print()
    print("  THE DIRECTORIES THE ROW'S WORDING DOES NOT DESCRIBE:")
    for i in range(0, len(unbacked), 3):
        print("      " + "  ".join(n.ljust(34) for n in unbacked[i:i + 3]))
    print()
    committed = L._git("show", "%s:%s" % (L.AS_OF, L.CENSUS)).stdout.decode("utf-8", "replace")
    quoted = [ln.strip() for ln in committed.split("\n")
              if "records a demonstrated failure" in ln]
    print("  AND THIS DOES NOT CONTRADICT THE COMMITTED CENSUS, which at %s reads" % L.AS_OF)
    print("      %s" % (quoted[0] if quoted else "<the row is not in the committed copy>"))
    print("  against the %d of %d above.  The committed copy is a reading at an older"
          % (row, population))
    print("  population and mg-05c6's rule is that nobody refreshes it until the bound trips —")
    print("  which is r1's subject and is quantified there.  Two readings of one row at two")
    print("  trees are not a disagreement; taking them as one would be this ticket's own defect.")
    print()
    print("  mg-99f4's OWN DIRECTORY IS IN THAT LIST: %s"
          % ("yes" if "subset_consumability_99f4" in unbacked else "NO, and that is a "
             "disagreement with the record rather than a confirmation of it"))
    print()
    print("  WHAT THIS IS AND IS NOT.  It is a split of one row by which file supplied the")
    print("  token, using a4's own detector and a4's own extension pair.  It is NOT a claim")
    print("  that any of these directories lacks evidence its instrument can fail — several")
    print("  ship a negative control and are counted on the row ABOVE it — and it is not a")
    print("  claim the row is wrong.  The row measures `a tracked .txt or .md records a")
    print("  demonstrated failure`, which is a weaker and still useful thing than what it")
    print("  says.  REPORTED AND NOT REPAIRED: the row is mg-9876's, its wording is mg-9876's")
    print("  call, and re-scoping another instrument's detector from here is the worse thing")
    print("  even when the re-scoping would be right.")
    print()
    print("=" * W)
    print("MEASURED — %d of %d members of that row are not backed by a transcript at %s."
          % (len(unbacked), row, L.AS_OF))
    print("=" * W)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except L.Refused as exc:
        sys.stderr.write("mg-cd8d r2: REFUSED — %s\n" % exc)
        sys.exit(2)
