"""mg-e7bc audit kernel -- an INDEPENDENT instrument for auditing mg-04a8.

WHY IT DOES NOT IMPORT THE SUBJECT'S KERNEL.  `../face_geometry_instr_5f9a/
kern5f9a.py` is the repair's own runner and `../face_geometry_audit_d0e2/
kernd0e2.py` is the previous audit's.  Running either learns that the tool is
deterministic.  So the mutation runner, the row parser, the summary parser and
the corruption generators below are written here from the source text.

THE ONE THING THIS FILE DOES IMPORT FROM THE SUBJECT is the repaired label check
itself -- `check_labels` out of `d2_deletion.py` -- because that function IS the
subject of the primary measurement.  Auditing it means running THAT code, not a
paraphrase of it.  Everything the check is fed (the artifact text, the exit code,
the registered fail-set, the baseline CANNOT FAIL set) is derived here.

NOTHING UNDER ../face_geometry IS WRITTEN.  Every mutation is applied to a copy
in a temporary directory; every battery run captures stdout as BYTES through
`subprocess.run` rather than a pipeline, whose exit status in POSIX sh is the
last command's and would mask a battery exiting 1 (mg-f922).

PREDICTIONS ARE REGISTERED IN THE `PREDICTIONS` TABLE OF EACH SCRIPT, printed
before the runs, and scored afterwards.  A miss is printed as a miss and kept.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
PKG = os.path.join(ROOT, "code", "face_geometry")
INSTR = os.path.join(ROOT, "code", "face_geometry_instr_5f9a")
ART = os.path.join(PKG, "controls_output.txt")
FC = "face_complex.py"

BAR = "=" * 78
MARKERS = ("[CANNOT FAIL]", "[PASS]", "[FAIL]")   # longest first: prefix safety

SCORE = []
FINDINGS = []


def claim(ok, text, differs_under, detail=""):
    """A claim of THIS instrument's own.  `ok` False sets the exit status.

    `differs_under` is carried here for the same reason mg-d0e2 required it of
    the subject: an audit that does not state what would move its own answers
    is asking to be believed on the same terms as the thing it is auditing.
    Section 3 of this audit tests the subject's statements by making the change;
    the ones below are written to the same standard and several are tested the
    same way.
    """
    SCORE.append(ok)
    print("  [%s] %s" % ("HOLDS " if ok else "BROKEN", text))
    if detail:
        print("        " + detail)
    print("        WOULD DIFFER UNDER: %s" % differs_under)


def finding(fires, text):
    """A fact about the SUBJECT, kept apart from `claim` deliberately.

    `claim` BROKEN means this instrument is wrong; `finding` firing means
    mg-04a8 is.  Only the first sets the exit status, so this audit can be run
    in CI by anyone without its exit code meaning two different things.
    """
    if fires:
        FINDINGS.append(text)
    print("  [%s] %s" % ("FINDING" if fires else "clear  ", text))


def head(title):
    print()
    print("-" * 78)
    print(title)
    print("-" * 78)


def read(path):
    with open(path) as fh:
        return fh.read()


# ------------------------------------------------------------------ parsing
def scored_rows(text):
    """(label, name) for every line whose FIRST non-space characters are a
    marker.  Written here rather than imported: the row population is the
    denominator of almost every number in this audit, and taking it from the
    subject would make "43 rows" a fact about the subject's own parser.
    """
    rows = []
    for ln in text.split("\n"):
        s = ln.strip()
        for m in MARKERS:
            if s.startswith(m):
                rows.append((m, s[len(m):].strip()))
                break
    return rows


def summary_names(text, header):
    """Names listed under a `CONTROLS ...` header in the battery's bottom line.

    The battery prints two such blocks and never both: `summarise` returns as
    soon as anything failed, so on a failing run the CANNOT FAIL list is absent.
    Names are truncated to 75 chars by the battery, so callers match by prefix.
    """
    out, on = [], False
    for ln in text.split("\n"):
        if ln.startswith(header):
            on = True
            continue
        if on and ln.startswith("   - "):
            out.append(ln[5:].rstrip().rstrip("."))
            continue
        if on and ln.strip():
            on = False
    return out


def baseline_cannot(text):
    return summary_names(text, "CONTROLS: 0 failures, but")


# ------------------------------------------------------- corruption library
def _split_marker(ln):
    s = ln.lstrip()
    for m in MARKERS:
        if s.startswith(m):
            return ln[:len(ln) - len(s)], m, s[len(m):]
    return None


def retag_rows(text, want, which=lambda i, m: True):
    """Replace the marker of selected scored rows with `want`, touching nothing
    else -- not the row's text, not the bottom-line summary.

    LEAVING THE SUMMARY ALONE IS WHAT MAKES THE RESULT A CORRUPTED ARTIFACT
    rather than a failing run.  A battery that really failed would print a
    matching `CONTROLS FAILED:` block; a corruption does not, and the
    disagreement between the two channels is the thing a non-vacuous label
    check has to notice.  `which(index, marker)` selects which rows to hit.
    """
    out, i = [], 0
    for ln in text.split("\n"):
        parts = _split_marker(ln)
        if parts is None:
            out.append(ln)
            continue
        indent, marker, rest = parts
        out.append(indent + (want if which(i, marker) else marker) + rest)
        i += 1
    return "\n".join(out)


def drop_row(text, index=0):
    """Delete one scored row LINE outright.  A corruption no list in the ticket
    names and the one direction neither check was designed around."""
    out, i, dropped = [], 0, None
    for ln in text.split("\n"):
        parts = _split_marker(ln)
        if parts is None:
            out.append(ln)
            continue
        if i == index:
            dropped = parts[1] + parts[2][:60]
            i += 1
            continue
        i += 1
        out.append(ln)
    return "\n".join(out), dropped


def lie_in_summary(text, name):
    """Rows untouched; the BOTTOM LINE gains a `CONTROLS FAILED:` block naming a
    row that in fact passed.  The mirror image of `retag_rows`: here the rows
    are honest and the summary is not."""
    block = "CONTROLS FAILED:\n   - %s.\n" % name[:75]
    return text.replace("CONTROLS: 0 failures, but",
                        block + "CONTROLS: 0 failures, but", 1)


# --------------------------------------------------------- mutation running
def apply_edits(text, edits, where):
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            raise AssertionError("%s: anchor occurs %d times, expected 1:\n%r"
                                 % (where, n, old))
        text = text.replace(old, new, 1)
    return text


def run_battery(edits_by_file, tag):
    """Copy `face_geometry`, apply the edits, run `controls.py`, return
    (stdout bytes, exit status).  An empty map is the unmutated baseline."""
    tmp = tempfile.mkdtemp(prefix="e7bc_%s_" % tag)
    try:
        dst = os.path.join(tmp, "face_geometry")
        shutil.copytree(PKG, dst)
        for base, edits in edits_by_file.items():
            path = os.path.join(dst, base)
            text = apply_edits(read(path), edits, "%s/%s" % (tag, base))
            with open(path, "w") as fh:
                fh.write(text)
        proc = subprocess.run([sys.executable, "controls.py"], cwd=dst,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
        return proc.stdout, proc.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------------------
# THE MUTATIONS, re-derived from the source text of `absorb_trace`,
# `gate_violations` and `diagonal_moves` in ../face_geometry/face_complex.py.
#
# The nine are the nine mg-d0e2 ran.  The two after them are this audit's own
# and no ticket's list names them: the `shape` gate has TWO return statements
# and mg-04a8 deletes them TOGETHER, on the stated ground that "they are one
# gate, and deleting one of two would leave the other answering".  That is an
# assertion about which branch its constructed pairs reach, and it is exactly
# the kind of assertion this lineage keeps finding to be untested.  So each
# return is deleted ALONE.
# ---------------------------------------------------------------------------
SHAPE_1 = [('''    m = len(A)
    if m != len(B):
        return Trace(False, "shape", 0)
    for i in range(m):''',
            '''    m = len(A)
    for i in range(m):''')]

SHAPE_2 = [('''        if len(A[i]) != len(B[i]):
            return Trace(False, "shape", 0)
        if A[i][i] != B[i][i]:''',
            '''        if A[i][i] != B[i][i]:''')]

DEL_SHAPE = SHAPE_1 + SHAPE_2

DEL_DIAGONAL = [('''        if A[i][i] != B[i][i]:
            return Trace(False, "diagonal", 0)
        for j in range(m):''',
                 '''        for j in range(m):''')]

DEL_MAGNITUDE = [('''        for j in range(m):
            if abs(A[i][j]) != abs(B[i][j]):
                return Trace(False, "magnitude", 0)
    parent = list(range(m))''',
                  '''    parent = list(range(m))''')]

DEL_PARITY = [('''            if ri == rj:
                if pi ^ pj != need:
                    return Trace(False, "parity", signs_read)
            else:''',
               '''            if ri == rj:
                pass
            else:''')]

DEL_SIGNS_READ = [('''            signs_read += 1
            need = 0''', '''            need = 0''')]

SWAP_ORDER = [('''        if A[i][i] != B[i][i]:
            return Trace(False, "diagonal", 0)
        for j in range(m):
            if abs(A[i][j]) != abs(B[i][j]):
                return Trace(False, "magnitude", 0)''',
               '''        for j in range(m):
            if abs(A[i][j]) != abs(B[i][j]):
                return Trace(False, "magnitude", 0)
        if A[i][i] != B[i][i]:
            return Trace(False, "diagonal", 0)''')]

DEL_DIAG_FROM_VIOLATIONS = [('''    if any(A[i][i] != B[i][i] for i in range(m)):
        bad.add("diagonal")''',
                             '''    if False:
        bad.add("diagonal")''')]

DEL_MAG_FROM_VIOLATIONS = [('''    if any(abs(A[i][j]) != abs(B[i][j])
           for i in range(m) for j in range(m)):
        bad.add("magnitude")''',
                            '''    if False:
        bad.add("magnitude")''')]

INVERT_ROUTING = [(
    '''    return any(A[i][i] != B[i][i] for i in range(len(A)))''',
    '''    return not any(A[i][i] != B[i][i] for i in range(len(A)))''')]

# The crux of the repair, made into a mutation: score the two constructed-pair
# rows against the PREDICATE'S OWN ANSWER instead of against the enumerated
# definition.  mg-04a8's own claims say this is what would put the two branches
# back out of reach; section 3 tests that statement by making the change.
BRUTEFORCE_TO_SELF = [(
    '''            truth = absorbable_bruteforce(A, B)           # the definition, enumerated''',
    '''            truth = tr.absorbable                        # MUTATION (mg-e7bc)''')]
