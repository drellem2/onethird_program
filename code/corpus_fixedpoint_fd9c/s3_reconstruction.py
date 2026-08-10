"""mg-fd9c / S3 -- IS THE RECONSTRUCTED ROW THE ANSWER?

THE TICKET'S ITEM 3, in full: *It is byte-stable across the same seven runs,
which is the one stable instrument we have.  If reconstruction is the fix, say
what it costs and what it cannot measure.  If it is not, say why.*

The answer this probe reaches is **yes for the published record and no for the
run**, and the two halves are not a hedge -- they are two different questions
that the word `corpus` has been carrying at once:

  what was COMMITTED at ref X          -- a reconstruction answers it, exactly,
                                          forever, and is the right question
                                          for anything anyone publishes;
  what a probe RANGED OVER when it ran -- a reconstruction cannot answer it at
                                          all, because a tree's transcripts are
                                          untracked on the run that writes
                                          them, and that is the documented
                                          reason this arc globs the disk.

  S3a  the reconstruction is stable, and stable for a reason that is checkable
  S3b  WHAT IT CANNOT MEASURE -- with a size on each thing
  S3c  WHAT IT COSTS -- reachability, and a hand fact per figure
  S3d  the third option, which is neither, and is what S4 turns into a rule

Exit code = number of S3 checks that fail.
"""

import sys

import libfd9c as U

BAD = 0
A = U.A
B = U.B
G = U.G

U.bar("mg-fd9c / S3 -- IS THE RECONSTRUCTED ROW THE ANSWER?")
print("HEAD: %s" % U.head())

# ---------------------------------------------------------------------------
U.hdr("S3a  THE RECONSTRUCTION IS STABLE, AND FOR A CHECKABLE REASON")

recon_files = G.parent_corpus()
recon = U.census(B.read(p, r) for p, r in recon_files)
disk = U.census_from(U.file_stats())

print("  mg-9160's reconstruction is `everything tracked at %s` plus"
      % G.PARENT_REV)
print("  `mg-03d1's own seven transcripts as published at %s`."
      % G.PARENT_PUB)
print()
U.pop("the %d (path, ref) pairs `lib9160.parent_corpus()` returns"
      % len(recon_files))
print("      %-46s %s" % ("corpus", U.HEADFMT))
print("      %-46s %s" % ("the reconstruction", U.fmt(recon)))
print("      %-46s %s" % ("mg-03d1's published figures", "   517   1191    246"
                          "    626    400"))
print("      %-46s %s" % ("the disk at HEAD, for contrast", U.fmt(disk)))
print()
ok = tuple(recon[f] for f in U.FIELDS) == (517, 1191, 246, 626, 400)
print("      the reconstruction reproduces, field for field           %s"
      % ("yes" if ok else "*** NO"))
BAD += not ok
print()
print("  WHY IT IS STABLE, and this is the part worth more than the row: its")
print("  input is not a directory, it is a LIST OF BLOB HASHES.  Every path in")
print("  it resolves through `git ls-tree` at a fixed commit, so the census is")
print("  a function of two 40-character strings and of nothing else on this")
print("  machine.  A file arriving on disk cannot enter it; a file leaving")
print("  cannot leave it.")
print()
h = U.git("rev-parse", "%s^{tree}" % G.PARENT_REV).strip()[:12]
h2 = U.git("rev-parse", "%s^{tree}" % G.PARENT_PUB).strip()[:12]
print("      the two trees the reconstruction is a function of:")
print("          %s   %s" % (G.PARENT_REV, h))
print("          %s   %s" % (G.PARENT_PUB, h2))
print()
print("  AND THE LIVE DEMONSTRATION.  Since mg-03d1 published, the arc has")
print("  grown by %d transcripts and %d count rows -- S2d walks the %d commits"
      % (disk["files"] - 517, disk["rows"] - 1191, 245))
print("  that did it.  The reconstruction above is computed on THIS disk,")
print("  after all of that, and it still says 517 / 1191 / 246 / 626 / 400.")

# ---------------------------------------------------------------------------
U.hdr("S3b  WHAT A RECONSTRUCTION CANNOT MEASURE -- WITH A SIZE ON EACH")

print("  (1) IT CANNOT SEE AN UNTRACKED FILE, AND THAT IS THE WHOLE REASON")
print("      THIS ARC GLOBS THE DISK.  `lib56dc.outs()` says so in its own")
print("      docstring: *a tree's transcripts are untracked on the run that")
print("      first writes them, and an index-built corpus is empty on that")
print("      run.*  So on the ONE run whose output gets published, a")
print("      reconstruction of that run's corpus is short by the whole tree.")
print()
for tree in ("code/grain_axis_audit_03d1", "code/grain_arity_9160", U.TREE):
    n = len([p for p in B.all_transcripts() if p.startswith(tree + "/")])
    print("      %-46s %3d transcripts invisible on its own first run"
          % (tree, n))
