"""T3 -- the census, the copies of `A2 TOTAL BAD`, and the SOURCE.

Three questions, and none of them is answered by asking the copies:

  1. RE-DERIVE THE CENSUS INDEPENDENTLY.  "8 short" is mg-4700's number and
     mg-5040 accepted it.  It is re-computed here from `git ls-tree` at four
     named revisions, by this file, with the population written out.
  2. WERE ALL THE COPIES CORRECTED, AND IS THERE A FOURTH?  mg-5040 says the
     ticket's "three commit messages" was itself wrong: TWO messages, one
     document, and a published transcript as the fourth.  That enumeration is
     redone here over a WIDER population -- every commit object reachable
     from every ref, not from the pin -- because this history carries REBASE
     TWINS and a message counted once exists twice.
  3. FIND THE SOURCE, NOT THE COPIES.  Agreement among copies is worth
     nothing when they share a source, so what is counted here is INDEPENDENT
     DERIVATIONS: artifacts that are the transcript of a RUN of the checker
     that prints the figure, as against artifacts that quote one.

T3a  the census, re-derived at four revisions
T3b  what the committed transcripts CLAIM at those revisions
T3c  committed transcripts that state a figure with NO revision named
T3d  every commit-message object stating a figure, with its twins
T3e  every committed file stating a figure, with a disposition
T3f  independent derivations

    python3 code/species_bound_audit_6ef4/t3_census.py
"""

import os
import re
import sys

from kern6ef4 import hdr, REPO, git

bad = 0
missed = 0

REVS = [
    ("e8fbd4f", "mg-d633 wrote the census"),
    ("af432ee", "mg-821e REGENERATED it"),
    ("4372fae", "the pin -- the tree mg-821e's summaries shipped in"),
    ("HEAD", "the tree this audit runs in"),
]

TAG = "A2 TOTAL BAD"
# `A2 TOTAL BAD` followed by a number, allowing the words a summary puts
# between them.  Derived here rather than copied from mg-5040's r3, so that
# the two counts are two measurements and not one measurement twice.
FIG = re.compile(r"A2 TOTAL BAD[^0-9\n]{0,30}?(\d+)")
# THE CENSUS SENTENCE, AND ONLY IT.  `N markdown file(s)` occurs in this
# repository in three unrelated senses -- e2's own extent line, mg-6cb9's
# quotation of a committed copy of that line, and an instrument DECLARING how
# many markdown files IT contributes.  A bare `(\d+) markdown file\(s\)` pulls
# all three into one column and turns a census audit into noise, so the two
# spellings that state a census are matched and nothing else is.
CENSUS = re.compile(
    r"(?:EXTENT OF THIS NUMBER\.\s+|out_e2_crosssection\.txt says\s+)"
    r"(\d+)\s+markdown file\(s\)")
ANCHORED = re.compile(r"MEASURED AT [0-9a-f]{7}")


def row(label, ok, detail=""):
    global bad
    bad += (not ok)
    print("  %-64s %s" % (label[:64], "ok" if ok else "*** FINDING ***"))
    if detail:
        for ln in detail.splitlines():
            print("        %s" % ln)


def note(label, value):
    print("  %-64s %s" % (label[:64], value))


def score(pid, predicted, got):
    global missed
    hit = predicted == got
    missed += (not hit)
    print("  %-6s predicted %-24s got %-24s %s"
          % (pid, str(predicted), str(got), "" if hit else "*** MISSED ***"))
    return hit


def tree_paths(rev):
    code, out = git(["ls-tree", "-r", "--name-only", rev])
    if code != 0:
        raise RuntimeError("ls-tree %s failed" % rev)
    return out.splitlines()


def census(rev):
    """THE POPULATION, WRITTEN OUT: every tracked path at `rev` that ends in
    `.md` and sits under `docs/` or under `code/`.  That is the population
    `e2_crosssection.py` prints a count of, computed from the tree object
    instead of from a walk of the worktree -- so no probe, no untracked file
    and no instrument of this ticket can move it."""
    return sorted(p for p in tree_paths(rev)
                  if p.endswith(".md")
                  and (p.startswith("docs/") or p.startswith("code/")))


def blob(rev, path):
    code, out = git(["show", "%s:%s" % (rev, path)])
    return out if code == 0 else None


# ---------------------------------------------------------------------------
# T3a  THE CENSUS, RE-DERIVED
# ---------------------------------------------------------------------------
hdr("T3a  THE CENSUS, RE-DERIVED FROM `git ls-tree` AT FOUR REVISIONS")

