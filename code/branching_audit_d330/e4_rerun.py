"""E4 --- THE THING NO LIST NAMES: WHAT THE REPAIR DID TO THE AUDIT THAT
        COMMISSIONED IT.

mg-d330.  My brief says its list is a FLOOR and requires me to audit one thing
no list names and to say what I chose.

WHAT I CHOSE.  mg-13b2 edited `code/branching_audit_a218/c2_vertexsets.py` ---
a script belonging to the audit whose findings it repairs --- and said why:

    "mg-a218's own c2_vertexsets.py is widened to accept either column form so
     that a RE-RUN tells the truth instead of scoring its own repair as a
     SELF-ERROR."

That is the right instinct and it is applied to exactly ONE of mg-a218's five
`c*.py` scripts.  mg-a218 has five, four of them read the same rewritten
target, and its document says --- in the present tense, under REPRODUCE ---
which of them exit 1.  Nothing in the tree checks any of that.  My brief names
the delivered document, the vertex column, the labels and the withdrawal; it
does not name the auditing instrument's own health, and an audit whose repair
silently breaks its auditor is the same defect one level up.

So: every one of mg-a218's scripts is re-run against the repaired tree, its
verdict compared with its committed output and with what mg-a218's document
says about it, and each change is classified.

Exit 0 iff SELF-ERRORS == 0 AND FINDINGS == 0.
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
A218 = os.path.join(ROOT, "code", "branching_audit_a218")
A218_DOC = os.path.join(
    ROOT, "docs", "OneThird-Bratteli-Path-Algebras-Mge8b8Repair-IndependentAudit.md")

SELF, FIND = [], []


def selferr(m):
    SELF.append(m)
    print("   SELF-ERROR: " + m)


def finding(m):
    FIND.append(m)
    print("   FINDING: " + m)


SCRIPTS = ["selftest_a218.py", "c1_branching.py", "c2_vertexsets.py",
           "c3_withdrawal.py", "c4_seam.py", "c5_record.py"]

print("=" * 74)
print("E4  mg-a218'S OWN INSTRUMENT, RE-RUN AGAINST THE REPAIRED TREE")
print("=" * 74)
print("Nothing is written into code/branching_audit_a218/.  Each script is run")
print("in place with its stdout captured here, which is exactly what its own")
print("run_all.sh does except that run_all.sh REDIRECTS INTO THE COMMITTED")
print("OUTPUTS and would overwrite the record.")
print()


def nums(txt):
    s = re.search(r"^SELF-ERRORS: (\d+)", txt, re.M)
    f = re.search(r"^FINDINGS: (\d+)", txt, re.M)
    b = re.search(r"^TOTAL BAD: (\d+)", txt, re.M)
    return (int(s.group(1)) if s else None,
            int(f.group(1)) if f else None,
            int(b.group(1)) if b else None)


results = {}
print("   %-22s %-26s %-26s" % ("script", "committed output", "live now"))
print("   %-22s %-26s %-26s" % ("", "self/find/bad  exit", "self/find/bad  exit"))
for sc in SCRIPTS:
    outp = os.path.join(A218, "out_" + sc[:-3] + ".txt")
    try:
        committed = open(outp, encoding="utf-8").read()
    except OSError as exc:
        selferr("no committed output for %s: %s" % (sc, exc))
        continue
    p = subprocess.run([sys.executable, "-u", sc], cwd=A218,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    live = p.stdout.decode("utf-8", "replace")
    cs, cf, cb = nums(committed)
    ls, lf, lb = nums(live)
    results[sc] = (cs, cf, cb, ls, lf, lb, p.returncode, live)
    print("   %-22s %-2s/%-2s/%-2s  (exit %s)        %-2s/%-2s/%-2s  (exit %d)"
          % (sc, cs, cf, cb, "0" if (cb == 0) else "1", ls, lf, lb, p.returncode))
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("(i) WHICH VERDICTS MOVED, AND WHY")
print("-" * 74)
CLASSES = {
    "c2_vertexsets.py": ("REPAIRED AND WIDENED",
                         "mg-13b2 closed the finding AND widened the parser; "
                         "the only one of the five it touched"),
    "c4_seam.py": ("REPAIRED",
                   "the unmarked in-place edit at t1_tl.py:368 now carries a "
                   "marker, so the seam sweep has nothing to report"),
    "c5_record.py": ("REPAIRED",
                     "section 8's disposition list now agrees with the diff"),
}
moved = []
for sc in SCRIPTS:
    if sc not in results:
        continue
    cs, cf, cb, ls, lf, lb, rc, live = results[sc]
    if (cs, cf) == (ls, lf):
        continue
    moved.append(sc)
    kind, why = CLASSES.get(sc, ("UNCLASSIFIED", ""))
    print("   %s" % sc)
    print("      committed  SELF %s FINDINGS %s" % (cs, cf))
    print("      live       SELF %s FINDINGS %s" % (ls, lf))
    if sc in CLASSES:
        print("      [%s] %s" % (kind, why))
    else:
        print("      [NOT CLASSIFIED BY THE REPAIR] --- examined below")
print("   scripts whose verdict moved: %d of %d" % (len(moved), len(SCRIPTS)))
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("(ii) c1_branching.py --- THE ONE THAT WAS NOT WIDENED")
print("-" * 74)
if "c1_branching.py" in results:
    cs, cf, cb, ls, lf, lb, rc, live = results["c1_branching.py"]
    print("   c1 is mg-a218's PRIMARY script.  It produced E1 --- 'the invariant")
    print("   reproduces in every cell: 24 vertex-count, 53 vertex-dimension and")
    print("   121 edge cells, 0 disagreements' --- which is the claim my brief")
    print("   tells me must not be weakened.")
    print()
    print("   committed: SELF %s  FINDINGS %s" % (cs, cf))
    print("   live now : SELF %s  FINDINGS %s" % (ls, lf))
    print()
    qmarks = re.findall(r"vertex COUNT disagrees at beta=(\d) n=(\d): target \?",
                        live)
    dimfind = re.findall(r"dim L\(\d+,\d+\) at beta=\d disagrees", live)
    edgefind = re.findall(r"edge .*disagrees", live)
    print("   of the live FINDINGS:")
    print("     vertex-COUNT cells reading 'target ?'   : %d of 24" % len(qmarks))
    print("     vertex-DIMENSION cells disagreeing      : %d of 53" % len(dimfind))
    print("     EDGE cells disagreeing                  : %d of 121" % len(edgefind))
    print()
    print("   MECHANISM, read out of the source rather than guessed.  c1 parses")
    print("   the target's committed T1b2 block for a count table --- a line of")
    print("   a beta followed by six integers:")
    src = open(os.path.join(A218, "c1_branching.py"), encoding="utf-8").read()
    for l in src.splitlines():
        if "(?:\\d+\\s+){5}" in l or "tgt_counts = {}" in l:
            print("        %s" % l.strip())
    o1 = open(os.path.join(ROOT, "code", "branching_locate_db09",
                           "out_t1_tl.txt"), encoding="utf-8").read()
    seg = o1.split("T1b2  THE BRANCHING GRAPH AS VERSHIK-OKOUNKOV DEFINE IT")[1]
    seg = seg.split("T1c  SEMISIMPLICITY")[0]
    hits = [l for l in seg.splitlines()
            if re.match(r"\s*(\d)\s+((?:\d+\s+){5}\d+)\s*$", l)]
    print("   lines in the CURRENT out_t1_tl.txt that this parser matches: %d"
          % len(hits))
    print("   -- mg-13b2 removed the count table from T1b2 (i) on purpose: it")
    print("      is mg-a218's OWN finding X1 that the count was the defect. The")
    print("      parser that read it was not widened with c2's.")
    print()
    if len(qmarks) == 24 and not dimfind and not edgefind:
        print("   WHAT IS AND IS NOT WEAKENED, stated precisely:")
        print("     * 174 of the 198 cells --- 53 dimension and 121 edge --- still")
        print("       compare and still agree, 0 disagreements.")
        print("     * The 24 vertex-COUNT cells no longer compare against")
        print("       anything.  c1 books all 24 as FINDINGS against the target,")
        print("       printing 'target ?'.")
        print("     * The mathematics is untouched: c1's OWN measurement of the")
        print("       vertex sets, dimensions and the five multiplicity-2 edges")
        print("       is unchanged, and E1's numbers are reproduced afresh by")
        print("       this audit's e1 on a fourth instrument.")
        finding("mg-13b2 widened one of mg-a218's five scripts and not the "
                "sibling with the same stale parser: re-run on the repaired "
                "tree, c1_branching.py --- the script that produced mg-a218's "
                "E1 --- reports 24 FINDINGS against the target, all of them "
                "'target ?', because the count table its parser reads is the "
                "very thing mg-13b2 deleted. They are booked as FINDINGS and "
                "not as SELF-ERRORS, so the instrument accuses the target of "
                "disagreeing where its own parser went blind. 174 of the 198 "
                "cells still compare and still agree; 24 have gone dark and "
                "are reported as red.")
    else:
        print("   the failure is not the pure parser shape predicted; examine.")
        finding("c1_branching.py reports %s findings on the repaired tree with "
                "%d count-cells reading 'target ?', %d dimension and %d edge "
                "disagreements" % (lf, len(qmarks), len(dimfind), len(edgefind)))
    print()
    print("   AND c1's OWN POPULATION LINE IS NOW WRONG:")
    for l in live.splitlines():
        if "vertex counts:" in l and "cells compared" in l:
            print("     %s" % l.strip())
    print("     -- 0 were compared. 24 were compared against nothing.")
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("(iii) c3_withdrawal.py --- THE OTHER ONE THAT MOVED THE WRONG WAY")
print("-" * 74)
if "c3_withdrawal.py" in results:
    cs, cf, cb, ls, lf, lb, rc, live = results["c3_withdrawal.py"]
    print("   c3 is the mg-73df-shaped check: it sweeps 16 files for the")
    print("   withdrawn phrases and requires every occurrence to sit inside a")
    print("   withdrawal or correction.  mg-a218 reported 8 occurrences, all")
    print("   marked.  Live now:")
    for l in live.splitlines():
        if l.strip().startswith("FINDING:"):
            for part in l.split(";"):
                print("     %s" % part.strip()[:100])
    if lf:
        finding("c3_withdrawal.py --- the check that exists because a repair "
                "once fixed the prose while the instrument still asserted the "
                "error --- goes RED on the repaired tree, and all of its "
                "unmarked occurrences are inside mg-13b2's OWN new "
                "t5_labels.py and its committed output, where the withdrawn "
                "phrases sit as search needles with no marker beside them")
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("(iv) WHAT mg-a218'S DOCUMENT SAYS ABOUT ITS OWN EXIT CODES")
print("-" * 74)
adoc = open(A218_DOC, encoding="utf-8").read()
CLAIM = "`c2`, `c4` and `c5` exit `1`"
print("   its section 10, REPRODUCE, present tense:")
for (i, l) in enumerate(adoc.splitlines(), 1):
    if "exit `1`" in l or "Exit codes are the finding channel" in l:
        print("     %d: %s" % (i, l.strip()))
live_ones = [sc for sc in SCRIPTS
             if sc in results and results[sc][6] != 0]
print()
print("   states that these exit 1 : c2, c4, c5")
print("   actually exit 1 now      : %s"
      % ", ".join(s[:2] for s in live_ones) or "(none)")
if CLAIM in adoc:
    stated = {"c2", "c4", "c5"}
    actual = {s[:2] for s in live_ones}
    if stated != actual:
        finding("mg-a218's audit document says, in the present tense under "
                "REPRODUCE, that %s; on the repaired tree the scripts that "
                "exit 1 are %s. mg-13b2 edited that instrument and left the "
                "sentence describing it unchanged and unmarked --- the same "
                "label-versus-diff defect, one document over."
                % (CLAIM.replace("`", ""), ", ".join(sorted(actual)) or "none"))
else:
    selferr("could not locate mg-a218's exit-code sentence to check it")
print()
print("   NOT A FINDING, recorded: mg-a218's committed out_c2_vertexsets.txt is")
print("   deliberately NOT regenerated, and mg-13b2 says so and gives the")
print("   precedent (mg-a318 for mg-8a5c). A committed audit output is a record")
print("   of what was found, not a live gate. That call is right and is not")
print("   scored here. What is scored is the SENTENCE, which is present-tense")
print("   instructions to a reader who will run the code and get another answer.")
print()

print("-" * 74)
print("SELF-ERRORS: %d, population: the %d scripts re-run and the document read"
      % (len(SELF), len(SCRIPTS)))
print("FINDINGS: %d, population: the %d scripts of mg-a218's instrument and "
      "the exit-code sentence in its document" % (len(FIND), len(SCRIPTS)))
for f in FIND:
    print("   FINDING: " + f)
print("TOTAL BAD: %d" % (len(SELF) + len(FIND)))
sys.exit(1 if (SELF or FIND) else 0)
