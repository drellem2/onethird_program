"""q1_reason.py -- THE REASON, NOT THE ROW.

mg-69d1 repaired a reason.  A repair that fixes a reason can write a new wrong
one, and the new one arrives with the same protection the old one had: nobody
builds the input a sentence names, because a sentence is not a row.

So the new sentence is treated exactly as mg-e34a treated the old one.  It makes
two claims, each naming an input, and both inputs are BUILT here -- with bends
written in `lib2c77` from the sentence's own words, not imported from
`lib69d1`, so that "mg-69d1's measurement reproduces" is a second measurement
and not the same one read twice.

FOUR THINGS THIS ASKS THAT mg-69d1's OWN p3 DOES NOT

  (a) THE ROWS ARE g1's ROWS.  p3 scores the pairs at
      `(bent_c1, head_kern)` / `(head_c1, bent_kern)`, holding the un-bent side
      at HEAD.  g1 holds it at REV_A218: `(head_c1, old_kern)` /
      `(old_c1, head_kern)`.  p3's docstring says "the same three (script,
      kernel) rows g1's HALVES uses" and they are not the same rows.  Whether
      the difference changes a verdict is a measurement, made here.

  (b) A SECOND CONSPIRING PAIR, OF A DIFFERENT SHAPE.  p3 builds one, through
      an integer default of 0 that shifts a printed value.  Pair B conspires
      through a BOOLEAN default of False that adds a vertex which is not there.
      One mechanism demonstrated once is a demonstration of that mechanism.

  (c) A THIRD INPUT THAT IS NEITHER.  The corrected reason is written as two
      named cases.  Two named cases read as a partition unless something says
      otherwise, and a one-sided defect is neither.  It is built and scored
      against the same three rows.

  (d) IS `MOVED` A CATCH?  The whole reason turns on the word "catches".  g1's
      finding-booking block is EXECUTED here on synthetic input, in both
      directions, so that "caught" is a gate that was seen to fire and not a
      word that was read.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lib2c77 as L                                              # noqa: E402

R = L.Report(
    selfpop="every git read and c1 run this script performs, the requirement "
            "that each of the 6 bends really change the file it names, that "
            "the baseline run print c1's 24 vertex sets, and that each of the "
            "3 inputs really be the KIND of input it is called before any row "
            "is read against it",
    findpop="the 3 rows of g1's section (v) evaluated on 4 inputs -- a "
            "cancelling pair, two conspiring pairs of different shape, and a "
            "one-sided bend that is neither -- at g1's OWN row signature and "
            "again at p3's, 24 row readings; the two claims the corrected "
            "reason makes, scored against them; g1's finding-booking block "
            "executed in both directions; and the row's argument pair "
            "compared against 4755d02")

L.banner("Q1", "THE REASON mg-69d1 WROTE, AND THE INPUTS IT NAMES")
print("""
mg-76cc shipped a row and a reason and only the row was checked.  mg-69d1
repaired the reason.  This asks the repaired reason the question that was not
asked of the original: build what it names, and see.
""")

G1_REL = L.S58DA_DIR + "/g1_provenance.py"
g1_src = L.read_worktree(G1_REL)

# ---------------------------------------------------------------------------
L.rule("(i) THE KINDS OF OUTPUT mg-69d1 EMITTED, AND WHICH ONES THIS AUDIT "
       "CHECKED")
print("""   mg-69d1's own p4 enumerates the kinds it emitted.  This is the
   same enumeration made from OUTSIDE, over `git show --stat d01ff32`
   and the diff, with a column saying where in THIS audit each kind is
   checked.  A kind with no probe against it is named as unchecked
   rather than left off the list.""")
print()
KINDS = [
    ("row", "g1's HALVES[2] -- (script, kernel) argument pair",
     "q1 (v): parsed out of 4755d02 and out of the tree and compared"),
    ("reason (docstring)", "g1's module docstring, the corrected paragraph",
     "q1 (ii)-(iv): both named inputs built and measured"),
    ("reason (stdout)", "the paragraph g1 PRINTS in section (ii)",
     "q1 (vi): parsed out of g1's own committed transcript and scored"),
    ("label", "HALVES[2][1]: `cancellation` -> `conspiracy`",
     "q1 (v): compared against 4755d02"),
    ("comment", "the comment above HALVES, and lib76cc's above HALF_BOTH_ROW",
     "q1 (v): the anchor is exercised, not read"),
    ("source anchor", "lib76cc.HALF_BOTH_ROW, in a file the repair was not "
     "about", "q1 (v): matched against the tree, count required to be 1"),
    ("error message", "r1_kernel.py's `the conspiracy case was never a check "
     "of its own`", "q1 (vi): scored against the same measurement"),
    ("classifier column", "kern5f9a's `not determined`",
     "q3 -- NOT checked here"),
    ("bound sentence", "the narrowed sentence, in 7 places",
     "q2 and q3 -- NOT checked here"),
    ("transcript", "out_g1_provenance.txt and the four out_p*.txt",
     "q1 (vi) reads g1's; the rest NOT checked here"),
    ("document", "docs/repair-mg-69d1-bound-and-reason.md",
     "q3 (iv): its census sentences are in q3's population"),
    ("commit text", "d01ff32's message",
     "q3 (iv): its census sentences are in q3's population"),
]
print("   %-20s %-46s %s" % ("kind", "the artifact", "where it is checked"))
for kind, what, where in KINDS:
    print("   %-20s %-46s %s" % (kind, what[:46], where))
print()
unchecked = [k for k, _w, wh in KINDS if "NOT checked" in wh]
print("   %d kind(s) enumerated, %d of them NOT checked in this script and "
      "named: %s" % (len(KINDS), len(unchecked), ", ".join(unchecked)))
print()

# ---------------------------------------------------------------------------
L.rule("(ii) THE FOUR INPUTS, BUILT, AND SHOWN TO BE WHAT THEY ARE CALLED")
print("""   An input characterised by the script that reads it is an input
   nobody characterised.  Each pair below is required to be the KIND of
   pair its name claims BEFORE any row rests on it, and a pair that
   fails that requirement has its rows DROPPED rather than counted as
   agreeing.""")
print()

target = L.git_show("HEAD", L.TARGET_REL)
old_c1 = L.git_show(L.REV_A218, L.C1_REL)
old_kern = L.git_show(L.REV_A218, L.KERN_REL)
head_c1 = L.git_show("HEAD", L.C1_REL)
head_kern = L.git_show("HEAD", L.KERN_REL)

INPUTS = {}
BUILDERS = [
    ("cancelling", L.bend_c1_down, L.bend_kern_up,
     "kern's dim L(n,p) one too BIG, c1's dims one too SMALL"),
    ("conspiring-A", L.conspire_a_c1, L.conspire_a_kern,
     "kern gains DIM_SHIFT_69D1=1; c1 reads it with an INTEGER default of 0"),
    ("conspiring-B", L.conspire_b_c1, L.conspire_b_kern,
     "kern gains EXTRA_VERTEX_2C77=True; c1 reads it with a BOOLEAN default "
     "of False and appends a vertex"),
    ("one-sided", None, L.lone_kern,
     "kern's dims one too big and c1 UNTOUCHED -- neither cancelling nor "
     "conspiring"),
]
for name, cf, kf, why in BUILDERS:
    try:
        c1s = cf(head_c1) if cf else head_c1
        ks = kf(head_kern) if kf else head_kern
        INPUTS[name] = (c1s, ks)
        print("   %-14s c1 %+5d byte(s), kern %+5d byte(s)   %s"
              % (name, len(c1s) - len(head_c1), len(ks) - len(head_kern), why))
    except ValueError as e:
        R.selferr("the %s input could not be built (%s); its rows are DROPPED "
                  "rather than counted as passing" % (name, e))
print()

base_out, _rc = L.run_c1(target, old_c1, old_kern)
base_lines = L.vertex_lines(base_out)
REF = (L.sha(L.measuring_half(base_out))[:16], base_lines)
ok_base = R.check(len(base_lines) == 24,
                  "the baseline run printed %d vertex sets and not the 24 c1 "
                  "prints; every comparison below would be against a parse "
                  "and not a measurement, and all rows are DROPPED"
                  % len(base_lines))
print("   the baseline -- c1 and its kernel both at %s : sha %s, %d vertex "
      "sets" % (L.REV_A218[:8], REF[0], len(base_lines)))
print()

# ---------------------------------------------------------------------------
L.rule("(iii) THE THREE ROWS, AT g1's OWN SIGNATURE AND AGAIN AT p3's")
print("""   g1 holds the un-bent file at %s.  p3 holds it at HEAD.  Both are
   run on every input, because the corrected reason is a claim about
   g1's rows and p3 is what measured it.

     g1's rows   (bent c1, %s kern) / (%s c1, bent kern) / (bent, bent)
     p3's rows   (bent c1, HEAD kern)     / (HEAD c1, bent kern)     / same
