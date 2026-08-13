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

AS-OF PINNING, mg-20ee.  Every hit this script prints is `path:NNN` -- A LINE
NUMBER INTO A FILE THIS INSTRUMENT DOES NOT OWN, over a corpus that is the whole
repository.  Those addresses are not a property of anything mg-7ae5 established;
they are offsets into files every other ticket amends, so the transcript was
NON-REPRODUCIBLE BY CONSTRUCTION and had already gone stale.

The fix is mg-c824's, PROVEN on code/c3_audit_a94c3/a4_census.py: pin the bytes,
do not reformat the numbers.  A line number into someone else's file is a
volatile address by nature and no printing convention makes one stable; what CAN
be made stable is THE THING ADDRESSED.  So the corpus is read AT A DECLARED
COMMIT via `git ls-tree`/`git show` rather than from the working tree.

WHAT THIS DOES NOT CHANGE is what the instrument concludes: the patterns, the
hit counts' provenance, and the epilogue's scope statement are untouched.
"""

import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SELF = os.path.join('code', 'absent_step_7ae5')

# The commit whose corpus this transcript addresses.
#
# CHOSEN ON A MEASUREMENT: at this commit the committed transcript reproduces
# BYTE-IDENTICALLY (checked before one line of it was edited -- that is step 1 of
# the numbers-neutrality method passing, and it is the whole unlock).  It is the
# commit the transcript's own header already stamped.
#
# ITS REACHABILITY IS THE RESIDUAL COST, AND IT IS STATED RATHER THAN LEFT TO BE
# FOUND.  3fce8b9 is reachable from `origin/polecat-p7ae5` -- the polecat branch
# that produced this instrument -- but it is NOT AN ANCESTOR OF main: the
# refinery rebased the branch and main carries the twin 1024bc2.  The two are not
# interchangeable and the difference was MEASURED, not assumed: 1024bc2's corpus
# is 512 files against 3fce8b9's 508, and three raw-hit COUNTS move with it
# (15->18, 16->17, 49->51).  Counts are findings here, not addresses, so 1024bc2
# is the wrong pin and is recorded only as the fallback if 3fce8b9 is ever
# pruned.  If that happens this script EXITS NON-ZERO with an actionable message
# rather than falling back to a live read.
AS_OF = "3fce8b9aabcfaa37475fbc6c1f3df3ebe971753c"

# Override, for re-measuring against a different corpus: any commit-ish, or the
# literal WORKTREE.  Unset is the pinned default and is the only value that
# reproduces the committed transcript.
AT = os.environ.get("A4_NOVELTY_AT", "").strip() or AS_OF


def _git(*args):
    got = subprocess.run(["git", "-C", ROOT, *args], capture_output=True)
    if got.returncode != 0:
        raise SystemExit(
            "a4_novelty: cannot read the corpus at %s: %s\n"
            "  (A4_NOVELTY_AT=%r; unset it for the pinned run.)\n"
            "  If AS_OF itself is gone, origin/polecat-p7ae5 held it and main's\n"
            "  twin is 1024bc2 -- which is NOT equivalent: it moves three raw-hit\n"
            "  counts (15->18, 16->17, 49->51).  Re-pinning there is a\n"
            "  re-measurement and must be recorded as one."
            % (AT, got.stderr.decode("utf-8", "replace").strip(), AT))
    return got.stdout

PATTERNS = [
    ('DECISIVE', 'decomposability identity: Delta_1 = 0 <=> ordinal sum',
     r'Delta_1 *= *0|\\Delta_1 *= *0|Δ₁ *= *0'),
    ('DECISIVE', 'minimal counterexample is ordinal-sum INDECOMPOSABLE',
     r'(minimal|counterexample)[^.\n]{0,80}(indecomposab|not decomposab|decomposab)'),
    # ADDED AFTER THE FIRST RUN, AND THE REASON IS KEPT HERE RATHER THAN IN A
    # COMMIT MESSAGE.  The pattern above returned ONE hit, unrelated, and I was
    # a paragraph away from reporting 'minimal counterexamples are ordinal-sum
    # indecomposable' as new.  It is STATE.md's own glossary row 55 and
    # CONCEPTS.md:44, and I found it by READING while checking something else.
    # The grep missed it because the corpus says 'primitive' where I wrote
    # 'indecomposable'.  A vocabulary mismatch is exactly how a corpus search
    # produces a false NEW, so the repaired pattern is added and the miss is
    # published rather than quietly fixed.
    ('DECISIVE', 'the SAME fact in the corpus vocabulary: primitive / ordinal sum',
     r'primitiv[^.\n]{0,120}ordinal sum|ordinal sum[^.\n]{0,120}primitiv|'
     r'[Mm]inimal counterexamples? (are|is) primitive'),
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
    """The corpus AS OF the pinned commit.  Every `path:NNN` printed below is an
    offset into THESE bytes, so pinning the bytes is what pins the addresses."""
    if AT == "WORKTREE":
        out = []
        for dirpath, dirnames, filenames in os.walk(ROOT):
            dirnames[:] = [d for d in dirnames if d != '.git']
            rel = os.path.relpath(dirpath, ROOT)
            if rel.startswith(SELF):
                continue
            for f in filenames:
                if f.endswith(('.md', '.tex', '.html')):
                    out.append(os.path.relpath(os.path.join(dirpath, f), ROOT))
        return sorted(out)
    listing = _git("ls-tree", "-r", "--name-only", AT).decode("utf-8")
    return sorted(p for p in listing.split("\n")
                  if p.endswith(('.md', '.tex', '.html'))
                  and not p.startswith(SELF + os.sep))


def corpus_read(rel):
    if AT == "WORKTREE":
        with open(os.path.join(ROOT, rel), encoding='utf-8', errors='replace') as fh:
            return fh.read()
    return _git("show", "%s:%s" % (AT, rel)).decode('utf-8', 'replace')


files = corpus_files()
rev = AT[:7] if re.fullmatch(r"[0-9a-f]{40}", AT) else AT

print("=" * 78)
print("mg-7ae5 / A4 — NOVELTY AND ATTEMPT SWEEP")
print("=" * 78)
print("""AS-OF STAMP -- WHICH LINES BELOW ARE ADDRESSES AND WHICH ARE FINDINGS (mg-20ee)

  corpus read at : %s
      %s
      reachable from origin/polecat-p7ae5; NOT an ancestor of main, and main's
      twin 1024bc2 is not equivalent -- see a4_novelty.py's AS_OF note

  EVERY `path:NNN` BELOW IS AN ADDRESS, NOT A FINDING.  Each is an offset into a
  file this instrument DOES NOT OWN, and it moves whenever any other ticket
  amends that file.  They are valid at the commit named above and nowhere else.
  THE QUOTED LINE AFTER EACH ADDRESS IS THE PRIMARY ADDRESS -- it survives the
  file moving; the number after the colon does not.  The two are ONE OBJECT: if
  the corpus moves, expect BOTH to change together.  The same declaration covers
  the hardcoded `STATE.md:29` in this script's epilogue, which is an address into
  the same pinned corpus and is valid at the same commit.

  CORPUS-VALUED TOO, and this is stated because getting it wrong would be the
  same error one level up: the file count on the next line, EVERY `raw hits:`
  COUNT, and every per-file tally.  This instrument's corpus is THE WHOLE
  REPOSITORY, so a count of how much of it mentions a phrase measures the
  repository and not mg-7ae5 -- as A4's own closing paragraph already says
  ("Every count above is DOCUMENTARY, at this commit, over this file set").
  MEASURED, NOT ASSERTED: against HEAD this run moves 46 lines, of which 16 are
  raw-hit counts and the rest are addresses, tallies, or this block.

  WHAT IS STABLE, and it is what A4 actually concludes: the pattern set, the
  DECISIVE/NON-DECISIVE classification of each pattern, and the scope ruling in
  the closing paragraph -- that a grep can establish a PHRASE is absent and never
  that a STATEMENT is, so the pricing verdict rests on the READING of the hits
  and not on their number.  Run with no environment set and this transcript
  reproduces BYTE-IDENTICALLY, because the bytes read are pinned rather than
  live.  To ask the same questions of the CURRENT corpus instead:

      A4_NOVELTY_AT=HEAD python3 a4_novelty.py    (or =WORKTREE, or any commit)

  which RE-MEASURES AND RE-ADDRESSES.  Compare the two runs' CLASSIFICATIONS; the
  counts and the numbers after the colons are expected to differ, and their
  differing is not a defect in either run.
""" % (AT, "AS_OF, the pinned default" if AT == AS_OF else
       "OVERRIDE via A4_NOVELTY_AT -- NOT the as-of stamp " + AS_OF[:7]))
print("corpus: %d .md/.tex/.html files at %s, excluding %s/" % (len(files), rev, SELF))
print("  [a SIZE OF THE CORPUS at %s, so it is corpus-valued like the addresses "
      "and not a finding]" % rev)

# Read the pinned corpus once.  `git show` per (file, pattern) would be 10x the
# subprocesses for identical bytes; the hit lists are unaffected.
CORPUS = [(rel, corpus_read(rel).split("\n")) for rel in files]

for kind, label, pat in PATTERNS:
    rx = re.compile(pat, re.I)
    hits = []
    for rel, lines in CORPUS:
        for i, line in enumerate(lines, 1):
            if rx.search(line):
                hits.append((rel, i, line.strip()))
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
