"""mg-5f9a -- shared kernel for the instrumented-predicate landing.

WHAT THIS LANDING HAD TO DO DIFFERENTLY.  Two previous tickets wrote a sentence
saying WHY `absorbable_by_diagonal_twist` answered as it did, and both sentences
were produced beside the predicate rather than by it:

  mg-8a12  read `diag_preserved` and printed "the off-diagonal signs actually
           decide".  mg-f1b2 refuted it.
  mg-da45  replaced it with `deciding_gate`, which tested ALL diagonals and then
           ALL magnitudes.  The predicate interleaves the two BY ROW, so the two
           orders named different gates on 57 of the 297 biting pairs, and
           mg-1c80's M2 -- delete the gate the artifact called decisive --
           regenerated the artifact BYTE-IDENTICALLY.

So this landing does not write a third reason.  The predicate is instrumented:
`face_complex.absorb_trace` returns the gate it returned at and the number of
signs it read, and `absorbable_by_diagonal_twist` is a wrapper over it.  What
the rows print comes out of the code path.

WHAT THIS FILE IMPORTS, and it matters (mg-da45's rule, kept).  `face_complex`
and `posets` and nothing else.  `controls.py` is never imported: it is run as a
subprocess and read as bytes, so it cannot supply the evidence that it is right.
The pair (E.L^rel.E, D-A) is rebuilt here from `top_laplacians` and
`at_laplacian` rather than taken from `controls.claim1_pair`.

AND THE DECISION IS RE-DECIDED HERE, twice, without the union-find: by BFS
2-colouring of the sign-constraint graph, and (where m <= 8) by brute force over
all 2^m sign vectors.  A refactor of a decision procedure is only decision-
preserving if something outside it says so.
"""

import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                "..", "face_geometry")))

from face_complex import (                                          # noqa: E402
    top_laplacians, at_laplacian, linear_extensions, perm_sign,
)

FG = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                  "face_geometry"))
BAR = "=" * 78

MODES = ["ridge_facets", "split_free_as_interior", "ridge_drop",
         "facet_offbyone"]
ROW = {"ridge_facets": "I1", "split_free_as_interior": "I2",
       "ridge_drop": "I3", "facet_offbyone": "I4"}


def head(title):
    print("\n" + BAR + "\n" + title + "\n" + BAR)


def pair(P, sign_mode="true", incidence_mode="true"):
    """(E . L^rel_top . E, D - A) -- claim (1)'s two sides, rebuilt here."""
    td = top_laplacians(P, sign_mode=sign_mode, incidence_mode=incidence_mode)
    les, L = td["les"], td["L_rel"]
    s = [perm_sign(w) for w in les]
    m = len(les)
    twisted = [[s[i] * L[i][j] * s[j] for j in range(m)] for i in range(m)]
    return twisted, at_laplacian(P)[1]


def eq(A, B):
    return len(A) == len(B) and all(
        len(A[i]) == len(B[i]) and A[i] == B[i] for i in range(len(A)))


# ------------------------------------------------------------------ deciders
def absorbable_2colour(A, B):
    """S.A.S == B for a diagonal sign matrix S?  Decided by 2-colouring the
    graph of forced sign products, with no union-find anywhere."""
    m = len(A)
    if m != len(B) or any(len(A[i]) != len(B[i]) for i in range(m)):
        return False
    for i in range(m):
        for j in range(m):
            if abs(A[i][j]) != abs(B[i][j]):
                return False
            if i == j and A[i][j] != B[i][j]:
                return False
    colour = [None] * m
    for root in range(m):
        if colour[root] is not None:
            continue
        colour[root] = 0
        stack = [root]
        while stack:
            x = stack.pop()
            for y in range(m):
                if x == y or A[x][y] == 0:
                    continue
                need = 0 if B[x][y] == A[x][y] else 1
                want = colour[x] ^ need
                if colour[y] is None:
                    colour[y] = want
                    stack.append(y)
                elif colour[y] != want:
                    return False
    return True


def absorbable_bruteforce(A, B):
    """The definition, enumerated: is there s in {+1,-1}^m with s_i A_ij s_j =
    B_ij for every i, j?  Only used where m <= 8."""
    m = len(A)
    if m != len(B) or any(len(A[i]) != len(B[i]) for i in range(m)):
        return False
    for bits in range(1 << m):
        s = [1 - 2 * ((bits >> i) & 1) for i in range(m)]
        if all(s[i] * A[i][j] * s[j] == B[i][j]
               for i in range(m) for j in range(m)):
            return True
    return False


# ------------------------------------------------- the reason that was wrong
def priority_gate(A, B):
    """mg-da45's `deciding_gate`, VERBATIM, kept here as the thing this landing
    replaced -- ALL diagonals tested, then ALL magnitudes.

    It is not called by anything in `face_geometry` any more.  It lives here so
    the disagreement mg-1c80 measured can be re-measured against the trace the
    predicate now emits, rather than taken on trust from the audit's transcript.
    """
    m = len(A)
    if m != len(B) or any(len(A[i]) != len(B[i]) for i in range(m)):
        return "shape"
    if any(A[i][i] != B[i][i] for i in range(m)):
        return "diagonal"
    if any(abs(A[i][j]) != abs(B[i][j]) for i in range(m) for j in range(m)):
        return "magnitude"
    return "parity"


# ------------------------------------------------------- mutation machinery
def mutate_tree(edits, src_files=None):
    """Copy `face_geometry` to a temporary directory, apply (file, old, new)
    edits to the copy, and return the directory.

    NOTHING under ../face_geometry is written.  `old` must occur exactly once in
    its file; a patch that does not apply is an error and not a silent pass,
    because a mutation that was never applied looks exactly like a mutation the
    battery did not notice.
    """
    tmp = tempfile.mkdtemp(prefix="mg5f9a-")
    for f in (src_files or os.listdir(FG)):
        s = os.path.join(FG, f)
        if os.path.isfile(s):
            shutil.copy2(s, os.path.join(tmp, f))
    for fname, old, new in edits:
        path = os.path.join(tmp, fname)
        text = open(path).read()
        if text.count(old) != 1:
            raise SystemExit("patch anchor occurs %d times in %s, expected 1:\n%r"
                             % (text.count(old), fname, old[:120]))
        open(path, "w").write(text.replace(old, new))
    return tmp


def run_controls(cwd, nmax=5):
    """Run the control battery in `cwd` and return (stdout, exit code).  Never
    tee'd: the committed artifact is not touched by any run in this instrument."""
    r = subprocess.run([sys.executable, "controls.py", str(nmax)], cwd=cwd,
                       capture_output=True, text=True)
    return r.stdout, r.returncode


def write_main_tree(files):
    """Materialise `main`'s copy of the named face_geometry files in a temp dir.

    Used for the BEFORE half of the deletion test: mg-1c80's finding is that the
    deletion left the artifact byte-identical AT THAT COMMIT, and a landing that
    only shows the AFTER half is asking to be believed about the before.
    """
    tmp = tempfile.mkdtemp(prefix="mg5f9a-main-")
    repo = os.path.abspath(os.path.join(FG, "..", ".."))
    for f in files:
        blob = subprocess.run(["git", "show", "main:code/face_geometry/" + f],
                              cwd=repo, capture_output=True)
        if blob.returncode != 0:
            raise SystemExit("cannot read main:code/face_geometry/%s" % f)
        open(os.path.join(tmp, f), "wb").write(blob.stdout)
    return tmp
