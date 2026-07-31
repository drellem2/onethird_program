"""k2_five.py -- OPEN 2: was G-3 shut on FIVE, and is it still shut HERE?

mg-957f left OPEN 2 as "G-3 is shut at ONE revision, with 1 of 5 committed
outputs reproducing".  mg-76cc says it is now shut on five.  A gate closed on
2 of 5 -- or on 4 of 5 with the fifth unmentioned -- is the same defect with a
better ratio, so the five are counted here rather than read off a table.

WHAT THIS ASKS THAT mg-76cc's OWN r2 DOES NOT

  * THE POPULATION IS TAKEN FROM run_all.sh's SOURCE.  lib76cc.py carries the
    five filenames as a written list.  A written list cannot notice a sixth
    output being added, and "5 of 5" over a list of five that is missing one
    is exactly the shape of finding this arc keeps producing.  Here the
    redirections are read out of the runner.

  * THE CLONE'S HEAD IS THIS BRANCH'S HEAD.  mg-76cc's clone adds a scratch
    commit, so its fresh transcripts name a revision that exists only inside
    a temp directory.  This one commits nothing, so the fresh run names a
    revision anybody can `git show`.

  * THE NORMALISATION MUST ACT AT THE SAME POSITIONS ON BOTH SIDES.  A
    substitution that fires on the record and not on the re-run (or the other
    way round) is absorbing a difference rather than explaining one, and a
    count of surviving lines cannot tell the two apart.

  * THE STALENESS ROW IS RE-MEASURED WHERE THE RECORD NOW LIVES.  mg-76cc
    measured "commits from the record's revision to this HEAD: 0" in a
    worktree whose HEAD *was* the record's revision, and wrote beside it that
    "1 is the freshest a committed record can ever be".  On the branch the
    record actually landed on, it is not 0 and it is not 1.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import sys

import libe34a as L

R = L.Report(
    selfpop="the clone, the run_all.sh invocation, every transcript read and "
            "every normalisation this script performs, plus the requirement "
            "that the output population be enumerable from the runner's own "
            "source",
    findpop="for each output run_all.sh writes: that it reproduces byte for "
            "byte or that every line it differs on is explained by the one "
            "revision substitution, that the normalisation acts at the same "
            "positions on both sides, and that the record's revision is an "
            "ancestor of this HEAD -- plus the 2 controls in (v)")

L.banner("K2", "OPEN 2 -- G-3, COUNTED ON FIVE RATHER THAN READ OFF A TABLE")
print("""
The claim under audit is mg-76cc's: 5 of 5 committed outputs reproduce under
a named normalisation, with 0 lines unexplained.  Counted here, on the tree
as it stands on this branch.
""")

# ---------------------------------------------------------------------------
L.rule("(i) THE POPULATION, ENUMERATED FROM run_all.sh's OWN SOURCE")
print("""   Every redirection the runner makes, read out of the runner.  A
   written list of five cannot notice a sixth.""")
print()
runner = L.read_worktree(L.S58DA_DIR + "/run_all.sh")
runs = [ln.strip().split(None, 1)[1].strip()
        for ln in runner.splitlines()
        if ln.strip().startswith("run ") and len(ln.strip().split()) == 2]
tmpl = [ln.strip() for ln in runner.splitlines() if ">" in ln and "out_" in ln]
print("   the redirection in the runner's `run` function:")
for t in tmpl:
    print("      %s" % t[:70])
print()
print("   the scripts it invokes, and the output each writes:")
outs = []
for name in runs:
    o = "out_%s.txt" % name.rsplit(".", 1)[0]
    outs.append(o)
    print("      %-22s -> %s" % (name, o))
print()
print("   %d scripts, %d outputs" % (len(runs), len(outs)))
R.check(len(outs) > 0, "no `run <script>` lines were found in run_all.sh; the "
                       "population below is this script's idea of it and the "
                       "count is withdrawn")
missing = [o for o in outs
           if not os.path.exists(os.path.join(L.REPO, L.S58DA_DIR, o))]
R.check(not missing,
        "the runner writes %s, which is not committed in %s; a committed "
        "record that does not exist cannot fail to reproduce and would be "
        "counted as absent rather than as red"
        % (", ".join(missing), L.S58DA_DIR))
extra = [o for o in outs if o not in L.FIVE_OUTPUTS]
absent = [o for o in L.FIVE_OUTPUTS if o not in outs]
print("   against mg-76cc's written list of five: %d not on it, %d on it and "
      "not written" % (len(extra), len(absent)))
for o in extra:
    print("      the runner writes %s and mg-76cc's list does not have it" % o)
for o in absent:
    print("      mg-76cc's list has %s and the runner does not write it" % o)
R.gate(not extra and not absent,
       "run_all.sh's own redirections and mg-76cc's written FIVE_OUTPUTS "
       "list do not agree: %d written and not listed (%s), %d listed and not "
       "written (%s).  `5 of 5` is then a ratio over the wrong population"
       % (len(extra), ", ".join(extra) or "-", len(absent),
          ", ".join(absent) or "-"))
print()

COMMITTED = {}
for o in outs:
    COMMITTED[o] = L.git_show("HEAD", L.S58DA_DIR + "/" + o)

# ---------------------------------------------------------------------------
L.rule("(ii) run_all.sh IN A CLONE, AND WHAT REPRODUCES BYTE FOR BYTE")
print("""   In a clone, because the runner redirects INTO the very files under
   test: run it in place and the record and the re-run are the same
   bytes for the reason that they were written by the same command.
   Nothing is committed in the clone, so its HEAD is this branch's HEAD
   and the fresh transcripts name a revision that exists outside a temp
   directory.""")
print()
HEAD = L.head_rev()
tmp, tree = L.clone(carry=False, commit=False)
try:
    clone_head = L.head_rev(repo=tree)
    R.check(clone_head == HEAD,
            "the clone's HEAD (%s) is not this branch's HEAD (%s); every row "
            "below is about a tree nobody else has"
            % (clone_head[:12], HEAD[:12]))
    print("   this branch's HEAD  : %s" % HEAD[:12])
    print("   the clone's HEAD    : %s" % clone_head[:12])
    print("     %s" % L.subject(clone_head, repo=tree)[:90])
    print()
    out, rc = L.run_sh(L.S58DA_DIR, "run_all.sh", repo=tree)
    print("   run_all.sh exit %d" % rc)
    print("     (g4_fleet.py is predicted by the runner's own header to exit "
          "1 --")
    print("      mg-d330's second finding, booked OPEN by mg-58da and not "
          "closed here)")
    print()
    FRESH = {}
    for o in outs:
        p = os.path.join(tree, L.S58DA_DIR, o)
        if not os.path.exists(p):
            R.selferr("run_all.sh did not write %s in the clone; it is "
                      "DROPPED from the population rather than counted as "
                      "reproducing" % o)
            continue
        with open(p) as fh:
            FRESH[o] = fh.read()
finally:
    L.destroy(tmp)

print("   file                        committed  re-run  differing  byte for")
print("                               lines      lines   lines      byte")
raw_ok, raw_total, DIFFS = 0, 0, {}
for o in outs:
    if o not in FRESH:
        continue
    a, b = COMMITTED[o], FRESH[o]
    d = [(i + 1, x, y) for i, (x, y) in
         enumerate(zip(a.splitlines() + [None] * max(0, len(b.splitlines())
                                                     - len(a.splitlines())),
                       b.splitlines() + [None] * max(0, len(a.splitlines())
                                                     - len(b.splitlines()))))
         if x != y]
    DIFFS[o] = d
    raw_total += len(d)
    same = (a == b)
    raw_ok += same
    print("     %-26s %-10d %-7d %-10d %s"
          % (o, len(a.splitlines()), len(b.splitlines()), len(d),
             "YES" if same else "no"))
print()
print("   %d of %d reproduce byte for byte, over %d differing lines in all."
      % (raw_ok, len(FRESH), raw_total))
print("   Population: the %d outputs run_all.sh's own source says it writes."
      % len(outs))
print()

# ---------------------------------------------------------------------------
L.rule("(iii) THE ONE REVISION, AND EVERY LINE IT EXPLAINS")
print("""   The record names its own revision on one line of
   out_g1_provenance.txt.  That token, its 12- and 8-character forms and
   the subject g1 prints beside it are replaced by placeholders on the
   RECORD side; the clone's own HEAD and subject are replaced on the
   RE-RUN side.  Nothing else is touched.""")
print()
PLACE_R, PLACE_S = "<HEAD-REVISION>", "<HEAD-SUBJECT>"
SUBJ_WIDTH = 96


def recorded_rev(text):
    """The 12-character revision a transcript says it was taken at.

    Read off g1's `   <sha12>  HEAD of this branch` line.  Returns None if the
    transcript does not say -- which is not the same as saying nothing.
    """
    for raw in text.splitlines():
        s = raw.strip()
        if s.endswith("HEAD of this branch"):
            tok = s.split()[0]
            if len(tok) == 12 and all(c in "0123456789abcdef" for c in tok):
                return tok
    return None


def normalise(text, rev, subj):
    """(text, {lineno: how many substitutions on that line})."""
    hits, lines = {}, []
    for i, line in enumerate(text.splitlines(), start=1):
        n = 0
        for k in (40, 12, 8):
            n += line.count(rev[:k])
            line = line.replace(rev[:k], PLACE_R)
        if subj:
            n += line.count(subj[:SUBJ_WIDTH])
            line = line.replace(subj[:SUBJ_WIDTH], PLACE_S)
        if n:
            hits[i] = n
        lines.append(line)
    return "\n".join(lines), hits


REC12 = recorded_rev(COMMITTED.get("out_g1_provenance.txt", ""))
FRESH12 = recorded_rev(FRESH.get("out_g1_provenance.txt", ""))
R.check(REC12 is not None,
        "the committed out_g1_provenance.txt does not name a revision; there "
        "is nothing to normalise and (iv) is withdrawn")
R.check(FRESH12 is not None,
        "the fresh out_g1_provenance.txt does not name a revision")
print("   the committed record names : %s" % REC12)
print("   the fresh run names        : %s" % FRESH12)
print("   the clone's actual HEAD    : %s" % HEAD[:12])
R.gate(FRESH12 == HEAD[:12],
       "the fresh run's own transcript names %s and it was run at %s; a "
       "transcript that does not name the tree it was taken from cannot be "
       "normalised against it" % (FRESH12, HEAD[:12]))
print()
REC_FULL = L.resolve(REC12) if REC12 else None
REC_SUBJ = L.subject(REC_FULL) if REC_FULL else ""
NEW_SUBJ = L.subject(HEAD)
print("   record's subject  : %s" % REC_SUBJ[:80])
print("   HEAD's subject    : %s" % NEW_SUBJ[:80])
print()
print("   every differing line, and whether the substitution explains it:")
print()
norm_ok, unexplained, POSMISMATCH = 0, [], []
NORMTAB = {}
for o in outs:
    if o not in FRESH:
        continue
    na, ha = normalise(COMMITTED[o], REC_FULL or REC12 or "", REC_SUBJ)
    nb, hb = normalise(FRESH[o], HEAD, NEW_SUBJ)
    la, lb = na.splitlines(), nb.splitlines()
    d = [(i + 1, la[i] if i < len(la) else None, lb[i] if i < len(lb) else None)
         for i in range(max(len(la), len(lb)))
         if (la[i] if i < len(la) else None) != (lb[i] if i < len(lb) else None)]
    NORMTAB[o] = (sum(ha.values()), sum(hb.values()), len(d))
    norm_ok += (len(d) == 0)
    for lineno, x, y in d:
        unexplained.append((o, lineno, x, y))
    # the same positions on both sides
    if set(ha) != set(hb):
        POSMISMATCH.append((o, sorted(set(ha) ^ set(hb))))
    for lineno, x, y in DIFFS[o][:12]:
        expl = lineno not in [u[1] for u in unexplained if u[0] == o]
        print("     %-26s line %-4d %s"
              % (o, lineno, "revision substitution" if expl
                 else "NOT EXPLAINED"))
        if not expl:
            print("        committed: %s" % ((x or "<absent>")[:66]))
            print("        re-run   : %s" % ((y or "<absent>")[:66]))
print()
print("   file                        substitutions  substitutions  lines")
print("                               (committed)    (re-run)       differing")
for o in outs:
    if o not in NORMTAB:
        continue
    a, b, d = NORMTAB[o]
    print("     %-26s %-14d %-14d %d" % (o, a, b, d))
    R.gate(d == 0,
           "%s does not reproduce even with the one revision normalised "
           "away: %d line(s) survive it" % (o, d))
print()
print("   REPRODUCE UNDER THE NAMED NORMALISATION : %d of %d, %d lines "
      "unexplained." % (norm_ok, len(FRESH), len(unexplained)))
for o, lineno, x, y in unexplained:
    print("      %s line %d" % (o, lineno))
    print("         committed: %s" % ((x or "<absent>")[:66]))
    print("         re-run   : %s" % ((y or "<absent>")[:66]))
print()
print("   AND THE SUBSTITUTION ACTS AT THE SAME POSITIONS ON BOTH SIDES.")
print("   A substitution that fires on one side only absorbs a difference")
print("   instead of explaining it, and a count of surviving lines cannot")
print("   tell those apart.")
print("     files where the two sides' substitution positions differ : %d"
      % len(POSMISMATCH))
for o, where in POSMISMATCH:
    print("        %s at line(s) %s" % (o, ", ".join(str(w) for w in where)))
R.gate(not POSMISMATCH,
       "on %d output(s) the revision substitution fires at different line "
       "positions on the committed and re-run sides (%s); those lines are "
       "being absorbed rather than explained"
       % (len(POSMISMATCH), "; ".join("%s: %s" % (o, w)
                                      for o, w in POSMISMATCH)))
print()

# ---------------------------------------------------------------------------
L.rule("(iv) WHERE THE RECORD NOW SITS -- THE ROW mg-76cc MEASURED AS 0")
anc = L.is_ancestor(REC_FULL, "HEAD") if REC_FULL else False
print("   the committed record's revision : %s" % (REC_FULL or "-")[:12])
print("     an ancestor of this branch    : %s" % ("yes" if anc else "NO"))
if anc:
    dist = L.distance(REC_FULL, HEAD)
    print("     commits from it to this HEAD  : %d" % dist)
    print()
    print("""   mg-76cc measured this row as 0 and wrote beside it that "1 is
   the freshest a committed record can ever be".  That was true of the
   worktree it ran in, whose HEAD WAS the record's revision.  On the
   branch the record landed on it is %d: %d commit(s) from other tickets
   landed between the run and the commit.  The row is not gated by
   mg-76cc and is not gated here either -- what it bounds is how much
   the tree may have moved under a transcript that still normalises
   clean, and it is printed because a figure of 0 that is really %d is
   the difference between "written just now" and "written and then
   overtaken".""" % (dist, dist, dist))
