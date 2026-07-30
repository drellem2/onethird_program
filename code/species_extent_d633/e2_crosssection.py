"""E2 -- A STRUCK CLAIM MUST NOT STAND UN-STRUCK ELSEWHERE IN THE SAME
DOCUMENT.

mg-7dd3's B1.  `docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md` §4
struck the Aguiar-Mahajan §17.5 quotation -- "mg-7d75 printed it wrong", "the
book's species is Pi* in both slots" -- and §0 asserted it, live, unmarked, as
a direct quotation with a section citation, 310 lines above.  Both had been in
the file since `83ac472`.  Four passes went over it.  EVERY CHECKER WAS GREEN
AND EVERY EXTENT LINE WAS TRUE: the file is read, the statement is on the one
list, `S1 TOTAL BAD` is 0.

  * `check_doc.py` requires the STRICKEN string to occur only inside a strike.
    It does.  The stored string begins "Recall from Section 17.4 that" and
    §0's copy began differently.
  * `stricken_a4ef.py`'s X7 row is anchored on the same lead-in.
  * A LIST OF SENTENCES IS NOT A LIST OF CLAIMS, and no per-section checker can
    see this by construction -- which is why all of them were green.

THE RULE, AND IT IS NOT A LIST.  For every `~~struck~~` span, the longest run
of consecutive tokens it shares with the SAME DOCUMENT outside every strike.
A run of at least RUN_MIN tokens that is at least RUN_FRAC of the strike is
the claim itself said again.  Nothing here knows what any particular claim IS,
so it does not go stale when a new one is struck: a worker who strikes a
sentence writes the `~~`, and that is the whole input.

EXONERATION, and it is narrower than this arc's other three on purpose.  The
occurrence stands only if THE PARAGRAPH CARRYING IT SAYS THE CLAIM DOES NOT
HOLD, or if it sits in a fenced block quoting a checker's own table of
stricken strings.  A ticket id nearby is NOT enough: `kerna4ef.py` exonerates
on `mg-[0-9a-f]{4}` within six lines, and the paragraph five lines below §0's
misquotation contains an unrelated `mg-6f61` -- so that rule exonerates the one
occurrence in this repository that has to fire.  E2c measures exactly that
rather than asserting it.

    python3 code/species_extent_d633/e2_crosssection.py
"""

import os
import re
import sys

from kernd633 import (hdr, REPO, RUN_MIN, RUN_FRAC, md_files, strike_findings,
                      NEGATES, toks)

bad = 0
ROOTS = [os.path.join(REPO, "docs"), os.path.join(REPO, "code")]

FILES = []
for r in ROOTS:
    FILES += md_files(r)
FILES = sorted(set(FILES))


# ---------------------------------------------------------------------------
# E2a  the sweep
# ---------------------------------------------------------------------------
hdr("E2a  EVERY STRIKE AGAINST ITS OWN DOCUMENT")

print("  Rule: a run of >= %d shared tokens that is >= %.0f%% of the strike is"
      % (RUN_MIN, 100 * RUN_FRAC))
print("  the CLAIM said again, not a shared lead-in.  Every strike is listed")
print("  with its measurement whether it fires or not, so the margins are")
print("  visible instead of a verdict.")
print()

nstrikes = 0
withstrikes = 0
rows = []
for rel in FILES:
    text = open(os.path.join(REPO, rel), encoding="utf-8").read()
    found = strike_findings(text)
    if not found:
        continue
    withstrikes += 1
    nstrikes += len(found)
    fires = [f for f in found if f[4] is False]
    exon = [f for f in found if f[4] is True]
    quiet = [f for f in found if f[4] is None]
    print("  %-58s %2d strike(s)" % (rel, len(found)))
    print("      %2d below the rule, %2d exonerated, %2d STANDING"
          % (len(quiet), len(exon), len(fires)))
    for sl, rl, run, tot, ex, why in sorted(found, key=lambda f: -f[2] / max(1, f[3])):
        mark = ("*** STANDING UN-STRUCK ***" if ex is False else
                ("exonerated: " + why if ex else "below the rule"))
        print("        strike line %-5s run %3d of %3d (%3.0f%%)  "
              "restated at line %-5s  %s"
              % (sl, run, tot, 100 * run / max(1, tot),
                 rl if rl is not None else "-", mark))
        rows.append((rel, sl, rl, run, tot, ex))
    bad += len(fires)
    print()

print("  %d file(s) carry a strike, %d strike(s) measured, %d standing."
      % (withstrikes, nstrikes, bad))
print()


# ---------------------------------------------------------------------------
# E2b  CONTROLS -- the detector is shown to fire
# ---------------------------------------------------------------------------
hdr("E2b  CONTROLS -- a detector only ever seen to pass is worth nothing")

ctl = 0
DOC = os.path.join(REPO, "docs",
                   "OneThird-Species-Hopf-Monoids-Where-This-Lives.md")
doc = open(DOC, encoding="utf-8").read()

# (a) B1 itself, restored.  This is the state of the file from 83ac472 to
#     mg-d633: §0's paragraph carrying the sentence §4 strikes.
B1 = ('Aguiar–Mahajan §17.5, quoting their own §17.4: '
      '*"`K̄(Π)` is the algebra of\nsymmetric functions in '
      'noncommuting variables and `K(Π)` is the familiar Hopf algebra '
      'of\nsymmetric functions."*')
