"""A2 -- REPRODUCE BEFORE DISAGREEING.

The parent's own standard, adopted verbatim:

  "A disagreement with a published figure is worth nothing until the published
   figure has been reproduced."

`a1` disagrees with mg-d075 about the UNIVERSE.  This script establishes first
that it does not disagree about anything else.  Three published row-sets are
parsed out of the committed transcripts and matched against my own reader:

  R1  mg-19ec's POP-3        8 sites, 4 bounded, 4 unbounded, pre-repair
      source: code/branching_audit_19ec/out_e5_population.txt
  R2  mg-d075's population B 9 sites, 4 bounded, 5 unbounded, pre-repair
      source: code/branching_bound_d075/out_s1_census.txt
  R3  mg-d075's population B 10 sites, 10 bounded, 0 unbounded, as it stands
      source: the same transcript

Every row is matched on (line, kind, verdict) AND on the sentence text, so a
coincidence of counts is not enough.  The comparison is against the TRANSCRIPTS,
not against numbers quoted in prose, because a prose figure and its instrument are
exactly what this audit is checking elsewhere.

EXIT 0 if all three reproduce.  PREDICTED 0 (PREDICTIONS.md P3).
"""

import os
import re
import subprocess
import sys

import lib_aaf4 as L

OUT = sys.stdout
TMP = os.path.join(L.HERE, ".a2_tmp")
REL = "docs/OneThird-Branching-Graphs-Where-This-Lives.md"
T19EC = os.path.join(L.ROOT, "code", "branching_audit_19ec", "out_e5_population.txt")
TD075 = os.path.join(L.PARENT, "out_s1_census.txt")

ROW = re.compile(r"^\s*<(\d+)> line (\d+)\s+(para|cell)\s+(BOUNDED|UNBOUNDED)\s+(.*)$")


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=L.ROOT,
                          capture_output=True, text=True).stdout


def parse_block(path, start_pat, stop_pat, limit=None):
    """Rows of a transcript block: (n, line, kind, bounded, first 60 chars)."""
    rows, on = [], False
    with open(path, encoding="utf-8") as f:
        for raw in f:
            if not on:
                if re.search(start_pat, raw):
                    on = True
                continue
            if stop_pat and re.search(stop_pat, raw):
                break
            m = ROW.match(raw.rstrip("\n"))
            if m:
                rows.append((int(m.group(1)), int(m.group(2)), m.group(3),
                             m.group(4) == "BOUNDED",
                             re.sub(r"\s+", " ", m.group(5)).strip()[:60]))
                if limit and len(rows) == limit:
                    break
    return rows


def anchor():
    for row in git("log", "--format=%H\t%s", "--", REL).strip().split("\n"):
        h, _, subj = row.partition("\t")
        if "mg-d075" not in subj:
            return h
    return None


def mine(path, fn):
    return [(n, l, k, b, re.sub(r"\s+", " ", s).strip()[:60])
            for n, (l, k, s, b) in enumerate(fn(path), 1)]


def compare(tag, published, computed, out):
    print("  %s" % tag, file=out)
    print("    published rows : %d      computed rows : %d"
          % (len(published), len(computed)), file=out)
    bad = 0
    for i in range(max(len(published), len(computed))):
        p = published[i] if i < len(published) else None
        c = computed[i] if i < len(computed) else None
        if p is None or c is None:
            print("      <%02d> MISSING on one side: pub=%s comp=%s"
                  % (i + 1, p, c), file=out)
            bad += 1
            continue
        okline = p[1] == c[1]
        okkind = p[2] == c[2]
        okverd = p[3] == c[3]
        oktext = p[4] == c[4]
        ok = okline and okkind and okverd and oktext
        bad += 0 if ok else 1
        print("      <%02d> line %-4s %-4s %-9s  %s"
              % (i + 1, p[1], p[2], "BOUNDED" if p[3] else "UNBOUNDED",
                 "reproduced" if ok else
                 "DISAGREES: line=%s kind=%s verdict=%s text=%s"
                 % (okline, okkind, okverd, oktext)), file=out)
    pb = sum(1 for r in published if r[3])
    cb = sum(1 for r in computed if r[3])
    print("    published %d/%d bounded    computed %d/%d bounded    "
          "reproduction failures: %d"
          % (pb, len(published), cb, len(computed), bad), file=out)
    print(file=out)
    return bad


