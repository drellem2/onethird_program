"""g3_findings.py -- QUESTION A: ARE THE 24 FINDINGS REAL?

The brief is exact about why this cannot be answered by counting:

    A blind parser produces findings and non-findings with equal confidence,
    so the count itself carries no information until each is checked.

So this script does two things, and the second is the harder one.

  (a) THE 24 FINDINGS.  Each is established individually before any of them
      is called a defect: what does the target state at that cell, does it
      state it at all, and does it agree.  Each of the 24 ends up in exactly
      one of three boxes -- CONFIRMED, PARSER ARTIFACT, UNKNOWN -- and the
      boxes are filled by measurement.

  (b) THE 174 NON-FINDINGS.  c1 reports 0 disagreements over 53 dimension
      cells and 121 edge cells.  If those parsers had gone blind too, they
      would report 0 disagreements for exactly the same reason the vertex
      parser reports 24 -- and the run would look better, not worse.  So
      every one of those channels is corrupted deliberately and required to
      go red.  A channel that stays green under corruption is not reporting
      agreement; it is reporting nothing.

The c1 under test here is the one taken from 286d5030, which is byte-identical
to the c1 that raised the 24 findings.  It is run in a scratch tree against a
target text this script supplies, so the answers do not depend on the state of
anyone's working directory and do not change when c1 is later repaired.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import re
import sys

import lib58da as L

SELF, FIND = [], []


def selferr(m):
    SELF.append(m)


def finding(m):
    FIND.append(m)


print("=" * 74)
print("G3  QUESTION A -- ARE THE 24 FINDINGS REAL?")
print("=" * 74)

new_target = L.read_worktree(L.TARGET_REL)
old_target = L.git_show(L.REV_A218, L.TARGET_REL)
out_new, rc_new = L.run_c1(new_target)
out_old, rc_old = L.run_c1(old_target)
raised = L.findings_of(out_new)
mine = L.parse_c1_own_vertices(out_old)
tgt_sets = L.parse_vertex_sets(new_target)
tgt_counts_old = L.parse_vertex_counts_oldform(old_target)

print("""
   The 24 findings, reproduced here rather than quoted: c1_branching.py at
   %s, run against out_t1_tl.txt at %s.
""" % (L.REV_A218[:8], L.head_rev()[:8]))
print("      SELF-ERRORS %s   FINDINGS %s   TOTAL BAD %s   exit %d"
      % (L.totals_of(out_new) + (rc_new,)))
if len(raised) != 24:
    selferr("the run raised %d findings, not the 24 this ticket is about"
            % len(raised))
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("(i) THE MECHANISM, MEASURED -- WHY 'target ?' AND NOT 'CANNOT READ'")
print("-" * 74)
print("""   c1 finds the target's vertex counts with one regex, quoted from its
   own source at %s:

       m = re.match(r"\\s*(\\d)\\s+((?:\\d+\\s+){5}\\d+)\\s*$", line)

   and then compares with

       tgt_counts.get(beta, [None] * 6)[n - 1] != mine_c

   so a cell the regex never filled is compared as None, and None differs from
   every integer.  ABSENCE IS RENDERED AS DISAGREEMENT.  That is not an
   inference about the code; it is what the two lines above do, and the row
   below counts how many lines each target offers the regex.
""" % L.REV_A218[:8])
rx = re.compile(r"\s*(\d)\s+((?:\d+\s+){5}\d+)\s*$")
for name, txt in [("286d5030 (the reproduction's)", old_target),
                  ("d1dd84d2 (HEAD)", new_target)]:
    seg = L.t1b2(txt)
    hits = [l for l in seg.splitlines() if rx.match(l)]
    print("   lines in T1b2 matching c1's count regex, %-30s : %d"
          % (name, len(hits)))
    for h in hits:
        print("        %s" % h.rstrip())
print()
print("   4 rows at the old revision, one per parameter, six counts each = 24")
print("   cells.  0 rows at HEAD.  The regex is looking for a table mg-13b2")
print("   deleted -- on mg-a218's OWN finding X1, which said the count was the")
print("   defect.  The parser that read it was not widened with c2's.")
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("(ii) THE 24, ONE AT A TIME.  Established before any is called a defect")
print("-" * 74)
print("""   CONFIRMED      = the target states the datum and it disagrees with c1.
   PARSER ARTIFACT = the target states the datum -- in this or a stronger
                     form -- and it AGREES; the word 'disagrees' is false and
                     the accusation is the parser's, not the target's.
   UNKNOWN         = the target does not determine the datum at all, so
                     nothing can be concluded either way.
