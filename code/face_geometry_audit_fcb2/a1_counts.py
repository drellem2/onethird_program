"""mg-fcb2 A1 -- EVERY COUNT THE REPAIR PRINTS, AND AN INPUT THAT MOVES IT.

The ticket: *for each number the repair prints, construct an input that changes
it.  A number that cannot move is a property, and printing it as a result
inflates the battery.*

mg-e35b landed exactly that standard -- it is F3, and the repair's own commit
message says "TWO PRINTED MEASUREMENTS WERE TAUTOLOGIES AND ARE NOW PROPERTIES".
`verify_e35b.py` section V6 is where the repair states it has finished the job:
its header reads "EVERY COUNT THIS REPAIR PRINTS, and whether it could have come
out differently", it lists eleven, and it scores that the list is complete.

This script does not read that table and agree with it.  For each of its eleven
rows it CONSTRUCTS an input and reports whether the count actually moved; and it
goes looking, in the artifact, for counts the table does not contain.

PREDICTED EXIT: 1 -- P1 and P2 are refutations of claims the repair makes.
"""

import ast
import builtins
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

import lib_fcb2 as L

fc, po = L.import_face_geometry()
sys.path.insert(0, L.FACE_GEOMETRY)
import controls                                                  # noqa: E402
import face_complex                                              # noqa: E402
from posets import all_posets                                    # noqa: E402

REPAIR = os.path.join(L.REPO_ROOT, "code", "face_geometry_repair_e35b")


# --------------------------------------------------------------------------
# running NEGATIVE CONTROL 4 under a constructed input, and reading its counts
# --------------------------------------------------------------------------

FIGURES = [
    ("site_corrupted", r"named load-bearing site is corrupted on (\d+)/(\d+) posets"),
    ("coverage", r"coverage at `le_to_facet` is (\d+)/(\d+), of which (\d+) carry"),
    ("dichotomy",
     r"-- (\d+) biting \(poset, row\) pairs = (\d+) NON-SIMILAR \+ (\d+) GAUGE "
     r"\+ (\d+) unclassified"),
    ("swap01_gauge",
     r"classified GAUGE on (\d+)/(\d+) of the posets where it bites, and on (\d+) of them"),
    ("not_gauge", r"while saying NOT-GAUGE on (\d+) of the (\d+) biting pairs"),
    ("target_identical",
     r"byte-identical to the uncorrupted target on (\d+)/(\d+) \(poset, mutation\) pairs"),
    ("multi_ridge",
     r"no ridge lies in >= 3 facets under any of the four mutations on any of "
     r"the (\d+) posets \(([^)]*)\)"),
    ("m4m5",
     r"moves it on (\d+)/(\d+) posets and M5 \(one edge deleted\) on (\d+)/(\d+)"),
]
VAC_RE = re.compile(r"(I\d) (\d+) vacuous = (\d+) did-not-apply \+ (\d+) applied-but-unseen")


def parse_counts(text):
    """Read the section's own printed figures back out of its own output.

    EVERY PATTERN IS MATCHED WITHIN ONE LINE and never across a newline: the
    mg-c067 audit's figure grammar crossed a newline and read the tail of a
    commit sha as part of a population, and that is a defect of the instrument,
    not of the thing measured.  `re.MULTILINE` is not used and `.` never sees a
    newline because each search runs on a single line.
    """
    out = {}
    lines = text.splitlines()
    for key, pat in FIGURES:
        rx = re.compile(pat)
        hits = [m.groups() for line in lines for m in [rx.search(line)] if m]
        out[key] = hits[0] if len(hits) == 1 else ("AMBIGUOUS/ABSENT", len(hits))
    vac = {}
    for line in lines:
        for m in VAC_RE.finditer(line):
            vac[m.group(1)] = tuple(m.groups()[1:])
    out["vacuity"] = tuple(sorted(vac.items()))
    return out


