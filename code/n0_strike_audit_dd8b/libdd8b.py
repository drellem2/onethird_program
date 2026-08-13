"""mg-dd8b shared corpus reader -- READ AT A DECLARED COMMIT (mg-20ee).

WHY THIS EXISTS.  s1, s2, s3 and s4 all print `path:NNN` -- line numbers into
`docs/` documents this instrument does not own -- and s1's and s2's headline
COUNTS are counts over those same documents.  All four read them from the
WORKING TREE, so the transcripts were NON-REPRODUCIBLE BY CONSTRUCTION and had
already gone stale: mg-24fb amended the mg-33f5 document after these ran, and a
worktree re-run on 2026-08-13 moves the primary term from 8 occurrences on 7
lines to 9 on 8, and every address with it.

Here the counts are not merely corpus-valued -- COUNTING IS THE CENSUS'S WHOLE
JOB -- so a live read does not just relocate a reader, it silently re-answers
the question at a corpus the verdict was never taken over.

THE FIX IS mg-c824's, PROVEN on code/c3_audit_a94c3/a4_census.py: pin the bytes,
do not reformat the numbers.  A line number into someone else's file is a
volatile address by nature and no printing convention makes one stable; what CAN
be made stable is THE THING ADDRESSED.

AS_OF IS CHOSEN ON A MEASUREMENT, NOT ON A NAME, and the obvious name was WRONG.
80bd591 is the commit that CARRIES these four transcripts, and it does not
reproduce them: STATE.md gained a line before it landed, so s3's last strong-form
assertion sits at :210 there against the committed :209.  The transcripts were
written on a polecat branch and the branch was rebased onto a main that had
already moved -- so the commit a transcript is COMMITTED AT is not in general the
commit it was MEASURED AT, and taking the first for the second is how a pinning
silently re-measures.

AS_OF = dafe759 is the NEWEST ancestor at which ALL FOUR committed transcripts
reproduce with ZERO differing lines -- checked before the transcripts were
touched, which is step 1 of the numbers-neutrality method passing.  It is also an
ANCESTOR OF main, so this pin does not depend on a polecat branch surviving.

One measurement trap worth keeping, because it sent the first attempt to the
wrong commit: s1 prints `len(text)`, which is CHARACTERS, and these documents are
full of multibyte `—`/`⟹`/`₀`.  A byte count disagrees with the transcript by 302
and makes a matching revision look like a mismatched one.
"""
import os
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#: The commit whose bytes every address and every count below is taken over.
AS_OF = "dafe75910f731927affdf366457d681e262acf62"

#: Override, for re-measuring against a different corpus: any commit-ish, or the
#: literal WORKTREE.  Unset is the pinned default and is the only value that
#: reproduces the committed transcripts.
AT = os.environ.get("N0_STRIKE_AT", "").strip() or AS_OF


def _git(*args):
    got = subprocess.run(["git", "-C", REPO, *args], capture_output=True)
    if got.returncode != 0:
        raise SystemExit(
            "mg-dd8b: cannot read the corpus at %s: %s\n"
            "  (N0_STRIKE_AT=%r; unset it for the pinned run.)"
            % (AT, got.stderr.decode("utf-8", "replace").strip(), AT))
    return got.stdout.decode("utf-8", "replace")


def exists_at(rel):
    if AT == "WORKTREE":
        return os.path.exists(os.path.join(REPO, rel))
    got = subprocess.run(["git", "-C", REPO, "cat-file", "-e", "%s:%s" % (AT, rel)],
                         capture_output=True)
    return got.returncode == 0


def read_at(rel):
    """REPO/rel as of AT.  Every `rel:NNN` this instrument prints is an offset
    into THESE bytes, so pinning the bytes is what pins the addresses."""
    if AT == "WORKTREE":
        with open(os.path.join(REPO, rel), encoding="utf-8", errors="replace") as fh:
            return fh.read()
    return _git("show", "%s:%s" % (AT, rel))


def log_at(rel):
    """The commits touching `rel` UP TO AT.

    s4 asked this of `origin/main`, which grows: the answer was 'how many
    commits have touched this file by the time you happen to run me'.  Asked of
    AT it is a property of the pinned corpus, like every other number here."""
    ref = "origin/main" if AT == "WORKTREE" else AT
    return [l for l in _git("log", "--oneline", ref, "--", rel).strip().split("\n")
            if l.strip()]


def stamp(script):
    """The as-of block every transcript of this instrument opens with."""
    return """\
==============================================================================
AS-OF STAMP -- WHICH LINES BELOW ARE ADDRESSES AND WHICH ARE FINDINGS (mg-20ee)
==============================================================================
  corpus read at : %s
      %s

  EVERY `:NNN` BELOW IS AN ADDRESS, NOT A FINDING.  Each is an offset into a
  `docs/` file this instrument DOES NOT OWN, and it moves whenever another
  ticket amends that file.  They are valid at the commit named above and
  nowhere else.  THE QUOTED LINE UNDER EACH ADDRESS IS THE PRIMARY ADDRESS --
  it survives the file moving; the number does not.

  AND SO ARE THE COUNTS, which is the part that matters here: the occurrence
  and line counts, the per-document line/character sizes, and the commit
  tallies are all taken OVER THE PINNED CORPUS.  This instrument's job IS to
  count, so a live read would not merely relocate a reader -- it would
  re-answer the question at a corpus the verdict was never taken over.  It had
  already done so: mg-24fb amended the mg-33f5 document after these transcripts
  were written.

  WHAT IS STABLE: the term sets, the controls, and the adjudication each
  section reaches.  Run with no environment set and this transcript reproduces
  BYTE-IDENTICALLY.  To ask the same questions of the CURRENT corpus:

      N0_STRIKE_AT=HEAD python3 %s      (or =WORKTREE, or any commit)

  which RE-MEASURES AND RE-ADDRESSES.  Both runs are correct about their own
  corpus, and their disagreeing is not a defect in either.
""" % (AT,
       "AS_OF, the pinned default" if AT == AS_OF
       else "OVERRIDE via N0_STRIKE_AT -- NOT the as-of stamp " + AS_OF[:7],
       script)