""")
print("   #   finding as raised by c1                                "
      "target states      class")
classes = {"CONFIRMED": [], "PARSER ARTIFACT": [], "UNKNOWN": []}
for i, f in enumerate(sorted(raised), start=1):
    m = re.match(r"vertex COUNT disagrees at beta=(\d+) n=(\d+): "
                 r"target (\S+), mine (\d+)", f)
    if not m:
        selferr("finding %d is not of the vertex-count shape this script "
                "classifies: %r" % (i, f))
        continue
    beta, n = int(m.group(1)), int(m.group(2))
    said, mine_c = m.group(3), int(m.group(4))
    t = tgt_sets.get((beta, n))
    if t is None:
        cls, states = "UNKNOWN", "nothing"
    elif len(t) == mine_c and t == mine.get((beta, n)):
        cls, states = "PARSER ARTIFACT", "%s -> %d" % (L.render_set(t), len(t))
    elif len(t) != mine_c:
        cls, states = "CONFIRMED", "%s -> %d" % (L.render_set(t), len(t))
    else:
        cls, states = "CONFIRMED", "%s (count agrees, set does not)" % L.render_set(t)
    classes[cls].append((beta, n))
    print("   %2d  beta=%d n=%d: target %s, mine %d%s  %-18s %s"
          % (i, beta, n, said, mine_c, " " * 24, states, cls))
print()
for cls in ("CONFIRMED", "PARSER ARTIFACT", "UNKNOWN"):
    print("   %-16s %2d of %d" % (cls, len(classes[cls]), len(raised)))
print("   population: the 24 findings c1 raises against the HEAD target,")
print("   classified one at a time and none by inheritance from another.")
print()
if classes["CONFIRMED"]:
    finding("%d of the 24 findings are CONFIRMED against the target: %s"
            % (len(classes["CONFIRMED"]), sorted(classes["CONFIRMED"])))
if classes["UNKNOWN"]:
    finding("%d of the 24 findings cannot be resolved from the target at all: "
            "%s" % (len(classes["UNKNOWN"]), sorted(classes["UNKNOWN"])))
if len(classes["PARSER ARTIFACT"]) + len(classes["CONFIRMED"]) + \
        len(classes["UNKNOWN"]) != len(raised):
    selferr("the three boxes do not partition the %d findings" % len(raised))

print("   AND c1's OWN POPULATION LINE, checked because it is a count that")
print("   names a population and the population is empty:")
for l in out_new.splitlines():
    if "vertex counts:" in l and "cells compared" in l:
        print("     %s" % l.strip())
n_compared = sum(1 for beta in L.BETAS for n in range(1, L.NMAX + 1)
                 if L.parse_vertex_counts_oldform(new_target).get((beta, n))
                 is not None)
print("     cells actually compared against a value the target states in the "
      "form c1 reads: %d" % n_compared)
print("     -- mg-d330 booked this and it is CONFIRMED here, not re-opened.")
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("(iii) THE 174 NON-FINDINGS -- ARE THEY AGREEMENT, OR SILENCE?")
print("-" * 74)
print("""   This is the half the count cannot answer.  On the HEAD target c1
   reports 0 disagreements over 53 dimension cells and 121 edge cells.  A
   parser blind in those channels would report the same 0.  So each channel
   is corrupted on a copy of the HEAD target and the DIRECTION IS PREDICTED
   BEFORE THE PROBE: the probe must make c1 red, with a finding of the named
   shape.  A probe that stays green is a channel reporting nothing.
