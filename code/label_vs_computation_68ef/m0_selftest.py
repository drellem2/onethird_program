"""m0 -- TEN WORLDS.  Six plants that MUST be caught, three that MUST NOT move, and one
that DOES NOT BIND HERE and says so.

m1's headline is a ZERO -- no real mislabelled column anywhere in 1252 tracked `.py`.  A zero is
what a narrowed class, a broken segmenter or a matcher that never fires returns for free, so every
figure m1 prints is bounded here by a world in which it is WRONG.

THE CLEAN LIBRARY IS ASSERTED GREEN BEFORE AND AFTER EVERY PLANT AND RE-MEASURED RATHER THAN
ASSUMED: a plant that silently fails to restore turns every later world into a statement about the
previous one.
"""

import ast
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib68ef as L                                                     # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
R = L.Report("m0  TEN WORLDS FOR A HEADLINE THAT IS A ZERO -- six CAUGHT, three REQUIRED-INERT, "
             "and one that DOES NOT BIND HERE")

PRE = L.resolve(L.PRE_CORRECTION)
PIN = L.resolve(L.AS_OF)
EXH = L.show(PRE, L.EXHIBIT_B)

# --------------------------------------------------------------------------- the clean baseline

CLEAN_TABLE = '''
def f(rows):
    R.line("     n | size a+b | H | ceiling 0.9399(a+b) | note")
    R.line("    ---+----------+---+---------------------+-----")
    for n, size, h in rows:
        ceil_ = 0.9399 * size
        R.line("    %2d | %8d | %d | %19.4f | %s" % (n, size, h, ceil_, "x"))
'''


def sweep(path, src, tight=False):
    """Every DISAGREE the check finds in one source.  This is m1's inner loop, called here so
    that a world breaks the SAME code the census runs and not a re-statement of it."""
    tree = ast.parse(src)
    assigns = L.local_assignments(tree)
    out = []
    for t in L.find_tables(path, src):
        if not t.paired:
            continue
        for i, c in enumerate(t.cols):
            if not L.formula_shaped(c, tight=tight):
                continue
            v, lits, elits = L.adjudicate(c, t.args[i], assigns)
            if v == L.DISAGREE:
                out.append((t.lineno, i, c, lits, elits))
    return out


def baseline():
    """The three facts every world is measured against."""
    return (len(sweep("<clean>", CLEAN_TABLE)),
            len(sweep(L.EXHIBIT_B, EXH)),
            len([t for t in L.find_tables(L.EXHIBIT_B, EXH) if t.paired]))


BASE = baseline()
R.line()
R.line("   baseline: %d flag(s) on the clean table, %d on the real exhibit at PRE, %d paired "
       "tables in it" % BASE)
R.line()
R.verdict(BASE == (0, 0, 6),
          "D0  THE CLEAN LIBRARY IS GREEN AND THE INSTRUMENT SEES THE EXHIBIT",
          "0 flags on a correctly-labelled table, 0 on the real exhibit (its mislabel is in "
          "PROSE, which m2.1 measures), and 6 paired tables found -- a run where the last number "
          "were 0 would make every world below a statement about an empty class")


sample = [L.EXHIBIT_A, L.EXHIBIT_B, "code/control_audit_9876/a4_sweep.py"]
batch = L.show_many(PIN, sample)
R.verdict(all(batch[p] == L.show(PIN, p) for p in sample),
          "D0b THE BATCH READER AGREES WITH `git show` BYTE FOR BYTE",
          "every population above is read through `cat-file --batch` for speed, and a reader that "
          "silently truncated a blob would shrink a census without failing -- checked on %d "
          "file(s) rather than assumed" % len(sample))


def check_clean(tag):
    got = baseline()
    if got != BASE:
        raise L.Refused("the clean library did not restore after %s: %s != %s"
                        % (tag, got, BASE))


# =============================================================================================
R.banner("PLANTS THAT MUST BE CAUGHT")

# --- D1 ------------------------------------------------------------------------------------
planted = CLEAN_TABLE.replace("ceiling 0.9399(a+b)", "ceiling  (1-c)(a+b)")
hits = sweep("<planted>", planted)
R.caught(len(hits) == 1 and hits[0][3] == [1.0] and hits[0][4] == [0.9399],
          "D1  A MISLABELLED COLUMN IS CAUGHT -- label `(1-c)(a+b)`, computation `0.9399 * size`",
          "this is the world m1.3's zero is a measurement in: without it, `0 disagreements` and "
          "`a detector that cannot fire` print the same page.  Got %s" % (hits,))
check_clean("D1")