print("  POPULATION: every TRACKED path ending `.md` under docs/ or code/,")
print("  at the named revision.  Not a walk of the worktree: this")
print("  instrument's own markdown sits under code/ and would perturb the")
print("  number it is measuring (mg-4700's kept defect 3).")
print()

HELD = {}
for rev, what in REVS:
    HELD[rev] = census(rev)
    print("      %-8s %-46s %3d file(s)" % (rev, what, len(HELD[rev])))
print()
score("P3a", 131, len(HELD["af432ee"]))
score("P3b", 105, len(HELD["e8fbd4f"]))
score("P3c", True, len(HELD["HEAD"]) >= 155)


# ---------------------------------------------------------------------------
# T3b  WHAT THE COMMITTED TRANSCRIPTS CLAIMED
# ---------------------------------------------------------------------------
hdr("T3b  CLAIMED vs HELD -- the committed transcript at each revision")

print("  For each revision, every tracked file at that revision containing")
print("  the sentence `N markdown file(s)` is found and its figure read.")
print("  Nothing is taken from a commit message here.")
print()

CLAIMS = {}
for rev, _what in REVS:
    found = []
    for p in tree_paths(rev):
        if not (p.endswith(".txt") or p.endswith(".md")):
            continue
        text = blob(rev, p)
        if not text:
            continue
        for m in CENSUS.finditer(text):
            found.append((p, int(m.group(1))))
    CLAIMS[rev] = found
    held = len(HELD[rev])
    for p, n in found:
        print("      %-8s %-52s claims %3d  holds %3d  %s"
              % (rev, p[-52:], n, held,
                 "SHORT BY %d" % (held - n) if n != held else "agrees"))
    if not found:
        print("      %-8s (no committed file states a census figure)" % rev)
print()
af = [n for _p, n in CLAIMS["af432ee"]]
row("mg-821e's regenerated census agrees with the tree it shipped in",
    all(n == len(HELD["af432ee"]) for n in af) if af else True,
    "claimed %s, held %d.  mg-4700's F3 re-derived independently: the number\n"
    "is not taken from mg-4700 and it comes out the same."
    % (af, len(HELD["af432ee"])))


# ---------------------------------------------------------------------------
# T3c  TRANSCRIPTS THAT STATE A FIGURE WITH NO REVISION NAMED
# ---------------------------------------------------------------------------
hdr("T3c  STALE vs WRONG -- which committed census figures name a revision")

print("  mg-5040's repair to F3 is that `e2` now prints `MEASURED AT <rev>`")
print("  beside the count, so a committed copy goes STALE rather than WRONG:")
print("  git cannot move the revision, so the sentence stays true of the tree")
print("  it names.  That protects transcripts written AFTER it.  This asks")
print("  how many committed transcripts at HEAD are NOT protected.")
print()

unanchored, anchored = [], []
for p in tree_paths("HEAD"):
    if not (p.endswith(".txt") or p.endswith(".md")):
        continue
    text = blob("HEAD", p)
    if not text or not CENSUS.search(text):
        continue
    (anchored if ANCHORED.search(text) else unanchored).append(
        (p, [int(m.group(1)) for m in CENSUS.finditer(text)]))

print("      anchored (say MEASURED AT <rev>):   %d" % len(anchored))
for p, ns in anchored:
    print("          %-58s %s" % (p[-58:], ns))
print("      UNANCHORED (a bare number):         %d" % len(unanchored))
for p, ns in unanchored:
    print("          %-58s %s  held at HEAD: %d"
          % (p[-58:], ns, len(HELD["HEAD"])))
print()
row("every committed census figure at HEAD names the revision it counts",
    not unanchored,
    "%d do not.  For those the sentence is WRONG at HEAD and not STALE, and\n"
    "no reader can tell which tree they were true of.  The repair is\n"
    "forward-only, which is a fair thing for a repair to be -- and the\n"
    "population it does not cover is not named anywhere in mg-5040."
    % len(unanchored))
score("P3d", True, len(unanchored) >= 1)


# ---------------------------------------------------------------------------
# T3d  EVERY COMMIT-MESSAGE OBJECT STATING A FIGURE
# ---------------------------------------------------------------------------
hdr("T3d  EVERY COMMIT MESSAGE STATING A FIGURE FOR `%s`" % TAG)

