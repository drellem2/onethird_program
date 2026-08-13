"""mg-79ba -- shared kernel for the INDEPENDENT AUDIT of mg-17aa.

A SANDBOX AND A SOURCE INJECTOR, and nothing that computes a number the tree
under test also computes.  That restriction is deliberate: mg-17aa's own
`nc4_row_stats` docstring names "two procedures computing one quantity" as how
this lineage got a gate name that was not the code's, and an auditor that
recomputes 297 to check 297 has taken the same bet.  So every claim in this
suite is one of

  (a) a STRUCTURAL fact about `controls.py`'s source, read by `ast`, which is
      exact and has no second route to disagree with; or
  (b) a DIFFERENCE BETWEEN TWO RUNS of the tree under test, where the only
      thing this suite supplies is the edit between them.

Both are checkable by someone who does not trust this file.

WHAT AN INJECTION HERE IS AND IS NOT.  `mutate()` rewrites source lines of a
COPY of `code/face_geometry/` in a temporary directory.  The real tree is never
written to.  An injected world is a hypothesis made runnable -- "suppose a pair
cleared both forced gates" -- and is NOT a claim that the mathematics permits
it.  Where that distinction changes what a result means, the claim says so.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FG = os.path.join(REPO, "code", "face_geometry")

BAR = "=" * 78

# The blob of code/face_geometry/controls.py at 744cfd5, the commit mg-17aa
# branched from -- the tree carrying mg-e35b's deferral.  Pinned by BLOB and not
# by a ref for the reason mg-17aa's own demo_wrong_way.py gives: `main` moves.
PRE_17AA_BLOB = "da160f680e9a96f2628b3a20fdc983d03b65eb0d"


class Score(object):
    """A claim list.  `BROKEN` is a failure of THIS audit's assertion, not of
    the tree -- several claims below assert that something goes red."""

    def __init__(self):
        self.rows = []

    def claim(self, text, ok, detail=""):
        self.rows.append((text, bool(ok)))
        print("  [%s] %s%s" % ("HOLDS" if ok else "BROKEN", text,
                               ("\n        " + detail) if detail else ""))
        return bool(ok)

    def report(self):
        broken = sum(1 for _, ok in self.rows if not ok)
        print("\n" + BAR)
        print("%d claim(s) scored; %d BROKEN." % (len(self.rows), broken))
        print(BAR)
        return 1 if broken else 0


def head(text):
    print("\n" + BAR)
    print(text)
    print(BAR)


def pinned_source():
    """The pre-mg-17aa controls.py, from the pinned blob."""
    r = subprocess.run(["git", "cat-file", "-p", PRE_17AA_BLOB],
                       cwd=REPO, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def sandbox(src=None):
    """A throwaway copy of code/face_geometry/.  `src` overrides controls.py."""
    tmp = tempfile.mkdtemp(prefix="mg79ba_")
    for f in ("controls.py", "face_complex.py", "posets.py"):
        shutil.copy(os.path.join(FG, f), tmp)
    if src is not None:
        with open(os.path.join(tmp, "controls.py"), "w") as fh:
            fh.write(src)
    return tmp


def mutate(tree, edits):
    """Apply (old, new) source substitutions to the sandbox's controls.py.

    Every edit must match EXACTLY ONCE.  Returns the list of edits that did
    not, so a silently-failed injection is a reported claim and not a world
    that quietly did not exist -- mg-17aa's own D2 is an injection that
    "passed" because nothing checked it had landed.
    """
    p = os.path.join(tree, "controls.py")
    src = open(p).read()
    missed = []
    for old, new in edits:
        if src.count(old) != 1:
            missed.append((old, src.count(old)))
            continue
        src = src.replace(old, new)
    with open(p, "w") as fh:
        fh.write(src)
    return missed


def run(tree, n="5"):
    """Run the battery.  Returns (exit code, stdout+stderr)."""
    r = subprocess.run([sys.executable, "controls.py", n], cwd=tree,
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def rows(out):
    """Every scored row of the artifact, as (verdict, first 90 chars).

    The artifact prints `[PASS] ...`, `[FAIL] ...` and `[CANNOT FAIL] ...`.
    Rows are keyed by their opening words because that is what a reader
    identifies them by; the full text carries live counts and moves between
    worlds by design.
    """
    out_rows = []
    for line in out.split("\n"):
        s = line.strip()
        for tag in ("[PASS]", "[FAIL]", "[CANNOT FAIL]", "[SILENT]"):
            if s.startswith(tag):
                out_rows.append((tag, s[len(tag):].strip()[:90]))
                break
    return out_rows


def row_diff(base, other):
    """Rows whose VERDICT changed between two runs, keyed on the row's opening
    words.  A row that appears in one run and not the other is reported as
    such rather than silently dropped."""
    b = {}
    for tag, key in base:
        b.setdefault(key, []).append(tag)
    o = {}
    for tag, key in other:
        o.setdefault(key, []).append(tag)
    changed, gone, added = [], [], []
    for key in b:
        if key not in o:
            gone.append((b[key][0], key))
        elif b[key] != o[key]:
            changed.append((b[key][0], o[key][0], key))
    for key in o:
        if key not in b:
            added.append((o[key][0], key))
    return changed, gone, added


# ---------------------------------------------------------------- injections
#
# Source anchors, verified to match exactly once by `mutate`.  They are written
# out here rather than inline so that a reader can see the whole set of things
# this audit is able to change about the tree under test.

ANCHOR_VB = "            vb = gate_violations(L_mut, target)"
ANCHOR_LMUT = ("            L_mut, target_mut = "
               "claim1_pair(P, incidence_mode=mode)")
ANCHOR_COND = ("              theorem_absorb == 0 and "
               "theorem_blocked == theorem_app,")
ANCHOR_COND_OLD = "              theorem_absorb == 0 and theorem_diag == theorem_app,"


def inject_clear_gate(mode, k=1):
    """Make the k-th biting pair of `mode` clear BOTH forced gates.

    This is the world the [CANNOT FAIL] row's own printed sentence says it
    fails on: "if some pair cleared both forced gates ... this row FAILS".
    """
    return (ANCHOR_VB,
            ANCHOR_VB + "\n"
            "            _inj79ba[mode] = _inj79ba.get(mode, 0) + 1\n"
            "            if mode == %r and _inj79ba[mode] == %d:\n"
            "                vb = frozenset()          # mg-79ba injection\n"
            % (mode, k))


def inject_shape_mismatch(mode, k=1):
    """Make the k-th biting pair of `mode` have a SHAPE mismatch.

    A biting pair counted in `app` and in neither `diag_moved` nor
    `diag_preserved`, because the shape guard `continue`s before them.  This is
    the input P3 predicts refutes the PRE-mg-17aa conjunct.

    THE SMALLER MATRIX IS SQUARE, and it has to be.  The first attempt appended
    a row, giving an (m+1) x m matrix, and BOTH trees died with an IndexError
    inside `not_isospectral` -- the gauge dichotomy block runs BEFORE the shape
    guard and indexes A[i][i].  That is a real fragility in `controls.py` (its
    own comment says "Shape is settled FIRST ... nothing below may index into a
    ragged matrix", and the dichotomy above it does), but no shipped corruption
    reaches it, it is outside this ticket, and it is reported in README.md
    rather than fixed here.
    """
    return (ANCHOR_LMUT,
            ANCHOR_LMUT + "\n"
            "            if mode == %r and not mat_eq(L_mut, L_true) "
            "and len(L_mut) > 1:\n"
            "                _inj79ba['shape'] = _inj79ba.get('shape', 0) + 1\n"
            "                if _inj79ba['shape'] == %d:\n"
            "                    L_mut = [r[:-1] for r in L_mut[:-1]]"
            "   # mg-79ba: SQUARE, one smaller\n"
            % (mode, k))


ANCHOR_ABSORB = "            if absorbable_by_diagonal_twist(L_mut, target):"


def inject_absorbable(mode, k=1):
    """Make the k-th biting pair of `mode` REPORT absorbable while leaving its
    gate violations intact.

    The other disjunct of the [CANNOT FAIL] row's printed failure condition --
    "or the predicate did report absorbable".  Note what this world is: the two
    procedures DISAGREEING, not the mathematics changing.  A pair with a
    violated forced gate cannot be absorbable, so no input can produce this
    honestly; that is the point of running it.
    """
    return (ANCHOR_ABSORB,
            "            if mode == %r:\n"
            "                _inj79ba['abs'] = _inj79ba.get('abs', 0) + 1\n"
            "            if absorbable_by_diagonal_twist(L_mut, target) or ("
            "_inj79ba.get('abs') == %d and mode == %r):   # mg-79ba\n"
            % (mode, k, mode))


PRELUDE = ("from posets import all_posets, POSET_COUNTS, cover_string",
           "from posets import all_posets, POSET_COUNTS, cover_string\n"
           "\n_inj79ba = {}      # mg-79ba injection counters, per mutation mode\n")
