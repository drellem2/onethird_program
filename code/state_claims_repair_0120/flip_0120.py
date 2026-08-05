#!/usr/bin/env python3
"""mg-0120 — THE FLIP HARNESS: every repaired verdict SHOWN RETURNING THE OTHER ANSWER.

THE ARGUMENT THIS FILE EXISTS TO CLOSE.  `verdicts0120.py` replaces six literals with six
computations.  That is not by itself a repair, because an expression that returns `False`
today is indistinguishable from the literal `False` it replaced until somebody has seen it
return something else.  A control nobody has seen fail is not evidence.  So each of the six
is put to inputs on which it MUST come out the other way, and a row whose verdict never moves
is reported NOT PROVEN CAPABLE OF BOTH ANSWERS and is not counted as repaired.

TWO TIERS, AND THE FIRST ONE IS THE STRONGER.

  TIER 1 — HISTORY.  Each verdict is evaluated at `bd24efc` (mg-16eb's revision, where the
           defect it is about must still be present) and at the working tree (where mg-a74f's
           repair has landed).  A verdict that differs across that pair has been shown to
           move ON TWO REAL TREES THAT SOMEBODY ELSE MADE.  No construction of mine is
           involved and there is nothing for me to have rigged.

  TIER 2 — CONSTRUCTION.  Each verdict is also handed an input built here for the purpose.
           This tier is what covers the rows history does not happen to separate, and it is
           the only way to reach a verdict value that no revision in this repository
           produces.

THE THREE VALUES.  A verdict is `True` (holds), `False` (BROKEN) or `None` (RESPECIFIED — the
sentence the row is about is not in the file at this revision).  "Both ways" is read strictly:
a row is PROVEN only if BOTH `True` AND `False` have been observed from it.  Two rows reach
`None` on the repaired tree, and for those, seeing `None` and `False` is NOT enough — the
construction that produces `True` is built and named.  Where a value is unreachable and I
could not construct it, this file SAYS SO on the row rather than rounding up.

THE HARNESS'S OWN CONTROL — section 3.  A harness that reports PROVEN for everything is
worth nothing until it has been seen to report NOT PROVEN.  Two stand-ins are put through
the identical code path: one pinned to the literal `False` and one to the literal `True` —
that is, the exact shape this repair removed.  If either is reported PROVEN, this file exits
non-zero on itself.

    D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
    NODE_PATH="$D/node_modules" python3 code/state_claims_repair_0120/flip_0120.py

Without the renderers, rows 2 and 6 cannot be constructed and are reported UNPROBED rather
than passed.  NOTHING IS WRITTEN TO THE WORKING TREE: every construction lives in a throwaway
`git worktree`, removed on the way out.
"""
import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import verdicts0120 as V                                            # noqa: E402

BEFORE = "bd24efc"
NAME = {True: "holds", False: "BROKEN", None: "RESPECIFIED"}


def show(v):
    return NAME[v]


# =========================================================================================
# TIER 2 — THE CONSTRUCTIONS.  Each returns (label, verdict, detail-line).  Each is written
# so that the value it is reaching for is stated in the label, and a construction that fails
# to reach it is a finding about this repair, not about the row.
# =========================================================================================
def c_v3(wt_head, have_node):
    """Reach `False` at the REPAIRED revision by neutralising the direction mg-a74f added.

    The two cross-checks are located by their PREDICATES, which are the bytes mg-a74f wrote
    for exactly this purpose, and each is turned into a tautology — `set(X) == set(X)` — so
    the check still runs, still prints, and can no longer fail.  Nothing else in the file is
    touched.  If either substitution is a no-op the construction reports itself IMPOSSIBLE
    rather than testing nothing and passing."""
    orig = wt_head.read(V.CTL)
    subs = [("set(DELEGATED_PRESENTATION) == set(DELEGATED)",
             "set(DELEGATED) == set(DELEGATED)"),
            ("set(want_pres) == set(want)", "set(want) == set(want)")]
    patched = orig
    for a, b in subs:
        if a not in patched:
            return ("C3  both reverse-direction cross-checks made tautologies", "IMPOSSIBLE",
                    f"    {a!r} is not in delta_control.py — construction not made")
        patched = patched.replace(a, b)
    wt_head.write(V.CTL, patched)
    try:
        v, _d = V.v3_two_tables(None, _wt=wt_head, ctl_text=patched)
    finally:
        wt_head.write(V.CTL, orig)
    return ("C3  both reverse-direction cross-checks made tautologies "
            "(`set(X) == set(X)`)", v,
            "    two substitutions in delta_control.py, in a throwaway worktree; the checks "
            "still run\n    and still print — they can no longer fail")


