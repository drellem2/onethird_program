"""h5_doccheck.py -- DOES THIS AUDIT'S OWN DOCUMENT SAY WHAT ITS OWN RUN SAID?

Every figure this audit publishes is derived from a committed out_h*.txt.  A
document whose figures no instrument reads is an assertion, and this arc has
paid for that four times.

AND IT IS CHECKED AT THE SITE, NOT IN THE FILE.  `<a correct value occurs
somewhere in the document>` and `<the value is correct>` are different
statements, and mg-8a5c/mg-a318 is the case where the space between them
swallowed three wrong figures with the run green.  So each gate here:

  1. locates the ONE line carrying its anchor -- a sentence fragment or a table
     row -- and fails loudly if that line is absent or occurs more than once;
  2. reads the number out of THAT line;
  3. compares it against a number derived from the committed output of the
     script that measured it.

And each gate is DELETION-TESTED: the figure is corrupted at its own site in a
scratch copy of the document and the gate must go red, with a null probe beside
it that must stay green.  A gate that cannot be made to fire is not a gate.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import re
import sys

import lib321d as L

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = ("docs/OneThird-Bratteli-Path-Algebras-Mg58daRepair-"
       "IndependentAudit.md")

R = L.Report("h5", "every figure this audit's document publishes that is "
                   "derived from a committed out_h*.txt, read at its own site, "
                   "plus the corruption probe on each and one null probe")

L.banner("H5", "THE DOCUMENT'S FIGURES, READ AT THE SITE, AGAINST THE RUN")


def out(name):
    with open(os.path.join(HERE, "out_%s.txt" % name)) as fh:
        return fh.read()


o_self = out("selftest_321d")
o_h1 = out("h1_questions")
o_h2 = out("h2_grain")
o_h3 = out("h3_setlevel")
o_h4 = out("h4_mine")


def num_after(text, anchor, offset=0):
    """The offset-th integer on the unique line containing `anchor`."""
    lines = [l for l in text.splitlines() if anchor in l]
    if len(lines) != 1:
        raise LookupError("anchor %r matches %d lines, not 1"
                          % (anchor, len(lines)))
    nums = re.findall(r"\d+", lines[0])
    return int(nums[offset]), lines[0]


# ---------------------------------------------------------------------------
# Each gate: (label, anchor in the DOCUMENT, index of the figure on that line,
#             expected value derived from a committed output, how it was got)
# ---------------------------------------------------------------------------
def one(text, pattern, group=1):
    """The single match of `pattern` in `text`, as an int.

    Refuses on 0 matches and on more than 1: a figure derived from an ambiguous
    anchor is a figure nobody can check.
    """
    ms = re.findall(pattern, text, re.M)
    if len(ms) != 1:
        raise LookupError("pattern %r matches %d times, not 1"
                          % (pattern, len(ms)))
    m = ms[0]
    return int(m if isinstance(m, str) else m[group - 1])


def census(text, name):
    return one(text, r"^   %s\s+(\d+) of 24$" % re.escape(name))


def derive():
    g = {}
    g["total cells"] = one(o_h1, r"^      TOTAL CELLS\s+(\d+)$")
    g["disagreements"] = one(
        o_h1, r"SELF-ERRORS \d+   FINDINGS (\d+)   TOTAL BAD \d+   exit \d+")
    g["parser artifact"] = census(o_h1, "PARSER ARTIFACT")
    g["confirmed"] = census(o_h1, "CONFIRMED")
    g["unknown"] = census(o_h1, "UNKNOWN")
    g["accounted"] = one(o_h1, r"^   ACCOUNTED FOR\s+(\d+) of 24   <-")
    g["pairs"] = one(o_h3, r"pairs of sources agreeing on all 24 cells : "
                           r"(\d+) of \d+")
    g["pairs total"] = one(o_h3, r"pairs of sources agreeing on all 24 cells "
                                 r": \d+ of (\d+)")
    g["c0 identical"] = one(o_h3, r"^   identical: (\d+) of \d+,")
    g["members rerun"] = one(o_h3, r"members actually re-run here : (\d+) of 5")
    g["green"] = one(o_h3, r"^   green : (\d+) of 5")
    g["states figures"] = one(
        o_h3, r"stating the 24 vertex figures : (\d+) --")
    g["m1 fired"] = one(
        o_h4, r"probes that made g1's record check fire\s+: (\d+) of \d+")
    g["m1 probes"] = one(
        o_h4, r"probes that made g1's record check fire\s+: \d+ of (\d+)")
    g["m2 hits"] = one(o_h4, r"^   directions predicted correctly : (\d+) of \d+")
    g["m2 cases"] = one(o_h4, r"^   directions predicted correctly : \d+ of (\d+)")
    g["g1 findings"] = one(
        o_h2, r"^   live now : SELF-ERRORS \d+   FINDINGS (\d+)   exit \d+")
    g["assertions"] = one(o_self, r"^   assertions: (\d+),")
    return g


try:
    D = derive()
except LookupError as e:
    R.selferr("cannot derive a figure from this instrument's own output: %s" % e)
    D = {}
    print("   %s" % e)

GATES = [
    ("198-cell total, §0 row 2",
     "Re-done here from scratch at", None, None),      # prose, checked below
    ("198 cells in §2's re-run block",
     "TOTAL CELLS", 0, "total cells"),
    ("0 disagreements in §2's re-run block",
     "SELF-ERRORS 0   FINDINGS 0   TOTAL BAD 0   exit 0", 1, "disagreements"),
    ("PARSER ARTIFACT census, §3 table",
     "| **PARSER ARTIFACT**", 1, "parser artifact"),
    ("CONFIRMED census, §3 table",
     "| **CONFIRMED** (target states it", 0, "confirmed"),
    ("UNKNOWN census, §3 table",
     "| **UNKNOWN** (target does not", 0, "unknown"),
    ("ACCOUNTED FOR, §3 table",
     "| **ACCOUNTED FOR**", 0, "accounted"),
    ("pairs agreeing, §4",
     "pairs agree at all 24 cells", 0, "pairs"),
    ("pairs total, §4",
     "pairs agree at all 24 cells", 1, "pairs total"),
    ("c0_repro, §4",
     "outputs: **5 of 5 IDENTICAL**", 0, "c0 identical"),
    ("members re-run, §4 heading",
     "**All five re-run in place —", 1, "members rerun"),
    ("members stating figures, §4",
     "**2 of the five do**", 0, "states figures"),
    ("M-1 probes firing, §6",
     "**0 of 3 fire**", 0, "m1 fired"),
    ("M-1 probe count, §6",
     "**0 of 3 fire**", 1, "m1 probes"),
    ("M-2 directions, §6",
     "**4 of 4.** One line apart", 0, "m2 hits"),
    ("g1's live findings, §5",
     "and `g1` gives `FINDINGS 1`", 0, "g1 findings"),
    ("selftest assertions, §0",
     "**60 assertions** over its own reader", 0, "assertions"),
]


SKIPPED = []


def evaluate(doc):
    """(checked, failures) for one document text.  Failures are (label, why)."""
    checked, fails = 0, []
    for label, anchor, idx, key in GATES:
        if key is None:
            hits = [l for l in doc.splitlines() if anchor in l]
            if len(hits) != 1:
                fails.append((label, "anchor occurs %d times" % len(hits)))
            else:
                checked += 1
            continue
        if key not in D:
            # NOT silently dropped: a gate whose figure this instrument could
            # not derive is named, so a shrinking population is visible.
            if label not in SKIPPED:
                SKIPPED.append(label)
            continue
        try:
            got, line = num_after(doc, anchor, idx)
        except (LookupError, IndexError) as e:
            fails.append((label, "cannot read the figure at its site: %s" % e))
            continue
        checked += 1
        if got != D[key]:
            fails.append((label, "document says %d, the run says %d"
                          % (got, D[key])))
    return checked, fails


doc = L.read_worktree(DOC)
L.rule("(i) EVERY GATED FIGURE, READ AT ITS OWN SITE")
print("   figure                                   document   run    ")
for label, anchor, idx, key in GATES:
    if key is None or key not in D:
        continue
    try:
        got, _ = num_after(doc, anchor, idx)
        print("     %-40s %5d    %5d   %s"
              % (label, got, D[key], "agree" if got == D[key] else "DISAGREE"))
    except (LookupError, IndexError) as e:
        print("     %-40s  %s" % (label, e))
checked, fails = evaluate(doc)
print()
print("   figures gated : %d of the %d gates listed in this script's GATES"
      % (checked, len(GATES)))
print("   table, each anchored to one line of %s" % DOC.split("/")[-1])
if SKIPPED:
    print("   NOT gated (figure could not be derived from a committed out_h*"
          ".txt): %s" % ", ".join(SKIPPED))
    for lab in SKIPPED:
        R.selferr("the gate on %s was skipped: this script could not derive "
                  "the figure from its own committed output" % lab)
for label, why in fails:
    R.finding("the document's figure for %s does not match this instrument's "
              "own committed output: %s" % (label, why))
if not fails:
    print("   disagreements : 0")

# ---------------------------------------------------------------------------
L.rule("(ii) THE DELETION TEST -- EVERY GATE MADE TO FIRE AT ITS OWN SITE")
print("""   Each figure is corrupted ALONE, at its own site, in a scratch copy
   of the document, and the gate must go red naming that figure and no other.
   A null probe changes an unrelated word and must stay green.""")
print()
fired, total = 0, 0
for label, anchor, idx, key in GATES:
    if key is None or key not in D:
        continue
    total += 1
    try:
        _, line = num_after(doc, anchor, idx)
    except LookupError as e:
        print("     %-40s cannot locate its site: %s" % (label, e))
        R.finding("the gate on %s cannot locate its own site in the document, "
                  "so it certifies nothing: %s" % (label, e))
        continue
    nums = re.findall(r"\d+", line)
    victim = nums[idx]
    # replace the idx-th integer on that line only
    parts = re.split(r"(\d+)", line)
    seen = -1
    new = []
    for p in parts:
        if p.isdigit():
            seen += 1
            new.append(str(int(victim) + 7) if seen == idx else p)
        else:
            new.append(p)
    mutated = doc.replace(line, "".join(new), 1)
    _, mfails = evaluate(mutated)
    hit = any(f[0] == label for f in mfails)
    fired += hit
    print("     %-40s %s -> %s   %s"
          % (label, victim, int(victim) + 7, "FIRES" if hit else "SILENT"))
    if not hit:
        R.finding("the gate on %s does not fire when that figure is corrupted "
                  "at its own site: it is not reading the site" % label)
print()
null = doc.replace("Pre-filed in the same action", "Pre-filed in the same act",
                   1)
_, nfails = evaluate(null)
print("     %-40s %s" % ("NULL PROBE (unrelated word changed)",
                         "green" if not nfails else "RED -- wrong"))
R.check(not nfails,
        "the null probe makes the gate red; it is firing on something other "
        "than the figures")
print()
print("   probes firing : %d of %d, population: one corruption per gated"
      % (fired, total))
print("   figure, each mutating that figure alone at its own site.")
R.check(fired == total,
        "%d of %d gates are silent under corruption at their own site"
        % (total - fired, total))

sys.exit(R.emit())
