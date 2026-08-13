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

  T3  THE ABSORBABILITY ANSWER IS ACCOUNTED FOR, wherever the population put
      it: in a row's scored condition, or in the [CANNOT FAIL] row, never in
      neither and never in both.  It is read by PARSING controls.py by role and
      by RUNNING it and reading what it publishes -- never by string-searching
      it.  This target has frozen that file twice (mg-da45 froze the deferral,
      mg-17aa froze the post-mg-17aa state including a tautology) and is
      re-aimed at the property here (mg-686c, on mg-79ba's F2).

      Run `python3 verify_landing.py --target 3` for T3 alone: it is
      self-contained, and `demo_t3_unfrozen.py` uses that to watch it stay
      green through repairs and go red on the deletions it exists to catch.

  T4  WHERE THE FALSE PREMISE STILL LIVES.  It is printed by mg-fcf1's own
      instrument, which this landing does not touch.  Named and counted here so
      that "corrected" is never read as "corrected everywhere".

Pure Python 3.  No third-party packages.  Runtime ~15 s.
"""

import ast
import os
import re
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
    # WHICH LITERALS ROW I4 CARRIES DEPENDS ON WHETHER IT STILL SCORES
    # ABSORBABILITY, and that is read out of the row rather than assumed
    # (mg-17aa).  This list was written when it did.  mg-17aa extended the
    # [CANNOT FAIL] treatment to all four rows, so the row now prints the
    # BLOCKING SPLIT instead of the predicate's decision -- different words,
    # THE SAME numbers, and both derived from T1's own independent sweep, which
    # is the property this check was built to have.  Hardcoding the old list
    # would freeze a landing's scope into a live runner; hardcoding the new one
    # would erase that mg-da45 deliberately kept the clause.  Reading the row
    # does neither.
    dp = t["magnitude"] + t["parity"]            # diagonal-preserved, from T1
    if "row DOES score it" in row:
        wanted = [
            "preserved on %d of the %d" % (dp, t["app"]),
            "%d are settled by |s_i s_j| = 1" % t["magnitude"],
            "%d off-diagonal magnitudes differ on them" % t["mag_entries"],
            "%d entries differ in SIGN ALONE" % t["sign"],
            "while %d reach the parity system" % t["parity"],
        ]
    else:
        wanted = [
            "Absorbability is NOT scored in this row",
            "(%d on the diagonal, %d on an off-diagonal magnitude with the "
            "diagonal intact, %d on shape)" % (t["app"] - dp, dp, 0),
        ]
    print("  row I4 %s absorbability, so the literals checked are the %s set"
          % ("SCORES" if "row DOES score it" in row else "does NOT score",
             "mg-da45" if "row DOES score it" in row else "mg-17aa"))
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
#
# READING controls.py BY ROLE, NEVER BY LITERAL (mg-686c).
#
# Every helper below exists so that TARGET 3 can ask a question about what
# `controls.py` DOES without ever asking what it SAYS.  Nothing here matches a
# name, a spelling or a byte of that file: each site is reached by following a
# role -- "the row emitted with the [CANNOT FAIL] label", "the branch whose
# tallies that row is scored on", "the function that branch's own decision is
# passed to".  A rename, a reworded conjunct, a third forced gate or a
# differently spelled scored condition all leave these resolutions intact,
# which is precisely what the three frozen literals they replace did not.

def _fn_of(tree, node):
    """The innermost FunctionDef of `tree` that contains `node`."""
    best, best_n = None, None
    for fn in ast.walk(tree):
        if isinstance(fn, ast.FunctionDef):
            body = list(ast.walk(fn))
            if any(n is node for n in body) and (best_n is None or len(body) < best_n):
                best, best_n = fn, len(body)
    return best


def _assigned_in(fn):
    """name -> every expression its value depends on inside `fn`: what is
    assigned to it, AND the tests of the branches deciding whether that
    assignment happens.

    THE GUARDS ARE NOT OPTIONAL, and leaving them out is how the first draft of
    this helper got the wrong answer: a tally written `blocked += 1` under `if
    gate_violations(...)` has a literal 1 on its right-hand side, so a reading
    that follows values alone calls every counter in this file a written-in
    constant.  What the counter depends on is the gate.
    """
    out = {}

    def rec(stmts, guards):
        for s in stmts:
            if isinstance(s, ast.Assign):
                tgts, val = s.targets, s.value
            elif isinstance(s, ast.AugAssign):
                tgts, val = [s.target], s.value
            elif isinstance(s, ast.For):
                tgts, val = [s.target], s.iter
            else:
                tgts, val = [], None
            for t in tgts:
                for nm in ast.walk(t):
                    if isinstance(nm, ast.Name):
                        out.setdefault(nm.id, []).extend([val] + guards)
            inner = guards + ([s.test] if isinstance(s, (ast.If, ast.While)) else [])
            for fld in ("body", "orelse", "finalbody"):
                if getattr(s, fld, None):
                    rec(getattr(s, fld), inner)
            for h in getattr(s, "handlers", []):
                rec(h.body, guards)

    rec(fn.body, [])
    return out


def _closure(fn, expr, depth=8):
    """Every name `expr` transitively depends on inside `fn`, and every call
    reached on the way.  This is how "is this value COMPUTED, or written in?"
    is asked without naming any of the names that currently compute it."""
    asg, seen, calls = _assigned_in(fn), set(), []
    frontier = {n.id for n in ast.walk(expr) if isinstance(n, ast.Name)}
    for _ in range(depth):
        nxt = set()
        for nm in sorted(frontier - seen):
            seen.add(nm)
            for val in asg.get(nm, []):
                for sub in ast.walk(val):
                    if isinstance(sub, ast.Call):
                        calls.append(sub)
                    elif isinstance(sub, ast.Name):
                        nxt.add(sub.id)
        frontier = nxt - seen
        if not frontier:
            break
    return seen, calls


def _callee(call):
    f = call.func
    return f.id if isinstance(f, ast.Name) else getattr(f, "attr", None)


def _aug_targets(node):
    return {a.target.id for a in ast.walk(node)
            if isinstance(a, ast.AugAssign) and isinstance(a.target, ast.Name)}


def _names(node):
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}


def resolve_theorem_site(tree):
    """The four NEGATIVE CONTROL 4 sites TARGET 3 is about, reached by role.

    Returns (row_call, condition, branch, builder_fn) or None -- and None is
    itself a finding: it means the shape this target checks is no longer
    resolvable and a human has to re-aim it, which is a louder and more useful
    failure than a substring quietly going missing.
    """
    for call in ast.walk(tree):
        if not isinstance(call, ast.Call):
            continue
        # (1) THE ROW, by its label and not by the emitter's name: the only
        #     thing asked of it is that it is published as one that cannot fail.
        if not any(kw.arg == "cannot_fail" and isinstance(kw.value, ast.Constant)
                   and kw.value.value is True for kw in call.keywords):
            continue
        fn = _fn_of(tree, call)
        if fn is None:
            continue
        for cond in call.args[1:]:
            names, _ = _closure(fn, cond)
            # (2) THE BRANCH, by the tallies: the `if` in the same function
            #     under which the quantities this row is scored on accumulate.
            for br in [n for n in ast.walk(fn) if isinstance(n, ast.If)]:
                if not (set().union(*[_aug_targets(s) for s in br.body]
                                    or [set()]) & names):
                    continue
                # (3) THE BUILDER, by the decision: whatever function that same
                #     branch's decision is handed to in order to build a row's
                #     conjuncts.
                builder = None
                for n in ast.walk(fn):
                    if (isinstance(n, ast.Assign) and isinstance(n.value, ast.Call)
                            and _names(br.test) & {a.id for a in n.value.args
                                                   if isinstance(a, ast.Name)}):
                        name = _callee(n.value)
                        for g in ast.walk(tree):
                            if isinstance(g, ast.FunctionDef) and g.name == name:
                                builder = g
                return call, cond, br, builder
    return None


ROW_COND = re.compile(r"\b(I\d+) = ((?:[^;.\n]*?\[[A-Z ]+\])"
                      r"(?: AND [^;.\n]*?\[[A-Z ]+\])*)")
ROW_CLAIM = re.compile(r"\b(I\d+) on (\d+)/(\d+)\b")


def target_3():
    head("TARGET 3 -- THE ABSORBABILITY ANSWER IS ACCOUNTED FOR, WHEREVER THE "
         "POPULATION PUT IT")
    print("  mg-f1b2's own remedy was to DROP `absorb == 0` from row I4.  The")
    print("  ticket that landed this deliberately did not: the count is true,")
    print("  what was false was the reason printed for scoring it.  That")
    print("  remains the record of mg-da45's scope and is not withdrawn.")
    print()
    print("  THIS TARGET HAS NOW FROZEN THE FILE TWICE AND IS UNFROZEN HERE")
    print("  (mg-686c, on mg-79ba's F2).  It first scored three SOURCE LITERALS")
    print("  of the PRE-mg-17aa state -- `cond = cond and absorb == 0`,")
    print("  `forced = (diag_preserved == 0)` and the routing row's condition --")
    print("  i.e. it froze the DEFERRAL, so it necessarily went red the day the")
    print("  deferred item landed.  mg-17aa diagnosed that correctly and then")
    print("  replaced them with three source literals OF THE POST-mg-17aa")
    print("  STATE, one of which -- `theorem_absorb == 0 and theorem_blocked ==")
    print("  theorem_app` -- was a verbatim freeze of a conjunct mg-79ba then")
    print("  showed to be a TAUTOLOGY.  So this file refused the repair of a")
    print("  defect it had frozen: mg-79ba applied three different spellings of")
    print("  the minimal fix and all three left the battery green at exit 0 and")
    print("  took this file to exit 1.  The freeze, not the wording, was what")
    print("  blocked -- and a second literal froze the routing quantity, so the")
    print("  same widening mg-17aa itself performed would have broken it too.")
    print()
    print("  THE GENERAL FORM, which is why the repair is a re-aiming and not a")
    print("  new pair of literals: A CONTROL KEYED ON SOURCE LITERALS FREEZES")
    print("  THE STATE IT WAS WRITTEN AGAINST, INCLUDING THAT STATE'S DEFECTS,")
    print("  AND THEN REFUSES THEIR REPAIR.  Where a control has to be stable,")
    print("  key it on the property, not on the bytes that currently express it.")
    print()
    print("  WHAT IS STILL BEING GUARDED is unchanged and is what the literals")
    print("  were for: the clause cannot be dropped SILENTLY.  A deletion by")
    print("  hand and a removal decided by the population are different acts and")
    print("  only the second is licensed.  So controls.py is now read in exactly")
    print("  two ways -- PARSED (ast, by role) and RUN (its own printed output)")
    print("  -- and never string-searched.  Each row below carries the class of")
    print("  its own scored condition, by the same standard the section it")
    print("  watches applies to its rows.")

    ctree = ast.parse(open(os.path.join(FG, "controls.py")).read())
    run = subprocess.run([sys.executable, "controls.py", "5"], cwd=FG,
                         capture_output=True, text=True)
    out = run.stdout

    # --- what the battery PUBLISHES about itself ------------------------
    conds = dict(ROW_COND.findall(out))
    cf = [l for l in out.split("\n") if l.strip().startswith("[CANNOT FAIL]")]
    theorem = [l for l in cf if ROW_CLAIM.search(l)]
    claims = ROW_CLAIM.findall(theorem[0]) if theorem else []
    check("[CONTINGENT] the battery PUBLISHES the decomposition this target "
          "reads: one scored condition per NEGATIVE CONTROL 4 row, conjunct by "
          "conjunct with each conjunct's class, and a [CANNOT FAIL] row "
          "carrying the rows whose answer it holds (%d row(s) decomposed, %d "
          "row(s) claimed by the theorem row)" % (len(conds), len(claims)),
          len(conds) == len(MODES) and len(claims) == len(conds),
          "; ".join("%s = %s" % (t, c) for t, c in sorted(conds.items())))
    carried = {t for t, _, _ in claims}
    scored = {t for t, c in conds.items() if "absorb" in c.lower()}
    print()
    print("  ACCOUNTED FOR: scored in the row = %s; carried by the theorem row "
          "= %s" % (", ".join(sorted(scored)) or "none",
                    ", ".join(sorted(carried)) or "none"))
    check("[FORCED ON THIS POPULATION, reported and NOT counted as this "
          "target's evidence] every row's absorbability answer is accounted "
          "for in exactly one of the two places -- never in neither (a silent "
          "deletion) and never in both (counted twice).  It is FORCED because "
          "on this population all %d rows route to the theorem row, and one "
          "variable decides both publications; what would make it contingent "
          "is a population with a pair that clears both forced gates, which "
          "mg-79ba's a2 runs and this landing does not stage"
          % len(conds),
          all((t in scored) != (t in carried) for t in conds))
    check("[CONTINGENT] and the theorem row's per-row claim is `absorbable on "
          "0 of them` for every row it carries, read out of its own published "
          "counts rather than out of its prose (%s)"
          % ", ".join("%s %s/%s" % c for c in claims),
          bool(claims) and all(a == b for _, a, b in claims))

    # --- what the battery IS, parsed by role ----------------------------
    site = resolve_theorem_site(ctree)
    check("[CONTINGENT] the four sites this target is about are RESOLVABLE BY "
          "ROLE in controls.py -- the row published as one that cannot fail, "
          "the expression it is scored on, the branch under which that "
          "expression's tallies accumulate, and the function that branch's own "
          "decision is handed to", site is not None,
          "" if site else "UNRESOLVABLE -- the shape moved and this target must "
                          "be re-aimed by hand, which is the loud failure a "
                          "substring test does not give you")
    if site:
        _, cond, branch, builder = site
        section = _fn_of(ctree, branch)
        names, calls = _closure(section, branch.test)
        check("[CONTINGENT] WHICH rows the theorem row carries is COMPUTED FROM "
              "THE POPULATION, not written in: the branch's test is not a "
              "constant and depends on %d name(s) reached through %d call(s) "
              "into the sweep, so a corruption some pair of which can be "
              "absorbed puts the clause back with no edit here -- and widening "
              "the routing to a third forced gate, or renaming any of these, "
              "leaves this row green"
              % (len(names), len(calls)),
              not isinstance(branch.test, ast.Constant)
              and len(calls) >= 1 and len(names) >= 2,
              "line %d, depends on: %s" % (branch.test.lineno,
                                           ", ".join(sorted(names))))
        cnames, _ = _closure(section, cond)
        tallies = set().union(*[_aug_targets(s) for s in branch.body] or [set()])
        check("[CONTINGENT] and the theorem row is SCORED on that population "
              "too: its condition is not a constant and reads %d of the %d "
              "quantities accumulated under that branch, so it FAILS -- it does "
              "not merely misreport -- if what it asserts stops being true"
              % (len(cnames & tallies), len(tallies)),
              not isinstance(cond, ast.Constant) and bool(cnames & tallies),
              "line %d, scored on: %s" % (cond.lineno,
                                          ", ".join(sorted(cnames & tallies))))
        params = {a.arg for a in builder.args.args} if builder else set()
        conditional = False
        if builder:
            for br in [n for n in ast.walk(builder) if isinstance(n, ast.If)]:
                if not (_names(br.test) & params):
                    continue
                reads = any(
                    (isinstance(n, ast.Constant) and isinstance(n.value, str)
                     and "absorb" in n.value.lower())
                    or (isinstance(n, ast.Name) and "absorb" in n.id.lower())
                    for n in ast.walk(br))
                conditional = conditional or reads
        check("[CONTINGENT] and the clause itself is STILL IN the file and "
              "still CONDITIONAL: `%s` offers a conjunct reading the "
              "absorbability answer under a branch keyed on the routing "
              "decision it is passed, so deleting it by hand -- or hard-wiring "
              "it in unconditionally -- turns this row red"
              % (builder.name if builder else "the conjunct builder"),
              conditional,
              "" if conditional else "no absorbability conjunct is offered "
                                     "under a branch keyed on a parameter")

    # --- and the shape of the battery itself ----------------------------
    check("[CONTINGENT] the battery still exits 0 with 0 failures",
          run.returncode == 0 and "CONTROLS FAILED" not in out)
    check("[CONTINGENT] at least one row is labelled [CANNOT FAIL] and the "
          "bottom line still denies the all-pass banner (%d such row(s); the "
          "COUNT is reported and not scored, because a later row honestly "
          "routed to the label would redden a census of it -- the wrong-"
          "direction shape this whole target is being repaired for)" % len(cf),
          len(cf) >= 1 and "bottom line is NOT 'all controls pass'" in out)
    nc4 = [l for l in out.split("\n")
           if l.strip().startswith("[") and " the " in l
           and any(l.strip().startswith("[PASS] " + t + " ") for t, _ in MODES)]
    check("[CONTINGENT] all four NEGATIVE CONTROL 4 mutation rows are still "
          "[PASS]", len(nc4) == 4)

    # --- and this target's own invariant, scored rather than promised ---
    me = [f for f in ast.walk(ast.parse(open(os.path.abspath(__file__)).read()))
          if isinstance(f, ast.FunctionDef) and f.name == "target_3"][0]
    reads = [n for n in ast.walk(me)
             if isinstance(n, ast.Call) and _callee(n) == "read"]
    parsed = [n for p in ast.walk(me)
              if isinstance(p, ast.Call) and _callee(p) == "parse"
              for n in ast.walk(p)
              if isinstance(n, ast.Call) and _callee(n) == "read"]
    check("[CONTINGENT] and THIS TARGET holds itself to the rule it was "
          "repaired under: every read of a source file in it flows into "
          "`ast.parse`, so there is no text of controls.py for a substring "
          "test to freeze (%d read(s), %d of them parsed)"
          % (len(reads), len(parsed)),
          len(reads) >= 1 and len(reads) == len(parsed))


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
    # `--target 3` runs T3 alone.  It exists because T3 is the target that has
    # now been frozen twice, so it is the one that has to be WATCHED going red
    # and green on planted trees -- and a demonstration that pays for T1's 8 s
    # gate rebuild on every world is a demonstration that gets run once and then
    # trimmed.  T3 is self-contained: it takes nothing from T1 or T2.
    only = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--target" else None
    if only == "3":
        target_3()
        bad = [n for n, ok in RESULTS if not ok]
        print()
        print("%d claim(s) scored; %d BROKEN." % (len(RESULTS), len(bad)))
        for n in bad:
            print("   - " + n)
        return 1 if bad else 0
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
        print("mg-da45's finding stands: `absorb == 0` was true, and the reason")
        print("printed for scoring it was false -- the predicate never read a")
        print("sign.  What has changed since (mg-17aa) is that the clause is no")
        print("longer in row I4's scored condition at all: the second forced")
        print("gate, |s_i s_j| = 1, settles the 3 posets whose diagonal")
        print("survives, so the answer is forced on all four rows and is stated")
        print("once in the [CANNOT FAIL] row.  This file no longer scores THAT")
        print("THE DEFERRAL HOLDS -- it scores that the clause was routed and")
        print("not deleted, which is what those three literals were protecting.")
        print()
        print("AND IT NO LONGER SCORES THAT EITHER BY SOURCE LITERALS (mg-686c,")
        print("on mg-79ba's F2).  mg-17aa replaced three frozen literals of the")
        print("state it inherited with three of the state it shipped, one of")
        print("them a verbatim freeze of a conjunct later shown tautological --")
        print("so this file REFUSED that conjunct's repair, in all three of the")
        print("spellings mg-79ba tried, while the battery stayed green.  TARGET")
        print("3 now reads controls.py only by PARSING it by role and by RUNNING")
        print("it, and what it scores is that the absorbability answer is")
        print("accounted for in exactly one place, that the routing which")
        print("decides where is computed from the population, and that the row")
        print("holding it is scored on the population too.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
