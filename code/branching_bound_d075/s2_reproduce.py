"""S2 -- THE PARENT'S 8/4/4, REPRODUCED AGAINST ITS OWN COMMITTED TRANSCRIPT, and
the ONE CLAUSE whose removal turns 8 into 9.

WHY THIS SCRIPT EXISTS.  s1 says the number is 9.  A disagreement with a published
figure is worth nothing until the published figure has been reproduced -- otherwise
"9, not 8" is indistinguishable from a parser bug of mine.  So this script does two
things in order:

  R1  REPRODUCTION.  My independent re-implementation of the parent's STRICT
      predicate is run on the same file, and its output is compared SITE BY SITE
      against the parent's own committed transcript
      `code/branching_audit_19ec/out_e5_population.txt`, PARSED -- not eyeballed.
      Population: the 8 `<NN>` rows of that transcript's POP-3 block.
      Grain: (line number, BOUNDED/UNBOUNDED verdict), per row.
      If this does not match exactly, the disagreement is MINE and s1's 9 is void.

  R2  THE ONE CLAUSE.  STRICT and RELAXED differ in exactly one conjunct: whether
      the string "Young-Fibonacci" must share a SENTENCE with the numeral 33 or may
      sit anywhere in the table cell / paragraph.  R2 turns that single clause off
      and reports what appears.  Nothing else is changed, so whatever appears is
      attributable to that clause and to nothing else.

  R3  THE FLOOR -- a thing no brief in this lineage names.  The liveness rule is
      applied PER CELL, and a markdown table row is many cells.  So one ledger row
      can contribute both struck cells and live cells.  R3 counts the rows of this
      document that split that way, and names them.  Site <08>/<09> (line 414) is
      one: it is the fourth cell of row B4', whose second cell opens "(the reading
      this replaces...)" -- the exact phrase the strike regex matches.

EXIT 0 if R1 reproduces the parent exactly.  PREDICTED 0.
Note the asymmetry on purpose: this script gates on AGREEING with the parent, not on
disagreeing.  s1 is where the disagreement is scored.
"""

import os
import re
import subprocess
import sys

import lib_d075 as L

OUT = sys.stdout
ITEM = "mg-d075"
RELPATH = "docs/OneThird-Branching-Graphs-Where-This-Lives.md"
PARENT = os.path.join(L.ROOT, "code", "branching_audit_19ec",
                      "out_e5_population.txt")

# THE DOCUMENT IS READ AT THE PRE-REPAIR ANCHOR, NOT AS IT STANDS.
# The first form of this script read the working tree, and once this repair had
# bounded the sites it exited 1 -- correctly, and for a reason that was entirely
# mine: mg-19ec's 8 / 4 / 4 is a measurement OF A COMMIT, not a live property of
# the file, and reproducing it against a tree that has since been repaired
# measures the repair, not the reproduction.  The anchor is derived the same way
# s3 derives it (newest commit touching the document whose subject does not name
# this work item) and is PRINTED, so the reproduction is checkable.


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=L.ROOT, capture_output=True,
                          text=True).stdout


def anchor():
    for row in git("log", "--format=%H\t%s", "--", RELPATH).strip().split("\n"):
        h, _, subj = row.partition("\t")
        if ITEM not in subj:
            return h, subj
    return None, None


def prerepair_doc():
    h, subj = anchor()
    tmp = os.path.join(L.HERE, ".prerepair_doc.md")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(git("show", "%s:%s" % (h, RELPATH)))
    return tmp, h, subj

ROW = re.compile(r"^\s*<(\d+)>\s+line\s+(\d+)\s+(para|cell)\s+(BOUNDED|UNBOUNDED)")


def parse_parent():
    """The 8 POP-3 rows of the parent's committed transcript: (n, line, kind, bnd)."""
    rows, inpop3 = [], False
    with open(PARENT, encoding="utf-8") as f:
        for line in f:
            if "POP-3" in line:
                inpop3 = True
            if inpop3 and "THE TWO POPULATIONS OVERLAP" in line:
                break
            m = ROW.match(line)
            if inpop3 and m:
                rows.append((int(m.group(1)), int(m.group(2)), m.group(3),
                             m.group(4) == "BOUNDED"))
    return rows


def parent_totals():
    """The parent's own printed population/bounded/unbounded, read from its text."""
    got = {}
    with open(PARENT, encoding="utf-8") as f:
        txt = f.read()
    blk = txt.split("POP-3", 1)[1]
    m = re.search(r"population\s*:\s*(\d+)", blk)
    got["population"] = int(m.group(1)) if m else None
    m = re.search(r"bounded\s*:\s*(\d+)", blk)
    got["bounded"] = int(m.group(1)) if m else None
    m = re.search(r"unbounded\s*:\s*(\d+)", blk)
    got["unbounded"] = int(m.group(1)) if m else None
    return got


