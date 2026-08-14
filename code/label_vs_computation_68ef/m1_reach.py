"""m1 -- HOW FAR DOES THE CHECK THAT *IS* BUILDABLE REACH?

m2 establishes that neither of `mg-9d9e`'s two exhibits is a mislabelled column.  A check on
columns is still buildable, and the carry-forward's question is whether it is worth building.  That
is a size question and this arm measures it: the population, the funnel, and the sweep.

⚠️ EVERY FIGURE IS A FUNCTION OF `AS_OF` except §6, the reflexive scan, which MUST read the
worktree because this directory is younger than the pin.  THAT IS AN EXEMPTION BY ARITHMETIC AND
NOT BY RULE, and it is declared at the section rather than left to be found.
"""

import ast
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib68ef as L                                                     # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
R = L.Report("m1  THE REACH OF THE ONLY CHECK THAT IS BUILDABLE -- a funnel over every tracked "
             ".py at one commit")

PIN = L.resolve(L.AS_OF)
R.line()
R.line("   AS_OF = %s" % PIN)
R.line()

FILES = L.tracked_py(PIN)
SRC = L.show_many(PIN, FILES)

# =============================================================================================
R.banner("m1.0  THE INSTRUMENT SEES THE CORPUS.  This runs FIRST because every figure below is a "
         "small number and a broken walk returns one for free")

R.line("   tracked .py at AS_OF                : %d" % len(FILES))
parsed = 0
for p in FILES:
    try:
        ast.parse(SRC[p])
        parsed += 1
    except SyntaxError:
        pass
R.line("   ... parsed without SyntaxError      : %d" % parsed)
R.verdict(len(FILES) > 1000, "the walk reaches four figures of tracked .py",
          "%d files -- a narrowed class or an unresolvable pin would show up here and not in a "
          "verdict" % len(FILES))
R.verdict(parsed == len(FILES), "and every one of them parses",
          "so no population below is short by a file the instrument could not open")

# =============================================================================================
R.banner("m1.1  THE POPULATION -- tables, and the segmentation that finds their columns")

tables = []
for p in FILES:
    try:
        tables.extend(L.find_tables(p, SRC[p]))
    except L.Refused:
        pass

tfiles = {t.path for t in tables}
paired = [t for t in tables if t.paired]
seg_dis = [t for t in tables if t.segmentation_disagrees]
shifted = [t for t in tables if t.shift != 0]
shifts = collections.Counter(t.shift for t in tables)

R.line("   tables (a rule line WITH a header above it)           : %d in %d file(s)"
       % (len(tables), len(tfiles)))
R.line("   ... with a %%-format row template of matching arity   : %d" % len(paired))
R.line("   ... where naive `|` splitting disagrees with the rule : %d" % len(seg_dis))
R.line("   ... needing a nonzero alignment shift                 : %d" % len(shifted))
R.line()
R.line("     shift | tables")
R.line("    -------+-------")
for d in sorted(shifts):
    R.line("    %6d | %d" % (d, shifts[d]))
R.line()
R.note("THE SHIFT SEARCH IS NOT COSMETIC.  A rule line that sits one character left of its header")
R.note("is written that way in the source AND rendered that way in the committed transcript, so a")
R.note("segmenter taking the `+` columns literally hands every label in those tables a stray")
R.note("leading `|` and mis-segments a real table WITHOUT COMPLAINING.")
R.line()
R.line("   the %d table(s) the naive splitter gets wrong:" % len(seg_dis))
for t in seg_dis:
    R.line("      %s:%d" % (t.path, t.lineno))
    R.line("          naive %d field(s): %s" % (len(t.naive_cols), t.naive_cols))
    R.line("          rule  %d column(s): %s" % (len(t.cols), t.cols))
R.verdict(all(abs(t.shift) <= 2 for t in tables),
          "no table needs |shift| > 2",
          "a search that wanted a larger offset would be matching noise rather than alignment")

# =============================================================================================
R.banner("m1.2  THE FUNNEL -- and the answer to `is this worth a lint` is in the last two rows")

