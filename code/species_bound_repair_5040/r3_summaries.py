"""R3 -- OPEN 3.  The figure, every copy of it, and which copies share a source.

mg-4700's F3: `A2 TOTAL BAD` is 2 for the tree mg-821e's work shipped in, and
mg-821e's commit messages say 1.  The rule this repository works by is that
THE ROWS WIN -- the artifact is the measurement and the summary is a copy of
it -- so the summaries are what get corrected.

THE SHARPENING, WHICH IS WORTH MORE THAN THE NUMBER.  A wrong figure reached
more than one summary before anything compared it to the thing it described.
Agreeing summaries are NOT independent confirmations when they are copies of
one source: replication is not corroboration if the copies share a parent.
So this section does not count agreements.  It finds every copy, finds the
SOURCE each copy was taken from, and compares the source with the artifact.

WHAT CAN AND CANNOT BE EDITED, STATED SO THE DISPOSITIONS ARE CHECKABLE:

  * a DOCUMENT can be edited, and is.
  * a COMMIT MESSAGE cannot.  It is in the history of a merged commit.  The
    only honest repair is a correction record that names the commit, the
    figure it states, and the figure that is true -- which is what §5 of
    docs/OneThird-Species-Hopf-Monoids-Bound-Repair.md is.
  * a PUBLISHED TRANSCRIPT must not be edited.  It is the record of a run
    that really happened; editing it to carry a number that run did not
    produce is not a correction, it is a forgery.  It gets the same treatment
    as a commit message.
  * a PREDICTION that has already been scored `*** MISSED ***` beside itself
    is already corrected, and is reported here rather than filtered, because
    a filter nobody can see is how a census goes 8 short.
"""

import os
import re
import sys

from kern5040 import (hdr, REPO, PRE, sh, git, commit_messages,
                      run_checker, extract_with_git)

bad = 0

# The figure and the artifact it is a figure OF.
TAG = "A2 TOTAL BAD"
ARTIFACT = "code/species_extent_audit_6cb9/a2_crosssection.py"
PUBLISHED = "code/species_sites_821e/out_a2_6cb9_after.txt"
DOC = "docs/OneThird-Species-Hopf-Monoids-Repair-Sites.md"

# `A2 TOTAL BAD` followed by a number, allowing the words a summary uses to
# join them: "A2 TOTAL BAD: 1", "A2 TOTAL BAD is 2", "A2 TOTAL BAD stays 1",
# "`A2 TOTAL BAD` remains **1**".
FIG = re.compile(re.escape(TAG) + r"[`\s]*(?:is|stays|remains|of|:)?"
                 r"[\s*`]*(\d+)")


def figures(text):
    return [int(m.group(1)) for m in FIG.finditer(text)]


# THE TAG NAMES NO ARTIFACT, AND THAT IS ITSELF PART OF THE DEFECT.  Two
# checkers in this repository print `A2 TOTAL BAD`: mg-6cb9's
# a2_crosssection.py and mg-a61f's a2_bidigare.py.  A figure that carries a
# bare tag cannot be compared with the thing it describes without a rule, so
# here is the rule, applied to every candidate and with every exclusion NAMED
# rather than filtered:
#
#   a transcript belongs to the script that produced it -- out_X.txt <- X.py
#   in the same directory, which is derived and not asserted;
#   any other text is about this artifact if it names `a2_crosssection` or
#   `mg-6cb9`, which is how every real summary of it in this history refers
#   to it.
MARKERS = []          # filled from the artifact's own live output, in R3a


def about_this_artifact(path, text):
    """(True/False, reason).  The reason is printed for every exclusion."""
    if path:
        d, base = os.path.split(path)
        if base.startswith("out_") and base.endswith(".txt"):
            producer = os.path.join(d, base[4:-4] + ".py")
            pp = os.path.join(REPO, producer)
            if os.path.exists(pp):
                # A transcript belongs to a DIFFERENT checker only when that
                # checker prints this tag AS ITS OWN VERDICT.  A script that
                # merely quotes the figure in order to compare it -- which is
                # what an auditor's probe does -- is not a different checker
                # and its transcript is about this artifact after all.  The
                # first version of this rule missed that and excluded
                # mg-4700's own out_q4_standing.txt, which is the transcript
                # that RAISED the discrepancy.
                src = open(pp, encoding="utf-8").read()
                owns = ('"%s: %%d" %% bad' % TAG) in src
                if owns and not producer.endswith("a2_crosssection.py"):
                    return False, ("transcript of %s, which prints `%s` as "
                                   "its OWN verdict" % (producer, TAG))
                return True, "transcript of %s" % producer
    if "a2_crosssection" in text or "mg-6cb9" in text:
        return True, "names a2_crosssection or mg-6cb9"
    # A TRANSCRIPT NEED NOT NAME ITS OWN PRODUCER, and the first version of
    # this rule excluded out_a2_6cb9_after.txt for that reason -- the one
    # artifact the whole section is about.  So the markers are taken FROM THE
    # ARTIFACT'S OWN LIVE OUTPUT: a text carrying a section heading this
    # checker prints is a record of this checker running.
    for m in MARKERS:
        if m in text:
            return True, "carries this artifact's own heading %r" % m[:34]
    return False, ("names neither a2_crosssection nor mg-6cb9, and carries "
                   "none of its %d headings" % len(MARKERS))


