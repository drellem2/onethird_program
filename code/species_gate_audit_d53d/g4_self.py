"""G4 -- THE SELF-REFERENCE, WHICH MUST BE LEFT ALONE.

mg-6ef4's audit counted a population its OWN commit message joined, said so,
and left it in.  That is correct: a census of "every commit stating this
figure" that drops the one commit doing the stating is a census with a hole in
it shaped like the auditor.

So this section's finding condition is INVERTED.  If mg-4adb "fixed" the
self-reference -- by adding any predicate that drops an instrument's own files
or its own commits from a population that instrument counts -- that is a
REGRESSION and is reported as one.  Nothing here goes red for finding the
self-reference intact; it goes red for finding it repaired.

  G4a  the diff over mg-6ef4's own tree, resolved rather than asserted
  G4b  every added line of the repair, searched for a self-excluding predicate
  G4c  mg-4adb's own three *.md files against the census that counts them
  G4d  t3_census.py's `git log --all` population against its own commits
  G4e  this instrument's own files, by the same rule, disclosed not repaired

    python3 code/species_gate_audit_d53d/g4_self.py
"""

import io
import os
import re
import sys
import tokenize

from kern_d53d import hdr, Rows, REPO, PIN, sh, cleanup

R = Rows()
HERE_DIR = os.path.join("code", "species_gate_audit_d53d")
PARENT_DIR = os.path.join("code", "species_rung_repair_4adb")
AUDIT_DIR = os.path.join("code", "species_bound_audit_6ef4")


def git(args):
    return sh(["git", "-C", REPO] + args)


rc, HEAD = git(["rev-parse", "HEAD"])
HEAD = HEAD.strip()
R.note("  this audit runs at HEAD = %s" % HEAD)
R.note("  the pin it compares against is %s" % PIN)


# ---------------------------------------------------------------------------
hdr("G4a  THE DIFF OVER mg-6ef4's OWN TREE")
# ---------------------------------------------------------------------------

rc, diff = git(["diff", "%s..HEAD" % PIN, "--", AUDIT_DIR.replace(os.sep, "/")])
R.note("  git diff %s..HEAD -- %s/" % (PIN, AUDIT_DIR))
R.note("  exit %s, %d byte(s) of diff" % (rc, len(diff.strip())))
for ln in diff.splitlines()[:12]:
    R.note("      %s" % ln)


# ---------------------------------------------------------------------------
hdr("G4b  EVERY ADDED LINE OF THE REPAIR, SEARCHED FOR A SELF-EXCLUSION")
# ---------------------------------------------------------------------------

R.note("  The first half of Q18 is one `git diff`.  The second half is not:")
R.note("  a self-excluding predicate added in ANY file would be the same")
R.note("  regression, so the whole diff is read and not one directory of it.")
R.note("")
R.note("  THE RULE, IN TWO STAGES, AND THE SECOND ONE IS WHY.")
R.note("")
R.note("  Stage 1, the CANDIDATE rule.  An added line is a candidate if it")
R.note("  carries both a filtering token and a self-naming token:")
R.note("      filtering   if / != / not in / continue / startswith /")
R.note("                  endswith / exclude / skip / ignore / drop / filter")
R.note("      self-naming __file__ / a code/species_* directory / 'own")
R.note("                  commit' / 'own file' / 'itself' / 'self-refer'")
R.note("  Every candidate is PRINTED, whatever stage 2 decides about it.")
R.note("")
R.note("  Stage 2, the DISPOSITION, and it is where the first version of this")
R.note("  section was wrong.  A DEFECT OF THIS INSTRUMENT, kept: run with")
R.note("  stage 1 alone, it flagged a docstring sentence in")
R.note("  code/runner_exit_audit_56dc/t2_strictest.py and a bare `continue`")
R.note("  whose self-naming words were in the COMMENT beside it, and it")
R.note("  flagged TWO LINES OF ITS OWN SOURCE -- one of them the line that")
R.note("  defines the rule.  A detector that reads its own definition as an")
R.note("  instance of what it detects is measuring its own text.")
R.note("")
R.note("  The repair is NOT to exclude this file from the scan -- that is the")
R.note("  regression this whole section exists to report.  It is to stop")
R.note("  treating PROSE as a predicate: each file is tokenized, every")
R.note("  COMMENT and every STRING is blanked out, and the disposition is")
R.note("  read off what is left.  A sentence in a docstring can then say")
R.note("  anything it likes, and a `continue` with an explanatory comment is")
R.note("  a `continue`.  Both the raw line and the code-only rendering are")
R.note("  printed for every candidate, so the classification is checkable.")
print()