""" % (L.REV_A218[:8], L.REV_A218[:8], L.REV_A218[:8]))

ROWSETS = {
    "g1": lambda c1s, ks: [("c1 half", c1s, old_kern),
                           ("kern half", old_c1, ks),
                           ("both together", c1s, ks)],
    "p3": lambda c1s, ks: [("c1 half", c1s, head_kern),
                           ("kern half", head_c1, ks),
                           ("both together", c1s, ks)],
}
VERDICTS = {}
if ok_base:
    for name in ("cancelling", "conspiring-A", "conspiring-B", "one-sided"):
        if name not in INPUTS:
            continue
        c1s, ks = INPUTS[name]
        print("   %s" % name.upper())
        print("     %-10s %-16s %-18s %-18s %s"
              % ("rows", "row", "baseline", "measured", "verdict"))
        for which in ("g1", "p3"):
            v = {}
            for rname, rc1, rk in ROWSETS[which](c1s, ks):
                got = L.g1_verdict(target, rc1, rk, REF)
                if got["cells"] == 0:
                    R.selferr("the %s / %s / %s run printed no vertex sets; "
                              "that row is DROPPED rather than read as "
                              "IDENTICAL" % (name, which, rname))
                    continue
                v[rname] = got["same"]
                print("     %-10s %-16s %-18s %-18s %s"
                      % (which, rname, REF[0], got["sha"],
                         "IDENTICAL" if got["same"] else "MOVED"))
            VERDICTS[(name, which)] = v
        print()

    # -- each input is the kind it is called ---------------------------------
    can = VERDICTS.get(("cancelling", "g1"), {})
    R.check(can.get("c1 half") is False and can.get("kern half") is False,
            "the `cancelling` pair's halves do not both move, so it is not a "
            "pair of individually-visible changes and the rows read against "
            "it say nothing")
    for cname in ("conspiring-A", "conspiring-B"):
        con = VERDICTS.get((cname, "g1"), {})
        R.check(con.get("c1 half") is True and con.get("kern half") is True,
                "the `%s` pair's halves are not both no-ops, so it is not a "
                "conspiring pair and the rows read against it say nothing"
                % cname)

# ---------------------------------------------------------------------------
    L.rule("(iv) THE CORRECTED REASON, SCORED")
    print("""   The sentence now in g1 says two things:

     "on a CANCELLING pair both HALF rows MOVE and `both together`
      prints IDENTICAL; on a CONSPIRING pair both HALF rows print
      IDENTICAL and `both together` MOVES"

   Scored below at g1's own row signature.  The third and fourth lines
   are inputs the sentence does not name, and they are here because two
   named cases read as a partition unless something says they do not.
