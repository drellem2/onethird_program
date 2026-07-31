"""S1 -- THE POPULATION, DEFINED BY A PROPERTY INSTEAD OF BY A FILENAME.

mg-c2b3 scoped its sweep as *"63 `run_all.sh`, 23 containing `| tee`"*.  Two
things in that sentence are not properties of the defect:

  * `run_all.sh` is a NAMING CONVENTION.  Two runners in the arc are called
    `run_audit.sh`, are `#!/bin/sh`, set `set -e`, and carried eight `| tee`
    pipelines between them.  They were unrepaired at HEAD after the sweep
    reported the arc clean.
  * `| tee` is a SHAPE.  The property is `a pipeline whose exit status is
    consumed and whose discarded stage can fail`.  `| tee` is one shape of it;
    `git diff ... | wc -c | tr -d ' '` under `set -e` is another, and three of
    those are in the arc in files that ARE named `run_all.sh` -- so the shape
    rule missed them even where the name rule did not.

So this probe defines the population by a predicate over CONTENT and prints the
predicate next to every count.  Three nested populations:

  P0  every tracked `*.sh`                                   (no name rule)
  P1  ...containing a real pipeline on a command line        (parse, not grep)
  P2  ...whose status is CONSUMED and whose discarded
      stage CAN FAIL                                          (the defect)

and, beside them, the two name/shape-defined populations the sweep used, so the
difference is a measured row rather than an argument.

THE CLEARANCE.  mg-c2b3's 34-of-34 result cleared what it examined.  What it
examined was filename-defined, so the clearance is SOUND ABOUT ITS POPULATION
AND SILENT ABOUT THE REST.  S1 states the corrected population; S2 reads the
status of everything in it that the sweep did not read.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib7522 as L

BAD = 0

L.bar("S1  THE POPULATION -- BY PROPERTY, NOT BY NAME")


def classify(src_map, ref):
    """{path: [(line, text, c1, c3, why3)]} over every pipeline in every file."""
    out = {}
    for p, s in sorted(src_map.items()):
        rows = []
        se = L.has_set_e(s)
        for i, line in L.pipelines(s):
            c1 = se and not L.guarded(line)
            why3 = []
            c3 = False
            for st in L.discarded_stages(line):
                v, w = L.stage_can_fail(p, st, ref)
                why3.append(w)
                c3 = c3 or bool(v)
            rows.append((i, line, c1, c3, "; ".join(why3)))
        if rows:
            out[p] = rows
    return out


def census(ref, label):
    global BAD
    L.hdr("S1a  %s" % label)

    p0 = L.ls_sh(ref)
    src = L.sources(p0, ref)
    named = [p for p in p0 if os.path.basename(p) == "run_all.sh"]
    rows = classify(src, ref)

    p1 = {p: r for p, r in rows.items()}
    p2 = {p: [x for x in r if x[2] and x[3]] for p, r in rows.items()}
    p2 = {p: r for p, r in p2.items() if r}
    tee = {p: L.tee_pipelines(s) for p, s in src.items() if L.tee_pipelines(s)}

    def n(d):
        return len(d), sum(len(v) for v in d.values())

    print("  PREDICATE                                              files  pipelines")
    print("  P0  tracked `*.sh`, any depth, NO name rule            %5d          -"
          % len(p0))
    print("      ...of which named `run_all.sh` (the sweep's pop.)  %5d          -"
          % len(named))
    print("      ...of which NOT so named                           %5d          -"
          % (len(p0) - len(named)))
    print("  P1  ...containing a REAL pipeline on a command line    %5d      %5d"
          % n(p1))
    print("  P2  ...status CONSUMED and discarded stage CAN FAIL    %5d      %5d"
          % n(p2))
    print()
    print("  THE SWEEP'S TWO RULES, over the same files:")
    print("      shape rule  -- a real `| tee` pipeline             %5d      %5d"
          % n(tee))
    print("      name rule   -- a real `| tee` in a `run_all.sh`    %5d      %5d"
          % n({p: v for p, v in tee.items()
               if os.path.basename(p) == "run_all.sh"}))
    print()

    print("  P2 IN FULL -- every member, with the clause each line satisfies:")
    print()
    for p, r in sorted(p2.items()):
        print("    %s   [%s]" % (p, "run_all.sh" if os.path.basename(p) ==
                                 "run_all.sh" else "NOT named run_all.sh"))
        for i, line, _c1, _c3, why3 in r:
            print("        %4d  %s" % (i, line.strip()[:88]))
            print("              discards: %s" % why3[:88])
    print()

    print("  IN P1 BUT NOT IN P2 -- named, with WHICH clause fails, because")
    print("  a population that only lists its positives cannot be checked:")
    print()
    any_out = False
    for p, r in sorted(p1.items()):
        outs = [x for x in r if not (x[2] and x[3])]
        if not outs:
            continue
        any_out = True
        print("    %s" % p)
        for i, line, c1, c3, why3 in outs:
            fail = "C1 (status not consumed)" if not c1 else "C3 (%s)" % why3[:60]
            print("        %4d  %-56s  fails %s" % (i, line.strip()[:56], fail))
    if not any_out:
        print("    (none -- every pipeline in P1 is in P2)")
    print()
    return p0, p1, p2, tee


L.hdr("S1  what this probe measures, and the two rules it replaces")
print("  A population is defined by a PREDICATE OVER CONTENT.  Every count")
print("  below prints its predicate on the same line, so a reader can check")
print("  the rule and not only the number.  `run_all.sh` appears exactly")
print("  once, as the sweep's rule being measured -- never as this probe's.")

pin = census(L.PINNED, "AT THE SWEEP'S PINNED %s -- the world it repaired"
             % L.PINNED)
head = census(None, "AT HEAD, ON DISK -- the world as it stands")

# ---------------------------------------------------------------------------
L.hdr("S1b  WHAT THE NAME RULE COULD NOT CONTAIN, AND WHAT THE SHAPE RULE COULD NOT")

pin_p2, head_p2 = pin[2], head[2]
pin_tee = pin[3]

missed_by_name = sorted(p for p in pin_tee
                        if os.path.basename(p) != "run_all.sh")
print("  MISSED BY THE NAME RULE (a real `| tee`, not called run_all.sh),")
print("  at %s:" % L.PINNED)
for p in missed_by_name:
    print("      %-52s %d pipeline(s)" % (p, len(pin_tee[p])))
print("      -> %d file(s), %d pipeline(s)"
      % (len(missed_by_name), sum(len(pin_tee[p]) for p in missed_by_name)))
print()

missed_by_shape = sorted(p for p in pin_p2 if p not in pin_tee)
print("  MISSED BY THE SHAPE RULE (in P2, but no `| tee` on the line), at %s:"
      % L.PINNED)
for p in missed_by_shape:
    print("      %-52s %d line(s)" % (p, len(pin_p2[p])))
print("      -> %d file(s), %d pipeline(s)"
      % (len(missed_by_shape), sum(len(pin_p2[p]) for p in missed_by_shape)))
print()
print("  These two sets are DISJOINT and neither is empty.  A sweep keyed on")
print("  the name misses the first; a sweep keyed on the shape misses the")
print("  second; only the property covers both.")

# ---------------------------------------------------------------------------
L.hdr("S1c  THE STATE OF THE ARC AT HEAD, AFTER THIS REPAIR")

print("  P2 at HEAD is the list of pipelines still throwing away a status")
print("  something reads.  This repair's forward half is that it is EMPTY.")
print()
if head_p2:
    for p, r in sorted(head_p2.items()):
        print("    *** STILL SWALLOWING: %s -- %d line(s)" % (p, len(r)))
        for i, line, _c1, _c3, why3 in r:
            print("          %4d  %s" % (i, line.strip()[:80]))
    BAD += sum(len(r) for r in head_p2.values())
else:
    print("    P2 at HEAD is EMPTY -- 0 files, 0 pipelines.")
    print()
    print("    EXTENT OF THAT.  It ranges over every tracked `*.sh` in this")
    print("    repository at HEAD, at any depth, under the P2 predicate above.")
    print("    It does NOT range over pipelines built at run time by a Python")
    print("    caller, over `.sh` files that are untracked, or over any commit")
    print("    other than HEAD.  Those limits are stated because a stated")
    print("    limit is checkable and an omission is not.")

# ---------------------------------------------------------------------------
L.hdr("S1d  THE RETROACTIVE CLEARANCE, RESTATED OVER THE CORRECTED POPULATION")

pin_all = sorted(pin_p2)
swept = [p for p in pin_all if os.path.basename(p) == "run_all.sh"
         and p in pin_tee]
unswept = [p for p in pin_all if p not in swept]
print("  mg-c2b3 read the status of every `| tee` target in a `run_all.sh`:")
print("  34 of 34, all 0.  That result is SOUND ABOUT ITS POPULATION.  Over")
print("  the property-defined population it covers:")
print()
print("      P2 members inside the sweep's population   %2d file(s)" % len(swept))
print("      P2 members OUTSIDE it                      %2d file(s)" % len(unswept))
for p in unswept:
    print("          %-52s %d line(s)" % (p, len(pin_p2[p])))
print()
print("  The clearance is silent about the second group.  S2 reads their")
print("  exit status directly -- the way the 34 were read -- so that the")
print("  cleared population and the corrected population are the same set.")

print()
L.bar("S1 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts pipelines still in P2 at HEAD, and")
print("nothing else.  It does not count P1 members that fail a clause -- those")
print("are listed above with the clause each fails, which is a stronger record")
print("than a count.  It ranges over tracked `*.sh` at HEAD and at %s."
      % L.PINNED)
sys.exit(1 if BAD else 0)