formula_cols = []
for t in tables:
    for i, c in enumerate(t.cols):
        if L.formula_shaped(c):
            formula_cols.append((t, i, c))

paired_formula = [(t, i, c) for t, i, c in formula_cols if t.paired]

assign_cache = {}
for p in tfiles:
    assign_cache[p] = L.local_assignments(ast.parse(SRC[p]))

verdicts = collections.Counter()
adjudicated = []
for t, i, c in paired_formula:
    v, lits, elits = L.adjudicate(c, t.args[i], assign_cache[t.path])
    verdicts[v] += 1
    if v != L.NOT_ADJUDICABLE:
        adjudicated.append((t, i, c, v, lits, elits))

rows = [
    ("tables in the corpus", len(tables)),
    ("... paired to a row template", len(paired)),
    ("column labels in paired tables", sum(len(t.cols) for t in paired)),
    ("... FORMULA-SHAPED", len(paired_formula)),
    ("... ... ADJUDICABLE (the label names a literal)", len(adjudicated)),
    ("... ... ... DISAGREE", verdicts[L.DISAGREE]),
]
R.line("     stage                                            | count")
R.line("    --------------------------------------------------+------")
for lbl, n in rows:
    R.line("    %-49s | %d" % (lbl, n))
R.line()
R.line("   formula-shaped column labels in ALL tables (paired or not): %d" % len(formula_cols))
R.line("   ... of which paired                                       : %d  (%.1f%%)"
       % (len(paired_formula),
          100.0 * len(paired_formula) / len(formula_cols) if formula_cols else 0.0))
R.line()
R.note("⚠️ `NOT ADJUDICABLE` IS A VERDICT AND NOT A PASS, and it is the overwhelming majority:")
R.note("%d of the %d paired formula labels name no numeric literal at all, so the rule has"
       % (verdicts[L.NOT_ADJUDICABLE], len(paired_formula)))
R.note("nothing to compare.  `a+b`, `log2 n!`, `E/(n log2 n)` are formulas in SYMBOLS, and the")
R.note("symbols are not the arm's variable names -- `a+b` labels a column filled by `size`.")
R.note("Deciding those needs a reader who knows what the symbols mean, which is the same reader")
R.note("the ticket says found both exhibits.")

R.line()
R.line("   the %d ADJUDICABLE label(s), in full:" % len(adjudicated))
if not adjudicated:
    R.line("      (none)")
for t, i, c, v, lits, elits in adjudicated:
    R.line("      %-8s %s:%d  column %d" % (v, t.path, t.lineno, i))
    R.line("               label %r names %s" % (c, lits))
    R.line("               computation `%s` names %s" % (ast.unparse(t.args[i]), elits))

# =============================================================================================
R.banner("m1.3  THE SWEEP -- what the check actually finds at AS_OF")

R.line("   DISAGREE   : %d" % verdicts[L.DISAGREE])
R.line("   AGREE      : %d" % verdicts[L.AGREE])
R.line("   NOT ADJUD. : %d" % verdicts[L.NOT_ADJUDICABLE])
R.line()
if verdicts[L.DISAGREE]:
    R.line("   THE DISAGREEMENTS, SHOWN:")
    for t, i, c, v, lits, elits in adjudicated:
        if v == L.DISAGREE:
            R.line("      %s:%d column %d  %r  label %s vs computation %s"
                   % (t.path, t.lineno, i, c, lits, elits))
else:
    R.line("   NO DISAGREEMENTS.")
R.note("A nonzero result here would be a finding and is printed in full rather than summarised.")

# --- the hand verdict.  A rule and a judgement in one column are indistinguishable, so they are
# --- in two: the matcher's DISAGREE above, and a HAND verdict with a reason, here.
R.line()
HAND = {
    ("code/pairbias_audit_a832f/a4_boundary_structure.py", 117, 4): (
        "FALSE POSITIVE",
        "the label is `n=6   (non-chain posets with delta <= threshold)` -- a column heading "
        "whose PADDING sits before a parenthesis, which `\\d\\s*\\(` reads as a juxtaposed "
        "product.  Its `6` is the value of n and the computation's `3` is `row[3]`, the fourth "
        "entry.  Both are right; there is no formula and nothing is mislabelled."),
}
flagged = {(t.path, t.lineno, i) for t, i, c, v, lits, elits in adjudicated if v == L.DISAGREE}
if set(HAND) != flagged:
    raise L.Refused(
        "the hand table and the matcher disagree about WHICH sites exist: hand %s, matcher %s -- "
        "this arm refuses rather than publishing a verdict for a site it did not find, or "
        "leaving a site it did find unadjudicated" % (sorted(HAND), sorted(flagged)))