class patched(object):
    """Install attribute patches on the tree under audit and take them off again.

    Everything this script calls an "input" is applied here: the population the
    section is run over, or a substitution of one named ingredient.  Nothing is
    edited on disk, and `controls`' scoring globals are snapshotted so that a
    constructed run cannot leak a row into a later one.
    """

    def __init__(self, **attrs):
        self.attrs = attrs
        self.saved = []

    def __enter__(self):
        for dotted, val in self.attrs.items():
            modname, name = dotted.split("__", 1)
            mod = {"controls": controls, "face_complex": face_complex}[modname]
            self.saved.append((mod, name, getattr(mod, name)))
            setattr(mod, name, val)
        self.state = (list(controls.FAIL), list(controls.CANNOT_FAIL),
                      list(controls.ROW_NAMES))
        return self

    def __exit__(self, *exc):
        for mod, name, val in reversed(self.saved):
            setattr(mod, name, val)
        controls.FAIL[:] = self.state[0]
        controls.CANNOT_FAIL[:] = self.state[1]
        controls.ROW_NAMES[:] = self.state[2]
        return False


def run_nc4(nmax=5, **attrs):
    buf, old = io.StringIO(), sys.stdout
    with patched(**attrs):
        sys.stdout = buf
        try:
            controls.negative_control_incidence(nmax)
        finally:
            sys.stdout = old
    return buf.getvalue()


# --------------------------------------------------------------------------
# the constructed inputs
# --------------------------------------------------------------------------

def widened_all_posets(n):
    """The population with n = 1 ADMITTED.  The section builds its population as
    `range(2, nmax + 1)`, so the one-element poset is the nearest legal input it
    has never been run on -- and it is the input on which the coverage line's
    sentence is FALSE."""
    return (controls.__dict__["_orig_all_posets"](1)
            + controls.__dict__["_orig_all_posets"](2)) if n == 2 \
        else controls.__dict__["_orig_all_posets"](n)


controls.__dict__["_orig_all_posets"] = all_posets


CALLS = {"blind": 0, "credulous": 0}


def blind_detector(A, B, perms):
    CALLS["blind"] += 1
    return None


def credulous_detector(A, B, perms):
    """Returns a witness for EVERY pair it is shown.  The call count is kept so
    that a count which does not move can be distinguished from a patch that was
    never reached -- "I substituted something and nothing happened" is worth
    nothing without that."""
    CALLS["credulous"] += 1
    return (list(range(len(A))), [1] * len(A))


def identity_only_perms(P, mode):
    return [list(range(len(fc.linear_extensions(P))))]


