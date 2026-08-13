#!/usr/bin/env python3
"""mg-3902 — the negative control for `a2_pin_resolves.py`.

THE RULE THIS FILE EXISTS TO OBEY, and it is this ticket's own deliverable 2 turned on the
ticket: *a check that has never been shown to fail is not a check.*  mg-3902 was sent to make
mg-9bc2's staleness control go red and did (mutate a pinned ledger row → `DRIFT`, exit 1,
worklist exactly `8`).  Shipping a NEW control without doing the same thing to it would be
the audit reproducing the defect class it was sent to find, one file later.

Every mutation is applied to a COPY of the twin's text in memory.  The working tree is never
written.  Each row names the outcome it requires and the string that must appear.

THE BASELINE-ABSENCE GUARD IS mg-9876's, AND IT IS HERE BECAUSE IT IS NOT OPTIONAL.  A
mutation scores CAUGHT when its `expect` string is in the mutated report — a one-sided
membership test that cannot distinguish a string the mutation caused from a string the report
prints unconditionally.  `"8 9" in out` matched section 1's row listing for its whole life in
`code/rendered_twin_pin_9bc2/negative_control.py` for exactly that reason.  So every expect
string is checked against the UNMUTATED report first, and one already present is scored
UNFALSIFIABLE and takes this harness non-zero.

NOTHING BELOW NAMES A COMMIT AS A LITERAL.  The pinned commit is the one thing every
reconciliation moves, so a fixture that spells it out is a fixture with an expiry date — and
mg-2f44 demonstrated in this lineage that it can expire SILENTLY.  Each mutation reads the
commit out of the pin it was handed.

THE ORPHAN ROW IS THE ONE THING IN THIS SUITE THAT WRITES (mg-daba) — it and `a1_prerepair.py`'s
third row, which construct the SAME object — and it is worth knowing what it writes.  `c308368`'s defect — byte-identical STATE.md at a commit reachable only from a branch
nobody maintains — cannot be reproduced from anything already in this repository without
depending on `origin/polecat-p0e8c` surviving, which is the very property mg-3902 warned not
to rely on.  So the row CONSTRUCTS one: `git commit-tree` on the PINNED COMMIT'S OWN TREE
yields a commit whose STATE.md hashes to the pinned digest exactly, and which no ref points
at.  That is a loose object in `.git`, not a change to the working tree, and it is written
with fixed author and committer identity and timestamps, so its hash is the same on every run
and the object is created once and thereafter found rather than rewritten.  It is unreachable
by construction and `git gc` prunes it.

The row scores the world that MATTERS MOST here: the two halves of the acceptance criterion
in CONFLICT.  Byte-identity holds and main-ancestry does not, so a control that graded only
the digest would call it clean — which is what happened, on `main`, for the run that made
mg-3902 exist.
"""

import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
TWIN = os.path.join(ROOT, "docs", "state-of-the-wall.html")

sys.path.insert(0, HERE)
import a2_pin_resolves as A2  # noqa: E402

MUTATIONS = []


def mutation(name, expect):
    def deco(fn):
        MUTATIONS.append((name, expect, fn))
        return fn
    return deco


def _pinned_commit(text):
    m = re.search(r"\n  commit: ([0-9a-f]{7,40})", text)
    return m.group(1) if m else None


def _a_commit_with_a_different_state(pinned_sha):
    """A REAL commit whose STATE.md is not the pinned digest.  Derived, never typed."""
    rc, revs = A2.git("rev-list", "--max-count=60", "HEAD", "--", "STATE.md")
    if rc != 0:
        return None
    for rev in revs.split():
        rc2, blob = A2.git("show", f"{rev}:STATE.md", binary=True)
        if rc2 == 0 and hashlib.sha256(blob).hexdigest() != pinned_sha:
            return rev[:7]
    return None


@mutation("pin repointed at a REAL commit carrying a DIFFERENT STATE.md",
          "THE PIN NAMES ONE REVISION AND DIGESTS ANOTHER")
def m_wrong_real_commit(text):
    """The live defect this ticket found, reproduced on demand.

    `c308368` WAS this input, landed on main and green under all six of mg-9bc2's sections.
    """
    sha = re.search(r"\n  state-sha256: ([0-9a-f]{64})", text)
    pinned = _pinned_commit(text)
    if not sha or not pinned:
        return text
    wrong = _a_commit_with_a_different_state(sha.group(1))
    if wrong is None or wrong == pinned:
        return text
    # Both copies move together on purpose: mg-9bc2's section 6 already owns "the two copies
    # disagree", and a mutation that trips two controls at once proves nothing about either.
    return text.replace(pinned, wrong)


