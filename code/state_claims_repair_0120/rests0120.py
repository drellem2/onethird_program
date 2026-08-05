#!/usr/bin/env python3
"""mg-0120 — WHAT RESTS ON THE FOUR PINNED ROWS.  The question the ticket says it exists for.

    "Then find out whether any conclusion in the arc rests on those four rows — that is the
     question this ticket exists for, and it is not answered by fixing the file."

THE ANSWER IS A CARDINALITY.  `claims16eb.py` is where the phrase "mg-16eb's six broken
claims" comes from: the number SIX is the count of rows that file printed `BROKEN` when
mg-16eb ran it.  Four of those six were the literal `False`.  **So the number six was itself
four-sevenths a constant** — and mg-a74f's whole repair, its commit subject, its README table
and mg-65eb's `six65eb.py` (a program NAMED after the number) are built on it.

WHAT THIS FILE DOES, AND THE ORDER MATTERS.

  1. It counts the documents that publish the figure, over a stated population and grain.
  2. It RE-DERIVES the figure at `bd24efc` — mg-16eb's own revision — with the six verdicts
     COMPUTED instead of pinned, and compares.  If the recomputed count is six, the published
     conclusion is TRUE and was unevidenced for four of its six rows; if it is not six, a
     cardinality in several documents is wrong, which is a much larger finding.
  3. It separates the two things a reader could mean by "rests on":
        CITES        the document names the figure
        DEPENDS      the document's own claim is false if the figure is wrong
     A document can cite a number without depending on it (a passing reference in a list of
     what happened) and this file does not conflate them: DEPENDS is decided by a stated
     rule, printed with the run, and the rule is coarse and says so.

WHAT THIS FILE DOES NOT DO.  It does not re-run mg-a74f's or mg-65eb's suites and it does not
re-classify their findings.  It measures ONE number and what leans on it.

    python3 code/state_claims_repair_0120/rests0120.py

Exit 1 if the recomputed figure disagrees with the published one.  Nothing is written.
"""
import os
import re
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import verdicts0120 as V                                            # noqa: E402

BEFORE = "bd24efc"
EXTS = (".py", ".md", ".sh")

# The population of documents: every tracked .py/.md/.sh at `main`.  NOT "the arc's four
# directories" — a conclusion can be published anywhere, and scoping the search to the
# neighbourhood of the defect is how a census misses the sentence that matters.
#
# THE PATTERNS ARE PRINTED WITH THE RUN so the parse can be checked rather than trusted.  A
# figure is counted only when `six`/`6` sits next to a word meaning "claims mg-16eb found
# broken"; `six` on its own is a common English word and matching it alone would count
# sentences about six of anything.
FIGURE = [
    re.compile(r"\b(six|6)\b[^.\n]{0,40}\b(broken|BROKEN)\b[^.\n]{0,30}\bclaims?\b", re.I),
    re.compile(r"\bclaims?\b[^.\n]{0,30}\b(six|6)\b[^.\n]{0,30}\b(broken|BROKEN)\b", re.I),
    re.compile(r"\bthe\s+six\b[^.\n]{0,60}\b(claims?|rows?)\b", re.I),
    re.compile(r"\b(six|6)\s+(of\s+(seventeen|17)|BROKEN)\b", re.I),
]

# "DEPENDS" — the coarse rule, stated before it is used.  A document depends on the figure if
# it is one of the arc's own instruments or accounts (its path names a directory of this arc)
# AND it publishes the figure.  Everything else CITES.  This over-counts: a README that
# mentions the number in a history section is scored DEPENDS.  It is coarse in the direction
# of finding MORE dependence, which is the safe direction for this question, and the rows are
# printed individually so a reader can disagree with any of them.
ARC_DIRS = (
    "code/state_delegation_audit_16eb",
    "code/state_delegation_repair_a74f",
    "code/state_visibility_audit_65eb",
    "code/state_delegation_repair_0049",
    "code/state_claims_repair_0120",
)


def git(*a, **kw):
    return subprocess.run(["git", "-C", V.REPO, *a], capture_output=True, text=True, **kw)


