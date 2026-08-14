#!/usr/bin/env python3
"""mg-372e — census of every spelling of the REFUTED per-slot constant.

The ticket named one spelling, `2/(n+1)`.  A sibling sweep tonight missed a live
defect because the live site was written another way, so this script sweeps SIX
forms and says, at every hit, WHICH FORM it matched.  The count this prints is a
count of TEXTUAL OCCURRENCES OF A SPELLING, not of defects: classification into
LIVE / CITED / DERIVED is done by hand and recorded in the verdict, because no
regex can tell "the programme has this value" from "this value is refuted".

Forms swept
  EPS   `2/(n+1)` and spaced/LaTeX renderings   -- eps_spec normalisation
  EINV  `(n-1)/3`                               -- the SAME conjecture in E[inv] units
  DQ    `2/(3n)`                                -- the SAME conjecture in d*qbar units
  PROSE `two over n plus one`, `per-slot constant`

COLLISION: `1 - lambda_std(W_n) <= 2/(n+1)` is the Cheeger bound on the witness
poset W_n = C_n + C_1 and is a DIFFERENT QUANTITY that happens to be the same
expression.  A blanket edit on the string would have corrupted it.  Flagged, not
counted as a site.

PINNED AT ONE COMMIT SINCE mg-528e.  The corpus was `os.walk(ROOT)` -- the
working tree, including files git never tracked and excluding the ones a
`git clean` had taken -- so this census was a function of when you ran it and of
whose checkout you ran it in.  It reads `lib372e.AS_OF` now.  Two things follow
and both are in the README: the count STOPS MOVING, and the COLLISION list below
is PERMUTED against the committed one, because `os.walk` emits
directory-enumeration order and git sorts (mg-0e77's R3, met on real data).
"""
import re
import sys

import lib372e

ROOT = lib372e.ROOT

FORMS = [
    ("EPS",   re.compile(r"2\s*/\s*\(\s*n\s*[+]\s*1\s*\)|\\[dt]?frac\{2\}\{n\s*[+]\s*1\}")),
    ("EINV",  re.compile(r"\(\s*n\s*[-−]\s*1\s*\)\s*/\s*3")),
    ("DQ",    re.compile(r"2\s*/\s*\(\s*3\s*n\s*\)")),
    ("PROSE", re.compile(r"two over n plus one|per-slot constant", re.I)),
]

# a hit is a COLLISION when the line is about the spectral gap of a named poset
COLLISION = re.compile(r"lambda_std|λ_std|Φ\^?\*|Cheeger|W_n|W_m|n\(n\s*[-−]\s*1\)")

def main():
    hits = []
    for path, lines in lib372e.corpus():
        for i, line in enumerate(lines, 1):
            for name, pat in FORMS:
                if pat.search(line):
                    kind = "COLLISION" if COLLISION.search(line) else name
                    hits.append((path, i, name, kind))

    print("mg-372e CENSUS — occurrences of the refuted per-slot constant, by spelling")
    print("=" * 78)
    print()
    lib372e.banner()
    print("What this is a count of: TEXTUAL OCCURRENCES of one of six spellings,")
    print("one row per (file, line, form).  A line matching two forms counts twice,")
    print("once per form.  It is NOT a count of defects.")
    print()

    by_form = {}
    for _, _, form, _ in hits:
        by_form[form] = by_form.get(form, 0) + 1
    print("-- by spelling --")
    for name, _ in FORMS:
        print(f"   {name:6s} {by_form.get(name, 0):4d}")
    print(f"   {'TOTAL':6s} {len(hits):4d}")
    print()

    coll = [h for h in hits if h[3] == "COLLISION"]
    print(f"-- flagged COLLISION (different quantity, same expression): {len(coll)} --")
    for path, ln, form, _ in coll:
        print(f"   {path}:{ln}  [{form}]")
    print()

    print("-- by file (docs/ and STATE.md first; code/ is instrument evidence) --")
    order = {}
    for path, ln, form, kind in hits:
        order.setdefault(path, []).append((ln, form, kind))

    def rank(p):
        return (0 if p == "STATE.md" else 1 if p.startswith("docs/") else 2, p)

    for path in sorted(order, key=rank):
        rows = order[path]
        forms = sorted({f for _, f, _ in rows})
        print(f"   {len(rows):4d}  {path}   ({'+'.join(forms)})")
    print()
    print(f"files carrying at least one spelling: {len(order)}")
    print(f"  of which docs/: {sum(1 for p in order if p.startswith('docs/'))}")
    print(f"  of which code/: {sum(1 for p in order if p.startswith('code/'))}")

    # the HTML twin, checked by name because it has been stale before (mg-9bc2)
    twin = "docs/state-of-the-wall.html"
    print()
    print("-- the HTML twin, checked by name --")
    if not lib372e.exists(twin):
        print("   docs/state-of-the-wall.html: ABSENT")
        return 1
    n = len(order.get(twin, []))
    print(f"   docs/state-of-the-wall.html: {n} occurrences of any swept spelling")
    if n == 0:
        print("   -> NOT a site.  It is a 2026-07-19 rendering that predates mg-200d")
        print("      entirely and never carried the formula; it says so in its own banner.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