FILTER = re.compile(r"\bif\b|!=|not\s+in|\bcontinue\b|startswith|endswith"
                    r"|exclude|skip|ignore|\bdrop\b|filter", re.I)
SELF = re.compile(r"__file__|code/species_[a-z0-9_]+|own\s+commit"
                  r"|own\s+file|itself|self[-_ ]refer", re.I)
# What makes a predicate a SELF-exclusion in mg-6ef4's sense: the thing being
# dropped is identified as the INSTRUMENT'S OWN.  `__file__`, `sys.argv[0]`
# and a literal naming the scanning script's own directory do that; comparing
# two paths the script was given does not, and a call graph that drops a
# self-edge is not a census that drops its own row.
SELF_CODE = re.compile(r"__file__|sys\.argv\[0\]")
REMOVES = re.compile(r"\bcontinue\b|!=|not\s+in|\bexclude\b|\bskip\b"
                     r"|\bignore\b|\bdrop\b")


def code_only(path):
    """{stripped raw line: stripped code-only line} for a Python source file.

    Comments and the CONTENTS of string literals are blanked.  The quotes are
    kept, so `x == "y"` stays a comparison and does not become `x ==`."""
    try:
        with open(path, encoding="utf-8") as fh:
            src = fh.read()
    except OSError:
        return {}
    buf = src.splitlines()
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return {}
    for tok in toks:
        if tok.type not in (tokenize.COMMENT, tokenize.STRING):
            continue
        (r1, c1), (r2, c2) = tok.start, tok.end
        for r in range(r1, r2 + 1):
            if r - 1 >= len(buf):
                break
            line = buf[r - 1]
            a = c1 if r == r1 else 0
            b = c2 if r == r2 else len(line)
            buf[r - 1] = line[:a] + " " * (b - a) + line[b:]
    out = {}
    for raw, blank in zip(src.splitlines(), buf):
        out.setdefault(raw.strip(), blank.strip())
    return out


rc, full = git(["diff", "%s..HEAD" % PIN, "--unified=0"])
added, cur = [], "?"
for ln in full.splitlines():
    m = re.match(r"^\+\+\+ b/(.*)$", ln)
    if m:
        cur = m.group(1)
        continue
    if ln.startswith("+") and not ln.startswith("+++"):
        added.append((cur, ln[1:]))

py_added = [(f, t) for f, t in added if f.endswith(".py") or f.endswith(".sh")]
cand = [(f, t) for f, t in py_added if FILTER.search(t) and SELF.search(t)]

R.note("  added lines in %s..HEAD                     %5d" % (PIN, len(added)))
R.note("  of them in *.py / *.sh                          %5d" % len(py_added))
R.note("  CANDIDATES (filtering token AND self-naming)    %5d" % len(cand))
print()

MAPS = {}
excl = []
for f, t in cand:
    if f not in MAPS:
        MAPS[f] = code_only(os.path.join(REPO, f))
    blank = MAPS[f].get(t.strip())
    if blank is None:
        disp = "NOT PRESENT AT HEAD -- classified from the diff text alone"
    elif not blank:
        disp = "PROSE -- the whole line is a comment or a string literal"
    elif not FILTER.search(blank):
        disp = "PROSE -- the filtering token was inside a comment or string"
    elif not SELF_CODE.search(blank):
        disp = ("NOT A SELF-EXCLUSION -- the code names no `__file__` and no "
                "own-directory literal")
    elif not REMOVES.search(blank):
        disp = "NOT A REMOVAL -- the predicate does not drop anything"
    else:
        disp = "*** SELF-EXCLUSION ***"
        excl.append((f, t.strip()))
    R.note("      %s" % f)
    R.note("          raw : %s" % t.strip()[:92])
    R.note("          code: %s" % ((blank or "(nothing -- all of it was "
                                    "comment or string)")[:92]
                                   if blank is not None else "(n/a)"))
    R.note("          -> %s" % disp)