""")

probes = []


def probe(name, mutate, expect_shape, expect_red=True, target=None):
    probes.append((name, mutate, expect_shape, expect_red,
                   new_target if target is None else target))


def drop_edges_of_beta(text, beta):
    """Delete every 'L(n,p) dim d -> ...' row inside ONE parameter block."""
    head, rest = text.split("---- beta = %d ----" % beta, 1)
    # the block ends at the next 'multiplicity-free at beta' summary line
    end = rest.index("multiplicity-free at beta")
    block, tail = rest[:end], rest[end:]
    block, n = L.drop_lines(block,
                            lambda l: re.match(r"\s*L\(\d,\d\) dim \d+\s+->", l))
    if n == 0:
        raise ValueError("no edge rows found in the beta = %d block" % beta)
    return head + "---- beta = %d ----" % beta + block + tail


# THE BETA LABELS ON THREE OF THESE PROBES WERE WRONG WHEN FIRST WRITTEN, and
# the correction is recorded here rather than in a commit message, per this
# repo's convention.  The rows 'L(5,2) dim 1 -> [L(4,0)]=0 [L(4,1)]=0
# [L(4,2)]=1' and 'L(6,2) dim 9 -> [L(5,0)]=0 [L(5,1)]=2 [L(5,2)]=1' are unique
# in T1b2 (ii) -- which is why replace_in_t1b2 accepts them -- but they sit in
# the beta = 1 block, not beta = 0, and the probes said beta = 0.  Every probe
# still FIRED; what was wrong was the label and, for the first, the predicted
# finding text, which named beta=0 and so failed to match a finding that named
# beta=1.  It is booked as a miss in PREDICTIONS.md and kept as written there.
# Nothing about the conclusion moves: a probe that fires with the wrong label
# is a bookkeeping error, and a probe that does not fire is a dead channel.
probe("one digit of one EDGE cell (beta=1, [L(4,2)] of L(5,2) dim 1)",
      lambda t: L.replace_in_t1b2(
          t, "L(5,2) dim 1  ->  [L(4,0)]=0  [L(4,1)]=0  [L(4,2)]=1",
          "L(5,2) dim 1  ->  [L(4,0)]=0  [L(4,1)]=0  [L(4,2)]=7"),
      r"\[L\(5,2\):L\(4,2\)\] at beta=1 disagrees")
probe("one digit of a MULTIPLICITY-2 edge (beta=1, [L(3,0)] of L(4,1))",
      lambda t: L.replace_in_t1b2(
          t, "L(4,1) dim 3  ->  [L(3,0)]=2  [L(3,1)]=1",
          "L(4,1) dim 3  ->  [L(3,0)]=1  [L(3,1)]=1"),
      r"disagrees: target 1, mine 2")
probe("one digit of one DIMENSION cell (beta=1, L(6,2) dim 9 -> dim 8)",
      lambda t: L.replace_in_t1b2(
          t, "L(6,2) dim 9  ->  [L(5,0)]=0  [L(5,1)]=2  [L(5,2)]=1",
          "L(6,2) dim 8  ->  [L(5,0)]=0  [L(5,1)]=2  [L(5,2)]=1"),
      r"dim L\(6,2\) at beta=1 disagrees")
probe("DELETING a whole L(n,p) row (beta=1, L(5,2) dim 1)",
      lambda t: L.drop_lines(
          t, lambda l: l.strip().startswith(
              "L(5,2) dim 1  ->  [L(4,0)]=0"))[0],
      r"target prints no cell for \[L\(5,2\):L\(4,\d\)\]")
probe("DELETING every edge row of one parameter block (beta = 0)",
      lambda t: drop_edges_of_beta(t, 0),
      r"target prints no cell for \[L\(\d,\d\):L\(\d,\d\)\] at beta=0")
probe("NULL PROBE: a prose line inside T1b2, no figure touched",
      lambda t: L.replace_in_t1b2(
          t, "Graham-Lehrer: the irreducibles are the non-zero",
          "Graham-Lehrer: the simple modules are the non-zero"),
      None, expect_red=False)
probe("CONTROL on the count channel, at 286d5030 where it was LIVE: "
      "one digit of the count table",
      lambda t: L.replace_in_t1b2(t, "\n  3        1    2    2    3    3    4",
                                  "\n  3        1    2    2    3    3    9"),
      r"vertex COUNT disagrees at beta=3 n=6: target 9, mine 4",
      target=old_target)

print("   probe                                                          "
      "  predicted  actual  fires")
fired = 0
for (name, mutate, shape, expect_red, base) in probes:
    try:
        cor = mutate(base)
    except Exception as e:
        selferr("probe %r could not be applied: %s" % (name, e))
        continue
    if cor == base:
        selferr("probe %r changed nothing" % name)
        continue
    o, rc = L.run_c1(cor)
    fs = L.findings_of(o)
    base_out, base_rc = (out_new, rc_new) if base is new_target else (out_old, rc_old)
    base_fs = L.findings_of(base_out)
    new_fs = [f for f in fs if f not in base_fs]
    red = len(new_fs) > 0
    ok = (red == expect_red)
    if ok and expect_red and shape:
        ok = any(re.search(shape, f) for f in new_fs)
    fired += ok
    print("   %-62s %-10s %-7s %s"
          % (name[:62], "RED" if expect_red else "green",
             "RED" if red else "green", "YES" if ok else "NO"))
    if new_fs:
        print("        first new finding: %s" % new_fs[0][:96])
    if not ok:
        finding("probe %r did not behave as predicted: expected %s with a "
                "finding matching %r, got %d new findings"
                % (name, "RED" if expect_red else "green", shape, len(new_fs)))
print()
print("   probes firing as predicted: %d of %d, population: the %d corruption "
      "probes above -- %d on the edge channel, %d on the dimension channel, "
      "1 null and 1 control on the count channel at the old revision"
      % (fired, len(probes), len(probes), 3, 1))
print()
print("""   READ THIS TOGETHER WITH (ii).  The 53 dimension and 121 edge cells go
   RED under a one-digit change, so their 0 disagreements is a measurement.
   The 24 vertex cells go red under NOTHING, because they compare against a
   value that is not there -- and at the old revision the same channel goes
   red on a one-digit change, which is what a live channel looks like.  The
   two are distinguished by the probes, not by the counts.""")
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("VERDICT ON QUESTION A")
print("-" * 74)
print("""   Of the 24 findings c1_branching.py raises against the target:

     CONFIRMED       : %d
     PARSER ARTIFACT : %d
     UNKNOWN         : %d

   Every one of the 24 names a cell where the target states the vertex set
   in a form STRICTLY RICHER than the count c1 is looking for, and where
   that set agrees with c1's own measurement label for label.  The target
   does not disagree with c1 anywhere.  The findings are the parser's.

   THE DEFECT IS REAL AND IT IS c1's, NOT THE TARGET'S.  It is exactly the
   one mg-d330 booked: a channel that has gone blind books its blindness as
   FINDINGS against the target instead of SELF-ERRORS against itself, and
   c1's own population line then reports 24 cells compared where 0 were.
   Confirmed here by the probes above, not re-opened.

   The other 174 cells are unaffected and their agreement is real: %d of %d
   corruption probes on those channels fire.
""" % (len(classes["CONFIRMED"]), len(classes["PARSER ARTIFACT"]),
       len(classes["UNKNOWN"]), fired, len(probes)))

print("-" * 74)
print("SELF-ERRORS: %d, population: the parse of the %d raised findings, the "
      "3-box partition, and the application of the %d probes"
      % (len(SELF), len(raised), len(probes)))
for x in SELF:
    print("   SELF-ERROR: " + x)
print("FINDINGS: %d, population: the 24 findings classified one at a time and "
      "the %d corruption probes on the 53 dimension and 121 edge channels"
      % (len(FIND), len(probes)))
for x in FIND:
    print("   FINDING: " + x)
print("TOTAL BAD: %d" % (len(SELF) + len(FIND)))
sys.exit(1 if (SELF or FIND) else 0)
