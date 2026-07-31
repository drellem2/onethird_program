"""T4 -- DO NOT DISTURB, AND PRESERVE THE DISCLOSURES.

An audit that lands a finding by quietly removing the record of an earlier one
has not landed anything.  So before any finding of mine is worth reading, the
things this repair was told to leave alone are re-run and the things it
disclosed about itself are checked for still being there.

  T4a  mg-dee4's tree, BYTE-UNCHANGED, and its two disclosures verbatim: the
       A5 reach-from-stdout defect that scored `0 of 5` on a perfect run and
       would have read the forced-failure check as a PASS for the wrong
       reason, and the kept P4 prediction miss.
  T4b  mg-70c7's OWN kept misses and its five recorded instrument defects.
  T4c  The population table at `bee07a1`, re-derived: P0 72, P1 23/53,
       P2 errexit 19/26, P2 either 20/27, shape 19/42, name 17/34.
  T4d  The property population at `1ee1f1b^` -- exactly the four repaired
       files -- and 0 at HEAD, with the comparison anchor read out of the
       source to check it is still FIXED and not moving.
  T4e  The 8 discarded `git diff` executions, run, at the execution grain.

A REMOVED DISCLOSURE IS A REGRESSION AND IS COUNTED AS ONE.  These checks
raise BAD, not FINDINGS: a disturbed fixture is a defect of the tree under
audit's landing, not an observation about its reasoning.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib56dc as M

sys.path.insert(0, os.path.join(M.REPO, M.S7522))
import lib7522 as L                                            # noqa: E402

BAD = 0
FINDINGS = []

M.bar("T4  DO NOT DISTURB -- THE DISCLOSURES AND THE FIGURES")

# ---------------------------------------------------------------------------
M.hdr("T4a  mg-dee4's TREE AND ITS TWO DISCLOSURES")

diff = M.git("diff", "--name-only", "%s..HEAD" % M.DEE4_REV, "--", M.DEE4)
changed = [l for l in diff.splitlines() if l.strip()]
print("      files of %s changed since %s   %3d"
      % (M.DEE4, M.DEE4_REV, len(changed)))
for f in changed:
    print("          *** %s" % f)
if changed:
    BAD += len(changed)

DISCLOSURES = [
    ("the A5 reach-from-stdout defect",
     ["A defect in this instrument, recorded rather than smoothed away",
      "target script's **name in the runner's stdout**",
      "0 of 5",
      "would have read *\"0 later\nsteps ran\"* as a PASS for the same wrong reason"]),
    ("the kept P4 prediction miss",
     ["P4 — I predicted a hole in the corrected population and there is none",
      "Measured: **0**"]),
    ("the second kept miss, the moving 263 -> 275 figure",
     ["That is **F2 reproduced inside the audit of F2**"]),
]
dee4_out = M.read("%s/OUTCOMES.md" % M.DEE4, None)
print()
for label, needles in DISCLOSURES:
    have = [n for n in needles if n.replace("\n", " ") in
            " ".join(dee4_out.split())
            or n in dee4_out]
    ok = len(have) == len(needles)
    print("      %-48s %d of %d phrase(s) present  %s"
          % (label, len(have), len(needles), "OK" if ok else "*** MISSING ***"))
    for n in needles:
        if n not in have:
            print("          *** absent: %s" % n[:60])
    if not ok:
        BAD += 1
print()
print("  AND THE SAME QUESTION PUT TO THE PUBLISHED SIDE, because a")
print("  disclosure that survives in a transcript and vanishes from the")
print("  document is a disclosure a reader will not meet:")
print()
for rel in (M.SUBJECT_DOC, "%s/README.md" % M.SUBJECT,
            "%s/OUTCOMES.md" % M.SUBJECT):
    text = M.read(rel, None)
    n = len(re.findall(r"recorded rather than smoothed away|"
                       r"kept as written|MISS", text))
    print("      %-52s %2d disclosure phrase(s)"
          % (os.path.basename(rel), n))

# ---------------------------------------------------------------------------
M.hdr("T4b  mg-70c7's OWN KEPT MISSES AND RECORDED DEFECTS")

oc = M.read("%s/OUTCOMES.md" % M.SUBJECT, None)
misses = [l.strip() for l in oc.splitlines() if re.search(r"\*\*MISS", l)]
print("      rows in OUTCOMES.md scored MISS                   %3d" % len(misses))
for l in misses:
    m = re.match(r"\|\s*\*\*(\w+)\*\*", l)
    print("          %-6s %s" % (m.group(1) if m else "?", l[:64]))
if len(misses) != 4:
    BAD += 1
    print("      *** expected the 4 kept misses R4b, R6c, R6d, R6e ***")
print()
defects = re.search(r"Five defects in this instrument", oc)
numbered = re.findall(r"^\*\*(\d)\.", oc, re.M)
print("      the heading says `Five defects in this instrument`  %s"
      % ("yes" if defects else "*** NO ***"))
print("      numbered defect paragraphs under it                %3d"
      % len(numbered))
if not defects or len(numbered) != 5:
    BAD += 1
    print("      *** the recorded instrument defects are not five ***")
print()
doc = M.read(M.SUBJECT_DOC, None)
print("      the published document names the same five         %s"
      % ("yes" if "Five defects in this instrument are recorded" in doc
         else "*** NO ***"))
print("      ...and the two prediction misses                   %s"
      % ("yes" if "Two predictions missed and are kept" in doc
         else "*** NO ***"))
if "Five defects in this instrument are recorded" not in doc or \
        "Two predictions missed and are kept" not in doc:
    BAD += 1

# ---------------------------------------------------------------------------
M.hdr("T4c  THE POPULATION TABLE AT %s, RE-DERIVED" % M.PINNED)

print("  The predicate is `lib7522`'s, used AT ITS SOURCE and not copied: the")
print("  question here is whether the PUBLISHED FIGURE still holds under the")
print("  rule that produced it.  Whether that rule is the right one is T3's")
print("  question and it is asked with fixtures written from scratch.")
print()


def census(ref):
    sh = L.ls_sh(ref)
    srcs = L.sources(sh, ref)
    p1f = p1p = 0
    err_f, err_p, val_f, val_p, either_f, either_p = 0, 0, 0, 0, 0, 0
    shape_f = shape_p = name_f = name_p = 0
    for f, src in srcs.items():
        pipes = L.pipelines(src)
        if pipes:
            p1f += 1
            p1p += len(pipes)
        tees = L.tee_pipelines(src)
        if tees:
            shape_f += 1
            shape_p += len(tees)
            if os.path.basename(f) == "run_all.sh":
                name_f += 1
                name_p += len(tees)
        e = v = 0
        for i, line in pipes:
            ok, arm, _w = L.consumed(src, line, i)
            if not ok:
                continue
            if not any(L.stage_can_fail(f, st, ref)[0]
                       for st in L.discarded_stages(line)):
                continue
            if "ERREXIT" in arm:
                e += 1
            if "VALUE" in arm:
                v += 1
        err_f += 1 if e else 0
        err_p += e
        val_f += 1 if v else 0
        val_p += v
        if e or v:
            either_f += 1
            either_p += max(e, v) if (e and v) else (e + v)
    return dict(p0=len(sh), p0_named=sum(1 for p in sh
                                         if os.path.basename(p) == "run_all.sh"),
                p1=(p1f, p1p), err=(err_f, err_p), val=(val_f, val_p),
                either=(either_f, either_p), shape=(shape_f, shape_p),
                name=(name_f, name_p))


c = census(M.PINNED)
EXPECT = [("P0  tracked `*.sh`, any depth, no name rule", c["p0"], 72),
          ("    ...of which named `run_all.sh`", c["p0_named"], 64),
          ("P1  files / pipelines", c["p1"], (23, 53)),
          ("P2  ERREXIT arm, files / pipelines", c["err"], (19, 26)),
          ("P2  EITHER arm, files / pipelines", c["either"], (20, 27)),
          ("    shape rule -- a real `| tee`", c["shape"], (19, 42)),
          ("    name rule -- `| tee` in a `run_all.sh`", c["name"], (17, 34))]
print("      %-46s %-12s %-12s %s" % ("row", "published", "re-derived", ""))
for label, got, want in EXPECT:
    ok = got == want
    if not ok:
        BAD += 1
    print("      %-46s %-12s %-12s %s"
          % (label, str(want), str(got), "AGREES" if ok else "*** DIFFERS ***"))
print()
print("      rows of the published population table re-derived   %d of %d"
      % (sum(1 for _l, g, w in EXPECT if g == w), len(EXPECT)))

# ---------------------------------------------------------------------------
M.hdr("T4d  THE PROPERTY POPULATION AT %s, AND 0 AT HEAD" % M.PRE)

pre = census(M.PRE)
head = census(None)
FOUR = sorted(["code/face_geometry_audit_f1b2/run_audit.sh",
               "code/face_geometry_audit_fcf1/run_audit.sh",
               "code/state_delegation_audit_16eb/run_all.sh",
               "code/state_delegation_repair_0049/run_all.sh"])
err_members, either_members = [], []
for f, src in L.sources(L.ls_sh(M.PRE), M.PRE).items():
    for i, line in L.pipelines(src):
        ok, arm, _w = L.consumed(src, line, i)
        if not ok or not any(L.stage_can_fail(f, st, M.PRE)[0]
                             for st in L.discarded_stages(line)):
            continue
        either_members.append(f)
        if "ERREXIT" in arm:
            err_members.append(f)
print("  mg-dee4's C3 says the property population at %s is EXACTLY the four"
      % M.PRE)
print("  files mg-7522 repaired.  That claim is under the ERREXIT clause, so")
print("  it is checked under the ERREXIT clause; the widened clause is")
print("  reported beside it rather than substituted for it.")
print()
err_set, either_set = sorted(set(err_members)), sorted(set(either_members))
print("      the ERREXIT population at %s          %2d file(s)"
      % (M.PRE, len(err_set)))
for f in err_set:
    print("          %-56s %s" % (f, "as published" if f in FOUR else "*** EXTRA"))
for f in [x for x in FOUR if x not in err_set]:
    print("          *** MISSING %s" % f)
if err_set != FOUR:
    BAD += 1
    print("      *** the four published members are not the errexit population ***")
print()
print("      the WIDENED population at the same ref     %2d file(s)"
      % len(either_set))
for f in either_set:
    print("          %-56s %s"
          % (f, "" if f in FOUR else "the member the VALUE arm adds (F6)"))
print()
print("      the ERREXIT arm at HEAD                   %d file(s), %d pipeline(s)"
      % head["err"])
print("      the WIDENED population at HEAD            %d file(s), %d pipeline(s)"
      % head["either"])
if head["err"] != (0, 0):
    BAD += 1
    print("      *** the errexit arm at HEAD is not 0 ***")
print()
s4 = M.read("%s/s4_unpin.py" % M.S7522, None)
lib = M.read("%s/lib7522.py" % M.S7522, None)
pinned_lit = re.search(r'^PINNED\s*=\s*"([0-9a-f]{7,40})"', lib, re.M)
pinned_call = re.findall(r"changed_since\(L\.PINNED\)", s4)
head_call = re.findall(r"changed_since\(None\)", s4)
exhibit = "0 BY CONSTRUCTION" in s4
print("      `lib7522.PINNED` is a literal revision     %s"
      % (pinned_lit.group(1) if pinned_lit else "*** NOT A LITERAL ***"))
print("      the COMPARISON, anchored to it            %d call(s)"
      % len(pinned_call))
print("      a HEAD-anchored call beside it            %d call(s)"
      % len(head_call))
print("      ...labelled as the EXHIBITION, not the comparison   %s"
      % ("yes -- the source says `0 BY CONSTRUCTION`" if exhibit
         else "*** NO ***"))
if not pinned_lit or not pinned_call:
    BAD += 1
    print("      *** the comparison is not against a fixed ref ***")
elif head_call and not exhibit:
    BAD += 1
    print("      *** a HEAD-anchored call with nothing saying why ***")
else:
    print("      The comparison is still against a fixed pre-repair ref, and")
    print("      the moving one is the 2x2's own exhibit of why it must not be.")

# ---------------------------------------------------------------------------
M.hdr("T4e  THE 8 EXECUTIONS, RUN -- at the execution grain")

RUNNERS = ("code/state_delegation_audit_16eb/run_all.sh",
           "code/state_delegation_repair_0049/run_all.sh")
runs, nonzero = [], 0
for rel in RUNNERS:
    src = M.read(rel, M.PRE)
    loops = M.for_loops(src)
    for line, it, bind, text in M.pipeline_executions(src, "git diff"):
        if bind is None:
            BAD += 1
            print("      *** %s:%d iteration not derivable" % (rel, line))
            continue
        lp = [l for l in loops if l[2] <= line <= l[3]]
        full = L.loop_bindings(src, lp[0][2], lp[0][3], bind) if lp else bind
        argv = L.argv_of(text.split("|")[0], full)
        if argv is None:
            BAD += 1
            print("      *** %s:%d argv not derivable" % (rel, line))
            continue
        code, _out = M.run_argv(argv, M.REPO, timeout=300)
        if code != 0:
            nonzero += 1
        runs.append((rel, line, it, argv, code))
print("  %-46s %-38s %s" % ("execution", "discarded stage", "exit"))
for rel, line, it, argv, code in runs:
    print("  %-46s %-38s %s"
          % (rel.replace("code/", "") + ":%d#%d" % (line, it),
             " ".join(argv[1:])[:38], "-" if code is None else code))
print()
print("      EXECUTIONS run here                       %3d" % len(runs))
print("      ...exiting 0                              %3d" % (len(runs) - nonzero))
print("      SOURCE LINES those executions come from   %3d"
      % len({(r, l) for r, l, _i, _a, _c in runs}))
if nonzero:
    BAD += nonzero
    print("      *** %d exit non-zero ***" % nonzero)

print()
M.bar("T4 TOTAL FINDINGS: %d   TOTAL BAD: %d" % (len(FINDINGS), BAD))
print()
for f in FINDINGS:
    print(f)
if not FINDINGS and not BAD:
    print("(nothing disturbed: mg-dee4's tree is byte-unchanged, both of its")
    print(" disclosures and all four of mg-70c7's kept misses are present, the")
    print(" seven published population rows re-derive, the property population")
    print(" is the four repaired files at %s and the errexit arm is 0 at" % M.PRE)
    print(" HEAD, the comparison anchor is fixed, and 8 of 8 executions exit 0)")
print()
print("EXTENT OF THOSE NUMBERS.  TOTAL BAD counts a changed file in mg-dee4's")
print("tree, a disclosure phrase that is gone, a kept miss that is no longer")
print("scored MISS, a published population row that does not re-derive, a")
print("property-population member that is not one of the four, a non-zero")
print("errexit arm at HEAD, a moving comparison anchor, and a non-zero")
print("discarded status among the 8.  It ranges over mg-dee4's tree, mg-70c7's")
print("OUTCOMES and document, every tracked `*.sh` at %s / %s / HEAD, and the"
      % (M.PINNED, M.PRE))
print("8 executions of 3 source lines.  It does NOT re-measure mg-c2b3's 34.")
sys.exit(min(len(FINDINGS) + BAD, 120))