print("  POPULATION: every commit object reachable from EVERY ref")
print("  (`git rev-list --all`), not from the pin.  mg-5040 enumerated from")
print("  the pin and reported TWO messages.  This history is rebased by a")
print("  merge queue, so one authored message can exist as several commit")
print("  OBJECTS -- and a count of objects and a count of texts are different")
print("  numbers that a single figure cannot carry.")
print()

# `--no-walk` was in this call and had to come out: with `--all` it lists the
# REF TIPS, 123 of them, and calls that "every commit reachable from every
# ref".  The population sentence would have been false about the population
# the instrument actually took, in the section about populations.  Kept in
# OUTCOMES.md.
code, out = git(["log", "--all", "--format=%H%x1e%B%x1f"])
records = [r for r in out.split("\x1f") if "\x1e" in r]
objects, texts = [], {}
for rec in records:
    sha, msg = rec.split("\x1e", 1)
    sha = sha.strip()
    figs = FIG.findall(msg)
    if not figs:
        continue
    subject = msg.strip().splitlines()[0]
    objects.append((sha[:7], figs, subject))
    texts.setdefault(msg.strip(), []).append(sha[:7])
note("commit objects examined", len(records))

for sha, figs, subject in sorted(objects, key=lambda x: x[2]):
    print("      %-8s says %-10s %s" % (sha, ",".join(figs), subject[:52]))
print()
note("commit OBJECTS stating a figure", len(objects))
note("distinct message TEXTS", len(texts))
twins = {t: s for t, s in texts.items() if len(s) > 1}
note("texts existing as more than one object (rebase twins)", len(twins))
for t, s in twins.items():
    print("          %s   %s" % (", ".join(s), t.splitlines()[0][:48]))
print()
row("mg-5040's count of message-side copies is a count of objects",
    len(objects) == len(texts),
    "%d objects, %d texts.  mg-5040 reported the figure as 'two commit\n"
    "messages'.  Neither number is wrong; the sentence does not say which\n"
    "one it is, and in a rebased history they are not the same -- which is\n"
    "the population question this arc raises against everybody else."
    % (len(objects), len(texts)))
score("P3e", True, len(objects) >= 4)
score("P3f", 3, len(texts))


# ---------------------------------------------------------------------------
# T3e  EVERY COMMITTED FILE STATING A FIGURE, WITH A DISPOSITION
# ---------------------------------------------------------------------------
hdr("T3e  EVERY COMMITTED FILE AT HEAD STATING A FIGURE, AND ITS DISPOSITION")

# A figure is CORRECTED where the same file says so within six lines -- the
# window is stated so it can be argued with, and every disposition is printed
# whether or not it is convenient.
MARK = re.compile(r"CORRECTED|correction|WRONG|MISSED|\*\*\*|is \*\*2\*\*"
                  r"|remains|stays|prediction", re.I)
files = []
for p in tree_paths("HEAD"):
    text = blob("HEAD", p)
    if not text or TAG not in text:
        continue
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        m = FIG.search(ln)
        if not m:
            continue
        near = "\n".join(lines[max(0, i - 6):i + 7])
        files.append((p, i + 1, int(m.group(1)), bool(MARK.search(near))))

for p, ln, n, marked in files:
    print("      %-56s:%-5d says %s   %s"
          % (p[-56:], ln, n,
             "marked" if marked else "*** BARE ***"))
print()
bare = [f for f in files if not f[3] and f[2] == 1]
note("occurrences of the figure in committed files at HEAD", len(files))
note("of those, stating the OLD figure with nothing beside it", len(bare))
for p, ln, n, _m in bare:
    print("          %s:%d" % (p, ln))
row("no committed file at HEAD states the old figure bare", not bare,
    "See the list above.  These are inside this repository at HEAD, and each\n"
    "one is a place a reader meets `%s 1` with nothing next to it." % TAG)
score("P3h", True, len(bare) >= 1)


# ---------------------------------------------------------------------------
# T3f  INDEPENDENT DERIVATIONS
# ---------------------------------------------------------------------------
hdr("T3f  HOW MANY TIMES WAS THE FIGURE ACTUALLY DERIVED?")