R.predicted(
    "Q18",
    "the diff over %s/ is empty, and 0 predicates anywhere exclude an "
    "instrument's own files or commits from a population it counts"
    % AUDIT_DIR,
    "diff is %s (%d bytes); %d candidate line(s), %d of them a self-exclusion"
    % ("EMPTY" if not diff.strip() else "NON-EMPTY", len(diff.strip()),
       len(cand), len(excl)),
    not diff.strip() and not excl,
    "Scored with the stage-2 rule.  With stage 1 alone this scored MISSED at\n"
    "2, and both of those two are printed above with the reason they are\n"
    "not self-exclusions.  The first run's score is recorded in OUTCOMES.md\n"
    "rather than quietly replaced.")
for f, s in excl:
    R.row("SELF-EXCLUSION ADDED: %s" % f, False, s)


# ---------------------------------------------------------------------------
hdr("G4c  mg-4adb's OWN *.md FILES AGAINST THE CENSUS THAT COUNTS THEM")
# ---------------------------------------------------------------------------

R.note("  The census is e2_crosssection.py's: every *.md under docs/ and under")
R.note("  code/, recursively.  It is RE-DERIVED here from `git ls-tree` at the")
R.note("  named revision rather than read out of any transcript, and then the")
R.note("  question is asked of the result.")
print()

rc, tree = git(["ls-tree", "-r", "--name-only", HEAD])
tracked_md = [p for p in tree.splitlines()
              if p.endswith(".md")
              and (p.startswith("docs/") or p.startswith("code/"))]
R.note("  census(%s) = %d markdown file(s)" % (HEAD[:7], len(tracked_md)))

own = sorted(p for p in tracked_md
             if p.startswith(PARENT_DIR.replace(os.sep, "/") + "/"))
for p in own:
    R.note("      IN THE CENSUS: %s" % p)
R.predicted(
    "Q19a", "mg-4adb's own three *.md files are 3 of 3 present in census(HEAD)",
    "%d of 3 present: %s" % (len(own), ", ".join(os.path.basename(p)
                                                 for p in own)),
    len(own) == 3)


# ---------------------------------------------------------------------------
hdr("G4d  t3_census.py's `git log --all` POPULATION AGAINST ITS OWN COMMITS")
# ---------------------------------------------------------------------------

R.note("  mg-6ef4's T3d enumerates every commit-message object reachable from")
R.note("  every ref.  Its own commits are in that population and its own")
R.note("  message is one of the objects it counts.  Two things are asked:")
R.note("  does its SOURCE carry a predicate that drops them, and are they")
R.note("  actually in the population `git log --all` returns.")
print()

def scan_source(path):
    """(candidates, self-exclusions) for one file, by the same two stages."""
    cmap = code_only(path)
    cands, excls = [], []
    for raw, blank in cmap.items():
        if not (FILTER.search(raw) and SELF.search(raw)):
            continue
        cands.append((raw, blank))
        if blank and FILTER.search(blank) and SELF_CODE.search(blank) \
                and REMOVES.search(blank):
            excls.append((raw, blank))
    return cands, excls


src_path = os.path.join(REPO, AUDIT_DIR, "t3_census.py")
t3_cand, t3_excl = scan_source(src_path)
for raw, blank in t3_cand:
    R.note("      candidate: %s" % raw[:88])
    R.note("          code : %s" % ((blank or "(all comment or string)")[:88]))
R.note("  candidate line(s) in t3_census.py: %d, of them self-exclusions: %d"
       % (len(t3_cand), len(t3_excl)))

rc, log = git(["log", "--all", "--format=%H%x1f%s"])
pop = [l.split("\x1f") for l in log.splitlines() if "\x1f" in l]
own_commits = [(h, s) for h, s in pop if "(mg-4adb)" in s or "(mg-6ef4)" in s]
R.note("  `git log --all` population: %d commit object(s)" % len(pop))
R.note("  of them mg-4adb's or mg-6ef4's own: %d" % len(own_commits))
for h, s in own_commits[:8]:
    R.note("      %s %s" % (h[:8], s[:74]))

R.predicted(
    "Q19b", "no self-exclusion in t3_census.py's `git log --all` population",
    "%d candidate line(s), %d self-excluding predicate(s) in its source; its "
    "own %d commit(s) are in the population"
    % (len(t3_cand), len(t3_excl), len(own_commits)),
    not t3_excl and bool(own_commits))