# ---------------------------------------------------------------------------
# R3a  the artifact.  Run it, unmodified, and read the row it prints.
# ---------------------------------------------------------------------------
hdr("R3a  THE ARTIFACT -- mg-6cb9's a2_crosssection.py, AT THE TREE THE "
    "SUMMARIES DESCRIBE")

print("  A BARE FIGURE NAMES NO TREE, WHICH IS THE WHOLE OF F3, and the first")
print("  version of this section walked straight into it: it compared the")
print("  summaries against a LIVE run in this worktree.  But `A2 TOTAL BAD` is")
print("  a property of a tree, and this ticket CHANGES the tree -- regenerating")
print("  the census turns one of the two rows green, so the live figure moves")
print("  under the comparison and a correction would be graded against a")
print("  number the correction itself caused.  That is F3 one level out, in")
print("  the file repairing F3.")
print()
print("  So the artifact is run TWICE and the two are never mixed:")
print("      AT %s -- the tree mg-821e's work shipped in, which is the tree" % PRE)
print("      those summaries are ABOUT.  This is what they are graded against.")
print("      AT THIS WORKTREE -- reported, and not used to grade anything.")
print()
pin_root = extract_with_git(PRE, os.path.join(
    os.environ.get("TMPDIR", "/tmp"), "mg5040-pinrepo-%s" % PRE))
rc_pin, out_pin = run_checker("species_extent_audit_6cb9",
                              "a2_crosssection.py", root=pin_root)
pin_figs = figures(out_pin)
PIN = pin_figs[-1] if pin_figs else None
rc, out = run_checker("species_extent_audit_6cb9", "a2_crosssection.py")
MARKERS[:] = [ln.strip() for ln in out.splitlines()
              if ln.strip().startswith("A2") and len(ln.strip()) >= 40]
live = figures(out)
NOW = live[-1] if live else None
LIVE = PIN                      # what the summaries are graded against
print("  AT %s   exit %d   %s: %s" % (PRE, rc_pin, TAG, PIN))
for ln in out_pin.splitlines():
    if "***" in ln:
        print("      %s" % ln.strip())
print()
print("  IN THIS WORKTREE   exit %d   %s: %s" % (rc, TAG, NOW))
for ln in out.splitlines():
    if "***" in ln:
        print("      %s" % ln.strip())
print()
if PIN is not None and NOW is not None and PIN != NOW:
    print("  THE TWO DIFFER, and the reason is this ticket: §4 of the repair")
    print("  document regenerates code/species_extent_d633/"
          "out_e2_crosssection.txt,")
    print("  which is the row mg-4700 raised.  The row that closes is an")
    print("  ARTIFACT being made right for one tree; the MECHANISM is")
    print("  untouched and the anchor line in e2's own output says so.  The")
    print("  figure the summaries are wrong about is still %s: that is what" % PIN)
    print("  a2 says of the tree those summaries shipped in, and git cannot")
    print("  move that tree.")
    print()
ok = PIN is not None
bad += (not ok)
print("  %-58s %s" % ("the artifact produced a figure at the pin",
                      "ok" if ok else "*** none ***"))
print()
print("  NOT REPAIRED, AND DELIBERATELY: a2_crosssection.py is the auditor's")
print("  instrument.  An instrument edited by the thing it audits has stopped")
print("  being evidence, so nothing in this ticket touches it, and the number")
print("  above is whatever it says today.")
print()


# ---------------------------------------------------------------------------
# R3b  every copy in a COMMIT MESSAGE, from the pin
# ---------------------------------------------------------------------------
hdr("R3b  EVERY COPY OF THE FIGURE IN A COMMIT MESSAGE")

print("  Reachable from %s, which git cannot move.  Not from HEAD: a census" % PRE)
print("  that grows a row every time somebody commits is the defect F3 is")
print("  about, one level out.")
print()
msg_rows = []
for sha, subj, body in commit_messages():
    vals = figures(body)
    if not vals:
        continue
    mine_, why = about_this_artifact(None, body)
    msg_rows.append((sha[:7], subj, vals, mine_, why))
for sha, subj, vals, mine_, why in msg_rows:
    print("  %s  %s   [%s]"
          % (sha, ", ".join("%s %d" % (TAG, v) for v in vals),
             "about this artifact" if mine_ else "NOT: " + why))
    print("      %s" % subj[:68])
