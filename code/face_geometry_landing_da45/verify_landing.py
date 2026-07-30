#!/usr/bin/env python3
"""mg-da45 -- re-measure every fact this landing prints, without asking
`controls.py` for any of it.

This landing closes mg-f1b2's F1: NEGATIVE CONTROL 4's row I4 kept an
absorbability condition whose PRINTED REASON was false.  `absorbable_by_
diagonal_twist` has two forced gates -- `s_i^2 = 1` pins every diagonal entry
and `|s_i s_j| = 1` pins every absolute value -- and mg-8a12 routed on the first
while printing that the second gate's verdict was a decision about signs.

So this instrument exists for one reason, and it is the reason the defect
reached a fifth generation: MG-8A12 TOOK ITS ROUTING NUMBER FROM THE AUDITOR
(mg-fcf1's `out_nc4.txt:27`) INSTEAD OF MEASURING IT.  Nothing below is taken
from mg-f1b2, from `out_gates.txt`, or from the ticket -- and nothing below
imports `controls.py`, so the corrected file cannot supply the evidence that it
is corrected.

Four targets:

  T1  WHICH GATE DECIDES, rebuilt from `face_complex` alone, for all four
      corruptions on all 86 posets with 2 <= n <= 5, plus the antichains to
      n = 6 where the row's three cited posets live.

  T2  THE ARTIFACT.  `controls_output.txt` regenerates byte-identically, the
      numbers row I4 now prints are T1's numbers, and no line of the file or of
      its source still carries the false premise.

  T3  THE CONDITION IS UNCHANGED, which is what the ticket asked for: row I4
      still scores `absorb == 0`, the routing still routes on `diag_preserved`,
      and the battery's scoring shape (0 failures, 2 [CANNOT FAIL] rows, exit 0)
      is what it was before this landing.

  T4  WHERE THE FALSE PREMISE STILL LIVES.  It is printed by mg-fcf1's own
      instrument, which this landing does not touch.  Named and counted here so
      that "corrected" is never read as "corrected everywhere".

Pure Python 3.  No third-party packages.  Runtime ~15 s.
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
FG = os.path.join(REPO, "code", "face_geometry")
FCF1 = os.path.join(REPO, "code", "face_geometry_audit_fcf1")

sys.path.insert(0, FG)

from face_complex import (                                        # noqa: E402
    linear_extensions, perm_sign, top_laplacians, at_laplacian, mat_eq,
    absorbable_by_diagonal_twist,
)
from posets import all_posets                                     # noqa: E402

RESULTS = []
MODES = [("I1", "ridge_facets"), ("I2", "split_free_as_interior"),
         ("I3", "ridge_drop"), ("I4", "facet_offbyone")]


def head(title):
    print()
    print(title)
    print("-" * len(title))


def check(name, ok, detail=""):
    """A claim THIS LANDING makes.  A false one is a failure and exits 1."""
    RESULTS.append((name, ok))
    print("  [%s] %s" % ("HOLDS " if ok else "BROKEN", name))
    if detail:
        print("        " + detail.replace("\n", "\n        "))
    return ok


def refuted(name, detail=""):
    """A claim mg-8a12 PRINTED, shown false here.  Reported, never scored."""
    print("  [REFUTED] %s" % name)
    if detail:
        print("        " + detail.replace("\n", "\n        "))


def twisted(P, incidence_mode="true"):
    """L^rel for `P` under `incidence_mode`, in the twisted basis the claim-(1)
    test compares -- rebuilt here rather than imported from controls.py."""
    td = top_laplacians(P, incidence_mode=incidence_mode)
    s = [perm_sign(w) for w in td["les"]]
    L, m = td["L_rel"], len(td["les"])
    return [[s[i] * L[i][j] * s[j] for j in range(m)] for i in range(m)]


def gate(A, B):
    """Which of the predicate's gates settles (A, B).  Written from the
    predicate's DOCSTRING, not from controls.py's copy of the same idea."""
    m = len(A)
    if m != len(B) or any(len(A[i]) != len(B[i]) for i in range(m)):
        return "shape"
    if any(A[i][i] != B[i][i] for i in range(m)):
        return "diagonal"
    if any(abs(A[i][j]) != abs(B[i][j]) for i in range(m) for j in range(m)):
        return "magnitude"
    return "parity"


# --------------------------------------------------------------------- T1
def target_1():
    head("TARGET 1 -- WHICH GATE DECIDES, rebuilt from face_complex alone")
    print("  A 'not absorbable' reached at the diagonal or the absolute-value")
    print("  gate is forced by arithmetic whatever the signs are.  Only the")
    print("  parity system is a place where a sign is consulted at all.")
    print()
    ps = [P for n in range(2, 6) for P in all_posets(n)]
    tally, tot_app, tot_parity, tot_sign = {}, 0, 0, 0
    print("  %-4s %6s %9s %10s %8s %9s %10s"
          % ("row", "bites", "diagonal", "magnitude", "parity", "absorb",
             "sign-only"))
    for tag, mode in MODES:
        app = par = mag = dia = ab = sign_entries = mag_entries = 0
        for P in ps:
            L_true, L_mut, target = twisted(P), twisted(P, mode), at_laplacian(P)[1]
            if mat_eq(L_mut, L_true):
                continue
            app += 1
            ab += absorbable_by_diagonal_twist(L_mut, target)
            g = gate(L_mut, target)
            if g == "diagonal":
                dia += 1
                continue
            m = len(L_mut)
            mag_entries += sum(1 for i in range(m) for j in range(m)
                               if abs(L_mut[i][j]) != abs(target[i][j]))
            sign_entries += sum(1 for i in range(m) for j in range(m)
                                if abs(L_mut[i][j]) == abs(target[i][j])
                                and L_mut[i][j] != target[i][j])
            mag += g == "magnitude"
            par += g == "parity"
        tally[tag] = dict(app=app, diagonal=dia, magnitude=mag, parity=par,
                          absorb=ab, sign=sign_entries, mag_entries=mag_entries)
        tot_app += app
        tot_parity += par
        tot_sign += sign_entries
        print("  %-4s %6d %9d %10d %8d %9d %10d"
              % (tag, app, dia, mag, par, ab, sign_entries))
    tally["total"] = dict(app=tot_app, parity=tot_parity, sign=tot_sign)
    print()
    check("every absorbability answer in the four scored rows is settled at a "
          "FORCED gate: %d of %d biting (poset, mutation) pairs reach the parity "
          "system" % (tot_parity, tot_app),
          tot_parity == 0 and tot_app > 0)
    check("not one entry anywhere in those rows differs in SIGN ALONE (%d), so "
          "there was no sign for the predicate to decide on" % tot_sign,
          tot_sign == 0)
    i4 = tally["I4"]
    check("row I4's diagonal survives on %d of its %d biting posets -- the count "
          "mg-8a12 routes on is right" % (i4["magnitude"] + i4["parity"], i4["app"]),
          i4["magnitude"] + i4["parity"] == 3 and i4["app"] == 61)
    refuted("'the diagonal is preserved on 3 of them, SO the predicate had to "
            "decide on the off-diagonal signs and could have returned "
            "absorbable' (mg-8a12, controls_output.txt row I4)",
            "All %d are settled at the ABSOLUTE-VALUE gate: %d off-diagonal\n"
            "magnitudes differ on them and %d entries differ in sign alone.\n"
            "The predicate returns False before a sign is read."
            % (i4["magnitude"], i4["mag_entries"], i4["sign"]))
    print()
    print("  AND IT IS FORCED AT EVERY n, not just measured to n=5.  The three")
    print("  posets are antichains; the off-by-one is prefixes_true(rot(w)) with")
    print("  rot the cyclic rotation of POSITIONS, so exactly one neighbour of")
    print("  each vertex of the adjacent-transposition graph changes:")
    per_row = []
    for n in range(3, 7):
        P = [Q for Q in all_posets(n) if not Q.less][0]
        m = len(linear_extensions(P))
        L_mut, target = twisted(P, "facet_offbyone"), at_laplacian(P)[1]
        mm = sum(1 for i in range(m) for j in range(m)
                 if abs(L_mut[i][j]) != abs(target[i][j]))
        so = sum(1 for i in range(m) for j in range(m)
                 if abs(L_mut[i][j]) == abs(target[i][j])
                 and L_mut[i][j] != target[i][j])
        per_row.append((n, m, mm, so))
        print("    n=%d  |L(P)|=%-4d magnitude mismatches=%-5d (%d per row)  "
              "sign-only=%d  absorbable=%s"
              % (n, m, mm, mm // m, so, absorbable_by_diagonal_twist(L_mut, target)))
    check("2|L(P)| magnitudes differ and 0 signs do, at n = 3, 4, 5 and 6 alike",
          all(mm == 2 * m and so == 0 for _, m, mm, so in per_row))
    return tally


# --------------------------------------------------------------------- T2
def target_2(tally):
    head("TARGET 2 -- THE ARTIFACT: it regenerates, and it now says T1's numbers")
    run = subprocess.run([sys.executable, "controls.py", "5"], cwd=FG,
                         capture_output=True, text=True)
    committed = open(os.path.join(FG, "controls_output.txt")).read()
    check("controls_output.txt regenerates byte-identically from a fresh run",
          run.stdout == committed,
          "%d bytes, exit %d" % (len(run.stdout), run.returncode))
    i4 = [l for l in committed.split("\n") if "I4 the facet enumeration" in l
          and l.strip().startswith("[")]
    check("the artifact has exactly one row I4", len(i4) == 1)
    row = i4[0] if i4 else ""
    t = tally["I4"]
    wanted = [
        "preserved on %d of the %d" % (t["magnitude"] + t["parity"], t["app"]),
        "%d are settled by |s_i s_j| = 1" % t["magnitude"],
        "%d off-diagonal magnitudes differ on them" % t["mag_entries"],
        "%d entries differ in SIGN ALONE" % t["sign"],
        "while %d reach the parity system" % t["parity"],
    ]
    for w in wanted:
        check("row I4 prints %r, and T1 measured it independently" % w, w in row)
    tot = tally["total"]
    check("the routing row prints the section total T1 measured: %r"
          % ("%d of the %d biting" % (tot["parity"], tot["app"])),
          "%d of the %d biting" % (tot["parity"], tot["app"]) in committed)
    # NOT a bare-absence test, and the first draft of this instrument was one --
    # it fired on the repair itself.  The correction QUOTES each false sentence
    # in order to name it false, which is how this arc's repairs are required to
    # land ("the false self-report is named false", mg-f1b2 on mg-8a12's C3
    # repairs).  What must not survive is an occurrence that still ASSERTS the
    # premise, so every occurrence has to sit inside a denial.
    dead = ["the off-diagonal signs actually decide",
            "had to decide on the off-diagonal signs and could have",
            "was decided on the off-diagonal signs",
            "the answer is a real decision",
            "row I4 is falsifiable"]
    marks = ["mg-f1b2", "was false", "is false", "They do not",
             "printed the opposite", "neither measured nor true", "IT IS NOT"]
    src = open(os.path.join(FG, "controls.py")).read()
    for d in dead:
        loose, seen = [], 0
        for where, text in (("controls.py", src), ("the artifact", committed)):
            start = 0
            while True:
                i = text.find(d, start)
                if i < 0:
                    break
                seen += 1
                start = i + 1
                window = text[max(0, i - 400):i + 400]
                if not any(k in window for k in marks):
                    loose.append("%s:%d" % (where, text[:i].count("\n") + 1))
        check("the false premise %r asserts nothing -- %s" % (
                  d, "it does not appear at all in controls.py or the artifact"
                  if not seen else
                  "%d occurrence(s) in controls.py + the artifact, every one of "
                  "them quoted inside a correction" % seen), not loose,
              ("STILL ASSERTED AT " + ", ".join(loose)) if loose else "")


# --------------------------------------------------------------------- T3
def target_3():
    head("TARGET 3 -- THE CONDITION IS UNCHANGED, which is what was asked for")
    print("  mg-f1b2's own remedy was to DROP `absorb == 0` from row I4.  The")
    print("  ticket that landed this deliberately did not: the count is true,")
    print("  what was false was the reason printed for scoring it.  So the")
    print("  scoring must be verifiably where it was.")
    src = open(os.path.join(FG, "controls.py")).read()
    check("row I4 still scores absorbability (`cond = cond and absorb == 0`)",
          "cond = cond and absorb == 0" in src)
    check("the forced/theorem routing still routes on the diagonal gate "
          "(`forced = (diag_preserved == 0)`)",
          "forced = (diag_preserved == 0)" in src)
    check("the routing row's condition is untouched "
          "(`0 < len(forced_rows) < len(muts)`)",
          "0 < len(forced_rows) < len(muts)" in src)
    run = subprocess.run([sys.executable, "controls.py", "5"], cwd=FG,
                         capture_output=True, text=True)
    out = run.stdout
    cf = [l for l in out.split("\n") if l.strip().startswith("[CANNOT FAIL]")]
    check("the battery still exits 0 with 0 failures", run.returncode == 0
          and "CONTROLS FAILED" not in out)
    check("still exactly 2 [CANNOT FAIL] rows, and the bottom line still denies "
          "the all-pass banner", len(cf) == 2
          and "bottom line is NOT 'all controls pass'" in out)
    nc4 = [l for l in out.split("\n")
           if l.strip().startswith("[") and " the " in l
           and any(l.strip().startswith("[PASS] " + t + " ") for t, _ in MODES)]
    check("all four NEGATIVE CONTROL 4 mutation rows are still [PASS]",
          len(nc4) == 4)


# --------------------------------------------------------------------- T4
def target_4():
    head("TARGET 4 -- WHERE THE FALSE PREMISE STILL LIVES, named not claimed")
    print("  mg-8a12 did not invent the sentence; it adopted it.  The origin is")
    print("  mg-fcf1's own audit instrument, and this landing does not touch")
    print("  another item's committed audit artifact.  So it is counted here")
    print("  rather than left for the next reader to discover.")
    origin = os.path.join(FCF1, "audit_nc4.py")
    out_nc4 = os.path.join(FCF1, "out_nc4.txt")
    phrase = "the off-diagonal signs decide"
    live = [p for p in (origin, out_nc4) if phrase in open(p).read()]
    check("mg-fcf1's instrument still prints it, on %d file(s), and this landing "
          "says so instead of claiming the repo is clean" % len(live),
          len(live) == 2,
          "\n".join(os.path.relpath(p, REPO) for p in live))
    ctl = open(os.path.join(FG, "controls.py")).read()
    check("controls.py names that origin, so the correction is followable from "
          "the file that acted on it", "out_nc4.txt:27" in ctl)


def main():
    print("mg-da45 -- CLOSING mg-f1b2's F1: THE PRINTED REASON, RE-MEASURED")
    print("=" * 78)
    print("Nothing here is inherited from mg-f1b2, from out_gates.txt or from")
    print("the ticket, and nothing here imports controls.py.  The [REFUTED] row")
    print("is mg-8a12's printed claim; the [HOLDS] rows are this landing's.")
    tally = target_1()
    target_2(tally)
    target_3()
    target_4()
    print()
    print("=" * 78)
    bad = [n for n, ok in RESULTS if not ok]
    print("%d claim(s) scored; %d BROKEN." % (len(RESULTS), len(bad)))
    for n in bad:
        print("   - " + n)
    if not bad:
        print()
        print("The condition row I4 scores is unchanged and still true; what")
        print("changed is that the file now MEASURES which gate settled it and")
        print("prints that instead of a decision that never happened.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
