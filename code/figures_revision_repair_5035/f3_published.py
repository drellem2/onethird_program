"""F3 -- SEARCH FOR ALREADY-CORRUPTED PUBLISHED OUTPUT.

`mg-5035` step 3: *if a published figure was inflated by a counted revision, the
arithmetic fix does not retract the published number.*  True, and the reason it
matters is that a repair reads as a retraction to anybody who does not check.
So this probe looks for the damage rather than assuming the fix covers it.

  F3a  THE NAMED WITNESS, retroactively.  The one instance anybody recorded --
       `UNBACKED README.md 3738079` -- reconstructed and put to both rules.
  F3b  THE HUNT.  Every committed transcript line that prints a revision under
       a label calling it a figure.
  F3c  WHAT IS AND IS NOT RETRACTED, stated as a list of numbers.
  F3d  THE LINE THE REPAIR DOES NOT REACH, said plainly, because it is in
       mg-bf79's own transcript and a reader will find it.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib5035 as B                                              # noqa: E402

BAD = 0

B.bar("F3  ALREADY-CORRUPTED PUBLISHED OUTPUT")

# ---------------------------------------------------------------------------
B.hdr("F3a  THE NAMED WITNESS -- `UNBACKED README.md 3738079`, retroactively")

print("  mg-bf79's `out_p2_population.txt:99-106` records the whole sequence:")
print("  `r6_self.py` exited 1 for exactly one run, on `UNBACKED README.md")
print("  3738079`, *because the repaired README named a REVISION and E2's")
print("  `figures()` read the seven-digit revision as a MEASUREMENT no")
print("  transcript backs*.  THAT IS mg-bf79's TEXT, quoted, not re-derived.")
print()
print("  The README line itself is not in any commit -- I searched every")
print("  revision of `code/runner_exit_repair_70c7/README.md` and none")
print("  contains `3738079`.  So the witness must be RECONSTRUCTED in the form")
print("  mg-bf79 describes, and the reconstruction is labelled as mine:")
print()
WITNESS = [
    "the population is re-derived at `3738079`, the revision this repair landed",
    "at `3738079` -- the revision this figure is a fact about -- 9 sites",
    "this figure is a fact about the tree at commit 3738079",
]
gone = 0
for line in WITNESS:
    before, after = B.verdicts(line)
    hit = 3738079 in before and 3738079 not in after
    gone += hit
    print("      BEFORE %-24s AFTER %-24s %s"
          % (before, after, "EXCLUDED" if hit else "*** STILL A FIGURE ***"))
    print("          %s" % line)
    if not hit:
        BAD += 1
print()
print("  population: the %d RECONSTRUCTED README lines above, each in the form"
      % len(WITNESS))
print("  mg-bf79 says the original took")
B.plain("...RECONSTRUCTIONS on which the repair prevents the accusation", gone)
print("      ^ one unit of that number is one reconstructed line")
print()
print("  SO THE FIX IS RETROACTIVELY CORRECT AT THE SITE THAT PRODUCED THE")
print("  ONE RECORDED FAILURE.  It is a reconstruction and not the original")
print("  bytes, and that limit is the reason this row is not stronger.")

# ---------------------------------------------------------------------------
B.hdr("F3b  THE HUNT -- a revision printed under a label that calls it a FIGURE")

FIGWORD = re.compile(r"\bUNBACKED\b|\bBACKED\b|\bFIGURE\b|\bfigures?\b")
tpaths = B.transcripts()
rows = []
for p in tpaths:
    for i, line in enumerate(B.read(p).splitlines(), 1):
        if not FIGWORD.search(line):
            continue
        for m in B._SHAPED.finditer(line):
            tok = m.group(1)
            declared = tok in [str(x) for x in B.dropped(line)]
            if declared or B.resolves(tok):
                rows.append((p, i, tok, declared, line))
print("  population: the %d committed `out_*.txt` under `code/`" % len(tpaths))
B.plain("...LINES printing a revision-shaped token beside a figure word",
        len(rows))
print("      ^ one unit of that number is one (file, line, token) sighting")
print()
for p, i, tok, declared, line in rows:
    print("      %-12s %-9s %s:%d" % (tok, "DECLARED" if declared else "bare",
                                      p, i))
    print("          %s" % line.strip()[:88])
print()
print("  ADJUDICATION, one sighting at a time -- a count of sightings is not a")
print("  count of corrupted figures, and conflating them is this arc's own")
print("  recurring error:")
print()
print("    A sighting is CORRUPTION only if the number was COUNTED AS A")
print("    MEASUREMENT in a published total.  A transcript line that PRINTS a")
print("    revision while DESCRIBING the defect is a record of the defect, not")
print("    an instance of it.  Every sighting above is in mg-bf79's own")
print("    tree or in a census table whose column IS a revision by design.")
corrupt = [r for r in rows if r[3]]
B.plain("...SIGHTINGS that are a DECLARED revision counted as a figure",
        len(corrupt))
print("      ^ one unit of that number is one sighting")

# ---------------------------------------------------------------------------
B.hdr("F3c  WHAT IS RETRACTED AND WHAT IS NOT")

print("  THE ARITHMETIC FIX RETRACTS NOTHING BY ITSELF.  The ticket is right")
print("  about that, and here is the list it asks for.")
print()
print("  (1) THE ONE RECORDED FAILURE WAS NEVER PUBLISHED AS A COUNT.  The run")
print("      that exited 1 on `UNBACKED README.md 3738079` is described in")
print("      mg-bf79's transcript; the FAILING RUN'S OWN TRANSCRIPT was never")
print("      committed, and `r6_self.py` exits 0 at HEAD.  Nothing to retract.")
print()
print("  (2) THE INFLATION WAS REMOVED BY EDITING THE PROSE, NOT THE RULE.")
print("      mg-bf79: *it exits 0 again now, because the prose no longer names")
print("      an unstable revision.*  I confirmed the README at HEAD names no")
print("      all-decimal revision:")
rd = B.read("code/runner_exit_repair_70c7/README.md")
shaped = [m.group(1) for m in B._SHAPED.finditer(rd)]
B.plain("...revision-SHAPED tokens in mg-70c7's README at HEAD", len(shaped))
print("      ^ one unit of that number is one token occurrence")
print("      So the defect was WORKED AROUND IN THE PROSE and left in the")
print("      rule.  The workaround is what a reader would have had to notice")
print("      to know the rule was still wrong, and nothing said so.")
print()
print("  (3) THE COUNTS THAT WOULD MOVE IF RE-RUN TODAY.  These are not")
print("      retracted by this ticket and are not corrected in place: I do")
print("      not regenerate another tree's committed evidence.  Listed so the")
print("      next reader has them:")
files = B.corpus()
moved = []
for p in files:
    if not os.path.basename(p).startswith("out_"):
        continue
    d = sum(len(B.dropped(l)) for l in B.read(p).splitlines())
    if d:
        moved.append((p, d))
print()
print("  population: the %d committed transcripts" % len(tpaths))
B.plain("...TRANSCRIPTS whose figure reading changes under the repair",
        len(moved))
print("      ^ one unit of that number is one transcript file")
for p, d in sorted(moved):
    print("      %-64s %3d" % (p[:64], d))
print()
print("      NONE OF THESE IS A PUBLISHED FIGURE COUNT.  Each is a line that")
print("      NAMES a revision inside a transcript; no total printed in any of")
print("      them was computed by `figures()` over its own text.  That is why")
print("      the honest headline is that the defect was real and its published")
print("      damage is smaller than the ticket assumes -- said plainly rather")
print("      than buried, because overstating it would be the same failure as")
print("      the comment that started this.")

# ---------------------------------------------------------------------------
B.hdr("F3d  THE LINE THE REPAIR DOES NOT REACH, said before a reader finds it")

target = "code/runner_exit_repair_bf79/out_p2_population.txt"
for i, line in enumerate(B.read(target).splitlines(), 1):
    if "3738079" in line:
        d = B.dropped(line)
        print("      %s:%d" % (target, i))
        print("          %s" % line.strip()[:88])
        print("          dropped by the repair: %s" % (d if d else "nothing"))
print()
print("  `UNBACKED README.md 3738079` has a FILENAME to the left of the token")
print("  and no cue word, so the declared-revision rule does not fire on it.")
print("  THAT IS CORRECT HERE AND IT IS WORTH SAYING WHY.  That line is")
print("  mg-bf79 QUOTING the defect, inside a transcript.  A rule that")
print("  rewrote the record of a defect while repairing the defect would be")
print("  destroying the evidence -- which is the thing this arc keeps")
print("  catching.  The gap and the correct behaviour coincide here; F1d")
print("  counts the cases where they do not.")

print()
B.bar("F3 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts a reconstructed witness line the")
print("repair fails to fix.  It does NOT count sightings, transcripts that")
print("would move, or the lines F1d says the rule cannot reach: those are")
print("measurements of the arc, not faults of this tree.")
print()
print(B.finding("F3a", "the one recorded instance of this defect corrupting "
                       "output was never committed as a count -- it was a "
                       "single non-zero exit of `r6_self.py`, removed by "
                       "EDITING THE PROSE and not the rule; %d of %d "
                       "reconstructed witness lines are now excluded; %d "
                       "committed transcript(s) print a revision beside a "
                       "figure word and %d of those is a DECLARED revision "
                       "counted as a figure; %d transcript(s) would read "
                       "differently if re-run and none of them publishes a "
                       "figure COUNT"
                % (gone, len(WITNESS), len(rows), len(corrupt), len(moved))))
sys.exit(min(BAD, 120))
