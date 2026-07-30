"""h1_questions.py -- WERE THE TWO QUESTIONS ACTUALLY KEPT SEPARATE?

mg-d330 left one open item that was two questions wearing one label:

  A  are the 24 findings c1_branching.py raises REAL?   (about the parser)
  B  does the 198-cell reproduction still stand?        (about provenance)

A single verdict written across both -- "the instrument is sound" -- answers
neither and reads as answering both.  So this script does not ask whether the
document SAYS they are separate.  It checks three things that a merged verdict
could not survive:

  1. the two answers are DIFFERENT (B: yes, A: no).  One verdict cannot be
     both.
  2. they are produced by DIFFERENT scripts with independent exit codes, and
     neither script reads the other's conclusion.
  3. each is independently re-derived HERE, on this instrument's own reader,
     and agrees.

B is re-derived by re-running at the old revision, because that is cheap and
there is therefore no excuse for the assertion form.  A is re-derived by
classifying all 24 cells one at a time.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import sys

import lib321d as L

R = L.Report("h1", "the 3 separation checks, the 6 checks on B's re-run, "
                   "the 4 checks on A's census, and the 24 cells classified "
                   "independently here")

L.banner("H1", "THE TWO QUESTIONS -- KEPT SEPARATE, AND EACH ANSWERED?")

doc = L.read_worktree(L.DOC_58DA)
HEAD = L.head_rev()

# ---------------------------------------------------------------------------
L.rule("(i) THE REVISIONS, NAMED IN FULL")
print("   %s  mg-a218, where the 198-cell reproduction was taken" % L.REV_A218)
print("      %s" % L.subject(L.REV_A218)[:88])
print("   %s  mg-58da, the repair under audit" % L.REV_58DA)
print("      %s" % L.subject(L.REV_58DA)[:88])
print("   %s  HEAD of this branch" % HEAD)
print()
print("   the document names B's revision as a 12-char prefix; does it resolve?")
named = "286d5030902d" in doc
print("      '286d5030902d' appears in the document          : %s" % named)
if named:
    resolved = L.full_rev("286d5030902d")
    print("      git rev-parse '286d5030902d'                    : %s" % resolved)
    R.check(resolved == L.REV_A218,
            "the revision the document names for B does not resolve to the "
            "revision the reproduction was taken at")
else:
    R.finding("the document does not name the revision B is claimed at; a "
              "reproduction whose revision is not named cannot be re-run")

# ---------------------------------------------------------------------------
L.rule("(ii) SEPARATION CHECK 1 -- THE TWO ANSWERS ARE DIFFERENT")
print("""   A single verdict cannot answer 'yes' and 'no'.  So if the document's
   two answers point in opposite directions, they are not one verdict wearing
   two labels.  Read out of the bottom-line table's own rows.""")
print()
rows = {}
for line in doc.splitlines():
    if line.startswith("| **B** |") or line.startswith("| **A** |"):
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows[cells[0].strip("* ")] = cells
for k in ("B", "A"):
    if k not in rows:
        R.finding("the document's bottom-line table has no row for question %s"
                  % k)
    else:
        print("   row %s: %s" % (k, rows[k][1][:60]))
        print("        -> %s" % rows[k][2][:96])
print()
if "B" in rows and "A" in rows:
    b_yes = "YES" in rows["B"][2]
    a_no = "NO" in rows["A"][2] and "PARSER ARTIFACT" in rows["A"][2]
    print("   B's answer is affirmative               : %s" % b_yes)
    print("   A's answer is negative (not real)       : %s" % a_no)
    R.check(b_yes and a_no,
            "the two questions do not receive opposite answers in the "
            "bottom-line table; a merged verdict cannot be ruled out this way")
    R.check(rows["B"][2] != rows["A"][2],
            "questions A and B are given the SAME answer text -- one verdict "
            "written across both")

# ---------------------------------------------------------------------------
L.rule("(iii) SEPARATION CHECK 2 -- DIFFERENT SCRIPTS, INDEPENDENT EXITS")
print("""   The stronger form of the same check: A and B are answered by
   different programs, each with its own exit code, and neither reads the
   other's conclusion.  If g3 consulted g1's verdict the two would be one.""")
print()
g1 = L.git_show(L.REV_58DA, L.S58DA_DIR + "/g1_provenance.py")
g2 = L.git_show(L.REV_58DA, L.S58DA_DIR + "/g2_redo.py")
g3 = L.git_show(L.REV_58DA, L.S58DA_DIR + "/g3_findings.py")
print("   g1_provenance.py answers B    : %s"
      % ("QUESTION B" in g1 and "QUESTION A" not in g1.split('"""')[1]))
print("   g3_findings.py   answers A    : %s"
      % ("QUESTION A" in g3))
cross = []
for name, src in (("g1", g1), ("g2", g2), ("g3", g3)):
    for other in ("out_g1_provenance.txt", "out_g2_redo.txt",
                  "out_g3_findings.txt"):
        if other in src:
            cross.append("%s reads %s" % (name, other))