def main():
    bad = 0
    L.rule(OUT, "S2  the parent's 8/4/4 reproduced against its own transcript,\n"
                "    and the ONE CLAUSE that turns 8 into 9.")
    print(file=OUT)
    DOC, anch, subj = prerepair_doc()
    print("  THE DOCUMENT IS READ AT THE PRE-REPAIR ANCHOR, DERIVED", file=OUT)
    print("    document : %s" % RELPATH, file=OUT)
    print("    commit   : %s" % (anch or "<none>"), file=OUT)
    print("    subject  : %s" % (subj or "")[:100], file=OUT)
    print("    mg-19ec's 8/4/4 is a measurement OF THIS COMMIT.  Reproducing it",
          file=OUT)
    print("    against the repaired working tree would measure the repair.", file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------------ R1
    L.rule(OUT, "  R1  REPRODUCTION.  Population: the 8 <NN> rows of the POP-3\n"
                "      block of code/branching_audit_19ec/out_e5_population.txt.\n"
                "      Grain: (line number, BOUNDED verdict) per row.")
    p = parse_parent()
    tot = parent_totals()
    mine = L.strict_sites(DOC)
    print("    parent transcript rows parsed : %d" % len(p), file=OUT)
    print("    parent printed population     : %s" % tot["population"], file=OUT)
    print("    parent printed bounded        : %s" % tot["bounded"], file=OUT)
    print("    parent printed unbounded      : %s" % tot["unbounded"], file=OUT)
    print("    my STRICT re-implementation   : %d sites, %d bounded, %d unbounded"
          % (len(mine), sum(1 for t in mine if t[3]),
             sum(1 for t in mine if not t[3])), file=OUT)
    print(file=OUT)

    def ck(label, ok, extra=""):
        nonlocal bad
        print("    %-56s %s%s" % (label, "ok" if ok else "BAD", extra), file=OUT)
        if not ok:
            bad += 1

    ck("parent's transcript prints 8 rows", len(p) == 8, "   (%d)" % len(p))
    ck("parent's printed population is its own row count",
       tot["population"] == len(p), "   (%s vs %d)" % (tot["population"], len(p)))
    ck("my strict count equals the parent's population",
       len(mine) == tot["population"], "   (%d vs %s)" % (len(mine), tot["population"]))
    ck("my strict bounded equals the parent's bounded",
       sum(1 for t in mine if t[3]) == tot["bounded"])
    ck("my strict unbounded equals the parent's unbounded",
       sum(1 for t in mine if not t[3]) == tot["unbounded"])
    print(file=OUT)
    print("    ROW BY ROW  (parent line/verdict  vs  mine)", file=OUT)
    for i in range(max(len(p), len(mine))):
        pl = "%4d %-9s" % (p[i][1], "BOUNDED" if p[i][3] else "UNBOUNDED") \
            if i < len(p) else "   -  -        "
        ml = "%4d %-9s" % (mine[i][0], "BOUNDED" if mine[i][3] else "UNBOUNDED") \
            if i < len(mine) else "   -  -        "
        same = (i < len(p) and i < len(mine) and p[i][1] == mine[i][0]
                and p[i][3] == mine[i][3])
        print("      <%02d>  %s   %s   %s" % (i + 1, pl, ml,
                                              "ok" if same else "BAD"), file=OUT)
        if not same:
            bad += 1
    print(file=OUT)

    # ------------------------------------------------------------------ R2
    L.rule(OUT, "  R2  THE ONE CLAUSE.  STRICT demands the naming string in the\n"
                "      SAME SENTENCE as the numeral.  Turn that conjunct off and\n"
                "      change nothing else.")
    rel = L.relaxed_sites(DOC)
    keyA = {(a, re.sub(r"\s+", " ", s)) for a, _, s, _ in mine}
    extra = [t for t in rel if (t[0], re.sub(r"\s+", " ", t[2])) not in keyA]
    print("    STRICT  : %d sites, %d bounded, %d unbounded"
          % (len(mine), sum(1 for t in mine if t[3]),
             sum(1 for t in mine if not t[3])), file=OUT)
    print("    RELAXED : %d sites, %d bounded, %d unbounded"
          % (len(rel), sum(1 for t in rel if t[3]),
             sum(1 for t in rel if not t[3])), file=OUT)
    print("    admitted by dropping the same-sentence clause: %d" % len(extra),
          file=OUT)
    print(file=OUT)
    L.show_sites(extra, OUT)
    ck("every site STRICT found is still found by RELAXED",
       all((a, re.sub(r"\s+", " ", s)) in
           {(x[0], re.sub(r"\s+", " ", x[2])) for x in rel}
           for a, _, s, _ in mine))
    ck("RELAXED admits sites and retracts none",
       len(rel) == len(mine) + len(extra), "   (%d = %d + %d)"
       % (len(rel), len(mine), len(extra)))
    print(file=OUT)
    print("    AND THE PARENT'S OWN OTHER INSTRUMENT ALREADY HAD IT.  The", file=OUT)
    print("    POP-1 block of the same transcript prints the line-307 sentence", file=OUT)
    print("    as its [09] and scores it unbounded.  Checked here by grep of", file=OUT)
    print("    the transcript, not by memory:", file=OUT)
    with open(PARENT, encoding="utf-8") as f:
        ptxt = f.read()
    pop1 = ptxt.split("POP-1", 1)[1].split("POP-2", 1)[0]
    hit = "Row 10 therefore has an index-set contact" in pop1
    ck("POP-1 of the parent's transcript contains the line-307 sentence", hit)
    print(file=OUT)
    print("    So the ninth site is not new evidence.  It is the parent's two", file=OUT)
    print("    instruments disagreeing with each other, and only the smaller", file=OUT)
    print("    number reaching the verdict.", file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------------ R3
    L.rule(OUT, "  R3  THE FLOOR -- liveness is applied PER CELL, so ONE ledger\n"
                "      row can yield both struck cells and live cells.\n"
                "      Population: every markdown table row of the document whose\n"
                "      cells (>30 chars) are not all on the same side.\n"
                "      Grain: one row.")
    with open(DOC, encoding="utf-8") as f:
        lines = f.read().split("\n")
    split_rows, fence = [], False
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if fence or not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if cells and set(cells[0]) <= set("-: "):
            continue
        big = [c for c in cells if len(c) > 30]
        if len(big) < 2:
            continue
        struck = [c for c in big if L.STRUCK.search(c)]
        live = [c for c in big if not L.STRUCK.search(c)]
        if struck and live:
            split_rows.append((i, len(big), len(struck), len(live), cells[0][:24]))
    print("    rows that split : %d" % len(split_rows), file=OUT)
    print(file=OUT)
    print("    %-6s %-26s %6s %7s %6s" % ("line", "row label", "cells",
                                          "struck", "live"), file=OUT)
    for i, nb, ns, nl, lab in split_rows:
        print("    %-6d %-26s %6d %7d %6d"
              % (i, re.sub(r"\*", "", lab), nb, ns, nl), file=OUT)
    print(file=OUT)
    b4 = [r for r in split_rows if r[0] == 414]
    ck("row B4' at line 414 splits struck/live", bool(b4))
    if b4:
        ck("at least 2 cells of row B4' are struck", b4[0][2] >= 2,
           "   (%d struck, %d live)" % (b4[0][2], b4[0][3]))
        ck("at least 1 cell of row B4' is live", b4[0][3] >= 1)
    ck("at least one OTHER row splits the same way",
       len([r for r in split_rows if r[0] != 414]) >= 1,
       "   (%d others)" % len([r for r in split_rows if r[0] != 414]))
    print(file=OUT)
    print("    ADJUDICATION.  This is not scored as a defect of the parent's", file=OUT)
    print("    census.  A ledger row that records a withdrawn reading and then", file=OUT)
    print("    states the reading that replaced it SHOULD contribute a live", file=OUT)
    print("    cell -- the replacement is a live claim.  What the per-cell rule", file=OUT)
    print("    cannot do is notice that the live cell inherits its SUBJECT from", file=OUT)
    print("    a struck cell beside it, and that is exactly the site whose", file=OUT)
    print("    figure this repair must bound.  Reported as a property of the", file=OUT)
    print("    instrument, with the count above, and not as a finding against", file=OUT)
    print("    a number.", file=OUT)
    print(file=OUT)

    os.remove(DOC)
    L.rule(OUT)
    print("SUMMARY s2_reproduce: anchor %s" % (anch or "")[:12], file=OUT)
    print("SUMMARY s2_reproduce: parent transcript rows %d; my strict %d sites, "
          "%d bounded" % (len(p), len(mine), sum(1 for t in mine if t[3])), file=OUT)
    print("SUMMARY s2_reproduce: reproduction checks failed %d" % bad, file=OUT)
    print("SUMMARY s2_reproduce: dropping the same-sentence clause admits %d site(s)"
          % len(extra), file=OUT)
    print("SUMMARY s2_reproduce: %d ledger row(s) of the document split struck/live"
          % len(split_rows), file=OUT)
    L.rule(OUT)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
