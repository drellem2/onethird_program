"""mg-7ae5 / A4 — HAS THIS BEEN SAID, AND HAS THE STEP BEEN ATTEMPTED?

Two jobs, and they are different:

  (1) NOVELTY of this document's own claims — the decomposability identity, the
      minimality consequence, the density-stratified ceiling, the margin.
  (2) PRICING evidence: is (T) a lemma NOBODY HAS ATTEMPTED, or a known-hard
      object?  The corpus is the only place that can be checked here, and what
      a grep can establish is bounded — it can show a PHRASE is absent, never
      that a STATEMENT is (STATE.md:29's limit on mg-145f's corpus search).

Every decisive pattern prints EVERY raw hit.  Adjudication is by reading and
happens in the deliverable, not here.  Files: *.md, *.tex, *.html under the
repository root, excluding this instrument's own directory.
"""

import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SELF = os.path.join('code', 'absent_step_7ae5')

PATTERNS = [
    ('DECISIVE', 'decomposability identity: Delta_1 = 0 <=> ordinal sum',
     r'Delta_1 *= *0|\\Delta_1 *= *0|Δ₁ *= *0'),
    ('DECISIVE', 'minimal counterexample is ordinal-sum INDECOMPOSABLE',
     r'(minimal|counterexample)[^.\n]{0,80}(indecomposab|not decomposab|decomposab)'),
    ('DECISIVE', 'delta of an ordinal sum = max of the sides',
     r'delta[^.\n]{0,40}(ordinal sum|oplus|\(\+\))|(ordinal sum|oplus)[^.\n]{0,40}delta'),
    ('DECISIVE', 'the density-stratified eps_0 ceiling',
     r'(density|d *>=|d *≥)[^.\n]{0,60}(eps_0|ε₀|varepsilon_0)|'
     r'(eps_0|ε₀|varepsilon_0)[^.\n]{0,60}(density|incomparability density)'),
    ('DECISIVE', 'the margin (n+1)^2/(n^2-n) or (n+1)/(n-1)',
     r'\(n\+1\)\^?2? */ *\(n\^?2? *- *n\)|\(n\+1\)/\(n-1\)'),
    ('DECISIVE', 'the transfer named as the CURRENCY CROSSING of the chain',
     r'currency[^.\n]{0,60}(cross|change)|cross[^.\n]{0,30}currenc'),
    ('NON-DECISIVE', 'the word "frozen-conditional"', r'frozen-conditional'),
    ('NON-DECISIVE', 'attempts ON L4 / the transfer', r'(attempt|prove|proof of)[^.\n]{0,20}L4'),
    ('NON-DECISIVE', 'near-ordinal-sum stability', r'near-ordinal-sum'),
]


def corpus_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d != '.git']
        rel = os.path.relpath(dirpath, ROOT)
        if rel.startswith(SELF):
            continue
        for f in filenames:
            if f.endswith(('.md', '.tex', '.html')):
                out.append(os.path.join(dirpath, f))
    return sorted(out)


files = corpus_files()
rev = subprocess.run(['git', '-C', ROOT, 'rev-parse', '--short', 'HEAD'],
                     capture_output=True, text=True).stdout.strip()

print("=" * 78)
print("mg-7ae5 / A4 — NOVELTY AND ATTEMPT SWEEP")
print("=" * 78)
print("corpus: %d .md/.tex/.html files at %s, excluding %s/" % (len(files), rev, SELF))

for kind, label, pat in PATTERNS:
    rx = re.compile(pat, re.I)
    hits = []
    for path in files:
        try:
            with open(path, encoding='utf-8', errors='replace') as fh:
                for i, line in enumerate(fh, 1):
                    if rx.search(line):
                        hits.append((os.path.relpath(path, ROOT), i, line.strip()))
        except OSError:
            pass
    print("\n%s — %s" % (kind, label))
    print("  raw hits: %d" % len(hits))
    if kind == 'DECISIVE':
        for (p, i, line) in hits[:40]:
            print("    %s:%d  %s" % (p, i, line[:150]))
        if len(hits) > 40:
            print("    ... %d more (this pattern is too broad to adjudicate by "
                  "reading; treated as NON-DECISIVE in the deliverable)" % (len(hits) - 40))
    else:
        seen = {}
        for (p, i, line) in hits:
            seen[p] = seen.get(p, 0) + 1
        for p in sorted(seen, key=lambda x: -seen[x])[:12]:
            print("    %-70s %d" % (p, seen[p]))

print("""
WHAT THIS CAN AND CANNOT ESTABLISH, kept rather than dropped.
A grep establishes that a PHRASE is absent.  It cannot establish that a
STATEMENT is absent — STATE.md:29's limit on mg-145f's corpus search, which it
marks 'NOT A LEDGER KIND AT ALL'.  Every count above is DOCUMENTARY, at this
commit, over this file set, and the pricing verdict in the deliverable rests on
the READING of the hits, not on the counts.""")
