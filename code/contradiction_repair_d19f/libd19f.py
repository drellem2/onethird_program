"""mg-d19f — shared helpers for the mg-51f4 / mg-28ff contradiction repair.

This ticket ADJUDICATES a contradiction between two landed canonical documents and then
REPAIRS the false one. Both halves are checkable and both are checked here rather than
asserted, for the reason mg-64cb's report gives in its own §3.3: a claim about another
document's text is exactly the kind of claim that gets carried outward without being read.

THE ONE THING THIS FILE MUST NOT DO is decide the contradiction by recency. mg-51f4's
document is the LATER of the two at its own commit and the EARLIER at HEAD (mg-28ff was
amended twice after mg-51f4 landed), so "the more recent document wins" answers the
question two different ways depending on which clock you read. The adjudication below is
over the TEXT OF mg-28ff AS mg-51f4 READ IT, at cb496e9, and over the underlying
measurement, and never over a timestamp.
"""

import os
import re
import subprocess

SELF_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(SELF_DIR, "..", ".."))

# The commit of mg-28ff that mg-51f4 read. mg-51f4's own doc landed at 2f76a01
# (2026-08-09T22:46:06+01:00); mg-28ff's repairs landed an hour later at b45aad8
# (23:48:52+01:00) and again at e35b51c. cb496e9 is mg-28ff's ONLY commit before 2f76a01,
# so it is not a choice -- it is the only text there was.
C_28FF_AS_READ = "cb496e9"
C_51F4_LANDING = "2f76a01"
C_28FF_REPAIR = "b45aad8"

DOC_51F4 = "docs/OneThird-SweepLoss-mg-51f4.md"
DOC_28FF = "docs/OneThird-L2-Conditionality-mg-28ff.md"
DOC_29FE = "docs/OneThird-L2-Conditionality-mg-29fe-IndependentAudit.md"


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args],
                          capture_output=True, text=True).stdout


def show(rev, path):
    return git("show", f"{rev}:{path}")


def head_lines(path):
    with open(os.path.join(REPO, path), encoding="utf-8") as fh:
        return fh.read().split("\n")


def find(lines, needle):
    """1-indexed line numbers whose text contains `needle`."""
    return [i + 1 for i, ln in enumerate(lines) if needle in ln]


def author_date(rev):
    return git("log", "-1", "--format=%ad", "--date=iso-strict", rev).strip()


def subject(rev):
    return git("log", "-1", "--format=%s", rev).strip()


def item_of(rev):
    """The work item that wrote a commit, read off the trailing `(mg-xxxx)` of its
    message. Read from the MESSAGE, never from a mention -- a commit that NAMES mg-51f4
    is not a commit BY mg-51f4, and conflating the two is the whole of r2's finding."""
    body = git("log", "-1", "--format=%B", rev)
    hits = re.findall(r"\((mg-[0-9a-f]{4})\)\s*$", body.strip())
    return hits[-1] if hits else "?"


def banner(title):
    print("=" * 78)
    print(title)
    print("=" * 78)