def main():
    print("== mg-fcb2 A1: every count the repair prints, and an input that moves it ==")
    print()

    base = run_nc4(5)
    b = parse_counts(base)
    print("  counts read back from NEGATIVE CONTROL 4 at HEAD:")
    for k in sorted(b):
        print("    %-18s %s" % (k, b[k]))
    print()

    # ---- P1: the coverage line's 86/86 -----------------------------------
    print("A1.1 -- THE COVERAGE LINE'S FIRST FIGURE")
    L.predicted("P1a", b["site_corrupted"] == ("86", "86"),
                "the printed figure at HEAD is %s/%s (predicted 86/86)"
                % b["site_corrupted"][:2])

    # (i) the two arguments are the SAME EXPRESSION, established from the source
    #     and not from the output, so this is a statement about the code path.
    src = open(os.path.join(L.FACE_GEOMETRY, "controls.py")).read()
    tree = ast.parse(src)
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef)
              and n.name == "negative_control_incidence")
    MARK = "named load-bearing site is corrupted"

    def carries_mark(node):
        return any(isinstance(s, ast.Constant) and isinstance(s.value, str)
                   and MARK in s.value for s in ast.walk(node))

    same_expr = None
    for node in ast.walk(fn):
        # The site is identified by the SENTENCE it prints, not by position:
        # this function contains several `%d/%d` format expressions and an
        # earlier version of this probe matched the first one it walked past,
        # which is the instrument check's `(yes, N)`.  That was a defect of this
        # audit's own instrument and is recorded in README.md.
        if not (isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod)
                and carries_mark(node.left)):
            continue
        args = node.right.elts if isinstance(node.right, ast.Tuple) else [node.right]
        assert len(args) >= 2, "the coverage line's argument tuple changed shape"
        same_expr = (ast.dump(args[0]) == ast.dump(args[1]),
                     ast.unparse(args[0]), ast.unparse(args[1]))
        break
    assert same_expr is not None, "the coverage sentence is no longer printed here"
    print("    the two arguments supplied for `%%d/%%d`: %r and %r -- same "
          "expression: %s" % (same_expr[1], same_expr[2], same_expr[0]))
    L.check("A1.1a the coverage line's numerator and denominator are DIFFERENT "
            "expressions, so the printed ratio is a measurement", not same_expr[0])
    L.predicted("P1b", same_expr[0],
                "numerator and denominator are the same expression (%s)"
                % same_expr[1])

    # (ii) an input on which the underlying property is FALSE and the print is
    #      unchanged.  This is the strongest form of "it cannot come out
    #      otherwise": the corruption is made a no-op, so the true count is 0.
    with patched(face_complex__le_to_facet_offbyone=face_complex.le_to_facet,
                 controls__le_to_facet_offbyone=face_complex.le_to_facet):
        noop = parse_counts(run_nc4(5))
        truth_noop = sum(1 for P in [Q for n in range(2, 6) for Q in all_posets(n)]
                         if controls.mutation_applied_at_site(P, "facet_offbyone"))
    print("    INPUT 1 -- `le_to_facet_offbyone := le_to_facet`, i.e. the named "
          "site is not corrupted on ANY poset.  True count %d/86.  The line "
          "prints %s/%s." % (truth_noop, noop["site_corrupted"][0],
                             noop["site_corrupted"][1]))
    L.check("A1.1b with the corruption replaced by a no-op the coverage line's "
            "first figure moves (it should read 0/86, since the site is then "
            "corrupted on no poset at all)",
            noop["site_corrupted"][:2] != ("86", "86"))

    # (iii) an input on which the sentence is false and the battery stays GREEN.
    with patched(controls__all_posets=widened_all_posets):
        wide_text = run_nc4(5)
        wide = parse_counts(wide_text)
    pop = [Q for n in (1, 2, 3, 4, 5) for Q in all_posets(n)]
    truth_wide = sum(1 for P in pop
                     if controls.mutation_applied_at_site(P, "facet_offbyone"))
    i4_row = [l for l in wide_text.splitlines() if "I4 the facet enumeration" in l]
    print("    INPUT 2 -- the population WIDENED to admit n = 1 (the section builds "
          "`range(2, nmax + 1)`; n = 1 is the nearest legal poset it has never "
          "been run on).  The line prints %s/%s; the true count is %d/%d, because "
          "`le_to_facet` and `le_to_facet_offbyone` BOTH return the empty chain on "
          "the one-element poset, so the site is not corrupted there.  Row I4 is "
          "still %s."
          % (wide["site_corrupted"][0], wide["site_corrupted"][1], truth_wide,
             len(pop), "[PASS]" if i4_row and "[PASS]" in i4_row[0] else "not [PASS]"))
    L.check("A1.1c the coverage line's sentence -- 'the named load-bearing site "
            "is corrupted on N/N posets' -- is TRUE on every population the "
            "section can be given",
            truth_wide == len(pop))
    L.predicted("P1c", wide["site_corrupted"][:2] == ("87", "87")
                and truth_wide == 86 and len(pop) == 87,
                "with n = 1 admitted the print reads %s/%s while the truth is "
                "%d of %d (predicted: prints 87/87, truth 86 of 87)"
                % (wide["site_corrupted"][0], wide["site_corrupted"][1],
                   truth_wide, len(pop)))

    # (iv) V6 claims to list every count this repair prints.  This one is not in it.
    v6src = open(os.path.join(REPAIR, "verify_e35b.py")).read()
    in_table = "corrupted on" in v6src.split("table = [")[1].split("]")[0] \
        if "table = [" in v6src else False
    L.check("A1.1d V6's table -- headed 'EVERY COUNT THIS REPAIR PRINTS' -- "
            "contains the coverage line's first figure", in_table)
    L.predicted("P1d", not in_table,
                "the 86/86 figure is absent from V6's eleven rows, which carry "
                "the 61/86 coverage figure from the same sentence instead")
    print()

    # ---- P2: V6's completeness row ---------------------------------------
    print("A1.2 -- V6'S OWN COMPLETENESS ROW")
    vt = ast.parse(v6src)
    cond_src = names = None
    for node in ast.walk(vt):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == "check" and len(node.args) >= 2:
            txt = ast.unparse(node.args[1])
            if "len(table)" in txt:
                cond_src = txt
                # builtins are not a source of information about the artifact;
                # an earlier version of this probe counted `len` as a free name
                # and scored P2a off prediction for it (recorded in README.md).
                names = sorted({n.id for n in ast.walk(node.args[1])
                                if isinstance(n, ast.Name)
                                and not hasattr(builtins, n.id)})
    print("    the scored condition is: %s" % cond_src)
    print("    the names it reads: %s" % names)
    tbl = next(n for n in ast.walk(vt)
               if isinstance(n, ast.Assign)
               and any(isinstance(t, ast.Name) and t.id == "table" for t in n.targets))
    all_literal = all(isinstance(e, ast.Constant)
                      for tup in tbl.value.elts for e in tup.elts)
    L.check("A1.2a the condition scoring V6's completeness reads the ARTIFACT, "
            "not the literal standing beside it",
            not (set(names) <= {"forced", "table"} and all_literal))
    L.predicted("P2a", set(names) <= {"forced", "table"} and all_literal,
                "the condition's only free names are %s, and `table` is a list of "
                "string literals %d rows long; nothing in it touches "
                "controls_output.txt" % (names, len(tbl.value.elts)))

    # ... and the demonstration: a TWELFTH count added to the ARTIFACT, with V6
    # left exactly as it is.
    verdict = twelfth_count_demo()
    L.check("A1.2b V6's completeness row goes RED when a twelfth count is added "
            "to the artifact it claims to have enumerated", verdict == "RED")
    L.predicted("P2b", verdict == "GREEN",
                "with a twelfth printed count in controls.py, V6's completeness "
                "row is %s -- it cannot fail on an omission, which is why the "
                "86/86 survived it" % verdict)
    print()

    # ---- the ticket's own requirement, row by row ------------------------
    print("A1.3 -- V6'S ELEVEN ROWS: AN INPUT CONSTRUCTED FOR EACH")
    print("    Each row is asked TWO questions, because they are different "
          "questions and V6 answers only the first:")
    print("      (1) does the count move at all, under any input constructed here?")
    print("      (2) does it move under the SPECIFIC mechanism V6's own `why` "
          "column names?  A reason that does not move the count is not a reason.")
    print()

    POP4 = "the population restricted to n <= 4"
    BLIND = ("the gauge detector replaced by one that never returns a witness "
             "(this row's own why: 'fails only if the detector is wrong')")
    CREDULOUS = ("a CREDULOUS detector returning a witness for every pair "
                 "(this row's own why: 'a detector that accepted everything "
                 "would print 297 here')")
    IDONLY = ("the candidate list narrowed to the identity alone (this row's own "
              "why: 'a detector answering by diagonal twist alone would print 0')")

    def zeros_only(v):
        """The multi-ridge row's CLAIM is the four zeros, not the population size
        printed beside them.  Comparing the whole tuple would score a moved
        population as a moved count, which is not what the row asserts."""
        return v[1] if isinstance(v, tuple) and len(v) == 2 else v

    def ratio_locked(v):
        """For the k/k rows the claim is that the two halves are LOCKED, not that
        the value is constant: a FORCED label says no input can make numerator
        differ from denominator."""
        return v[0] == v[1]

    # `own` marks the try that reproduces the mechanism the row's OWN `why`
    # column names.  Only three of the eleven `why`s name a mechanism at all;
    # the rest describe why the count is what it is.  Scoring a descriptive
    # `why` as a failed mechanism would be this audit inventing a claim to
    # refute, so those rows carry own=None and are not counted in A1.3b.
    rows = [
        # label, V6 verdict, count key, [(how, runner, own)], projection
        ("dichotomy: 297 = 288 + 9 + 0", "COULD MOVE", "dichotomy",
         [(POP4, lambda: run_nc4(4), False)], None),
        ("detector positive control: swap01 GAUGE 72/72", "FORCED BY MATHEMATICS",
         "swap01_gauge",
         [(BLIND, lambda: run_nc4(5, controls__signed_permutation_witness=blind_detector),
           True)], None),
        ("detector says NOT-GAUGE on 288 of 297", "COULD MOVE", "not_gauge",
         [(CREDULOUS,
           lambda: run_nc4(5, controls__signed_permutation_witness=credulous_detector),
           True),
          (POP4, lambda: run_nc4(4), False)], None),
        ("non-identity witness on 72/72 of swap01", "COULD MOVE", "swap01_gauge",
         [(IDONLY, lambda: run_nc4(5, controls__gauge_candidate_perms=identity_only_perms),
           True)], None),
        ("vacuity split I1/I2/I3 = 14/4/4", "COULD MOVE", "vacuity",
         [(POP4, lambda: run_nc4(4), False)], None),
        ("vacuity split I4 = 0 + 25", "COULD MOVE", "vacuity",
         [(POP4, lambda: run_nc4(4), False)], None),
        ("target byte-identical 344/344", "FORCED BY THE CODE PATH",
         "target_identical",
         [(POP4, lambda: run_nc4(4), False),
          ("`le_to_facet_offbyone := le_to_facet`",
           lambda: run_nc4(5,
                           face_complex__le_to_facet_offbyone=face_complex.le_to_facet,
                           controls__le_to_facet_offbyone=face_complex.le_to_facet),
           False)],
         ratio_locked),
        ("no ridge in >= 3 facets, I1/I2/I3 zeros", "FORCED BY CONSTRUCTION",
         "multi_ridge", [(POP4, lambda: run_nc4(4), False)], zeros_only),
        ("no ridge in >= 3 facets, I4 zero", "COULD MOVE", "multi_ridge",
         [(POP4, lambda: run_nc4(4), False)], zeros_only),
        ("coverage 61/86 at le_to_facet", "COULD MOVE", "coverage",
         [(POP4, lambda: run_nc4(4), False)], None),
        ("M4 moves the target on 82/86, M5 on 82/86", "COULD MOVE", "m4m5",
         [(POP4, lambda: run_nc4(4), False)], None),
    ]

    cache = {}
    results = []
    for label, v6, key, tries, proj in rows:
        proj = proj or (lambda v: v)
        before = proj(b[key])
        outcomes = []
        for how, run, own in tries:
            if how not in cache:
                cache[how] = parse_counts(run())
            after = proj(cache[how][key])
            outcomes.append((how, after != before, before, after, own))
        any_moved = any(o[1] for o in outcomes)
        own_reason = next((o for o in outcomes if o[4]), None)
        results.append((label, v6, any_moved, own_reason))
        print("    %s" % label)
        print("      V6 says: %-24s  under the inputs tried: %s"
              % (v6, "MOVES" if any_moved else "DOES NOT MOVE"))
        for how, did, bef, aft, own in outcomes:
            print("        %-6s %s%s" % ("MOVED" if did else "STUCK",
                                         "[V6's own why] " if own else "", how))
            print("               %s -> %s" % (bef, aft))
    print()
    print("    the substituted detectors were REACHED, so a count that did not "
          "move did not fail to move because the patch was never called: the "
          "blind detector was called %d times and the credulous one %d times."
          % (CALLS["blind"], CALLS["credulous"]))
    L.check("A1.3z this audit's own substitutions actually ran (a null result "
            "from a patch that was never reached is worth nothing)",
            CALLS["blind"] > 0 and CALLS["credulous"] > 0)
    print()

    could = [r for r in results if r[1] == "COULD MOVE"]
    could_moved = [r for r in could if r[2]]
    L.check("A1.3a every V6 row labelled COULD MOVE is moved by an input "
            "constructed here (%d of %d)" % (len(could_moved), len(could)),
            len(could_moved) == len(could))
    for label, v6, any_moved, _ in could:
        if not any_moved:
            print("      -> `%s` is labelled COULD MOVE and no input tried moves "
                  "it" % label)

    with_own = [r for r in results if r[3] is not None]
    own_ok = [r for r in with_own if r[3][1]]
    L.check("A1.3b of the %d rows whose `why` names a MECHANISM, that mechanism "
            "actually moves the count (%d of %d)"
            % (len(with_own), len(own_ok), len(with_own)),
            len(own_ok) == len(with_own))
    for label, v6, _, own in with_own:
        if not own[1]:
            print("      -> `%s`: V6's stated reason does not move it -- %s"
                  % (label, own[0]))
            print("         the binning is `if not_isospectral: ... elif "
                  "witness: ...`, so the 288 spectrally separated pairs never "
                  "reach the detector at all.  A detector that accepted "
                  "everything would still print 288.")

    forced = [r for r in results if r[1].startswith("FORCED")]
    forced_locked = [r for r in forced if not r[2]]
    print("    the %d FORCED rows, one at a time:" % len(forced))
    for label, v6, any_moved, own in forced:
        print("      %-42s %s" % (label[:42],
                                  "LOCKED under every input tried" if not any_moved
                                  else "moves under the input its own `why` names, "
                                       "which is what that `why` says it does"))
    print("    -- so %d of the %d are locked outright, and the third "
          "(FORCED BY MATHEMATICS) is falsifiable exactly where its own text says "
          "it is: by a wrong detector.  That is a correctly labelled row and this "
          "audit says so." % (len(forced_locked), len(forced)))

    # ---- the row labelled COULD MOVE that no input moves ------------------
    print()
    print("A1.4 -- THE I4 MULTI-RIDGE ZERO: A COUNT LABELLED `COULD MOVE` THAT "
          "CANNOT (unpredicted -- PREDICTIONS.md does not mention this row)")
    worst = 0
    seen = 0
    for n in range(1, 7):
        for P in all_posets(n):
            les = fc.linear_extensions(P)
            for fam in ([fc.le_to_facet(w) for w in les],
                        [fc.le_to_facet_offbyone(w) for w in les]):
                counts = {}
                for f in fam:
                    for i in range(len(f)):
                        r = f[:i] + f[i + 1:]
                        counts[r] = counts.get(r, 0) + 1
                worst = max([worst] + list(counts.values()))
                seen += 1
    print("    over every poset with n <= 6 and BOTH facet maps (%d families), "
          "the largest number of facets sharing a ridge is %d" % (seen, worst))
    print("    the reason, in one line: both maps return a chain of masks of "
          "sizes 1, 2, ..., n-1, so deleting the level-i mask leaves exactly two "
          "candidates to re-insert (|next \\ prev| = 2 at an interior level, and "
          "2 supersets/subsets at the ends) -- at most 2 facets share any ridge, "
          "at EVERY n, for either map.")
    L.check("A1.4a the artifact's claim that I4 'rebuilds the facet enumeration "
            "outright, so a ridge there CAN lie in >= 3 facets; its zero is the "
            "only one of the four that is a result'", worst >= 3)
    print()

    return L.finish("a1_counts")