print("   any of g1/g2/g3 reading another's output : %s"
      % (", ".join(cross) if cross else "NONE"))
R.check(not cross,
        "one of the scripts answering A or B reads another's output, so the "
        "two verdicts are not independent: %s" % ", ".join(cross))
print()
print("   each exits on its OWN totals (sys.exit(1 if (SELF or FIND) else 0)):")
for name, src in (("g1", g1), ("g2", g2), ("g3", g3)):
    own = "sys.exit(1 if (SELF or FIND) else 0)" in src
    print("      %-3s %s" % (name, own))
    R.check(own, "%s does not exit on its own totals" % name)

# ---------------------------------------------------------------------------
L.rule("(iv) QUESTION B, RE-DERIVED HERE -- THE RE-RUN, NOT AN ASSERTION")
print("""   'The change did not touch that path' is an assertion until the
   re-run shows it, and the re-run is cheap.  Done here, on this instrument's
   own scratch tree, independently of g1.""")
print()
old_target = L.git_show(L.REV_A218, L.TARGET_REL)
out_old, rc_old = L.run_c1(old_target, script_rev=L.REV_A218)
s, f, t = L.totals_of(out_old)
pops = L.cells_compared(out_old)
total_cells = sum(pops.values())
print("   c1_branching.py @ %s  vs  out_t1_tl.txt @ %s"
      % (L.REV_A218[:12], L.REV_A218[:12]))
print("      SELF-ERRORS %s   FINDINGS %s   TOTAL BAD %s   exit %d"
      % (s, f, t, rc_old))
for k in ("vertex", "vertex dimensions", "edge multiplicities"):
    print("      %-22s %3d cells compared" % (k, pops.get(k, -1)))
print("      %-22s %3d" % ("TOTAL CELLS", total_cells))
print()
R.check((s, f) == (0, 0),
        "the re-run at %s does not reproduce: SELF %s FINDINGS %s"
        % (L.REV_A218[:12], s, f))
R.check(rc_old == 0, "the re-run at %s exits %d, not 0"
        % (L.REV_A218[:12], rc_old))
R.check((pops.get("vertex"), pops.get("vertex dimensions"),
         pops.get("edge multiplicities")) == (24, 53, 121),
        "the re-run's three populations are not 24 / 53 / 121: %s" % pops)
R.check(total_cells == 198,
        "the re-run compares %d cells, not the 198 claimed" % total_cells)

committed = L.git_show(L.REV_A218, L.A218_DIR + "/out_c1_branching.txt")
print("   against out_c1_branching.txt as committed at that revision:")
print("      re-run    sha256 %s" % L.sha(out_old))
print("      committed sha256 %s" % L.sha(committed))
if out_old == committed:
    print("      BYTE-IDENTICAL.")
R.check(out_old == committed,
        "the re-run at %s is NOT byte-identical to the committed "
        "out_c1_branching.txt" % L.REV_A218[:12])
print()
print("   >> B, re-stated with the revision named in full, on this")
print("   >> instrument's own re-run: at")
print("   >> %s," % L.REV_A218)
print("   >> mg-a218's c1_branching.py compared %d cells against mg-e8b8's"
      % total_cells)
print("   >> committed out_t1_tl.txt and disagreed in %s of them." % f)

# ---------------------------------------------------------------------------
L.rule("(v) QUESTION A, RE-DERIVED HERE -- ALL 24, ONE AT A TIME")
print("""   Each of the 24 gets a status.  A residual UNKNOWN bucket is honest;
   a reduction of 24 to a smaller number without saying what happened to the
   rest is not.  So the population is fixed at 24 FIRST and every one of the
   24 is accounted for, whatever its status.""")
print()
new_target = L.read_worktree(L.TARGET_REL)
out_head, rc_head = L.run_c1(new_target, script_rev=L.REV_A218)
raised = {}
for x in L.findings_of(out_head):
    if x.startswith("vertex COUNT disagrees at beta="):
        key = x.split("at ", 1)[1].split(":", 1)[0]
        b = int(key.split("beta=")[1].split()[0])
        n = int(key.split("n=")[1])
        raised[(b, n)] = x
print("   findings the UNREPAIRED c1 raises against the HEAD target : %d"
      % len(L.findings_of(out_head)))
print("   of those, vertex-cell findings                            : %d"
      % len(raised))
R.check(len(raised) == 24,
        "the unrepaired c1 raises %d vertex-cell findings, not the 24 mg-d330 "
        "reported" % len(raised))

tgt = L.parse_vertex_cells(new_target)          # MY reader, subsection-anchored
mine = L.parse_c1_own_cells(out_head)           # c1's own measurement
print("   cells my own reader finds in the target's subsection (i)  : %d of 24"
      % sum(1 for c in L.CELLS if c in tgt))
print()
print("   #   cell         c1 raised            target states (my reader)   "
      "class")
