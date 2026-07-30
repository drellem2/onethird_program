"""selftest_321d.py -- calibrate this instrument before it is believed.

An audit whose own reader is untested is an audit that will report absence as
disagreement, which is the defect it was sent to look for.  It happened to this
instrument once already, on its first run: h3's reader for mg-2060's output
matched only one header form, recovered 0 of 24 cells, and the comparison duly
booked FOUR findings against an instrument that agrees at 24 of 24.  It is
recorded in h3's source and in the README, and the fix was in two places -- the
pattern, and the routing of 'I could not read it' to SELF-ERROR.

These assertions exist so the next one is caught here instead.

Exit 0 iff every assertion passes.
"""

import sys

import lib321d as L

N = [0]
BAD = []


def ok(cond, what):
    N[0] += 1
    if not cond:
        BAD.append(what)


print("=" * 74)
print("SELFTEST  mg-321d")
print("=" * 74)

# --- the target, read by my subsection-anchored reader ---------------------
tgt_text = L.read_worktree(L.TARGET_REL)
cells = L.parse_vertex_cells(tgt_text)
ok(len(cells) == 24, "the target yields 24 vertex cells")
for c in L.CELLS:
    ok(c in cells, "cell %s present" % (c,))
ok(cells[(3, 6)] == [(0, 1), (1, 5), (2, 9), (3, 5)], "beta=3 n=6 set")
ok(cells[(0, 1)] == [(0, 1)], "beta=0 n=1 set")
ok(cells[(1, 6)] == [(0, 1), (1, 4), (2, 9), (3, 1)], "beta=1 n=6 set")
ok(L.render(cells[(3, 6)]) == "[0:1,1:5,2:9,3:5]", "render round-trips")

# --- ABSENCE IS RETURNED AS ABSENCE, never as a value ----------------------
no_sub = tgt_text.replace("  (i) THE VERTEX SET", "  (i) SOMETHING ELSE", 1)
ok(L.vertex_subsection(no_sub) == "", "no subsection -> empty, not a guess")
ok(L.parse_vertex_cells(no_sub) == {}, "no subsection -> no cells at all")
one_gone = tgt_text.replace("     n=6  [0:1,1:5,2:9,3:5]\n", "", 1)
c2 = L.parse_vertex_cells(one_gone)
ok(len(c2) == 23, "deleting one row loses exactly one cell")
ok((3, 6) not in c2, "and it is the right cell")
ok((3, 5) in c2 and (2, 6) in c2, "and only that one")

# --- THE ANCHORING PROPERTY, which is why this reader is a third one -------
# A bracket row placed inside T1b2 but OUTSIDE subsection (i) must not be
# picked up.  A reader that scans the whole T1b2 block would take it.
MARK_II = "  (ii) THE EDGES"
ok(MARK_II in L.t1b2_block(tgt_text), "subsection (ii) is where I think it is")
poison = tgt_text.replace(
    MARK_II, MARK_II + "\n\n  beta = 2\n     n=1  [9:9]\n     n=7  [8:8]\n", 1)
pc = L.parse_vertex_cells(poison)
ok(pc.get((2, 1)) == [(0, 1)],
   "a bracket row AFTER subsection (i) does not overwrite a real cell")
ok(len(pc) == 24 and (2, 7) not in pc, "and adds no cell")
# and the same poison INSIDE subsection (i) IS read -- so the assertion above
# is about the anchor, not about the reader being inert
inside = tgt_text.replace("  (ii) THE EDGES",
                          "  beta = 2\n     n=7  [8:8]\n\n  (ii) THE EDGES", 1)
ok(L.parse_vertex_cells(inside).get((2, 7)) == [(8, 8)],
   "the same row INSIDE subsection (i) IS read -- the anchor is what differs")

# a stray SEVEN-INTEGER row -- what c1's count regex takes -- is nothing here
stray = tgt_text.replace("  (i) THE VERTEX SET",
                         "     2      9      9      9      9      9      9\n"
                         "  (i) THE VERTEX SET", 1)
