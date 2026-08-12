"""a3 -- the three named sites, and a term census with its own positive controls.

The ticket names three corpus sites where "alternating projection" already appears and
says: "Answer for the CLAIM, not the phrase."  This arm does two things.

  C1  Print each of the three sites with enough context to see WHAT IS BEING PROJECTED
      ONTO, and print the implementation those sites route to.  The question a reader
      must be able to settle from this output alone is: are these projections between
      TWO SUBSPACES (the note's Ran Pi_o vs Ran Pi_e, a principal-angle question), or
      between ONE SUBSPACE AND A CONE (a feasibility question)?

  C2  A term census over the whole corpus AND the two sibling repositories, for the
      vocabulary of what the note actually claims.  A census returning 0 everywhere is
      worthless unless some term returns nonzero, so POSITIVE CONTROLS are scored in
      the same table and must be nonzero: if they are not, the census is searching the
      wrong files and its zeros mean nothing.
"""

import os
import re
import subprocess

# Resolve every repo-relative path against the repository root rather than the caller's
# cwd, so this arm gives the same answer from the repo root and from its own directory.
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    os.pardir, os.pardir))
os.chdir(ROOT)

SITES = [
    ("docs/OneThird-L2-Conditionality-mg-28ff.md", 319),
    ("docs/OneThird-L2-Conditionality-mg-3bb9-RepairAudit.md", 105),
    ("code/l2_underclaim_audit_3bb9/README.md", 49),
]

IMPL = ("code/l2_underclaim_audit_3bb9/lib3bb9.py", 230, 12)

# (term, kind).  kind 'note' = vocabulary of what compression.tex claims.
#                kind 'ctrl' = positive control, MUST be nonzero somewhere.
TERMS = [
    ("alternating projection", "note"),
    ("principal angle", "note"),
    ("canonical correlation", "note"),
    ("maximal correlation", "note"),
    ("two projections", "note"),
    ("checkerboard", "note"),
    ("foliation", "note"),
    ("partial cube", "note"),
    ("even sweep", "note"),
    ("odd sweep", "note"),
    ("conditional variance", "note"),
    ("conditional expectation", "note"),
    ("block dynamics", "note"),
    ("Efron", "note"),
    ("pair-orientation", "note"),
    ("linear extension", "ctrl"),
    ("adjacent transposition", "ctrl"),
    ("hypercube", "ctrl"),
    ("spectral gap", "ctrl"),
    ("Dirichlet", "ctrl"),
]

TREES = [
    ("onethird_program (this worktree, docs+code+STATE.md)", ["docs", "code", "STATE.md"]),
    ("one_third", ["/Users/daniel/research/one_third"]),
    ("one_third_width_three", ["/Users/daniel/research/one_third_width_three"]),
]

EXCLUDE = "docs/imports/compression.tex"

# The census's own blind spot, stated rather than left implicit: one_third_width_three
# is 8.1 GB, almost all of it a Lean build tree under lean/.lake, so the search is
# restricted to source and prose extensions and those build dirs are skipped.  A term
# living only inside a compiled artifact would not be found.
INCLUDES = ["*.tex", "*.md", "*.py", "*.txt", "*.json", "*.lean", "*.html", "*.sh"]
EXCLUDE_DIRS = [".git", ".lake", "node_modules", "__pycache__"]


def count(term, roots):
    """Occurrences of `term`, case-insensitive, excluding the imported note itself and
    excluding this instrument (which necessarily contains every term in the list)."""
    tot = 0
    files = set()
    for root in roots:
        if not os.path.exists(root):
            continue
        cmd = (["grep", "-rniIF"]
               + ["--exclude-dir=%s" % d for d in EXCLUDE_DIRS]
               + (["--include=%s" % i for i in INCLUDES]
                  if os.path.isdir(root) else [])
               + ["--", term, root])
        p = subprocess.run(cmd, capture_output=True, text=True)
        for line in p.stdout.splitlines():
            path = line.split(":", 1)[0]
            if EXCLUDE in path:
                continue
            if "compression_novelty_623a" in path:
                continue
            tot += 1
            files.add(path)
    return tot, len(files)


