"""k4_doccheck.py -- DOES THIS REPAIR'S DOCUMENT SAY WHAT ITS OWN RUN SAID?

Every figure the document publishes is derived from a committed out_k*.txt.  A
document whose figures no instrument reads is an assertion, and this arc has
paid for that more than once.

AND IT IS CHECKED AT THE SITE, NOT IN THE FILE.  "a correct value occurs
somewhere in the document" and "the value is correct" are different statements,
and mg-8a5c/mg-a318 is the case where the space between them swallowed three
wrong figures with the run green.  So each gate here:

  1. locates the ONE line carrying its anchor, and fails loudly if that line is
     absent or occurs more than once;
  2. reads the number out of THAT line;
  3. compares it against a number derived from the committed output of the
     script that measured it.

Each gate is then DELETION-TESTED: the figure is corrupted at its own site in a
scratch copy of the document and the gate must go red, with a null probe beside
it that must stay green.  A gate that cannot be made to fire is not a gate.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import re
import sys

import lib7e58 as L

DOC = "docs/OneThird-Bratteli-Path-Algebras-Mg7e58ProvenanceRepair.md"

R = L.Report("k4", "every figure this repair's document publishes that is "
                   "derived from a committed out_k*.txt, read at its own site, "
                   "plus one corruption probe per gate and one null probe")

L.banner("K4", "THE DOCUMENT'S FIGURES, READ AT THE SITE, AGAINST THE RUN")


def out(name):
    with open(os.path.join(L.HERE, "out_%s.txt" % name)) as fh:
        return fh.read()


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


def derive():
    o_k1 = out("k1_grain")
    o_k2 = out("k2_selfprov")
    o_k3 = out("k3_setlevel")
    o_self = out("selftest_7e58")
    g = {}
    g["g1 probes"] = one(
        o_k1, r"probes whose direction was predicted correctly : (\d+) of \d+")
    g["g1 probe total"] = one(
        o_k1, r"probes whose direction was predicted correctly : \d+ of (\d+)")
    g["meas lines"] = one(
        o_k2, r"c1's measuring half, as printed : (\d+) lines")
    g["cells compared"] = one(o_k2, r"cells c1 compares in \(iii\)\s+: (\d+)")
    g["frozen"] = one(o_k2, r"population: the (\d+) committed records above")
    g["pairs"] = one(o_k3, r"pairs of sources agreeing on all 24 cells : "
                           r"(\d+) of \d+")
    g["pairs total"] = one(o_k3, r"pairs of sources agreeing on all 24 cells "
                                 r": \d+ of (\d+)")
    g["cell comparisons"] = one(o_k3, r"^   cells compared in total : (\d+)$")
    g["rerun"] = one(o_k3, r"members actually re-run here : (\d+) of 5")
    g["green"] = one(o_k3, r"^   green : (\d+) of 5")
    g["locality"] = one(o_k3, r"probes moving exactly their own cell : "
                              r"(\d+) of \d+")
    g["c0"] = one(o_k3, r"^     identical: (\d+) of \d+,")
    g["assertions"] = one(o_self, r"^   assertions: (\d+),")
    return g


try:
    D = derive()
except LookupError as e:
    R.selferr("cannot derive a figure from this instrument's own output: %s" % e)
    D = {}
    print("   %s" % e)

# (label, anchor in the DOCUMENT, index of the figure on that line, key)
GATES = [
    ("g1 deletion probes, §0",
     "**4 of 4** directions predicted correctly", 0, "g1 probes"),
    ("g1 probe count, §0",
     "**4 of 4** directions predicted correctly", 1, "g1 probe total"),
    # The index is the position of the figure among the integers ON ITS OWN
    # LINE, and these lines carry incidental digits -- a sha256 prefix, an
    # mg-id, a section number.  That is not a reason to move the figure
    # somewhere tidier: the whole point of this gate is that it reads the line
    # a reader reads.  The index is checked by the deletion test below, which
    # corrupts exactly this integer and requires the gate to fire.
    ("c1's measuring half, §0",
     "**125 lines**, on both forms", 4, "meas lines"),
    ("pairs agreeing, §0",
     "**The set-level property is intact and re-derived, not quoted.**",
     0, "pairs"),
    ("pairs total, §0",
     "**The set-level property is intact and re-derived, not quoted.**",
     1, "pairs total"),
    ("cell comparisons, §0",
     "over **240** cell comparisons", 2, "cell comparisons"),
    ("members re-run, §0",
     "**5 of 5** members re-run in place", 0, "rerun"),
    ("c0_repro, §0",
     "`c0_repro.sh` **5 of 5 IDENTICAL**", 0, "c0"),
    ("locality probes, §0",
     "**5 of 5** locality probes move their own cell", 0, "locality"),
    ("pairs agreeing, §3 table",
     "| pairs of sources agreeing at all 24 cells |", 1, "pairs"),
    ("pairs total, §3 table",
     "| pairs of sources agreeing at all 24 cells |", 2, "pairs total"),
    ("cell comparisons, §3 table",
     "| cells compared, over those pairs |", 0, "cell comparisons"),
    ("members re-run, §3 table",
     "| `mg-a218`'s members re-run in place |", 1, "rerun"),
    ("members green, §3 table",
     "| members green |", 0, "green"),
    ("c0_repro, §3 table",
     "| `c0_repro.sh` committed outputs identical |", 1, "c0"),
    ("locality probes, §3 table",
     "| readers moving at their own cell and no other |", 0, "locality"),
    ("frozen records, §4 B9",
     "**7 of 7 IDENTICAL**", 4, "frozen"),
    ("selftest assertions, §5",
     "a **65-assertion** self-test", 2, "assertions"),
    ("cells compared by c1, §4 B2",
     "moves none of the 198 cells either", 4, "cells compared"),
]

SKIPPED = []


def num_after(text, anchor, offset=0):
    """The offset-th integer on the unique line containing `anchor`."""
    lines = [l for l in text.splitlines() if anchor in l]
    if len(lines) != 1:
        raise LookupError("anchor %r matches %d lines, not 1"
                          % (anchor, len(lines)))
    nums = re.findall(r"\d+", lines[0])
    return int(nums[offset]), lines[0]


def evaluate(doc):
    checked, fails = 0, []
    for label, anchor, idx, key in GATES:
        if key not in D:
            if label not in SKIPPED:
                SKIPPED.append(label)
            continue
        try:
            got, _ = num_after(doc, anchor, idx)
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
print("   figure                                   document   run")
for label, anchor, idx, key in GATES:
    if key not in D:
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
    print("   NOT gated (figure could not be derived from a committed out_k*"
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
   of the document, and the gate must go red naming that figure.  A null probe
   changes an unrelated word and must stay green.""")
print()
fired, total = 0, 0
for label, anchor, idx, key in GATES:
    if key not in D:
        continue
    total += 1
    try:
        _, line = num_after(doc, anchor, idx)
    except LookupError as e:
        print("     %-40s cannot locate its site: %s" % (label, e))
        R.finding("the gate on %s cannot locate its own site, so it certifies "
                  "nothing: %s" % (label, e))
        continue
    nums = re.findall(r"\d+", line)
    victim = nums[idx]
    parts = re.split(r"(\d+)", line)
    seen, new = -1, []
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
null = doc.replace("a stated reason is checkable", "a stated reason is checkabl",
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
