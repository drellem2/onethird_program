"""E1 -- IS THE PRINTED EXTENT TRUE?  Measured against what the code READS.

mg-a4ef made every checker print its own extent.  That removes the failure
mode rather than detecting it -- a total that names its population cannot turn
"not examined" into "examined and clean" -- and it RELOCATES the trust to a
single point.  mg-7dd3 measured that point and found half of it false:

  s1_extent.py  printed "SKIPPED, NAMED, so the exclusion cannot grow unseen
                -- 5 file(s)".  The real exclusion was NINE: four run_all.sh
                inside the four trees the extent names, dropped by an
                extension filter that was in no extent line and no list.
  s2_seam.py    named two limits and omitted MIN_CHARS=300, which removed 6 of
                17 block quotes and 65 of 124 paragraphs from the comparison
                ALTOGETHER.
  check_doc.py  said "over ONE FILE ... It reads no code".  It reads two.

This file is the measurement, kept, so the next reader does not have to take
the extent lines on trust either.  Each checker is run under `trace_open.py`,
which records every path it opens for reading in text mode, and the recorded
set is compared with what the run PRINTS about itself.

  E1a  what each checker reads, listed.
  E1b  the printed extent against the read set, per checker.
  E1c  the passage-level extent of s2_seam.py, which is not a set of files.

    python3 code/species_extent_d633/e1_extents.py
"""

import json
import os
import re
import subprocess
import sys
import tempfile

from kernd633 import hdr, REPO

bad = 0
HERE = os.path.dirname(os.path.abspath(__file__))
TRACER = os.path.join(HERE, "trace_open.py")

CHECKERS = [
    ("check_doc.py", "code/species_repair_6f61/check_doc.py"),
    ("w3_scope.py", "code/species_remainder_f8fa/w3_scope.py"),
    ("s1_extent.py", "code/species_repair_a4ef/s1_extent.py"),
    ("s2_seam.py", "code/species_repair_a4ef/s2_seam.py"),
    ("e2_crosssection.py", "code/species_extent_d633/e2_crosssection.py"),
]


def trace(rel):
    """Run one checker under the tracer; (exit, stdout, text reads rel to
    REPO, binary read count).  Reads outside REPO -- the tempdir copies
    s1_extent.py makes for its own controls -- are dropped and counted."""
    path = os.path.join(REPO, rel)
    fd, rec = tempfile.mkstemp(prefix="d633_", suffix=".json")
    os.close(fd)
    env = dict(os.environ, D633_TRACE=rec, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, TRACER, os.path.basename(path)],
                       cwd=os.path.dirname(path), capture_output=True,
                       text=True, env=env)
    with open(rec, encoding="utf-8") as fh:
        data = json.load(fh)
    os.unlink(rec)
    inside, outside = [], 0
    for f in data["text"]:
        if f.startswith(REPO + os.sep):
            inside.append(os.path.relpath(f, REPO))
        else:
            outside += 1
    # mg-4adb, on mg-6ef4's F1.  `data["text"]` is now what the checker READ.
    # It used to be what the checker TRIED to read: the tracer recorded the
    # path before calling the real `open`, so an attempt that raised was
    # indistinguishable from a read, and every `want <= got` row below
    # certified an extent over files whose bytes nobody had seen.  The
    # attempts that RAISED are in `data["failed"]` -- kept, not dropped, and
    # reported in E1a -- because subtracting them silently would be the same
    # defect with the sign reversed.
    failed = sorted(set(os.path.relpath(f, REPO) for f in data["failed"]
                        if f.startswith(REPO + os.sep)))
    # NOTE: the tracer already drops runpy's own open of the target, ONCE.  A
    # checker that reads its own source as a TARGET -- s1_extent.py does, its
    # file being inside one of the four trees it scans -- is still recorded.
    return p.returncode, p.stdout, sorted(set(inside)), outside, \
        len(data["binary"]), failed


