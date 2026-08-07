"""mg-910c R1 -- census of the RATE claim across the whole repo, by spelling.

The claim being swept is NOT `eps_spec = 2/(n+1)`.  That is the FORMULA, and mg-372e swept it
(13 LIVE sites struck, and it swept it correctly).  This is the RATE:

    "per-slot adjacency symmetry buys Theta(n^2) -> Theta(n)"

a DIFFERENT STRING, refuted by mg-00a1 and not reachable by mg-372e, which ran before mg-00a1
returned.  A document can carry a correct strike of the formula and assert the rate one
paragraph later; mg-6bc2 and mg-200d both did.

Six spellings, in three shapes, because one spelling is how mg-7085 left a defect alive in two
sibling scripts tonight:

  ARROW  `Theta(n^2) -> Theta(n)` and its LaTeX/unicode renderings, whitespace-tolerant
  PROSE  "quadratic to linear", "an order improvement", "no longer quadratic", "an order"
  GROWS  "a factor that grows with n" / "not a constant"  -- mg-200d's headline wording
  RATEQ  "the rate is UNKNOWN" / "the true growth" -- the rate asserted as OPEN, which is also
         now false: mg-00a1 SETTLED it.  An open-question claim is a claim.
  THETA2 a bare `Theta(n^2)`  -- the COLLISION net, deliberately over-wide
  THETA1 a bare `Theta(n)`    -- the COLLISION net, deliberately over-wide

The last two exist to be over-wide.  `Theta(n^2)` is ALSO the correct answer for other things in
this corpus -- the baseline n(n-1)/6, the two-atom law's inversion count, mg-00a1's OWN new
theorem -- and `Theta(n)` is the correct answer for the consecutive-pairs branch and for the
LIBweak mobility configurations.  A sweep that struck on the string would have struck the new
theorem.  R2 carries the hand classification that separates them.

This script COUNTS.  It does not classify and it does not repair.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

EXTS = (".md", ".html", ".tex", ".txt", ".py")

# Whitespace-tolerant.  `\^?2` catches Theta(n^2) and Theta(n2); the unicode superscript and
# the LaTeX \Theta{...} forms are folded in by the alternation on the head.
_TH = r"(?:\\?Theta|Θ)"
_N2 = r"n\s*(?:\^\s*2|²|\*\*\s*2)"
# Markup that can sit BETWEEN the two halves without changing what a reader sees.  R3's N3
# control caught this: the first version of ARROW required whitespace only, so a site written
# `Θ(n²)` → `Θ(n)` -- each half in its OWN code span -- returned a clean zero.  That is the
# mg-7085 hazard exactly, and it fired against my own pattern before it fired against a document.
_SEP = r"[\s`*_$\\{}]*"

PATTERNS = {
    "ARROW": re.compile(
        _TH + r"\s*\(\s*" + _N2 + r"\s*\)" + _SEP + r"(?:->|→|\\to|\\rightarrow|to)" + _SEP
        + _TH + r"\s*\(\s*n\s*\)", re.I),
    "PROSE": re.compile(
        r"quadratic\s+(?:to|down\s+to|into)\s+linear"
        r"|an\s+order\s+improvement"
        r"|no\s+longer\s+quadratic"
        r"|from\s+quadratic\s+to", re.I),
    "GROWS": re.compile(
        r"factor\s+that\s+grows\s+with\s+.?n"
        r"|grows\s+with\s+.?n.?,?\s*not\s+a\s+constant"
        r"|gain\s+is\s+not\s+a\s+constant\s+factor", re.I),
    "RATEQ": re.compile(
        r"(?:the\s+)?rate\s+is\s+(?:now\s+)?(?:UNKNOWN|unknown|open)"
        r"|UNKNOWN\s+rate"
        r"|true\s+growth\s+of\s+the\s+disjunctive", re.I),
    "THETA2": re.compile(_TH + r"\s*\(\s*" + _N2 + r"\s*\)", re.I),
    "THETA1": re.compile(_TH + r"\s*\(\s*n\s*\)", re.I),
}

SKIP_DIRS = {".git", "__pycache__"}


def walk():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for fn in sorted(filenames):
            if fn.endswith(EXTS):
                yield os.path.join(dirpath, fn)


def main():
    by_spelling = {k: 0 for k in PATTERNS}
    by_file = {}
    total_lines = 0

    for path in walk():
        try:
            with open(path, encoding="utf-8") as fh:
                lines = fh.read().splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        rel = os.path.relpath(path, ROOT)
        hits = {}
        for i, line in enumerate(lines, 1):
            fired = [k for k, pat in PATTERNS.items() if pat.search(line)]
            if fired:
                total_lines += 1
                for k in fired:
                    by_spelling[k] += 1
                hits.setdefault(i, fired)
        if hits:
            by_file[rel] = hits

    print("mg-910c R1 -- CENSUS OF THE RATE CLAIM, BY SPELLING")
    print("=" * 78)
    print()
    print("  spelling   line-hits   what it is")
    order = ["ARROW", "PROSE", "GROWS", "RATEQ", "THETA2", "THETA1"]
    what = {
        "ARROW": "the rate itself, `Theta(n^2) -> Theta(n)`",
        "PROSE": "the same claim in words",
        "GROWS": "mg-200d's headline wording",
        "RATEQ": "the rate asserted as UNKNOWN/OPEN -- also now false",
        "THETA2": "bare Theta(n^2)  -- OVER-WIDE, the collision net",
        "THETA1": "bare Theta(n)    -- OVER-WIDE, the collision net",
    }
    for k in order:
        print("  %-9s  %8d   %s" % (k, by_spelling[k], what[k]))
    print()
    print("  distinct lines carrying at least one spelling: %d" % total_lines)
    print("  files: %d" % len(by_file))
    print()

    docs = {f: h for f, h in by_file.items() if f.startswith("docs/")}
    code = {f: h for f, h in by_file.items() if f.startswith("code/")}
    other = {f: h for f, h in by_file.items()
             if not f.startswith("docs/") and not f.startswith("code/")}

    for label, group in (("docs/", docs), ("code/", code), ("top level", other)):
        print("-" * 78)
        print("%s -- %d file(s)" % (label, len(group)))
        for f in sorted(group):
            kinds = sorted({k for ks in group[f].values() for k in ks})
            narrow = [k for k in kinds if k not in ("THETA1", "THETA2")]
            mark = "*" if narrow else " "
            print("  %s %-64s %2d lines  %s" % (mark, f, len(group[f]), ",".join(kinds)))
    print()
    print("-" * 78)
    print("`*` marks a file hit by a NARROW spelling (ARROW/PROSE/GROWS/RATEQ), i.e. a")
    print("candidate site for the rate claim itself.  An unmarked file was reached only by")
    print("the deliberately over-wide collision nets and is almost certainly a different")
    print("quantity.  R2 carries the hand classification; this script does not classify.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