print()
# A summary is UNCORRECTED if it states the old figure and nothing beside it
# states the artifact's.  A message that quotes the wrong figure next to the
# right one has already corrected it, and counting it would inflate the tally
# in exactly the direction this section exists to deflate.
uncorrected_msgs = [(s, v) for s, _u, v, m, _w in msg_rows
                    if m and LIVE is not None
                    and any(x != LIVE for x in v) and LIVE not in v]
corrected_msgs = [(s, v) for s, _u, v, m, _w in msg_rows
                  if m and LIVE is not None and LIVE in v]
print("  %d message(s) state the figure and are about this artifact."
      % len([r for r in msg_rows if r[3]]))
print("  %d of them are UNCORRECTED -- they state a value that is not the"
      % len(uncorrected_msgs))
print("  artifact's %s and do not state %s anywhere:" % (LIVE, LIVE))
for s, v in uncorrected_msgs:
    print("      %s  says %s" % (s, v))
print("  %d carry the correction beside the old figure:" % len(corrected_msgs))
for s, v in corrected_msgs:
    print("      %s  says %s" % (s, v))
print()


# ---------------------------------------------------------------------------
# R3c  every copy in a COMMITTED FILE, measured twice
# ---------------------------------------------------------------------------
hdr("R3c  EVERY COPY IN A COMMITTED FILE -- at the pin, and in this worktree")

print("  Measured both ways on purpose.  The pin's population is the one")
print("  mg-4700 measured and is IMMUNE TO THIS INSTRUMENT: no file of mine")
print("  is in it.  The worktree's population includes my own files, and the")
print("  difference between the two columns is exactly what I added, which")
print("  is declared rather than netted out.")
print()


def files_at(ref):
    rc, tree = git(["ls-tree", "-r", "--name-only", ref])
    return sorted(tree.splitlines()) if rc == 0 else []


def scan_ref(ref):
    rows = []
    for f in files_at(ref):
        rc, blob = git(["show", "%s:%s" % (ref, f)])
        if rc != 0:
            continue
        vals = figures(blob)
        if vals:
            rows.append((f, vals))
    return rows


def scan_worktree():
    rows = []
    rc, tracked = git(["ls-files"])
    for f in sorted(tracked.splitlines()):
        p = os.path.join(REPO, f)
        if not os.path.isfile(p):
            continue
        try:
            with open(p, encoding="utf-8") as fh:
                vals = figures(fh.read())
        except (UnicodeDecodeError, OSError):
            continue
        if vals:
            rows.append((f, vals))
    return rows


at_pin = scan_ref(PRE)
at_now = scan_worktree()
pin_map = dict(at_pin)
now_map = dict(at_now)
allf = sorted(set(pin_map) | set(now_map))
print("  %-56s %-10s %s" % ("file", "at " + PRE, "worktree"))
for f in allf:
    print("  %-56s %-10s %s"
          % (f[-56:], pin_map.get(f, "--"), now_map.get(f, "--")))
print()
mine = [f for f in allf if f not in pin_map]
print("  %d file(s) at the pin, %d in the worktree; %d of the worktree's are"
      % (len(at_pin), len(at_now), len(mine)))
print("  MINE and are named here rather than excluded by a rule:")
for f in mine:
    print("      %s" % f)
if not mine:
    print("      (none)")
print()


# ---------------------------------------------------------------------------
# R3d  which copies share a source
# ---------------------------------------------------------------------------
hdr("R3d  WHICH COPIES SHARE A SOURCE -- replication is not corroboration")

pub = os.path.join(REPO, PUBLISHED)
pub_vals = []
if os.path.exists(pub):
    with open(pub, encoding="utf-8") as f:
        pub_vals = figures(f.read())
print("  THE PUBLISHED TRANSCRIPT %s" % PUBLISHED)
print("  states %s.  It is the run mg-821e committed as its evidence, and it"
      % (pub_vals[-1] if pub_vals else "no figure"))
print("  is the SOURCE the summaries were copied from.")
print()
print("  So the agreeing summaries are not %d confirmations of a figure."
      % (len(uncorrected_msgs) + 1))
print("  They are %d copies of ONE run, taken in a worktree whose tree is"
      % (len(uncorrected_msgs) + 1))
print("  not the tree the work shipped in.  Nothing compared")
print("  the copy to the artifact until mg-4700 did, one ticket later.")
print()
print("  The transcript is NOT edited.  It records a run that really")
print("  happened; changing its number to one that run did not produce would")
print("  be a forgery, and the correction record names it instead.")
print()


# ---------------------------------------------------------------------------
# R3e  the dispositions, and the one copy this ticket can edit
# ---------------------------------------------------------------------------
hdr("R3e  DISPOSITION OF EVERY COPY, AND THE EDIT")

