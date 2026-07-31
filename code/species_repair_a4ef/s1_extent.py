"""S1 -- ONE LIST, EVERY TARGET, AND THE EXTENT PRINTED.

mg-73df, MAJOR: X3 -- the correction mg-f8fa's whole repair centres on -- was
still in force in `code/species_7d75/t6_fock_and_record.py` AND in the
committed `out_t6_fock_and_record.txt`, INSIDE A RUN ENDING `T6 TOTAL BAD: 0`,
because `check_doc.py` has the full list over one file and `w3_scope.py` has a
two-item list over a directory.  Every file covered, every statement covered,
NO STATEMENT COVERED IN EVERY FILE.

This file closes it the way mg-73df suggested and then does the half it did
not ask for.  The closing half: `stricken_a4ef.py` is the union of both
tables, and it is run here over the document AND all four code trees.  The
half nobody asked for: **the extent is PRINTED** -- a matrix of statements
against targets, so a reader of a passing run is told what passed, and
`S1 TOTAL BAD: 0` is a statement about a stated extent instead of an
unstated one.

  S1a  the EXTENT DECLARATION -- what this list is and what it is run over.
  S1b  the MATRIX: every correction against every target.
  S1c  the document half: every struck sentence survives only inside its
       strike, and the positive corrections are present.
  S1d  CONTROLS.  A detector only ever seen to pass is worth nothing:
         (a) the same detector at `ebecd89` -- the state mg-73df audited --
             must report MORE than it reports now, and must specifically name
             X3 in the committed output;
         (b) the same detector at `83ac472` -- before mg-f8fa -- must report
             more still, and must catch X4 and X5, the two `w3_scope` covers;
         (c) an injected statement in a scratch copy must raise the count, or
             the detector is reporting a constant;
         (d) the exoneration rule must NOT be disarmed by an adjacent
             unrelated phrase -- the false negative `w3_scope.py` recorded
             against itself and mg-73df's `c4_scope.py` reproduced against
             itself, run here as a control rather than trusted.

    python3 code/species_repair_a4ef/s1_extent.py
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

from kerna4ef import hdr, flat, scan
from stricken_a4ef import (CORRECTIONS, REQUIRED_IN_DOC, GONE_FROM_DOC,
                           TREES, EXCLUDE)

bad = 0
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
DOC = os.path.join(REPO, "docs",
                   "OneThird-Species-Hopf-Monoids-Where-This-Lives.md")
AUDITED_COMMIT = "ebecd89"      # the state mg-73df audited
PRE_F8FA_COMMIT = "83ac472"     # before mg-f8fa moved enforcement into code

# Fixtures for controls (c) and (d).  They contain a forbidden sentence ON
# PURPOSE, so they sit in a table DECLARED_TABLE names -- the same exoneration
# this file grants check_doc.py's STRICKEN and w3_scope.py's FORBIDDEN,
# applied to itself.  An exclusion that does not apply to the excluder is a
# hole, and `stricken_a4ef.py` is the ONE file this scan skips by name.
STRICKEN_FIXTURES = [
    "T5 measured it against every Hopf monoid axiom with 0 failures\n"
    "on 4399 basis elements.\n",
]

# Three ways an adjacent unrelated sentence has actually disarmed a checker in
# this arc.  The first is verbatim the one that disarmed mg-73df's c4_scope.py
# against t6_fock_and_record.py; the second is the one that disarmed
# w3_scope.py's first version against the pre-repair README.
DISARMERS = [
    "and the framework it ruled out is not the framework this ticket is "
    "about.",
    "the error mg-1953 repaired sits four lines above.",
    "this REPAIRED thing is a problem in another file entirely.",
]


# mg-d633 (mg-7dd3's BROKEN A1): THE CODE WAS WIDENED, NOT THE CLAIM NARROWED.
#
# This function used to filter on `.py/.txt/.md` BEFORE the named exclusion was
# consulted.  Four `run_all.sh` -- one in each of the four trees the extent
# names -- were therefore dropped by a rule that appeared in no extent line and
# on no printed list, while the run said "SKIPPED, NAMED, so the exclusion
# cannot grow unseen -- 5 file(s)".  A forbidden sentence planted in one of
# them exited 0.  The printed extent was WIDER THAN WHAT THE CODE READ, which
# is worse than printing none: a bare total invites the question `of what?`,
# and an extent line answers it.
#
# So the scan reads EVERY REGULAR FILE in each tree.  The only remaining
# exclusions are the five named in EXCLUDE and any file that is not decodable
# as UTF-8 text -- and the second kind is NAMED IN THE OUTPUT, one by one, as
# it is found, so it cannot grow unseen either.  There is no extension rule
# left to leave out of a sentence.
#
# mg-821e (mg-6cb9's F1, MAJOR): AND IT NOW RECURSES.  Until this ticket the
# walk was a single `os.listdir` and a `continue` past anything that is not
# `os.path.isfile`, so a SUBDIRECTORY was dropped by a rule no sentence
# carried -- word for word the defect the paragraph above describes, one level
# down.  The sentence was true, and true only because no tree under
# `code/species_*` happened to contain a directory: a claim contingent on a
# condition nobody had stated, which would have gone false silently on the day
# somebody added one.  mg-6cb9 measured it: X4 and X3 planted in
# `code/species_7d75/sub/leak.md` left this checker and `w3_scope.py` SILENT
# and `e1_extents.py` certifying the extent as TRUE.
#
# The choice was between stating the condition and removing it.  Removing it is
# strictly better -- a stated condition is a promise about the tree, and this
# repository has no way to keep one -- so the walk recurses and the claim is
# true BY CONSTRUCTION.  ONE directory rule survives and it is carried by a
# sentence, printed in the extent below: `__pycache__` is not descended into.
# It holds compiled bytecode written by these runs themselves; its contents are
# not decodable text, they are not authored, and they vary with the interpreter
# that last ran.  That rule is stated, so it can be argued with.
#
# mg-5040, on mg-4700's OPEN 1: THE SENTENCE STOPS QUANTIFYING OVER A SET THIS
# CODE ENUMERATES BY WALKING.
#
# The paragraph above is the SECOND generation of the same accident.  "EVERY
# REGULAR FILE" was true because no tree had a subdirectory (mg-6cb9 F1); the
# walk was made to recurse; it was then true because no tree had a SYMLINKED
# DIRECTORY (mg-4700 F1).  `os.walk` does not descend into one without
# `followlinks=True`, and the link lands in `dirnames`, so it is never a
# candidate file either -- a second directory rule carried by no sentence,
# invisible for exactly the reason the first one was.  A statement planted
# behind a link left this checker's scan reading 0 files below the root.
#
# EACH WIDENING BUYS EXACTLY ONE GENERATION.  Depth, then symlinks, then mount
# boundaries, then a directory this process cannot read, then whatever is
# next.  So this is not widened a third time.
#
# OF THE TWO OPTIONS mg-5040 NAMES, THIS TAKES THE FIRST: STATE THE WALK'S
# ACTUAL BOUND, so that the claim and the code describe the same set.  Not the
# second -- making a filesystem walk TOTAL means `followlinks=True` plus cycle
# detection, and it still leaves device nodes, unreadable directories and
# mount boundaries outside, which is the third widening wearing the word
# "total".
#
# A bound written in prose rots like any other copy, so it is not written in
# prose.  THE WALK RETURNS ITS OWN RESIDUE: every entry it declined, with the
# reason, WHETHER OR NOT ANYBODY THOUGHT OF THAT REASON IN ADVANCE.  The
# residue is printed beside the count, and any entry in it that is not the one
# stated rule is a FINDING that makes this run exit 1.  That is the
# subtraction: what generated the generations was not the depth rule or the
# symlink rule, it was the SILENCE, and the silence is what is removed.  The
# day a symlinked directory appears in one of these trees the sentence VISIBLY
# STOPS MATCHING instead of quietly stopping being true.
PYCACHE = "__pycache__"
STATED_DIR_RULES = (PYCACHE,)


def walk_residue(root, stated_dirs=STATED_DIR_RULES):
    """(files, stated, unstated) -- and nothing is dropped without landing in
    one of the last two.  `stated` and `unstated` are (relpath, reason) pairs.

    `os.walk` silently declines four kinds of thing: a directory named by the
    caller's own prune, a SYMLINKED directory (no `followlinks`), an entry
    that is not a regular file, and any directory it raised an error on --
    the last of which it swallows entirely unless `onerror` is given.  All
    four are returned here.  The list is not a list of the rules somebody
    remembered; it is a list of what actually happened.
    """
    files, stated, unstated = [], [], []
    if not os.path.isdir(root):
        return files, stated, unstated

    def onerror(err):
        p = getattr(err, "filename", None) or root
        unstated.append((os.path.relpath(p, root),
                         "os.walk raised %s and would otherwise have "
                         "dropped it in silence" % err.__class__.__name__))

    for dirpath, dirnames, filenames in os.walk(root, onerror=onerror):
        keep = []
        for d in sorted(dirnames):
            p = os.path.join(dirpath, d)
            rel = os.path.relpath(p, root)
            if d in stated_dirs:
                stated.append((rel, "directory rule, STATED: %s/" % d))
            elif os.path.islink(p):
                unstated.append((rel, "symlinked directory -- os.walk does "
                                      "not descend without followlinks"))
            else:
                keep.append(d)
        dirnames[:] = keep
        for f in sorted(filenames):
            p = os.path.join(dirpath, f)
            rel = os.path.relpath(p, root)
            if os.path.isfile(p):
                files.append(rel)
            elif os.path.islink(p):
                unstated.append((rel, "symlink that does not resolve to a "
                                      "regular file"))
            else:
                unstated.append((rel, "not a regular file"))
    return sorted(files), sorted(set(stated)), sorted(set(unstated))


def tree_files(root):
    """(scanned, undecodable, stated, unstated).

    Paths are relative to `root` and may contain a separator: the walk is
    RECURSIVE (mg-821e) and it NAMES WHAT IT DECLINED (mg-5040).
    """
    reached, stated, unstated = walk_residue(root)
    scanned, undecodable = [], []
    for rel in reached:
        p = os.path.join(root, rel)
        # EXCLUDE is matched on the path relative to the tree root and NOT
        # on the basename.  The five names are printed root-relative, so a
        # basename rule would make the printed list mean more than it says:
        # `sub/PREDICTIONS.md` would be dropped by a name the reader can
        # only see attached to the root.  It is read.
        if rel in EXCLUDE:
            stated.append((rel, "file rule, STATED: on the EXCLUDE list"))
            continue
        try:
            open(p, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            undecodable.append(rel)
            continue
        scanned.append(rel)
    return (sorted(scanned), sorted(undecodable), sorted(set(stated)),
            sorted(set(unstated)))


def tree_scanned(root):
    return tree_files(root)[0]


def scan_tree(root):
    """{correction_id: [(file, line)]} for everything still ASSERTED."""
    out = {}
    for f in tree_scanned(root):
        text = open(os.path.join(root, f), encoding="utf-8").read()
        for cid, _label, _doc, pats, own in CORRECTIONS:
            for ln, asserted in scan(text, pats, own):
                if asserted:
                    out.setdefault(cid, []).append((f, ln))
    return out


# ---------------------------------------------------------------------------
# S1a  the extent declaration
# ---------------------------------------------------------------------------
hdr("S1a  EXTENT DECLARATION -- what is enforced, and over what")

print("  THE LIST: %d corrections, from code/species_repair_a4ef/"
      "stricken_a4ef.py," % len(CORRECTIONS))
print("  which is the UNION of check_doc.py's %d STRICKEN rows and"
      % (len(CORRECTIONS) - 1))
print("  w3_scope.py's 2 FORBIDDEN rows, plus Y2, which is new here.")
print()
print("  THE TARGETS: the document, and %d code trees.  EVERY REGULAR FILE in"
      % len(TREES))
print("  each tree is read, AT ANY DEPTH -- there is no extension rule")
print("  (mg-d633) and no depth rule (mg-821e) --")
undecodable = []
subdirs = []
declined_stated = []
declined_unstated = []
for t in TREES:
    root = os.path.join(REPO, "code", t)
    scanned, undec, st, unst = tree_files(root)
    undecodable += [(t, f) for f in undec]
    declined_stated += [(t, r, why) for r, why in st]
    declined_unstated += [(t, r, why) for r, why in unst]
    nested = [f for f in scanned if os.sep in f]
    subdirs += [(t, f) for f in nested]
    print("      code/%-24s %3d file(s) read, %d of them below the tree root"
          % (t, len(scanned), len(nested)))
print()
print("  SKIPPED, NAMED, so the exclusion cannot grow unseen -- %d file(s):"
      % len(EXCLUDE))
for e in sorted(EXCLUDE):
    print("      %s" % e)
print("  and %d file(s) skipped as not decodable UTF-8 text, NAMED THE SAME"
      % len(undecodable))
print("  WAY rather than filtered by a rule no sentence carries:")
for t, f in undecodable:
    print("      code/%s/%s" % (t, f))
if not undecodable:
    print("      (none)")
print("  and ONE directory rule, which is the whole of the depth question:")
print("      %s/ is not descended into -- compiled bytecode these runs"
      % PYCACHE)
print("      write themselves, not authored text.  Nothing else is a")
print("      directory rule: the walk is os.walk and it recurses.")
print()
print("  THE BOUND OF 'EVERY REGULAR FILE', STATED (mg-5040, on mg-4700's")
print("  OPEN 1).  It means every regular file THE WALK ABOVE REACHED.  That")
print("  walk is os.walk WITHOUT followlinks, so it does not enter a")
print("  symlinked directory; it reads no entry that is not a regular file;")
print("  and until this ticket it dropped a directory it could not read")
print("  without saying so.  None of that is a promise about the shape of")
print("  these trees, because the walk now RETURNS EVERYTHING IT DECLINED,")
print("  with the reason, and both lists are printed here.  An entry that is")
print("  NOT the stated %s/ rule is a FINDING, counted into S1 TOTAL BAD"
      % PYCACHE)
print("  below.  So the sentence and the code describe the same set: the day")
print("  a symlinked directory appears, this run goes RED and the claim")
print("  visibly stops matching, rather than quietly stopping being true --")
print("  which is what happened twice, at mg-6cb9 F1 (no subdirectory) and")
print("  again at mg-4700 F1 (no symlinked directory).")
print("      DECLINED, STATED -- %d entr(ies):" % len(declined_stated))
for t, r, why in declined_stated:
    print("          code/%s/%s   %s" % (t, r, why))
if not declined_stated:
    print("          (none)")
print("      DECLINED, NOT STATED -- %d entr(ies):" % len(declined_unstated))
for t, r, why in declined_unstated:
    print("          code/%s/%s   %s" % (t, r, why))
if not declined_unstated:
    print("          (none -- and this line is the whole claim.  It is a")
    print("           measurement of what the walk did, not a list of the")
    print("           rules anybody remembered to write down)")
bad += len(declined_unstated)
print("  Those three lists are the WHOLE exclusion.  Until mg-d633 a fourth")
print("  existed and was printed nowhere: an extension filter that dropped the")
print("  four run_all.sh inside the four trees named above, so the extent line")
print("  claimed more than the code read (mg-7dd3 A1, BROKEN).  Until mg-821e")
print("  a FIFTH existed and was printed nowhere: this walk was a single")
print("  os.listdir, so every SUBDIRECTORY of every tree above was dropped by")
print("  a rule no sentence carried, and the sentence 'EVERY REGULAR FILE'")
print("  was true only because no tree happened to have one (mg-6cb9 F1,")
print("  MAJOR).  It is now true BY CONSTRUCTION rather than by accident of")
print("  the tree, and the count below says how many files are below a root:")
if subdirs:
    for t, f in subdirs:
        print("      code/%s/%s" % (t, f))
else:
    print("      (no tree has a file below its root today -- and if one gains")
    print("       a file tomorrow the line above will name it, which is the")
    print("       difference this ticket bought)")
print("  Note also what is NOT skipped: committed out_*.txt.  A forbidden")
print("  sentence in a committed output is precisely the defect this repair")
print("  closes.")
print()
print("  WHAT THE OTHER TWO CHECKERS COVER, STATED SO IT CANNOT BE READ AS")
print("  MORE:")
print("      check_doc.py   %2d of %d statements  x  1 file  (the document)"
      % (len(CORRECTIONS) - 1, len(CORRECTIONS)))
print("      w3_scope.py     2 of %d statements  x  1 tree  "
      "(code/species_7d75)" % len(CORRECTIONS))
print("      s1_extent.py   %2d of %d statements  x  %d trees + the document"
      % (len(CORRECTIONS), len(CORRECTIONS), len(TREES)))
print()
print("  A PASSING RUN OF EITHER OF THE FIRST TWO IS NOT COVERAGE OF THE")
print("  OTHER'S EXTENT.  That sentence is the whole of mg-73df's MAJOR.")
print()


# ---------------------------------------------------------------------------
# S1b  the matrix
# ---------------------------------------------------------------------------
hdr("S1b  EVERY CORRECTION x EVERY TREE")

found = {t: scan_tree(os.path.join(REPO, "code", t)) for t in TREES}
print("  key:  .  = the statement does not occur in that tree")
print("        ok = it occurs and every occurrence is marked as corrected")
print("        !! = STILL ASSERTED")
print()
print("  %-6s %-44s %s" % ("", "", "  ".join("%-9s" % t[8:17] for t in TREES)))
for cid, label, _doc, pats, own in CORRECTIONS:
    cells = []
    for t in TREES:
        root = os.path.join(REPO, "code", t)
        asserted = found[t].get(cid, [])
        if asserted:
            cells.append("!! x%-6d" % len(asserted))
            continue
        # present but exonerated?
        occurs = False
        for f in tree_scanned(root):
            text = open(os.path.join(root, f), encoding="utf-8").read()
            if scan(text, pats, own):
                occurs = True
                break
        cells.append("%-9s" % ("ok" if occurs else "."))
    print("  %-6s %-44s %s" % (cid, label[:44], "  ".join(cells)))
print()

total_asserted = 0
for t in TREES:
    for cid, hits in sorted(found[t].items()):
        for (f, ln) in hits:
            total_asserted += 1
            print("      STILL ASSERTED  %-6s code/%s/%s:%d" % (cid, t, f, ln))
bad += total_asserted
print()
print("  %d statement-occurrence(s) still asserted at source." % total_asserted)
print()


# ---------------------------------------------------------------------------
# S1c  the document half
# ---------------------------------------------------------------------------
hdr("S1c  THE DOCUMENT -- struck sentences struck, corrections present")

doc = open(DOC, encoding="utf-8").read()
ndoc = flat(doc)
unstruck = flat(re.sub(r"~~(.+?)~~", " ", doc, flags=re.S))

for cid, label, sentence, _pats, _own in CORRECTIONS:
    if sentence is None:
        continue
    f = flat(sentence)
    n = ndoc.count(f)
    outside = unstruck.count(f)
    ok = (n >= 1 and outside == 0)
    bad += (not ok)
    print("  %-6s %-46s occ %d  outside a strike %d  %s"
          % (cid, label[:46], n, outside,
             "ok" if ok else "*** STILL ASSERTED ***"))
print()
for label, s in REQUIRED_IN_DOC:
    ok = flat(s) in ndoc
    bad += (not ok)
    print("  %-58s %s" % (label, "ok" if ok else "*** MISSING ***"))
print()
for label, s in GONE_FROM_DOC:
    n = ndoc.count(flat(s))
    ok = (n == 0)
    bad += (not ok)
    print("  %-58s %s" % (label, "gone" if ok else "*** %d LEFT ***" % n))
print()


# ---------------------------------------------------------------------------
# S1d  controls
# ---------------------------------------------------------------------------
hdr("S1d  CONTROLS -- the detector is shown to fire, and shown not to be"
    " disarmed")

now = total_asserted


def count_at(commit, tmp):
    """Run the detector against code/species_7d75 as of `commit`."""
    tar = subprocess.run(["git", "archive", commit, "code/species_7d75"],
                         cwd=REPO, capture_output=True)
    if tar.returncode != 0:
        return None
    subprocess.run(["tar", "-x", "-C", tmp], input=tar.stdout, check=True)
    return scan_tree(os.path.join(tmp, "code", "species_7d75"))


ctl = 0
tmp = tempfile.mkdtemp(prefix="a4ef_")
try:
    for name, commit, must_catch in [
            ("(a) at %s, the state mg-73df audited" % AUDITED_COMMIT,
             AUDITED_COMMIT, ["X3", "X7"]),
            ("(b) at %s, before mg-f8fa" % PRE_F8FA_COMMIT,
             PRE_F8FA_COMMIT, ["X4", "X5"])]:
        sub = os.path.join(tmp, commit)
        os.makedirs(sub, exist_ok=True)
        hits = count_at(commit, sub)
        if hits is None:
            print("  %-46s git unavailable -- SKIPPED, and this line is the"
                  " record that it was not run" % name)
            continue
        n = sum(len(v) for v in hits.values())
        got = sorted(hits)
        ok = (n > now) and all(c in hits for c in must_catch)
        ctl += (not ok)
        print("  %-46s %2d asserted (now %d), catches %s  %s"
              % (name, n, now, ",".join(got), "ok" if ok else "*** FAILED ***"))
        if "X3" in hits:
            for (f, ln) in hits["X3"]:
                print("        and X3 there is at  %s:%d" % (f, ln))

    # (c) an injected statement must raise the count
    scratch = os.path.join(tmp, "inject", "code", "species_7d75")
    shutil.copytree(os.path.join(REPO, "code", "species_7d75"), scratch)
    with open(os.path.join(scratch, "injected.py"), "w",
              encoding="utf-8") as fh:
        fh.write('"""A file that says it, unmarked.\n\n'
                 + STRICKEN_FIXTURES[0] + '"""\n')
    n_inj = sum(len(v) for v in scan_tree(scratch).values())
    ok = n_inj == now + 1
    ctl += (not ok)
    print("  %-46s %2d asserted (now %d)                     %s"
          % ("(c) one statement injected into a scratch copy", n_inj, now,
             "ok" if ok else "*** FAILED ***"))

    # (d) the exoneration rule must not be disarmed by an adjacent unrelated
    #     phrase.  This is w3_scope.py's own recorded false negative, and
    #     mg-73df reproduced it against c4_scope.py.  Run, not trusted.
    body = STRICKEN_FIXTURES[0]
    x3pats, x3own = CORRECTIONS[1][3], CORRECTIONS[1][4]
    sub = 0
    for d in DISARMERS:
        text = body + d + "\n"
        hits = [ln for ln, a in scan(text, x3pats, x3own) if a]
        okd = bool(hits)
        sub += (not okd)
        print("  %-46s %s"
              % ("(d) not disarmed by: '%s ...'" % " ".join(d.split()[:4]),
                 "still asserted -- ok" if okd else "*** DISARMED ***"))
    # and the rule must still exonerate a marker that NAMES the repair
    text = body + "mg-a4ef corrected this: the count is per column.\n"
    hits = [ln for ln, a in scan(text, x3pats, x3own) if a]
    okm = not hits
    sub += (not okm)
    print("  %-46s %s" % ("(d) but a marker naming mg-a4ef DOES exonerate",
                          "ok" if okm else "*** DOES NOT EXONERATE ***"))
    ctl += (sub > 0)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

