"""mg-5035 -- shared instrument for the repair of `figures()`'s false
git-revision exclusion.

WHAT THIS FILE MAY NOT CONTAIN, GIVEN WHAT IT REPAIRS.  The defect being
repaired is a RULE THAT DID NOT DO WHAT ITS OWN LABEL SAID.  A library for that
repair may not open with a fresh copy of the rule under repair, and it may not
carry a docstring describing behaviour it does not have.  So:

  THE `BEFORE` RULE IS NOT RE-IMPLEMENTED HERE.  It is IMPORTED, from the one
  place in the arc that still has it: `lib56dc.figures(line, small=2)`.
  mg-56dc's parameterised third copy is byte-for-byte the pre-repair
  `lib7522.figures` semantics -- same three exclusions, and `small=2` is the
  same floor as `if v > 2`.  mg-bf79 kept that copy deliberately as "the only
  rule able to check the other two", and this ticket is the occasion it was
  kept for.  A/B here is therefore

      BEFORE  lib56dc.figures(line, small=2)     -- untouched by mg-5035
      AFTER   lib7522.figures(line)              -- repaired by mg-5035

  and neither side is written by me.  Reconstructing the deleted rule myself
  would have made the delta a fact about my reconstruction.

  `lib56dc` IS ALSO THIS TICKET'S POSITIVE CONTROL.  It is left unrepaired on
  purpose (PREDICTIONS/P2b).  A negative needs an instrument that could have
  shown the positive, and every "excluded now" row printed by this tree is
  printed beside a `lib56dc` reading that still says FIGURE.  If that column
  ever stops saying FIGURE, the control has stopped being one and the rows
  below stop being evidence.

THE GIT OBJECT DATABASE IS AN EVALUATION ORACLE HERE AND IS NOT IN THE SHIPPED
RULE.  `resolves()` below is used to LABEL tokens when scoring precision and
recall.  mg-bf79 rejected resolves-as-an-object as a RULE and was right to;
using it to score a text-only rule is a different act and is named as different
so the two cannot be confused.  Nothing in `lib7522.figures` calls it.

EVERY COUNT THIS TREE PRINTS NAMES ITS POPULATION AND ITS GRAIN IN ITS OWN
LABEL, not in a column header and not on the line above.  That is mg-bf79's
standard, adopted rather than re-invented, and `f4_self.py` measures it.
"""

import os
import re
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True,
                      check=True).stdout.strip()

sys.path.insert(0, os.path.join(REPO, "code", "runner_exit_repair_7522"))
sys.path.insert(0, os.path.join(REPO, "code", "runner_exit_audit_56dc"))
sys.path.insert(0, os.path.join(REPO, "code", "runner_exit_repair_70c7"))

import lib7522 as L            # noqa: E402  AFTER  -- the repaired rule
import lib56dc as A            # noqa: E402  BEFORE -- the untouched control
import lib70c7 as C            # noqa: E402  the forwarder, checked not copied


def git(*args, ok=(0,)):
    """Run git in the repository root.  Returns stdout, or None on an allowed
    non-zero exit."""
    r = subprocess.run(("git",) + args, cwd=REPO,
                       capture_output=True, text=True)
    if r.returncode not in ok:
        raise RuntimeError("git %s -> %d: %s" % (args, r.returncode, r.stderr))
    return r.stdout if r.returncode == 0 else None


def read(path, default=""):
    try:
        with open(os.path.join(REPO, path), encoding="utf-8",
                  errors="replace") as fh:
            return fh.read()
    except OSError:
        if default is None:
            raise
        return default


_RESOLVED = {}


def resolves(token):
    """EVALUATION ORACLE ONLY -- does `token` name a git object here?

    NOT A RULE.  See this module's docstring: its answer is a property of this
    repository's object database on the day it is asked, which is exactly why
    it is unfit to decide what a figure is and perfectly fit to LABEL tokens
    when scoring a rule that never consults it.
    """
    if token not in _RESOLVED:
        r = subprocess.run(["git", "rev-parse", "--verify", "--quiet",
                            "%s^{object}" % token],
                           cwd=REPO, capture_output=True, text=True)
        _RESOLVED[token] = (r.returncode == 0)
    return _RESOLVED[token]