def twelfth_count_demo():
    """Add a TWELFTH printed count to the artifact, leave `verify_e35b.py`
    untouched, and read V6's completeness row off the result.

    Done on a COPY of the tree, in a temporary directory.  Nothing under audit is
    edited: the point is what V6 does when the artifact grows, not what happens to
    this worktree.
    """
    tmp = tempfile.mkdtemp(prefix="fcb2_v6_")
    try:
        code = os.path.join(tmp, "code")
        os.makedirs(code)
        shutil.copytree(L.FACE_GEOMETRY, os.path.join(code, "face_geometry"))
        shutil.copytree(REPAIR, os.path.join(code, "face_geometry_repair_e35b"))
        cpath = os.path.join(code, "face_geometry", "controls.py")
        src = open(cpath).read()
        marker = 'print("  measured, not scored:")'
        assert marker in src, "the insertion point moved"
        src = src.replace(
            marker,
            marker + '\n    print("    * A TWELFTH PRINTED COUNT, added by '
                     'mg-fcb2 to test V6\'s completeness row: the population has '
                     '%d posets and %d of them have |L(P)| = 1" % '
                     '(N, sum(1 for P in ps if len(linear_extensions(P)) == 1)))',
            1)
        open(cpath, "w").write(src)
        art = os.path.join(code, "face_geometry", "controls_output.txt")
        with open(art, "w") as fh:
            subprocess.run([sys.executable, "controls.py", "5"], stdout=fh,
                           cwd=os.path.join(code, "face_geometry"), check=False)
        r = subprocess.run([sys.executable, "verify_e35b.py"], capture_output=True,
                           text=True, cwd=os.path.join(code, "face_geometry_repair_e35b"))
        rows = [l for l in r.stdout.splitlines() if "every printed count is classified" in l]
        extra = "A TWELFTH PRINTED COUNT" in open(art).read()
        print("    the artifact in the copy carries the twelfth count: %s" % extra)
        print("    V6's completeness row there: %s"
              % (rows[0].strip() if rows else "NOT FOUND"))
        if not rows or not extra:
            return "INCONCLUSIVE"
        return "GREEN" if "[PASS]" in rows[0] else "RED"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