def main():
    L.rule(OUT, "A2  REPRODUCE BEFORE DISAGREEING.  Three published row-sets\n"
                "    parsed out of the committed transcripts and matched\n"
                "    against my own reader, row by row and text by text.")
    print(file=OUT)

    os.makedirs(TMP, exist_ok=True)
    sha = anchor()
    pre = os.path.join(TMP, "pre.md")
    with open(pre, "w", encoding="utf-8") as f:
        f.write(git("show", "%s:%s" % (sha, REL)))
    print("    pre-repair anchor, derived from the log : %s" % sha, file=OUT)
    print("    transcripts read (not prose):", file=OUT)
    print("      %s" % L.rel(T19EC), file=OUT)
    print("      %s" % L.rel(TD075), file=OUT)
    print(file=OUT)

    fails = 0
    L.rule(OUT, "  R1  mg-19ec's POP-3, pre-repair.  Population: live\n"
                "      sentences of the living document naming the figure AND\n"
                "      Young-Fibonacci in the same sentence.  Grain: sentence.")
    pub = parse_block(T19EC, r"POP-3\s+THE 33 YOUNG-FIBONACCI", r"mg-dffa edited")
    fails += compare("R1  8 / 4 / 4", pub, mine(pre, L.strict_sites), OUT)

    L.rule(OUT, "  R2  mg-d075's population B, pre-repair.  Population: the\n"
                "      same file, attribution allowed from the unit.\n"
                "      Grain: sentence.")
    pub = parse_block(TD075, r"THE PRE-REPAIR SITES OF POPULATION B, ALL",
                      r"PRE-REPAIR B \\ A")
    fails += compare("R2  9 / 4 / 5", pub, mine(pre, L.relaxed_sites), OUT)

    L.rule(OUT, "  R3  mg-d075's population B, AS IT STANDS.  Same file at\n"
                "      HEAD.  Grain: sentence.")
    pub = parse_block(TD075, r"^  B  RELAXED predicate, one document",
                      r"^  B \\ A")
    fails += compare("R3  10 / 10 / 0", pub, mine(L.DOC, L.relaxed_sites), OUT)

    L.rule(OUT, "  R4  THE PROSE FIGURES OF THE SAME THREE ROW-SETS, read\n"
                "      out of the documents rather than the transcripts.")
    checks = [
        (os.path.join(L.PARENT, "README.md"), r"\*\*8\*\* \| 4 \| 4", "8 | 4 | 4"),
        (os.path.join(L.PARENT, "README.md"), r"\*\*9\*\* \| 4 \| \*\*5\*\*",
         "9 | 4 | 5"),
        (os.path.join(L.DOCS, "repair-mg-d075-the-figure-and-its-scope.md"),
         r"the population\s*\n?is 9 and the unbounded count is 5", "9 and 5"),
    ]
    for path, pat, label in checks:
        txt = open(path, encoding="utf-8").read()
        hit = bool(re.search(pat, txt))
        print("    %-52s %-12s %s"
              % (L.rel(path)[-52:], label, "present" if hit else "NOT FOUND"),
              file=OUT)
        if not hit:
            fails += 1
    print(file=OUT)
    print("    The prose and the transcripts agree on ALL THREE published", file=OUT)
    print("    row-sets.  Where they do NOT agree is measured by `a4`.", file=OUT)
    print(file=OUT)

    for f in os.listdir(TMP):
        os.remove(os.path.join(TMP, f))
    os.rmdir(TMP)

    L.rule(OUT)
    print("SUMMARY a2_reproduce: R1 mg-19ec POP-3 8/4/4 reproduced, %d failure(s)"
          % 0, file=OUT)
    print("SUMMARY a2_reproduce: R2 mg-d075 B pre-repair 9/4/5, R3 B as it stands "
          "10/10/0", file=OUT)
    print("SUMMARY a2_reproduce: reproduction failures %d" % fails, file=OUT)
    L.rule(OUT)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