# The SHAPE half of the repaired rule, re-stated here for enumeration only --
# this is the candidate population, not the decision.  The decision is
# `lib7522._is_declared_revision` and is never re-implemented in this tree.
_SHAPED = re.compile(r"(?<![\w.])(\d{7,40})(?![\w.])")


SELF = "code/figures_revision_repair_5035"


def corpus(include_self=False):
    """[path] -- every tracked `.md`, `.txt` and `.py` under the repository.

    One unit is one FILE.

    THE SUBJECT POPULATION EXCLUDES THIS TREE, AND THAT IS A DECISION WITH A
    REASON.  The question every census here asks is *what does the repair do to
    the arc?* -- and the arc is what existed before this repair.  Once this
    directory is committed, its own transcripts are tracked `.txt` files full
    of lines like `at 3738079 the census`, printed BY the probes AS EVIDENCE.
    Counting them makes the instrument its own subject.

    THE FIRST RUN AFTER COMMITTING DID EXACTLY THAT AND THE NUMBERS MOVED:
    the claim-side delta went 50 -> 109 and the backing-corpus loss went 1 -> 0,
    the second because `f2_contamination.py` PRINTS `478508621408` as one of the
    integers it reports leaving the corpus, which puts it back in.  A census
    that reports a number and thereby changes it is worth more as a recorded
    defect than as a tidied one, so both populations are printed everywhere and
    the SUBJECT one carries the headline.

    Pass `include_self=True` for the whole-repository figure.
    """
    return sorted(p for p in git("ls-files").split()
                  if p.endswith((".md", ".txt", ".py"))
                  and (include_self or not p.startswith(SELF)))


def shaped_occurrences(paths=None):
    """[(path, lineno, token, line)] -- every revision-SHAPED token in `paths`.

    One unit is one OCCURRENCE: the same token on two lines is two.  Shape only
    -- 7 to 40 decimal digits, no separator.  Whether each is DECLARED a
    revision is `lib7522._is_declared_revision`'s answer and not this
    function's; keeping the two apart is the whole point of the rule.
    """
    out = []
    for p in (corpus() if paths is None else paths):
        for i, line in enumerate(read(p).splitlines(), 1):
            for m in _SHAPED.finditer(line):
                out.append((p, i, m.group(1), line))
    return out


def verdicts(line):
    """(before, after) -- the two figure lists for one line.

    BEFORE is mg-56dc's untouched copy at the pre-repair floor; AFTER is the
    repaired rule.  Both are imported.
    """
    return A.figures(line, small=2), L.figures(line)


def dropped(line):
    """[int] -- what the repair removes from this line, in order.

    A multiset difference, not a set difference: a line naming the same
    revision twice loses it twice, and a count that says otherwise would be at
    the wrong grain.
    """
    before, after = verdicts(line)
    rest = list(after)
    out = []
    for v in before:
        if v in rest:
            rest.remove(v)
        else:
            out.append(v)
    return out


def transcripts():
    """[path] -- every committed `out_*.txt` under `code/`.

    One unit is one TRANSCRIPT FILE.  This is mg-70c7's `outs()` population
    restated as a path list; the rule that builds it is imported below so this
    is a name for a population and not a second implementation of one.
    """
    return sorted(p for p in git("ls-files").split()
                  if p.startswith("code/")
                  and os.path.basename(p).startswith("out_")
                  and p.endswith(".txt")
                  and not p.startswith(SELF))


# --- printing, borrowed in shape from mg-bf79 so the ledger is comparable ---

def bar(text):
    print("=" * 74)
    print(text)
    print("=" * 74)
    print()


def hdr(text):
    print("-" * 74)
    print(text)
    print("-" * 74)
    print()


def plain(label, value):
    """One COUNT ROW.  The label carries the population and the grain, because
    a grain that lives in a column header is the defect mg-56dc's O1 was."""
    print("      %-62s %6s" % (label, value))


def finding(fid, text):
    return "FINDING: %s %s" % (fid, text)