@mutation("pin names a commit THAT DOES NOT EXIST, consistently in both copies",
          "that commit DOES NOT EXIST in this repository")
def m_nonexistent_commit(text):
    """Consistent, machine-checkable, and entirely false — the input that scored CLEAN."""
    pinned = _pinned_commit(text)
    if not pinned:
        return text
    return text.replace(pinned, "0" * len(pinned))


@mutation("the pin's `commit:` field is deleted outright",
          "the pin carries no `commit:` field")
def m_drop_commit(text):
    return re.sub(r"\n  commit: [0-9a-f]{7,40}", "", text, count=1)


@mutation("the pin's `state-sha256` is deleted, leaving the commit unchecked",
          "the pin records no digest")
def m_drop_sha(text):
    return re.sub(r"\n  state-sha256: [0-9a-f]{64}", "", text, count=1)


@mutation("the whole STATE-PIN block is removed",
          "there is no provenance claim to resolve")
def m_no_pin(text):
    i = text.find(A2.PIN_START)
    j = text.find(A2.PIN_END) + len(A2.PIN_END)
    return text[:i] + text[j:]


def _an_orphan_commit_with_the_pinned_state(pinned):
    """A commit carrying the PINNED tree that no ref reaches.  Constructed, never found.

    `c308368` in a bottle: `git show <it>:STATE.md` hashes to the pin's digest, and no merge
    will ever bring it into `main`.  Fixed identity and dates make the hash deterministic, so
    this writes one loose object across all runs rather than one per run.
    """
    rc, tree = A2.git("rev-parse", "--verify", "--quiet", pinned + "^{tree}")
    if rc != 0:
        return None
    env = dict(os.environ,
               GIT_AUTHOR_NAME="mg-daba negative control",
               GIT_AUTHOR_EMAIL="mg-daba@invalid",
               GIT_AUTHOR_DATE="2000-01-01T00:00:00+0000",
               GIT_COMMITTER_NAME="mg-daba negative control",
               GIT_COMMITTER_EMAIL="mg-daba@invalid",
               GIT_COMMITTER_DATE="2000-01-01T00:00:00+0000")
    proc = subprocess.run(["git", "-C", ROOT, "commit-tree", tree, "-m",
                           "unreachable fixture for a3_negative_control.py"],
                          capture_output=True, text=True, env=env)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()[:7]


@mutation("pin repointed at an ORPHAN commit whose STATE.md is BYTE-IDENTICAL to the digest",
          "REACHABLE FROM NOTHING THIS REPOSITORY INTEGRATES")
def m_orphan_but_byte_identical(text):
    """The conflict case: byte-identity holds, main-ancestry does not.

    This is `c308368`'s shape and the reason the reachability half is graded at all.  Under
    the digest check alone this mutation is INDISTINGUISHABLE from a correct pin — which is
    not a prediction, it is what `main` reported for the run mg-3902 audited.
    """
    pinned = _pinned_commit(text)
    if not pinned:
        return text
    orphan = _an_orphan_commit_with_the_pinned_state(pinned)
    if orphan is None or orphan == pinned:
        return text
    return text.replace(pinned, orphan)