def c_v4(wt_before, have_node):
    """Reach `True` — a value NO revision of this repository produces for this row.

    `True` needs the sentence ASSERTED (so: `bd24efc`) and NEITHER direction refuted.  So
    E1 is made a no-op (no fenced example: the control does not exit 1 and every section is
    shown) and E2 is given `<details open>` (a reader IS shown all five)."""
    if not have_node:
        return ("C4  E1 neutralised + `<details open>`", "UNPROBED",
                "    renderers absent")
    v, _d = V.v4_exit_semantics(BEFORE, _wt=wt_before, have_node=True,
                               e1_example="", e2_prefix="<details open>\n\n")
    return ("C4  at bd24efc with E1 neutralised and E2 opened (`<details open>`)", v,
            "    the sentence is asserted at this revision and neither direction refutes it")


def c_v5(wt_head, have_node):
    """Reach `True` by pointing the same computation at a range where the sentence is true.

    A tip is BUILT: `db2b77d`'s presentation.py with exactly one message string altered and
    four self-test cases appended, committed in a throwaway worktree.  That is the file the
    sentence describes, so the same function must now say it holds."""
    base = V.at(V.BASE_0049, V.PRES)
    old_msg = '"no block (the region\'s first line is a blank separator)"'
    if old_msg not in base:
        return ("C5  a tip where ONLY a message and four cases changed", "IMPOSSIBLE",
                "    the message string is not in the base revision — not constructed")
    new = base.replace(old_msg, '"no block (the region\'s first line is a blank spacer)"', 1)
    new += ("\n\n_MG0120_CASES = [\n"
            "    ('case one', 1),\n    ('case two', 2),\n"
            "    ('case three', 3),\n    ('case four', 4),\n]\n")
    wt_head.write(V.PRES, new)
    V.git("-C", wt_head.dir, "add", V.PRES)
    subprocess.run(["git", "-C", wt_head.dir, "add", V.PRES], capture_output=True)
    r = subprocess.run(["git", "-C", wt_head.dir, "commit", "-q", "-m",
                        "mg-0120 flip construction: one message and four cases"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return ("C5  a tip where ONLY a message and four cases changed", "IMPOSSIBLE",
                f"    the construction commit failed: {r.stderr.strip()[:120]}")
    tip = subprocess.run(["git", "-C", wt_head.dir, "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    v, _d = V.v5_presentation_diff(tip)
    subprocess.run(["git", "-C", wt_head.dir, "reset", "-q", "--hard", "HEAD~1"],
                   capture_output=True)
    return (f"C5  a constructed tip {tip[:7]}: one message + four cases and nothing else", v,
            "    the same function, the same base, a range built to satisfy the sentence")


def c_v6(wt_head, have_node):
    """Reach `False` by moving one observed exit code in the transcript the row joins on."""
    rerun = V.at(None, V.RERUN)
    mutated = rerun.replace("got exit 1", "got exit 2", 1)
    if mutated == rerun:
        return ("C6  one observed exit moved in the transcript", "IMPOSSIBLE",
                "    no `got exit 1` in the transcript — not constructed")
    v, _d = V.v6_r1r2_table(None, rerun_text=mutated)
    return ("C6  one `got exit 1` -> `got exit 2` in mg-5644's re-run transcript", v,
            "    the document is handed to the function as text; the file is not touched")


def c_v7(wt_head, have_node):
    """Reach `False` by moving the section number the README asserts."""
    rdm = V.at(None, V.RDM)
    mutated = rdm.replace("re-run in section 8 of `run_all.sh`",
                          "re-run in section 7 of `run_all.sh`")
    if mutated == rdm:
        mutated = rdm.replace("section 8 of `run_all.sh`", "section 7 of `run_all.sh`")
    if mutated == rdm:
        return ("C7  the asserted section number moved", "IMPOSSIBLE",
                "    no `section 8 of run_all.sh` to move — not constructed")
    v, _d = V.v7_section_pointer(None, rdm_text=mutated)
    return ("C7  the README's asserted section moved 8 -> 7", v,
            "    the document is handed to the function as text; the file is not touched")


def c_v8(wt_head, have_node):
    """Reach `True` — again a value no revision produces — with `<details open>`.

    The row is about what a `<details>` at the top does.  Opened, it suppresses nothing, and
    a verdict that measures the property rather than naming it must say so."""
    if not have_node:
        return ("C8  `<details open>` at the top", "UNPROBED", "    renderers absent")
    r49 = V.at(BEFORE, V.R49)
    v, _d = V.v8_r5_details(BEFORE, have_node=True, r49_text=r49,
                            prefix="<details open>\n\n")
    return ("C8  at bd24efc with `<details open>` at the top of the target", v,
            "    the sentence is asserted at this revision and the container suppresses "
            "nothing")


# (constructor, THE VALUE IT IS REACHING FOR).  The target is declared here so the run can
# say REACHED or MISSED instead of printing a number and leaving the reader to work out
# whether it was the one being aimed at.  A MISSED construction is printed in full; it is a
# finding about this repair's constructions, not about the row.
CONSTRUCTIONS = {
    "claims16eb.py:94": (c_v3, False),
    "claims16eb.py:142": (c_v4, True),
    "claims16eb.py:156": (c_v5, True),
    "claims16eb.py:178": (c_v6, False),
    "claims16eb.py:194": (c_v7, False),
    "claims16eb.py:217": (c_v8, True),
}


def evaluate(fn, rev, wt, have_node):
    import inspect
    kw = {}
    params = inspect.signature(fn).parameters
    if "_wt" in params:
        kw["_wt"] = wt
    if "have_node" in params:
        kw["have_node"] = have_node
    return fn(rev, **kw)[0]


def main():
    have_node = V.renderers_present()
    print("=" * 100)
    print("mg-0120 — THE FLIP HARNESS.  Every repaired verdict shown returning the other "
          "answer.")
    print("=" * 100)
    print(f"  before revision   {BEFORE}  (mg-16eb's; the defect must still be present)")
    print(f"  after revision    the working tree")
    print(f"  renderers         {'marked + markdown-it present' if have_node else 'ABSENT'}")
    print("  constructions     applied in throwaway worktrees; the working tree is never")
    print("                    opened for writing by this program")
    print()

    wt_before = V.Worktree(BEFORE)
    wt_head = V.Worktree(None)
    rows = []
    try:
        print("1.  TIER 1 — HISTORY.  The same function at two real revisions.")
        print()
        for site, sentence, fn in V.SIX:
            a = evaluate(fn, BEFORE, wt_before, have_node)
            b = evaluate(fn, None, wt_head, have_node)
            print(f"  {site:<20s} {BEFORE} -> {show(a):<12s} working tree -> {show(b):<12s}"
                  f" {'MOVED' if a != b else 'same at both'}")
            print(f"  {'':<20s} {sentence[:74]}")
            rows.append([site, sentence, {a, b}, a, b])
        print()

        print("2.  TIER 2 — CONSTRUCTION.  An input built here to reach a value the two")
        print("    revisions above do not produce.")
        print()
        missed = []
        for row in rows:
            site = row[0]
            ctor, target = CONSTRUCTIONS[site]
            label, v, detail = ctor(
                wt_head if site not in ("claims16eb.py:142", "claims16eb.py:217")
                else wt_before, have_node)
            shown = show(v) if v in NAME else str(v)
            hit = ("REACHED" if v is target else
                   "not attempted" if v in ("UNPROBED", "IMPOSSIBLE") else "MISSED")
            if hit == "MISSED":
                missed.append((site, label, target, shown))
            print(f"  {site:<20s} {label}")
            print(f"  {'':<20s} reaching for {show(target):<12s} got {shown:<12s} {hit}")
            print(f"  {detail}")
            if v in NAME:
                row[2] = row[2] | {v}
        print()
        print(f"  {len(rows) - len(missed)} of {len(rows)} constructions reached the value "
              f"they were built to reach.")
        for site, label, target, shown in missed:
            print(f"    MISSED  {site}  {label}")
            print(f"            built to produce {show(target)}, produced {shown} — the "
                  f"construction does not do what its name says")
        print()

        print("3.  THE HARNESS'S OWN CONTROL.  Two stand-ins of the exact shape this repair")
        print("    removed, put through the identical Tier-1 code path.")
        print()
        control_ok = True
        for pinned in (False, True):
            def stand_in(rev=None, _wt=None, have_node=None, _p=pinned):
                return _p, "a literal"
            a = evaluate(stand_in, BEFORE, wt_before, have_node)
            b = evaluate(stand_in, None, wt_head, have_node)
            observed = {a, b}
            proven = {True, False} <= observed
            print(f"  a verdict pinned to the literal {str(pinned):<5s}  "
                  f"{BEFORE} -> {show(a):<12s} working tree -> {show(b):<12s}  "
                  f"reported {'PROVEN' if proven else 'NOT PROVEN CAPABLE OF BOTH ANSWERS'}")
            control_ok &= not proven
        print(f"  the harness rejects a pinned verdict: {control_ok}")
        print()
    finally:
        wt_before.close()
        wt_head.close()

    print("=" * 100)
    print("VERDICT.  A row is PROVEN only if both `holds` and `BROKEN` have been observed")
    print("from it.  `RESPECIFIED` is a third value and does not substitute for either.")
    print("=" * 100)
    bad = 0
    for site, sentence, observed, _a, _b in rows:
        proven = {True, False} <= observed
        bad += not proven
        seen = ", ".join(show(v) for v in sorted(observed, key=lambda x: str(x)))
        print(f"  [{'PROVEN' if proven else ' NOT  '}] {site:<20s} values observed: {seen}")
        if not proven:
            print(f"            {sentence[:84]}")
            print(f"            NOT PROVEN CAPABLE OF BOTH ANSWERS — this row is not "
                  f"counted as repaired.")
    print()
    print(f"  {len(rows) - bad} of {len(rows)} repaired verdicts are proven capable of both "
          f"answers.")
    print(f"  population: the 6 `claim()` rows of claims16eb.py that carried a literal on "
          f"the printed path.")
    print(f"  grain: a verdict value returned by one function.")
    print("=" * 100)
    return 0 if (bad == 0 and control_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