print("      ^ one unit of each is one file")
print()
print("  (2) IT CANNOT BE COMPUTED FROM ANY SINGLE COMMIT.  S2d walks 245")
print("      commits and mg-03d1's `517 / 1191` is the answer at NONE of")
print("      them.  Its figures live at a UNION of two refs -- which is not a")
print("      state this repository was ever in, and is exactly what makes the")
print("      reconstruction a reconstruction rather than a checkout.")
print()
onedisk = [p for p in G.corpus(G.PARENT_REV)]
print("      %-46s %6d" % ("files tracked at %s alone" % G.PARENT_REV,
                           len(onedisk)))
print("      %-46s %6d" % ("files in the reconstruction", len(recon_files)))
print("      %-46s %6d" % ("the difference: mg-03d1's own, untracked then",
                           len(recon_files) - len(onedisk)))
print("      ^ one unit of each is one file")
print()
print("  (3) IT CANNOT TELL YOU WHICH REGIME PRODUCED A FIGURE.  S1a's two")
print("      readings differ by the observer's own transcript; both of them")
print("      are readings of the SAME committed bytes, so a reconstruction")
print("      reproduces whichever one happens to be committed and cannot say")
print("      which it is.  1984 and 1966 reconstruct equally well.")

# ---------------------------------------------------------------------------
U.hdr("S3c  WHAT IT COSTS")

print("  (a) REACHABILITY.  A reconstruction is a promise about two commits")
print("      still being there.  Checked, not assumed:")
print()
for ref in (G.PARENT_REV, G.PARENT_PUB):
    try:
        U.git("rev-parse", "--verify", "%s^{commit}" % ref)
        exists = True
    except Exception:
        exists = False
    anc = False
    if exists:
        import subprocess
        anc = subprocess.run(["git", "merge-base", "--is-ancestor", ref,
                              "HEAD"], cwd=U.REPO).returncode == 0
    print("      %-12s exists: %-5s   an ancestor of HEAD: %-5s"
          % (ref, exists, anc))
    BAD += not exists
print()
print("      An ancestor is safe from garbage collection; a commit that is")
print("      merely present is not.  Both of mg-9160's are ancestors here,")
print("      and that is a fact about this branch and not a property of")
print("      reconstruction.")
print()
print("  (b) A HAND FACT PER FIGURE.  `PARENT_REV` and `PARENT_PUB` are two")
print("      constants a human worked out and typed into `lib9160.py`.  There")
print("      is no rule that recovers them: `the disk at the moment of the")
print("      run` is not recorded anywhere, and c9160 recovered it by reading")
print("      the transcripts and reasoning about what must have been")
print("      untracked.  So reconstruction is an ARCHIVAL ACT, once per")
print("      figure, by hand -- not an instrument you can point at the arc.")
print()
print("  (c) IT ANSWERS A DIFFERENT QUESTION, and the price is silent.  A")
print("      reconstruction of `what was committed at X` is a fine number and")
print("      it is not the number a probe globbing the disk computed.  Swap")
print("      one for the other without saying so and the figure stops being")
print("      about the thing its label says.")

# ---------------------------------------------------------------------------
U.hdr("S3d  SO: RECONSTRUCTION IS THE ANSWER FOR THE RECORD, NOT FOR THE RUN")

print("  For anything this arc PUBLISHES, reconstruction is the fix and its")
print("  cost is (a) and (b) above: two refs, worked out once, written down.")
print("  It buys a figure that is true forever instead of true for one commit")
print("  -- S2d measures that shelf life at 0 commits for mg-03d1's pair and 1")
print("  of 245 for mg-9160's.")
print()
print("  For what a PROBE RANGED OVER, reconstruction is not available, and")
print("  pretending otherwise is worse than the disk glob because it looks")
print("  reproducible.  What is available there is the thing S1b computes: the")
print("  figure PLUS the observer's own weight, which bounds the whole")
print("  disagreement between the two write regimes.")
print()
w = U.weight_of(U.file_stats(), lambda p: p.startswith(U.TREE + "/"))
print("  Worked on this tree's own figures, which is the only honest place to")
print("  try it first:")
print()
print("      %-46s %6d" % ("this tree's own rows, at this moment", w["rows"]))
print("      %-46s %6d" % ("the corpus row count on this disk", disk["rows"]))
print("      %-46s %s" % ("so my own arc-wide row figure is honestly",
                          U.render_figure(disk["rows"], "OBSERVED",
                                          low=disk["rows"] - w["rows"],
                                          ref=U.head())))
print()
U.note("S3", "RECONSTRUCTION FIXES THE RECORD AND CANNOT FIX THE RUN.  It is "
       "a function of two commit hashes, so it is stable by construction and "
       "not by luck -- and for the same reason it is blind to the untracked "
       "transcripts that are the entire output of the run being measured.  "
       "The published form therefore needs BOTH: a ref for the value and an "
       "observer's weight for the interval.")

print()
print("S3 TOTAL BAD: %d" % BAD)
sys.exit(min(BAD, 120))