""")
    print("     %-14s %-12s %-12s %-14s %s"
          % ("input", "c1 half", "kern half", "both together", "caught at"))
    for name in ("cancelling", "conspiring-A", "conspiring-B", "one-sided"):
        v = VERDICTS.get((name, "g1"))
        if not v:
            continue
        caught = [k for k in v if v[k] is False]
        print("     %-14s %-12s %-12s %-14s %d of 3 rows: %s"
              % (name,
                 "IDENTICAL" if v.get("c1 half") else "MOVED",
                 "IDENTICAL" if v.get("kern half") else "MOVED",
                 "IDENTICAL" if v.get("both together") else "MOVED",
                 len(caught), ", ".join(caught) or "NONE"))
    print()

    v = VERDICTS.get(("cancelling", "g1"), {})
    R.gate(v.get("c1 half") is False and v.get("kern half") is False
           and v.get("both together") is True,
           "the corrected reason's FIRST half does not hold at g1's own rows: "
           "a cancelling pair measured c1 %s / kern %s / both together %s, "
           "and the sentence in g1 says both halves MOVE and `both together` "
           "prints IDENTICAL"
           % tuple("IDENTICAL" if v.get(k) else "MOVED"
                   for k in ("c1 half", "kern half", "both together")))
    for cname in ("conspiring-A", "conspiring-B"):
        v = VERDICTS.get((cname, "g1"), {})
        R.gate(v.get("c1 half") is True and v.get("kern half") is True
               and v.get("both together") is False,
               "the corrected reason's SECOND half does not hold at g1's own "
               "rows for the %s pair: measured c1 %s / kern %s / both "
               "together %s, and the sentence in g1 says both halves print "
               "IDENTICAL and `both together` MOVES"
               % ((cname,) + tuple("IDENTICAL" if v.get(k) else "MOVED"
                                   for k in ("c1 half", "kern half",
                                             "both together"))))

    print("   g1's ROWS AGAINST p3's ROWS, verdict by verdict.  p3's docstring "
          "says it\n   uses `the same three (script, kernel) rows g1's HALVES "
          "uses`; it holds the\n   un-bent side at HEAD where g1 holds it at "
          "%s.  If a verdict differs, the\n   corrected reason was measured "
          "against rows that are not the rows it is about." % L.REV_A218[:8])
    print()
    diffs = []
    for name in ("cancelling", "conspiring-A", "conspiring-B", "one-sided"):
        a = VERDICTS.get((name, "g1"), {})
        b = VERDICTS.get((name, "p3"), {})
        if not a or not b:
            continue
        for k in sorted(set(a) | set(b)):
            if a.get(k) != b.get(k):
                diffs.append("%s/%s" % (name, k))
        print("     %-14s g1 %s   p3 %s   %s"
              % (name,
                 "".join("I" if a.get(k) else "M"
                         for k in ("c1 half", "kern half", "both together")),
                 "".join("I" if b.get(k) else "M"
                         for k in ("c1 half", "kern half", "both together")),
                 "agree" if not [k for k in a if a.get(k) != b.get(k)]
                 else "DIFFER"))
    print()
    print("     %d of %d row readings differ between the two signatures."
          % (len(diffs), sum(len(VERDICTS.get((n, "g1"), {}))
                             for n in ("cancelling", "conspiring-A",
                                       "conspiring-B", "one-sided"))))
    R.gate(not diffs,
           "p3 measured the corrected reason at rows that are not g1's: %d "
           "verdict(s) differ (%s) between holding the un-bent file at HEAD "
           "and holding it at %s, so the reason is unmeasured at the rows it "
           "describes" % (len(diffs), ", ".join(diffs), L.REV_A218[:8]))
print()

# ---------------------------------------------------------------------------
L.rule("(v) THE ROW ITSELF, AND THE ANCHOR IN THE FILE THE REPAIR WAS NOT "
       "ABOUT")
print("""   The repair says the row's (script, kernel) pair is UNCHANGED and
   only its LABEL moved.  Both halves of that are checked by parsing
   `HALVES` out of 4755d02 and out of the tree -- as source, so a
   rewritten expression cannot pass as the same argument.""")
print()


def halves_row(src):
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "HALVES":
                    return [[ast.unparse(e) for e in el.elts]
                            for el in node.value.elts]
    raise KeyError("HALVES")


then = halves_row(L.git_show("4755d02", G1_REL))
now = halves_row(g1_src)
print("   %-10s %-56s %s" % ("", "4755d02", "the tree"))
for i in range(max(len(then), len(now))):
    a = then[i] if i < len(then) else ["--"] * 4
    b = now[i] if i < len(now) else ["--"] * 4
    print("   row %-6d %-56s %s" % (i, ", ".join(a), ", ".join(b)))
print()
R.check(len(then) == 3 and len(now) == 3,
        "HALVES is not 3 rows on both sides (%d then, %d now); the comparison "
        "below is not between the same table" % (len(then), len(now)))
if len(then) == 3 and len(now) == 3:
    R.gate(then[2][2:] == now[2][2:],
           "the `both together` row's (script, kernel) argument pair CHANGED "
           "between 4755d02 (%s) and the tree (%s); the repair says it is "
           "unchanged" % (", ".join(then[2][2:]), ", ".join(now[2][2:])))
    print("   argument pair (script, kernel) : %s"
          % ("UNCHANGED" if then[2][2:] == now[2][2:] else "CHANGED"))
    print("   label                          : %s -> %s"
          % (then[2][1], now[2][1]))
    R.gate(then[2][1] != now[2][1],
           "the row's label did not move; the repair says the label was part "
           "of the reason and named the case the row does not catch")

lib76 = L.read_worktree("code/branching_repair_76cc/lib76cc.py")
anchor_val = None
for node in ast.walk(ast.parse(lib76)):
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == "HALF_BOTH_ROW":
                anchor_val = ast.literal_eval(node.value)
print()
print("   lib76cc.HALF_BOTH_ROW -- an EXACT source anchor, in a file mg-69d1")
print("   was not about, which r1_kernel.py's deletion test splices out of "
      "g1:")
print("     %r" % anchor_val)
if anchor_val is None:
    R.selferr("HALF_BOTH_ROW could not be parsed out of lib76cc.py; the "
              "anchor check is DROPPED rather than counted as passing")
else:
    n = g1_src.count(anchor_val)
    print("     occurrences in g1_provenance.py as it stands: %d" % n)
    R.gate(n == 1,
           "the source anchor lib76cc.HALF_BOTH_ROW matches g1_provenance.py "
           "%d times and r1_kernel.py's deletion test requires exactly 1; the "
           "label rename moved an anchor in a file the repair was not about "
           "and this is the check that it landed" % n)
print()

# ---------------------------------------------------------------------------
L.rule("(vi) IS `MOVED` A CATCH?  g1's FINDING-BOOKING BLOCK, EXECUTED")
print("""   The corrected reason turns entirely on the word `catches`.  A
   printed `MOVED` is a catch only if it books a finding, and g1 exits
   0 iff FINDINGS == 0.  So g1's own block is EXECUTED here on
   synthetic input, in both directions, rather than read.""")
print()
BLOCK = """for hname, hwhat, _c1s, _ks in HALVES:
    hit = [f for f, h in moved_on if h == hname]
    if hit:
        finding("""
start = g1_src.count(BLOCK)
R.check(start == 1,
        "g1's finding-booking block was found %d times by exact match and not "
        "once; the execution below is DROPPED rather than counted as passing"
        % start)
if start == 1:
    i = g1_src.index(BLOCK)
    j = g1_src.index("\nif not moved_on:", i)
    block_src = g1_src[i:j]
    for label, moved_on in (("nothing moved", []),
                            ("`both together` moved",
                             [("the HEAD target (SET form)",
                               "both together")]),
                            ("both halves moved",
                             [("the HEAD target (SET form)",
                               "c1_branching.py"),
                              ("the HEAD target (SET form)",
                               "kern_a218.py")])):
        booked = []
        ns = {"HALVES": [("c1_branching.py", "the script", None, None),
                         ("kern_a218.py", "its kernel", None, None),
                         ("both together", "conspiracy", None, None)],
              "moved_on": moved_on,
              "finding": booked.append,
              "L": type("L", (), {"REV_A218": L.REV_A218})}
        exec(compile(block_src, "<g1 block>", "exec"), ns)
        names = [n for n in ("c1_branching.py", "kern_a218.py",
                             "both together") if any(n in b for b in booked)]
        print("     %-24s -> %d finding(s) booked, naming: %s"
              % (label, len(booked), ", ".join(names) or "nothing"))
        R.check(len(booked) == len(moved_on),
                "g1's block booked %d finding(s) for %d moved row(s) (%s); "
                "the block is not the one-finding-per-moved-row wiring the "
                "reason assumes" % (len(booked), len(moved_on), label))
    print()
    print("   a MOVED row books a finding and g1 exits 0 iff FINDINGS == 0, "
          "so `catches`\n   is a gate that was seen to fire and not a word "
          "that was read.")
print()

L.finish(R)