hdr("E1a  WHAT EACH CHECKER ACTUALLY READS")

READS = {}
OUT = {}
FAILED = {}
for name, rel in CHECKERS:
    code, out, inside, outside, nbin, failed = trace(rel)
    READS[name] = inside
    OUT[name] = out
    FAILED[name] = failed
    docs = [f for f in inside if f.startswith("docs/")]
    codef = [f for f in inside if f.startswith("code/")]
    print("  %-20s exit %d   %3d file(s) under the repo "
          "(%d docs, %d code), %d outside, %d binary, %d ATTEMPTED AND FAILED"
          % (name, code, len(inside), len(docs), len(codef), outside, nbin,
             len(failed)))
print()
print("  'outside' is the temporary copies s1_extent.py makes for its own")
print("  controls (c) and (d).  'binary' is shutil.copytree's byte copies.")
print("  Both are counted and named rather than filtered silently: mg-7dd3")
print("  recorded that an open()-tracer which swallowed the second would have")
print("  hidden the very hole it was written to find.")
print()
print("  'ATTEMPTED AND FAILED' is mg-4adb, on mg-6ef4's F1, and it is a")
print("  column that did not exist because the tracer recorded the path")
print("  BEFORE calling open.  An attempt that raised was counted as a read,")
print("  so a checker could be certified as having read a file it could not")
print("  open.  Every row below reads the READ set; this column is the part")
print("  that used to be folded into it.")
for name, _rel in CHECKERS:
    for f in FAILED[name]:
        print("      %-20s could NOT open %s" % (name, f))
if not any(FAILED.values()):
    print("      (no checker attempted a read that failed)")
print()


# ---------------------------------------------------------------------------
# E1b  the printed extent, against the read set
# ---------------------------------------------------------------------------
hdr("E1b  THE PRINTED EXTENT AGAINST THE READ SET, PER CHECKER")

DOC = "docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md"
REPAIR_DOC = "docs/OneThird-Species-Hopf-Monoids-Repair.md"
TREES = ["species_7d75", "species_repair_6f61", "species_remainder_f8fa",
         "species_repair_a4ef"]
EXCLUDE = {"stricken_a4ef.py", "PREDICTIONS.md", "OUTCOMES.md",
           "out_c4_scope_73df_after.txt", "out_c5_doc_73df_after.txt"}


# mg-821e, on mg-6cb9's F1.  This helper WAS a non-recursive `os.listdir`,
# exactly like the two scans it exists to measure.  So the file whose whole job
# is deciding whether a printed extent is true shared the blind spot it was
# measuring: with X3 planted in `code/species_7d75/sub/leak.md`, `s1_extent.py`
# did not read it, `want` did not contain it, `want <= got` held, and E1
# certified the extent as TRUE over a file neither of them could see (mg-6cb9
# Q17e).  An instrument that computes its expectation the same way the subject
# computes its answer cannot disagree with the subject.
#
# It now walks.  The one directory rule is `__pycache__`, which is the rule the
# two scans print in their own extent lines -- copied here deliberately rather
# than imported, so that if either of them widens or narrows it, E1's
# expectation does NOT move with it and the disagreement shows up as a
# finding.
#
# mg-5040, on mg-4700's OPEN 1.  The paragraph above closed the instance and
# left the class: E1 walked, the subjects walked, and BOTH declined a
# SYMLINKED DIRECTORY, so with a forbidden statement planted behind a link
# `want` did not contain it, `want <= got` held, and E1 CERTIFIED THE EXTENT
# AS TRUE a second time (mg-4700 F1, D2c).  Making E1's walk wider than the
# subjects' would be the third widening and would buy one generation.
#
# What removes the class is that a walk which NAMES ITS OWN RESIDUE can
# disagree without out-walking anybody.  `regular()` and `residue()` below
# come from one traversal that returns what it declined; E1 fires when its own
# residue carries an entry that is not the stated `__pycache__` rule, and
# separately when a SUBJECT's printed output does not name an entry E1's
# independent walk declined.  So E1 no longer needs to reach further than the
# thing it measures -- it needs the thing it measures to say what it did not
# reach.
PYCACHE = "__pycache__"
STATED_DIR_RULES = (PYCACHE,)


