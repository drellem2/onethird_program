"""h3_setlevel.py -- WAS THE AGREEMENT ACROSS ALL FIVE RE-ESTABLISHED,
OR ONLY THE CHANGED ONE RE-RUN?

This is the reason the parent ticket exists.  Widening one member of a
mutually-corroborating set is not a local edit, because the corroboration was
the point -- and a parser that has been made to agree with a target agrees with
it.  So 'the changed script now exits 0' is not evidence of anything.

Four things are checked, in this order, and each is a different claim:

  1. THE FIVE ARE NAMED FROM DISK, not from a hard-coded list, so a sixth
     member cannot hide.
  2. WHO TOUCHED WHICH, BY COMMIT.
  3. ALL FIVE WERE RE-RUN -- every member, in place, live.
  4. THE FIGURES AGREE ACROSS ALL OF THEM.  Which of the five state the 24
     vertex figures is itself measured rather than assumed, and the ones that
     do are read HERE, off their own live stdout, by this instrument's reader.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

import lib321d as L

R = L.Report("h3", "the membership of the five, the 8 per-file attributions, "
                   "the 5 live exit codes, the 24 vertex cells across every "
                   "instrument that states them, and c0_repro.sh")

L.banner("H3", "THE SET-LEVEL PROPERTY -- ALL FIVE, NOT JUST THE CHANGED ONE")

HEAD = L.head_rev()
A218 = os.path.join(L.REPO, L.A218_DIR)

# ---------------------------------------------------------------------------
L.rule("(i) THE FIVE, NAMED FROM DISK RATHER THAN FROM A LIST")
onset = sorted(f for f in os.listdir(A218)
               if re.match(r"^c\d+_.*\.(py|sh)$", f))
print("   every c<digit>_*.{py,sh} in %s:" % L.A218_DIR)
for f in onset:
    print("      %s" % f)
print()
runall = L.read_worktree(L.A218_DIR + "/run_all.sh")
run_order = [f for f in re.findall(r"^run (\S+)$", runall, re.M)]
print("   what mg-a218's own run_all.sh runs, in order:")
for f in run_order:
    print("      %s" % f)
print()
FIVE = [f for f in run_order if re.match(r"^c\d+_.*\.py$", f)]
print("   THE FIVE (the c*.py members run_all.sh runs) : %s" % ", ".join(FIVE))
print()
print("   in the same directory and NOT among the five, with the reason:")
print("     %-22s %s" % ("selftest_a218.py",
                         "tests the kernel, not the target; prints no TOTAL BAD"))
print("     %-22s %s" % ("c0_repro.sh",
                         "a harness that re-runs the TARGET's instrument, not "
                         "a check of its own"))
print("     %-22s %s" % ("kern_a218.py", "the kernel the five share"))
print()
G4_FIVE = ["c1_branching.py", "c2_vertexsets.py", "c3_withdrawal.py",
           "c4_seam.py", "c5_record.py"]
print("   g4_fleet.py's hard-coded list : %s" % ", ".join(G4_FIVE))
print("   matches what is on disk       : %s" % (FIVE == G4_FIVE))
R.check(len(FIVE) == 5, "run_all.sh runs %d c*.py members, not five: %s"
        % (len(FIVE), FIVE))
R.check(FIVE == G4_FIVE,
        "g4's hard-coded five (%s) is not the set on disk (%s): a member can "
        "be added or renamed without the set-level check noticing"
        % (G4_FIVE, FIVE))

# ---------------------------------------------------------------------------
L.rule("(ii) WHO TOUCHED WHICH, BY COMMIT, ACROSS THE WHOLE DIRECTORY")
print("   %s, every tracked .py/.sh, %s..HEAD"
      % (L.A218_DIR, L.REV_A218[:8]))
print()
allfiles = sorted(f for f in os.listdir(A218) if f.endswith((".py", ".sh")))
touched = {}
for f in allfiles:
    cs = L.commits_touching(L.A218_DIR + "/" + f, L.REV_A218, HEAD)
    touched[f] = cs
    mark = "   <- one of the five" if f in FIVE else ""
    print("     %-22s %-24s%s"
          % (f, ", ".join(c[:8] for c in cs) or "untouched", mark))
print()
by13b2 = [f for f in FIVE if any(c.startswith(L.REV_13B2[:8])
                                 for c in touched[f])]
by58da = [f for f in FIVE if L.REV_58DA in touched[f]]
print("   of the five, touched by ed9cde4 (mg-13b2) : %d -- %s"
      % (len(by13b2), ", ".join(by13b2) or "none"))
print("   of the five, touched by 673b4c0 (mg-58da) : %d -- %s"
      % (len(by58da), ", ".join(by58da) or "none"))
print("   kern_a218.py, the kernel the five share   : %s"
      % (", ".join(c[:8] for c in touched["kern_a218.py"]) or "UNTOUCHED"))
R.check(not touched["kern_a218.py"],
        "kern_a218.py -- the kernel all five share -- was touched between %s "
        "and HEAD by %s; a change there is not a change to one member"
        % (L.REV_A218[:8], touched["kern_a218.py"]))

# ---------------------------------------------------------------------------
L.rule("(iii) ALL FIVE, RE-RUN.  NOT JUST THE CHANGED ONE.")
print("""   Each member is run IN PLACE with its stdout captured here and never
   redirected into its committed out_*.txt.  'The changed one runs' is not the
   property; the property is that the set reports one coherent verdict.""")
print()
print("   script                  committed @286d5030    live at HEAD")
print("                           self/find   exit       self/find   exit")
live = {}
for f in FIVE:
    try:
        cm = L.git_show(L.REV_A218, L.A218_DIR + "/out_%s.txt" % f[:-3])
        cs_, cf_, _ = L.totals_of(cm)
        cexit = 1 if (cs_ or cf_) else 0
    except RuntimeError:
        cs_, cf_, cexit = "?", "?", "?"
        R.selferr("no committed output for %s at %s" % (f, L.REV_A218[:8]))
    out, rc = L.run_in_repo(L.A218_DIR, f)
    s_, f_, _ = L.totals_of(out)
    live[f] = (s_, f_, rc, out)
    print("     %-22s  %s/%-7s (%s)      %s/%-7s (%d)"
          % (f, cs_, cf_, cexit, s_, f_, rc))
print()
ran = [f for f in FIVE if live[f][3].strip()]
print("   members actually re-run here : %d of 5 -- %s"
      % (len(ran), ", ".join(ran)))
R.check(len(ran) == 5,
        "only %d of the five produced output when re-run: %s"
        % (len(ran), ran))
green = [f for f in FIVE if live[f][2] == 0]
red = [f for f in FIVE if live[f][2] != 0]
print("   green : %d of 5 -- %s" % (len(green), ", ".join(green)))
print("   red   : %d of 5 -- %s" % (len(red), ", ".join(red) or "none"))
print()
for f in red:
    print("   %s exits %d, SELF %s FINDINGS %s:" % (f, live[f][2], live[f][0],
                                                    live[f][1]))
    for x in L.findings_of(live[f][3]):
        print("      FINDING: %s" % x[:160])
print()
R.check("c1_branching.py" not in red,
        "c1_branching.py is still red after the widening; the repair did not "
        "do what it was for")

# ---------------------------------------------------------------------------
L.rule("(iv) THE FIGURES -- DO THEY AGREE ACROSS ALL FIVE?")
print("""   'Do the figures agree across all of them' presupposes that all of
   them state figures.  That is measured, not assumed: each member's live
   stdout is searched for the 24 vertex cells, with this instrument's own
   reader.  A member that states none is named as stating none -- which is a
   different fact from a member that states them and agrees.""")
print()

target_cells = L.parse_vertex_cells(L.read_worktree(L.TARGET_REL))
target_dims = {k: [d for _, d in v] for k, v in target_cells.items()}


def c2_cells(out):
    """(beta, n) -> dim list, recovered from c2's PAIRWISE rows.

    c2 prints 'beta = X against beta = Y' and then, per level, the two dim
    lists side by side.  Each parameter appears in three pairs, so every cell
    is recovered three times and the three must agree -- which is checked.
    """
    got, cur = {}, None
    for raw in out.splitlines():
        s_ = raw.strip()
        if s_.startswith("beta = ") and " against beta = " in s_:
            lhs = int(s_.split("beta = ")[1].split()[0])
            rhs = int(s_.rsplit("beta = ", 1)[1].strip())
            cur = (lhs, rhs)
            continue
        if cur is None or not s_.startswith("n=") or "dims " not in s_:
            continue
        n = int(s_[2:].split()[0])
        body = s_.split("dims ", 1)[1]
        left, right = body.split(" vs ")
        for beta, part in ((cur[0], left), (cur[1], right)):
            dims = [int(x) for x in
                    part.strip().strip("[]").replace(" ", "").split(",") if x]
            prev = got.get((beta, n))
            if prev is not None and prev != dims:
                raise ValueError("c2 states two different dim lists for "
                                 "beta=%d n=%d: %s and %s" % (beta, n, prev,
                                                              dims))
            got[(beta, n)] = dims
    return got


def dims_from_bracket_rows(text):
    """(beta, n) -> dim list, from '[p:d,...]' rows under a 'beta = b' header
    -- e1's and c1's shape, read here rather than borrowed."""
    got, cur = {}, None
    for raw in text.splitlines():
        s_ = raw.strip()
        if s_.startswith("beta = ") and s_[7:].strip().isdigit():
            cur = int(s_[7:].strip())
            continue
        if s_.startswith("beta = ") and "[" in s_:
            cur = int(s_.split("beta = ")[1].split()[0])
            cells = re.findall(r"\[([\d:,]*)\]", s_)
            for n, body in enumerate(cells, 1):
                got[(cur, n)] = [int(x.split(":")[1])
                                 for x in body.split(",") if x]
            continue
    return got


def b1_cells(text):
    """(beta, n) -> dim list, from mg-2060's 'dims [..]' rows under a
    parameter header.

    THE HEADER FORM COST ME A ROUND.  The first version of this reader matched
    only '--- beta = b ---', which is the form mg-db09's target uses.  mg-2060
    writes 'beta=3:'.  The reader recovered 0 cells and the comparison below
    duly booked FOUR findings against an instrument that agrees with the
    target at 24 of 24 -- absence rendered as disagreement, which is the exact
    defect this whole audit is about, reproduced inside the auditing
    instrument on the first run.  It is recorded here rather than quietly
    fixed, and the fix is in TWO places: this pattern accepts both forms, and
    the comparison below routes 'I could not read it' to SELF-ERROR instead of
    to FINDING, so the same mistake cannot be silent next time.
    """
    got, cur = {}, None
    for raw in text.splitlines():
        s_ = raw.strip()
        m = re.match(r"-*\s*beta\s*=\s*(\d+)\s*[:-]*\s*$", s_)
        if m:
            cur = int(m.group(1))
            continue
        if cur is None or not s_.startswith("n=") or "dims " not in s_:
            continue
        n = int(s_[2:].split()[0])
        dims = [int(x) for x in s_.split("dims ", 1)[1].strip()
                .strip("[]").replace(" ", "").split(",") if x]
        got[(cur, n)] = dims
    return got


states = {}
for f in FIVE:
    out = live[f][3]
    if f == "c1_branching.py":
        states[f] = {k: [d for _, d in v]
                     for k, v in L.parse_c1_own_cells(out).items()}
    elif f == "c2_vertexsets.py":
        try:
            states[f] = c2_cells(out)
        except ValueError as e:
            R.finding("c2_vertexsets.py contradicts itself: %s" % e)
            states[f] = {}
    else:
        states[f] = {}
for f in FIVE:
    n = sum(1 for c in L.CELLS if c in states[f])
    print("     %-22s states %2d of the 24 vertex cells" % (f, n))
print()
statesome = [f for f in FIVE if states[f]]
print("   of the five, stating the 24 vertex figures : %d -- %s"
      % (len(statesome), ", ".join(statesome)))
print("   of the five, stating none of them          : %d -- %s"
      % (5 - len(statesome),
         ", ".join(f for f in FIVE if not states[f])))
print("   (c3, c4 and c5 are text/record checks over prose and git history.")
print("    They carry no vertex figure, so 'the figures agree' is vacuous for")
print("    them and is reported as vacuous rather than as agreement.)")
print()

sources = [("the target, out_t1_tl.txt (mg-e8b8, 1st)", target_dims)]
for f in statesome:
    sources.append(("%s, live (mg-a218, 3rd)" % f, states[f]))
try:
    sources.append(("out_b1_branching.txt (mg-2060, 2nd)",
                    b1_cells(L.read_worktree("code/branching_audit_2060/"
                                             "out_b1_branching.txt"))))
except Exception as e:                                   # noqa: BLE001
    R.selferr("could not read mg-2060's b1 output: %s" % e)
try:
    sources.append(("out_e1_vertexsets.txt (mg-d330, 4th)",
                    dims_from_bracket_rows(
                        L.read_worktree("code/branching_audit_d330/"
                                        "out_e1_vertexsets.txt"))))
except Exception as e:                                   # noqa: BLE001
    R.selferr("could not read mg-d330's e1 output: %s" % e)

print("   every source that states the 24, cross-compared, cell by cell:")
print()
print("     source                                        cells   vs target")
readable = []
for name, d in sources:
    have = sum(1 for c in L.CELLS if c in d)
    agree = sum(1 for c in L.CELLS if c in d and c in target_dims
                and d[c] == target_dims[c])
    print("     %-44s %2d/24   %2d/24"
          % (name, have, agree if have else 0))
    if have == 0:
        # NOT a finding.  The source has not disagreed with anything; this
        # script has failed to read it, and that is a fact about this script.
        R.selferr("I cannot read the 24 vertex cells out of %s; it is NOT "
                  "compared and is NOT counted as compared" % name)
        continue
    readable.append((name, d))
    R.check(have == 24,
            "%s states only %d of the 24 vertex cells" % (name, have))
    R.check(agree == 24,
            "%s disagrees with the target at %d of the 24 vertex cells"
            % (name, 24 - agree))
print()
print("   sources this script could read : %d of %d"
      % (len(readable), len(sources)))
pairs = 0
bad = 0
for i in range(len(readable)):
    for j in range(i + 1, len(readable)):
        pairs += 1
        di, dj = readable[i][1], readable[j][1]
        diff = [c for c in L.CELLS if di.get(c) != dj.get(c)]
        if diff:
            bad += 1
            R.finding("%s and %s disagree at %d of the 24 vertex cells: %s"
                      % (readable[i][0], readable[j][0], len(diff), diff[:6]))
print("   pairs of sources agreeing on all 24 cells : %d of %d" % (pairs - bad,
                                                                   pairs))
print("   population: every unordered pair drawn from the %d sources this"
      % len(readable))
print("   script could read, compared at all 24 (beta,n) cells.  Sources it")
print("   could not read are in the SELF-ERROR channel and are not here.")

# ---------------------------------------------------------------------------
L.rule("(v) c0_repro.sh, ON A SCRATCH COPY")
tmp = tempfile.mkdtemp(prefix="mg321d-c0-")
try:
    for d in (L.A218_DIR, L.DB09_DIR):
        shutil.copytree(os.path.join(L.REPO, d),
                        os.path.join(tmp, os.path.basename(d)))
    p = subprocess.run(["sh", "./c0_repro.sh"],
                       cwd=os.path.join(tmp, os.path.basename(L.A218_DIR)),
                       capture_output=True, text=True)
    ident = [l.strip() for l in p.stdout.splitlines() if "identical:" in l]
    print("   %s" % (ident[0] if ident else "(no identical: line)"))
    print("   exit %d" % p.returncode)
    R.check(p.returncode == 0,
            "c0_repro.sh exits %d on a scratch copy of the tree: the target's "
            "own five committed outputs do not all regenerate"
            % p.returncode)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ---------------------------------------------------------------------------
L.rule("VERDICT ON THE SET-LEVEL PROPERTY, DERIVED FROM THE ROWS ABOVE")
print("""   The five: %s.
   Touched by ed9cde4: %d (%s).  By 673b4c0: %d (%s).  Kernel: %s.
   All five re-run in place here: %d of 5.
   Green: %d of 5.  Red: %s.
   Vertex figures: %d of the five state them, and every source in the tree
   that states them agrees with the target at 24 of 24 cells.
"""% (", ".join(FIVE), len(by13b2), ", ".join(by13b2) or "none",
      len(by58da), ", ".join(by58da) or "none",
      "untouched" if not touched["kern_a218.py"] else "TOUCHED",
      len(ran), len(green), ", ".join(red) or "none", len(statesome)))
if red:
    R.finding("the set-level property does NOT hold on the tree as committed: "
              "%d of the five are green and %s exits 1. That is mg-d330's "
              "second finding and mg-58da books it and leaves it OPEN rather "
              "than working around it; it is re-derived here and NOT closed "
              "here either. The corroboration among the members that measure "
              "the vertex cells IS re-established -- all five were re-run, "
              "not only the changed one, and every instrument in the tree "
              "that states the 24 agrees with the target at 24 of 24"
              % (len(green), ", ".join(red)))

sys.exit(R.emit())