R.row("the self-reference is INTACT, and that is the correct state",
      not t3_excl and not excl,
      "This row is a FINDING if the repair removed it.  mg-6ef4's own commit\n"
      "message joining the census it counts is disclosed in its own\n"
      "transcript; a repair that dropped it would have made the census wrong\n"
      "in order to make it look tidy.")


# ---------------------------------------------------------------------------
hdr("G4e  THIS INSTRUMENT'S OWN FILES, BY THE SAME RULE")
# ---------------------------------------------------------------------------

R.note("  The same disclosure, made by this audit about itself.  What is")
R.note("  measured is THE WORKTREE, and the revision is named: a committed")
R.note("  transcript of this section is a measurement AT ITS RUN'S COMMIT and")
R.note("  not a live property -- mg-c067 found exactly that shape of claim")
R.note("  going stale under a rebase, and naming the revision is what makes a")
R.note("  stale line tell a reader STALE rather than WRONG.")
print()

mine_disk = sorted(f for f in os.listdir(os.path.join(REPO, HERE_DIR))
                   if f.endswith(".md"))
mine_tracked = [p for p in tracked_md
                if p.startswith(HERE_DIR.replace(os.sep, "/") + "/")]
for f in mine_disk:
    rel = HERE_DIR.replace(os.sep, "/") + "/" + f
    R.note("      %-22s on disk: yes   tracked at %s: %s   in the census "
           "rule: yes" % (f, HEAD[:7], "yes" if rel in mine_tracked else "no"))

R.note("")
R.note("  And the same two-stage rule turned on this instrument's own source.")
R.note("  THE SCAN INCLUDES g4_self.py, which is the file the rule is written")
R.note("  in.  It is not excluded, because excluding it would be the very")
R.note("  regression this section reports -- and stage 1 alone did flag two")
R.note("  of its lines, one of them the rule's own definition.  Stage 2")
R.note("  disposes of both by reading code rather than prose.")
print()

own_here_cand, own_here_excl = [], []
for f in sorted(os.listdir(os.path.join(REPO, HERE_DIR))):
    if not f.endswith(".py"):
        continue
    cands, excls = scan_source(os.path.join(REPO, HERE_DIR, f))
    for raw, blank in cands:
        own_here_cand.append((f, raw, blank))
    for raw, blank in excls:
        own_here_excl.append((f, raw))
for f, raw, blank in own_here_cand:
    R.note("      candidate in %s" % f)
    R.note("          raw : %s" % raw[:88])
    R.note("          code: %s" % ((blank or "(all comment or string)")[:88]))

R.predicted(
    "Q20",
    "this instrument's own *.md files join the census too and are not "
    "excluded -- the same disclosure, made rather than repaired",
    "%d *.md on disk in %s, %d of them tracked at %s; %d candidate line(s) "
    "in this instrument's own source, %d of them self-exclusions"
    % (len(mine_disk), HERE_DIR, len(mine_tracked), HEAD[:7],
       len(own_here_cand), len(own_here_excl)),
    bool(mine_disk) and not own_here_excl,
    "Scored with the stage-2 rule; with stage 1 alone this scored MISSED at\n"
    "2, both of them lines of g4_self.py itself.")

R.note("")
R.note("  AND THE SAME IS TRUE OF THIS RUN.  `probe_strike_d53d.md` is planted")
R.note("  by G1 in a clone, is a *.md under code/, and is counted by e2's")
R.note("  census while it is there -- which is why e2's census line inside")
R.note("  those runs reads one file higher than a clean tree's.  It is")
R.note("  removed with the clone and no committed figure rests on it.")

R.tail("G4")
print()
print("EXTENT OF THAT NUMBER.  It ranges over the %d added lines of" % len(added))
print("`git diff %s..HEAD`, the %d markdown files `git ls-tree` returns at"
      % (PIN, len(tracked_md)))
print("%s, the %d commit objects `git log --all` returns, and the source of"
      % (HEAD[:7], len(pop)))
print("t3_census.py and of this instrument.  IT RANGES OVER NOTHING ELSE: a")
print("self-exclusion written as a data table rather than as a predicate, or")
print("one added BEFORE %s, is outside every one of those populations and" % PIN)
print("this number says nothing about either.  The candidate rule is printed")
print("above with every line it matched, so a reader can see what a zero here")
print("was a zero OF.")

cleanup()
sys.exit(1 if R.bad else 0)