def walk_residue(root, stated_dirs=STATED_DIR_RULES):
    """(files, stated, unstated) -- nothing is dropped without landing in one
    of the last two.  `stated`/`unstated` are (relpath, reason) pairs.

    Copied into each subject rather than shared, deliberately, for the reason
    the paragraph above this one gives: an instrument that computes its
    expectation with the subject's own code cannot disagree with the subject.
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


def regular(tree):
    """Every regular file of a tree, repo-tree-relative, AT ANY DEPTH -- that
    is, at any depth THIS WALK REACHED.  `residue()` is the other half of the
    sentence and is not optional (mg-5040)."""
    return walk_residue(os.path.join(REPO, "code", tree))[0]


def residue(tree):
    """(stated, unstated) -- what the walk behind `regular()` declined."""
    _f, st, unst = walk_residue(os.path.join(REPO, "code", tree))
    return st, unst


def check(label, ok, detail=""):
    global bad
    bad += (not ok)
    print("  %-64s %s" % (label[:64], "ok" if ok else "*** FALSE ***"))
    if detail and not ok:
        print("        %s" % detail)


# --- check_doc.py -----------------------------------------------------------
print("  check_doc.py -- claims TWO files, and names both")
got = set(READS["check_doc.py"])
check("reads exactly {this document, the repair document}",
      got == {DOC, REPAIR_DOC}, "read: %s" % sorted(got))
check("the printed extent names the document it enforces over",
      DOC in OUT["check_doc.py"])
check("the printed extent names the SECOND file too",
      REPAIR_DOC in OUT["check_doc.py"])
check("and still says it reads no code",
      "reads no code" in OUT["check_doc.py"]
      and not [f for f in got if f.startswith("code/")])
print()

# --- w3_scope.py ------------------------------------------------------------
print("  w3_scope.py -- claims ONE tree, every regular file")
got = set(READS["w3_scope.py"])
want = {"code/species_7d75/" + f for f in regular("species_7d75")}
check("reads every regular file of code/species_7d75 (%d)" % len(want),
      want <= got, "missing: %s" % sorted(want - got))
check("reads nothing else under code/",
      not [f for f in got if f.startswith("code/")
           and not f.startswith("code/species_7d75/")])
check("run_all.sh is among them -- the file the old filter dropped",
      "code/species_7d75/run_all.sh" in got)
check("the printed extent says 'every regular file'",
      "every regular file" in OUT["w3_scope.py"])
check("and says AT WHAT DEPTH -- the condition F1 left unstated",
      "at any depth" in OUT["w3_scope.py"].lower())
check("and names the ONE directory rule it keeps",
      PYCACHE in OUT["w3_scope.py"])
check("the printed file count agrees with what was read",
      ("files read: %d" % len(got & want)) in OUT["w3_scope.py"],
      "printed: %s" % re.search(r"files read: \d+", OUT["w3_scope.py"]))
print()

# --- s1_extent.py -----------------------------------------------------------
print("  s1_extent.py -- claims the document + 4 trees, less a NAMED list")
got = set(READS["s1_extent.py"])
want, excluded = set(), set()
for t in TREES:
    for f in regular(t):
        (excluded if f in EXCLUDE else want).add("code/%s/%s" % (t, f))
check("reads the document", DOC in got)
check("reads every non-excluded regular file of all four trees (%d)"
      % len(want), want <= got, "missing: %s" % sorted(want - got))
check("reads NONE of the %d files it names as skipped" % len(excluded),
      not (excluded & got), "read anyway: %s" % sorted(excluded & got))
check("the four run_all.sh are read -- the A1 hole, closed",
      all("code/%s/run_all.sh" % t in got for t in TREES))
printed_skips = set(re.findall(r"^ {6}(\S+)$", OUT["s1_extent.py"], re.M))
check("every skipped file is NAMED in the run",
      EXCLUDE <= printed_skips,
      "not named: %s" % sorted(EXCLUDE - printed_skips))
check("the printed extent says AT WHAT DEPTH (mg-6cb9 F1)",
      "at any depth" in OUT["s1_extent.py"].lower())
check("and names the ONE directory rule it keeps",
      PYCACHE in OUT["s1_extent.py"])
nested = sorted("code/%s/%s" % (t, f) for t in TREES for f in regular(t)
                if os.sep in f and f not in EXCLUDE)
check("every file BELOW a tree root is read (%d today)" % len(nested),
      all(n in got for n in nested),
      "not read: %s" % sorted(n for n in nested if n not in got))
for t in TREES:
    n = len([f for f in got if f.startswith("code/%s/" % t)])
    nsub = len([f for f in got if f.startswith("code/%s/" % t)
                and f.count("/") > 2])
    check("the printed count for code/%s is %d, and %d were read" % (t, n, n),
          ("code/%-24s %3d file(s) read, %d of them below the tree root"
           % (t, n, nsub)) in OUT["s1_extent.py"])
print()
print("  %d file(s) sit below a tree root today.  That number is printed"
      % len(nested))
print("  rather than assumed: when it was 0 and both walks were")
print("  non-recursive, 'EVERY REGULAR FILE' was a TRUE sentence resting on a")
print("  condition no sentence stated, and E1 -- listing the same way -- could")
print("  not disagree.  E1 walks now, so the two computations are independent")
print("  and a scan that stops at the root is a FINDING here, not a match.")
print()

# --- the residue, which is the other half of every sentence above -----------
#
# mg-5040, on mg-4700's OPEN 1.  Every check above compares what a checker
# READ against what E1's walk REACHED.  Two walks that decline the same thing
# agree, and that agreement is what certified a false extent twice: once when
# neither descended into a subdirectory (mg-6cb9 F1) and once when neither
# followed a symlinked directory (mg-4700 F1).  `want <= got` cannot see it,
# by construction, and no amount of widening E1's walk fixes the shape --
# it only moves the next generation one rule to the side.
#
# These rows compare the walk against ITSELF: what did it decline, and does
# the checker that quantifies over its output SAY SO.  A row here can fail
# with `want <= got` holding everywhere, which is the whole point.
print("  the WALK'S RESIDUE -- what the enumeration declined, and whether the")
print("  sentence that quantifies over it says so (mg-5040)")
_subject_of = {"species_7d75": ["w3_scope.py", "s1_extent.py"],
               "species_repair_6f61": ["s1_extent.py"],
               "species_remainder_f8fa": ["s1_extent.py"],
               "species_repair_a4ef": ["s1_extent.py"]}
_unstated_all = []
for t in TREES:
    st, unst = residue(t)
    _unstated_all += [(t, r, why) for r, why in unst]
    check("%s: declined nothing unstated (%d stated)" % (t, len(st)),
          not unst,
          "NOT STATED: %s" % ["%s -- %s" % (r, w) for r, w in unst])
for t, r, why in _unstated_all:
    for sub in _subject_of.get(t, []):
        check("%s names code/%s/%s, which its walk declined" % (sub, t, r),
              r in OUT.get(sub, ""),
              "the extent claims every regular file at any depth and this "
              "entry is not in it: %s" % why)
if not _unstated_all:
    print("      nothing was declined outside the stated rules, in %d tree(s)."
          % len(TREES))
    print("      That is a MEASUREMENT of this run, not a list of the rules")
    print("      anybody remembered: plant a symlinked directory and the row")
    print("      above goes red without one line of this file changing.")
print()


# --- e2_crosssection.py -----------------------------------------------------
print("  e2_crosssection.py -- claims every *.md under docs/ and code/")
got = set(READS["e2_crosssection.py"])
want = set()
for root in ("docs", "code"):
    for dp, dns, fns in os.walk(os.path.join(REPO, root)):
        dns[:] = [d for d in dns if d != "__pycache__"]
        for fn in fns:
            if fn.endswith(".md"):
                want.add(os.path.relpath(os.path.join(dp, fn), REPO))
check("reads every .md under docs/ and code/ (%d)" % len(want), want <= got,
      "missing: %s" % sorted(want - got)[:5])
check("reads no .py, .txt or anything else",
      not [f for f in got if not f.endswith(".md")],
      "also read: %s" % [f for f in got if not f.endswith(".md")])
check("the printed extent states that count",
      ("%d markdown file(s)" % len(got)) in OUT["e2_crosssection.py"])
print()


# ---------------------------------------------------------------------------
# E1c  s2_seam.py, whose extent is passages and not files
# ---------------------------------------------------------------------------
hdr("E1c  s2_seam.py -- an extent that is not a set of files")

got = set(READS["s2_seam.py"])
check("reads exactly one file, the document", got == {DOC},
      "read: %s" % sorted(got))

text = open(os.path.join(REPO, DOC), encoding="utf-8").read()
LINES = text.splitlines()


def norm(s):
    s = re.sub(r"[*`~>|#]", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def blocks_of(pred):
    out, cur, start = [], [], None
    for i, ln in enumerate(LINES):
        if pred(ln):
            if start is None:
                start = i + 1
            cur.append(ln)
        else:
            if cur:
                out.append((start, i, "\n".join(cur)))
            cur, start = [], None
    if cur:
        out.append((start, len(LINES), "\n".join(cur)))
    return out


for label, items in [
    ("block quotes", blocks_of(lambda ln: ln.startswith(">"))),
    ("prose paragraphs",
     blocks_of(lambda ln: ln.strip() and not ln.startswith(">")
               and not ln.startswith("#") and not ln.startswith("|"))),
]:
    over60 = [p for p in items if len(norm(p[2])) > 60]
    over300 = [p for p in items if len(norm(p[2])) > 300]
    under = [p for p in items if len(norm(p[2])) <= 60]
    check("%s: the run says %d passage(s), %d over 300, %d over 60"
          % (label, len(items), len(over300), len(over60)),
          ("%3d passage(s): %3d over 300 chars" % (len(items), len(over300)))
          in OUT["s2_seam.py"]
          and ("%3d over 60 chars" % len(over60)) in OUT["s2_seam.py"])
    named = OUT["s2_seam.py"].count("lines %d-%d:" % (under[0][0], under[0][1])) \
        if under else 1
    check("%s: all %d passage(s) compared by NEITHER pass are printed"
          % (label, len(under)),
          all(("lines %d-%d:" % (a, b)) in OUT["s2_seam.py"]
              for a, b, _t in under) and named >= 1)
print()
print("  The point of E1c: s2_seam.py's extent is a claim about PASSAGES, and")
print("  the passages it excludes are now enumerated in its own output rather")
print("  than summarised by a threshold that the extent sentence omitted.")
print()

print("=" * 78)
print("E1 TOTAL BAD: %d" % bad)
print("=" * 78)
print()
print("EXTENT OF THIS NUMBER.  Five checkers, each run ONCE, unmodified, under")
print("an instrumented `open`.  It compares WHAT WAS READ with WHAT WAS")
print("PRINTED and nothing else: it does not test whether a checker's rules")
print("are right, whether its list is complete, or whether it FIRES on what it")
print("reads.  A checker that opens every file and looks at none of them")
print("passes E1 and fails E3, which is why both exist.")
sys.exit(1 if bad else 0)
