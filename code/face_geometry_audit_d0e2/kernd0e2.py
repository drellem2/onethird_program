"""mg-d0e2 audit kernel -- run a control battery under a SOURCE MUTATION and
compare the artifact BYTE FOR BYTE.

This is the deletion test as mg-1c80 defined it and as mg-5f9a was told to pass:
remove from the predicate the gate the artifact's explanation names, regenerate
the artifact, and see whether it moves.  A gate whose removal leaves the bytes
alone is not what produced them, whatever the prose says.

WHY THIS FILE EXISTS SEPARATELY FROM `../face_geometry_instr_5f9a/d2_deletion.py`.
That one is the repair's own instrument and it reports the repair passing.  An
audit that runs the subject's own test learns only that the test is
deterministic.  So the mutations here are re-derived from the source text of
`absorb_trace` rather than imported, the byte comparison is against a baseline
this file generates itself, and the mutation set is a SUPERSET: mg-5f9a ran the
deletion on two of the four gate labels its own `ABSORB_GATES` tuple defines,
and the ticket says every gate the explanation names.

NOTHING UNDER ../face_geometry IS WRITTEN.  Each run copies the package to a
fresh temporary directory, edits the copy, and runs `controls.py` there as a
subprocess with stdout captured as BYTES -- not through `tee`, whose exit status
in a pipeline is the last command's and would mask a battery exiting 1.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.normpath(os.path.join(HERE, "..", "face_geometry"))


def _load(path):
    with open(path, "r") as fh:
        return fh.read()


def apply_edits(text, edits, where):
    """Apply (old, new) pairs, requiring each `old` to occur EXACTLY ONCE.

    An edit that matches twice, or not at all, is a silently different
    experiment -- the failure mode that lets a deletion test report on a
    deletion it did not make.  So it raises instead.
    """
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            raise AssertionError(
                "%s: anchor occurs %d times, expected exactly 1:\n%r"
                % (where, n, old))
        text = text.replace(old, new, 1)
    return text


def run_battery(edits_by_file, tag, source_pkg=None):
    """Copy the package, apply the edits, run controls.py, return
    (stdout_bytes, exit_status).  `edits_by_file` maps a basename to a list of
    (old, new) pairs; an empty map is the unmutated baseline."""
    src = source_pkg or PKG
    tmp = tempfile.mkdtemp(prefix="d0e2_%s_" % tag)
    try:
        dst = os.path.join(tmp, "face_geometry")
        shutil.copytree(src, dst)
        for base, edits in edits_by_file.items():
            path = os.path.join(dst, base)
            # READ, THEN OPEN FOR WRITING.  `open(path, "w")` truncates the
            # moment it is evaluated, and Python evaluates it before the
            # argument expression -- so writing this as one statement fed
            # `apply_edits` an empty file and every anchor "occurred 0 times".
            # The anchor-count assertion is what turned that into a stack trace
            # instead of a battery run on unmutated source reported as a
            # deletion test.
            text = apply_edits(_load(path), edits, "%s/%s" % (tag, base))
            with open(path, "w") as fh:
                fh.write(text)
        proc = subprocess.run([sys.executable, "controls.py"],
                              cwd=dst, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
        return proc.stdout, proc.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------------------
# THE MUTATIONS.  Each is a deletion of ONE named gate from the predicate,
# written as the exact source lines it removes, so that what was deleted is
# readable here and not only describable.
# ---------------------------------------------------------------------------

DEL_SHAPE = [
    ("""    m = len(A)
    if m != len(B):
        return Trace(False, "shape", 0)
    for i in range(m):
        if len(A[i]) != len(B[i]):
            return Trace(False, "shape", 0)
        if A[i][i] != B[i][i]:""",
     """    m = len(A)
    for i in range(m):
        if A[i][i] != B[i][i]:"""),
]

DEL_DIAGONAL = [
    ("""        if A[i][i] != B[i][i]:
            return Trace(False, "diagonal", 0)
        for j in range(m):""",
     """        for j in range(m):"""),
]

DEL_MAGNITUDE = [
    ("""        for j in range(m):
            if abs(A[i][j]) != abs(B[i][j]):
                return Trace(False, "magnitude", 0)
    parent = list(range(m))""",
     """    parent = list(range(m))"""),
]

DEL_PARITY = [
    ("""            if ri == rj:
                if pi ^ pj != need:
                    return Trace(False, "parity", signs_read)
            else:""",
     """            if ri == rj:
                pass
            else:"""),
]

DEL_SIGNS_READ = [
    ("""            signs_read += 1
            need = 0""",
     """            need = 0"""),
]

# Not a deletion: the same two forced gates in the OTHER order.  Every answer is
# unchanged by construction; only the label the trace returns can move.  It is
# here because "the printed gate depends on the order" is the claim the artifact
# now makes about itself, and a claim about order is tested by changing it.
SWAP_ORDER = [
    ("""        if A[i][i] != B[i][i]:
            return Trace(False, "diagonal", 0)
        for j in range(m):
            if abs(A[i][j]) != abs(B[i][j]):
                return Trace(False, "magnitude", 0)""",
     """        for j in range(m):
            if abs(A[i][j]) != abs(B[i][j]):
                return Trace(False, "magnitude", 0)
        if A[i][i] != B[i][i]:
            return Trace(False, "diagonal", 0)"""),
]

# The SECOND place the artifact names gates, and no ticket's list names it: the
# exhaustive companion whose counts are what the artifact offers as proof that a
# trace label is or is not load-bearing ("both forced gates violated on 58").
DEL_DIAGONAL_FROM_VIOLATIONS = [
    ("""    if any(A[i][i] != B[i][i] for i in range(m)):
        bad.add("diagonal")""",
     """    if False:
        bad.add("diagonal")"""),
]

DEL_MAGNITUDE_FROM_VIOLATIONS = [
    ("""    if any(abs(A[i][j]) != abs(B[i][j])
           for i in range(m) for j in range(m)):
        bad.add("magnitude")""",
     """    if False:
        bad.add("magnitude")"""),
]

# The routing quantity the repair split out and the routing row names by name.
INVERT_DIAGONAL_MOVES = [
    ("""    return any(A[i][i] != B[i][i] for i in range(len(A)))""",
     """    return not any(A[i][i] != B[i][i] for i in range(len(A)))"""),
]

FC = "face_complex.py"


def report(label, base_bytes, out, status, pred_change, pred_exit):
    """Print one deletion-test line and return True if it matched prediction."""
    changed = out != base_bytes
    ok = (changed == pred_change) and (status == pred_exit)
    print("  %-34s bytes %6d -> %6d  %-16s exit %d   predicted %s/%d  %s"
          % (label, len(base_bytes), len(out),
             "CHANGED" if changed else "BYTE-IDENTICAL",
             status,
             "changed" if pred_change else "identical", pred_exit,
             "MATCH" if ok else "*** MISS ***"))
    return ok, changed