def show(path, line, span=6):
    if not os.path.exists(path):
        print("    *** MISSING: %s" % path)
        return
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()
    lo = max(0, line - 1 - span)
    hi = min(len(lines), line + span)
    for k in range(lo, hi):
        mark = ">>" if k == line - 1 else "  "
        text = lines[k].rstrip()
        if len(text) > 150:
            text = text[:150] + " ..."
        print("    %s %5d  %s" % (mark, k + 1, text))


def main():
    print("a3 -- the three named sites, read for their CLAIM rather than their phrase")
    print()
    print("C1a -- the three sites the ticket names")
    for path, line in SITES:
        print()
        print("  %s:%d" % (path, line))
        show(path, line, 4)
    print()
    print("C1b -- the implementation all three sites route to")
    print()
    print("  %s:%d" % (IMPL[0], IMPL[1]))
    show(IMPL[0], IMPL[1], IMPL[2])
    print()

    # A mechanical read of the routed implementation, so the classification below is
    # not purely a matter of my reading it.
    src = open(IMPL[0], encoding="utf-8", errors="replace").read()
    seg = src[max(0, src.find("alternating") - 2000): src.find("alternating") + 3000]
    marks = {
        "mentions a CONE or ORTHANT": bool(re.search(r"orthant|cone|nonnegative", seg, re.I)),
        "mentions TWO subspaces": bool(re.search(r"two subspace|second subspace", seg, re.I)),
        "mentions conditional expectation": bool(re.search(r"conditional expectation|E\[.*\|", seg)),
        "mentions principal angles": bool(re.search(r"principal angle", seg, re.I)),
        "projects onto ONE span (proj())": bool(re.search(r"def proj", seg)),
    }
    print("C1c -- mechanical read of that implementation's own text")
    for k, v in marks.items():
        print("       %-38s %s" % (k, "YES" if v else "no"))
    print()
    print("       compression.tex section 4 needs: TWO subspaces (Ran Pi_o, Ran Pi_e),")
    print("       both ranges of CONDITIONAL EXPECTATIONS, compared by PRINCIPAL ANGLES.")
    print()

    print("C2 -- term census.  Extensions searched: %s" % " ".join(INCLUDES))
    print("      Dirs skipped: %s  (one_third_width_three is 8.1 GB, almost all of it"
          % " ".join(EXCLUDE_DIRS))
    print("      a Lean build tree; a term living only in a compiled artifact would")
    print("      not be found here.)")
    print("      'ctrl' rows are POSITIVE CONTROLS and must be nonzero;")
    print("      if they were zero the census would be looking at the wrong files and")
    print("      the 'note' rows' zeros would mean nothing.")
    print()
    hdr = "  %-24s %-6s" % ("term", "kind")
    for name, _ in TREES:
        hdr += " %-22s" % name.split(" ")[0]
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    ctrl_all_zero = True
    note_hits = []
    for term, kind in TERMS:
        row = "  %-24s %-6s" % (term, kind)
        tot_across = 0
        for _name, roots in TREES:
            c, nf = count(term, roots)
            tot_across += c
            row += " %-22s" % ("%d hits / %d files" % (c, nf))
        print(row)
        if kind == "ctrl" and tot_across > 0:
            ctrl_all_zero = False
        if kind == "note" and tot_across > 0:
            note_hits.append((term, tot_across))
    print()
    print("  POSITIVE CONTROLS: %s" % (
        "*** ALL ZERO -- CENSUS IS NOT SEARCHING THE CORPUS, ITS ZEROS MEAN NOTHING ***"
        if ctrl_all_zero else "nonzero, so the census reaches the corpus"))
    print("  'note' vocabulary present anywhere in the three trees: %s"
          % (", ".join("%s (%d)" % t for t in note_hits) if note_hits else "NONE"))


if __name__ == "__main__":
    main()