# --- D2 ------------------------------------------------------------------------------------
R.line()
R.note("D2 IS A COUNTERFACTUAL AND IS LABELLED ONE.  The ticket says `s1.6's HEADER labelled the")
R.note("per-node ceiling (1-c)(a+b)`; m2.1 measures that the header it means is the section's")
R.note("PROSE and that the column header was right at both revisions.  D2 asks the question the")
R.note("ticket's wording suggests: IF the mislabel had been in the column, would the check have")
R.note("caught it?  The exhibit is read out of the tree and ONE substitution is made on the")
R.note("column header line -- the file is never re-typed (mg-d2c2).")
before = [ln for ln, s, _ in L._string_constants(ast.parse(EXH)) if "note's ceiling" in s]
cf = EXH.replace("note's ceiling 0.9399(a+b)", "note's ceiling  (1-c)(a+b)")
if cf == EXH:
    raise L.Refused("D2 substituted nothing -- the exhibit's column header is not where it was")
hits = sweep(L.EXHIBIT_B, cf)
R.caught(len(hits) == 1 and hits[0][3] == [1.0] and hits[0][4] == [0.9399],
          "D2  AND IT WOULD HAVE BEEN CAUGHT IN THE REAL FILE, had it been in the column",
          "one substitution on line %s of the exhibit read at PRE, and the check flags exactly "
          "that column: %s" % (before, hits))
check_clean("D2")

# --- D3 ------------------------------------------------------------------------------------
R.line()
R.note("MY FIRST TWO DRAFTS OF D3 WERE WRONG AND THE CONTROL WAS FIXED RATHER THAN THE CLAIM,")
R.note("TWICE.  It asserted NUMLIT's identifier guard was load-bearing on the exhibit -- it is")
R.note("not -- and then over the corpus, and it is not there either.  D3 now measures BOTH halves")
R.note("and one of them is a recorded non-binding rather than a pass.")
R.line()

_ALL = L.show_many(PIN, L.tracked_py(PIN))
TABLE_FILES = sorted(p for p, s in _ALL.items() if "|" in s and "---+" in s)
CACHE = {p: _ALL[p] for p in TABLE_FILES}


def corpus_flags():
    n = 0
    for p, s in CACHE.items():
        try:
            n += len(sweep(p, s))
        except (SyntaxError, L.Refused):
            pass
    return n


guarded = L.label_literals("log2 n!"), L.label_literals("shape-A c = E/(n log2 n)")
broken = L.NUMLIT
L.NUMLIT = re.compile(r"\d+(?:\.\d+)?")          # no identifier guard
try:
    unguarded = L.label_literals("log2 n!"), L.label_literals("shape-A c = E/(n log2 n)")
    dirty_n = corpus_flags()
finally:
    L.NUMLIT = broken
clean_n = corpus_flags()

R.line("     label                       | with the guard | without it")
R.line("    -----------------------------+----------------+-----------")
R.line("    %-28s | %14s | %s" % ("log2 n!", guarded[0], unguarded[0]))
R.line("    %-28s | %14s | %s" % ("shape-A c = E/(n log2 n)", guarded[1], unguarded[1]))
R.line()
R.caught(guarded == ([], []) and unguarded == ([2.0], [2.0]),
          "D3  THE GUARD DOES WHAT IT CLAIMS: without it, `log2` contributes a literal 2",
          "so a label naming a base-2 logarithm would claim a `2` that its computation, which "
          "spells `math.log2(x)` and no literal, does not have")

R.line()
R.note("⚠️ AND IT DOES NOT BIND ON THIS CORPUS, WHICH IS RECORDED RATHER THAN CLAIMED AS A PASS.")
R.verdict(dirty_n == clean_n,
          "D3b  removing the guard moves the corpus figure NOT AT ALL: %d -> %d over %d "
          "table-bearing file(s)" % (clean_n, dirty_n, len(TABLE_FILES)),
          "because `log2 n!` carries NO OPERATOR and so is not formula-shaped -- the funnel's "
          "earlier stage already excludes every label the guard protects.  That is a fact about "
          "THIS corpus and not about the guard, and a directory resting on it would be reporting "
          "a quiet window as a repair")
check_clean("D3")

# --- D4 ------------------------------------------------------------------------------------
orig_shift = L._best_shift
L._best_shift = lambda rule, header, span=3: (0, 0)
try:
    ts = L.find_tables(L.EXHIBIT_B, EXH)
    stray = [t for t in ts if any(c.startswith("|") for c in t.cols)]
    R.caught(len(stray) > 0,
              "D4  FORCING shift = 0 MIS-SEGMENTS %d REAL TABLE(S) WITHOUT COMPLAINING"
              % len(stray),
              "every label in them gains a stray leading `|`, e.g. %r -- a segmenter that took "
              "the rule line's `+` columns literally would publish those as column names"
              % (stray[0].cols[1] if stray else None))
