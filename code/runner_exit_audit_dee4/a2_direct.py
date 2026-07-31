"""A2 -- WERE THE STATUSES READ DIRECTLY, AND AT WHAT GRAIN?

mg-7522 claims, in its commit message, its README, its OUTCOMES.md, its
published document and its own transcript:

    "the 11 discarded statuses read directly, 11 of 11 exit 0, so the
     corrected population of 45 has now been read in full"

The audit ticket asks specifically whether those were read DIRECTLY, the way
mg-c2b3's 34 were, rather than inferred from the presence of a fix.  Two
different things are being claimed and they have different evidence:

  A2a  THE 8 `| tee` SITES.  In `s2_status.py` these are DERIVED: the rows come
       from `tee_pipelines(pre)` and `invocation(line)` over the runner's own
       pre-repair bytes.  A2a re-derives that list independently and checks
       that the transcript's 8 rows are exactly it.

  A2b  THE 3 `git diff` SITES.  These are NOT derived.  They are a hand-written
       list of three argv in the body of `s2_status.py`, and this is where the
       finding is:

         * all three source lines sit INSIDE `for` loops, so the three lines
           execute EIGHT discarded `git diff`s at run time, not three;
         * the row labelled `state_delegation_audit_16eb/run_all.sh:39` runs a
           command that is not on line 39.  Line 39 is the `nmd=` line and
           carries a `':!*.md'` pathspec; the hand-written argv has no
           pathspec and uses the SECOND loop pair of line 38.

       So the `':!*.md'` form -- one of the three lines the whole section is
       about -- has no status read anywhere in any shape, and four of the eight
       runtime executions were never run at all.  (Three hand-listed argv, two
       DISTINCT commands, covering four of eight by argv-identity.)

  A2c  ALL EIGHT, READ DIRECTLY.  Rather than report a hole, this probe fills
       it: every one of the eight is executed as a list argv and its exit code
       read.  If they are all 0, mg-7522's CONCLUSION survives at the finer
       grain and only its enumeration was wrong.  That is the honest shape of
       the finding and it is printed either way.

  A2d  THE WORD "VERIFIED".  `OUTCOMES.md` says the byte counts are "verified
       against the pre-repair output (`0 / 0 / 0 / 0 / 2111 / 0`, unchanged)".
       No probe in mg-7522's tree computes a byte count.  Both arms are run
       here on the same inputs -- the pre-repair pipeline and the post-repair
       redirect -- and compared value by value.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libdee4 as L

BAD = 0
FINDINGS = []
OUTSIDE = ("code/face_geometry_audit_f1b2/run_audit.sh",
           "code/face_geometry_audit_fcf1/run_audit.sh")

L.bar("A2  THE STATUSES, READ DIRECTLY -- AND AT WHICH GRAIN")

# ---------------------------------------------------------------------------
L.hdr("A2a  THE 8 `| tee` SITES -- DERIVED, NOT LISTED")

print("  COMPARISON, so the pre-repair bytes are read at the pin %s," % L.PINNED)
print("  which is the anchor `s2_status.py` itself uses for this arm.")
print()
derived = []
for runner in OUTSIDE:
    pre = L.read(runner, L.PINNED)
    for n, line in L.tee_pipelines(pre):
        inv = L.invocation(line)
        derived.append((runner, n, inv[1] if inv else "*** NOT PARSED ***"))
print("    %-46s %-6s %s" % ("runner", "line", "discarded stage"))
L.rows([(r, n, s) for r, n, s in derived], (46, 6), indent="    ")
print()
print("      derived `| tee` sites                      %4d" % len(derived))

TRANS = "%s/out_s2_status.txt" % L.TREE
trans = L.read(TRANS, None) if L.exists(TRANS, None) else ""
rows_in_transcript = [l for l in trans.splitlines()
                      if "run_audit.sh:" in l and "nothing was being" in l]
print("      rows in mg-7522's committed transcript     %4d" % len(rows_in_transcript))
for r, n, s in derived:
    tag = "%s:%d" % (os.path.basename(os.path.dirname(r)) + "/"
                     + os.path.basename(r), n)
    if not any(tag in l and s in l for l in rows_in_transcript):
        BAD += 1
        FINDINGS.append("A2a %s %s absent from mg-7522's transcript" % (tag, s))
        print("          *** %s %s not found in the transcript" % (tag, s))
print()
print("  VERDICT.  These 8 are read DIRECTLY and the list is DERIVED from the")
print("  runner's own bytes -- the row set cannot drift from the source, and")
print("  the transcript carries a real exit code and a real wall time for")
print("  each.  This half of the claim is sound.")

# ---------------------------------------------------------------------------
L.hdr("A2b  THE 3 `git diff` SITES -- A HAND-LIST, AT THE WRONG GRAIN")

# mg-7522's hand-written list, copied verbatim from s2_status.py so that the
# comparison is against what the probe RAN and not against what it said.
GITROWS = [
    ("code/state_delegation_audit_16eb/run_all.sh", 38,
     ["git", "diff", "a4aeeb9..HEAD", "--", "code/state_layer_audit_218d"]),
    ("code/state_delegation_audit_16eb/run_all.sh", 39,
     ["git", "diff", "3a80d99..HEAD", "--", "code/state_delegation_audit_5644"]),
    ("code/state_delegation_repair_0049/run_all.sh", 39,
     ["git", "diff", "a4aeeb9..HEAD", "--", "code/state_layer_audit_218d"]),
]

print("  THE SOURCE LINES, at %s -- the bytes mg-7522 repaired:" % L.PRE_REPAIR)
print()
srcs = {}
for path in sorted({p for p, _n, _a in GITROWS}):
    srcs[path] = L.read(path, L.PRE_REPAIR).split("\n")
for path, n, argv in GITROWS:
    line = srcs[path][n - 1].strip()
    print("      %s:%d" % (path, n))
    print("          source : %s" % line[:66])
    print("          RAN    : %s" % " ".join(argv))
    src_has_pathspec = ":!" in line
    argv_has_pathspec = any(":!" in a for a in argv)
    if src_has_pathspec != argv_has_pathspec:
        BAD += 1
        FINDINGS.append(
            "A2b %s:%d -- the source line carries a `':!*.md'` pathspec and "
            "the argv that was run does not; the discarded stage of that line "
            "was never executed" % (path, n))
        print("          *** the source line has a `':!*.md'` pathspec and the")
        print("              argv does not.  This row did not run line %d's" % n)
        print("              discarded stage; it ran line %d's, second"
              % (n - 1))
        print("              loop iteration, under line %d's label. ***" % n)
    print()

print("  THE LOOPS.  Each line sits inside a `for pair in ...` loop, so the")
print("  number of discarded statuses at RUN TIME is not the number of lines:")
print()
# EXECUTION ORDER, not source order: the loop runs every pipeline line once
# per pair, so the sequence is (pair 1, line 38), (pair 1, line 39), (pair 2,
# line 38)...  Ordering it any other way would make a multiset comparison with
# OUTCOMES.md's `0 / 0 / 0 / 0 / 2111 / 0` read as a difference when it is a
# permutation, which is an error of the instrument and not of the subject.
EXPANDED = []
for path in sorted(srcs):
    ls = srcs[path]
    pairs, plines = [], []
    for i, l in enumerate(ls, 1):
        if l.strip().startswith("for pair in"):
            buf, j = l, i
            while buf.rstrip().endswith("\\") and j < len(ls):
                buf += ls[j]
                j += 1
            for tok in buf.split('"')[1::2]:
                if " " in tok.strip():
                    base, d = tok.strip().split(None, 1)
                    pairs.append((base, d))
        if "wc -c" in l and "$(git diff" in l:
            plines.append((i, l))
    for base, d in pairs:
        for i, l in plines:
            argv = ["git", "diff", "%s..HEAD" % base, "--", d]
            if ":!" in l:
                argv.append(":!*.md")
            EXPANDED.append((path, i, argv))
    print("      %-48s %d pair(s), %d pipeline line(s), %d execution(s)"
          % (path, len(pairs), len(plines), len(pairs) * len(plines)))
print()
print("      pipeline LINES mg-7522 counted             %4d" % len(GITROWS))
print("      argv mg-7522 hand-listed                   %4d" % len(GITROWS))
print("      DISTINCT commands among them               %4d"
      % len({" ".join(a) for _p, _n, a in GITROWS}))
print("      discarded `git diff` EXECUTIONS at run time %3d" % len(EXPANDED))
ran = {(" ".join(a)) for _p, _n, a in GITROWS}
never = [(p, n, a) for p, n, a in EXPANDED if " ".join(a) not in ran]
print("      of those, never executed by mg-7522        %4d" % len(never))
for p, n, a in never:
    print("          %s:%d  %s" % (os.path.basename(os.path.dirname(p)), n,
                                   " ".join(a[1:])))
if never:
    BAD += 1
    FINDINGS.append(
        "A2b the 3 `git diff` rows are a hand-list of %d argv (%d distinct "
        "commands) over source lines that execute %d discarded statuses at "
        "run time; %d of the %d were never run, and the `':!*.md'` form of "
        "line 39 was never run in any shape"
        % (len(GITROWS), len(ran), len(EXPANDED), len(never), len(EXPANDED)))

# ---------------------------------------------------------------------------
L.hdr("A2c  ALL EIGHT, READ DIRECTLY -- FILLING THE HOLE RATHER THAN REPORTING IT")

print("  Each row runs the DISCARDED stage with nothing in the way and reads")
print("  its exit status -- the number `wc -c` replaced with its own.  This")
print("  is mg-c2b3's K3b method and mg-7522's own, applied at the grain the")
print("  source lines actually execute at.  LIST argv, no shell, so")
print("  `returncode` is the target's own status.")
print()
print("    %-42s %-46s %s" % ("source line", "discarded stage", "exit"))
nonzero = []
for p, n, argv in EXPANDED:
    code, _out = L.run_argv(argv, L.REPO, timeout=300)
    if code != 0:
        nonzero.append((p, n, argv, code))
    print("    %-42s %-46s %s"
          % ("%s:%d" % (os.path.basename(os.path.dirname(p)), n),
             " ".join(argv[1:])[:46], L.code_str(code)))
print()
print("      %d of %d exit 0" % (len(EXPANDED) - len(nonzero), len(EXPANDED)))
if nonzero:
    BAD += 1
    FINDINGS.append("A2c %d of %d discarded statuses are NON-ZERO"
                    % (len(nonzero), len(EXPANDED)))
else:
    print()
    print("  SO THE CONCLUSION SURVIVES AND THE ENUMERATION DOES NOT.")
    print("  mg-7522's retroactive clearance said `11 of 11`.  At the grain")
    print("  the source actually executes, the eleven lines are EIGHT `| tee`")
    print("  invocations plus EIGHT `git diff` invocations = 16 discarded")
    print("  statuses.  mg-7522 read the 8 tee ones, and 3 hand-listed argv")
    print("  (2 distinct commands) covering 4 of the 8 git ones.  All 8 git")
    print("  ones read here are 0, so nothing was being swallowed: the")
    print("  finding is about the word DIRECTLY and about the population --")
    print("  which is the whole subject of this ticket -- and not about the")
    print("  verdict.")
print()
print("  WHAT REMAINS UNEXAMINED, named rather than folded into a total:")
print("      * the same fact at every intermediate commit.  Read at HEAD, on")
print("        one machine.  mg-7522 states this too and it is inherited.")
print("      * the 34 of mg-c2b3's own population are NOT re-run here.  They")
print("        are cited, not re-measured, and `45 of 45` is therefore 8 of 8")
print("        re-derived by me plus 3 re-derived by me plus 34 INHERITED.")

# ---------------------------------------------------------------------------
L.hdr("A2d  THE WORD `VERIFIED` -- THE BYTE COUNTS, ON BOTH ARMS")

print("  OUTCOMES.md: \"`wc -c < FILE` counts the same bytes the pipeline")
print("  did, verified against the pre-repair output (`0 / 0 / 0 / 0 / 2111")
print("  / 0`, unchanged)\".  `verified` is one of the three markers")
print("  mg-7522's own general form names, and NO probe in its tree computes")
print("  a byte count.  So both arms are run here, on the same inputs.")
print()
CLAIMED_SIX = ["0", "0", "0", "0", "2111", "0"]
pre_vals, post_vals = [], []
import subprocess
for p, n, argv in EXPANDED:
    # PRE-REPAIR ARM: the pipeline as it stood.  This is the one place a shell
    # is deliberately used, because reproducing the pipeline IS the check.  It
    # is `/bin/sh -c` with a list argv whose single string is written here, and
    # its own returncode is read below.
    shell_text = "%s | wc -c | tr -d ' '" % " ".join(
        "'%s'" % a if ":!" in a else a for a in argv)
    c1, o1 = L.run_argv(["/bin/sh", "-c", shell_text], L.REPO, timeout=300)
    # POST-REPAIR ARM: redirect, guard, then `wc -c < FILE`.
    tmp = os.path.join(L.REPO, "_dee4_diff.tmp")
    with open(tmp, "wb") as fh:
        pp = subprocess.run(argv, cwd=L.REPO, stdout=fh, stderr=subprocess.PIPE)
    size = os.path.getsize(tmp)
    os.unlink(tmp)
    pre_vals.append(o1.strip())
    post_vals.append(str(size))
    ok = o1.strip() == str(size) and c1 == 0 and pp.returncode == 0
    if not ok:
        BAD += 1
        FINDINGS.append("A2d byte counts differ at %s:%d" % (p, n))
    print("      %-40s pre %-8s post %-8s %s"
          % ("%s:%d" % (os.path.basename(os.path.dirname(p)), n),
             o1.strip(), size, "AGREE" if ok else "*** DIFFER ***"))
print()
six = post_vals[:6]
print("      the six values of state_delegation_audit_16eb : %s"
      % " / ".join(six))
print("      OUTCOMES.md says                              : %s"
      % " / ".join(CLAIMED_SIX))
if six == CLAIMED_SIX:
    print("      -> the `verified` claim HOLDS, re-derived on both arms")
else:
    BAD += 1
    FINDINGS.append("A2d the six byte counts are %s, OUTCOMES.md says %s"
                    % (" / ".join(six), " / ".join(CLAIMED_SIX)))
print()
print("  AND THE HALF THE FIGURE DOES NOT COVER.  OUTCOMES.md's parenthesis")
print("  lists SIX values, and `state_delegation_repair_0049` executes two")
print("  more that are not in it:")
print("      state_delegation_repair_0049 : %s" % " / ".join(post_vals[6:]))
print("  They are unchanged too, so the claim is true; it is named because a")
print("  figure covering 6 of 8 under the sentence `the byte counts` is the")
print("  same shape as `11 of 11` covering 4 of 8.")

print()
L.bar("A2 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts a derived `| tee` site missing from")
print("mg-7522's transcript, a hand-listed argv that does not match the")
print("source line it is labelled with, a runtime execution never read, a")
print("non-zero discarded status, and a byte count that moved between the")
print("two arms.  It ranges over the 11 pipeline lines mg-7522 names and the")
print("16 discarded statuses they execute.  It does NOT range over mg-c2b3's")
print("own 34, which are INHERITED here and not re-measured.")
print()
for f in FINDINGS:
    print("FINDING: %s" % f)
sys.exit(1 if BAD else 0)