R.gate(anc,
       "the revision the committed record names (%s) is not an ancestor of "
       "this branch's HEAD; the record was taken on a tree this branch does "
       "not contain" % (REC_FULL or "-")[:12])
print()

# ---------------------------------------------------------------------------
L.rule("(v) THE NORMALISATION IS NOT A BLANKET -- CONTROLS")
print("""   A comparison that forgives everything reproduces everything.  Two
   perturbations of the COMMITTED side, each of which must still be
   caught after normalisation -- and one of the REVISION itself, which
   must NOT be, because that is what the normalisation is for.""")
print()


def bump_a_digit(text):
    """Increment the last digit of the first line that ends in one.

    Derived from the file rather than written: a control that names a literal
    ("change 198 to 197") silently changes nothing the day that literal is not
    in the file, and a control that changed nothing reports nothing while
    still printing a row.
    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line and line[-1].isdigit():
            lines[i] = line[:-1] + str((int(line[-1]) + 1) % 10)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text


def blank_first_line(text):
    lines = text.splitlines()
    if not lines:
        return text
    lines[0] = "   mg-e34a control line"
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


ALT = L.PRE_7E58_REV or L.REV_A218
ALT_SUBJ = L.subject(ALT)


def swap_revision(text):
    """Make the record name a DIFFERENT real revision, subject and all.

    This is the residual weakness r2 states in its own verdict -- "a
    transcript naming some other real revision would normalise clean" -- and
    it is DEMONSTRATED here rather than restated, because the token is
    re-derived from the mutated transcript exactly as the normalisation
    derives it from the real one.
    """
    t = text.replace(REC12 or "@", ALT[:12])
    t = t.replace((REC_FULL or "@")[:8], ALT[:8])
    if REC_SUBJ:
        t = t.replace(REC_SUBJ[:SUBJ_WIDTH], ALT_SUBJ[:SUBJ_WIDTH])
    return t


# (label, file, mutation, must the difference SURVIVE normalisation?, the
#  revision+subject the mutated record is normalised against)
CONTROLS = [
    ("a digit changed in out_g3_findings.txt", "out_g3_findings.txt",
     bump_a_digit, True, None),
    ("a whole line replaced in out_g4_fleet.txt", "out_g4_fleet.txt",
     blank_first_line, True, None),
    ("the record made to name ANOTHER REAL REVISION, subject and all",
     "out_g2_redo.txt", swap_revision, False, (ALT, ALT_SUBJ)),
]
print("   control                                             applied  "
      "survives  must")
for label, o, fn, must_survive, altnorm in CONTROLS:
    if o not in FRESH:
        R.selferr("the control %r is on %s, which was not produced; it is "
                  "DROPPED rather than counted as passing" % (label, o))
        continue
    before = COMMITTED[o]
    after = fn(before)
    applied = after != before
    rev, subj = altnorm if altnorm else (REC_FULL or "", REC_SUBJ)
    survived = None
    if applied:
        a, _ = normalise(after, rev, subj)
        b, _ = normalise(FRESH[o], HEAD, NEW_SUBJ)
        survived = (a != b)
    print("     %-50s %-8s %-9s %s"
          % (label[:50], "yes" if applied else "NO",
             "-" if survived is None else ("YES" if survived else "no"),
             "survive" if must_survive else "absorb"))
    R.check(applied,
            "the control %r changed nothing, so what it reports is about "
            "nothing; it is DROPPED rather than counted as passing" % label)
    if applied:
        R.gate(survived == must_survive,
               "the control %r %s the normalisation and it must %s it"
               % (label, "survives" if survived else "is absorbed by",
                  "survive" if must_survive else "be absorbed by"))
print()
print("   population: the %d controls above -- %d that must survive the"
      % (len(CONTROLS), len([c for c in CONTROLS if c[3]])))
print("   normalisation and %d that must be absorbed by it.  The third is"
      % len([c for c in CONTROLS if not c[3]]))
print("   NOT a defect being certified: it is the residual weakness r2 names")
print("   in its own verdict, shown rather than asserted.")
print()

# ---------------------------------------------------------------------------
L.rule("VERDICT ON OPEN 2")
print("""   COUNTED, NOT READ OFF A TABLE.

     %d of %d reproduce byte for byte.
     %d of %d reproduce under the one-revision normalisation, with %d
     lines unexplained.

   The population is the %d outputs run_all.sh's own source says it
   writes, and it agrees with mg-76cc's written list.  What the gate
   does NOT establish is unchanged and is not restated as if it did:
   the revision token itself is not reproduced, and the record now sits
   behind this HEAD rather than at it.
""" % (raw_ok, len(FRESH), norm_ok, len(FRESH), len(unexplained), len(outs)))

sys.exit(R.emit())
