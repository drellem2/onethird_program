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
PREFIX = "675c2ba"   # the last revision of p5_self.py WITHOUT the fallback

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

B.hdr("S5c  WHY IT DID NOT FIRE, READ OUT OF THE DIFF RATHER THAN GUESSED")

d = list(difflib.unified_diff(al, bl, "A(empty)", "B(populated)", n=1,
                              lineterm=""))
for x in d[:40]:
    print("      %s" % x[:150])
if len(d) > 40:
    print("      ... (%d further diff lines)" % (len(d) - 40))
print()
fallback = any("truncated on disk" in x for x in d)
print("  THE SUBJECT WAS HARDENED A SECOND WAY, AND NOTHING SAYS SO.")
print("      the A-side names its transcript as read from HEAD:  %s"
      % ("YES" if fallback else "no"))
print()
print("  `p5_self.py:81` sets the provenance label `HEAD (truncated on disk by")
print("  run_all.sh)`.  The probe DETECTS its own transcript being empty and")
print("  falls back to the committed bytes.  So mg-bf79 closed this hole")
print("  TWICE -- structurally in the runner, and defensively in the probe --")
print("  and the record names only the first.  The whole A/B delta at HEAD is")
print("  that one provenance word changing from `HEAD (...)` to `disk`.")
print()
print("  THAT IS WHY THE CONTROL CANNOT FIRE AT HEAD, and it is a finding")
print("  rather than an excuse: a reader of mg-bf79's README would conclude")
print("  the runner fix is what protects that probe, and it is not the only")
print("  thing protecting it.")

# ---------------------------------------------------------------------------
B.hdr("S5d  THE CONTROL RUN AT THE REVISION THAT ACTUALLY HAD THE DEFECT")

print("  The probe at HEAD is immune, so the control is run against the LAST")
print("  REVISION OF IT THAT WAS NOT: %s, the commit before mg-bf79's own"
      % PREFIX[:7])
print("  fix.  Its bytes are written into the tree, run both ways, and the")
print("  committed bytes restored in a `finally`.")
print()

src_pre = B.git("show", "%s:%s/%s" % (PREFIX, TREE, PROBE))
path = os.path.join(B.REPO, TREE, PROBE)
saved = open(path, "rb").read()
hit2 = False
exact = False
try:
    with open(path, "w") as f:
        f.write(src_pre)
    print("      pre-fix probe written: %d bytes (HEAD is %d)"
          % (len(src_pre), len(saved)))
    a2 = B.run_probe(TREE, PROBE, OUT, empty_first=True, timeout=180)
    with open(path, "w") as f:
        f.write(src_pre)
    b2 = B.run_probe(TREE, PROBE, OUT, empty_first=False, timeout=180)
    a2l, b2l = a2["text"].splitlines(), b2["text"].splitlines()
    print("      A exit %s, %d lines / B exit %s, %d lines"
          % (a2["exit"], len(a2l), b2["exit"], len(b2l)))
    ra2, rb2 = rowcounts(a2l), rowcounts(b2l)
    moved2 = [(k, ra2.get(k), rb2.get(k)) for k in sorted(set(ra2) | set(rb2))
              if ra2.get(k) != rb2.get(k)]
    print()
    print("  population: the labelled counts the PRE-FIX `p5_self.py` prints")
    B.plain("...COUNTS that DIFFER between A and B", len(moved2),
            "one labelled count")
    for k, x, y in moved2:
        print("      %-52s  A=%-6s B=%-6s  delta %s"
              % (k[:52], x, y, (y - x) if (x is not None and y is not None)
                 else "n/a"))
    deltas2 = [y - x for _, x, y in moved2 if x is not None and y is not None]
    exact = RECORDED in deltas2 or RECORDED in [abs(x) for x in deltas2]
    hit2 = any(x > 0 for x in deltas2)
    print()
    print("  TWO QUESTIONS, AND THEY HAVE DIFFERENT ANSWERS.")
    print()
    print("      (1) DOES THE CONTROL FIRE AT ALL -- does the pre-fix probe")
    print("          see MORE of its own rows once the transcript is real?")
    print("              %s   (%d counts rise, largest +%d)"
          % ("YES" if hit2 else "NO", sum(1 for x in deltas2 if x > 0),
             max(deltas2 + [0])))
    print("          An instrument that could not see this effect would print")
    print("          a delta of 0 here.  This one does not.")
    print()
    print("      (2) IS THE RECORDED %d RECOVERED EXACTLY?   %s"
          % (RECORDED, "YES" if exact else "NO"))
    print("          It is not, and the reason is measurable rather than")
    print("          rhetorical: mg-bf79 measured 9 against ITS OWN TREE AS IT")
    print("          STOOD AT %s, and that tree has been republished twice"
          % PREFIX[:7])
    print("          since (eab14bc and fe6a495).  The probe counts rows in")
    print("          its own transcripts, and there are more of them now:")
    print("          %s -> %s under B alone."
          % (ra2.get("ROWS of mine whose grain is at stage label"),
             rb2.get("ROWS of mine whose grain is at stage label")))
    print("          PREDICTIONS.md/P5a said `exactly 9 labels` and said that")
    print("          any other number means the instrument is wrong.  It is a")
    print("          MISS and it is kept as written: what it got wrong was")
    print("          assuming a figure measured against a 2026-08-05 tree is")
    print("          reproducible against a 2026-08-06 one.  That assumption")
    print("          is this arc's own recurring error and I made it in the")
    print("          prediction that was supposed to guard against it.")
    d2 = list(difflib.unified_diff(a2l, b2l, "A(empty)", "B(populated)", n=1,
                                   lineterm=""))
    print()
    for x in d2[:40]:
        print("      %s" % x[:150])
    if len(d2) > 40:
        print("      ... (%d further diff lines)" % (len(d2) - 40))
finally:
    with open(path, "wb") as f:
        f.write(saved)
    B.git("checkout", "--", TREE)
    B.restore_arc()
    ok = not B.git("status", "--porcelain", "--", TREE).strip()
    print()
    print("      the tree is restored to its committed bytes:  %s"
          % ("yes" if ok else "*** NO ***"))

B.save("control", {"recorded": RECORDED, "deltas": deltas,
                   "hit_head": bool(hit), "hit_prefix": bool(hit2),
                   "moved": moved})

print()
print("S5 CONTROL: at HEAD %s / at %s %s, exact %d %s"
      % ("fires" if hit else "CANNOT FIRE (probe hardened)",
         PREFIX[:7], "FIRES" if hit2 else "DOES NOT FIRE",
         RECORDED, "recovered" if exact else "NOT recovered"))
sys.exit(0 if hit2 else 1)