bad += ctl
print()

print("=" * 78)
print("S1 TOTAL BAD: %d" % bad)
print("=" * 78)
print()
print("EXTENT OF THIS NUMBER, stated because mg-73df's MAJOR is what happens")
print("when it is not: %d corrections over the document and %d code trees,"
      % (len(CORRECTIONS), len(TREES)))
print("EVERY REGULAR FILE of each AT ANY DEPTH, less the %d named above, the %d"
      % (len(EXCLUDE), len(undecodable)))
print("named as undecodable, and anything under %s/ -- and those three"
      % PYCACHE)
print("lists are the whole of it, which is a claim about the CODE and not")
print("about the shape the trees happen to have today (mg-821e).")
print("EVERY REGULAR FILE means every regular file THE WALK REACHED, and the")
print("walk names what it declined: %d stated, %d not stated (mg-5040).  A"
      % (len(declined_stated), len(declined_unstated)))
print("non-empty second list is a finding here, so this sentence cannot be")
print("true by accident of the tree the way it was at mg-6cb9 and again at")
print("mg-4700.")
print("It says NOTHING about docs/ other than the one document")
print("named above, about the audit trees code/species_audit_a61f,")
print("code/species_audit_73df, code/species_audit_7dd3 or the instrument")
print("code/species_extent_d633, or about any statement not in the list.")
print("AND IT SAYS NOTHING ABOUT WHETHER A STRUCK CLAIM IS RESTATED ELSEWHERE")
print("IN THE DOCUMENT IN OTHER WORDS -- this list matches SENTENCES, and a")
print("sentence is not a claim (mg-7dd3 B1).  That is:")
print("    python3 code/species_extent_d633/e2_crosssection.py")
sys.exit(1 if bad else 0)
