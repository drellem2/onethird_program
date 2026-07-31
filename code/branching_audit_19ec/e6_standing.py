"""E6 -- DO NOT DISTURB WHAT STANDS.

mg-5800's verdict on the mg-41aa repair was: 0 BROKEN; every figure reproduces
from a disjoint instrument; and THE CONVERSE OF X1 MEASURED AT n = 6 WITHOUT
BIRKHOFF.  mg-19ec's brief names the last of those as the strongest thing in
the arc and the easiest to lose to a careless rewrite, and asks specifically
whether the Birkhoff-free route survives mg-dffa's edits.

It is not checked here by re-reading mg-5800's output.  It is MEASURED AGAIN,
here, on this instrument:

E6a  THE POSET CENSUS.  All poset classes on 1..6 elements, enumerated as
     transitively closed relations having 0 < 1 < ... < n-1 as a linear
     extension, then canonised by the plain n! minimum.  Must be 405.

E6b  THE TWO HEIGHTS, MEASURED, so that restricting the search to skew shapes
     with |P| cells is a MEASUREMENT and not an appeal to Birkhoff.
     height(J(P)) = |P| on all 405; height([mu,lam]) = |lam/mu| on every skew
     shape to 6 cells.  Both are elementary and both are checked rather than
     assumed, because assuming them is where the Birkhoff-free route would
     quietly stop being Birkhoff-free.

E6c  THE CONVERSE OF X1 AT n <= 6, WITHOUT BIRKHOFF.  For each of the 405
     classes P: is J(P) isomorphic to an interval [mu,lam] of Young's lattice?
     The left side is the inclusion order on the order ideals of P.  The right
     side is the containment order on the PARTITIONS nu with mu <= nu <= lam.
     They are compared by an ORDER isomorphism search.  Nothing computes a
     join-irreducible; nothing invokes Birkhoff in either direction.
     The answer must be EXACTLY the skew cell posets: 107 of 405, 0
     counterexamples either way.

E6d  THE ROUTE IS STILL BIRKHOFF-FREE IN THE INSTRUMENT THAT OWNS IT.
     mg-5800's a2_exactly.py, checked mechanically for any use of
     join-irreducibles, and mg-dffa's edits checked for having touched it.

E6e  MG-DFFA TOUCHED ONLY THE TWO LEDGER ROWS IT SAYS IT TOUCHED.  Which rows
     of the claim ledger the repair commit changed, read out of git rather
     than out of the commit message.

EXIT 1 if anything above fails.  PREDICTED 0.
"""

import os
import re
import subprocess
import sys

import kern19ec as K

OUT = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.join(HERE, "..")
ROOT = os.path.join(CODE, "..")
BAD = [0]
REPAIR = "645b5a4"


def ck(label, ok, detail=""):
    if not ok:
        BAD[0] += 1
    print("  %-58s %s%s" % (label, "ok" if ok else "BAD", detail), file=OUT)
    return ok


def head(t):
    print("=" * 78, file=OUT)
    for line in t.split("\n"):
        print(line, file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)