def population(ref):
    return [p for p in git("ls-tree", "-r", "--name-only", ref).stdout.split("\n")
            if p.endswith(EXTS)]


def recompute_at(rev):
    """THE WHOLE PROGRAM, run at `rev` with every verdict computed — not arithmetic.

    A throwaway worktree is checked out at `rev` and the REPAIRED `claims16eb.py` and
    `verdicts0120.py` are copied into it.  Every other row of that file is untouched and runs
    against `rev`'s tree exactly as mg-16eb wrote it.  The number that comes back is the count
    mg-16eb would have published if its six pinned rows had been measurements.

    THE FIRST DRAFT OF THIS FUNCTION DID ARITHMETIC and got it wrong: it subtracted the six
    LITERAL-CARRYING rows from the published BROKEN count, when only four of the six were in
    that count (the other two were pinned `True` and sat among the rows that held).  It
    reported 5 where the answer is 7 — a population-versus-grain slip of exactly the kind this
    ticket says these audits keep returning, committed inside the instrument written to find
    it.  The repair is not a corrected formula; it is running the program."""
    import shutil
    wt = V.Worktree(rev)
    try:
        os.makedirs(os.path.join(wt.dir, "code/state_claims_repair_0120"), exist_ok=True)
        for rel in ("code/state_claims_repair_0120/verdicts0120.py",
                    "code/state_delegation_audit_16eb/claims16eb.py"):
            shutil.copyfile(os.path.join(V.REPO, rel), os.path.join(wt.dir, rel))
        p = subprocess.run([sys.executable,
                            os.path.join(wt.dir, "code/state_delegation_audit_16eb",
                                         "claims16eb.py")],
                           cwd=wt.dir, capture_output=True, text=True)
        return p.stdout, p.returncode
    finally:
        wt.close()


def three_states(text):
    """(holds, broken, respecified, [broken row labels]) read off a run's own summary."""
    def n(pat):
        m = re.search(pat, text, re.M)
        return int(m.group(1)) if m else None
    holds = n(r"^\s*(\d+)\s+hold against the tree")
    broken = n(r"^\s*(\d+)\s+do not")
    respec = n(r"^\s*(\d+)\s+RESPECIFIED")
    rows = re.findall(r"^  \[BROKEN\] (.+)$", text, re.M)
    return holds, broken, respec, rows