ok(L.parse_vertex_cells(stray) == cells,
   "a stray seven-integer row changes nothing this reader sees")

# --- c1's own measurement, read off its own stdout -------------------------
out, rc = L.run_c1(tgt_text, script_rev=L.REV_A218)
mine = L.parse_c1_own_cells(out)
ok(len(mine) == 24, "c1's own section (i) yields 24 cells")
ok(mine[(3, 6)] == [(0, 1), (1, 5), (2, 9), (3, 5)], "c1's beta=3 n=6")
ok(all(mine[c] == cells[c] for c in L.CELLS),
   "c1's own measurement equals the target at all 24 -- the fact question A "
   "turns on")

# --- the report readers ----------------------------------------------------
ok(L.totals_of(out) == (0, 24, 24), "unrepaired c1 vs HEAD target: 0/24/24")
ok(rc == 1, "and it exits 1")
ok(len(L.findings_of(out)) == 24, "24 findings read back")
ok(L.selferrs_of(out) == [], "and no self-errors")
FAKE = ("SELF-ERRORS: 3, population: p\n   SELF-ERROR: a\n"
        "FINDINGS: 2, population: q\n   FINDING: b\nTOTAL BAD: 5\n")
ok(L.totals_of(FAKE) == (3, 2, 5), "totals_of on a synthetic report")
ok(L.findings_of(FAKE) == ["b"], "findings_of on a synthetic report")
ok(L.selferrs_of(FAKE) == ["a"], "selferrs_of on a synthetic report")

# --- BOTH population wordings, pre- and post-repair ------------------------
old_w = "     vertex counts: 24 cells compared, population: ...\n"
new_w = ("     vertex cells: 24 cells compared, 0 not compared because this "
         "script could not read them; population: ...\n")
ok(L.cells_compared(old_w) == {"vertex": 24}, "reads the pre-repair wording")
ok(L.cells_compared(new_w) == {"vertex": 24}, "reads the post-repair wording")
ok(L.cells_compared("") == {}, "and invents nothing from silence")
live_out, _ = L.run_c1(tgt_text, script_rev=L.REV_A218,
                       script_text=L.read_worktree(L.A218_DIR +
                                                   "/c1_branching.py"))
ok(L.cells_compared(live_out).get("vertex") == 24,
   "the repaired c1's own population line is read")

# --- git ------------------------------------------------------------------
ok(L.full_rev("286d5030902d") == L.REV_A218, "the named revision resolves")
ok(L.commits_touching(L.A218_DIR + "/c1_branching.py", L.REV_A218,
                      L.head_rev()) == [L.REV_58DA],
   "c1_branching.py was touched by exactly one commit since 286d5030")
ok(L.commits_touching(L.A218_DIR + "/kern_a218.py", L.REV_A218,
                      L.head_rev()) == [],
   "the kernel was touched by none")
ok(L.sha("") ==
   "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
   "sha256 of the empty string")

# --- the Report scaffolding ------------------------------------------------
r = L.Report("t", "p")
ok(r.check(True, "no") is True and r.findings == [], "check() is quiet on True")
ok(r.check(False, "yes") is False and r.findings == ["yes"],
   "check() books on False")
r2 = L.Report("t", "p")
ok(r2.findings == [] and r2.self_errs == [], "a fresh report is empty")

print()
print("   assertions: %d, population: this instrument's target reader, its "
      "anchoring" % N[0])
print("   property, its report readers for both population wordings, its git")
print("   helpers and its Report scaffolding.")
print("   failed: %d" % len(BAD))
for b in BAD:
    print("      FAILED: %s" % b)
print()
print("SELF-ERRORS: %d, population: the %d assertions above"
      % (len(BAD), N[0]))
print("FINDINGS: 0, population: this script checks only itself and makes no "
      "claim about the audit's target")
print("TOTAL BAD: %d" % len(BAD))
sys.exit(1 if BAD else 0)