def reachability_truth_table(base):
    """All four branches of `classify_reachability`, each reached by a DERIVED input.

    THE TABLE ABOVE CAN ONLY WATCH THE GRADE FIRE.  A grade that fires is half of a control;
    the other half is the escape hatch that keeps it off correct work, and an escape hatch
    nobody has watched OPEN is exactly as unfalsifiable as a check nobody has watched fire.
    `in-flight` is that hatch, and there is no rot-proof fixture for it in a tree that equals
    `main`: an ancestor of HEAD that is not an ancestor of `main` exists only while a branch
    is unmerged, so a row that waited for one would pass or rot depending on the day it ran.
    It is reached here by handing the classifier a SUBSTITUTE integration ref — the pinned
    commit's own parent — against which the pinned commit is by construction not an ancestor
    while remaining one of HEAD.  The world is real; only the name `origin/main` is stood in
    for.

    `unknown` is the row that guards this suite's own kept defect: with no integration ref
    resolvable, the classifier must say it cannot tell, not `orphan`.

    Returns the number of holes.
    """
    print("=" * 92)
    print("THE CLASSIFIER'S FOUR BRANCHES — each reached by a derived input, none by a literal")
    print("=" * 92)
    print()

    pinned = _pinned_commit(base)
    rc, full = A2.git("rev-parse", "--verify", "--quiet", (pinned or "HEAD") + "^{commit}")
    if rc != 0:
        print("SETUP FAILED: the pinned commit does not resolve, so no branch below can be")
        print("              reached.  This is a hole, not a pass.")
        return 1

    orphan = _an_orphan_commit_with_the_pinned_state(pinned)
    cases = [
        ("integration", "the real integration refs", full, A2.INTEGRATION_REFS),
        ("in-flight", "a substitute integration ref: the pinned commit's own parent",
         full, (pinned + "~1",)),
        ("unknown", "an integration ref that resolves nowhere", full,
         ("refs/heads/no-such-integration-branch-mg-daba",)),
        ("orphan", "the real integration refs, against the constructed orphan",
         orphan, A2.INTEGRATION_REFS),
    ]

    holes = 0
    width = max(len(c[1]) for c in cases)
    print(f"{'want'.ljust(12)}  {'input'.ljust(width)}  got           detail")
    print("-" * 92)
    for want, label, rev, refs in cases:
        if rev is None:
            print(f"{want.ljust(12)}  {label.ljust(width)}  SETUP FAILED  the fixture could "
                  f"not be constructed")
            holes += 1
            continue
        got, detail = A2.classify_reachability(rev, refs)
        if got != want:
            holes += 1
        print(f"{want.ljust(12)}  {label.ljust(width)}  {got:<12}  {detail}")
    print()
    if holes:
        print(f"{len(cases) - holes} of {len(cases)} branches reached; {holes} hole(s).")
    else:
        print(f"All {len(cases)} branches reached, including the two that must NOT grade.")
    print()
    return holes


def main():
    base = open(TWIN, encoding="utf-8").read()

    print("=" * 92)
    print("mg-3902 — NEGATIVE CONTROL for a2_pin_resolves.py")
    print("=" * 92)
    print()

    rc, _ = A2.git("rev-parse", "--git-dir")
    if rc != 0:
        # NOT A PASS, and it must not be silent.  Without history the control under test
        # reports NOT APPLICABLE by design, so every row below would be vacuous.
        print("REFUSED: no git repository at ROOT, so a2_pin_resolves.py reports NOT")
        print("         APPLICABLE and none of these mutations can be demonstrated.  This is")
        print("         reported rather than scored, and it is NOT a green: it is a run that")
        print("         took no coverage at all.")
        return 0

    base_code, base_lines = A2.report(base)
    base_report = "\n".join(base_lines)
    if base_code != 0:
        print(f"REFUSED: the UNMUTATED twin is already at exit {base_code}.  Every row below")
        print("         would be scored against a baseline that is itself red, so 'the")
        print("         mutation caused it' would be unsupported.  Fix the pin first.")
        print()
        print(base_report)
        return 2

    rows, holes = [], 0
    for name, expect, fn in MUTATIONS:
        mutated = fn(base)
        if mutated == base:
            rows.append((name, "SETUP FAILED", "mutation was a no-op — the fixture has rotted"))
            holes += 1
            continue
        if expect in base_report:
            rows.append((name, "UNFALSIFIABLE",
                         f"{expect!r} is in the UNMUTATED report too, so this row could not "
                         f"have failed"))
            holes += 1
            continue
        code, lines = A2.report(mutated)
        text = "\n".join(lines)
        ok = code == 2 and expect in text
        rows.append((name, "CAUGHT" if ok else "HOLE",
                     f"exit {code}; looked for {expect!r} (absent from the baseline)"))
        if not ok:
            holes += 1

    width = max(len(r[0]) for r in rows)
    print(f"{'mutation'.ljust(width)}  verdict        detail")
    print("-" * 92)
    for name, verdict, detail in rows:
        print(f"{name.ljust(width)}  {verdict:<13}  {detail}")
    print()
    print(f"{len(rows) - holes} of {len(rows)} caught; {holes} hole(s).")
    print()

    holes += reachability_truth_table(base)

    if holes:
        print("A HOLE IS A FINDING, NOT A TEST FAILURE TO SUPPRESS — it is a way the pin can")
        print("lie that this control does not see.  Write it down before silencing it.")
        return 1
    print("Every mutation was caught, and the unmutated twin is clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
