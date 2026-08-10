"""lib_a71f -- shared definitions for mg-a71f.

IMPORTS `lib_1abe` RATHER THAN PARAPHRASING IT, for cf8e5's reason and not out
of thrift: this ticket REPAIRS the census, so a second definition of the
census's own rules that agrees with them today is worse than no second
definition at all -- it would agree right up to the moment the repair made them
disagree, and then it would hide that.

The one thing that is NOT inherited is the provenance declaration.  cf8e5's
`lib_f8e5.Ledger` docstring records why, and it is the defect most worth
inheriting the fix for: `lib_1abe.Ledger.__init__` prints
`provenance_block("code/" + SELF_DIR)` with `SELF_DIR` bound in ITS module, so
an importer that does nothing declares the CENSUS's digest as its own -- a TRUE
digest of the WRONG directory, which the R3 control passes because it agrees.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

sys.path.insert(0, os.path.join(REPO, "code", "transcript_census_1abe"))
import lib_1abe as C  # noqa: E402  -- the census's own definitions, imported

git = C.git
git_ok = C.git_ok
resolve = C.resolve
blob_at = C.blob_at
carrying_commit = C.carrying_commit
transcripts = C.transcripts
conclusion_verdict = C.conclusion_verdict
code_digest = C.code_digest
main_rev = C.main_rev

SELF_DIR = "census_timeout_a71f"
CENSUS_DIR = "code/transcript_census_1abe"

# The prior census, preserved in this directory VERBATIM rather than referred
# to by commit.  The ticket's constraint is "keep the old census's numbers
# beside it, do not overwrite", and a reader who has to run `git show` to see
# the number being corrected is a reader who will not.
PRIOR_T2 = os.path.join(HERE, "prior_1abe_t2_census_at_81214a9.txt")
PRIOR_AS_OF = "81214a9c02ee624dc1261c69db50d47ed659728f"

# THE PRE-REPAIR INSTRUMENT, NAMED BY BLOB AND NOT BY COMMIT, AND NOT BY
# `PRIOR_AS_OF` EITHER.  Two defects of mine live in this constant.
#
# (1) a1's first draft read the pre-repair source at `PRIOR_AS_OF`, on the
#     reasoning that the published figures are facts about that commit.  They
#     are -- and `code/transcript_census_1abe/t2_census.py` DOES NOT EXIST
#     THERE.  `81214a9` is the revision the census MEASURED; the census's own
#     code was committed after the run that measured it.  The control refused
#     with a SELF-ERROR on its first execution, which is the only reason this
#     comment is not a false one.
# (2) the obvious fix -- `git log -1 main -- t2_census.py` -- is a moving ref
#     with a subject that walks out from under it.  The moment mg-a71f merges,
#     `main`'s carrying commit for that path IS THE REPAIR, and the arm that
#     checks "the pre-repair guard looked like this" would fail forever, on a
#     true statement, for the same reason `audit_c067/out_c1_rebase.txt` fails.
#     Committing that defect inside the ticket that annotates it would have
#     been the whole arc in one file.
#
# So the pre-repair source is pinned by its BLOB sha, which is this census's
# own remedy (`code_digest`: "NOT a commit sha -- a commit sha is displaced by
# every rebase, a blob digest is not"), applied to the instrument that proposed
# it.  `5e2e4d8` is where the blob was found; the blob is what is read.
BEFORE_BLOB = "60c65a51f15958953e0c799fae9706b69a43a18f"
BEFORE_SEEN_AT = "5e2e4d824fa8e0916f28f43a86d015baa20467b3"


def blob_by_sha(sha):
    """Bytes of a blob by its own sha, or None.  Immune to every ref."""
    import subprocess
    r = subprocess.run(["git", "cat-file", "blob", sha], cwd=REPO,
                       capture_output=True)
    return r.stdout if r.returncode == 0 else None

C067 = "code/audit_c067/out_c1_rebase.txt"
C067_CARRIER = "47e56b3bd628682aff4d547a78b4001e3a05ae1d"
NOTE_END = "# ---- end of mg-a71f note; the transcript as committed follows ----"


def provenance_block(rev="HEAD"):
    return C.provenance_block("code/" + SELF_DIR, rev)


class Ledger(C.Ledger):
    """mg-1abe's ledger with the declaration pointed at THIS directory."""

    def __init__(self, title, reads_outside_tree=True):
        self.findings = 0
        self.self_errors = 0
        print("=" * 78)
        print(title)
        print("=" * 78)
        print("    " + C.provenance_block("code/" + SELF_DIR, "HEAD"))
        print("    %s %s" % (C.REACH_PREFIX,
                             "yes" if reads_outside_tree else "no"))
        if reads_outside_tree:
            print("    ^ THIS TRANSCRIPT IS NOT PINNABLE BY ANY TREE.  It reads"
                  " repository-global state\n      -- refs, history, the file "
                  "list of `main` -- so it is a fact about the object store as"
                  " it\n      stood at the run, and the NEXT commit anyone "
                  "makes displaces it.  Declaring that\n      is the only "
                  "honest thing an instrument in this class can do.")