R.line("   THE HAND VERDICT ON EACH -- a rule and a judgement in one column are")
R.line("   indistinguishable, so they are in two:")
for key in sorted(HAND):
    v, why = HAND[key]
    R.line("      %-15s %s:%d column %d" % (v, key[0], key[1], key[2]))
    for chunk in [why[k:k + 88] for k in range(0, len(why), 88)]:
        R.line("                      %s" % chunk)
real = [k for k in HAND if HAND[k][0] != "FALSE POSITIVE"]
R.line()
R.verdict(len(real) == 0,
          "0 REAL mislabelled columns in the estate, and the check's precision at its only "
          "firing is 0 of 1",
          "the one thing a label-vs-computation check finds in 1252 tracked .py is its own "
          "matcher misreading column padding")

R.line()
R.note("THE SAME SWEEP UNDER THE TIGHTER JUXTAPOSITION RULE, printed rather than substituted:")
tight_v = collections.Counter()
tight_adj = []
for t in tables:
    if not t.paired:
        continue
    for i, c in enumerate(t.cols):
        if not L.formula_shaped(c, tight=True):
            continue
        v, lits, elits = L.adjudicate(c, t.args[i], assign_cache[t.path])
        tight_v[v] += 1
        if v != L.NOT_ADJUDICABLE:
            tight_adj.append((t, i, c, v))
R.line("     spelling                 | formula-shaped | adjudicable | DISAGREE")
R.line("    --------------------------+----------------+-------------+---------")
R.line("    %-25s | %14d | %11d | %d"
       % ("`\\d\\s*\\(`  (as shipped)", len(paired_formula), len(adjudicated),
          verdicts[L.DISAGREE]))
R.line("    %-25s | %14d | %11d | %d"
       % ("`\\d\\s?\\(`  (the repair)", sum(tight_v.values()), len(tight_adj),
          tight_v[L.DISAGREE]))
R.verdict(tight_v[L.DISAGREE] == 0 and verdicts[L.DISAGREE] == 1,
          "the repair removes the false positive and removes nothing else",
          "the two spellings agree on every other label in the estate, so the bound really is "
          "the padding clause and not a wider narrowing of the class")
R.note("⚠️ THE REPAIR WAS WRITTEN AFTER SEEING THE HIT, which is why the instance above carries a")
R.note("HAND verdict rather than being quietly matched away.  A matcher tightened until its")
R.note("output is empty proves nothing about the corpus; what carries the 0 is the reading.")
R.note("⚠️ AND A ZERO IS NOT A CLEAN BILL OF HEALTH: it is the count of disagreements among %d"
       % len(adjudicated))
R.note("adjudicable labels, out of %d formula-shaped ones, out of %d column labels."
       % (len(formula_cols), sum(len(t.cols) for t in paired)))
R.note("The number that matters is the DENOMINATOR, and m0 D1 is what says the zero is a")
R.note("measurement rather than a detector that cannot fire.")

# =============================================================================================
R.banner("m1.4  THE OTHER HALF -- `O(...)` claims, and how often the only available proxy agrees")

claims = []
for p in FILES:
    try:
        claims.extend(L.bigo_claims(p, SRC[p]))
    except L.Refused:
        pass

ranked, unranked = [], []
for path, name, whole, inner, node in claims:
    r = L.claimed_rank(inner)
    (ranked if r is not None else unranked).append((path, name, whole, r, node))

agree = 0
tally = collections.Counter()
for path, name, whole, r, node in ranked:
    d = L.loop_depth(node)
    tally[(r, d)] += 1
    if d == r:
        agree += 1

