"""mg-ec63 / S5 -- THE POSITIVE CONTROL: THE ONE INSTANCE WITH A KNOWN ANSWER.

An instrument that reports "no damage anywhere" is indistinguishable from an
instrument that cannot see damage.  There is exactly one instance in this arc
whose answer is already on the record: mg-bf79 found that `run_all.sh`'s `>`
kept `p5_self.py` from seeing its own transcript, and that this HID NINE of its
own labels.

That tree now carries the structural fix, so it is OUTSIDE the population S2
sweeps -- which is precisely why it can be the control.  Its transcript is
populated when the probe reads it, so B is the committed state, and A has to be
reconstructed by emptying the file the way the OLD runner did.

IF THIS SECTION DOES NOT RECOVER NINE, THE INSTRUMENT IS WRONG AND THE RECORD
IS RIGHT, and this file says so in advance rather than adjusting afterwards.

Exit code = 0 if the control recovers the recorded number, 1 if it does not.
"""

import difflib
import os
import re
import sys

import lib_ec63 as B

TREE = "code/runner_exit_repair_bf79"
PROBE = "p5_self.py"
OUT = "out_p5_self.txt"
RECORDED = 9

print("mg-ec63 / S5 -- THE POSITIVE CONTROL (mg-bf79's NINE HIDDEN LABELS)")
print("HEAD: %s" % B.head())

B.hdr("S5a  THE TREE, AND WHY IT IS NOT IN THE SWEPT POPULATION")

steps, _ = B.parse_runner(TREE)
ops = sorted(set(o for _, _, o in steps))
print("  %s" % TREE)
print("  resolved steps: %d, operators: %s" % (len(steps), ", ".join(ops)))
print()
print("  Its runner writes `X.new` and `mv`s it, so nothing is empty when the")
print("  probe reads it.  That is the fix this ticket is NOT about applying.")
print("  Here the tree is used the other way round: as the one case where the")
print("  answer is on the record before I measure it.")

B.hdr("S5b  A AND B, AND THE DELTA")

a = B.run_probe(TREE, PROBE, OUT, empty_first=True, timeout=180)
b = B.run_probe(TREE, PROBE, OUT, empty_first=False, timeout=180)

al, bl = a["text"].splitlines(), b["text"].splitlines()
print("  A (own transcript emptied first, the OLD runner's behaviour)")
print("      exit %s, %d lines" % (a["exit"], len(al)))
print("  B (own transcript holding its committed bytes)")
print("      exit %s, %d lines" % (b["exit"], len(bl)))
print()

NUM = re.compile(r"(?<![\w.])(\d+)(?![\w.])")


def rowcounts(lines):
    """Every `N of M` and every leading count, keyed by the label it sits on."""
    out = {}
    for ln in lines:
        m = re.search(r"\.\.\.(.+?)\s{2,}(\d+)\s*$", ln)
        if m:
            out[m.group(1).strip()] = int(m.group(2))
    return out


ra, rb = rowcounts(al), rowcounts(bl)
moved = [(k, ra.get(k), rb.get(k)) for k in sorted(set(ra) | set(rb))
         if ra.get(k) != rb.get(k)]
print("  population: the labelled counts `p5_self.py` prints")
B.plain("...COUNTS printed under A", len(ra), "one labelled count")
B.plain("...COUNTS printed under B", len(rb), "one labelled count")
B.plain("...COUNTS that DIFFER between A and B", len(moved),
        "one labelled count")
print()
for k, x, y in moved:
    print("      %-52s  A=%-6s B=%-6s  delta %s"
          % (k[:52], x, y, (y - x) if (x is not None and y is not None)
             else "n/a"))

deltas = [y - x for _, x, y in moved if x is not None and y is not None]
print()
print("  THE RECORDED ANSWER IS %d HIDDEN LABELS." % RECORDED)
hit = RECORDED in deltas or RECORDED in [abs(d) for d in deltas]
print("      a delta of %d appears in the table above:  %s"
      % (RECORDED, "YES" if hit else "NO"))
print()
if hit:
    print("  The instrument recovers the number that was on the record before")
    print("  it ran.  Every SAME row in S3 is therefore a SAME row, and not a")
    print("  blind instrument reporting silence.")
else:
    print("  IT DOES NOT.  The record stands and this instrument is suspect.")
    print("  The deltas it did find are printed above rather than suppressed,")
    print("  and S6 carries this as a defect of THIS suite.")

B.hdr("S5c  THE DIFF ITSELF, SO THE NUMBER IS NOT TAKEN ON TRUST")

d = list(difflib.unified_diff(al, bl, "A(empty)", "B(populated)", n=1,
                              lineterm=""))
for x in d[:60]:
    print("      %s" % x[:150])
if len(d) > 60:
    print("      ... (%d further diff lines)" % (len(d) - 60))

B.save("control", {"recorded": RECORDED, "deltas": deltas, "hit": bool(hit),
                   "moved": moved})

print()
print("S5 CONTROL: %s" % ("RECOVERED" if hit else "NOT RECOVERED"))
sys.exit(0 if hit else 1)
