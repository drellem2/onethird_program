"""Cross-check the repair's prose against the repair's own outputs.

Narrow, and worth stating narrowly: this does NOT re-derive the mathematics.  It
checks that two documents quote this instrument correctly --

    docs/OneThird-Counterexample-Under-The-Action-Repair.md          (the repair)
    docs/OneThird-Counterexample-Under-The-Action.md                 (the repaired passages)

-- and, separately, that the sentences the repair STRUCK from the target document
appear there ONLY inside a "> **STRUCK" epitaph.

WHAT mg-0a11 FOUND, AND WHAT CHANGED HERE (mg-a893)
====================================================
The first version of this file did four things wrong, and all four are the same
mistake: IT THREW AWAY THE LOCATION OF WHAT IT WAS CHECKING.

    prose = norm(target + "\\n" + repair)
    out   = norm("\\n".join(open(f).read() for f in OUTS))

Both documents were concatenated before matching, and so were all four instrument
outputs.  So a figure was certified if it appeared ANYWHERE in EITHER document and
its printed value appeared ANYWHERE in ANY output.  mg-0a11 got 10 of 14
meaning-changing mutations past it, of which the sharpest was M1a: the headline
`1/38760` made WRONG THROUGHOUT the repair document still passed, because the
target document carries its own copy of the string.

Four properties replace it, and none of them is a longer list of substrings.

  PER DOCUMENT.   Every figure names the document it must appear in, and how many
                  times.  A figure deleted from one document is no longer covered
                  by the other one's copy.  (M1a, M11.)
  PER OUTPUT.     Every figure names the ONE output file that must have printed
                  it, so a value cannot be corroborated by an unrelated file.
  PER SECTION.    Every figure names the ATX heading path its occurrences must sit
                  under -- mg-4acd's `heading` field, borrowed.  A figure that
                  survives a section deletion by being restated elsewhere does not
                  pass.  (M7a.)
  PER TABLE ROW.  Table cells are checked against their ROW KEY, not as free
                  strings, and the row is checked against the line the instrument
                  printed.  Two cells cannot be swapped between rows and both
                  still be "present".  (M5, M6.)

Two more, on prose rather than figures:

  LIVE.           Framing, caveats and status language are named and required, in
                  a named section, outside any epitaph.  A caveat deleted while
                  the claim it qualifies stays is a failure.  (M7b, M8, M9, M10.)
  QUOTED, NOT ASSERTED.  A struck sentence may appear in the REPAIR document only
                  inside an epitaph or inside double quotation marks.  The repair
                  legitimately quotes the claims it retracts; it may not assert
                  them.  (M12.)

WHAT THIS STILL DOES NOT DO, said plainly.  It compares prose against printed
values; it does not know what either means.  A figure that was wrong when it was
certified is wrong now.  The guards at the end are a list of forbidden phrasings
and a list is a list somebody chose -- they are NOT what closes mg-0a11's battery;
the six structural properties above are.  See section 8.2 of the repair document
for the coverage boundary and for why mg-4acd's presentation-record digest is
complementary to this file rather than a replacement for it.

Run after run_all.sh.  Exit 1 on any failure.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCSDIR = os.path.join(HERE, "..", "..", "docs")
DOC_PATHS = {
    "target": os.path.join(DOCSDIR, "OneThird-Counterexample-Under-The-Action.md"),
    "repair": os.path.join(DOCSDIR, "OneThird-Counterexample-Under-The-Action-Repair.md"),
}
OUT_FILES = ("out_section4.txt", "out_theorem4.txt", "out_cycles.txt",
             "out_controls.txt", "out_cores.txt")

# (label, doc, section, needle, exact count, out file, string the instrument printed)
#
# `section` is a substring that must appear in the ATX heading path of EVERY
# occurrence of `needle` in that document; None means "anywhere in the document".
# `count` is the EXACT number of occurrences.  Exactness is the point: a deleted
# occurrence is a failure even when another one survives.
FIGURES = [
    # -- the primary measurement, in the repair -----------------------------
    ("n=8 exact p / repair", "repair", None, "1/38760", 9,
     "out_section4.txt", "1/38760"),
    ("n=8 exact p / target", "target", None, "1/38760", 4,
     "out_section4.txt", "1/38760"),
    ("n=8 p spelled out / repair", "repair", None, "1/38760 = 2.6 \u00d7 10\u207b\u2075", 1,
     "out_section4.txt", "1/38760 = 2.58e-05"),
    ("n=8 p spelled out / target", "target", None, "1/38760 = 2.6 \u00d7 10\u207b\u2075", 1,
     "out_section4.txt", "1/38760 = 2.58e-05"),
    ("n=7 exact p / repair", "repair", None, "1/286", 4,
     "out_section4.txt", "1/286"),
    ("n=7 exact p / target", "target", None, "1/286", 1,
     "out_section4.txt", "1/286"),
    ("n=6 exact p / repair", "repair", None, "1/7", 3,
     "out_section4.txt", "1/7"),
    ("n=6 exact p / target", "target", None, "1/7", 1,
     "out_section4.txt", "1/7"),
    ("n=8 group / repair", "repair", None, "6 of 20", 3,
     "out_section4.txt", "8        9    20     6       6      YES"),
    ("n=8 group / target", "target", None, "6 of 20", 2,
     "out_section4.txt", "8        9    20     6       6      YES"),
    ("n=7 group / repair", "repair", None, "3 of 13", 3,
     "out_section4.txt", "7        9    13     3       3      YES"),
    ("n=6 group / repair", "repair", None, "1 of 7", 2,
     "out_section4.txt", "6        9     7     1       1      YES"),
    ("n=8 extremal count", "repair", "9. What this does NOT show",
     "12 extremal posets at `n = 8`", 1, "out_section4.txt", "6420           12"),
    ("bonferroni 3", "repair", "3.3 What is a hypothesis", "7.7 \u00d7 10\u207b\u2075", 1,
     "out_section4.txt", "7.74e-05"),
    ("bonferroni 7", "repair", "3.3 What is a hypothesis", "1.8 \u00d7\n  10\u207b\u2074", 1,
     "out_section4.txt", "0.000181"),
    ("joint", "repair", None, "1.29 \u00d7 10\u207b\u2078", 4,
     "out_section4.txt", "1.29e-08"),
    # -- the dependence, section 3.4 ----------------------------------------
    ("honest p over the cores", "repair", "VERDICT",
     "The honest exact `p` over the cores is **`1/5`**", 1,
     "out_cores.txt", "THE HONEST EXACT p OVER THE DISTINCT CORES IS 1/5."),
    ("cut extensions measured", "repair", "3.4 THE DEPENDENCE", "257", 2,
     "out_cores.txt", "cut extensions inside the population : 257"),
    ("inheritance control fires", "repair", "3.4 THE DEPENDENCE", "1378 of 1378", 1,
     "out_cores.txt", "CHANGED, i.e. the control FIRES      : 1378"),
    ("five cores pooled", "repair", "3.4 THE DEPENDENCE",
     "The five cores, pooled over", 1,
     "out_cores.txt", "distinct cores in the whole e = 9 family, n = 5..8 : 5"),
    ("core reduction is inert elsewhere", "repair", "3.4 THE DEPENDENCE",
     "**553**", 1, "out_cores.txt", "8           691            553            138"),
    ("cut-free at n=7,8", "repair", "3.4 THE DEPENDENCE", "cut-free member", 1,
     "out_cores.txt", "7        13                   13            0"),
    ("extremal core covers", "repair", "3.4 THE DEPENDENCE",
     "0<2 1<3 1<4 2<3 2<4 3<5", 1,
     "out_cores.txt", "0<2 1<3 1<4 2<3 2<4 3<5"),
    ("nothing enters after n=6", "repair", "3.4 THE DEPENDENCE",
     "**Nothing enters the family after\n`n = 6`.**", 1,
     "out_cores.txt", "6 -> 7               13            YES"),
    # -- vacuity ------------------------------------------------------------
    ("vacuity row", "repair", "1.2 The `e = 3` group cannot fail",
     "counterexamples to V", 1, "out_section4.txt", "counterexamples to V"),
    # -- the raw table extended ---------------------------------------------
    ("raw qmass z n=8", "repair", "4. THE POWERED TEST", "+3.72", 1,
     "out_section4.txt", "z=+3.72"),
    ("raw qfrac z n=8", "repair", None, "+6.91", 2,
     "out_section4.txt", "z=+6.91"),
    ("saturation n=8", "repair", "9. What this does NOT show", "36 of 6420", 1,
     "out_section4.txt", "8          6420           36"),
    # -- Theorem 4 general --------------------------------------------------
    ("theorem4 cases", "repair", None, "972", 2,
     "out_theorem4.txt", "(poset, weight) cases: 972"),
    ("theorem4 nonuniform", "repair", None, "891", 2,
     "out_theorem4.txt", "NOT the uniform-move weight: 891"),
    ("theorem4 matrix cases", "repair", None, "228", 2,
     "out_theorem4.txt", "(poset, weight) cases: 228"),
    # -- cycles -------------------------------------------------------------
    ("n<=8 exhaustive", "repair", None, "19,440", 2,
     "out_cycles.txt", "19440 non-chain posets at n <= 8"),
    ("n=8 classes", "repair", "7. The cycle negative", "16,998", 1,
     "out_cycles.txt", "16998"),
    ("n=9 witness e", "repair", "7. The cycle negative", "1431", 1,
     "out_cycles.txt", "e(P) = 1431"),
    ("n=9 margins", "repair", "7. The cycle negative", "80/159", 1,
     "out_cycles.txt", "80/159"),
    ("n=10 e", "repair", "7. The cycle negative", "7134", 2,
     "out_cycles.txt", "e(P) = 7134"),
    ("n=11 e", "repair", "7. The cycle negative", "78474", 2,
     "out_cycles.txt", "78474"),
    # -- controls -----------------------------------------------------------
    ("lemma control", "repair", None, "2583 levels", 2,
     "out_controls.txt", "2583 levels, 0 bad"),
    ("N2 fires", "repair", None, "190 mismatches", 1,
     "out_controls.txt", "190 mismatches under the mutation"),
    ("N1 fires", "repair", "8. Controls", "34 disagreements", 1,
     "out_controls.txt", "34 disagreements under the mutation"),
    ("N3 fires", "repair", "8. Controls", "25 posets differ", 1,
     "out_controls.txt", "25 posets where the two differ"),
    ("A001035", "repair", "8. Controls", "6129859", 1,
     "out_controls.txt", "6129859"),
    ("A000112", "repair", "8. Controls", "16999", 1,
     "out_controls.txt", "16999"),
]

# (label, doc, section, row key cells, column index, expected cell, out file, out line)
#
# The row is located by its LEADING CELLS, so a value moved to another row fails
# even though the string is still somewhere in the table.
ROWS = [
    # -- section 3.1: the group table, where VACUOUS is the defect under repair
    ("group table n=8 status", "repair", "3.1 Every group containing",
     ["8", "**9**", "20", "6", "6", "2"], 6, "**non-vacuous**",
     "out_section4.txt", "8         9     20      6        6         2 non-vacuous"),
    ("group table n=7 status", "repair", "3.1 Every group containing",
     ["7", "**9**", "13", "3", "3", "2"], 6, "**non-vacuous**",
     "out_section4.txt", "7         9     13      3        3         2 non-vacuous"),
    ("group table n=6 status", "repair", "3.1 Every group containing",
     ["6", "**9**", "7", "1", "1", "2"], 6, "**non-vacuous**",
     "out_section4.txt", "6         9      7      1        1         2 non-vacuous"),
    ("group table n=8 e=3 vacuous", "repair", "3.1 Every group containing",
     ["8", "3", "6", "6", "6", "1"], 6, "*VACUOUS*",
     "out_section4.txt", "8         3      6      6        6         1    VACUOUS"),
    # -- section 1.2: Proposition V has no counterexample at any n
    ("proposition V n=8", "repair", "1.2 The `e = 3` group cannot fail",
     ["counterexamples to V"], 6, "0",
     "out_section4.txt", "8                   6                    6                    0"),
    ("proposition V n=3", "repair", "1.2 The `e = 3` group cannot fail",
     ["counterexamples to V"], 1, "0",
     "out_section4.txt", "3                   1                    1                    0"),
    # -- section 2: the population
    ("population n=8", "repair", "2. The population",
     ["8", "**16998**", "**10578**", "**0**"], 4, "**6420**",
     "out_section4.txt", "8         16998        10578            0           6420           12"),
    ("population n=8 extremal", "repair", "2. The population",
     ["8", "**16998**", "**10578**", "**0**"], 5, "**12**",
     "out_section4.txt", "8         16998        10578            0           6420           12"),
    # -- section 3.2: the test table, now carrying the core-level p
    ("test table n=8 core p", "repair", "3.2 The test",
     ["8", "9", "20", "6", "6", "**perfect**", "`1`", "**`1/38760`**", "38760", "5"],
     10, "**`1/5`**",
     "out_cores.txt", "8       20          6              5              1          1/38760            1/5"),
    ("test table n=7 core p", "repair", "3.2 The test",
     ["7", "9", "13", "3", "3", "**perfect**", "`1`", "`1/286`", "286", "5"],
     10, "**`1/5`**",
     "out_cores.txt", "7       13          3              5              1            1/286            1/5"),
    ("test table n=6 core p", "repair", "3.2 The test",
     ["6", "9", "7", "1", "1", "**perfect**", "`1`", "`1/7`", "7", "5"],
     10, "**`1/5`**",
     "out_cores.txt", "6        7          1              5              1              1/7            1/5"),
    # -- section 3.4: the dependence
    ("dependence n=7->8 identity", "repair", "3.4 THE DEPENDENCE",
     ["7 \u2192 8", "20"], 2, "**YES**",
     "out_cores.txt", "7 -> 8               20            YES                0         13 of 13"),
    ("dependence n=6->7 identity", "repair", "3.4 THE DEPENDENCE",
     ["6 \u2192 7", "13"], 2, "**YES**",
     "out_cores.txt", "6 -> 7               13            YES                0          7 of 7"),
    ("dependence n=5->6 not identity", "repair", "3.4 THE DEPENDENCE",
     ["5 \u2192 6", "4"], 2, "no",
     "out_cores.txt", "5 -> 6                4             no                3          2 of 2"),
    ("cut-free table n=8", "repair", "3.4 THE DEPENDENCE",
     ["8", "20", "**20**"], 3, "**0**",
     "out_cores.txt", "8        20                   20            0"),
    ("cut-free table n=6", "repair", "3.4 THE DEPENDENCE",
     ["6", "7", "4"], 3, "**3**",
     "out_cores.txt", "6         7                    4            3"),
    ("cores table n=8", "repair", "3.4 THE DEPENDENCE",
     ["8", "20", "6", "5", "1", "`1/38760`"], 6, "**`1/5`**",
     "out_cores.txt", "8       20          6              5              1          1/38760            1/5"),
    ("cores table n=6", "repair", "3.4 THE DEPENDENCE",
     ["6", "7", "1", "5", "1", "`1/7`"], 6, "**`1/5`**",
     "out_cores.txt", "6        7          1              5              1              1/7            1/5"),
    ("extremal core row", "repair", "3.4 THE DEPENDENCE",
     ["**6**", "**`1/3`**", "**`1`**"], 4, "`0<2 1<3 1<4 2<3 2<4 3<5`",
     "out_cores.txt", "6           1/3        1        6,7,8  0<2 1<3 1<4 2<3 2<4 3<5"),
    # -- section 4: the powered test, cell by cell against its row
    ("powered n=8 rho|e", "repair", "4. THE POWERED TEST",
     ["8", "6420", "670"], 3, "**\u22120.273**",
     "out_section4.txt", "8      6420      670      qmass      -0.2052     -16.60     0.0050     -0.273"),
    ("powered n=7 rho|e", "repair", "4. THE POWERED TEST",
     ["7", "671", "127"], 3, "**\u22120.261**",
     "out_section4.txt", "7       671      127      qmass      -0.2626      -5.65     0.0050     -0.261"),
    ("powered n=6 rho|e", "repair", "4. THE POWERED TEST",
     ["6", "88", "27"], 3, "**\u22120.287**",
     "out_section4.txt", "6        88       27      qmass      -0.2978      -1.76     0.0800     -0.287"),
    ("powered n=8 tau_b", "repair", "4. THE POWERED TEST",
     ["8", "6420", "670"], 4, "\u22120.2052",
     "out_section4.txt", "8      6420      670      qmass      -0.2052     -16.60     0.0050     -0.273"),
    ("powered n=8 z", "repair", "4. THE POWERED TEST",
     ["8", "6420", "670"], 5, "**\u221216.60**",
     "out_section4.txt", "8      6420      670      qmass      -0.2052     -16.60     0.0050     -0.273"),
    ("powered n=6 perm p", "repair", "4. THE POWERED TEST",
     ["6", "88", "27"], 6, "0.0800",
     "out_section4.txt", "6        88       27      qmass      -0.2978      -1.76     0.0800     -0.287"),
    ("powered n=8 qfrac rho|e", "repair", "4. THE POWERED TEST",
     ["8", "6420", "670"], 7, "+0.018",
     "out_section4.txt", "8      6420      670      qfrac       0.0064       0.54     0.5600      0.018"),
    ("powered n=7 qfrac rho|e", "repair", "4. THE POWERED TEST",
     ["7", "671", "127"], 7, "+0.011",
     "out_section4.txt", "7       671      127      qfrac      -0.0569      -1.29     0.1900      0.011"),
    ("powered n=6 qfrac rho|e", "repair", "4. THE POWERED TEST",
     ["6", "88", "27"], 7, "\u22120.009",
     "out_section4.txt", "6        88       27      qfrac      -0.2259      -1.53     0.1250     -0.009"),
    # -- section 5: the deflation, L* is not the argmax in general
    ("deflation n=7 argmax", "repair", "5. THE DEFLATION",
     ["7", "669", "583"], 3, "309",
     "out_section4.txt", "7           669                    583                    309"),
    ("deflation n=6 argmax", "repair", "5. THE DEFLATION",
     ["6", "88", "83"], 3, "59",
     "out_section4.txt", "6            88                     83                     59"),
]

# (label, doc, section, sentence)  -- must be present, and outside every epitaph.
LIVE = [
    # the target's replacement sentences
    ("target: n=9 is exact", "target", None,
     "The smallest `n` carrying a majority cycle is exactly 9."),
    ("target: theorem 4 general", "target", None,
     "For **any** probability weight on the `P`-compatible moves"),
    ("target: corrected verdict", "target", None,
     "Corrected verdict on the quotient side"),
    # the repair's framing, which mg-0a11's M7b/M8/M9/M10 removed silently
    ("repair: generating observations", "repair", "3.3 What is a hypothesis",
     "the generating observations, and their `p`-values are not evidence"),
    ("repair: post-hoc is a hypothesis", "repair", "3.3 What is a hypothesis",
     "found after the fact among the groups that happened to be non-vacuous is a hypothesis"),
    ("repair: pre-specification, and only that", "repair", "3.3 What is a hypothesis",
     "**What is true about `n = 8` is the PRE-SPECIFICATION, and only that.**"),
    ("repair: dependence is the problem", "repair", "3.3 What is a hypothesis",
     "Multiplicity, however, was never the problem. **Dependence is**"),
    ("repair: honest p is 1/5", "repair", "3.4 THE DEPENDENCE",
     "THE HONEST EXACT `p` OVER THE DISTINCT CORES IS `1/5`"),
    ("repair: not a retraction", "repair", "3.4 THE DEPENDENCE",
     "Read this as a correction to the strength claimed, not as a retraction of the finding."),
    ("repair: n=9 is exact", "repair", "7. The cycle negative",
     "So the smallest `n` carrying a majority cycle is exactly 9."),
    ("repair: not a filter", "repair", "9. What this does NOT show",
     "**Not a filter.**"),
    ("repair: not a filter, the figure", "repair", "9. What this does NOT show",
     "still retains 36 of 6420 posets at `n = 8`"),
    ("repair: not explained", "repair", "9. What this does NOT show",
     "**Not explained.**"),
    ("repair: not a counterexample statement", "repair", "9. What this does NOT show",
     "**Not a counterexample statement.**"),
    ("repair: dependence caveat", "repair", "9. What this does NOT show",
     "**Not three independent sizes.**"),
]

# Struck from the TARGET.  Must be PRESENT there, and every occurrence inside an
# epitaph -- the retraction has to be legible where the claim stood.
STRUCK_TARGET = [
    "tied with every other member of its group",
    "not weakly, but by an",
    "no cycle in 4200 random posets at each of `n = 8, 9, 10`",
    "rank 1 of 5 tied with 4 at `n = 7`",
]

# Struck from the REPAIR by mg-a893.  Same rule, in the repair document.
STRUCK_REPAIR = [
    "**The `n = 8` group is a pre-specified test in a new population.**",
    "PRE-SPECIFIED REPLICATION, `n = 8`, `e = 9`: 6 of 20, perfect, exact",
]

# May be absent; but wherever a struck sentence DOES appear in either document it
# must be QUOTED (inside double quotation marks) or inside an epitaph.  The repair
# quotes the claims it retracts; it must not assert them.
NEVER_ASSERTED = STRUCK_TARGET + STRUCK_REPAIR


def norm(s):
    """Unicode minus / times / non-breaking hyphen -> ASCII, for figure matching."""
    return (s.replace("−", "-").replace("–", "-").replace("—", "-")
             .replace("×", "x").replace("’", "'")
             .replace("“", '"').replace("”", '"'))


# --------------------------------------------------------------------------
# the section model: which ATX heading path is in force at each offset
# --------------------------------------------------------------------------

def heading_map(doc):
    """[(start, end, path)] over the whole document, fenced code excluded."""
    spans, stack, fence = [], [], None
    pos, seg_start, path = 0, 0, ""
    for line in doc.split("\n"):
        s = line.lstrip()
        if fence is None and (s.startswith("```") or s.startswith("~~~")):
            fence = s[:3]
        elif fence is not None and s.startswith(fence):
            fence = None
        elif fence is None and s.startswith("#"):
            h = s.lstrip("#")
            level = len(s) - len(h)
            title = h.strip()
            if 1 <= level <= 6:
                spans.append((seg_start, pos, path))
                while stack and stack[-1][0] >= level:
                    stack.pop()
                stack.append((level, title))
                path = " / ".join(t for _, t in stack)
                seg_start = pos
        pos += len(line) + 1
    spans.append((seg_start, pos, path))
    return spans


def path_at(spans, i):
    for a, b, p in spans:
        if a <= i < b:
            return p
    return ""


def occurrences(doc, needle):
    out, i = [], doc.find(needle)
    while i >= 0:
        out.append(i)
        i = doc.find(needle, i + 1)
    return out


# --------------------------------------------------------------------------
# epitaphs, and the quoted-not-asserted rule
# --------------------------------------------------------------------------

def struck_regions(doc):
    """Spans occupied by a '> **STRUCK' block quote."""
    spans, pos, start = [], 0, None
    for line in doc.split("\n"):
        s = line.lstrip()
        if start is None and s.startswith("> **STRUCK"):
            start = pos
        elif start is not None and not s.startswith(">"):
            spans.append((start, pos))
            start = None
        pos += len(line) + 1
    if start is not None:
        spans.append((start, pos))
    return spans


def inside(spans, i):
    return any(a <= i < b for a, b in spans)


def is_quoted(doc, i, j):
    """Is doc[i:j] inside a pair of double quotes on its own line?"""
    a = doc.rfind("\n", 0, i) + 1
    b = doc.find("\n", j)
    if b < 0:
        b = len(doc)
    return doc[a:i].count('"') % 2 == 1 and '"' in doc[j:b]


# --------------------------------------------------------------------------
# GFM table rows
# --------------------------------------------------------------------------

def table_rows(doc, spans, section):
    """[(cells, offset)] for every GFM table row inside `section`."""
    out, pos = [], 0
    for line in doc.split("\n"):
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            if section is None or section in path_at(spans, pos):
                out.append(([c.strip() for c in s[1:-1].split("|")], pos))
        pos += len(line) + 1
    return out


# --------------------------------------------------------------------------

def main():
    docs = {k: open(p).read() for k, p in DOC_PATHS.items()}
    ndocs = {k: norm(v) for k, v in docs.items()}
    spans = {k: heading_map(v) for k, v in ndocs.items()}
    epitaphs = {k: struck_regions(v) for k, v in ndocs.items()}
    outs = {f: norm(open(os.path.join(HERE, f)).read()) for f in OUT_FILES}

    bad = []

    print("=" * 78)
    print("CHECK 1: every figure, IN ITS DOCUMENT, IN ITS SECTION, AGAINST ONE OUTPUT")
    print("=" * 78)
    for label, doc, section, needle, count, outf, printed in FIGURES:
        d = ndocs[doc]
        hits = occurrences(d, norm(needle))
        n_ok = len(hits) == count
        s_ok = section is None or all(section in path_at(spans[doc], i) for i in hits)
        o_ok = norm(printed) in outs[outf]
        ok = n_ok and s_ok and o_ok and hits
        if not ok:
            bad.append(("figure: " + label,
                        "%s: %d occurrence(s), wanted %d%s%s"
                        % (doc, len(hits), count,
                           "" if s_ok else "; outside section %r" % section,
                           "" if o_ok else "; %s did not print %r" % (outf, printed))))
        print("  [%s] %-38s %-7s n=%d/%d sec:%s out:%s"
              % ("ok  " if ok else "FAIL", label[:38], doc, len(hits), count,
                 "yes" if s_ok else "NO ", "yes" if o_ok else "NO "))

    print()
    print("=" * 78)
    print("CHECK 2: table cells, AGAINST THEIR ROW KEY and the printed row")
    print("=" * 78)
    for label, doc, section, key, col, expect, outf, printed in ROWS:
        rows = [c for c, _ in table_rows(ndocs[doc], spans[doc], section)]
        keyn = [norm(k) for k in key]
        match = [c for c in rows if c[:len(keyn)] == keyn]
        v_ok = len(match) == 1 and len(match[0]) > col and match[0][col] == norm(expect)
        o_ok = norm(printed) in outs[outf]
        ok = v_ok and o_ok
        if not ok:
            bad.append(("row: " + label,
                        "%d row(s) with key %s%s%s"
                        % (len(match), key,
                           "" if not match or v_ok else
                           "; column %d is %r, wanted %r"
                           % (col, match[0][col] if len(match[0]) > col else None, expect),
                           "" if o_ok else "; %s did not print %r" % (outf, printed))))
        print("  [%s] %-38s %-7s row:%s cell:%s out:%s"
              % ("ok  " if ok else "FAIL", label[:38], doc,
                 "yes" if len(match) == 1 else "NO ",
                 "yes" if v_ok else "NO ", "yes" if o_ok else "NO "))

    print()
    print("=" * 78)
    print("CHECK 3: framing, caveats and status language are LIVE where they belong")
    print("=" * 78)
    for label, doc, section, sentence in LIVE:
        d = ndocs[doc]
        hits = occurrences(d, norm(sentence))
        live = [i for i in hits if not inside(epitaphs[doc], i)]
        s_ok = section is None or any(section in path_at(spans[doc], i) for i in live)
        ok = bool(live) and s_ok
        if not ok:
            bad.append(("live: " + label,
                        "%s: %d occurrence(s), %d live%s"
                        % (doc, len(hits), len(live),
                           "" if s_ok else ", none in section %r" % section)))
        print("  [%s] %-46s %-7s %s"
              % ("ok  " if ok else "FAIL", label[:46], doc,
                 "live" if ok else "MISSING, STRUCK OR MOVED"))

    print()
    print("=" * 78)
    print("CHECK 4: struck sentences are quoted ONLY inside their epitaphs")
    print("=" * 78)
    for doc, struck in (("target", STRUCK_TARGET), ("repair", STRUCK_REPAIR)):
        print("  %d '> **STRUCK' block(s) in the %s document"
              % (len(epitaphs[doc]), doc))
        for s in struck:
            hits = occurrences(ndocs[doc], norm(s))
            ok = bool(hits) and all(inside(epitaphs[doc], i) for i in hits)
            if not ok:
                bad.append(("struck: " + s[:46],
                            "%s: %s" % (doc, "ABSENT -- the retraction is not legible"
                                        if not hits else "APPEARS IN LIVE PROSE")))
            print("    [%s] %-52s %s"
                  % ("ok  " if ok else "FAIL", s[:52],
                     "quoted, and only inside an epitaph" if ok
                     else ("ABSENT" if not hits else "APPEARS IN LIVE PROSE")))

    print()
    print("=" * 78)
    print("CHECK 5: a struck claim may be QUOTED but never ASSERTED, in EITHER document")
    print("=" * 78)
    for s in NEVER_ASSERTED:
        for doc in ("target", "repair"):
            d = ndocs[doc]
            hits = occurrences(d, norm(s))
            loose = [i for i in hits
                     if not inside(epitaphs[doc], i)
                     and not is_quoted(d, i, i + len(norm(s)))]
            if loose:
                bad.append(("asserted: " + s[:40],
                            "%s: %d occurrence(s) neither quoted nor in an epitaph"
                            % (doc, len(loose))))
            if hits:
                print("    [%s] %-40s %-7s %d occurrence(s), %d asserted"
                      % ("ok  " if not loose else "FAIL", s[:40], doc,
                         len(hits), len(loose)))

    print()
    print("=" * 78)
    print("GUARDS -- a list, and therefore NOT what closes mg-0a11's battery")
    print("=" * 78)
    guards = []
    ctl = outs["out_controls.txt"]
    if "ALL CONTROLS PASS, AND ALL FOUR NEGATIVE CONTROLS FIRE." not in ctl:
        guards.append("out_controls.txt does not end clean")
    # Precise per-file failure markers.  A blanket "does the word FAIL appear"
    # test is not usable here: several of these files legitimately print the word
    # (out_section4.txt's own title is "THE GROUPS WHERE THE TEST CAN FAIL").
    for f, markers in (("out_theorem4.txt", ("   FAIL ",)),
                       ("out_cycles.txt", ("Traceback", "AssertionError")),
                       ("out_section4.txt", ("Traceback", "AssertionError")),
                       ("out_cores.txt", ("Traceback", "AssertionError")),
                       ("out_controls.txt", ("  FAIL ",))):
        for m in markers:
            if m in outs[f]:
                guards.append("%s contains %r" % (f, m))
    if "FAILURES: 0" not in outs["out_theorem4.txt"]:
        guards.append("out_theorem4.txt does not report FAILURES: 0")
    if "inheritance failures                 : 0" not in outs["out_cores.txt"]:
        guards.append("out_cores.txt does not report 0 inheritance failures")
    if "disagreements                        : 0" not in outs["out_cores.txt"]:
        guards.append("out_cores.txt does not report a well-defined core")
    repair = ndocs["repair"]
    # the conditionality discipline the target set for itself, applied to the repair
    for pat in ("the counterexample is", "counterexamples are frozen and have",
                "we have shown that no counterexample",
                "qmass = 1 detects a counterexample",
                "the extremal posets are counterexamples"):
        if pat.lower() in repair.lower():
            guards.append("repair contains an unconditional claim: %r" % pat)
    # the repair must not claim a filter or a mechanism it does not have
    for pat in ("is a filter", "explains why", "mechanism is established"):
        if pat.lower() in repair.lower():
            guards.append("repair overclaims: %r" % pat)
    # mg-0a11 acceptance 1: "NEW POPULATION" is retired.  It may be quoted in an
    # epitaph; it may not be asserted.
    for doc in ("repair", "target"):
        d = ndocs[doc]
        low = d.lower()
        for i in occurrences(low, "new population"):
            if not inside(epitaphs[doc], i) and not is_quoted(d, i, i + 14):
                guards.append("%s asserts 'new population' at offset %d" % (doc, i))
    # status drift, in the overclaiming direction
    for pat in ("established fact", "no majority cycle exists, at any",
                "confirms the separation", "independent replications",
                "three independent tests"):
        for doc in ("repair", "target"):
            d = ndocs[doc]
            for i in occurrences(d.lower(), pat):
                if not inside(epitaphs[doc], i) and not is_quoted(d, i, i + len(pat)):
                    guards.append("%s asserts %r" % (doc, pat))
    for g in guards:
        print("  [FAIL] %s" % g)
    if not guards:
        print("  all guards clean")

    print()
    if bad or guards:
        print("%d check(s) failed, %d guard(s) tripped" % (len(bad), len(guards)))
        for label, why in bad:
            print("    %-44s %s" % (label, why))
        return 1
    print("ALL %d FIGURES VERIFIED PER DOCUMENT / PER SECTION / PER OUTPUT,"
          % len(FIGURES))
    print("%d TABLE CELLS VERIFIED AGAINST THEIR ROW KEY, %d SENTENCES LIVE,"
          % (len(ROWS), len(LIVE)))
    print("%d STRUCK SENTENCES CONFINED TO THEIR EPITAPHS, %d NEVER ASSERTED,"
          % (len(STRUCK_TARGET) + len(STRUCK_REPAIR), len(NEVER_ASSERTED)))
    print("GUARDS CLEAN.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