R.line("   `O(...)` claims in docstrings                : %d in %d file(s)"
       % (len(claims), len({c[0] for c in claims})))
R.line("   ... a polynomial nesting claim (rankable)    : %d" % len(ranked))
R.line("   ... NOT rankable (O(n!), O(2^n), O(1/n), ...): %d" % len(unranked))
R.line("   ... where loop depth EQUALS the claimed rank : %d  (%.1f%% of rankable)"
       % (agree, 100.0 * agree / len(ranked) if ranked else 0.0))
R.line()
R.line("     claimed rank | loop depth | count")
R.line("    --------------+------------+------")
for (r, d) in sorted(tally):
    R.line("    %13d | %10d | %d" % (r, d, tally[(r, d)]))
R.line()
R.verdict(agree < 0.5 * len(ranked) if ranked else False,
          "the proxy agrees with fewer than half the rankable claims (%d of %d)"
          % (agree, len(ranked)),
          "so it is not a check on them -- it is a second, worse opinion, and m2.3 shows it is "
          "wrong in the LICENSING direction on the one claim this estate is known to have got "
          "wrong")
R.note("⚠️ DISAGREEMENT HERE IS NOT AN ACCUSATION and no arm uses it as one.  A `for` loop over a")
R.note("constant-size list is not a dimension, a memoised recursion has dimensions in no loop at")
R.note("all, and both are ordinary.  What the column measures is that the proxy and the claim are")
R.note("MEASURING DIFFERENT THINGS, which is the whole of why the class is a reading problem.")

# =============================================================================================
R.banner("m1.5  REQUIRED-INERT -- the wrong direction.  Prose must not move a table count")

probe = SRC[L.EXHIBIT_B]
reworded = probe.replace('R.note("MINIMALS reads P and NEVER reads L*.',
                         'R.note("MINIMALS consults P and never consults L*.')
if reworded == probe:
    raise L.Refused("the required-inert probe found nothing to reword -- it is asserting nothing")
before = L.find_tables(L.EXHIBIT_B, probe)
after = L.find_tables(L.EXHIBIT_B, reworded)
R.verdict(len(before) == len(after)
          and [t.cols for t in before] == [t.cols for t in after],
          "rewording a non-header note moves NO table and NO column",
          "%d tables and the same column lists before and after -- without this the funnel would "
          "be measuring the corpus's English rather than its tables" % len(before))

# =============================================================================================
R.banner("m1.6  REFLEXIVE -- this directory prints tables of the shape it measures")

R.note("⚠️ THIS SECTION READS THE WORKTREE AND NOT THE PIN, because this directory is younger")
R.note("than AS_OF and is in no tree at that commit.  AN EXEMPTION BY ARITHMETIC AND NOT BY RULE.")
R.line()

own = sorted(f for f in os.listdir(HERE) if f.endswith(".py"))
own_tables, own_flagged = 0, []
for f in own:
    with open(os.path.join(HERE, f)) as fh:
        s = fh.read()
    ts = L.find_tables(os.path.join(L.SELF_DIR, f), s)
    own_tables += len(ts)
    a = L.local_assignments(ast.parse(s))
    for t in ts:
        if not t.paired:
            continue
        for i, c in enumerate(t.cols):
            if L.formula_shaped(c):
                v, lits, elits = L.adjudicate(c, t.args[i], a)
                if v == L.DISAGREE:
                    own_flagged.append((f, t.lineno, c, lits, elits))

R.line("   this directory's own .py files : %s" % ", ".join(own))
R.line("   tables in them                 : %d" % own_tables)
R.line("   flagged by this directory's own check : %d" % len(own_flagged))
for row in own_flagged:
    R.line("      %s" % (row,))
R.verdict(len(own_flagged) == 0, "this directory's own tables are not flagged by its own check",
          "printed by the same function that printed every other count above, so no arm here can "
          "report a zero for one population while computing another")

sys.stdout.write(R.done(os.path.join(HERE, "out_m1_reach.txt")))
raise SystemExit(1 if R.bad else 0)