# --------------------------------------------------------------------------
# THE TWO CLASSIFIERS, side by side.  Neither is imported: t2's bucketing lives
# inside a threaded worker holding a lock over three shared dicts, and there is
# no seam to call.  So both are TRANSCRIBED -- and a1 CHECKS each transcription
# against the source text it claims to be a transcription of, which is the only
# thing that makes a transcription admissible.
# --------------------------------------------------------------------------

def bucket_before(status, got, committed):
    """t2_census.py as it stood at `81214a9` -- the code that produced every
    published census figure.  `got is None` is the ONLY route to TIMED-OUT."""
    if got is None:
        if status == "timeout":
            return "TIMED-OUT"
        if status.startswith("failed"):
            return "RUNNER-FAILED"
        return "NOT-REGENERATED"
    if got == committed:
        return "REPRODUCES"
    return "DIFFERS"


def bucket_after(status, got, committed):
    """t2_census.py as repaired by mg-a71f.  The guard is the timeout STATUS,
    with one deliberate exception: byte-identical under a kill still
    REPRODUCES, because a truncated write cannot forge the whole blob."""
    if got is None or (status == "timeout" and got != committed):
        if status == "timeout":
            return "TIMED-OUT"
        if status.startswith("failed"):
            return "RUNNER-FAILED"
        return "NOT-REGENERATED"
    if got == committed:
        return "REPRODUCES"
    return "DIFFERS"


# --------------------------------------------------------------------------
# Census transcripts, read back as data.
# --------------------------------------------------------------------------

def parse_t2_rows(text):
    """{transcript-path-without-`code/`: (carry, verdict)} from a T2a table.

    T2a's row is fixed-width: 52 + 8 + 16 + 15 + detail.  Parsed by SPLITTING
    rather than by column offset, because a path longer than 52 chars is
    truncated by the producer and the columns then shift -- reading offsets
    would silently mis-key exactly the long rows.
    """
    rows = {}
    started = False
    for line in text.splitlines():
        if line.startswith("T2a --"):
            started = True
            continue
        if started and line.startswith("T2b --"):
            break
        if not started or not line.startswith("    "):
            continue
        f = line.split()
        if len(f) < 3 or f[0] in ("transcript",):
            continue
        if "/out_" not in f[0]:
            continue
        rows[f[0]] = (f[1], f[2])
    return rows


def parse_t2_counts(text):
    """{bucket: count} from a T2b table."""
    counts = {}
    started = False
    for line in text.splitlines():
        if line.startswith("T2b --"):
            started = True
            continue
        if started and line.startswith("T2c --"):
            break
        f = line.split()
        if started and len(f) >= 4 and f[1].isdigit() and f[2] == "of":
            counts[f[0]] = int(f[1])
    return counts


def parse_t2_flips(text):
    """Every path listed under `every FLIPS, named:`."""
    out, started = [], False
    for line in text.splitlines():
        if line.strip() == "every FLIPS, named:":
            started = True
            continue
        if started:
            s = line.strip()
            if not s or s == "(none)":
                break
            if not s.startswith("code/"):
                break
            out.append(s)
    return out