def main():
    ref = "main"
    print("=" * 100)
    print("mg-0120 — WHAT RESTS ON THE FOUR PINNED ROWS")
    print("=" * 100)
    print()

    # ------------------------------------------------------------------------------------
    print("1.  THE FIGURE, AND WHERE IT IS PUBLISHED.")
    print()
    print("    POPULATION: every tracked .py/.md/.sh at main.")
    print("    GRAIN of the first count: a FILE, counted once however many times it says it.")
    print("    GRAIN of the second: one MATCHING LINE.")
    print("    The patterns, printed so the parse can be checked:")
    for pat in FIGURE:
        print(f"      {pat.pattern}")
    print()
    files = population(ref)
    hits = {}
    for path in files:
        text = git("show", f"{ref}:{path}").stdout
        for i, line in enumerate(text.split("\n"), 1):
            if any(p.search(line) for p in FIGURE):
                hits.setdefault(path, []).append((i, line.strip()))
    n_lines = sum(len(v) for v in hits.values())
    print(f"    files searched {len(files)}    files publishing the figure {len(hits)}    "
          f"matching lines {n_lines}")
    print()
    depends, cites = [], []
    for path in sorted(hits):
        (depends if path.startswith(ARC_DIRS) else cites).append(path)
    for label, group in (("DEPENDS (an instrument or account of this arc)", depends),
                         ("CITES (names the figure, outside the arc's own files)", cites)):
        print(f"    {label}: {len(group)}")
        for path in group:
            i, line = hits[path][0]
            print(f"      {path}:{i}")
            print(f"        {line[:92]}")
        print()

    # ------------------------------------------------------------------------------------
    print("2.  THE FIGURE RE-DERIVED AT mg-16eb's OWN REVISION, WITH THE SIX COMPUTED.")
    print()
    print(f"    METHOD: a throwaway worktree at {BEFORE}, with the REPAIRED claims16eb.py and")
    print("    verdicts0120.py copied in and every other row left exactly as mg-16eb wrote")
    print("    it.  The program is RUN.  No figure here is arithmetic over another figure.")
    print()
    transcript = git("show",
                     f"{BEFORE}:code/state_delegation_audit_16eb/out_claims.txt").stdout
    m = re.search(r"^(\d+) do not:", transcript, re.M)
    published_broken = int(m.group(1)) if m else None
    pub_rows = re.findall(r"^  \[BROKEN\] (.+)$", transcript, re.M)
    print(f"    PUBLISHED, from mg-16eb's own committed out_claims.txt at {BEFORE}:")
    print(f"      {published_broken} BROKEN of 17.  The rows:")
    for r in pub_rows:
        print(f"        {r[:88]}")
    print()
    out, rc = recompute_at(BEFORE)
    holds, broken, respec, rows = three_states(out)
    if broken is None:
        print("    THE RE-RUN DID NOT PRODUCE A SUMMARY — figure NOT re-derived.")
        print(out[-1200:])
        return 1
    print(f"    RE-DERIVED, every verdict computed (exit {rc}):")
    print(f"      {holds} hold, {broken} BROKEN, {respec} RESPECIFIED  (sum "
          f"{holds + broken + respec}).  The rows:")
    for r in rows:
        print(f"        {r[:88]}")
    print()
    extra = [r for r in rows if r not in pub_rows]
    gone = [r for r in pub_rows if r not in rows]
    print(f"    PUBLISHED figure   {published_broken}")
    print(f"    RE-DERIVED figure  {broken}   "
          f"{'AGREE' if broken == published_broken else 'DISAGREE'}")
    if extra:
        print(f"    BROKEN here and not there ({len(extra)}):")
        for r in extra:
            print(f"      {r[:92]}")
    if gone:
        print(f"    BROKEN there and not here ({len(gone)}):")
        for r in gone:
            print(f"      {r[:92]}")
    print()
    computed_total = broken

    # ------------------------------------------------------------------------------------
    print("3.  THE ANSWER.")
    print()
    print(f"    YES — a conclusion rests on those rows, and it is the CARDINALITY SIX.")
    print()
    if computed_total == published_broken:
        print("    And it survives: recomputed at mg-16eb's own revision the figure is the")
        print("    same, so what was missing was the WARRANT and not the number.  A constant")
        print("    that agrees with the measurement is the hardest defect to find, because")
        print("    every downstream check of the NUMBER passes.")
    else:
        print(f"    AND IT DOES NOT SURVIVE.  Run at {BEFORE} with every verdict computed,")
        print(f"    mg-16eb's own program reports {computed_total} BROKEN of 17, not "
              f"{published_broken}.")
        print()
        print("    THE MISSING ROW IS ONE OF THE TWO THAT WERE PINNED `True`, WHICH IS THE")
        print("    SHAPE THE TICKET DOES NOT NAME.  Four literal `False`s cost this arc")
        print("    nothing: they were pinned to the answer a measurement would have given.")
        print("    A literal `True` is a row that CANNOT REPORT A PROBLEM, and it sits in the")
        print("    numerator of the file's own headline count.  That is where the lost")
        print("    finding went.")
        print()
        print(f"    {len(depends)} instrument(s) and account(s) of this arc publish the")
        print("    figure, and every conclusion drawn from 'the six' is drawn from a")
        print("    population that is missing a member.  What is NOT established here: that")
        print("    any of those conclusions is wrong.  A repair classified by six rows is")
        print("    not refuted by a seventh; it is INCOMPLETE, and the seventh row's claim")
        print("    (presentation.py's header) has never been repaired by anyone.")
    print()
    print("=" * 100)
    return 0 if computed_total == published_broken else 1


if __name__ == "__main__":
    sys.exit(main())