finally:
    L._best_shift = orig_shift
check_clean("D4")

# --- D5 ------------------------------------------------------------------------------------
orig_seg = L._segment
L._segment = lambda header, rule, shift: [x.strip() for x in header.split("|")]
try:
    ts = L.find_tables(L.EXHIBIT_B, EXH)
    tgt = [t for t in ts if any("note's ceiling" in c for c in t.cols)]
    R.caught(len(tgt) == 1 and not tgt[0].paired,
              "D5  NAIVE `|` SPLITTING LOSES THE EXHIBIT'S OWN TABLE ENTIRELY",
              "the header contains the delimiter inside `H(word | earlier)`, so it splits into 6 "
              "fields against the row template's 5 placeholders and the table goes UNPAIRED -- "
              "the obvious implementation is blind exactly where the class was found")
finally:
    L._segment = orig_seg
check_clean("D5")

# --- D6 ------------------------------------------------------------------------------------
orig_rank = L.claimed_rank
L.claimed_rank = lambda inner: 2
try:
    claims = L.bigo_claims(L.EXHIBIT_A, L.show(PIN, L.EXHIBIT_A))
    ranks = {L.claimed_rank(c[3]) for c in claims}
    R.caught(ranks == {2},
              "D6  A claimed_rank THAT ANSWERS FOR EVERYTHING RANKS `O(n!)` AND `O(2^n)` TOO",
              "m1.4 splits 43 claims into 33 rankable and 10 not, and a rank function with no "
              "refusal would fold the 10 in and report a proxy agreement rate over a population "
              "that includes claims the proxy cannot be about")
finally:
    L.claimed_rank = orig_rank
check_clean("D6")

# =============================================================================================
R.banner("WORLDS THAT MUST NOT MOVE -- the wrong direction")

# --- D7 ------------------------------------------------------------------------------------
R.line()
reworded = EXH.replace("R.note(\"MINIMALS reads P and NEVER reads L*.",
                       "R.note(\"MINIMALS consults P and never consults L*.")
if reworded == EXH:
    raise L.Refused("D7 found nothing to reword -- it would be asserting nothing")
a = L.find_tables(L.EXHIBIT_B, EXH)
b = L.find_tables(L.EXHIBIT_B, reworded)
R.verdict([t.cols for t in a] == [t.cols for t in b] and len(sweep(L.EXHIBIT_B, reworded)) == 0,
          "D7  REWORDING A NOTE MOVES NO TABLE, NO COLUMN AND NO VERDICT",
          "%d tables before and after -- without this the funnel would be measuring the corpus's "
          "English rather than its tables" % len(a))

# --- D8 ------------------------------------------------------------------------------------
noformula = CLEAN_TABLE.replace("ceiling 0.9399(a+b)", "ceiling in bits   ")
hits = sweep("<noformula>", noformula)
R.verdict(len(hits) == 0 and "0.9399" in noformula,
          "D8  A COLUMN WITH NO FORMULA IN ITS LABEL IS NEVER FLAGGED",
          "the computation still spells 0.9399 and the label no longer makes a claim about it, "
          "so there is nothing to disagree with.  Without this the check would be flagging every "
          "column whose heading is prose")

# --- D9 ------------------------------------------------------------------------------------
prose_only = EXH.replace("H(W_v | earlier words) <= (1-c)(a+b)",
                         "H(W_v | earlier words) <= (1-c)(a+b) at each node")
if prose_only == EXH:
    raise L.Refused("D9 found no prose formula to perturb -- it would be asserting nothing")
R.verdict(len(sweep(L.EXHIBIT_B, prose_only)) == 0,
          "D9  AND A FORMULA IN PROSE IS INVISIBLE TO IT, WHICH IS THE WHOLE FINDING",
          "the exhibit's actual defect is edited HERE, in the string the correction deleted, and "
          "the check does not move -- a column check cannot reach a sentence, and that is why "
          "m2 concludes the class is a reading problem rather than a lint")

check_clean("D9")
R.line()
R.verdict(baseline() == BASE,
          "THE CLEAN LIBRARY IS GREEN AFTER THE LAST WORLD TOO, RE-MEASURED",
          "%s -- asserted before and after every plant rather than at the end alone" % (BASE,))

sys.stdout.write(R.done(os.path.join(HERE, "out_m0_selftest.txt")))
raise SystemExit(1 if R.bad else 0)