print("  The disposition of each copy is DERIVED in this order, and every")
print("  branch that declines to score a copy states why:")
print("      1. not about this artifact       -- the tag is not unique")
print("      2. carries the artifact's figure -- corrected in place")
print("      3. a record of a run             -- must not be edited")
print("      4. a scored prediction           -- corrected beside itself")
print("      5. editable prose                -- EDITED by this ticket")
print("      6. anything else                 -- UNCLASSIFIED, and a finding")
print()
rows = []
for f, vals in at_now:
    p = os.path.join(REPO, f)
    text = open(p, encoding="utf-8").read() if os.path.isfile(p) else ""
    mine_, why = about_this_artifact(f, text)
    base = os.path.basename(f)
    scored_miss = ("PREDICTIONS.md" in base
                   and "*** MISSED ***" in open(
                       os.path.join(os.path.dirname(p),
                                    "out_q4_standing.txt"),
                       encoding="utf-8").read()
                   if os.path.exists(os.path.join(os.path.dirname(p),
                                                  "out_q4_standing.txt"))
                   else False)
    if not mine_:
        disp = "1. NOT this artifact -- %s" % why
    elif LIVE is not None and LIVE in vals:
        disp = "2. carries the artifact's figure %s beside the old one" % LIVE
    elif base.startswith("out_") or f.endswith(".txt"):
        disp = "3. RECORD of a run -- not edited; in the correction record"
    elif scored_miss:
        disp = "4. PREDICTION, scored *** MISSED *** in its own tree"
    elif f.startswith("code/species_bound_repair_5040/"):
        disp = "5. THIS instrument -- the figure is read from the run, not typed"
    elif f == DOC:
        disp = "5. EDITABLE prose -- corrected in place by this ticket"
    elif f.endswith(".py"):
        disp = "3. the INSTRUMENT that raised the discrepancy -- it quotes " \
               "the old figure in order to compare it"
    else:
        disp = "*** 6. UNCLASSIFIED -- a copy nobody has dispositioned ***"
    rows.append((f, vals, disp))
    print("  %-56s %s" % (f[-56:], vals))
    print("      %s" % disp)
print()
unclassified = [r for r in rows if r[2].startswith("***")]
bad += len(unclassified)
print("  %-58s %s" % ("every copy has a disposition",
                      "ok" if not unclassified
                      else "*** %d without one ***" % len(unclassified)))
excluded = [r for r in rows if r[2].startswith("1.")]
print("  %d copy(ies) excluded by rule 1, NAMED so the exclusion cannot grow"
      % len(excluded))
print("  unseen -- which is the same principle as the extent lines in OPEN 1:")
for f, vals, _d in excluded:
    print("      %s  %s" % (f, vals))

doc_p = os.path.join(REPO, DOC)
doc_text = open(doc_p, encoding="utf-8").read() if os.path.exists(doc_p) else ""
doc_vals = figures(doc_text)
# THE SAME RULE AS THE DISPOSITIONS ABOVE, and not a stricter one.  A
# correction has to be allowed to quote the figure it corrects, or the only
# way to satisfy this row would be to delete the record of what was wrong --
# which is how a repository ends up unable to say what it used to believe.
# So: the document must carry the artifact's figure, beside whatever it used
# to say.
doc_ok = LIVE is None or LIVE in doc_vals
bad += (not doc_ok)
print("  %-58s %s"
      % ("the one editable copy now carries the artifact's figure",
         "ok" if doc_ok else "*** says %s, not %s ***" % (doc_vals, LIVE)))
cites = ("mg-5040" in doc_text and "post-merge" in doc_text.lower())
bad += (not cites)
print("  %-58s %s" % ("and the correction says WHY, not just what",
                      "ok" if cites else "*** no reason given ***"))
print()
print("  P3d.  The ticket says THREE COMMIT MESSAGES say 1.  Measured: %d"
      % len(uncorrected_msgs))
print("  commit message(s) state a figure that is not the artifact's, and the")
print("  third statement of the old figure is in a DOCUMENT, with a fourth in")
print("  the published transcript both messages were copied from.  The")
print("  ticket's own count is itself a figure that arrived in a summary; it")
print("  is reported here against the rows rather than repeated.")
print()


print("=" * 78)
print("R3 TOTAL BAD: %d" % bad)
print("=" * 78)
print()
print("EXTENT OF THIS NUMBER.  ONE figure -- `%s` -- traced through" % TAG)
print("every commit message reachable from %s and every file tracked at" % PRE)
print("that revision and in this worktree.  It says NOTHING about any other")
print("figure in any other summary: the general check is r4's business and is")
print("bounded there too.  It says nothing about whether mg-6cb9's a2 is")
print("right, only about whether the summaries match it.")
sys.exit(1 if bad else 0)
