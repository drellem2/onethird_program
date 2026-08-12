"""mg-ac0c `a3` — is `a2`'s closure arithmetic already in the corpus?

`mg-7564` §0's discipline, kept: **every raw hit of a DECISIVE pattern is printed in full and
adjudicated by READING it**, not by tuning the pattern until it agrees with me.  A grep that
returns 0 because the pattern was narrowed is not a novelty finding.

The patterns are split into two classes and the split is the honest part:

* **DECISIVE** — narrow enough that every hit can be printed and read. A `0` here means
  something, and a non-zero count is adjudicated in the deliverable.
* **NON-DECISIVE** — returns hundreds of hits on ordinary English (*"does not close"*,
  *"2×"*). These are run and their counts printed **so that nobody mistakes them for
  evidence**. They establish nothing in either direction and are labelled so.
"""

import os
import re
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DECISIVE = [
    ("the closure requirement as a formula: n/(2(n+1))",
     r"n\s*/\s*\(\s*2\s*\(\s*n\s*\+\s*1\s*\)|2\s*\(\s*n\s*\+\s*1\s*\)"),
    ("a threshold on ε₀ / ε_leak at one half",
     r"(ε₀|ε_leak|eps_leak|varepsilon_0|varepsilon_\{\\mathrm\{leak\}\})[^.\n]{0,60}(1/2\b|0\.5\b|one half)"),
    ("ε₀ pinned at 1 — the vacuous/largest-admissible end",
     r"(ε₀|ε_leak)\s*=\s*1\b"),
    ("chain (I)/(III)'s demand at ε₀ = 1, i.e. ε_dem = 1/2",
     r"ε_dem[^.\n]{0,30}(1/2\b|0\.5\b)|(1/2|0\.5)[^.\n]{0,30}ε_dem"),
    ("the dial: raising ε₀ relaxes L1b and strengthens L4",
     r"(ε₀|ε_leak)[^.\n]{0,80}(relax|loosen)[^.\n]{0,80}(strengthen|tighten|harder)"),
    ("Δ₁ ≤ 1 used as the trivial universal pin on the prefix constant",
     r"Δ₁\s*≤\s*1\b|Delta_1\s*\\le\s*1\b"),
]

NON_DECISIVE = [
    ("does not close (ordinary English)", r"never clos|cannot close|does not close"),
    ("a residual wall of 2×",             r"\b2(\.0)?\s*[x×]\b"),
    ("opposite directions",               r"opposite (way|direction)|pull(s)? (the )?other way"),
]

SKIP_DIRS = {".git", "__pycache__"}
SKIP_SELF = os.path.join("code", "downstream_constants_ac0c")


def files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        rel_dir = os.path.relpath(dirpath, ROOT)
        if rel_dir.startswith(SKIP_SELF):
            continue
        for fn in filenames:
            if fn.endswith((".md", ".tex", ".html")):
                yield os.path.join(dirpath, fn)


def sweep(rx):
    out = []
    for path in ALL:
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                for i, line in enumerate(fh, 1):
                    if rx.search(line):
                        out.append((os.path.relpath(path, ROOT), i, line.strip()))
        except OSError:
            continue
    return out


rev = subprocess.run(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"],
                     capture_output=True, text=True).stdout.strip()
ALL = sorted(files())

print("=" * 100)
print(f"a3 — NOVELTY SWEEP. Corpus at {rev}; {len(ALL)} .md/.tex/.html files searched.")
print("     This instrument's own directory is EXCLUDED (it would match everything).")
print("=" * 100)
print()
print("#" * 100)
print("# DECISIVE PATTERNS — every raw hit printed, no truncation")
print("#" * 100)
for label, pat in DECISIVE:
    hits = sweep(re.compile(pat, re.I))
    print()
    print("-" * 100)
    print(f"PATTERN: {label}")
    print(f"  regex : {pat}")
    print(f"  RAW HITS: {len(hits)}")
    for path, i, line in hits:
        print(f"    {path}:{i}")
        print(f"      {line[:240]}")

print()
print("#" * 100)
print("# NON-DECISIVE PATTERNS — counts only, and they establish NOTHING")
print("#" * 100)
print("# These match ordinary English. They are run and reported so that a reader cannot")
print("# mistake a large count for a refutation of novelty or a small one for support.")
for label, pat in NON_DECISIVE:
    hits = sweep(re.compile(pat, re.I))
    print(f"    {label:<40} raw hits: {len(hits):>5}   ← NOT EVIDENCE, either way")

print()
print("=" * 100)
print("a3 — WHAT THIS SECTION CAN AND CANNOT ESTABLISH")
print("=" * 100)
print("  It CAN establish that a PHRASE is absent. It CANNOT establish that a STATEMENT is")
print("  absent — the same limit STATE.md:29 puts on mg-145f's corpus search, which it marks")
print("  'NOT A LEDGER KIND AT ALL'. Every count above is DOCUMENTARY, at this commit, over")
print("  this file set. The adjudication of the raw hits is in the deliverable, by reading.")