print("  An artifact DERIVES the figure if it is the transcript of a run of")
print("  `a2_crosssection.py` -- it carries that script's OWN section")
print("  headings.  Everything else QUOTES.")
print()
print("  THE MARKERS ARE TAKEN FROM THE PRODUCER'S SOURCE, not written out")
print("  here.  mg-5040 kept as its defect 4 that a hand-written rule")
print("  excluded the one artifact its section was about; a list of headings")
print("  read out of `a2_crosssection.py` cannot drift from what that script")
print("  prints.  AND TWO DIFFERENT CHECKERS IN THIS REPOSITORY PRINT")
print("  `%s`: mg-a61f's `a2_bidigare.py` prints it as its own" % TAG)
print("  verdict, about something else entirely.  Its transcripts are")
print("  reported separately rather than counted, because a name collision")
print("  is not a disagreement.")
print()

A2SRC = "code/species_extent_audit_6cb9/a2_crosssection.py"
src = blob("HEAD", A2SRC) or ""
# Every string literal this script can print VERBATIM: long enough not to
# collide by accident, and free of format specifiers and escapes so that what
# is searched for is what would appear on stdout.
MARKERS = sorted({s for s in re.findall(r'"([^"\n]{28,})"', src)
                  if "%" not in s and "\\" not in s})
THRESHOLD = max(3, len(MARKERS) // 4)
print("      markers lifted from %s: %d" % (A2SRC, len(MARKERS)))
for m in MARKERS[:3]:
    print("          %s" % m[:66])
print("      a file counts as a DERIVATION at >= %d of them (a quarter).  The"
      % THRESHOLD)
print("      marker count is printed for every candidate below, so the")
print("      threshold can be argued with instead of taken on trust -- and")
print("      the two populations are not close together.")
print()

derivations, foreign, quoters = [], [], []
for p in tree_paths("HEAD"):
    if p == A2SRC:
        continue
    text = blob("HEAD", p)
    if not text or not FIG.search(text):
        continue
    hits = sum(1 for m in MARKERS if m in text)
    if hits >= THRESHOLD:
        derivations.append((p, FIG.findall(text)[0], hits))
    elif re.search(r"^A2 TOTAL BAD:", text, re.M):
        foreign.append((p, FIG.findall(text)[0], hits))
    elif hits:
        quoters.append((p, FIG.findall(text)[0], hits))

for p, n, h in derivations:
    print("      DERIVES  %-52s says %s   (%d markers)" % (p[-52:], n, h))
for p, n, h in sorted(quoters, key=lambda x: -x[2])[:6]:
    print("      quotes   %-52s says %s   (%d markers)" % (p[-52:], n, h))
for p, n, h in foreign:
    print("      OTHER A2 %-52s says %s   (%d markers -- a different "
          "checker's verdict)" % (p[-52:], n, h))
print()
vals = sorted(set(n for _p, n, _h in derivations))
note("independent derivations of a2_crosssection's figure", len(derivations))
note("distinct values among them", vals)
note("transcripts of a DIFFERENT checker printing the same tag", len(foreign))
print()
row("the derivations of this figure agree with each other", len(vals) <= 1,
    "Values found: %s.  Two transcripts of the SAME checker sit in this\n"
    "repository saying different numbers.  The one every commit message\n"
    "copied says %s; the other was committed FIRST and says %s, and nothing\n"
    "in the arc compares them.  That is the answer to 'find the source, not\n"
    "the copies': there is ONE source for the figure that spread, a second\n"
    "derivation contradicting it was already in the tree, and agreement\n"
    "among the copies was never evidence about either."
    % (vals, "1" if "1" in vals else "?", "2" if "2" in vals else "?"))
print()
print("  REPLICATION IS NOT CORROBORATION.  %d copies of this figure exist"
      % (len(objects) + len(files)))
print("  in this repository -- %d commit objects and %d file occurrences --"
      % (len(objects), len(files)))
print("  and they rest on %d derivation(s), which do not agree.  Counting the"
      % len(derivations))
print("  copies measures how often the number was TYPED, not how often it was")
print("  MEASURED.")


# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("T3 TOTAL BAD: %d" % bad)
print("T3 PREDICTIONS MISSED: %d" % missed)
print("=" * 78)
print()
print("EXTENT OF THESE NUMBERS.  The census population is every TRACKED `.md`")
print("path under docs/ or code/ at four named revisions, read from tree")
print("objects.  The figure population is every commit object reachable from")
print("every ref, plus every tracked file at HEAD.  It says NOTHING about")
print("untracked files, nothing about any figure other than `%s`," % TAG)
print("nothing about branches that have been deleted, and nothing about")
print("whether the figure itself is right -- only about how many times it was")
print("copied and how many times it was derived.")
sys.exit(1 if bad else 0)
