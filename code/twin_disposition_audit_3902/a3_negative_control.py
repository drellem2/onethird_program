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
    if holes:
        print("A HOLE IS A FINDING, NOT A TEST FAILURE TO SUPPRESS — it is a way the pin can")
        print("lie that this control does not see.  Write it down before silencing it.")
        return 1
    print("Every mutation was caught, and the unmutated twin is clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