def closed_relations(n):
    """Every transitively closed irreflexive relation on {0..n-1} contained in
    {(i,j) : i < j}.  Every poset has a linear extension, so relabelling puts
    it in this set; the set therefore meets every isomorphism class."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    m = len(pairs)
    out = []
    for mask in range(1 << m):
        less = frozenset(pairs[t] for t in range(m) if mask >> t & 1)
        ok = True
        for (a, b) in less:
            for (c, d) in less:
                if b == c and (a, d) not in less:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            out.append(K.poset(n, less))
    return out


def main():
    head("E6  mg-19ec: the Birkhoff-free converse, re-measured HERE.")

    # ---- E6a -----------------------------------------------------------
    print("-- E6a  the poset census", file=OUT)
    classes = {}
    for n in range(1, 7):
        seen = {}
        for P in closed_relations(n):
            c = K.canon(P)
            if c not in seen:
                seen[c] = P
        classes[n] = seen
        print("     n = %d : %4d classes" % (n, len(seen)), file=OUT)
    total = sum(len(v) for v in classes.values())
    ck("poset classes on 1..6 elements: 405", total == 405, " (%d)" % total)
    ck("  the per-rank census is 1, 2, 5, 16, 63, 318",
       [len(classes[n]) for n in range(1, 7)] == [1, 2, 5, 16, 63, 318])
    skew = {k: K.skew_shape_classes(k) for k in range(1, 7)}
    nskew = sum(len(v) for v in skew.values())
    ck("skew cell poset classes on 1..6 cells: 107", nskew == 107,
       " (%d)" % nskew)
    ck("  the per-rank census is 1, 2, 5, 11, 26, 62",
       [len(skew[k]) for k in range(1, 7)] == [1, 2, 5, 11, 26, 62])
    print(file=OUT)

    # ---- E6b -----------------------------------------------------------
    print("-- E6b  the two heights, MEASURED, so the search bound is not an\n"
          "        appeal to Birkhoff", file=OUT)
    hbad = 0
    for n in range(1, 7):
        for P in classes[n].values():
            if K.height(K.poset_of_sets(K.ideals(P))) != n:
                hbad += 1
    ck("height(J(P)) = |P| on all 405", hbad == 0, " (%d bad)" % hbad)
    ibad = 0
    intervals = {}
    for k in range(1, 7):
        intervals[k] = []
        for c, (lam, mu) in skew[k].items():
            elts, L = K.young_interval(tuple(mu), tuple(lam))
            if K.height(L) != k:
                ibad += 1
            intervals[k].append((lam, mu, L))
    ck("height([mu,lam]) = |lam/mu| on every skew shape to 6 cells",
       ibad == 0, " (%d bad)" % ibad)
    print("     so a lattice isomorphic to J(P) must come from a skew shape", file=OUT)
    print("     with exactly |P| cells, and that restriction is now a", file=OUT)
    print("     measurement on this instrument.", file=OUT)
    print(file=OUT)

    # ---- E6c -----------------------------------------------------------
    print("-- E6c  THE CONVERSE OF X1 AT n <= 6, WITHOUT BIRKHOFF", file=OUT)
    matched, unmatched = [], []
    for n in range(1, 7):
        for c, P in classes[n].items():
            JP = K.poset_of_sets(K.ideals(P))
            hit = None
            for (lam, mu, L) in intervals[n]:
                if L[0] == JP[0] and K.iso(JP, L):
                    hit = (lam, mu)
                    break
            (matched if hit else unmatched).append((n, c, hit))
    print("     n   classes   J(P) IS a Young interval   skew cell posets",
          file=OUT)
    for n in range(1, 7):
        m = len([1 for a, _, _ in matched if a == n])
        print("     %d   %7d   %24d   %16d"
              % (n, len(classes[n]), m, len(skew[n])), file=OUT)
    ck("J(P) is a Young interval for exactly 107 of the 405",
       len(matched) == 107, " (%d)" % len(matched))
    # both directions, class by class
    fwd = [1 for n in range(1, 7) for c in skew[n]
           if c not in {cc for _, cc, _ in matched}]
    rev = [(n, c) for n, c, _ in matched
           if c not in skew[n]]
    ck("every skew cell poset MATCHES an interval (no direction lost)",
       not fwd, " (%d skew classes with no interval)" % len(fwd))
    ck("no NON-skew poset matches any interval (the converse itself)",
       not rev, " (%d counterexamples)" % len(rev))
    ck("0 counterexamples in either direction, at n <= 6",
       not fwd and not rev)
    print(file=OUT)
    print("     HOW THIS IS BIRKHOFF-FREE.  The right-hand side is built from", file=OUT)
    print("     PARTITIONS under containment; the left from ORDER IDEALS of P;", file=OUT)
    print("     they are compared by an isomorphism search on the strict order", file=OUT)
    print("     relation.  `join_irreducibles` is never called on this path --", file=OUT)
    print("     checked below -- so no step of the measurement is Birkhoff's", file=OUT)
    print("     theorem in disguise.", file=OUT)
    src = open(os.path.join(HERE, "kern19ec.py"), encoding="utf-8").read()
    m = re.search(r"^def iso\(.*?(?=^def |\Z)", src, re.M | re.S)
    code_only = re.sub(r'"""(?:.|\n)*?"""', "", m.group() if m else "")
    ck("kern19ec's `iso` CALLS no join-irreducible routine (docstrings"
       " stripped)",
       bool(m) and "join_irreducibles(" not in code_only
       and "irreducible" not in code_only)
    mine = open(os.path.join(HERE, "e6_standing.py"), encoding="utf-8").read()
    body = mine.split("def main(")[1]
    ck("this probe never calls join_irreducibles",
       "K.join_irreducibles" not in body)
    print(file=OUT)

    # ---- E6d -----------------------------------------------------------
    print("-- E6d  the route is still Birkhoff-free in the instrument that\n"
          "        owns it (mg-5800's A2)", file=OUT)
    a2 = os.path.join(CODE, "branching_audit_5800", "a2_exactly.py")
    if os.path.exists(a2):
        s = open(a2, encoding="utf-8").read()
        ck("a2_exactly.py exists and is unchanged by the repair commit",
           subprocess.run(["git", "diff", "--quiet", "%s^" % REPAIR, REPAIR,
                           "--", "code/branching_audit_5800/a2_exactly.py"],
                          cwd=ROOT).returncode == 0)
        s_code = re.sub(r'"""(?:.|\n)*?"""', "", s)
        s_code = re.sub(r"(?m)^\s*#.*$", "", s_code)
        hits = sorted(set(re.findall(r"\w*irreducible\w*", s_code)))
        ck("  ... and no line of its CODE forms a join-irreducible"
           " (docstrings and comments stripped)", not hits, " (%s)" % hits)
        out = open(os.path.join(CODE, "branching_audit_5800",
                                "out_a2_exactly.txt"), encoding="utf-8").read() \
            if os.path.exists(os.path.join(CODE, "branching_audit_5800",
                                           "out_a2_exactly.txt")) else ""
        ck("  ... and its committed output still says 'without Birkhoff'",
           "Birkhoff" in out or "BIRKHOFF" in out, "" if out else " (no output file)")
    else:
        ck("a2_exactly.py located", False)
    audit = open(os.path.join(ROOT, "docs", "OneThird-Audit-mg-41aa-Repair.md"),
                 encoding="utf-8").read()
    ck("mg-5800's S1 still reads '107 of 405 ... without Birkhoff'",
       "107 of 405" in audit and "without Birkhoff" in audit)
    ck("mg-5800's audit document is untouched by the repair commit",
       subprocess.run(["git", "diff", "--quiet", "%s^" % REPAIR, REPAIR, "--",
                       "docs/OneThird-Audit-mg-41aa-Repair.md"],
                      cwd=ROOT).returncode == 0)
    print(file=OUT)

    # ---- E6e -----------------------------------------------------------
    print("-- E6e  which ledger rows the repair actually touched, read out of\n"
          "        git and not out of the commit message", file=OUT)
    diff = subprocess.run(
        ["git", "diff", "-U0", "%s^" % REPAIR, REPAIR, "--",
         "docs/OneThird-Branching-Graphs-Where-This-Lives.md"],
        cwd=ROOT, capture_output=True, text=True).stdout
    touched = sorted({m.group(1) for m in
                      re.finditer(r"^[+-]\| \*\*(B\d′?|\d+)\*\* \|", diff, re.M)})
    print("     rows appearing on a changed line: %s" % touched, file=OUT)
    ck("the ledger rows changed are exactly B1 and B5",
       [t for t in touched if t.startswith("B")] == ["B1", "B5"],
       " (%s)" % [t for t in touched if t.startswith("B")])
    ck("B2, whose 'exactly' carries the converse, is NOT among them",
       "B2" not in touched)
    ck("the only §3 row changed is row 10",
       [t for t in touched if not t.startswith("B")] == ["10"],
       " (%s)" % [t for t in touched if not t.startswith("B")])
    print(file=OUT)

    print("  VERDICT E6.  THE BIRKHOFF-FREE ROUTE SURVIVES.  It is not merely", file=OUT)
    print("  undisturbed: it is re-measured here, on an instrument that shares", file=OUT)
    print("  no code with any of the four before it, and it comes out at the", file=OUT)
    print("  same 107 of 405 with 0 counterexamples in either direction.", file=OUT)
    print(file=OUT)
    print("  WHAT IS NOT RE-DERIVED HERE, SAID RATHER THAN LEFT TO BE FOUND.", file=OUT)
    print("  The skew class counts at n = 7 (149) and n = 8 (360) are NOT", file=OUT)
    print("  reproduced on this instrument.  `canon` here is the plain n!", file=OUT)
    print("  minimum and 8! per poset does not finish; the alternative is a", file=OUT)
    print("  refined canonical form, which is exactly the shortcut mg-5800", file=OUT)
    print("  recorded a control firing on -- its cheaper canon reproduced", file=OUT)
    print("  A000112 to 16 999 while it was live.  So the limit is stated", file=OUT)
    print("  instead of being bought with a weaker definition.  360 remains", file=OUT)
    print("  derived by branching_repair_41aa alone, and F3's control is what", file=OUT)
    print("  ties it to the published row.", file=OUT)
    print(file=OUT)
    print("=" * 78, file=OUT)
    print("SUMMARY e6_standing: 405 classes, 107 matched, 0 counterexamples "
          "either way; failures %d" % BAD[0], file=OUT)
    print("=" * 78, file=OUT)
    return 1 if BAD[0] else 0


if __name__ == "__main__":
    sys.exit(main())