census = {"CONFIRMED": [], "PARSER ARTIFACT": [], "UNKNOWN": []}
for i, cell in enumerate(L.CELLS, 1):
    b, n = cell
    if cell not in raised:
        continue
    tv = tgt.get(cell)
    mv = mine.get(cell)
    if mv is None:
        R.selferr("c1's own measurement for beta=%d n=%d could not be read "
                  "out of its stdout by this script" % (b, n))
        cls = "UNKNOWN"
    elif tv is None:
        cls = "UNKNOWN"
    elif tv == mv:
        cls = "PARSER ARTIFACT"
    else:
        cls = "CONFIRMED"
    census[cls].append(cell)
    print("   %2d  beta=%d n=%d    target ?, mine %-4d %-27s %s"
          % (i, b, n, len(mv or []), L.render(tv) if tv is not None
             else "(not stated)", cls))
print()
accounted = sum(len(v) for v in census.values())
for k in ("CONFIRMED", "PARSER ARTIFACT", "UNKNOWN"):
    print("   %-16s %2d of 24" % (k, len(census[k])))
print("   %-16s %2d of 24   <- every one of the 24 has a status"
      % ("ACCOUNTED FOR", accounted))
print("   population: the 24 vertex cells (beta,n), beta in {3,2,1,0},")
print("   1 <= n <= 6, that the unrepaired c1 raises against the HEAD target.")
R.check(accounted == 24,
        "%d of the 24 findings have a status; %d are silently unaccounted for"
        % (accounted, 24 - accounted))
if census["CONFIRMED"]:
    R.finding("%d of the 24 are CONFIRMED against the target: %s"
              % (len(census["CONFIRMED"]), census["CONFIRMED"]))
if census["UNKNOWN"]:
    print("   NOTE: %d are UNKNOWN, which is an honest residue and is stated "
          "as one." % len(census["UNKNOWN"]))

# ---------------------------------------------------------------------------
L.rule("(vi) DOES MY CENSUS AGREE WITH mg-58da'S -- ROWS, NOT SUMMARY?")
g3out = L.git_show(L.REV_58DA, L.S58DA_DIR + "/out_g3_findings.txt")
their_rows = {}
for line in g3out.splitlines():
    s_ = line.strip()
    if "beta=" not in s_ or "target ?" not in s_:
        continue
    for lbl in ("PARSER ARTIFACT", "CONFIRMED", "UNKNOWN"):
        if s_.endswith(lbl):
            b = int(s_.split("beta=")[1].split()[0])
            n = int(s_.split("n=")[1].split(":")[0])
            their_rows[(b, n)] = lbl
            break
print("   rows in g3's own table carrying a class label : %d" % len(their_rows))
their_census = {k: sorted(c for c, v in their_rows.items() if v == k)
                for k in census}
for k in ("CONFIRMED", "PARSER ARTIFACT", "UNKNOWN"):
    print("   %-16s  g3's rows %2d   mine %2d   %s"
          % (k, len(their_census[k]), len(census[k]),
             "agree" if sorted(census[k]) == their_census[k] else "DISAGREE"))
R.check(len(their_rows) == 24,
        "g3's table carries %d classified rows, not 24" % len(their_rows))
for k in census:
    R.check(sorted(census[k]) == their_census[k],
            "my classification and g3's rows disagree in the %s bucket: mine "
            "%s, g3's %s" % (k, sorted(census[k]), their_census[k]))
print()
print("   and g3's own SUMMARY lines, compared against g3's own ROWS:")
for k in ("CONFIRMED", "PARSER ARTIFACT", "UNKNOWN"):
    want = None
    for line in g3out.splitlines():
        p = line.strip()
        if p.startswith(k) and " of 24" in p:
            want = int(p.split()[-3])
            break
    print("      %-16s summary says %s, rows say %d"
          % (k, want, len(their_census[k])))
    R.check(want == len(their_census[k]),
            "g3's summary says %s for %s but its own rows say %d"
            % (want, k, len(their_census[k])))

# ---------------------------------------------------------------------------
L.rule("(vii) AND THE DOCUMENT'S OWN THREE BUCKETS, SUMMED")
got = {}
for k in ("CONFIRMED", "PARSER ARTIFACT", "UNKNOWN"):
    for line in doc.splitlines():
        if line.startswith("| **%s**" % k):
            cell = [c.strip() for c in line.strip("|").split("|")][1]
            digits = "".join(ch for ch in cell if ch.isdigit() or ch == " ")
            got[k] = int(digits.split()[0])
            break
print("   the document's own table: %s" % got)
print("   sum: %s" % sum(got.values()))
R.check(sum(got.values()) == 24,
        "the document's three buckets sum to %d, not 24 -- a silent reduction"
        % sum(got.values()))
for k in got:
    R.check(got[k] == len(census[k]),
            "the document says %s = %d; measured here it is %d"
            % (k, got[k], len(census[k])))

sys.exit(R.emit())