# The repair is REVERSED, not spliced next to.  Two earlier versions of this
# control were themselves the defect, and both are kept in OUTCOMES.md:
#   1. it truncated the document at §0's paragraph, which removed §4's strike
#      along with everything after it -- so the restored file had nothing to
#      compare and the control read "0 findings, expected 1".  A control that
#      deletes the strike it is testing for reports the detector as broken.
#   2. it inserted B1 INTO the corrected paragraph, whose own words say the
#      quotation is a misquotation -- so the occurrence was exonerated, and
#      correctly.  Restoring a false belief beside its correction does not
#      restore the false belief.
CORRECTION = re.compile(r"(?s)Aguiar–Mahajan §17\.5, quoting their own "
                        r"§17\.4, records both values.*?"
                        r"rest of its own document\.\n")
if not CORRECTION.search(doc):
    print("  *** §0's corrected paragraph is not where this control expects")
    print("      it: the control cannot run, and this line is the record ***")
restored = CORRECTION.sub(lambda _m: B1 + "\n", doc, count=1)
hits = [f for f in strike_findings(restored) if f[4] is False]
ok = len(hits) == 1
ctl += (not ok)
print("  (a) B1 restored -- §0 carries the sentence §4 strikes      %s"
      % ("fires, 1 finding -- ok" if ok
         else "*** %d finding(s), expected 1 ***" % len(hits)))
for sl, rl, run, tot, _e, _w in hits:
    print("        strike line %d restated at line %d, run %d of %d"
          % (sl, rl, run, tot))

# (b) the same sentence, in a paragraph that RETRACTS it, must not fire.
retracted = restored.replace(B1, "This is a misquotation and is struck at "
                             "§4: " + B1)
hits_b = [f for f in strike_findings(retracted) if f[4] is False]
ok = not hits_b
ctl += (not ok)
print("  (b) the same sentence in a paragraph that RETRACTS it       %s"
      % ("silent -- ok" if ok else "*** FIRES, %d ***" % len(hits_b)))

# (c) THE NARROWING, MEASURED.  mg-a4ef's exoneration rule -- a ticket id
#     within six lines -- applied to (a) must NOT fire, which is why this file
#     does not use it.  If this control ever goes quiet, the narrowing has
#     stopped being load-bearing and can be dropped.
NAMES_A_REPAIR = re.compile(r"mg-(?:6f61|f8fa|a61f|73df|a4ef)", re.I)
WINDOW = 6                      # kerna4ef.WINDOW, copied rather than imported
lines = restored.splitlines()
# The line control (a) actually reported, not a line found by re-searching for
# a fragment: an earlier version of this control looked for "is the algebra of"
# and matched AM §10.10's "`A/J` is the algebra of flats" 78 lines earlier, and
# reported the ±6-line rule as NOT disarmed.  Kept in OUTCOMES.md.
target = (hits[0][1] - 1) if hits else None
window = ("\n".join(lines[max(0, target - WINDOW):target + WINDOW + 1])
          if target is not None else "")
m = NAMES_A_REPAIR.search(window)
disarmed = bool(m)
ctl += (not disarmed)
print("  (c) mg-a4ef's ±%d-line ticket-id rule, applied to (a)        %s"
      % (WINDOW, "DISARMED -- ok, the narrowing is load-bearing" if disarmed
         else "*** not disarmed: this file's narrowing may be unnecessary ***"))
if disarmed:
    off = window[:m.start()].count("\n")
    print("        `%s` sits %d line(s) from the restatement, and is about an"
          % (m.group(0), abs(off - min(target, WINDOW))))
    print("        UNRELATED correction.  That is why exoneration here needs")
    print("        the paragraph to SAY the claim does not hold.")

# (d) an unrelated long quotation must not fire: the run test must be measuring
#     repetition of a STRUCK claim, not length.
noise = doc + "\n\n" + " ".join(toks(doc)[:400]) + "\n"
hits_d = [f for f in strike_findings(noise) if f[4] is False]
ok = not hits_d
ctl += (not ok)
print("  (d) 400 tokens of this document appended, no new strike     %s"
      % ("silent -- ok" if ok else "*** FIRES, %d ***" % len(hits_d)))

# (e) the rule must not fire on a document with no strikes at all.
ok = not strike_findings("# a document\n\nwith no strikes in it at all.\n")
ctl += (not ok)
print("  (e) a document with no strike                               %s"
      % ("silent -- ok" if ok else "*** FIRES ***"))
bad += ctl
print()


print("=" * 78)
print("E2 TOTAL BAD: %d" % bad)
print("=" * 78)
print()
print("EXTENT OF THIS NUMBER.  %d markdown file(s) -- every *.md under docs/"
      % len(FILES))
print("and under code/, recursively.  %d of them carry at least one strike and"
      % withstrikes)
print("%d strike(s) were measured; a file with no `~~` contributes nothing and"
      % nstrikes)
print("is not evidence of anything.  IT READS NO .py, NO .txt AND NO CODE: a")
print("claim struck in a document and asserted in a code tree is s1_extent.py's")
print("extent, not this one, and that division is the whole of mg-73df's MAJOR")
print("said once more.  WITHIN a document it compares a strike ONLY against")
print("that document -- a claim struck here and asserted in ANOTHER file is")
print("invisible to every checker in this repository, and that is the next")
print("hole, named rather than closed.  And it matches VERBATIM RUNS: a claim")
print("restated in different words, at any length, is invisible to it.")
sys.exit(1 if bad else 0)
